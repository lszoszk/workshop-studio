I need to build one complete HTML page, keeping it to a reasonable length. The data arrives as WORKSHOP_DATA.pdf_text, which may be an array of records or an object, so I'll handle both cases.

Next I'm sorting the records by page and splitting each page's text into lines, tagging every line with its page and position. Header lines get matched against the symbol, and footers are trimmed from the end, dropping blanks, the GE. marker, date stamps, and small bare numbers until real text is reached.

I'm now working out how the stream gets parsed: each line keeps its page and position, and blank lines stay in so heading detection can skip past them. For cover handling, everything before the first heading or paragraph start counts as cover, and the paragraph-start lines get indexed up front so the walk can find where the body begins.

I'm setting up the walk over the lines: blanks get skipped, and a label like "I." or "A." marks a heading whose text runs until the next label or paragraph number. I'm checking that a page break can't slip junk into a heading.

I'm handling heading text now: a line after a label like "I." joins the heading until the next label or paragraph number, with blank lines skipped. I'm weighing whether to cap how many lines a heading can collect, since a footnote near a page bottom could otherwise get pulled into it.

I'm now defining how headings get their path: a Roman label resets the part, a letter label sets a subsection under it, and unlabelled headings sit beneath the most recent label, so each heading knows where it belongs.

I'm checking whether a short line after a paragraph's end could be a heading, and I'm weighing whether to accept only the immediately following line or to skip blank lines before the next paragraph number.

I'm checking the rule for spotting unlabelled headings: whether a short line should count only when the very next line is a paragraph number, or whether blank lines in between are fine too.

I'm checking the rule for spotting a two-line heading: a candidate line that is followed by a paragraph number counts as a heading only if the line before it also passes the same test, and I'm weighing whether the previous line belongs to the current paragraph rather than an existing heading.

I'm still checking how a two-line heading gets joined: if the line before a candidate already sits in the current paragraph and passes the same test, I'd pull it out and merge the two. A wrapped line that starts lowercase would fail that test, so it stays with the paragraph.

I'm checking whether a footnote line that ends a page could be mistaken for an unlabelled heading when the next page opens with a paragraph number. Footnote text usually ends with a period or a digit, so the test should mostly hold, but I'll also skip any candidate that falls in a suspect region near a page break.

I'm settling on the rule for suspect regions: once a line near a page break looks like footnote text, I'll flag that page, so candidate headings there don't get pulled out. The flag resets when the page changes.

I'm checking whether a heading candidate falls inside a suspect footnote region at the bottom of a page: if it does, it can't be a heading. Footnote blocks run to the page's end, so a candidate on the next page is fine, and I'm only applying this suspect check to paragraph lines.

I'm treating a line as a suspect footnote when it's a bare number or starts with a number followed by a capital letter, a quotation mark, or a document symbol like "E/". Once a page has a suspect line, I'm marking the rest of that page's lines as suspect too, so the flag resets when the page changes. Then a heading candidate inside that suspect area can't be pulled out, while one on the next page still can. I'm also checking that a real paragraph line starting with a number, like "17 Sustainable", doesn't get caught by that test.

I'm settling how suspect lines are flagged: a line starting with a number and a space, a bare number, an asterisk, or a paragraph running past 300 words. The paragraph's first line after its number is taken as text and not checked.

I'm now checking whether the suspect flag should carry through the rest of the page, since a footnote block always runs to the page foot, and I'm settling that a paragraph start after a footnote on the same page can't happen, so the flag only needs resetting when the page changes.

I'm checking whether footnote lines at the bottom of a page could be mistaken for headings, and I'm settling on flagging any page where a suspect footnote line appears so candidates there don't get pulled out.

I'm settling how headers and footers get handled: the first nonblank line counts as the header only if it matches the symbol, and if it doesn't I'll warn but keep the line as body text. Each line will carry its page and a kind tag, and at the end I'll check that the per-kind counts add up to the total nonblank lines, with no unclassified leftovers.

I'm settling the footer pass: working back from the end of each page, blank lines get skipped, and lines starting with a GE. document reference, a run of six-digit codes, or a bare page number count as footers, stopping at the first line that doesn't match. Bare numbers that don't match the page get logged, since a footnote number at the foot could look the same, and I'm still checking whether the last footnote might be misread.

I'm settling the labelled heading collection: after the label line, I'll gather the following nonblank lines until I hit another label or a paragraph start, capped at four lines so a wrapped "A." heading joins correctly.

Now I'm working out how to extract the first few words of each heading, dropping any digits that are glued onto the end of a word or punctuation mark.

I'm working out how to clean the first few words of each heading: trailing digits glued to a word or punctuation mark get stripped, while plain numbers like "Article 2" stay put. I'm checking the pattern against cases like "Covenant1" and codes such as "E/C.12/GC/27", which should be left alone.

I'm now handling the first few words of each heading, stripping digits that are glued onto the end of a word or punctuation mark. I'm limiting that cut so that tokens like "C.12" don't get mangled, and I'm still thinking through how to walk the token stream so I get six usable words even after the removals.

I'm settling the rule for dropping stray digits that follow punctuation in the first words, and I'm keeping a number when nothing precedes it. I'm also normalizing curly quotes and dashes before comparing text.

I'm reconciling the normalized first-words string with the found output, and checking that both come to six words. Next I'm flagging the definition of suspect lines and counting them per page within the paragraph totals. I also want a check-panel line tallying hyphens at line ends, noting that no joining happens there. For numbering, I'll confirm the paragraph numbers run sequentially from 1 and report any duplicates or gaps by page.

I'm laying out the checks list, each with an id, title, expected and actual values, and a status, plus a button that filters the paragraphs table to the rows a check concerns. Then I'll move on to tab 01.

Now I'm working out how the checks list will be laid out and how each check links to its rows, with tab 02 showing only the paragraphs a check concerns. I'm keeping the number of clickable controls on each view low, opening one heading panel at a time, and treating the failing-checks tally as a count of checks marked fail.

Now I'm laying out the checks list: each one gets an id, a title, expected and actual values, and a status, and checks that flag something count as info rather than failures. The header will show how many checks pass, going red if any fail or amber-neutral if some haven't run yet. I'll start with the paragraph count as check 1.

I'm listing the remaining checks: the numbering, first words, flagged and suspect lines, headers and footers, headings, nothing lost, and the export round trip. For headers and footers, I'll expect the symbol on every page's first line, and page numbers on every page except the first, so the count should be pages minus one.

Now I'm settling the export format: JSON records carrying the symbol, paragraph number, section, page range, text, flags, the first-words match, citation, and document link, plus a text_lines field with the lines joined by pipes. Filenames will swap slashes for hyphens, so the symbol becomes something like E-C.12-GC-27.

I'm building the Markdown export next: headings as section markers, each paragraph with its number in bold, and a flag note where needed. The front matter gets today's date and the document's URL, and the Markdown then goes out with the JSON export, skipped entirely when there are no paragraphs.

I'm laying out the table: a number button in the first cell, with the whole row toggling the detail row, plus a keyboard-friendly button for expansion.

I'm now working out how each expanded paragraph will show its text, marking the suspect lines inside the running text and placing the reference words beside the found ones. There's also a toggle to reveal the raw PDF lines, with a page marker wherever a new page begins.

I'm setting up the state for the page: which tab is open, which paragraphs are expanded, and an optional row filter. Tile one will compare the paragraphs found against the count the document reports, and tile two will count first-word matches against the reference.

Now I'm setting up the flagged-paragraphs table, counting the pages that contain suspect lines and long paragraphs.

I'm laying out the rest of the page: a header with the symbol, title, adoption date, page count and source, plus a status note on the right that shows how many paragraphs are flagged. The main area will use a grid with a 260px side rail next to the content, stacking vertically below 800px. The footer will carry the source, the build time and a short statement, and each check in the checks panel will be its own block.

I'm laying out the check list next: each check gets a title, an expected value, a found value, and a status, plus a button that jumps to the matching rows on the paragraphs tab where that applies. The nothing-lost check will tally cover, header, heading, paragraph, footer, and unclassified lines against an independent raw count, passing only when everything adds up and nothing is unclassified.

Now I'm sorting the records by page and parsing the text into lines, then building the paragraph and checks lists.

Now I'm stepping through each page's lines, first checking whether the first line matches the symbol so it can be tagged as a header.

Now I'm stepping through each page's lines to pick out the footers, which are the GE symbol lines, the rows of six-digit codes, and bare numbers. I'm checking whether a bare number matches the page number, counting it if so and recording it as an oddity if not, then gathering everything between the header and the footers into one stream.

I'm walking through the lines with a cursor, tracking the current paragraph, part, and sub-heading, and classifying each line as a paragraph start, a label, or a continuation.

I'm finishing up the paragraph-classification pass, which tags header and footer lines, then walks the remaining lines with a cursor to track the current paragraph, part, and sub-heading. I'm adding a small helper to find the next non-blank line and setting up a way to tell which section a line belongs to.

Now I'm handling the labelled headings: each one gathers up to four following lines as its title, and any paragraph still open gets closed off.

Now I'm sorting out how labelled headings split the stream: a Roman numeral opens a new part and resets the subsection and sub-heading, while a letter opens a subsection under the current part. A heading closes whatever paragraph was open, so any line after it without a paragraph start is left unclassified and will show up red. Only lines before the first heading or paragraph start count as cover.

I'm now writing the paragraph-start branch of the parser, which matches a number like "12." or "12. text" and opens a new paragraph record that takes the current section and the page.

I'm now checking each unlabelled line to see whether it should join the open paragraph or start a heading, and I'm handling the case where the previous line was a paragraph line that could be a continuation.

I'm working out how to recognise unlabelled heading lines: if the line before a paragraph-like heading has no suspect flag and reads as a heading, I'll merge it with the current line into one title and reclassify the earlier line.

I'm now writing the code that pushes each non-heading line onto the open paragraph, and I'm checking whether it's flagged as suspect by page.

Next I'm adding a per-page suspect flag: any line matching a suspect trigger turns on flagging for the rest of that page, and every line on that page then inherits the flag.

Still writing the line-push logic, adding each line to the open paragraph with its page and suspect flag.

Now I'm finalizing each paragraph: joining its lines into one text, working out its start and end pages, and collecting the suspect lines and word count to decide whether it gets flagged.

Now I'm working out how to flag suspect lines: a bare number, a line starting with an asterisk, or a number followed by a space, and every later line on that page inherits the flag. Each paragraph then gets its text joined and its page range set, and it is flagged if it has suspect lines or runs over 300 words.

I'm working out the suspect-flag regex next: a bare number or an asterisk-led line, plus a number followed by a capitalised word, with a rough heading test that keeps titles short and skips lines ending in punctuation or a digit.

Now I'm writing the UI rendering code, starting with the state object that tracks the active tab.

I'm wiring up the tab state and rendering the two panels, with the paragraph table filled in once and rebuilt only when the filter changes.

I'm setting up the page header with the title, a status badge, and a meta line, then splitting the layout into a summary rail and a main column with two tabs.

Now I'm laying out the tab panels: the first holds the result tiles, the mismatch list, and two accordions for checks and flagged paragraphs, while the second gets a paragraph table that is filled once and rebuilt only when the filter changes.

I'm wiring the status tiles and the flagged-paragraphs table, with the four summary figures showing how each is computed.

I'm building the paragraph table now, with each row showing a short preview of the paragraph text cut at a word boundary, and I'm tracking which headings come before each paragraph so they can be listed alongside it.

I'm writing the detail row for each paragraph, with its path, the marked text, and the reference-versus-found first words, plus a copy button for the citation.

I'm now wiring the per-paragraph detail row: the path, the marked-up text with consecutive suspect lines grouped into a single highlight, the reference versus found first words, and buttons to copy the citation or show the raw PDF lines. The copy button will fall back to a hidden textarea if the clipboard API isn't available.

Now I'm wiring the click handlers: a jump-to-paragraph action that clears any active filter, switches to the second tab, makes sure the row exists, expands it, and moves focus to its button. A check that lists specific paragraphs will set a filter, switch tabs, and show a note above the table with a link to clear it. I'm also adding a download helper that wraps the content in a Blob and triggers a click on a link.

Now I'm defining the two-tab page's check list: a count check against the reference, a numbering check that looks for duplicates and gaps in the paragraph sequence, and a summary of how many checks pass, fail, or are noted.

I'm now defining the checks for the second panel. The first compares the paragraph count with the reference. The second looks for duplicate numbers and gaps in the sequence, listing the affected paragraphs. The third compares first words against the reference and lists any mismatches. The rest are notes covering flagged paragraphs, suspect lines, headers and footers, headings, whether anything was lost, and a round-trip check.

Now I'm writing the Markdown export: a YAML front matter block with the title, symbol, adoption date, source URL, extraction date, and paragraph count, followed by the paragraphs themselves.

Still writing the Markdown export, which starts with a YAML front matter block holding the title, symbol, adoption date, source, extraction date, and paragraph counts.

Now I'm finishing the flag notes: footnotes aren't separated, so any suspect lines in a paragraph are counted, and a paragraph that is only flagged for length gets a plain note saying so. Then I'm setting up the section label from the nearest heading and disabling exports when there are no paragraphs.

Now I'm writing the first-words helper, normalizing quotes and dashes and collapsing whitespace before comparing text.

I'm writing the first-words helper now: it goes through the tokens of a paragraph, skipping stray page numbers that follow sentence punctuation, and strips trailing digits from words that look like footnote markers, stopping after six words.

I'm checking the first-words helper: a bare number after sentence-ending punctuation gets dropped as a stray page marker, while abbreviations like "No." keep it, and a trailing footnote digit is stripped from words that aren't slash-separated references.

Now I'm writing out the Markdown export and the flag notes, along with the first-words helper that skips stray page numbers and strips footnote digits.

Now I'm setting the progress bar width from found over reference, coloring it red when the counts don't match, and getting the final JavaScript ready while keeping the escaping careful.

