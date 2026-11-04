I'm laying out a single complete HTML file of roughly 1500 lines, so I'll plan it carefully but efficiently. The main constraint is keeping each view to about seven clickable elements, and the tabs, filter headings, and clear-all button already come close to that limit on the first tab.

Now I'm working out how to pull the parenthetical state labels out of each record's text with a trailing-match regex, and I want to confirm it won't blow up on long inputs.

I'm working through how to split out the state names: each parenthetical group at the end of a record gets checked, and it only counts as a state if it has no comma and stays under 60 characters, otherwise the record is marked as not found. I'm also sketching the paragraph-number pattern, which should catch things like "144.43" and "71" at the start of a line.

I'm sorting out the paragraph numbers by comparing the major and minor parts as integers, since a plain numeric parse would put 144.5 before 144.43. Records without a paragraph number will go to the end. Date sorting is next, with the header click deciding whether it runs ascending or descending.

I'm settling the filter state as a set of fields: keyword, mechanism, body, type, state, year range, SDG, and theme chips that combine with AND. For the counts beside each option, I'm weighing whether to tally them across the whole file or only within the chosen mechanism, leaning toward keeping them stable against the full dataset.

Next I'm wiring up the search box on tab 02 so it stays in sync with the keyword filter, with both inputs writing to the same state value. I'm also making sure only one filter section can be open at a time, toggling each button's expanded state and hiding the other panels, with a hidden attribute rule in the CSS. Then I'll check the clickable element count on the first tab, which currently sits around nine once the tabs, headings, clear-all, and the States link are counted.

Now I'm setting the Overview tab's first tile to count the filtered records, with a per-type breakdown underneath and the Type filter starting on "all".

I'm checking the Overview tiles: the first one counts the filtered records with a per-type breakdown, and each mechanism gets its own tile showing counts, documents, latest year, and share. The UPR tile will open an in-place list of the top States for the current filter. Next I'm setting up the theme bar chart, where clicking a bar adds a theme filter, and a stacked year chart per mechanism. I also need to make sure the chart canvases get destroyed and recreated cleanly, with animations switched off.

Now I'm laying out the chart labels: long theme names need wrapping onto lines of about 34 characters so the bar chart stays readable, with the value drawn at the end of each bar through a small inline plugin. I also need to make the chart container a fixed 380px tall with aspect ratio turned off, and render the charts only once the first tab is visible, since a canvas inside a hidden tab measures zero.

Now I'm setting up the table on tab 02 with a caption and its columns, and each row needs to be expandable. I'm weighing whether to make the row itself focusable with aria-expanded or to put a button in the first cell. I'll put a button with aria-expanded in the first cell, and have clicking the row toggle it too, so Enter works from the keyboard.

I'm wiring the table rows so a button in the first cell toggles the detail, with the row click handled once through delegation so Enter works from the keyboard. The expanded state lives by record index, so it survives re-rendering when more rows are shown, and I'm planning the detail row's layout with the large paragraph number and full text.

I'm defining how the table's detail row will show the full text with the keyword highlighted by splitting the raw text on an escaped regex, and I'm setting the column layout to Date, Body, Symbol, Para., First line, and Recommending State.

I'm settling the Tab 03 checks: each one will be a line with a pass or fail marker, a label, and its values, and the failures can sit inside a native details element so the long lists of records without a State stay out of the way.

I'm going to make the record-count check compare the number of loaded records against the declared count. Next, I'll confirm that the mechanism, body, and year partitions each add up to the total on the full file. For the type check, I'm summing the per-type counts against the headline tile total on the filtered set, using the same function the tiles use. Then I'll recompute the top themes with a separate loop to cross-check the chart and table.

I'm checking the table data for tab 03: the rendered rows only exist on tab 01, so the DOM can go stale after filter changes. I'm thinking of caching the chart and table values in a `lastFig` object whenever tab 01 renders, and comparing those against a fresh recount of the filtered records.

I'm working out how the Tab 03 checks will compare the figures against the chart data. The bar values can come from the chart instance when it exists and matches the current filter, and I'm weighing that against a second computation and the table rows.

I'm settling how the Tab 03 checks will get their figures: a cached result from the last overview render, rebuilt if the filter has changed, and then compared against a second, independent count. I'm also confirming that no bar exceeds the filtered total and that each document link points to the UN docs domain.

I'm checking the paragraph numbers per mechanism, expecting every UPR record to carry one, and I'll flag it as a warning if not. Then I'm verifying that UPR records each have at least one recommending State, listing any that don't along with their symbol and the tail of their text inside a details element.

I'm working through the rest of the Tab 03 checks: duplicate texts, missing themes, SDGs and affected persons, then a random sample of ten records with a draw-again button tied to a seed.

I'm settling the sample check: ten random records drawn from a seed. The first draw will pick a random seed and show it in the box, and after that I'll offer a "Draw again" option alongside a "Draw with this seed" button, which keeps the number of clicks down.

I'm laying out the sample draw: a shuffle seeded by mulberry32 over the filtered records, taking the first ten. Each card will be a single collapsed line showing the symbol, paragraph, first line, and verdict, with only one open at a time.

I'm working out the sample tally line: the number of themes that fit, don't fit, or are unsure, shown against the ten records drawn.

I'm settling the sample tally so the result shows how many drawn themes fit, don't fit, or are unsure, along with how many were judged out of the drawn total and which seed produced them. I also want the sample to reset whenever the filter changes, so a stale draw never sits beside new filter results. On the last tab I'm laying out the method notes, the buttons for downloading the CSV and copying a summary, and a data source line.

I'm writing the CSV export: a commented header with the filters and row count, then the columns, with list fields joined by pipes and quotes escaped. The download goes through a temporary link, and the blob URL gets revoked afterwards. Next is a copy-summary button that tries the clipboard API and falls back to a hidden textarea.

I'm laying out the page header: a "UHRI · Kenya" label, a title naming the UN recommendations and observations for Kenya, and a line with the source link, record and document counts, the years covered, and the build date. Then a footer repeating the record count and source link, and I'm colour-coding the mechanisms: UPR in orange, treaty bodies in teal, special procedures in purple, with grey for anything unrecognised.

I'm laying out the filter panel: a keyword box, then selects for mechanism, body, type, and state, each showing its count per value. Rebuilding every select on each change would drop focus from the one the user just touched, so I'll only refresh the dependent ones and keep the element they're working in.

I'm setting the body select to rebuild only when the mechanism changes, and resetting it if the chosen body no longer exists under the new mechanism. The state select only appears when states were extracted, sorted by count and then alphabetically, and filtering on a state means the record's state list has to contain it. I'm about to lay out the year-range and SDG selects next.

I'm setting the year selects to span every distinct year in the file, defaulting to the earliest and latest, and only treating the filter as active when they differ. If the "from" year ends up above "to," I'll swap them. The SDG select lists the goals present in the data, labelled with their names, and records missing a year are only dropped when a year filter is in effect.

I'm laying out the page's layout: a fixed rail beside the main column that stacks on narrow screens, with the tabs set up for keyboard arrow and home/end navigation. I'm also deciding how the first line of each record is shortened when the text runs past 120 characters.

I'm deciding how the first line of each record gets shortened, and I'm keeping the paragraph number inside the text. Numbers will be formatted with thousands separators, and I'm working out how the timeline will stack its bars by mechanism, with years along the x-axis.

I'm setting up the Chart.js timeline with a value-label plugin, so I'm writing the bar colours and the plugin that will draw each bar's count at its end.

I'm adding the value labels by drawing each bar's count at its end, then wiring clicks on the bars to add that theme to the filters.

I'm making each theme in the table a button that adds it to the filters, and adding a small hint under the table about spotting legacy labels through wide or old year ranges, with the sample check in 03 as the way to judge them.

I'm setting the Overview tab's UPR tile to carry a "see the States" toggle that reveals a top-ten list of States making recommendations to Kenya, in place beneath the tiles, and showing a plain message when no UPR records match the filter. Each mechanism tile will show a coloured dot and name, the record count as the big figure, the document count with the latest year, and its share of the total.

I'm settling the summary bits for the overview: the record breakdown by type, with a fallback label for records that have no type, and a one-line note explaining how each tile is computed.

I'm checking the partition counts per mechanism against the total, keeping missing values as their own bucket so a gap would show up rather than vanish.

I'm writing the check function next, one that returns a list of labelled results with a pass, fail, or warn status. For the partition checks, I'll count only records that have a value and flag any gap as an explicit count of records without one, so a missing value shows up instead of disappearing.

Still writing styles...

Still writing styles...

I'm laying out the rail beside the main column, with a header row holding the "Filters" label and a clear-all button, then the big record count, its share bar, and the active filter chips. Below that go three collapsible filter sections, each toggled by a header button that controls its body.

I'm writing the record-rendering helpers next: the precomputed fields for each record, including the state list and the keyword search string, plus the first line shortened for display.

I'm working out how to pull the state names out of each UPR record's text: I'll match the trailing parenthesised list and split it into individual country names, dropping any entry that contains a comma or is overly long.

I'm sorting the records by paragraph number, comparing the numeric parts so that 10 comes after 9, and I'm working out the mechanism order with the three main bodies first and the rest alphabetical after them.

I'm writing the comparison for sorting the records by paragraph number, splitting each number into its parts so that 144.10 sorts after 144.9, and putting missing numbers last. Then I'm sorting by date in the chosen direction, then by body, then by paragraph.

I'm writing the table's caption to show how many matching records there are, sorted newest first, with the Date header able to reverse the order. The Date header carries an aria-sort value of descending, and I'm adding a source line under the table noting where the rows come from.

I'm adding the copy-citation button for each row, with a label that changes when there's no paragraph number, and a short "Copied" confirmation that reverts after a couple of seconds. The copy will try the clipboard API first and fall back to a hidden textarea if that's blocked.

Still writing the copy helper: it tries the clipboard API first and falls back to a hidden textarea, then sets a status message showing whether the copy worked.

I'm adding the event handling next: a single click listener on the body that reads data-act attributes to handle chip removal, section toggles, adding a theme from the table, the states toggle, and row expansion.

I'm wiring the remaining interactions: sorting by date, copying citations with a brief confirmation, the sample draw controls, and the verdict and card toggles. After each verdict click the panel re-renders, so I'm restoring focus to the same button by id and keeping the seed input's value in state.

I'm setting up the sample section as its own container, separate from the checks, so that verdict clicks only redraw the sample and not the whole panel. Then I'm writing the check runner, starting with a record-count check that compares the number of loaded records against the reported total.

I'm writing the check-runner's last items: a note on how many distinct IDs match the record count, a scan for duplicate texts, and a list of which records lack themes, SDGs, or affected persons, shown as informational notes rather than failures. I'm also checking how many UPR paragraphs carry a paragraph number, warning only if some are missing.

I'm getting the mulberry32 seeded random generator set up next, so the sample draws are reproducible from a seed value.

Still writing the sampling logic: I'm seeding the random generator, shuffling a copy of the filtered pool, and taking the first ten records as the sample, then rendering each sampled card with its verdict buttons.

I'm giving each sampled card a body with the full text, its UN theme labels, and Fits, Doesn't fit, and Unsure buttons. Next I'm adding a CSV download and a summary copy for the filtered records, sorted the same way as the table.

I'm setting up the overview charts next: a horizontal bar chart with wrapped two-line labels, and a stacked timeline, both destroyed and redrawn on each render. If no records match the filters, I'll show a "No records match" message in place of the charts.

I'm laying out the overview panel's skeleton: a headline row of tiles, a mechanism tile row with colored dots, a states box, and two figures, each with a chart, a fallback message, and a table. Each note under those blocks stays to two sentences, and the header will show the year range and the list of distinct years.

I'm defining the filter function now: it checks each record against the selected mechanism, body, state, and year range, then stores the filtered set and resets the sample.

I'm defining the filter logic: a record passes only if it matches the selected filters, and when the year range has been narrowed, records with no year are dropped while full-range records keep everything. The active filters then show up as chips, covering the keyword, mechanism, body, type, state, year range, SDG, and themes, with a clear-all button that resets them.

I'm continuing the sample-draw and filter wiring, then planning the rail and section visibility so the headings hide once the user moves past the overview tabs.

I'm defining the helper functions next: an escape function for HTML, a highlight function that wraps the keyword matches in marks, and a tile builder for the headline numbers.

I'm working out the overview numbers next: a count and type breakdown for the filtered records, plus a year range, with the years tile falling back to a dash when there are none.

Then I'm grouping the records by mechanism in a single pass, giving each one its count, distinct documents, latest year, and share of the total.

Next I'm wiring up the row expansion and the rest of the table, with each row's detail shown in a collapsible section.

I'm building the table rows now: each one shows the date, body, a link to the symbol, the paragraph number, a button with the first text, and the state cell, with the row itself toggling its detail on click.

I'm building the table rows now, with each one showing its date, body, symbol link, paragraph number, first-line button, and state cell. The row toggles its detail on click, while links inside it keep their own behavior.

Now I'm writing the CSV export, with a helper that quotes cells containing commas, quotes, or line breaks.

I'm writing the CSV export helper now, so that cells containing commas, quotes, or line breaks get quoted properly. Then I'm building the summary text for the filtered records.

I'm writing the summary text now, with the year range, the filters, the breakdown by type and mechanism, and the ten most frequent themes, and I'll show it in a read-only box so the user can see what gets copied. After that I'm finishing the method notes: every figure comes from a loop over the records in the browser, and the keyword filter matches each word as a plain substring.

Now I'm writing the source and licence lines, and the build date, after the method notes.

Next I'm wiring up the tab switching and the main render function, so the active panel refreshes whenever the user changes tabs.

I'm wiring up the search box in the records tab so typing there updates the same filter as the rail, syncing the other input without moving the cursor, and I'm starting on the rail's record count.

I'm wiring the chart click handlers so clicking a theme bar adds that theme to the filters, and setting the hover cursor to a pointer over clickable bars. Then I'm adding the mechanism select handler, which clears the body filter when the chosen body doesn't belong to the new mechanism.

I'm making the body and type dropdowns depend on the selected mechanism, with missing values labeled as "(no body)" or "(no type)" so they can still be filtered.

I'm checking the chart's theme totals against the table rows, comparing each count with a fresh tally over the filtered records to confirm they match.

I'm checking the chart's theme totals against the table rows, pulling the bar values and the table's data attributes so I can compare them directly when the figure has already been drawn for the current filter.

I'm checking the chart's theme totals against the table by reading the bar values and the table's data attributes, if the figure was already drawn for this filter. If it wasn't, I'll recompute the counts from the filtered records and compare those instead.

Now I'm checking the code that compares the chart's theme totals against the table, reading the drawn values if the figure is current, and otherwise recomputing them from the filtered records.

I'm writing the keyword debounce so both search boxes stay in sync, with the other box updated only when its value differs, and then applying the filter.

I'm setting up the sample section next: a seed box that updates the seed as the user types, and a draw that picks ten random records, with a message when no records match the filters.

I'm finishing the code now, so I'm checking for correctness and making sure the chart's largest bar never exceeds the filtered count. I'm also adding keyboard handling for the tab buttons.

