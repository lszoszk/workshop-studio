I need to put together one complete HTML file, keeping it under about 1500 lines and working through the code carefully. I'll follow the plan's constraints, including the cap of seven clickable items per view, along with its header, tabs, and rail counts. The data will come from the workshop records, and I'm checking the metadata fields as I go.

I'm sketching the page layout: a header with the label, title and status, a four-tab navigation bar, and a main area with a side rail that hides on the Draft tab. The rail will hold the filter controls, search, and document selectors. I'm also checking the click count per view, since the plan caps it at about seven, and the Clear all button only needs to show when filters are active.

I'm mapping the committee codes to their full names, with a fallback to the bare code for any that aren't in the map. Next I'm precomputing each record's normalized text, its footnote marker count, and a cleaned version with the markers stripped out.

I'm working out how to flag records that span more than one committee. A symbol can name two bodies, like the CMW/CERD pairing, so I'm checking whether it holds more than one committee code to mark a record as joint. I'm also looking at how the leading paragraph number and the pinpoint are pulled out of each record.

Next I'm working out how to count the committee codes in each symbol, so I can tell whether a record is joint. I'll normalize "CAT/OP" to "CAT-OP" first, then match the codes in one pass, with the longer names listed ahead of their prefixes so CAT-OP isn't read as CAT.

I'm working out the joint flag by counting the distinct committee codes in each symbol, so a record with two symbol codes counts as joint. A symbol with no codes, like A/48/18, just uses its own committee.

For the citation, I'll pair the symbol with the pinpoint, and for shared records I'll add the committee and the document name.

I'm working out how the pinpoint for each record gets built: paragraph zero becomes "preamble," a leading lettered marker like "(b)" becomes "subpara. (b)," and everything else reads as "para." followed by the number.

I'm now checking how the duplicate pinpoints should be keyed: I'll combine the symbol, the pinpoint, and the title so that lettered subparagraphs don't get mistaken for numbered paragraphs with the same digits.

I'm settling on the quotation format now: the shown text with the footnote markers removed, and when the leading paragraph number matches the pinpoint, I'll drop that number from the front so it isn't repeated. The citation goes after the quoted text.

I'm now settling how the query parser tokenizes input: it skips whitespace, treats any of the double-quote characters as opening a phrase that must be closed, and splits parentheses into their own tokens. Any other run of non-space characters becomes a word.

I'm handling the query parser's word rules now: a hyphen at the start of a token means NOT, and I'm checking how a hyphenated word like "ill-treatment" stays whole while I scan it.

I'm checking the query parser's handling of a straight quote, apostrophe, or hyphen, and whether the normalized match should also count curly forms as hits, which means comparing against the raw stored text.

I'm building a strict match mode alongside the normal one, so a hit only counts if the literal characters in the query appear in the shown text, without any curly-quote or dash normalization. That means evaluating the same Boolean tree a second time with regexes built from the raw lowercased terms instead of the normalized ones.

I'm working out how the phrase tokens get built: each word in a quoted phrase gets escaped, and the words are joined with a whitespace gap so they match across line breaks. I'm also deciding whether a trailing asterisk on a word inside a phrase should work the same way as it does for single words.

I'm writing out the query parser's expression rules, starting with OR as the loosest operator and building each combination into a tree node as I go.

I'm writing out the parser's precedence chain: NOT binds tightest, then AND, then OR, with parentheses taking priority, and I'm listing the syntax errors to report, like an AND with no left operand or an unmatched closing paren. I'll echo the parsed query back in plain English, so a single word becomes "the word…", a phrase gets quoted, and the operators read as "and" and "or".

I'm settling on how the parser turns the expression into a tree, with the phrase and word terms as leaves and "and" and "or" joining them, plus a "not" that applies to a single term. For the echo, I'll describe a word plainly and a phrase in curly quotes, and describe a right-side "not" as "but not," which keeps the plain-English readback readable.

Next I'm defining the evaluation step, with a helper that counts the term leaves in the tree and another that collects the positive terms, skipping any that sit under an odd number of NOTs. If there are no positive terms, the query is NOT-only, and the echo says so.

I'm now checking how the evaluator runs each term: a non-global regex per term, compiled once with the `u` flag, so the test has no state carried between records. I'll cache the query-matching records, then re-filter by committee, years, and document whenever a filter changes, and count the per-committee checkbox numbers against the filter that's ignored.

I'm now going over how the bracketed checkbox counts should work: I'll count the records that pass the query, year, and document filters, ignoring committee ticks, and check that the bracketed totals add up to that set's size plus its extra joint committee counts.

I'm weighing whether the committee bar chart should count each joint record toward every committee it belongs to, even when the committee filter has hidden one of them. That would make a bar show hits for a committee that isn't ticked, and it would also let one click on a bar collapse the whole chart down to a single column.

I'm weighing whether the bracketed checkbox counts and the bar chart should cover the same set. The counts could run over the paragraphs that pass the query and year and document filters, so a user can see what ticking a committee would add, while the chart and table stay on the current hits.

I'm checking the totals: the checkbox brackets should add up to the base set's size plus its joint extras, while the chart bars should match the hits plus their joint extras. Clearing all filters will reset the chips and the query.

I'm setting the year inputs to take numbers as typed, falling back to the default when a field is empty. The document dropdown will group titles by committee, using each distinct title once, and sort them by year and then by short title. The committee list in the rail stays narrow and collapsed by default under its filter heading.

I'm wiring up the search help list so it appears when the box is empty and focused, and an arrow key can open it and move between the three example buttons. Clicking an example fills the box and runs the search, while Escape or leaving the wrapper closes it.

I'm wiring the help panel to close when focus leaves the wrapper, while clicks on it keep focus in the input. On load the input gets focus, so the help opens right away when the box is empty. Search runs from the button or Enter, and an empty applied query shows all paragraphs.

Next I'm adding a message under the box for parse errors and deciding what the counts show when nothing matches, leaning toward plain zeros beside the error. Then I'm turning to the overview tab, where a horizontal bar chart sits beside its table, with the bars sorted from largest to smallest. Since the datalabels plugin isn't available, I'm writing a small inline plugin that draws each value at the end of its bar.

Still writing the chart's value labels and axis settings...

Still wiring up the overview chart: I'm planning to redraw it on each render and keep the bars sorted, with the chart sized to the number of committees.

Now I'm working out the overview chart's click and hover behavior, with a tick on a bar selecting that committee alone. When no paragraphs match, the chart gets swapped for a "No paragraphs match" message. I'm also planning a note that joint General Comments count under both committees, so the bars can sum to more than the hits.

I'm laying out the paragraphs tab next: a live summary line, the ordering control, and a results list where each row's heading is itself the toggle button, with the symbol link kept as a separate element beside it.

I'm laying out how each row opens: a click on the article toggles it unless the click lands on a link, button, or the detail area, or the user has selected text. Only the open row shows its buttons, and the "show as stored" and "show the full paragraph" controls live there.

Now I'm working out how the row's text gets trimmed: the display function picks the stored or shown text, and if it runs past about 700 characters and isn't in full view, it cuts at the last word boundary and adds an ellipsis.

Now I'm looking at how to highlight matched terms in the shown text: I'll build a regex from the positive search words, with each character swapped for a class that also matches curly quotes and dashes.

I'm normalizing the query words to lowercase with quotes unified, and I'm noting that the highlight pattern has to match across removed footnote marks the same way the search does.

I'm looking at how the highlight function will escape HTML and wrap each match in a mark tag as it walks through the text. The one edge case is a term made only of asterisks, which could produce a zero-length match, so I'm weighing whether to reject such terms as an error.

I'm adding a guard so a term made only of asterisks gets rejected with a parse error, and I'm making sure the highlight loop steps past any zero-length match. The combined highlight pattern will put longer phrases first, so they win over shorter words at the same spot.

I'm laying out the checks to run: whether the query is understood, whether the totals and chart sums agree, whether highlighting matches the hits, and whether the normalisation holds. Each check gets a name, a pass or fail result, and a short detail, and a failing one will mark the tab with a red dot.

I'm weighing whether a numbering mismatch or a duplicate pinpoint should count as a failed check, since that would turn the header red for common queries. I'm leaning toward failing only real mismatches among the hits and noting lettered subparagraphs without failing them.

Still sorting out the results ordering: default by year and title, a document order option, and a most-matches-first option that counts highlighted terms in each paragraph.

I'm working out how to show the page size: 25 rows at a time, with a "Show 25 more" button that appends the next batch and resets whenever the hits change. For the paging check, I'm counting the rendered article rows against the hits, since the listed rows plus what's still remaining should equal the total.

I'm adding a context link to each open row that jumps to the previous or next paragraph of the same title, using a lookup by title and paragraph number, and I'm noting that a missing neighbor just shows a plain message.

I'm adding a context link to each open row that shows the paragraph before or after it under the same title, plus a copy helper that falls back to a selectable box when the clipboard isn't available, with a live message confirming what was copied.

I'm settling on a status box fixed to the bottom-left that holds the copied text in a scrollable area, with a textarea fallback when the clipboard isn't available, and I'm weighing whether it should clear itself or stay until clicked.

I'm adding the draft tab's item list, where each entry shows its quotation, citation, and a remove button, plus a "Copy all" action.

I'm working out the copy-all action, which joins each item's quotation into one text block, and I'm planning CSV export with a byte-order mark and CRLF line endings, quoting fields and doubling any inner quotes.

Next I'm working out the draft's copy formats: each item's quotation is just the quoted text, with the citation on its own line after it, and the single-quote copy button combines both. The CSV export drops the quote marks from the copied text, so the fields stay clean.

Next I'm planning the checks panel as a plain list of quirks, each with a count and one example pinpoint and citation, and skipping any collapsible details elements. I'm also planning a single-column layout for the Draft tab, with the rail hidden and a grid that stacks below 820px.

I'm laying out the tab roles and keyboard handling, then the header line showing the paragraph count, document count, committee count and year range, with the source link taken from the source URL when it exists. The footer will carry the source, the build info if present, the statement, and a credit for Chart.js.

Writing the filtering logic in code now...

I'm settling the committee filter: the counts next to each code will show how many paragraphs match, and I'm leaning toward always showing them rather than only after a search, since they're useful either way. Then I'll add the big headline number of matching paragraphs, shown against the full total, with a live region so screen readers pick up changes.

I'm laying out the filter rail: a heading with a "Clear all" button, then the big count of matching paragraphs, then the active filter chips for committees, years and document, each removable. The search block comes next, with a short syntax help list where a space or AND joins words.

Next I'm adding the operator help list: OR for either word, NOT or a leading minus to leave a term out, quotes for an exact phrase, parentheses for grouping, and a trailing star for word endings, with a note that only capitalised operators count. Then I'm adding example buttons and a live echo line that reports which paragraphs match the query.

I'm working out the strict check for the normalisation: whether any hit would only match once curly quotes or dashes are folded into straight ones. I'll test each term against the raw lowercased text rather than the normalised form, since phrase quotes are syntax and only apostrophes and hyphens inside terms matter.

Next I'm writing the quirk checks: counting records with paragraph 0, symbols shared across several titles, joint records, and duplicated pinpoints.

Now I'm working out the quirk notes for each row: a mismatch note when the text's leading number differs from the stored paragraph, a lettered sub-paragraph note, a duplicate-pinpoint note, and a joint-record note with both committee badges shown.

Next I'm checking how committee codes are assigned to each record: a normal record takes its code from the committee field plus any codes derived from its symbol, so a CAT record with symbol A/53/44 gets just CAT, and a CAT-OP symbol gives CAT-OP.

I'm checking the symbol-derived codes next: a CEDAW symbol should match whole words only, so the shorter CED pattern doesn't fire inside it. Symbols like CRC and CMW separated by commas, or joined by a dash, should each yield their own code. I'm also noting that a shared symbol like HRI/GEN/1/Rev.9 keeps the committee from the record's own field.

Working through the joint-record case, I'm building the committee and year summary over the matching paragraphs and handling the no-search wording. I'm also writing the pinpoint pattern for lettered sub-paragraphs and planning the compact CSS.

Now I'm writing the row renderer: each row picks its text (stored or shown), truncates anything over 700 characters unless it's expanded, and highlights matches. Footnote marks get a line noting how many were removed, with a button to show the text as stored.

I'm now setting up the detail panel for each row: copy buttons for the citation and quotation, an "Add to draft" action, and a short line showing the citation style. Context links will let me step to the previous and next paragraphs.

Wiring up the click handling on the results list next, with one delegated listener that routes each action button to its own handler. After each change I'll re-render that row and put focus back on the button the user pressed.

Now I'm writing the highlight pattern builder: each character gets mapped so curly apostrophes, quotes and dashes all match their straight versions in the text.

I'm working out the match pattern now: the regex runs over the normalised text, with the same word boundaries and wildcard handling, and phrase words joined by plain whitespace.

Checking the regex escaping: in unicode mode, "\-" and "\/" are invalid outside a character class, so I'll leave hyphens and slashes unescaped and only escape the true syntax characters. The `\u00ad` inside the character class is fine as long as the string carries it through to the regex source correctly.

Next I'm working out the tokenizer for the search box, which will treat any of the double-quote characters as the start or end of a phrase.

Still writing the tokenizer: I'm handling parentheses, double-quote characters that open and close phrases, and a leading minus as NOT, then scanning plain words up to the next space, bracket or quote.

Now I'm writing the tokenizer loop, so a word runs up to the next space, bracket or quote, and AND, OR and NOT become operator tokens while other words stay as plain words.

Now I'm writing the normalisation function: it strips the footnote markers, folds curly quotes and dashes into straight ones, and lowercases everything. I'm leaving the record text untrimmed, but the query gets trimmed, and I'll note that a NOT-only query matches any paragraph lacking those terms.

Now I'm setting up the search state and the rendering pipeline, with the parsed query, the ticked and open rows, and a recompute step that refreshes the results when the query changes.

Now I'm writing the chart code: counting hits per committee, sorting the counts from highest to lowest with ties broken alphabetically, and rendering them into the chart wrapper.

Still writing the chart configuration...

Still writing the chart rendering code...

Still wiring up the filter rail: the committee checkboxes get built once, and later renders only update their count labels so focus stays put. The all/none buttons follow the same approach.

Now I'm setting up the help panel's semantics and the arrow-key navigation through the example buttons.

Now I'm settling the sort orders for the results: by document oldest first and then paragraph, or by number of matches with newer years first. For the default, I'm sorting by year newest first, then title, then paragraph.

I'm building the citation for each record and then the copied quotation: the text is wrapped in curly quotes followed by the citation. For the plain-text copy, I'm dropping a leading paragraph number when it matches the paragraph, and I'm checking whether a regex that strips it should also handle footnote marks that come before the text.

Now I'm checking the totals, making sure the listed rows match the hit count and that the bracket sum equals the base plus the joint extras.

Now I'm checking the totals: the chart sum should match the hits plus the joint extras, which it does by construction. Next I'm verifying the normalisation and numbering, flagging any duplicate or mismatched pinpoints, and making sure each hit that matches gets a highlight.

Now I'm checking the fail case: a hit that matches in the normalised text but gets no highlight gets listed as "matched, not highlighted" and the check fails. I'm also watching for cases where footnote marks sit between words, since the gap pattern should cover a space or a mark, and where a mark follows a period without a space.

Now I'm writing the CSS, starting with the color variables for the paper background, ink, rules and the red accent.

Now I'm working on the bar and checklist rendering, and I'll keep the same row elements in place so focus doesn't move.

Writing the CSS variables and the tab layout next.

Now I'm defining the committee name lookup, which maps each treaty body code to its full name.

Still writing the committee name lookup, which maps each treaty body code to its full name.

Still working through the search box: I'm mapping out the tokenizer's operator handling and getting the regex escaping right. Next I'm setting up the precomputed text for each record, first working through how the query terms will be prepared.

Now I'm working out the record fields: the text is copied into a clean string, and I'm computing its normalised form, the count of footnote marks, a display version with the marks stripped, and any leading paragraph number or lettered sub-item.

Now I'm writing the code that builds each record's committee list: the primary committee comes first, followed by any other codes found in the symbol, with the joint flag set when there is more than one.

Still working out the copy text: I'm building the quotation from the paragraph and citation, and checking how a leading paragraph number should be stripped before it's pasted.

Now I'm working out the final field values: the copy text drops a leading paragraph number when it matches, and each record's word count comes from its trimmed shown text. Then I'm building the lookup maps by id and by title and paragraph, and counting the distinct documents and committees for the summary line.

Now I'm writing the query parser, which tokenizes the search string and walks it with a recursive descent over brackets, OR and NOT.

Still writing the query parser: I'm handling the OR level, which combines AND-groups, and raising clear error messages for unbalanced brackets or operators that lack a word on one side.

Still writing the query parser: the AND and NOT handling reads a NOT right after an AND, and two terms next to each other count as an implicit AND. Once the top level finishes, any leftover token that isn't a closing bracket is reported as an unbalanced parenthesis.

Still working through the query parser: the term builder handles phrases by splitting them into normalised words, and for single words it strips a trailing star into a prefix-match flag.

Now I'm defining the query matcher: each word or phrase becomes a regex bounded so it only matches whole words, with a trailing star allowing any ending.

Now I'm writing the query matcher's phrase handling, building the echo label for each term, and starting the describe helper.

Still working on the query describer: I'm writing a helper that turns each node into plain words, with phrases quoted, wildcard terms described as starting with the stem, and negations and nested groups wrapped in brackets where needed.

Now I'm working out the query's negation and positive terms, collecting the non-negated terms in a list so I can tell whether the query has any positive terms at all.

Now I'm building the highlight step, which walks the text with a reusable global regex and wraps each match while escaping the parts in between.

Still writing the highlight and count helpers, which walk the text with the match pattern and skip any empty matches.

Still writing the query evaluation: I'm defining how each parsed node is checked against a record, with negation flipping the result and strict matching using the shown text. Next I'm wiring up the recompute step that filters the records whenever the query changes, and then the sort handling.

Now I'm writing the render functions: the rail with the count, chips, echo and error, then the summary line and the results list.

Now I'm writing the checks: a function that returns the list of quirks, rendered into the checks panel, with the status in the header and a dot on the 04 tab.

Now I'm writing the checks and quirks panel: a list of computed checks rendered with pass marks, plus a static set of known quirks and a short note on how the figures are computed.

Now I'm wiring up the export and draft-saving handling, starting with the document dropdown's options and the year inputs.

Now I'm finishing the draft-saving setup and writing the copy helper, which shows a short confirmation once the text is copied.

Still writing the clipboard helper: I'm trying the browser's clipboard API first and falling back to a read-only text box with a select-and-copy button if that fails.

Still writing the download helper: it builds a blob from the content, points a hidden link at it, and triggers the save.

Now I'm wrapping up the draft-saving and copy helpers, and checking how the download and copy messages are shown.

Now I'm adding the search box markup: a label, the query input with its search button, and a hidden help panel tied to the input.

Now I'm adding the search box markup, with a label, the query input and its button, and a hidden help panel tied to the input.

Now I'm laying out the search box markup, with a label, the query input and its button, and a hidden help panel tied to the input.

Now I'm laying out the CSS for the page: base colours and fonts, focus outlines, and hidden elements kept hidden.

Still writing the page styles: I'm setting the base colours and fonts, the focus outlines, and making sure hidden elements stay hidden, then laying out the header tabs and the two-column grid with the filter rail beside the results.

Now I'm styling the results: the rail is set up, and each result row gets a top rule and a bold heading button. Badges are small outlined mono tags, and the pinpoint reference is shown in red mono next to the symbol and year.

Still working on the page styles: I'm laying out the buttons, the selected-state chips with their accent border, and the checkbox rows that take a highlight when ticked.

Now I'm rendering the rail's summary: the match count, the total, and the active filter chips for committees, years and document.

Now I'm wiring up the rail's expanding toggle and the row heading buttons, so each result can open to show its full text.

Now I'm rendering each result row: the heading toggle, whether the full text is open, and a shortened display that cuts at a word boundary and adds an ellipsis when the text runs long.

Now I'm finishing the row notes: a mismatch warning when the text's leading words don't match the paragraph number, and a note for lettered sub-paragraphs.

Now I'm adding the detail block's buttons and the context links, which let the user move to the previous or next record.

Still writing the context block: it shows the neighbouring paragraph in the same document, or a note if there is none.

Still writing the context block: each row's previous and next links look up the neighbouring paragraph in the same document, preferring unlettered records, and show a note when there isn't one.

Now I'm writing the row markup: the heading toggle with its badges and short title, then the meta line with the symbol link, pinpoint and year, and finally the text, notes and detail block.

Now I'm writing the results renderer: it shows the first page of matching rows and, if there are no matches, a message suggesting how to adjust the search.

Now I'm working out the summary line and the order control: the match count and totals, then a separate line stating how the results are sorted, with a select labelled "Order" that lists each sort option.

Now I'm checking the computed checks and quirks, starting the list of checks with the query-parsing one.

Still working through the checks: the next part compares the number of rows actually on the page with the number that should be shown, and the total against the match count. I'll also refresh the checks after the "show more" button, since the totals change then.

Now I'm checking the highlight: for each result, I'm counting whether the search terms actually appear in the shown text, so I can flag any row where nothing matches.

Now I'm checking the numbering: I'm flagging any row whose text doesn't start with its paragraph number, any duplicated paragraph, and any lettered sub-paragraph, then working out whether the check passes.

Now I'm checking the marker counts: the stored text is split on the footnote marks, and the rebuilt text is compared with the original, along with the number of marks against the stored count.

Next I'm looking at how the text is normalised, and then checking that each draft item still matches the text it was saved from.

Finally, I'm setting the status line and rendering the header status with its dot, and then moving on to the fourth panel.

Now I'm writing the quirks list, with one entry per known oddity and an example from the data, such as the symbol that holds the most documents.

Still writing the refilter logic, which runs the search again after the filters change.

Still writing the refilter logic: I'm recomputing the base set from the year range and the selected document, counting the committee ticks, and keeping only the hits that match a ticked committee before sorting and re-rendering.

Now I'm sorting the matches by how many search terms they hit, then falling back to year and paragraph order, and precomputing title ranks so the sort isn't slow.

Now I'm rendering the draft panel: the list of collected items, each with its quotation and citation, and an empty-state message when nothing has been added yet.

Still writing the draft export: I'm building the CSV output next.

Checking the marks and the draft entries against their stored text, then setting the status line.

Writing the results section markup now: a heading, a summary line, an order selector, a note that the page only reads records, the results container, and a "show more" button.

Now I'm checking how the search query tokenizes, including the parentheses, the hyphenated word "ill-treatment", and a leading minus sign for exclusion.

Still working out how the search terms get matched in the highlighting, including the quoted phrases and the wildcard words.

Still working out the highlight pattern: the search terms are joined with alternation, deduplicated, and sorted longest first. I'm also checking that the case-insensitive matching handles the Unicode characters correctly.

Now I'm finishing the footer text: the source line, a note that the page's own code handles the counting, matching and sorting without calling a model, and a credit for Chart.js.

Still working through the code: I'm setting up the query echo, the parse-error message, and the highlight pattern from the positive terms, plus the document selector and the committee "all" and "none" buttons.

Now I'm wiring up the redraw helper: it swaps out a single result row after an action and moves focus back to the button that was pressed.

Now I'm wiring up the click handler on the results container: it finds the row that was clicked and either runs the action on its button or toggles the row open, unless the click landed on a link, the detail block, or a text selection.

Still writing the click handling: the results container catches clicks on each row, and the buttons inside it act on the matching paragraph.

Now I'm double-checking how the quote is built, wrapping the copy text in curly quotation marks, and then writing out the final HTML file.

