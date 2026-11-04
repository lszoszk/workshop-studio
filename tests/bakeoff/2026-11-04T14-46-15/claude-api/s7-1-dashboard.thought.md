I'm planning a large single HTML file, aiming for under about 1500 lines, and I want the design settled before writing it. The key constraint is keeping each view to roughly seven clickable things. Four tabs plus three filter headings already reach seven, so anything extra like "clear all" or the chips would push past the limit.

I'm sorting out the remaining controls: "Clear all" is an extra button, but it still keeps the count around seven. Chips only show up when a filter is active, so they don't add to the baseline. Next I'm working out the data setup, pulling the country and records from the dataset and precomputing a few fields per record for searching and sorting.

I'm working out how to decide which states a record belongs to, with a regex that pulls parenthesized groups from the end of the text and keeps only the short ones with no commas. I'm also settling the filter state, with an array of themes that combine with AND across all active filters.

I'm laying out the filter controls as selects for mechanism, body, type and state, so each counts as a single clickable. The three filter headings open as an accordion, one at a time, with the panels hidden until expanded. On the State and Themes tabs I'll hide the accordion and keep only the number, the bar and the chips, while Clear all stays in the header.

I'm settling the shared keyword field: the search box on the Records tab and the one in the filter rail will both bind to the same state value, debounced at 300 ms and kept in sync. Next I'm laying out the four tabs, with Overview holding the tiles, FIG.01, a table and FIG.02, and planning a small inline plugin to draw the values at the ends of the horizontal bars.

I'm laying out the chart click handling so theme names in the table also work as small link-style buttons for keyboard users, and the chart and table will both feed into the same theme filter.

I'm settling the chart and tile details: FIG.02 will be a stacked bar over every year from the first to the last in the filtered records, with one dataset per mechanism and a legend, and an empty-state message when nothing matches. The overview tiles will count the filtered records, showing "of N in the file" when a filter is active, with a per-type breakdown underneath.

I'm laying out the overview tiles and the mechanism cards, with a small colour dot for each mechanism and a "see the States" link that expands a list of the ten States in place. Under the first chart I'll add a table of theme, records, share and years, and on the Records tab a search box, a sortable Date column and expandable rows, with a "Show 50 more" control for paging.

I'm deciding where the State filter goes: it sits under heading 02 as a select with counts, shown only when states were found. Then I'm settling the table's column order, with State placed after the first line, since the narrow layout needs six columns to fit.

I'm settling the column order: State goes after Para. and before First line, so the first-line text has room to wrap in the narrow layout. For sorting, I'm ordering by date, then body, then paragraph number, with paragraphs compared as major and minor parts and missing paragraphs placed last. The Date header only flips the date direction, so the tie-breakers stay the same either way.

I'm writing the highlight helper so it matches the keywords against the raw text and escapes each piece separately, which avoids breaking HTML entities. I'm also laying out the expanded row, with a large red paragraph number and the full text, then the theme, SDG and SDG-name lists.

I'm settling the detail row: each record expands to show its full paragraph number and text, followed by the theme, SDG and target lists, plus a copy-citation button and a link to the UN document. Clicks on links and buttons inside rows shouldn't toggle the expansion, and keyboard users can open rows with Enter or Space.

I'm moving on to the checks section: the full data gets partition checks, and the filtered set gets chart-versus-table checks. Each line will show a label and two values with a pass or fail mark, using a warning style for paragraph-number issues. I'm also planning a sum check per type against the filtered headline total.

I'm settling the overview numbers next: the top ten themes get counted with a second, independent pass, and I'll store those figures so the chart and table can be checked against them on the check tab.

I'm settling the checks: a link check that the document URL starts with the UN docs prefix and ends with the symbol, allowing for URL-encoded slashes. For the chart-versus-table comparison, I'll rely on the stored theme stats, since the chart may be stale when its tab is inactive.

I'm checking the links next: each document URL should start with the UN docs prefix and end with its symbol, allowing for encoded slashes, and I'll list any failures. Then I'm planning a paragraph-number check per mechanism, where UPR should reach 100% and anything lower gets a warning, followed by a States check that counts UPR records with a state and lists the ones without, showing the symbol and the last 80 characters of the text.

I'm working through the sample section now: pulling ten records from the current filter with a seeded random generator, so the same filter always gives the same ten.

I'm setting up the sample draw: the same filter and seed should always produce the same ten records, so I'll shuffle over the filtered set in file order using a seeded generator. Before the first draw there'll be just one button, and afterwards a seed box with "Draw again" and "Draw with this seed" controls.

I'm weighing whether the seed should be used on the first click or whether that button should pick a random seed instead. Using the seed in the box for the first draw keeps it reproducible, and then "Draw again" would switch to a new random seed.

I'm laying out the sample section: each card shows the symbol, paragraph number and first words on one line, with the full text, theme chips and verdict buttons only in the open card, and the state tracks the seed, the chosen ids, the verdicts and which card is open as the filter changes.

I'm handling the sample tally: each verdict count goes in the summary line along with the judged total and the seed. If the filter has changed since the draw, a note tells the user to draw again rather than mixing old judgments with the new filter.

I'm settling the first-visit sample: the initial button draws with the seed in the box, which defaults to 1, so the first draw is reproducible. After that, "Draw again" picks a fresh random seed, and "Draw with this seed" reuses whatever is typed in the box.

I'm finalising the Method tab next, with a short explanation of the data, a button to download the CSV, and a button to copy a summary. The source and build date go alongside. Since the file has no licence field, I'll point readers to the source page to check the terms before republishing rather than stating one myself.

I'm writing the CSV export: a BOM at the very start, then the header row with the record fields, with lists joined by pipes and quotes escaped. I'm also planning a download through a temporary blob link, and a guard so that cells starting with a formula character are neutralised.

I'm settling the Method tab's CSV export and the summary copy, and I'm working out how the year filters should behave: the selects default to no bound, and choosing a from-year after a to-year swaps them so the range stays valid.

I'm working out the header: a label with the country, a title, and a source line linking to the record's source page along with the record count, document count, year span and build date. For the source link, I'm only going to allow a safe URL.

I'm laying out the overview tiles next: one per mechanism with its colour, record and document counts, latest year and share of the filtered set. The UPR tile gets a button that opens a panel listing the ten States that made the most recommendations to this country.

I'm working out the States list next: for each filtered UPR record, every recommending state counts once, with whitespace normalised, and the top ten sorted by count with ties in alphabetical order. I'll note that these are counts of recommendations rather than influence, since co-sponsors are counted for each one.

I'm checking whether a parenthetical at the end of a UPR text can be read as a State name, and noting that a short group like "(see paragraph 5)" without a comma would wrongly pass as one. I'll let the check panel show those cases for review, and maybe tighten the rule so groups starting with a lowercase word are rejected.

I'm going over the paragraph-number pattern: it should take the leading number, including a decimal part, and I'm sorting rows by major and minor parts. I'm also setting the date sort to compare the ISO date strings, with missing dates handled separately.

I'm checking the tab markup next: a tablist with roving tabindex, arrow keys and Home/End moving between tabs, and each panel hidden until selected. The filter rail should only appear on the first two tabs. I'm also adding a visible focus ring, and I'm still deciding how the bar chart labels will fit, since the theme names can run to about sixty characters.

Writing the bar value label plugin...

I'm wiring the bar chart's value labels: a small plugin that draws each count at the end of its bar, and I'm widening the x-axis range so the numbers fit without being clipped. I'll keep the axis itself hidden and register the plugin on each chart, colouring the bars in the deep red.

Next I'm adding the chart's click handling, where a click on a bar adds that theme to the filter, plus a cursor change on hover. The second chart is stacked bars by year with a legend and the mechanism colours, and I'll destroy any existing chart before drawing a new one.

I'm working out how the body dropdown should stay in sync: it only needs rebuilding when the mechanism changes, and any selected body that doesn't belong to the new mechanism gets reset. The other selects are filled once at startup, and I'm counting document types for their options.

I'm laying out the filter chips and accordion: each filter section opens one at a time, and the active chips name the keyword, mechanism, body, type, state, year range, SDG and any themes that are applied.

I'm laying out the Tab 02 detail view: a search field with a label, and a table caption showing how many of the matching records are displayed, sorted newest first, along with the source. Keywords get split into words for highlighting, and each row's detail is built from its text, with a large paragraph number or a dash when there isn't one. SDG numbers will show alongside their names.

I'm setting up the table's row handling: each record gets a main row, and its detail row is only built the first time it's expanded. Toggling will show or hide the detail and update aria-expanded, and I'm weighing whether to re-render the rows or patch the DOM so keyboard focus stays on the row.

I'm wiring the click handling on the table body so a copy button copies the citation, links are left alone, and any other click on a main row toggles its detail. I'm weighing whether to create each detail row on first expand and flip its visibility in place, so keyboard focus stays on the row.

I'm setting up the table rows so each main row is focusable and carries an expanded state. Expanding a row fills its detail only the first time, and "show more" appends rows rather than re-rendering. A filter or sort change does a full re-render and clears the expansions. Copy buttons inside the detail row are the only clicks I handle there.

Writing the copy helper now, with a fallback path if the clipboard API fails.

I'm writing the check-rendering helper now, mapping each status to a mark and label. Failing checks get a red mark and warnings a separate one, with the detail shown in its own column.

I'm writing the sample section as its own container, so it can re-render on interaction without touching the checks, and I'll keep focus on the sample header after each toggle.

Now I'm settling the Method tab text: every figure comes from a plain loop over the records, with no estimates, no model calls and no network requests. Records are paragraphs from UN documents, deduplicated by document symbol, and the year comes from each document's date. Filters combine with AND, and themes are the UN's labels as supplied, where one record can carry several.

I'm writing the Method tab text now, starting with how every figure is calculated and the note that labels come from the UN index rather than from this app.

Still writing the stylesheet: a paper-toned background, dark ink, and a single red accent, with the monospace labels in uppercase.

I'm laying out the rest of the stylesheet: a centred container with the header rule, the tab row, and a two-column grid with a fixed filter rail. Tabs are mono-styled buttons, with the selected one in red and a red underline. Notes get a short muted paragraph with a "How this is computed" label, and the summary tiles use a responsive grid with large serif numbers.

Next I'm writing the click handler for the table body, where a copy button copies the citation and links are left alone.

Now I'm writing the record-parsing step: pulling the paragraph number from the start of each text, and the state from the trailing parenthesis.

Now I'm writing the state-extraction step, which only applies to UPR records: it reads the parenthesised recommending-state group at the end of each text and splits it into individual states.

I'm working out the rest of the record-parsing step, where the Recommending State comes from the trailing parenthesised group in each UPR text, split into individual states and kept only if each one is short and has no commas.

I'm writing the filter logic now: each record must pass every active filter, and year bounds exclude records that have no year.

I'm writing the filter logic for the theme and state checks, with a keyword match on the lowercased text. Then I'm building a helper that tallies the top ten themes by record count, along with each theme's year range.

I'm checking the theme tally by counting each theme once per record, using a plain object for the counts and sorting the top ten from those. I'll also handle records with no year so the year range stays accurate.

I'm working out the chip list and how removing a chip resyncs the controls, and I'm about to build the body options from the unique bodies in the file.

Now I'm laying out the overview tiles: a total count of records with the breakdown by type, the distinct document count, and the year span, followed by a tile per mechanism.

Now I'm rendering the overview tiles: the total record count with the types present, the distinct documents and year span, then a tile for each mechanism showing its count, latest year and share of the filtered set. The UPR tile gets a button to open the States panel.

I'm writing the tab-two render next: it will reset the table's row list, sync the search box, and keep the sorted rows and shown count, with renderRecords filling the first fifty rows and toggling the show-more button.

Now I'm writing the row markup: each main row is focusable with an expanded state, showing the date, body, symbol link, paragraph number, state and first line of text, with a hidden detail row beneath it.

I'm setting up the state cell, which lists the recommending states or shows a "State not found" note, and the safe-URL helper that falls back to a hash link unless the address starts with http.

Writing the check-rendering code now, with a count comparison first, and I'm building the partition sums next.

Still working on the sanity checks: I'm building the partition totals by counting records per mechanism with independent filters, so a record missing its mechanism will show up as a failure.

I'm building the sanity checks for the figure: comparing the bar values from the shared top-themes function against a second, independent count, and checking that the table rows match those bars. I also want the largest bar to stay within the filtered record total.

I'm working through the duplicate check now: counting how many text values appear more than once and how many extra records that adds up to, flagged as a warning when any are found. I'm also deciding whether to list the affected symbols.

I'm writing the sample section now, using a seeded random generator so the same records get drawn each time, and shuffling a copy of the filtered list in file order to pick up to ten.

Now I'm setting up the sample section: a seeded random draw over the filtered records in file order, picking up to ten, with a seed input and buttons to draw again or draw with the entered seed.

Now I'm writing the method tab: a download button and a copy button, with the summary text built from the country, the filters in use, the matching and total record counts, the document count and year span, the breakdowns by type and mechanism, and the ten most frequent themes.

Now I'm writing the download step: the filtered rows go out as a CSV blob in file order by date, with a status line reporting how many rows were prepared.

I'm setting the rail up as a static block in the HTML, with ids for the count, the progress bar, the chip list and the accordion, and I'll fill the selects from JavaScript. The chip-removal path for the keyword filter needs to clear both keyword inputs as well.

I'm laying out the rail's markup now: a static block with ids for the count, progress bar, chip list and accordion, with the selects filled from JavaScript. Next I'm setting up the records-tab search box and the chart wrappers, and I'm checking that the overview container is visible before the charts draw.

Still writing chart helpers...

Still writing chart colours...

I'm putting together the source note for each figure, with the chart description and the table fallback, and I'm working out how the FIG.02 table should lay out its year rows.

Now I'm writing the accordion code, so each section header toggles its panel and closing one section closes the others.

I'm wiring up the filter controls: the mechanism and body selects reset the body choice when the mechanism changes, and the year and SDG selects update the filter state. The year selects swap their values if the range is reversed, and I'm filling the year and SDG options from the records as the page initialises.

Now I'm setting up the state options, counting each record once per state and sorting by count and then name. Next I'm wiring the clear-all control to reset the filters and sync the inputs, then the main update step that recomputes the filtered rows and re-renders the rail and active tab.

I'm wiring the overview's states button through a delegated click on the body container, re-rendering after it's clicked and returning focus to it. The theme chart and table buttons will add a theme and refresh the view, with each button carrying an index into the current top-themes list rather than the raw theme text. Finally I'm setting the header's year range and the rail's "matching records" label.

Still writing highlight helper...

Still writing the detail panel markup, with a labelled block for each set of items.

I'm writing the detail panel's markup now: a large paragraph number, then the full text with highlights, and a labelled block for each set of tags.

Still writing the detail panel markup: a large paragraph number, the full text with highlights, and a labelled block of tags for each set of themes, SDGs, targets and affected persons.

I'm finishing the detail panel markup: a large paragraph number, the full text with highlights, and labelled blocks for themes, SDGs, targets and affected persons, plus the copy and open-document actions.

Still writing the timeline helper, grouping the records by year and mechanism for the chart.

Now I'm finishing the export and the tab layout, with the CSV columns, the header comments for source, filters and row counts, and the active-tab state.

Still writing the tooltip and the table fallback for each chart, reusing the same esc helper so labels stay safe.

Still writing the overview tiles and the explanatory paragraph, with the record count, document count and year range, plus an empty-state message for when nothing matches.

Still writing the HTML document, with the metadata and page layout.

