I'm settling on the format for the full app: one complete HTML document in a single code block, with at most a few short sentences before it and nothing after. I'm keeping it compact, under about 1500 lines, while covering every requirement. The header will carry a monospace "UHRI · Kenya" label and a serif title about the UN human rights recommendations and observations for Kenya.

I'm checking the header details next: the label and title both take the country from the data file. Then I'm going through the source line, the left-rail filters, and how the headings and tabs appear on each view, and working out whether the click count stays within the limit.

I'm sorting out the filter setup: the Type control goes in the section 02 rail rather than on the overview tile, which will just show the breakdown by type. Next I'm sketching the overview tiles for the total, documents, and year span, plus a per-mechanism tile with its own share and note. I also want a themes bar chart whose clicks add theme chips, which means a new chip type to handle.

I'm laying out the records tab next: a search box synced with the keyword filter, a caption, and a table with Date, Body, Symbol, Para., First line, and the recommending State for UPR rows only. Rows sort by date descending by default, with a click on the Date header reversing the order, and matches get highlighted in the text.

I'm wrapping up the remaining details: the footer line with the record count and a source link, and the Method tab with its plain-language notes, a CSV download built from a Blob, a copy-summary button, and the source, licence, and build date. The Records tab's Recommending State column stays limited to UPR rows, with a matching state filter in the rail.

I'm working out the filter logic for the rest of the app: a year range that swaps if reversed, and a goal selector built only from the SDG goals actually present in the records, with names drawn from the lookup and a fallback label. The keyword box in the left rail and the search box on the Records tab will share one state, debounced so typing stays smooth. I'm also checking the paragraph-number pattern so it reads the leading number correctly from entries like "144.43".

I'm checking the paragraph-number pattern against entries like "144.43" and "71." so that the leading number is read correctly, and I'm working out how the recommending-State pattern pulls out the bracketed country names from the end of each line.

I'm checking how the Venezuela-style nested parentheses get matched, so the regex keeps the whole bracketed name together. Then I'll split the trailing run into its top-level groups and strip the outer brackets from each, so that a name like "Venezuela (Bolivarian Republic of)" comes out intact.

I'm checking how the State field handles parentheses that contain a comma, such as "(Iran, Islamic Republic of)". My plan is to drop those groups and keep any others that qualify, falling back to "State not found" only when nothing is left, and to note that rule in the Method tab.

I'm sorting records by date descending, then by body, then by paragraph number with missing numbers last, falling back to file order. For the timeline I'm using the filtered records' first and last years, with an empty chart if nothing matches. The themes chart will show the top ten themes in the filtered set, ties in alphabetical order, with percentages to one decimal.

I'm working out the checks panel: first the record count against the headline number, then whether the mechanism, body, and year counts add back up to the full record total, and whether the type breakdown matches the headline figure. I'm also planning to confirm the themes chart matches its table and that the largest bar stays within the filtered count, and to check that each document link points to the UN documents site and ends with its symbol.

I'm going through the checks panel for the data: comparing the paragraph-number share per mechanism against the 100% expected for UPR, and listing any records without a recommending State alongside their symbols. I'm also looking for duplicate IDs and text entries, and noting which fields like themes, SDGs and affected persons are not labelled in the file.

I'm settling the bar chart details: red bars at 80% opacity with each count drawn at the end of its bar by a small inline plugin. The stacked chart for mechanisms will use the chart's own legend and mechanism colours, and each tile gets a matching coloured dot.

I'm settling the filter state as a single object covering keyword, mechanism, body, type, state, year range, SDG and themes, with clicking a bar or theme chip adding a removable theme chip that combines with the others.

I'm settling the headline tiles, which will show the file total as a fixed figure, while the per-mechanism tiles use the filtered counts for records, documents, latest year, and share.

I'm deciding that the headline tile shows the whole file's total, with a breakdown by type, and that the documents and years tiles follow the same fixed file-wide figures while the mechanism tiles stay on the filtered set.

I'm settling the mechanism select with its three options and their colours, then the body select, which lists only the bodies in the chosen mechanism along with their file-wide counts. The type filter comes next.

I'm setting the year selects to run from the earliest to the latest year in the file, with the range swapping if the ends are reversed, and showing a "Years" chip only when it narrows the set. The SDG select will list only the goals present in the records, and the keyword box in the rail will stay in sync with the search box on the Records tab.

I'm laying out the records table: rows filtered and sorted, with keyword matches highlighted in the text using escaped patterns built into safe DOM nodes. Clicking a row will open a detail row beneath it, and the row itself will be keyboard-focusable with its expanded state exposed.

I'm moving on to the records table's detail view: each row expands in place to show the full text and labelled fields, with a copy-citation button and a link to the UN document. I'm also planning pagination at 50 rows with a button to load more, and a caption that flips between newest-first and oldest-first when the date header is sorted. I'm considering how to expose the sort state on that header.

I'm setting the table's column order: date, body, symbol, paragraph number, first line, and recommending state, which only applies to UPR records and shows a dash otherwise. The state cell will join multiple states with semicolons, fall back to "State not found" when none is listed, and I'm still weighing whether that wording suits UPR rows with no state. The symbol will link to the source document, and clicks on that link must not toggle the row's detail view. Below the table, a caption will state the shown and matching counts and the sort direction, and a source line will credit the UHRI and OHCHR data. Last, the Method tab needs a handful of sentences covering the CSV and summary copy buttons and the source, with the licence line pointing readers to the source link since the file has no licence field.

I'm writing the CSV export next: a few comment lines with the country, source, build date and filters, then a header row and one row per filtered record in table order, with quotes escaped and a hidden link to download it. The summary copy will give the headline counts, year span, mechanism split and top ten themes for the filtered set. After that comes the checks panel, which runs a set of consistency tests on the data.

I'm working out the Method tab copy and the checks panel next. The file's first-line text gets cut at 120 characters, at the last space before that, with an ellipsis only when it's actually shortened. I'm also planning a "see the States" link under the UPR tile that opens a list of the ten States making the most recommendations, counted against the current filter.

I'm now working out how the overview's clicks will behave: the three tabs and three headings, plus the check button and the "see the States" link, all count as clickable. For the themes chart, I'm drawing the top ten themes from the filtered records as horizontal bars, so clicking a bar will add that theme as a chip if it isn't already one. I'm also deciding that the chart gets rebuilt from scratch on each overview render, which keeps things simple with Chart.js.

I'm checking the chart against the table: I'll recount each of the top ten themes from the filtered records and confirm the bar values match the rows, with no bar exceeding the filtered total. For the timeline, I'm building a year axis from the earliest to latest year in the filtered set and zero-filling each mechanism's series. Dates sort correctly as ISO strings, and numbers will be formatted for en-GB.

I'm finishing the date ordering, since ISO date strings compare correctly as plain strings, and I'll treat any missing date as an empty string. The header's year span comes from the earliest and latest years in the file, and the document count is the number of distinct symbols. I'm setting up the records once at load, pairing each record with its index, paragraph number, recommending states and a lowercased search string.

I'm writing the keyword matcher now: the query gets split into lowercase words, and a record passes only if every word appears in its searchable text. Then I'm writing a helper that pulls the recommending state names out of the text, reading each parenthesised group and keeping only names that are short and contain no commas.

I'm pulling the State names out of each UPR record's text: a regex grabs the parenthesised groups, and each name counts once per record. Paragraph numbers come from the leading digits of the text, so "144.43" and "71." both parse cleanly.

I'm working out how to sort paragraph numbers so that 144.5 comes after 144.43 rather than before it, since a plain numeric comparison would get the decimal parts wrong.

I'm working out the sort order for the table: date descending by default, with the body, paragraph number and file index as tie-breakers. Paragraph numbers will compare as floats so that 10 follows 9, and any missing number will sort last. Clicking the Date header will reverse the direction.

I'm settling how the table's date sort will reverse: only the date comparison flips, with body, paragraph, and file index still breaking ties. Rendering the rows by hand for about 2,264 records should be fine, capped at 50 per page. For expanding a row, I'll keep a set of expanded item indices, rebuild the body on toggle, and restore focus to the clicked row via its data attribute.

I'm wiring up the filter state for the rail: keyword, mechanism, body, type, State, year range, SDG and theme chips, each chip able to clear its own filter. The keyword box stays in sync with the search on tab 02 through one shared setter, and the body options get rebuilt whenever the mechanism changes. The render step will then refresh the rail, chips, overview and table together.

I'm deciding whether the overview should render only while its tab is open or always, since charts sized on a hidden canvas can come out at zero width. I'm leaning toward rendering it always and relying on Chart.js's resize handling when the panel shows. I'm also working out how switching tabs will show and hide the panels and which rail headings stay visible on each one.

I'm settling the overview tiles: the file-wide total, a breakdown of counts by record type, plus the documents and years tiles. Then I'll finish the headings for the rail, with keyword first, mechanism and body second, and years and SDG third.

I'm settling the mechanism tiles next: one per mechanism present in the filtered set, each showing its record count, document count, latest year and share of the filtered records. The UPR tile gets a "see the States" button that opens a list of the ten States making the most recommendations to the country, counted among the filtered UPR records.

I'm now writing the self-check panel: comparing the record count against the header number, confirming the mechanism, body, year and type partitions each sum back to the total, and checking the chart bars against recomputed theme counts. I'm also flagging any broken links and any UPR paragraph-number coverage below 100%.

I'm working out the self-check panel's States section: counting how many UPR records have at least one recommending State, and listing the ones that don't, along with whatever trailing parenthesised text they hold, capped at twenty entries. Anything with missing States gets flagged as a warning.

I'm moving on to the self-checks: each record should pass, and any inconsistencies will be flagged with their values. I'm also checking the duplicate text and the records missing themes, SDGs or affected groups, showing those counts as notes rather than failures, and comparing the chart bars against the table.

Next I'm laying out the footer and the source link, and I'm fixing the colour for each mechanism so the charts stay consistent.

Next I'm setting the page's colours and fonts (paper background, ink, rule lines and a red accent, with Georgia for headings and a monospace face for labels) and planning a two-column grid with a filter rail beside the main panel that stacks on narrow screens. I'll make focus rings visible with a red outline, then start writing the code, keeping it compact at roughly 700 to 900 lines.

Now I'm working out the layout for the page: the header, the filter rail, and the tabs, with the rail stacking under the main panel on narrow screens.

I'm laying out the stylesheet next: a paper-toned palette with a red accent, Georgia headings, monospace labels, and visible red focus rings for keyboard users. The next part of the code is still being written, so I'll keep it going as the header and typography rules settle.

I'm laying out the stylesheet now: a paper-toned palette with a red accent, Georgia headings, monospace labels, and visible red focus rings. Next comes the tab bar, where arrow keys will move between tabs.

I'm defining the data constants next: the record list, the total count, the SDG name lookup, the mechanism colour map, and three patterns for parsing trailing parenthesised text and paragraph numbers.

I'm writing the state-extraction step for the UPR records: pulling the trailing parenthesised text from each record and collecting the recommending States into a set.

I'm going through how the UPR records get their trailing State groups parsed, and planning to show the raw run text when nothing is found, capped at twenty entries with a "and n more" note.

Still working out the record aggregates and the year range.

I'm building the filter logic next: a keyword match over each record's text and symbol, then filtering by mechanism, body, type, State, year range and SDG, plus any selected theme chips.

Filtering is applied per record: a record must pass every active check (mechanism, body, type, State, year range, SDG and selected themes) and match each keyword word in its text or symbol. I'm finishing the filter so each condition is checked against the record's own fields.

Writing the theme counting helper: tallying each theme's record count and its earliest and latest year across the filtered set.

I'm writing the overview render next: the total record count, a breakdown by record type, and the documents and year-range tiles from the full dataset. Then I'll build the mechanism tiles from the filtered set.

I'm building the overview's mechanism tiles from the filtered set, one per mechanism, each showing its record count, document count, latest year and share of the filtered records. I'm writing the headline and tile rendering with a small DOM helper.

Now I'm wiring up the overview's rendering, including the theme chart and its table, using a short `esc` helper for any text placed into the markup.

Still wiring up the chart code, with the theme bar chart set to horizontal bars and click handling on the bars.

I'm wiring the theme bar chart to horizontal bars with a plugin that prints each count at the end of its bar, and I'm leaving room on the right by raising the axis maximum. Clicking a bar will add that theme as a filter chip.

Still working on the chart setup: the theme bars will be horizontal, and I'm checking the table's percentages and year ranges against the chart. Next is the timeline figure, which will group the filtered records by year for each mechanism.

Now I'm writing the timeline figure: stacked vertical bars by year, one colour per mechanism, with the axes starting at zero.

I'm setting up the self-checks now, starting with the record count: comparing the total number of records against the count field in the data, and marking it as matching or not.

I'm writing the self-checks now, starting with a partition check for each grouping: summing the record counts per mechanism, body, year and type, and confirming each total matches the headline count.

Still writing the self-checks: the chart-versus-table check will recount each theme's records and compare those numbers against the values actually printed in the table cells.

Still writing the link check: each record's document URL gets decoded, and I'm testing that it points to docs.un.org and ends with the record's symbol.

Still writing the self-checks: the link check decodes each record's document URL and confirms it points to docs.un.org and ends with the record's symbol. Next I'm checking paragraph-number coverage per mechanism, and I'll start on the State tally.

I'm working out the state check: a record counts as having a State when its trailing parentheses yield at least one State, and I'll flag any UPR record without one, showing the raw trailing text so it can be inspected. Then I'll check duplicate text values by comparing the total record count with the number of distinct texts.

I'm adding the duplicate-text check, which reports how many text values appear in more than one record, marked as a warning when there are any. Then I'm flagging the records missing themes, SDGs or affected persons as informational notes, and tallying the final check count.

Still writing the table code for the records tab, a sorted and paged view with expandable rows.

Still writing the table sort: date descending by default, with body and paragraph number kept in ascending order within each date.

Still building the table: I'm writing a renderer that sorts the matching records by date, newest first by default, with body and paragraph number kept in ascending order within each date. It shows the first batch of rows with a "more" control and a caption giving the count and sort direction.

Still building the records table: I'm writing the row builder for each record, with the date, body, a symbol link that opens the document in a new tab, the paragraph number right-aligned, and the first line of the text.

Still building the detail row for each record: it's a sub-row that shows the full text, its links and its labels when a row is expanded.

Still building the detail row: it shows the paragraph number, or a note that none is in this extract, along with the full text, its labels, and buttons to copy the citation and open the UN document.

Still building the detail row: the citation button copies the symbol with the paragraph number when there is one, and its label notes when none was found. The copy handler will show a brief "Copied" confirmation for two seconds.

Still building the detail row: it lists the themes, SDGs, SDG targets, affected persons and section, and shows the recommending State for UPR records.

Still writing the highlight helper: it escapes the search words for a regex, then wraps each match in a mark element while keeping the rest of the text as plain nodes.

Next I'm finishing the highlight helper: the regex is case-insensitive and the words are non-empty, so there are no zero-length matches to guard against. I'm applying highlighting to the first line of each row and to the full text in the detail view.

Still building the search and filter wiring: the keyword box in the rail and the one on the records tab stay in sync, and both are applied 300 ms after typing. Next I'm updating the match count, the "of total" line, and the share bar width, then adding the filter chips.

Still building the filter controls: the active filters appear as removable chips, with a "Clear all" that resets everything, and the three rail sections open one at a time from their headings.

Still building the rail headings: the keyword section has a search box with a note that matching is literal and applied after a short pause, the mechanism section holds the mechanism, body, type and optional State selects, and the years section holds the from and to year selects along with the SDG select.

I'm setting up the filter controls for the rail: the mechanism select will list each mechanism, the body select will show the counts for each body, and the state select will sort the States by how often they appear among the reviews.

Still building the overview: I'm adding a panel of the ten States that made the most recommendations to Kenya, with a toggle link that opens and closes it, and the UPR tile links to it only when that mechanism is in the current filter.

Still writing the method notes and the summary builder: I'm composing the sentences on how filters combine, how theme counts and paragraph numbers are derived, and that nothing is estimated, then building the text for copying the current summary with its active filters.

Still wiring up the tab keyboard handling, so each tab responds to its own event.

Still wiring the tab keyboard handling: each tab takes its own click, and the arrow keys move between tabs with wraparound.

Still building the app's render loop: a single render pass filters the records once, then updates the rail, chips, overview and table from that set. The theme counts need to be in place before the checks run against them, and I'll keep the checks computed on every pass since they're cheap. Next is keeping focus steady when a row is expanded.

I'm writing the HTML skeleton now, with the header, a filter rail, and the main content area laid out in a two-column structure.

Still building the HTML skeleton: the header with the label, title and source line, then a filter rail with keyword, mechanism, years and SDG sections, and a main area with three tabs.

Still building the overview tiles: the total-records tile sits alongside a breakdown by type, and the UPR tile links to the States panel only when that mechanism is in the current filter.

Now I'm laying out the overview markup: a hero row with the total-records tile, the documents and years tiles, a mechanism tile row, and a slot for the States panel.

Still laying out the overview markup: the figures, the theme table, and the checks section, which opens from a toggle button with the number of checks in its label.

Still writing the records table: the header row gets a sortable date column, with body, symbol and paragraph columns beside it, and the caption is filled in with the current count.

Still writing the records markup: the date sort button, the body, symbol, paragraph, first-line and State columns, and a "Show 50 more" button beneath the table.

Still writing the records markup: the download and copy buttons sit in a row with a status line, and a data source note goes beneath the method notes.

Still writing the overview renderer: the total tile reads from the full record set, and the type breakdown is counted and sorted by size.

Still building the overview tiles: each mechanism tile shows its record count, document count and latest year, filtered to the current selection.

Still writing the overview tiles: each mechanism card shows its record count, document count, latest year and share of the filtered set, with a "see the States" button added to the UPR card.

Still wiring the mechanism tiles: each card takes its own click handler for the States toggle, so the "see the States" button on the UPR card opens and closes the panel.

Still writing the States panel: it lists the ten States that made the most recommendations, and each row shows its count from the filtered UPR records.

Still writing the chart code: I'm wiring up the theme and timeline charts and the end-of-line labels.

Still writing the theme renderer: it counts the filtered set, shows an empty-state message when nothing matches, and draws the bar chart with end-of-bar value labels.

Still wiring the theme chart: the bars take end-of-bar value labels, and the table is filled from the same ranked list.

Still wiring the timeline chart, with the year counts drawn from the filtered set and an empty-state message when nothing matches.

Still writing the timeline chart: it spans every year in the filtered set, with a dataset per mechanism that counts its records for each year.

Still writing the timeline chart: the years span the filtered records, and each mechanism gets its own stacked dataset counting its records per year.

Still wiring the rail: the match count and "of total" line update from the filtered set, and a share bar tracks how much of the file is currently matching.

Still building the filter chips: each active filter gets a removable chip for keyword, mechanism, body, type, State and year range.

Still building the filter chips: the chip list now covers the mechanism, body, type, State, year range, SDG and theme filters, and each removable chip is wired to clear its own filter.

Still writing the filter logic: the body dropdown rebuilds from whichever mechanism is selected, clearing itself if the old body no longer applies.

Still wiring the filter controls: the mechanism change clears the body if it no longer applies, the year and keyword inputs are kept in order, and the keyword box waits a moment before it applies.

Still wiring the keyword box: syncing the two search inputs to the stored keyword, and only resetting their text when it actually differs so the typing caret stays put.

Still writing the export helpers: a CSV cell escaper, then an export function that builds its rows from the sorted set.

Still writing the CSV export: the rows are built from the sorted set, starting with a header and a block of meta lines that record the filters and row count.

Still writing the CSV export: each row's cells are escaped and joined, and the blob is being built to download.

Still writing the export code: the CSV is built from the sorted rows with a UTF-8 byte-order mark, and the download link is clicked, with a copy summary to follow.

Still writing the check helpers: the theme counts are read back from the rendered table, and a runChecks function will return the results for the current set.

Still writing the accordion toggles: one open section at a time, with the Keyword, Mechanism and Years headers each flipping their own panel.

Still wiring the tabs: each tab panel gets shown or hidden with its matching selected state, and the rail headings hide on the last tab.

Still writing the page header and footer: the label line, the title about the UN recommendations for Kenya, the source line with the record and document counts, and the footer link to the data source.

Still wiring the CSS: the rail gets its fixed width, the big numbers use the serif face at 52px, and the share bar is a thin track with a filled accent bar.

Still writing the CSS: the accordion buttons are full-width with a top rule and turn accent-colored when open, the tabs get a thick bottom border on the selected one, and the tiles, big numbers and tables are styled to match.

Still wiring the CSS: the checks and state rows get their status badges and the detail rows get a tinted background, with the layout collapsing to one column on narrow screens.

Still writing the check rows: each check gets a status badge, and its detail line and optional bullet list are added under the name.

Still wiring the check helpers: the partition counts are checked against the total, and the failing symbols are collected into a short list.

Still wiring the check helpers: the partition totals are compared against the headline count, and the chart figures are being checked against the table rows.

Checking the chart values against the table rows now: each bar count gets recounted from the filtered records, and the table's numbers get read back out to compare. Any mismatch between the bars, the recount and the table gets tallied as a failure.

Still wiring the link checks: each record's document link is being decoded and matched back to its symbol, and any that don't resolve get collected.

Still wiring the link checks: each record's document link is decoded and matched back to its symbol, and any that don't resolve are collected into a list.

Still wiring the upr check: the paragraph-number share per mechanism is totaled and the UPR share gets flagged if it falls short of full coverage.

Still writing the upr check: records without a State in parentheses get listed, with a note if there are more than twenty.

Still writing the checks: the ids are counted for distinct values against the total, and duplicate text values are tallied, with a warning if any turn up.

Still writing the checks: the remaining checks cover the unlabelled themes, SDGs and affected persons, each counting the records that have no entry.

Still wiring the checks: the remaining checks cover the unlabelled themes, SDGs and affected persons, each counting the records that have no entry.

Still writing the CSS: the page gets its paper background and ink text, the accent colour is set, and focus outlines are added for keyboard users.

Still writing the CSS: the rail gets a sticky position with a dark top rule, and the layout is a two-column grid that puts the filter rail beside the main content.

Still styling the rail: the top row, the link button, the large number, the share bar and the chips.

Still writing the CSS: the accordion buttons get a mono label with a plus or minus marker, and the section bodies get their select and input styling.

Still writing the CSS: the heading styles are being set, with the rules for the tab bar and the hint text just before them.

Still writing the CSS: the grid gets a three-column layout for the mechanism cards, and the tile, number and dot styles are being set.

Still writing the CSS: the table cells get their padding and bottom rules, and the chart and source line are styled to sit under each figure.

Still writing the CSS: the table rows get a hover tint, the cells get their right-aligned number styling, and the search row is laid out as a flex line with the input growing to fill it.

Still writing the CSS: the detail cells get a tinted background with extra padding, the big numbers use the serif face in accent color, and the full-text block gets its line spacing and a readable width.

Still writing the CSS: the labels list gets its two-column grid with mono uppercase terms, and the check rows and their status badges are styled.

Still writing the CSS: the badge styles get their warn, fail and note colours, the list under each check is indented and muted, and the states box and footer get their rules.

Still writing the CSS: the sidebar's bottom edge, the accordion toggles, the form controls, the tab bar, and the card and table styles are being set, and the layout collapses to a single column on narrow screens.

Still writing the markup: the header, the sidebar's top row with the clear button, the match count and share bar, the chips, and the first keyword accordion section.

Still writing the markup: the keyword and mechanism sections of the sidebar are being filled in, with the mechanism selects set up in the body section.

Still writing the markup: the sidebar's keyword, mechanism and year sections are filled in, and the main column's tab bar is being set up.

Still writing the markup: the tab bar gets its three tabs, with the first one selected and the other two set to be skipped in tab order.

Writing the overview panel: the two hero tiles show the total record count with its type breakdown, and the document count, each with a short note on how the figure is computed.

Still writing the markup: the overview panel's hero tiles, mechanism tiles and the first figure's chart box are in place, with the canvas being set up.

Still writing the overview panel: the record and document tiles are filled from the file, and the theme chart and its matching table are being set up with their source note.

Still writing the markup: the search row and the records panel are being laid out.

Still writing the records panel: the search field and the table's header row are set up, with the date sort button in the first column.

Still writing the markup: the method panel's ordered list is filled in from script, followed by the CSV and summary buttons and the data line.

Still writing the script: the constants and small helpers are being defined, covering escaping, number formatting, percentages and slugs.

Still writing the script: the data constants are set, with the country name, the source label, the record list and the per-mechanism colours defined.

Still writing the script: the record list is being mapped into items, each with its paragraph number, its mechanism colour, and the states named in its trailing parenthetical.

Still writing the script: the record items are being built, each with its paragraph number and the states named in its trailing parenthetical, and the year list is being derived next.

Still writing the script: the year list and the state counts are being built from the record items.

Still writing the script: the year list and the state counts are being built from the record items, with the state tally keyed by name.

Still writing the script: the state tally is keyed by name, and the filter state and the sidebar accordion toggles are being wired up.

Still writing the script: the select options are being filled from the record data, with mechanism, body, type, state, year and SDG values each getting their counts.

Still writing the script: the year and state filter controls are being synced with the current filter, and the keyword inputs are being checked so typing isn't overwritten.

Still writing the script: the filter sync is kept separate so the keyword inputs are left alone unless the keyword path calls it, and the body dropdown is being filled from the records for the chosen mechanism.

Still writing the script: the mechanism and body dropdowns are wired so that picking a mechanism repopulates the bodies and re-renders the list.

Still writing the render path: the filter sync, the rail, the chips and the overview are being called in order, with the table rendered last.

Still writing the table renderer: the rows are sorted, the first page is sliced off, and the body is being cleared before the empty-state check.

Still writing the table renderer: the rows are being drawn into the body, with the caption and the date sort label updated to match the current order.

Still writing the table rows: each row gets its click handler and keyboard focus, and its expanded state is tracked for the detail row.

Still writing the table rows: each row's date, body, symbol link and paragraph number are being filled in, with the states column set from the record's parenthetical.

Still writing the table rows: each row's date, body, symbol link and paragraph number are being filled in, with the states column set from the record's parenthetical.

Still writing the table rows: the keyboard focus is restored after each toggle, and the detail row's markup is being started.

Still writing the detail row: the cell spans the table, and its label rows for mechanism, type, section, themes, SDGs, targets and affected persons are being set up.

Still writing the detail row: the label list for mechanism, type, themes, SDGs and targets is being built, with missing values shown as not labelled.

Still writing the detail row: the label list is being built from the record's mechanism, type, themes, SDGs and targets, with the recommending State added for UPR entries and missing values shown as not labelled.

Still writing the detail panel: the header line with the body, date and symbol is set, followed by the paragraph number, the full-text area and the label list.

Still writing the detail panel: the paragraph number and the full text are filled in, with the labels and a copy button and a link to the UN document added.

Still writing the script: the copy helper is being wired to the clipboard, with a fallback for browsers without it, and the button label flips to "Copied" for two seconds before reverting.

Still writing the script: the sort comparator is being defined to order rows by date, then body, then paragraph number, with the original index as the final tiebreak.

Still writing the script: the sort comparator and the first-line helper are being defined, and the search-word list is being built from the keyword filter.

Still writing the script: the chart end-labels plugin is being defined to draw each value next to its bar, and the theme renderer is being started.

Still writing the theme renderer: the top-ten table rows are being built with each theme's count and share of the filtered records.

Still writing the theme chart: the bar colours and tooltip labels are set, and the top-ten table rows are being built with each theme's count, share and year span.

Still writing the theme chart: the bar tooltips and axis scaling are being set, and the chart's click handler is adding the clicked theme to the filters.

Still writing the overview: the total count is being set, and the summary figures for the filtered records are next.

Still writing the overview: the mechanism tiles and the chips are being set up.

Still writing the chip row: each active filter gets a button that clears it and re-renders, and the keyword filter also needs its own reset path.

Still writing the filter reset: the keyword debounce handler will sync both inputs to the typed value before re-rendering, and the chip and clear paths will blank both keyword boxes directly.

Still writing the script: the Method section is being set up, with the sentences about how records are counted, how documents and years are dated, and how filters combine.

Still writing the Method section: the six sentences cover how records are counted, how documents and years are dated, how filters combine, how theme counts work, what a paragraph number and recommending State mean, and that nothing leaves the page except the clipboard and CSV download.

Still writing the footer: the source line is being added with a link to the OHCHR data, the build date, and a note that the licence is on the source page since the file carries no licence field.

Still writing the footer: the tab keys are being wired so arrow left and right move between the three tabs.

Still writing the script: the Chart.js plugin list, the canvas accessibility labels and the header's source line are being wired in next.

Still writing the render checks: the check list is being set up with its pass, warning and fail labels, and each result gets rendered into the list.

Still writing the render checks: each result is rendered as a list item with its name, a pass, warning, failure or info badge, and any supporting detail lines.

Still writing the checks: the cross-check that the largest bar matches the filtered count is in, and the table's theme rows are being compared to the bars.

Still writing the summary helper: it builds the top themes, the document and year counts, and the per-mechanism totals.

Still writing the summary helper: the copy text is built from the country line, the filtered and total record counts, the document and year span, the per-mechanism totals, and the top themes.

Still writing the final message: a short preface, then the single HTML block with nothing after it.

Still writing the data helpers: the select options for the year range and filters are being filled from the record counts.

Still writing the filter selects: the mechanism, type and year options are being filled in with their record counts.

Still writing the select fillers: the goal options are being built from the SDG list, and the State dropdown is sorted by record count and hidden when there are no States.

Still writing the filter helpers: the state dropdown is being built and hidden when there are no States, and the chip labels for the mechanism filter are being set.

Still writing the render helpers: the mechanism tiles each get a states toggle, and the panel either shows the State list or stays closed depending on the open flag.

Still wrapping up the state handling: the state panel is hidden by default, and the mechanism tiles' toggle is wired so the list opens and closes in the same render pass.

