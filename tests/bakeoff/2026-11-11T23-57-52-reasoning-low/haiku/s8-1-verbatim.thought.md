I'm starting to build the app as one complete HTML document, which needs to stay under roughly 1,500 lines while still being full-featured. I'll keep the plan tight: first read the workshop records, then lay out the header and the left rail.

I'm mapping out the rest of the planned pieces: the query parser with its operator precedence, the term and highlight matching, the hit and filter logic, and how committees are pulled from symbols. I'm also working out how a citation is built, from the committee and document name down to the pinpoint paragraph.

I'm settling the remaining details: the copied quotation drops the leading number when it matches the paragraph, and the draft is saved with localStorage as a fallback. I'm also working through the checks, the known quirks at load, the prev/next context within the same title, and the sort options for document order or most matches first.

I'm settling the chart and filter rail details: a horizontal bar chart with a text table beside it, committee checkboxes that show counts after search, and a year range and grouped document select. The sidebar also gets a clear-all control, a search box with syntax help on focus, and a collapsible numbered filter section.

I'm working out how committees are derived for each record: the symbol codes plus the committee field, with joint symbols counting toward each committee they name. I'm also checking that the chart totals add up, since a record that names two committees gets counted under both bars.

I'm listing the committee full names next, starting with the treaty bodies and working down the list.

I'm working out how to recognise each committee from its symbol code, with CAT/OP needing special handling so it isn't also counted as plain CAT.

I'm checking the committee regexes: CAT/OP needs its own match so it isn't also counted as plain CAT, and word boundaries keep CED from catching CEDAW. I'm also deciding that a record counts as joint when its symbol contains a dash or a comma.

I'm settling the normalisation step: I'll strip the footnote markers, swap curly quotes and non-breaking spaces for plain ones, and lowercase everything so matching is consistent. Soft hyphens become ordinary hyphens, and I'm checking that word-boundary matching still treats a term after a hyphen as a separate word.

I'm settling how the query gets normalised: stripping the footnote marks first, then matching quotes and dashes and lowercasing, so the terms line up with the stored text. I'm still deciding whether to normalise the whole query string up front or each term after the tokens are parsed.

I'm defining the tokenizer now: it skips whitespace, emits parentheses as their own tokens, and reads quoted phrases up to the closing quote, flagging an error if none is found. Bare words are collected until a space, parenthesis, or quote, with the capitalised operators kept separate from ordinary terms. I'm leaving case alone at this stage so AND, OR and NOT still register as operators.

I'm settling the operator grammar now: an OR-level expression built from AND-level groups, where adjacent terms join implicitly and NOT binds tightest, with parentheses grouping the rest.

I'm defining the operator grammar for the query: OR is the loosest, AND can be implicit between adjacent terms, and NOT binds tightest. I'm also setting the error cases to report, including unclosed quotes, unmatched parentheses, empty groups, and an operator with nothing after it. For the echo, I'll render each term as its word or phrase, joined by "and" and "or".

I'm settling how the echo reads back the query: the parsed tree gets described term by term, with AND and OR joined as "and" and "or". When the whole query is only a NOT, I'll phrase it as paragraphs that do not contain the term, since "without the word X" reads awkwardly.

I'm making the term regex handle a trailing wildcard by matching any run of letters, digits, or underscores after the stem, and I'm escaping the rest of the word so special characters match literally. I'm going with a Unicode letter class instead of plain \w so accented words still match correctly.

I'm settling how the search term regex handles a trailing wildcard, escaping the rest of the word so special characters match literally, and building each word of a phrase separately so it can be joined with flexible whitespace.

I'm writing the highlight regex now, which needs to match the shown text case-insensitively and treat curly and straight quotes, dashes and soft hyphens as interchangeable, with flexible whitespace between the words of a phrase.

I'm finishing the highlight pattern now, mapping the straight quotes to a set that also covers the curly ones, and I'll keep the same boundary checks and whitespace handling as the search side.

I'm checking whether the highlight mapping for hyphens still matters, since the normalised text already turns every dash form into a plain hyphen. I'm also wondering whether the term matcher should escape straight apostrophes the same way.

I'm settling how matching runs: a record counts as a hit when the parsed query tree evaluates to true against the normalised text, with each term tested by its precompiled regex. I'm also leaving the highlight side out of that check, so a term that matches the text without a visible highlight is something I still need to verify.

I'm checking the normalisation by comparing hits whose text contains curly quotes or dashes against the words typed with straight characters, since those are the ones the normalisation would have changed.

I'm settling the integrity check for the footnote markers: I'll strip them to get the shown text, keep the removed pieces alongside, and confirm that reinserting them reproduces the stored text exactly.

I'm checking the integrity of the footnote markers by counting the literal "[[fn:" occurrences against the regex matches, since a mismatch would show a malformed marker. For the numbering, I'm flagging hits whose leading value isn't null, and I'm looking at whether records sharing a title and paragraph should be grouped to catch duplicate pinpoints.

I'm working through the final checks: confirming the draft lookup by id and comparing its text against the stored version, then making sure the rendered rows across pages add up to the total hit count.

I'm checking the chart total against the hits plus joint hits, and I'm adding a check that the committee counts sum to the same figure, since both should agree.

I'm checking how the committee codes map onto each record's symbol, expecting them to agree except for the CAT-OP case, and I'm looking at joint records to confirm they resolve to more than one committee.

I'm checking the committee logic against the symbols: a joint record with two symbols from the same committee would only count once, so the chart total would come up short and the check would flag it.

I'm now listing the load-time quirks to report: paragraph-zero records, symbols shared across documents, joint documents, duplicate pinpoints, and mismatched leading values, each with an example. Then I'll set up the checks, some of which depend on the current query, and show the pass or fail count in the header and the checks tab.

I'm settling the remaining checks: query, totals, chart, highlight, normalisation, numbering, footnote markers, and the draft lookup, with failures turning the header dot red. I'll also show a list of known quirks in the checks tab from load time, and add context links that open the neighbouring paragraphs of the same title in grey.

I'm settling the row layout now: a committee badge, the short title, the symbol linked to its document, the pinpoint and the year. The paragraph text goes beneath with its footnote marks stripped, plus a small toggle to show the stored version, and I'll keep anything longer than about 700 characters collapsed.

I'm settling the row layout so each article heading is a button that toggles the row open in place, with a fallback open control for accessibility. Long paragraphs get cut at about 700 characters with a link showing the full word count.

I'm now working out the copy behaviour: the button writes to the clipboard, and if that isn't available it falls back to a selectable textarea with a message. For quotations, I'll copy the shown text in curly quotes, dropping any leading paragraph number when it matches the paragraph. I'm also starting the citation builder, which begins with the symbol and pinpoint and adds a prefix for shared symbols.

I'm defining the citation format as committee, a short document name with its symbol, and the pinpoint, taking the document name from the title up to the first colon or " on ". For pinpoints, a paragraph of zero reads as "preamble", a lettered record gets its letter as a subparagraph, and anything else reads as "para. N".

I'm settling the draft entries now, which will hold the citation, the copied quotation, the text as copied, and the stored text alongside the symbol and paragraph.

I'm now defining the draft entries and the copy-all, download, and CSV export behaviour, with the draft kept in local storage and a memory fallback. The draft check will look each entry up by id and confirm its text still matches the stored version. I'm also starting to note how the filter rail should hide.

I'm settling the committee checkboxes next: each one shows a count of matching records, and I need to decide whether that count respects the other filters. If the bracketed counts ignore the year and document filters, they won't add up to the filtered hit total, so I'll have the check compare against a figure computed the same way.

I'm defining the committee checkboxes so each bracketed count is the number of hits that match the query, year and document filters for that committee, ignoring the committee filter itself. With every committee ticked, those counts should sum to the hits plus the joint hits, so the chart check will compare against that figure.

I'm settling the document dropdown next, grouping the titles under their committees and filtering on the exact title string. The committee checkboxes will be checked against the same pre-committee set, so the counts add up with every box ticked.

I'm setting up the year inputs as numeric fields bounded by the data's range, and the filter keeps paragraphs whose year falls between them. Active filters will appear as removable chips under the big match count, which reads as "279 matching paragraphs" out of 7,304. Last, the search box gets a Search button, submits on Enter, and shows a syntax help list when it's focused and empty.

I'm setting up the search box's behaviour: running the query on submit, and treating an empty query as "no search words", which lets every paragraph through the other filters. An unbalanced quote or parenthesis will show a message and return no results.

I'm now planning the overview chart: a horizontal bar chart of committee counts sorted by size, with the values drawn at the end of each bar and a click that narrows the view to that committee. I'll keep the gridlines faint and limit the x-axis ticks, and give the canvas an accessible label with the numbers, plus a small table beside it.

I'm wiring up the tab bar as a proper tablist, with arrow-key navigation and hidden panels. Paging will show 25 paragraphs at a time with a "Show 25 more" button, and sorting will offer either year or match count, with ties broken by year, title and paragraph.

I'm computing a match count for each hit by summing the global regex matches of the positive terms, which only matters when sorting by matches. Then I'll split the filtering into a base set (query, year and document) and the committee-filtered hits, so the checkbox counts and the totals line up.

I'm precomputing the per-record data: normalized text, the shown text, leading paragraph number, committees, joint flag, shared symbols, pinpoint, and citation parts. Then I'll evaluate the query tree against each record and build the filter flow, starting with the base set (query, years, document) and counting committees within it.

I'm working through how the totals and committee counts fit together for the filtered hits, and then sorting out how each lettered record gets its subparagraph pinpoint versus the preamble case.

I'm adding the amber notes for each row: a mismatch between the leading paragraph number in the text and the record's paragraph, a lettered sub-paragraph, a pinpoint shared with another record of the same title, and joint General Comments. I'll also keep the row details, with the copy-citation action, limited to the open row.

I'm working out the load-time stats for the header: the number of records, the distinct titles and committee codes, and the year range. I still need to settle how the committee count is worked out from the data.

I'm working out the header line now: a count of paragraphs, the distinct titles and committees, and the year range. For the source, I'll link it if it's a URL, and otherwise show it as plain text.

I'm laying out the header and footer: the tab labels for the overview, paragraphs, draft and check panels, and a collapsible rail heading that holds the committee checkboxes, year inputs and document dropdown. I'm also planning the search echo line and its error message before writing out the code.

I'm setting up the document's structure: a header with the title and load stats, then a rail for committees, years and documents alongside the main tabs.

I'm now laying out the search box and rail: a big match count with the total beneath it, the search field, and the filter inputs, while the page code takes shape.

I'm putting the search field, its Search button and the syntax and example panel into the rail, with a hint line, an echo line and a live error line beneath them.

I'm putting the committee checkboxes, year inputs and document dropdown into a collapsible panel under the rail heading, with the all and none buttons above the checkboxes. The hidden attribute is kept in check by a CSS rule, and the rail itself gets hidden on the Draft tab so the main column takes the full width.

I'm writing the syntax list in the app's own words, then adding the example buttons under it.

I'm laying out the overview with a bar chart of paragraphs per committee, a table beside it, and a short note on how the numbers are computed.

I'm laying out the paragraphs tab: a summary line with the hit, record and committee counts and the year span, a sort control, a list that shows 25 at a time with a "Show 25 more" button, and a draft tab with its own count and list.

Now I'm writing the JavaScript that loads the records and sets up the committee table, year filter, and document dropdown.

Writing the committee lookup table and the helper functions...

Still writing the search helpers...

Still writing the committee helpers...

Still writing the committee code helpers...

Still writing the code-matching helpers...

Still writing the citation helper...

Still writing the record preprocessing and the symbol-to-title map...

I'm defining the record preprocessing next, tying each row to its normalized text, leading paragraph number, and shared-symbol status.

Still writing the record preprocessing, tying each row to its shared-symbol and joint flags.

Still writing the query lexer...

Still writing the query lexer, handling the quoted phrases and parentheses.

Still writing the query parser, handling the minus prefix as a NOT token.

Still writing the query parser, working through the OR and AND levels of the expression tree.

Still writing the parser's primary-expression handling, so that an unexpected end of input raises an error.

Still writing the parser's primary-expression handling, so that an empty pair of parentheses or an unclosed one raises a clear error.

Still writing the phrase-term handling, splitting the quoted text into words.

Still writing the term matching, turning each word into a regex that respects word boundaries and wildcards.

Still writing the highlight pattern, mapping straight and curly quotes, hyphens and dashes to matching character sets.

Still writing the highlight helper, mapping straight and curly apostrophes, double quotes and dashes to matching character sets.

Still writing the highlight wrapper, building one combined pattern from the phrase and word terms.

Still writing the highlight helper, sorting the patterns so the longer phrases match first.

Still writing the match-checking logic: each node is tested against the normalized text, with NOT inverting the result and AND and OR combining their children.

I'm turning the echo line into a readable description: each term becomes "the word X" or "the phrase “X”", a NOT becomes "without ...", and AND and OR children are joined with "and" and "or".

I'm describing the echo line by walking the query tree: NOT becomes "without" and AND and OR children are joined, with the root-level NOT case getting its own wording. I'm also planning a term count and starting the compile function that parses the query and reports any error.

Still writing the state setup and the render function that computes the matches.

Still writing the filter logic, applying the year range, document choice and query check to each paragraph.

Still writing the sort logic for the paragraphs list.

Still writing the sorting helper, ordering by match count when that option is picked and falling back to year, then title and paragraph.

Still writing the summary line and the list rendering, counting matches against the committee total and falling back to a "no search words" note when there's no query.

Still writing the row markup, showing a preview of about 700 characters that breaks at a word boundary.

Still writing the row markup, adding the heading button with its expanded state and the preview toggle.

Still writing the row markup, adding the heading button with its open state, the badges, and the notes and paragraph text.

Still writing the row markup, adding the symbol link, the committee badges, and the pinpoint and year.

Still writing the context and copy helpers, with the neighbour lookup for the previous and next paragraphs and the citation-copy action.

Still writing the copy helper, using the clipboard and falling back to a selectable box if the browser refuses.

Still writing the draft handling, storing each entry's citation and copied quotation, with localStorage when the browser allows it and memory otherwise.

Still writing the draft export, joining each entry's quotation and citation into one block of text.

Still writing the check list, with the query-understood check reporting any parse error and otherwise noting that no search words means every paragraph that passes the filters is listed.

Still working on the totals check: I'm making sure the rendered row count matches the smaller of the display limit and the hit count, and that the committee checkbox counts add up to the base set plus the joint documents.

Still writing the totals and highlight checks, comparing the chart sum against the hit count plus joint documents and looking at whether each positive-term hit actually gets highlighted.

Still writing the highlight check: I'm counting how many hits have curly quotes or dashes in their shown text, for queries that use straight quotes, apostrophes or hyphens.

Still writing the highlight check, looking at whether any straight quotes, apostrophes or hyphens in the query also pick up curly quotes or dashes in the shown text.

I'm writing the marks check now: counting the literal footnote markers in each hit's text against the stored mark count, and confirming that no stray double brackets remain in the shown text.

Still writing the draft export and the CSV download, escaping quotes and adding a byte-order mark before the file is built.

I'm adding a set of quick data-quality notes to the load step: how many paragraph-zero records there are with an example, how many symbols are shared by several documents, how many joint documents there are, and how many title-and-paragraph pairs repeat. I'm also counting leading-number mismatches with an example, the lettered sub-paragraph records, and footnote marks sitting between letters.

Still writing the chart code, drawing a bar for each code that has at least one hit and checking that the bars add up to the total.

Still writing the chart's end labels, drawing each count just past its bar.

Still writing the chart options: the plugins, the axis styling, a click handler that narrows the view to the tapped code, and some right-side padding for the end labels.

Still writing the chart's bar settings and the table beneath it, with a label for each committee and an aria-label listing the counts.

I'm settling on the checkbox approach: the committee checkboxes get built once when the page loads, and each refresh only updates their counts and checked state. That way a keyboard user won't lose focus when clicking a box, since the element never gets replaced. Clicking a bar on the chart will narrow the view to that committee and sync the checkboxes to match.

I'm setting up the document dropdown, grouping titles under their committee and labelling each with its short title and symbol so duplicates stay distinct. Then I'll wire the year inputs and the committee chips to refresh the view.

Still writing the chat-style filter chips, the clear-all reset, and the search submit wiring, so the form runs the query and resets the result limit and open row each time.

Still wiring the search results: when the query has an error, the echo stays empty and the error message appears instead, and the summary says no results until the search is fixed. Next I'm setting up the tab switching, with arrow-key navigation and the rail hidden on the draft tab, and updating the tab labels with the draft count.

Now I'm wiring up the list rendering, with click handling delegated on the list for opening rows and the cite, quote, add and context actions. The full-text toggle and the stored-draft toggle each keep their own set of ids. "Show 25 more" raises the display limit and re-renders the list, and sorting and draft removal are handled the same way through delegation.

Still writing the stylesheet, starting with the color variables and the base body and kicker styles.

Still writing the stylesheet: the body font, the kicker labels, the big-number styling, and the two-column layout with its single-column variant when the side rail is hidden.

Still writing the stylesheet: the tab bar and its selected state, the highlight colour for matched words, and the badge styling for the committee labels.

Still writing the stylesheet: the badge and pin styles, the pass, note and fail colours, the row dividers, the chip and table styling, and the hint and status-dot rules.

Now I'm writing the JavaScript setup: the data constants and small helper functions, with the committee list and the escaping helper written out in full.

Still writing the helpers: escaping for HTML, a number formatter, a regex escaper, a function that strips footnote markers from the shown text, and a normaliser that folds curly quotes and dashes to plain ones and lowercases the text.

Still writing the record mapping: working out each row's shown text and matching leading numbers and lettered sub-paragraphs.

I'm defining the record mapping: each row gets its shown text, a leading number if it has one, and a lettered sub-paragraph marker where present.

Still writing the record mapping: each row gets its shown text, a leading paragraph number where it has one, and a lettered sub-paragraph marker where present. I'm also working out the pinpoint cite for each record, with the committee and short document name added only when the symbol is shared by several documents.

Still writing the record mapping: the pinpoint cite gets the committee and short document name only when a symbol is shared, and the copied text drops the leading paragraph number when it matches the paragraph.

Still writing the record setup: the duplicate check across the title and paragraph pairs, the leading-number and lettered sub-paragraph matching, and the footnote marks.

Now I'm writing the record-matching helper, with its `makeTerm` function splitting phrases into words.

Still writing the record-matching helper, with `makeTerm` turning each word or phrase into a boundary-checked pattern.

Still writing the term matching: each word or phrase gets a boundary-checked pattern for both normalised and highlight matching, with stars allowed on the end of words.

Still writing the term-building code: each word or phrase is turned into a boundary-checked pattern, with stars allowed at the end of words.

Writing the query parser's primary-term function now, with parentheses handled and an error raised for empty groups or an unclosed parenthesis.

Still writing the parser: the unary NOT handling and the AND and OR chain, with the next group of precedence checks left to write.

Still writing the parser: the AND and OR chain is in place, and the code is now checking for leftover tokens after the top-level expression.

Still writing the query parser: I'm checking for leftover tokens after the top-level expression, with a message for an unopened parenthesis or an unexpected token.

Still writing the describe helper, which turns each parsed node back into readable text, with phrases quoted and nested groups wrapped in parentheses.

Still writing the tab handling, with the tab list being collected from the tab bar so arrow keys can move between tabs.

Still wiring up the tab switching: setting the selected state and panel visibility, collapsing the side rail on the draft tab, and handling arrow keys to move between tabs.

Now I'm wiring up the tab-switching code so the side rail hides on the draft tab, with the rail's own hidden attribute toggled and a layout class as a fallback. The tab labels are set to include the current draft count.

Still writing the markup: the masthead with its kicker, title and status line, and the tab bar and panels above the record list.

Still writing the markup: the masthead, the tab bar with its panels, the side rail, and the footer.

Still writing the rail markup: the filter header with its clear button, the big match count, the search form, and the query help text.

Still writing the rail markup: the committee filter fieldset and the year range inputs.

Still writing the search examples and the syntax notes, with the list of operator forms and the example queries about to go in the examples block.

Still writing the search examples: the list of example queries opens under the box, with arrow keys moving between the buttons.

Now I'm laying out the search examples and syntax notes inside the form, so the list opens under the box and closes once typing starts or focus leaves the search area.

Still writing the overview panel: the per-committee bar chart and its table, with a short note on how the counts are worked out.

Still writing the overview and the answer line, which will show the count of matching paragraphs across the committees. Next I'm setting up the paragraphs tab, with a summary line, a sort menu and a list that loads more on request.

Still writing the page markup: the paragraphs tab's sort menu and the "Show 25 more" button, with the third tab's section opening next.

Still writing the markup for the draft tab: its heading with the quotation count, the copy and download buttons, and the message line. Then the fourth tab's checks and quirks sections.

Still writing the method notes and the main render setup, with the state object holding the query, filters and sort order.

Still writing the match count logic: the base set is filtered by the year range, the selected document, and the query, and the hits are those base records whose committee codes are ticked.

Still writing the match counting: each term gets a global pattern, and the match count per record is summed from those. Next I'm setting up the refresh step, which recomputes the results, sorts them, and redraws each panel, with the rail's big count and its "of" total coming after.

Still writing the render code: the committee counts for each checkbox are recalculated from the base set, and the checked states, chips and the query echo are updated to match.

Still writing the overview chart: the committee counts are tallied from the hits and sorted, then the bar chart and its table are filled in from that.

Still writing the list rendering: the summary line is built from the hits, counting how many committees and which years they cover.

Still writing the list rendering: the summary sentence now counts the committees and the year span across the hits, and the first page of results is written into the list, with the "Show 25 more" button shown only while more results remain.

Still writing the row rendering: each paragraph's text is cut to about 700 characters at a word boundary, unless it is open or already expanded.

Still writing the row rendering: the paragraph text is cut to about 700 characters at a word boundary unless it is open or expanded, and the word count and notes about the record's numbering and duplicates are being prepared.

Still writing the row markup: each paragraph's metadata line shows its badges, pinpoint, source document link and year, and the heading button toggles the open state.

Still writing the row markup: the footnote-mark line shows how many marks were removed and a link that switches between the shown and stored text.

Still writing the row markup: the open rows get their copy buttons for the citation, quotation and draft, and the context links sit beside them.

Still writing the row context block: the previous and next paragraphs are looked up by title and paragraph number, and the list is taken from that match.

Still writing the context block: when there is no neighbouring paragraph, a short grey note says so, otherwise the matching record's pinpoint, symbol and text fill a small box under the row.

Still writing the list handling: a click on an open-toggle button flips that row's open state and clears the context box.

Still writing the click handler: the open toggle, the full and stored text buttons, and the citation, quotation and draft copy actions are wired up by row id.

Switching the DOM handlers over to indexes now, so every row uses `data-i` instead of the record id.

Still writing the copy helper: after a successful copy the message shows what was copied, and if the browser refuses, the text goes into the fallback box for manual copying.

Still writing the draft-adding function: it refuses duplicates by record id, then stores the symbol, pinpoint, committee, title, year, document link, citation and both the shown and stored text.

I'm writing the draft list rendering now, with each quotation shown as a block and its citation beneath it, plus the draft count in the heading.

Still writing the draft list: each saved item gets a Remove button and a check that its stored text still matches the source record.

Still writing the draft export: the copy-all text joins each quotation with its citation, and downloads are built as blobs.

Still writing the checks: the next part lays out a list of checks, with each result added to the output.

Still writing the checks: the query check reports a parse error, notes when there are no search words, or otherwise shows the echoed query and its term count, and the totals and rendered-row count are being worked out next.

Still writing the totals check: it compares the listed rows against the hit count, and the checkbox counts against the base set plus its joint hits.

Still writing the chart check: the bar totals are summed across the hits, and that sum is compared against the hit count plus the joint hits.

Still writing the highlight check: it tests each hit's displayed text against the highlight patterns and counts how many hits turn up without a visible highlight.

Still writing the highlight check: it counts how many hits show a mark, and the check passes only if every hit has one.

Still writing the normalisation check: the query's straight quotes, apostrophes and hyphens are compared with the curly quotes and en or em dashes in the hit text, and the result shows how many hits use those forms.

Still writing the numbering check: it counts paragraphs whose leading number differs from the paragraph number, and tallies the duplicate and lettered records among the hits.

Still writing the marks check: each hit's footnote markers are counted against its recorded mark total, and the check looks for any leftover marker text in the displayed version.

Still writing the marks check: each hit's footnote markers are tested by splitting the stored text, so the even parts should rebuild the shown text and the odd parts should match the mark count.

Still writing the check results: the duplicate-draft and mark checks are wrapped up, and the overall pass is set only when every check holds.

Still writing the quirks list: it gathers the paragraph-zero records, the symbols shared across documents, the joint records, the duplicated pinpoints and the leading-number mismatches into short notes.

Still writing the header line: it states the paragraph count, the distinct General Comments titles and committee count, the year span, and links the source.

Still writing the header and footer: the header gives the paragraph count, distinct titles, committee count and year span, and the footer names the source and build date, with a Chart.js credit line.

Still wiring the chips and the year inputs, along with the tab and committee controls.

Still wiring the chips: committees, years and the document filter each add a removable chip, and clicking one resets that filter and refreshes the view.

Now I'm wiring the document dropdown, grouping the General Comments titles under their committees and labelling each option with its short title and symbol.

Now I'm finishing the document dropdown and the filter chips that sit above the results.

Still writing the final pieces of the app: the chips and the document dropdown are wired up, and I'm now setting the hit-line counts and the highlight source list.

Still writing the search runner: it compiles the query, stores the parsed tree and any error, collects the positive terms for highlighting, and resets the open rows and paging.

Still writing the search runner: the sort helper is being set up next, starting with a copy of the list so the original stays untouched.

Still writing the search runner: the sort helper is ordering hits by match count when a query is active, with the year order as the tie-break.

Still writing the summary helper: it builds the stats line from the hit list before the render code runs.

Still writing the summary helper: the stats line counts the hits, distinct committees and year span, and falls back to a message when the search cannot be read or has no words.

Still writing the summary: the stats line gets its totals, and the sort note is set to match the chosen ordering.

Now I'm finishing the header and the tab labels, and the pass or fail dot follows the checks: when any check fails, a red dot appears on the fourth tab.

Still writing the app's data and search helpers: the escape, format and regex-escape utilities are being set up next, along with the committee table.

Still writing the parser helper: it escapes regex characters and defines a letter-or-number class for matching words.

Still writing the code that builds the record set: it takes the committee and symbol for each paragraph and works out which committees it belongs to.

Now I'm setting up the example queries as a JavaScript array and rendering them as buttons, with each button's index driving the click handler.

Still wiring the keyboard controls: the search box hands focus to the example list on the down arrow, and the list moves focus between buttons with the arrows, closing on Escape.

Still wiring the keyboard and focus behaviour on the example queries, so the list opens on focus and closes when focus leaves the form.

Writing the endLabels plugin for the overview chart...

Writing the chart's click handling next, so a click on a bar opens that committee's results.

Still writing the chart setup: the bar values get their own label plugin, and the wrapper's height follows the number of committee rows.

Still writing the methods section: it explains that the page's own code does the counting, matching and sorting, with no model call and nothing leaving the browser, followed by a short numbered list of how the query is read.

Still writing the closing check of the example list's keyboard handling, so the arrows wrap round and Escape returns focus to the search box.

Still writing the rail: it builds the committee checkboxes from the committee table, each row carrying its code, name and a live count.

Still wiring the rail: it fills each committee's live count from the current search, ticks the checkboxes to match the chosen committees, and rebuilds the year and document chips.

Still writing the chip rendering: each active filter becomes a removable chip, and clicks on the chips are handled by one delegated listener.

Still wiring the chip and draft handlers: the chip row reads its filter from a shared list and runs whichever one was clicked, then refreshes the view.

Still writing the chart and summary code: the header's pass/fail line is being set from the check results, and I'm now wrapping up the remaining rendering helpers.

