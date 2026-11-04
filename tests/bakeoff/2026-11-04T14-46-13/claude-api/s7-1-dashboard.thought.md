I'm starting on a big build: one complete HTML file, around 1500 lines, written carefully. I'll plan it compactly but thoroughly. The tricky constraint is keeping clickable elements to about seven per view, since tabs, filter headings, and a clear-all control push the count to eight.

I'm now setting up the data layer: pulling the records from the workshop data and precomputing a paragraph number, sort key, extracted states, a first line, and search text for each one. For the UPR records, I'll pull out parenthesized state names from the end of the text, keeping only those short enough and free of commas, and mark a record as having no state if none qualify.

I'm laying out the global state the filters will track: the search query, mechanism, body, type, state, year range, SDG, and selected themes, with the filter chips and rail controls for each. The tab 01 rail is now the point of concern, with four tabs, Clear all, and three accordion headings already at eight clickable items against the seven-per-view target, so I'm weighing whether Clear all should only appear when a filter is active.

I'm settling the filter controls for section 02: Mechanism, Body, Type, and State as selects rather than a row of buttons, so only one heading's worth of controls is in play at a time. Body options will list the values present within the chosen mechanism, each with a count across the whole file.

I'm setting the filter selects for Mechanism, Body, Type, and State, with Body and State counted across the whole file. When the mechanism changes, I'll drop any body that no longer applies. The year range and SDG controls come next, and the keyword box appears in both the rail and the top of tab 02, kept in sync with a 300ms debounce.

I'm working out the overview tiles: the first one counts the filtered records, with a per-type breakdown underneath. After that come documents, the year span, and one tile per mechanism showing its share of the filtered set.

I'm moving on to the overview tiles: a "see the States" link on the UPR tile opens a list of the top ten states for the current filter. Mechanism tiles come next, showing the mechanisms present in the file with counts from the filtered set and a colour dot for each. I'm also planning the top-ten themes chart, a horizontal bar chart with counts at the bar ends, clicking a bar adding a theme filter, plus an aria-label and a table beneath it.

I'm making the chart wait until tab 01 is actually visible, since Chart.js sizes itself wrong inside a hidden container. Labels will wrap onto multiple lines, the value text needs room on the right, and the chart gets destroyed and rebuilt on each change, with a plain message in its place when nothing matches.

I'm settling the second chart as a stacked bar of records per year, one colour per mechanism, spanning every year in the filtered set, with grey as the fallback colour. Its legend sits on top and the tooltips stay at their defaults. Next I'm turning to the Records tab, with a search field, a caption, and a table whose columns run from date and body through symbol and paragraph to the first line, and I'm still weighing where the recommending state column belongs.

I'm settling the Records table's column order: date, body, symbol, paragraph, first line, and then the recommending state, which stays narrow. Clicking the Date header will flip only the date direction, while body and paragraph keep their ascending order, with rows missing a paragraph number handled separately.

I'm settling how each table row expands: the date cell will hold a toggle button with aria-expanded, and clicking anywhere on the row will do the same, with clicks on links ignored. An expanded row adds a full-width detail line beneath it, and the set of open rows is kept across "Show 50 more" updates.

Still writing the highlight helper, which escapes the text and wraps each keyword match in a mark tag.

I'm now tuning the highlight helper so it matches keywords on the raw text and escapes each piece separately, which keeps HTML entities from being hit. Expanded rows will get the same highlighting, including on the symbol link. I'm also laying out the expanded view: a large paragraph number, the full text, its labels, and a copy-citation button.

I'm wrapping up the expanded view: an "Open the UN document" link, and a copy-citation button that tries the clipboard API and falls back to a hidden textarea, then briefly shows "Copied". The button notes when a record has no paragraph number. Next I'm moving to a "Check this dashboard" panel on tab 03, where the data checks run against the whole file, and the chart-versus-table check uses the filtered set instead. I'm starting with the record count against the stated total, then the per-mechanism, per-body, and per-year sums, and finally the per-type partition against the total.

I'm checking the chart against the table by reading the numbers back from the rendered tab 01 rows and comparing them with the chart's data. The largest bar must not exceed the filtered count, and the comparison runs on the filtered set rather than the whole file.

I'm moving on to the lower checks now: one that verifies each document link points at the UN docs site and ends with its symbol, and the chart-versus-table check, which reads the stored top-themes numbers.

I'm now checking the tab 03 list: the last few checks cover paragraph-number coverage per mechanism and whether each UPR record has at least one state, with the records that don't listed so the reader can see what the parentheses held.

I'm finishing the tab 03 checks: duplicate text values and records with no labels get counted, and I'm laying out a pass or fail verdict for each one.

I'm picking the colour for the warning label next, checking that a dark amber on the cream background still reads clearly. For the random sample, I'll default the seed box to 1, with a "Draw again" button that picks a new random seed and a "Draw with this seed" button to reproduce a given draw.

I'm settling the random sample controls: before the first draw, only a "Check 10 at random" button appears, drawing with the seed in the box, which starts at 1. After that, "Draw again" picks a fresh random seed and fills the box, and "Draw with this seed" reruns the draw with whatever number is in the box.

Next I'm working out the random sample itself: a seeded generator picks ten records without replacement from the filtered set, in file order, and if fewer than ten match I draw all of them.

I'm laying out each card as a line with a toggle button, a separate symbol link beside it, and a verdict badge, so the link doesn't sit inside the button. The expanded body will hold the verbatim text, the theme chips, the three verdict buttons, and a short note for the section.

I'm settling the tally line for the random sample: it will count how many of the drawn records are judged to fit, don't fit, or are unsure, out of the ten judged.

I'm now setting up the tab 04 method notes and the export actions: a CSV download with a short comment header recording the country, source, build date, and filters applied, then the row count. The columns will cover the visible fields plus the full text, labels, and the document link.

I'm setting the export and summary actions for tab 04: a CSV download with a comment header for the country, source, build date, and filters, and a copy-summary button that also shows the text in a small preview box in case the clipboard fails.

I'm setting up the header and source line: the country and title, the source linked to its URL with the record and document counts, the year range, and the build date, with a fallback if the source link is missing. Then I'll add a footer with the record count and source link.

I'm setting up the year filters as two selects that default to the full range, swapping the values if the user picks a "from" year later than the "to" year. An active year range gets its own chip. For the SDG filter, I'm building a select with an "All goals" option and one entry per goal showing its count, and I need to handle the case where the goal names might be missing.

I'm setting up the rail as a 240px column beside the content, stacking it on narrow screens, and leaving it unsticky since open accordions could run taller than the viewport. The active-filter chips will each carry a removable × button. The rail only appears on tabs 01 and 02, and its accordions default to closed, with one open at a time.

I'm settling the visual details next: each mechanism gets its own colour, with a neutral grey for anything else. Under each figure I'll add a short mono note explaining how it was computed, plus a source line naming the filtered record count.

I'm making the theme names in the table into buttons, so keyboard users can filter by theme too, and adding a hint that says to click a bar to filter. Under the table I'll add a note to check a theme's labels on tab 03 before quoting it, and I'm leaving out any flag for themes that end early since I'd have to invent a cutoff for that. Clicking a bar will add a theme chip to the filter state.

I'm going to make the state names in the opened UPR list into buttons that set the state filter, even though it adds more clickable items, because it's a quick addition and useful. The list will show the top ten states for the current filter, and the state select in the tab 02 heading only appears when states were actually found.

I'm writing the export and summary functions for tab 04: the CSV download, the Excel BOM question, and the copy-summary fallback.

I'm writing the state-extraction helper now: it pulls the parenthesised country names off the end of each recommendation, dropping duplicates and anything with a comma or that's too long to be a state name.

I'm checking the regex used to pull state names from the end of each recommendation, looking at whether it could backtrack badly on long texts, and it looks linear since the alternatives don't overlap.

I'm working out how each record's state names get pulled from the trailing parenthesised groups, with nested parentheses like "Venezuela (Bolivarian Republic of)" kept whole. Next I'm setting up the record objects, reading each paragraph number and marking which records are UPR.

I'm finishing the record setup: each record keeps its states, year, themes, SDG tags and paragraph numbers, and I'm filtering out missing years so the year range only uses valid values.

I'm setting up the filter state and the function that computes which records match, starting with the word search that lowercases the query and splits it into terms.

I'm writing the record filter: it checks the mechanism, body, type, state, and year range, and treats records with no year as matching only when the full range is selected. Then I'm adding the SDG check and the word search, with the themes requiring every selected theme to match.

I'm writing the sort comparator for the record list: newest dates first by default, with the direction flipped by a stored sort setting, and ties falling back to body and paragraph order.

I'm working out how the sort key combines the paragraph's major and minor numbers, so records compare correctly, with missing paragraphs sorted to the end. Then I'll render the rail, overview, records, checks and method sections from the filtered set.

I'm making the overview rely on a single computed list of top themes, so the chart and table always agree, and the checks section will compare that list against a fresh calculation.

I'm working out how the overview draws on one shared list of top themes, so the chart and the table both read from it, and I'll compare the chart's values with that list when I run the checks.

I'm deciding that the overview always renders its non-chart parts so the checks can compare against the same data, and the chart gets drawn only when the overview tab is active. The timeline will use the years from the filtered set's minimum to maximum, with counts per mechanism in a fixed order, and I'll show a message if nothing matches. Next I'm setting up the Chart.js configuration for the figure.

Still writing the Chart.js config...

Still writing the chart's value labels...

Still writing the chart's value labels...

Still writing the chart's value labels...

I'm laying out the static HTML skeleton now: the filter rail with its chips and accordion sections, the tab bar, and the tab panels. The accordions will be generated by the page script.

I'm setting up the filter rail's inputs: the keyword field, then the mechanism, body, type and state selects, plus the year range and SDG select. The selects get filled in by the render function, since the body options depend on the chosen mechanism. I'll leave the keyword input alone during re-renders, and only rebuild a select when its options actually change.

I'm laying out the static HTML for the records tab, starting with its heading and the keyword search box, then the table. Since the filter selects don't change, I'm only rebuilding the body select on each rail render.

I'm laying out the records tab's markup now: a question heading, the keyword search, and a table with a caption, body, and a button to show more rows. The search placeholder will show the record count, and each row gets an id so clicking it can toggle the expanded view.

I'm laying out the records tab's markup: a question heading, the keyword search box, and a table with a caption, body, and a show-more button. Each row's detail view will be a full-width expansion with the paragraph number, text, labels, and actions.

I'm writing the detail row's markup: the paragraph number, the full text kept as-is, and labels for themes, SDGs, targets and affected persons, showing "not labelled" where a label is missing. Then the actions with a citation copy button that shows a brief "Copied" note.

I'm writing the checks section now: each check compares a computed value against an expected one and gets a pass, fail, warning, or note label, with any extra detail tucked into a collapsible block. The first check compares the record count against the stated total, and I'm working out what to show if that total is missing.

I'm writing the checks now, starting with a count check that compares the record total against the stated figure and warns if that field is missing. Then I'm adding a partition check so the mechanism, body and year totals each add back to the full set, plus a type breakdown on the filtered records.

I'm checking the state coverage for the UPR records next: every UPR record should have a state, and any that don't will be listed with a short excerpt of their text. Then I'll add a duplicate and gap check on the ids, plus notes on duplicate text and unlabelled records, before the random-sample label check goes in its own section below.

I'm planning to memoize the file-wide checks so they're computed once, while the filtered checks recompute on each render. The random-sample label check will go in its own section below the panel, and the method tab will cover the data source, a link to the source page, the build date, and a note that the licence isn't stated in the file, so the user should check the terms before republishing.

Now I'm writing the copy-summary text, with the source line, build date, and the active filters listed under it.

I'm finishing the overview tiles with each mechanism's record count, document count, latest year, and share of the filtered set, showing zeros and dashes when nothing matches. I'll order the mechanisms with UPR, treaty bodies and special procedures first, followed by the rest alphabetically, and add a "see the States" toggle inside the UPR tile.

I'm adding the state-level list directly under the overview tiles, with its counts for the current filter and a note that these count recommendations rather than influence. I'll also note how many UPR records in the filter have no State found, and fill the rail's State select with every State in the file, sorted by count.

Now I'm writing the CSS: a warm paper background with dark ink text, a red accent for focus outlines, and a monospace style for the small labels.

Still writing the CSS: a warm paper background with dark ink text, a red focus outline, and a monospace style for the small labels.

Still writing the CSS: table cells with wrapping text and right-aligned numbers, the filter chips and accordion headers with their +/– indicators, and inputs with a thin border on the paper background.

I'm now writing the CSS and the page's markup skeleton, with the header, tabs and layout grid.

Now I'm laying out the JavaScript helpers for escaping text, formatting numbers and percentages, and handling arrays.

I'm writing the helper for building the CSV export, with quoted fields and the active filters described in a summary block.

I'm now writing the top-themes helper: it counts each theme once per record, then sorts by frequency and keeps the top ten along with the years each one spans. Next I'm adding a small function that wraps long labels into lines of about 38 characters.

I'm wiring up the rail: a match count with the total in the file, the filter chips, and a body select that lists each body by its record count for the current mechanism.

I'm wiring the mechanism select so changing it clears the body filter, and I'm working out how the accordion toggles without a full re-render.

I'm building the overview tiles and the state-level list next, then wiring the mechanism and body filters so that changing one resets the other.

I'm settling the headline tiles: each one shows a big serif number with a short breakdown beneath it. I'll put a single note under the row explaining that records are every record in the current filter, documents are the distinct symbols, and years run from the first to the last year.

I'm working out the mechanism tiles next: each one counts its records, distinct documents, latest year, and share of the filtered set, with the UPR tile getting a link to the state list. Then I'm adding the themes chart under a "FIG.01" heading, with its title showing the filtered record count, and a short note under the table about how a theme's year range can reveal an older label.

I'm writing the theme table rows: each theme button shows its count, its share of the filtered records, and the years it spans. I'll add a "No records match" row for the empty case, and I'm planning to draw the two charts only when the overview tab is active, redrawing them when the tab opens and skipping them while it's hidden.

Now I'm writing the record-list rendering: sorting the filtered rows, showing a caption with how many are displayed against how many match and the current date direction, and adding a sortable date header with a reverse toggle. Then I'm looping over the first batch of rows, with a "more" button that hides once everything is shown.

Still writing the record rows: each one gets its date as a toggle button, the body, a link to the symbol, the paragraph number right-aligned, and the first-session field, with the state cell showing the states or "State not found" for UPR.

I'm wiring up the mechanism and body filters so changing one resets the other, and I'm making the accordion toggle its panels without a full re-render. Clicking a record row will expand its details, with the copy-citation button handled separately. Then I'm laying out the Checks tab as a static section that gets updated when its controls change.

Still writing the page markup: the Checks panel gets a short "Check this dashboard" heading with a line on how the app checks itself, followed by a sample section with its controls and tally.

Now I'm writing the sampling step for the random-check section: a seeded shuffle that picks up to ten records from the filtered set, with the seed kept in the box so a draw can be repeated.

Still writing the sampling code: a seeded shuffle that picks up to ten records, then storing the seed, the filter description and the total count so the draw can be reproduced. I'm also adding a random-seed button for drawing again.

Still writing the sample-card markup: each card gets a toggle button with its number, and a set of verdict buttons that record my judgement for that record.

Still writing the cards: each one has a toggle line with its number, the symbol link and the first line of the paragraph, plus a body with the full text, its themes, and three verdict buttons for fits, doesn't fit, or unsure. Now I'm working on the Method tab, which will be mostly static markup with a few buttons.

Still writing the filter-description helper: it collects the active keyword, mechanism, year range, SDG and theme filters into a list of labels, and I'm planning to have it feed both the chips and the summary.

I'm checking the theme counts against the table: I'll read the numbers from the rendered rows, strip the thousands separators, and confirm none exceeds the filtered total.

I'm checking the link validity by confirming each URL starts with the UN docs domain and ends with its symbol, and I'm counting duplicate texts and the unlabelled themes, SDGs and persons with their percentages.

I'm writing the check-result rows now: each shows a pass, fail, warning, or note marker, the check's name, and its values, with an expandable list of records where relevant.

I'm drafting the Method tab text now, covering how every number is a browser-side count, how the filters combine, how themes are counted per record, and how paragraph numbers, states and dates are read from the file.

I'm finishing the header line with the source link, record and document counts, date range, and build date, and I'm making the source link fall back to plain text when no URL is given. Then I'm converting the record count to a number and setting up the year selects from the available years, wiring their change handlers to update the range.

I'm wiring up the year selects to swap the range if the start passes the end, then re-syncing the controls and redrawing. Then I'm filling the static dropdowns once at startup: mechanisms, document types with a fallback label for blank values, states, goals, and years.

Now I'm finishing the dropdown setup and the record-count helpers.

Now I'm writing the render flow: filtering the records, computing the top themes, and updating the rail, overview, and whichever tab is active, with the Method tab text being drafted next.

Now I'm writing the CSV export: it builds a header row and a few comment lines recording the country, source, build date, active filters and row count, and then the data rows.

Now I'm working on the CSV export, adding a few comment lines at the top for the source, build date, active filters and row count. I'm also making sure the notes say the labels come from the UN and aren't checked by the app.

I'm setting up the tab keyboard handling so the arrow keys and Home and End move between the four tabs.

Still writing the keyboard handling and the tab-switching helper, with the aria state and focus following the chosen tab.

I'm setting up the state counts for the overview, tallying how often each state appears across the UPR records and sorting them by count. Next I'm moving on to the timeline chart, where I'll clear any old instance, work out the year span from the filtered records, and build per-mechanism counts for each year.

I'm wiring the timeline chart's stacked bars, one dataset per mechanism that has records in the filtered set, with colours from the mechanism palette and the legend on top. Both charts sit in fixed-height boxes, and the canvases get accessible labels, with the table serving as the text alternative for the first figure.

I'm laying out the table column widths and letting the symbol cell wrap long values. The expandable detail row gets a two-column grid with a large red paragraph number beside the text, and the keyboard handling already covers the buttons inside it.

Now I'm wiring the chip row so each active filter appears as a removable button, with its removal action clearing that one filter and refreshing the view. The filters I'm tracking are the search text, mechanism, document type, state, year range, SDG, and each theme, and clearing the year range resets it to the full span.

I'm finishing the state list and the chip removal wiring, with the UPR tile's toggle controlling whether the state list shows.

Now I'm finishing the write-up: a tally line that counts fit, doesn't fit, and unsure verdicts out of the judged total, with the seed shown and a note that these are the user's own judgements rather than app results. For an empty sample, the message will just prompt to draw ten records first.

