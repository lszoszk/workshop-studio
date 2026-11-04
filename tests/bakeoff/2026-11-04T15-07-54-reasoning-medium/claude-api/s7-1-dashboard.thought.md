I'm going to build this as one complete HTML document, aiming for something compact enough to stay under about 1500 lines while still covering everything. First I'm sketching the layout: a header, a left rail, and a main area with tabs. I'm also laying out the state I'll need to track, which covers the filters, the open heading, the active tab, sort direction, the expanded item, the sample seed, and the verdicts, with the keyword and mechanism filters among them.

I'm settling the rest of the filter design: the keyword and mechanism, body, type, and state filters are selects, and theme chips from chart clicks can be removed. I'm also planning a search box on tab 02 that stays synced with the keyword filter, and I'm setting up the paragraph-number and trailing-state parsing for the records.

I'm settling on how to handle the state parsing: every parenthesized group at the end of a record has to pass validation, and if any one fails, the record gets "State not found" rather than a partial result. Then I'm working out the sort order, which goes by date, then body, then paragraph number compared numerically by its major and minor parts, with file order as the final tiebreak, and the date direction can be toggled.

I'm working out the overview tiles next, weighing whether the record count should cover the whole file or only what the current filters leave visible.

I'm working out the overview tiles, deciding that the record count should follow the current filter and say so, with a per-type breakdown. The mechanism tiles will show a color dot, record and document counts, the latest year, and share of the filtered set, with the UPR tile offering a "see the States" link that expands in place to a top-ten list. Next I'm turning to the FIG.01 bar chart as a horizontal Chart.js bar setup.

I'm laying out the rest of the view logic: the chart click adds theme filters that stack as chips, and the rail shows the count against the file total. Headings are only on tabs 01 and 02, one open at a time, with everything closed by default. For the year and body selects, I'm pulling distinct years from the full dataset and swapping the range if it's reversed, and deciding whether body counts should cover the full file or just the chosen mechanism.

I'm now checking the figures against each other: the record count against the header total, the mechanism, body, and year breakdowns each summing back to the whole, and the chart bars against a fresh recount of the table rows.

Now I'm writing the consistency checks: a few link-format checks for the document URLs, a per-mechanism share of paragraph numbers with UPR expected to hit 100%, and a count of UPR records that yielded a state, listing any that didn't along with the tail of their text.

I'm adding the last checks: a duplicate test on IDs and text, plus a count of unlabelled entries. The file-integrity checks run over the whole dataset, while the chart check uses the filtered set. For the sample, I'm drawing 10 records from the current filter with a seeded generator, so the same seed gives the same draw.

I'm settling the sample step: it draws 10 records from whatever filter is active, and the first button becomes "Draw again" once a sample exists. The verdicts are kept per record ID for each draw, and a running tally sits alongside.

I'm wrapping up the export and method tab: a CSV download with the metadata as comment lines, a copy-summary button with a brief confirmation, and then I'll move on to how each record expands.

I'm setting up the table rows so each one opens on click or keyboard, using a real button in the first cell for the expand toggle, with a single delegated handler on the table body so the button's click doesn't toggle twice. The expanded view goes in a following full-width row showing the paragraph number and the full text.

I'm working out the export and detail views: each expanded row will show the full paragraph text, its themes, SDG labels, and a citation copy button, and the table will sit alongside a caption giving the matching count. I'm also keeping the search input out of the re-rendered area so typing doesn't lose focus.

I'm settling the rail: the three filter panels are built once, and only the select options for body get rebuilt when the mechanism changes, so the keyword inputs keep their focus while typing. Tab 03 and 04 will hide the headings container, and both search inputs get a 300ms debounce with the other one kept in sync immediately.

I'm planning the layout as a 240px rail beside the main column, stacking on narrow screens, with the tabs set up as an accessible tablist that works with the arrow keys. Since Chart.js can't size itself on a hidden canvas, I'll only draw the chart when the first tab is active, rendering it again on each tab switch while the rail stays up at all times. The chart will sit in a fixed 360px box with the aspect ratio off, and long labels get trimmed on the axis while the full names stay in the table below.

I'm working out how a click on a bar of the chart will add a theme filter, using the chart's nearest-point interaction along the y-axis so the click registers on the row. I'm also weighing whether to make the theme names in the table buttons too, so keyboard users can filter without the chart.

I'm settling the timeline chart: the years run from the earliest to the latest in the filtered set, with one stacked series per mechanism that appears anywhere in the full file so the legend stays stable. I'm also setting the header to read "UHRI · Kenya" with the title and a source line linking to the source URL.

I'm finishing the rail and tab setup: a 300ms debounce on both search inputs, with the other one kept in sync straight away. I'm also planning the UPR "see the States" link, which opens an inline top-ten list inside its tile.

I'm working out the state breakdown: ranking the top ten States across the filtered UPR records, with a note that these count recommendations rather than influence, and a separate count of records where no State was found. I'm also settling the year selects, defaulting to the full range, swapping the bounds if they're reversed, and only showing a chip when the range isn't the full span.

I'm settling the filter chips and the year selects: each chip has a remove button, and "Clear all" resets everything and syncs the controls. I'm also planning the "How computed" notes to stay within two sentences each, and a helper that escapes text before it goes into the page.

For the first line of each record, I'll collapse whitespace and cut at the last space before 120 characters, adding an ellipsis only when the text is actually shortened.

I'm sorting the filtered records by date, newest first by default, then by body name, then by paragraph number with unnumbered entries last. A "Date" header button will show the sort direction through aria-sort. The table starts with 50 rows, with a "Show 50 more" button for the rest, and the open record is tracked by index so only one row expands at a time.

I'm settling the summary copy: it lists the country, source, how many records match out of the total, the document count, the year span, the per-mechanism figures, the active filters, and the top ten themes with their counts. A shared filter-description helper will feed both that and the CSV. I also want the overview chart and its table to agree, so I'm checking the chart's values against a separate count of the themes, and I'll compute that overview data on every update while only drawing it when its tab is active.

I'm checking the theme counts two ways: the chart data against a separate count, and the table cells read straight from the DOM. Ties sort alphabetically by name, and I'll render the checks panel on every update.

I'm setting up the sample section as its own container with a fixed seed input, and keeping the checks panel separate so each can re-render on its own. I'm drawing the sample with a seeded shuffle over the filtered records in file order, so the same seed always gives the same ten picks.

I'm laying out the sample section: each sampled record gets a card with a verdict button set, and the open card shows the symbol, paragraph and full text along with its theme chips, or "not labelled" when there are none. The link to the document sits only in the open part, and the list of links that fail the check gets capped at twenty entries with a note for the rest.

I'm laying out the check results as a list, with each line showing a status label, the item name, and its values. For the mechanism coverage, the Universal Periodic Review line gets a warning if it falls short of 100%, while the others stay as plain information. I'm also planning a separate note on how many records have no themes, SDGs or affected groups, and I'm working out how to count duplicate text values.

I'm writing the JavaScript for the page now: precomputing each record's fields, then the text-escaping and first-line helpers.

I'm parsing the state names out of each UPR record: the text is matched for a run of parenthesised groups, each group is trimmed, and any group that is empty, contains a comma or runs past 60 characters makes the whole record count as having no States.

I'm now writing the filter function, which checks each record against the active mechanism, keyword, and year settings.

I'm setting up the overview to be built on every update, with the summary tiles and the states box filled in each time. The charts themselves only get drawn when the overview tab is active, so the hidden table stays current either way.

I'm laying out the tiles now: a headline tile with the record count and a breakdown by type, plus tiles for documents and year span, and one per mechanism with its colour dot. The UPR tile gets a "see the States" button that opens the top-ten list in place inside its tile.

I'm laying out the overview tiles: a headline count with the type breakdown, then documents, year span, and one tile per mechanism, with the UPR tile holding an in-place list of the top States. The theme table will show records, share of the filtered set, and year range for each theme, and the timeline chart gets a source footnote naming the country and build date.

I'm laying out the header and the rail with the count and the filters, and I'm starting on the skeleton markup for the page.

I'm setting up the filter controls next: a keyword box, the mechanism, body, type, state, year and SDG selects, and an accordion heading for each filter group.

I'm wiring up the filter controls next: each select gets populated once at startup, with the body list rebuilt whenever the mechanism changes, and the state options show a count for each one.

Since the current rewritten thinking already describes the page code being written, this next stretch is more of the same, so a short phrase fits.

Writing copy and CSV helpers...

Writing the clipboard copy helper with a fallback and a brief "Copied" note.

I'm writing the table row handling now: clicks on a copy button copy the citation, while clicks elsewhere on a row toggle its detail. Since the table re-renders after each toggle, I'll restore focus to the row's button afterwards.

Next I'm laying out the checks panel as a list of items, each with a status, a name and its values. A few of them are partition checks: I'll sum the mechanism counts and compare them against the total.

I'm styling the tabs and the contrast of the hint text, then starting on the JavaScript.

I'm defining the shorthand selectors and the HTML escaping and number formatting helpers, then getting the percentage formatting ready.

I'm defining the escaping helper for the text that goes into the highlighted snippets, since it has to handle the search words safely.

I'm working out the chart code and the summaries it draws from, so the same theme-level figures can feed both the tiles and the charts.

Setting up the Chart.js bar chart for the theme counts now, with horizontal bars and value labels.

Still wiring the chart tooltips and value labels, and setting up the timeline next.

I'm setting up the tab switching now: the active tab decides which panel shows and what gets rendered, with the charts only drawn on the overview and the records and checks built on demand. The filter summary on the last tab gets refreshed whenever the filters change.

I'm setting the sample section up with a seeded shuffle, so the same seed always draws the same ten records from the filtered set.

I'm wiring the sample section now: a seeded shuffle draws the same ten records for any given seed, and the button either uses a random seed or the one typed in. Once drawn, the card list and the tally of fit, not-fit and unsure answers get rendered, with card clicks handled through event delegation.

I'm writing the record-sorting logic next, so the table can show the newest first by default and flip to oldest first when toggled.

I'm working out how the records get sorted: newest first by default, with the date compared first, then the body, then the paragraph number, and the record index as a final tiebreak.



