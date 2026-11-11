I'm reading the attached UHRI data to build the app, which means writing a single complete HTML document in one code block. I'll take the country from the data's country field, and the header will show a monospace "UHRI · Kenya" label above a serif title about UN recommendations and observations for Kenya, with a linked source line and the record count.

I'm working out the rest of the layout for the app: the header details like the record and document counts, the years and built date, and then the left rail with its filters. The three filter sections start closed and open one at a time, and the rail trims down on the third tab.

I'm weighing whether the "Clear all" button should always show or only when a filter is active, since the count of clickable items in the view is running a bit over the target of about seven. Showing it only when a filter is set would bring the count back in range without losing anything useful.

I'm settling the tab labels as 01 Overview, 02 Records, and 03 Method & Export, since the spec calls for three. The Type filter belongs under rail heading 02 only, so I won't duplicate it on the Overview tab.

I'm settling the Type filter so it lives only in the rail under heading 02, starting on "all", and I'll note that in the tile rather than adding a second control. Each mechanism gets its own tile with records, documents, latest year, and share of the filtered set, plus a short "see the States" list that opens in place.

I'm sketching the rest of the app: a Chart.js bar chart of the ten most frequent themes that adds a theme as a filter chip when clicked, with a table beneath it, and a stacked records-per-year chart after that.

I'm laying out the Records tab next: a search field synced with the rail keyword, a table with date, body, symbol, paragraph, and first line (plus the recommending State on the UPR view), sorted newest first with a toggle on the date header. Matches get highlighted, rows load fifty at a time, and clicking a row expands it in place to show the full text and its labels.

I'm thinking about the row expansion now: clicking a row should reveal the detail beneath it, so I'll track which rows are open in a set keyed by id, since the rows are rendered fifty at a time. The open state is what makes the expansion work across those chunks.

I'm wiring up the expandable rows now: the first-line cell holds a button with aria-expanded, and clicking the row toggles the same state, so keyboard and mouse both work. Highlighted keyword matches will show up in the first line and in the expanded full text.

I'm working out how the table sorts: by date, with the newest first by default and a click on the Date header flipping that direction, then body alphabetically, paragraph number ascending, and file order as the last tiebreaker. I'm deciding whether a date-header click should reverse only the date part or the whole ordering, and I'm leaning toward reversing just the date.

I'm laying out the rest of the Method & Export tab: a short method note, a CSV download of the current filter with commented header lines, and a copy-summary button that puts the headline numbers into plain text.

I'm settling the footer and the licence line: the data file doesn't state a licence, so I won't invent one and will point readers to the source page instead.

I'm writing the Check panel's rules now: the record count against the stated total, the partition sums for mechanism, body, year and type, and the chart values against the table. Each check gets a pass or fail, and I'm also setting up a link test that the document URLs point to the UN docs site and end with the symbol.

I'm writing the Check panel's remaining rules: each UPR record should have a paragraph number and a recommending State, so I'll flag shortfalls as warnings, and I'll verify that the document links point to the UN docs site and end with the symbol. Records with no themes, SDGs, or affected persons will be reported as unlabelled, and duplicate text will be counted.

I'm checking the regex that pulls the recommending State out of each record's text, and I'm noting that it strips the outer parentheses and rejects any group containing a comma or longer than 60 characters, so that stray text doesn't get counted as a State.

I'm settling the State extraction: I'll keep only the groups that have no comma and are at most 60 characters, count each accepted group once per record, and mark a record "State not found" when none of its trailing groups pass.

I'm settling the State filter: it will match exactly on the extracted state name, and the state select only appears when at least one State is found in the file. The UPR tile's "see the States" link will open a plain ordered list of the top ten States by record count for the current filter, with no extra buttons.

I'm finishing the keyword filter: every typed word has to appear in either the text or the symbol, matched case-insensitively. The year selects will list only years that actually have records, though the timeline still shows the gaps.

I'm working through how the year filter behaves: the from and to selects default to the full range, and a chip only shows when the range is narrower than that, with reversed bounds swapped on change. For the SDG filter, I'm listing only the goals that actually appear in the records, using the numeric goal values and their names, alongside the mechanism and body selects.

I'm settling the filter chips: each active filter, whether keyword, mechanism, body, type, state, year range, SDG, or theme, gets a removable chip with its own label and an aria-label, and I'm weighing whether that many buttons on the first tab is too much.

I'm settling the Keyword search so the rail input and the tab 02 field share one state, and I'm keeping the rail headings closed until clicked, with only one open at a time.

I'm settling the keyword search so the rail input and the tab 02 field share one value, with the tab 02 box as the primary input and both updating on a 300ms debounce.

I'm building the rendering pipeline: one render function that filters the records and updates the rail, chips, tiles, theme chart and timeline chart, with the table shown fifty rows at a time. For the two Chart.js bar charts, I'll keep the instances and update them, and clicking a theme bar will add a theme filter chip unless it's already active.

I'm settling the chart colours and labels: the UPR bars will be a red at 80% opacity, the stacked FIG.02 bars get a distinct colour for each mechanism, and the Chart.js legend will serve as the label for the stacked chart.

I'm skipping the compact table under FIG.02 and keeping that table to FIG.01, since the spec only asks for it there. For the stacked chart I'll plot counts per mechanism across every year from the first to the last, zero years included. I'm setting up Chart.js 4 with a horizontal bar config for FIG.01, and I'll draw the value labels at the end of each bar with a small inline plugin rather than a separate library.

I'm laying out the per-mechanism tiles, each showing a colour dot, the label, the record count, the distinct document count, the latest year, and the share of the filtered set, with a dash for the share when nothing matches. I'm formatting numbers in UK style with one decimal place for percentages. I'm still deciding whether the headline tile's record count should follow the active filters or always show the whole file.

I'm weighing whether the headline tile should show the whole file or the filtered set, since the spec asks for the full count but also wants every tab on the same filtered data.

I'm wrapping up the headline tile: it will show the filtered record count against the total in the file, with a per-type breakdown of the filtered set, and with no filter applied it simply reads as every record. The Documents and Years tiles will use the filtered set too, so every tab stays on the same data. The header line still needs the source link, the record and document counts from the file, the first and last years, and the build date.

I'm now setting the footer line and the Method tab text, which will describe the method in generic terms rather than with hard-coded figures. I'm also planning the CSV export, with a header row and a few "#" comment lines at the top, quoting every field and doubling any embedded quotes before building the file as a Blob.

I'm now covering the clipboard side: the summary and citation copy will use the same helper, falling back to a hidden textarea and execCommand when the Clipboard API is blocked, and a "Copied" confirmation will show afterwards. I'm also checking each panel's checks so every line gets reported as a pass or a failure.

I'm writing the duplicate check now: it counts texts that appear more than once and the records involved, and I'm leaning toward reporting it as a warning rather than a failure.

I'm checking the per-mechanism shares against the paragraph totals, expecting full coverage for UPR and treating the other mechanisms as informational for now.

I'm now deciding how the "Links" section should work, though I'm still undecided on whether the state-check list should sit in a collapsed block to save space.

I'm checking which records fail the link check, listing each one by its symbol and document URL. I'm also working out whether the record IDs are unique, which means comparing the distinct count against the total. Then I'll set up the data preparation: each record gets its paragraph number, and UPR records get their listed states extracted from the text.

I'm checking the record preparation next: each record gets its paragraph number from the leading digits of its text, and UPR records get their listed states pulled out of the text too.

I'm writing the extractStates helper now, pulling the trailing parenthesised groups from each UPR record's text and keeping the ones that look like state names.

I'm writing the extractStates helper as a regex over the trailing parenthesised groups, keeping only the ones that look like state names, and deduplicating them within each record.

I'm checking the regex used to pull trailing state names: it scans the text with nested groups, and I'm confirming it can't backtrack badly on texts of a few thousand characters.

I'm writing the matches filter, which checks the mechanism, body, type and state filters in turn, and I'm building the state list for each UPR record from the trailing parenthesised groups.

I'm writing the filter function for the records, which checks each one against the active mechanism, body, type, state, year range, SDG, theme and keyword filters. For the keywords, every word has to appear in either the record's text or its symbol.

I'm writing the filtered theme counts for the chart: tallying each theme's count and year range over the filtered records, sorting by count and then label, and keeping the top ten. I'm also planning a cross-check that recounts those ten themes with a separate loop and confirms they match the bars and stay within the filtered total.

Now I'm sorting out the table: it'll show the filtered records in batches of fifty, with the date, body, symbol link, paragraph number, first line and state for each row, and the date header will be a sortable button.

Still writing table rows...

Still building the detail panel: the paragraph number in large red type or a note that none is present, then the full text, and labels for themes, SDGs and targets, affected persons and section, showing missing ones as missing.

Still writing the table rows...

I'm wiring up the table rows so that clicking a row expands its detail. Because the first-line button sits inside the row, I'll attach the click handler only to the row itself so a single click toggles it once, and stop link clicks from toggling as well.

I'm wiring up the table rows so a click on the row toggles its detail, while links inside the row are left alone. The toggle sits on the row itself, so the first-line button, which bubbles its click up to the row, only triggers it once.

Still building the filter rail: a live match count and share bar, the active-filter chips, and collapsible filter groups that hide on the timeline tab, with a Clear all button at the top.

I'm now laying out the filter rail's contents: the keyword group with a literal-match hint, a mechanism, body, type and state group where the state select only appears if states exist, and a year and SDG group. Only one group opens at a time, and the whole group list hides on the timeline tab.

Still writing the filter rail's active chips and the tab controls: each active filter gets a removable chip, and the tabs get arrow-key navigation.

I'm laying out the overview tab now: a serif heading asking what the UN has said and how much, then a row of headline tiles. The main tile shows the filtered record count with a per-type breakdown, and a short note explains how that number is computed and where the Type filter lives.

I'm now placing the overview's mechanism tiles, one per mechanism present in the data, each showing its records, documents, latest year and share. The UPR tile gets a small button that opens an in-place list of the top ten States that made recommendations to Kenya, with a note on how that count is computed.

I'm laying out the overview's headline tiles next: a large record-count tile with a per-type breakdown, plus a document and year range tile, each with a short note on how the number is computed. The UPR tile gets an in-place list of the top ten States making recommendations, and a figure below will chart the most frequent themes.

I'm laying out the overview tab's remaining pieces: a per-theme table with the same ten rows as the chart, then a stacked chart of records per year by mechanism, each with a note on how it's computed. A collapsed list of checks sits below, and I'm counting the clickable controls on that tab to see whether it stays manageable.

I'm laying out the methods tab now: a few plain sentences on how each number is counted, plus the two export buttons and the data source line.

I'm finishing the methods text: every figure is computed in the browser from the file, theme counts overlap so they exceed the record total, and keyword search is literal. Then I'm adding the two export buttons and a source line with the licence and build date.

Still writing the Chart.js end-of-bar label plugin.

Still writing the Chart.js label setup, with the bar labels placed just past each bar's end.

Still writing the Chart.js setup: the bar chart gets room past its longest bar and a click handler that adds the clicked theme as a filter, and the year chart is set up as stacked bars by mechanism.

Still writing the Chart.js setup and the record-count check.

Still writing the consistency checks: a record count against the declared total, and each mechanism, body and year breakdown summing back to the same number.

I'm writing the link check: each record's document URL is decoded and must start with the UN docs address and end with its symbol, and any failures get listed by symbol and URL.

Now I'm writing the checks on duplicate IDs and repeated texts, and tallying records that have no themes, SDGs or affected persons so they can be shown as not labelled.

I'm finishing the check panel: each check gets a name, its compared values, and a status mark. Passing checks show a tick, warnings show in amber, and failures show in red with the failing items listed in a scrollable monospace box.

I'm wiring the search box so both inputs stay in sync and update the results after a short pause. I'll also check that the charts still size correctly when their tab was hidden on first load.

Still writing the filter selects: the mechanism dropdown lists each value present in the data, and the treaty body dropdown narrows to the chosen mechanism with counts shown beside each name.

Still writing the Clear all button, the active filter chips, and the sort and tab handling for the records table.

Now I'm writing the record-count check and the partition checks, which sum the counts per mechanism, body and year back to the total. Next come the link checks, confirming each document URL starts with the UN docs address and ends with its symbol, followed by the duplicate and unlabelled-record tallies.

Still writing the Chart.js setup and the helper that builds the page's DOM elements.

Still writing the element helper: it sets classes, text, event handlers, and attributes, then appends child nodes.

Still writing the highlight helper: it splits each text on the search terms and wraps the matches in mark elements.

Still writing the helper that formats long text in the records table: it keeps the first sentence or so, cutting at the last space before the limit and adding an ellipsis.

Still writing the helper that cuts long text to a first line, breaking at the last space before the limit and adding an ellipsis, and I'm working out how the records table will show that line with search matches highlighted.

Still writing the JavaScript data setup: I'm defining the country, the SDG name lookup, and the mechanism colours, then starting to map each record.

Still writing the record setup: each record gets its text, year, paragraph number, themes, SDGs and states prepared, with the Universal Periodic Review records getting their recommending States pulled from the text.

Now I'm defining the sorting key for the paragraph numbers, splitting each into a main and sub number so that 144.43 sorts after 144 and before 145.

I'm building out the record preparation and the filter logic for the records table, then setting up how the mechanisms and treaty bodies are listed.

Still writing the render pipeline: each refresh filters the records, then updates the rail, overview, table, and, if the panel is open, the checks.

Now I'm wiring up the filter controls: the body dropdown gets rebuilt on each render with counts, and the chips, clear button, and selects all stay in sync with the current filters.

Still writing the select setup: the mechanism dropdown lists each mechanism with its file count, and the treaty body dropdown narrows to the chosen mechanism.

I'm filling in the year selects now: the start defaults to the earliest year in the data, and if the two ends are reversed they get swapped. When both ends cover the full range, the year filter counts as inactive.

Still writing the chip labels and their remove buttons, which clear the matching filter and refresh the page; I'm also making sure the mechanism choice drops the treaty body if it no longer belongs to that mechanism.

Still writing the filter helpers: the keyword is stored lowercase and trimmed, and the Empty-state handling will hide the charts and show a message when no records match.

I'm laying out the overview tiles now: the headline tile shows the record count with a breakdown by type, the Documents tile counts distinct symbols, and the Years tile shows the earliest and latest year in the filtered set.

Now I'm laying out the mechanism tiles as a grid, each with a coloured dot, the record count, and a line for documents, latest year and share of the filtered set. The UPR tile gets a "See the States" button that opens a short list of the top ten recommending States, with counts for the current filter.

Still writing the theme chart: I'm tallying how often each theme appears in the filtered records, keeping each theme's year range, and sorting to the top ten.

Still writing the timeline: I'm building a year-by-year series for each mechanism, counting the filtered records in every year.

Still writing the timeline's per-year counts, giving each mechanism its own colour and keeping the chart's data up to date on each refresh.

Still writing the CSV export: I'm building the header comment lines with the country, source, build date, active filters, and row count, then writing the column headers.

Still writing the CSV export: the header lines carry the country, source, build date, active filters and row count, and each record's full text, labels and dates go into the columns.

Still writing the copy-to-clipboard helper: it tries the clipboard API first and falls back to a hidden textarea if that fails.

Still writing the export helpers: the CSV builder escapes each field, the download link saves the filtered rows, and the copy-summary step falls back to a hidden textarea if the clipboard API fails.

Now I'm adding the expandable detail rows, showing each record's full verbatim text alongside its labels, SDGs and targets.

Still writing the table renderer: it sorts the filtered records and builds each row with its expandable detail.

Still writing the table renderer: it builds each row with its date, body, symbol link and paragraph number.

Still writing the table rows: each record's date, body, symbol link, paragraph number and first line of text go in, with the state cell alongside, and a click on the row opens its expandable detail.

Still writing the table rows: the Date header button shows the sort direction and updates on each render, and the row count caption reports how many matching records are shown, or says none match. A "Show 50 more" button sits under the table, followed by the source line.

Still writing the sort comparator for the table: it orders the rows by date in whichever direction is currently selected.

Still writing the table sort: date order follows the chosen direction, so the newest records come first by default and flip when the header is clicked.

Still writing the sort comparator and the keyboard handling for the tabs.

Still writing the tab keyboard handling: the arrow, Home and End keys move focus between the three tabs and show the matching panel. On the third tab I'm hiding the rail's group headings while keeping its number, bar and chips.

I'm finishing the filter rail for the third tab, which drops its group headings but keeps the number, the bar and the chips, and I'll keep the "Clear all" button visible while a filter is active. The "Every check" panel gets a toggle button and a hidden panel, and I'm computing the number of checks on every render so the label stays accurate. Each check gets its own row with a name, the compared values and a pass status.

Still writing the every-check helper: it builds the list of checks, each with its name, compared values and a pass, warn or fail status.

Still writing the every-check helper: it counts the records, checks that the declared count matches, and confirms that partitioning by mechanism, body and year still adds up to the full set.

Still writing the chart-versus-table check: each top theme's count is compared against the filtered records that carry that theme, and the largest bar has to fit within the filtered total.

Still writing the link check: each record's document URL has to start with the UN docs address and end with its symbol, and the symbol cannot be empty.

Still writing the link check and the paragraph-number check: each record's URL has to start with the UN docs address and end with its symbol, and I'm counting how many records have a paragraph number for each mechanism.

Still writing the link and paragraph checks, and now the states check: each UPR record's parenthesised states should be found, and any that aren't get listed with a short excerpt.

Still writing the every-check helper: the not-labelled records get counted for each field, shown as info rows, and any text that appears more than once gets flagged.

Still writing the "Every check" helper: each check is assembled with a name, its compared values and a status, and I'm noting that the label count comes from however many checks the helper returns.

Still writing the layout CSS: I'm setting the paper, ink, rule, red and muted colour variables, and choosing a serif for the title, a monospace face for labels and a system sans for body text.

Still writing the layout CSS: setting the paper, ink, rule, red and muted colour variables, with a serif title, a monospace face for labels and a system sans for body text.

Still writing the layout CSS: the paper, ink, rule, red and muted colour variables are set, along with a serif title, a monospace face for labels and a system sans for body text.

Still writing the filter rail markup: the Keyword, Mechanism and Years groups each get a button and a hidden panel, with the keyword field and its hint first.

Still writing the tab markup: the three tab buttons are set up with their ARIA roles and selection states, and the first panel is opening.

Still writing the tab markup and the overview panel's headline tiles, with the big record count and its breakdown.

Still writing the overview panel: the big record count sits in its own tile with the breakdown beneath, and the document and year tiles follow it.

Still writing the Records tab: the paragraph and document checks follow the same layout as the overview, with the table rows, sort header and "Show 50 more" button.

I'm laying out the Records tab now: a search field with a hint, then a table with a sortable date header, body, symbol, paragraph, first line and recommending state columns, followed by a "Show 50 more" control.

I'm laying out the page structure now: a masthead, a filter rail on the left, and three tabs for overview, records and method, with the records tab holding a search field and a sortable date column.

Still writing the page's CSS and markup: the tabs, filter rail and table layout are being set up.

Still writing the JavaScript: the data setup, the country-derived constants and the helpers for formatting numbers and extracting paragraph numbers and states.

Still writing the JavaScript data setup: deriving the year range, the mechanism order and the body and type groupings from the records.

Still writing the filter logic: the state for mechanism, body, type, year range and SDG is checked against each record, and the state counts across all records are tallied, with the UPR records deduplicated.

Still writing the filter matching: each record is checked against the mechanism, body, type, state, year range, SDG and theme filters, plus every keyword word against its text and symbol.

Still writing the year filter: when the from or to year changes, the other end defaults to the file's min or max, and if both end up at the extremes the filter is cleared.

Still writing the JavaScript: the rendering of the rail, with the match count and the share bar that tracks how many records are left after filtering.

Still writing the rail's chip row and clear-all control: each active filter becomes a removable chip, and the clear button only appears when there is at least one.

Still writing the chip row: each active filter becomes a removable button, and I'm working through the mechanism, body, type, state and year cases.

Still writing the chip row and the clear-all logic: each active filter gets a removable chip for keyword, mechanism, body, type, state, years, SDG and theme, and the clear control only appears when a chip exists.

Still writing the state filter: the keyword input is wired up next, with the raw text kept as typed and the lowercased words used for matching.

Still writing the keyword handler: the typed value is copied into the other search box, and a shared 300ms timer then saves the trimmed text and re-renders.

Still writing the state, year and SDG filter logic inside the matching function, and I'm setting up the select options that get rebuilt from the filter data.

Still writing the filter handlers: the mechanism select clears the body choice when it no longer applies, and the year-from control swaps its ends if they come out reversed.

Still wiring the year selects: the from and to values get read together, and a reversed range is swapped before it's stored, with the sync step updating both controls.

Still writing the overview tiles: the record count, the document count and the year figures are being filled from the filtered records.

Still writing the overview tiles: the mechanism tiles are being rebuilt on each render, with the filtered records, their documents, latest year and share for each mechanism.

Still writing the mechanism tiles: each one shows its record count, document count, latest year and share of the filtered set, with a short note on how those figures are computed.

Still writing the Records tab's mechanism breakdown: the top ten states for the filtered Universal Periodic Review recommendations are being tallied and sorted, with ties broken alphabetically.

Still writing the Records tab's mechanism breakdown, with the chart code for the ten most frequent themes next.

Still writing the chart code: the ten-theme bar chart is created once with empty data, then its labels and counts get refreshed on each render.

Still writing the Chart.js setup for the themes bar chart: horizontal bars with a fixed colour and thickness, with animation turned off and some right padding for the value labels.

Still writing the Chart.js options: the tooltip shows the record count, the axes are set up without gridlines, and clicking a bar sets the theme filter and re-renders.

Still writing the Chart.js plugin that draws each theme's count at the end of its bar.

Still writing the Chart.js plugin that draws each theme's count at the end of its bar.

Still writing the timeline: the years are listed from the earliest to the latest in the data, and the counts per mechanism per year are tallied for a stacked bar chart.

Still writing the chart code: the timeline's stacked bars get their axes and legend set up, and the checks panel is next, with its count and rows rebuilt on each render.

Still writing the check rendering: each check gets a status label, its name and values, and a list of items when there are any.

Still writing the records render: the filtered rows are sorted and the first batch is drawn into the table, with the caption showing how many are displayed out of the total.

Still writing the records caption and the load-more button: the caption counts the matching rows against the total, the button shows how many remain, and the date header flips its arrow with the sort direction.

Still writing the Records tab: the rows are sorted and the detail view is being built for each row, with the state column showing the states found for Universal Periodic Review records.

Still writing the record rows: clicking a row toggles its detail view, and I'm making sure keyboard focus lands back on that row's button after the table rebuilds.

Still writing the record rows and their focus handling: after each rebuild, keyboard focus goes back to the row that was toggled, and the Records tab now hides the filter rail while the other tabs keep it.

Still writing the click handler for the group buttons: each one toggles its group open or closed, and the panels are kept in sync with their expanded state.

Still writing the summary text: it leads with the country's matching record count out of the total and lists the active filters, then the document count and the date range.

Still writing the summary text: the matching count is shown against the total, followed by the document count, date range, the breakdowns by type and mechanism, and the top themes with a note that records can carry several themes.

Still writing the header and summary: the kicker and title are set from the country, and the meta line links the source with the record and document counts, the year range and the build date.

Still writing the CSV export: the header row and the metadata lines for the country, source, build date and active filters are being set up.

Still writing the CSV export: the header and metadata lines are set, and each sorted row is being written out with its state, first line, themes, SDGs and related fields.

Still writing the CSV export: the header and metadata lines are set, and each sorted row is being written out with its state, first line, themes, SDGs and related fields.

Still writing the CSV export: the copy helper is set up to use the clipboard API first, with a fallback if that fails.

Still writing the copy-to-clipboard helper: it falls back to a hidden textarea and execCommand when the clipboard API isn't available, and a flash function briefly swaps a button's label.

Still writing the clearAll handler: it resets every filter field and then syncs the inputs and re-renders.

Now I'm wiring up the filter selects, working out which bodies and mechanisms are available for the current selection and sorting them by record count.

Still writing the select filters: the body and mechanism options are rebuilt from the current selection with their counts, and the type select is set to match the filter state.

Still writing the select filters: the body options get rebuilt from the chosen mechanism with counts, while the year and SDG selects are fixed lists.

Still writing the filter markup: the keyword, mechanism, body and type controls are set up, the state select is hidden when no states are present, and the year and SDG options are being built.

Still writing the CSS: the page colours and base font are set, and the stylesheet is being filled in next.

Still writing the CSS: the stylesheet covers the masthead, typography and focus outlines, and the masthead title is being sized.

Still writing the stylesheet: the masthead, shell grid, rail and main areas are sized, with the tabs and a narrow-screen breakpoint being added.

Still writing the CSS: the tabs, the rail's big numbers and share bars, and the filter chips are being styled now.

Still writing the CSS: the input and select styles are set, and the tile grid is being laid out with its borders.

Still writing the CSS: the tiles, the figure captions and the chart container are being styled now.

Still writing the CSS: the table and caption styles are set, and the highlight and row hover colours are being added now.

Still writing the CSS: the lab rows, check items and status columns are being styled now.

Still writing the CSS: the stylesheet is adding the check rows, their header layout and the status colours for pass, warn, fail and info.

Still writing the CSS: the footer, buttons, screen-reader-only class and hint text styles are being added now.

Now I'm writing the stylesheet's note, source and question-heading rules, sizing the headings and the monospace labels.

Still writing the JavaScript: the helper functions for DOM access, number formatting and percentages are being set up, and the data object is read in.

Still writing the JavaScript: the helper functions for element creation, number formatting and mechanism colours and ordering are being defined.

Still writing the el helper: it sets attributes and event listeners from the props and appends the child nodes.

Still writing the JavaScript: the element helper and the paragraph-number and state-extraction regexes are being set up.

Still writing the state extraction: the regex captures the trailing run of parenthesised names, and each name is kept if it has no commas, is under 60 characters and isn't already in the list.

Still writing the state extraction: the regex matches the trailing run of parenthesised names, checking that the leftmost match only captures contiguous groups at the end.

Still writing the JavaScript: the record preparation reads each entry's text and index so the states can be pulled from the trailing parentheses.

Still writing the JavaScript: the record preparation is adding the parsed paragraph number, the lowercased search fields and the sorted theme, SDG and target lists.

Still writing the JavaScript: the trailing-date and year range helpers are being set up from the sorted year list.

Still writing the JavaScript: the state counts are being tallied across the records, so each state's count can be shown with its name.

Still writing the JavaScript: the country-and-counts helpers are being set up, with the record list, year range and mechanism list computed from the data.

Still writing the JavaScript: the trailing-date and year range helpers are being set up, and the filter-and-sort setup is wrapping up before the init function begins.

Still writing the JavaScript: the trailing-date and filter helpers are set up, and the page init is being wired up with the title, source line and record counts.

Still writing the JavaScript: the per-mechanism counts are being prepared, and the select filters are being filled in with the mechanism, type, state, year and SDG options.

Still writing the JavaScript: the select filters are wired up, with change handlers for mechanism, body, type, state and the year range.

Still writing the JavaScript: the year-range and SDG filter handlers are being wired up, and the bodies list is set from the chosen mechanism.

Still writing the JavaScript: the Chart.js setup is being guarded so the charts only render when the library is present, and the body list is rebuilt from the selected mechanism.

Still writing the JavaScript: the Chart.js setup is being guarded, and the HTML body is starting with the masthead and filter rail.

Still writing the JavaScript: the next block is the rail HTML, with the keyword filter group and its search input being laid out.

Still writing the HTML body: the masthead and filter rail are in place, and the first filter group, the keyword search, is done. Now I'm laying out the mechanism, body and type selects, plus the Recommending State filter.

Still writing the HTML body: the filter rail's year and SDG group is being laid out, with the from and to year selects and the goal select.

Still writing the JavaScript: the select filters are being filled and wired up, with change handlers that rebuild the body list and update the year range and SDG filter.

Still writing the HTML: the three summary tiles are being laid out, each with its headline number, a short caption and a note on how the figure is computed.

Still writing the HTML: the masthead and filter rail are in place, and now the main column's tabs and the first panel's summary tiles are being laid out.

Still writing the HTML: the theme chart note and the table of the ten most frequent themes are being laid out, with the record and percentage columns and the source line below.

Still writing the HTML: the source line and the records-per-year figure are being laid out, with the stacked bar chart and its empty-state message.

Still writing the HTML: the year chart's note and source line are laid out, and the checks toggle button is being added below.

I'm getting the panel-1 markup laid out, with the paragraph-level records and the UN document each one comes from.

Still writing the records table markup: the search box, the date header button, and the column headers for body, symbol, paragraph and first line.

Still writing the records table markup: the Recommending State column header is in place, and the table body, the "more" button and the source line are being laid out.

Still writing the HTML: the panel-2 method notes and the export buttons are being laid out, with the CSV download and copy-summary actions and a status line for their messages.

Still writing the HTML: the method notes are going in as plain sentences on how the counts, filters and themes are computed in the browser.

Now I'm setting up the methods notes, explaining that every figure is computed in the browser from the file's records, and that the theme counts and recommending-State counts are described plainly for the reader.

Still writing the JavaScript: the global state, filter object and the sort and paging variables are being declared.

Still writing the JavaScript: the mechanism-based body list is being built, and the main render function is being set up to filter the records, reset paging when the filters change, and redraw the rail, overview, records and checks.

Still writing the JavaScript: the rail's match count, subtitle and share bar are being updated, and the active filter chips are being rebuilt.

Still writing the JavaScript: the rail's chips and the clear-all button are being wired up, with each chip removing its filter and re-rendering the page.

Still writing the JavaScript: the select filters are being synced to the current state, with the mechanism select set and the body list rebuilt for that mechanism.

Still writing the JavaScript: the select filters are being synced, with the body list rebuilt for the chosen mechanism and reset if the current body no longer belongs to it.

Still writing the JavaScript: the body select is rebuilt from the chosen mechanism, and the type, state and year-range selects are being synced to the current filters.

Still writing the JavaScript: the overview's headline counts are being set, with the total matching records, the file total and a per-type breakdown.

Now I'm building the per-mechanism tiles in the overview, filtering the matching records for each mechanism and rendering their counts.

Still writing the JavaScript: the mechanism tiles are being built, with each mechanism's record count, document count and latest year shown.

Still writing the mechanism tiles: each one gets its record count, document count and latest year, and the UPR tile also gets the states block and a short note on how the share is computed.

Still writing the JavaScript: the mechanism tiles' helper is being finished, with a states block for the UPR tile that lists the top recommending States in a collapsible section.

Still writing the JavaScript: the Ten States list is being built inside the UPR tile's collapsible block, with each State shown alongside its recommendation count.

Still writing the JavaScript: the mechanism tiles' statesBlock helper is being written, with a toggle that shows or hides the list of the ten States making the most UPR recommendations.

Still writing the JavaScript: the theme tally is starting, with a map that counts each theme once per record.

Still writing the JavaScript: the theme tally is finishing up, with the top ten themes sorted by count and the chart's title, empty-state message and visibility being set.

Still writing the JavaScript: the theme chart is being fed the top ten labels and counts, with the table rows and the empty-state message set for the filtered records.

Still writing the JavaScript: the theme chart is being set up as a bar chart with an empty dataset, styled in the deep red colour.

Still writing the chart's onClick handler, so clicking a theme bar will set that theme as a filter.

Still writing the JavaScript: the Chart.js bar setup is being finished, with its click handler set to filter by a theme and its hover cursor changing over bars.

Still writing the JavaScript: the chart's value labels are being drawn at the end of each bar with a small plugin.

Still writing the JavaScript: the year chart is being set up, with the per-year counts grouped by mechanism.

Still writing the JavaScript: the year chart is being built with its own Chart.js instance, and its labels and per-mechanism datasets are being filled from the counts.

Still writing the year chart's options, with a stacked bar layout, a top legend, and light gridlines on the y-axis.

Still writing the JavaScript: the records table's sort function is being defined, comparing dates so that the direction follows the current sort setting.

Checking the sort direction: the comparator for ascending order is a < b gives -1, otherwise 1, and descending order just flips that sign. Since sortDir is -1 for descending, multiplying by sortDir gives the right result in both directions.

Checking the sort comparator once more: when the dates differ, multiplying by the sort direction flips the order for descending sorts. Still writing the sort's tie-breakers.

Still writing the JavaScript: the records table is being rendered from the filtered and sorted rows.

Still writing the JavaScript: the records table rows are being built from the sorted slice, each with its date, body and a link, and the first line of the record text is set as a toggle button.

Still writing the records table: each row gets its date, body, symbol link, paragraph number and first line as a toggle, and the detail row is added when expanded.

Still writing the JavaScript: the table's detail-toggle function is being defined to add or remove a record's index from the set of expanded rows.

Still writing the records table: the date-sort toggle is being wired so the header reverses order, and the row count caption and "show more" button are being updated.

Still writing the JavaScript: the records sort is being finished, and the table's row count caption, date header label and "show more" button are being updated to match the current sort direction and visible rows.

Still writing the JavaScript: the detail panel's helper is being defined, with a copy-citation button whose label flashes after copying.

Still writing the JavaScript: the copy button is being defined so it reads its own element before the async copy and flashes its label afterwards.

Still writing the detail panel: the paragraph number, full text, and labels for themes, SDGs, targets and persons are being laid out, with a citation line to follow.

Still writing the detail panel's links and labels: the Open-document link and a monospace citation line, then the Themes, SDGs, SDG targets and Affected persons rows, each falling back to "not labelled" when empty.

Still writing the runChecks function: it starts an output list and reads the declared record count from the data.

Still writing the runChecks function: the record count is being compared with the declared count, and the per-mechanism, body, year and type breakdowns are being summed to confirm they add up to the total.

Still writing the checks: the chart's top-ten bars are being recounted against the filtered records, and the largest bar is being compared with the total.

Still writing the checks: the links are being tested against the UN document prefix, with the count of valid links shown against the total.

Still writing the checks: the paragraph-number coverage is being computed per mechanism, with the UPR result flagged if its coverage falls short.

Still writing the checks: the paragraph numbers are being tallied per mechanism, with UPR marked as a warning if any of its records lack one, and the other mechanisms reported for information only.

Still writing the checks: the paragraph numbers are being tallied, and the UPR records are being checked for recommending States, with a warning if any of them name none.

Still writing the checks: the distinct id values are being counted against the record total, and a Map is being built to tally something else next.

