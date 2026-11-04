I'm planning a single HTML file under about 1500 lines, so I need to be careful with the build. The main limit is keeping clickable items in a view to around seven: four tabs and three filter headings, with the filter content tucked inside closed headings.

I'm settling the rail and tab layout now: the rail keeps its headings on tabs 01 and 02, while 03 and 04 drop down to just the number, bar, and chips. For tab 02, I'll bind one keyword state to both the rail input and the search box at the top, so the two stay in sync.

I'm working out how to parse each record, tagging it with a paragraph and any State names found at the end of its text, plus a stable index for sorting. The State detection uses a parenthesized-group regex anchored to the end of the text, and I'm checking that it won't backtrack badly on texts up to about 2500 characters.

I'm checking how the state-detection regex handles the match position. Because it isn't anchored at the start, the engine returns the leftmost spot where the parenthesized groups run to the end of the text, so a stray "(a)" mid-sentence gets skipped when it isn't followed by the terminator. A single trailing group like "(France);" or a run like "(Cabo Verde) (Slovenia) (Togo);" both match cleanly. The weak case is a parenthesized acronym before the real states, such as "(CAT) (France);", which would be taken as a state name unless I add a filter.

I'm parsing the state names out of the parenthesized groups, keeping only those without commas and under 60 characters, and skipping the record if none of its groups qualify. Then I'm working out how to sort by date descending, then body, then paragraph number, and I'm checking how to compare numbers like "144.100" against "144.43" so the sort doesn't misplace them.

I'm settling the sort order: date first, then body, then paragraph number compared as numeric pairs so "144.100" doesn't land before "144.43", with records lacking a paragraph number pushed to the end. For the date header I'll just flip the date comparison and leave the rest ascending, with a caption noting oldest first. Then I'm defining the filter state, covering keyword, mechanism, body, type, State, year range, SDG, and a list of theme chips that all have to match, each shown as a removable chip.

I'm working out the filter dependencies next: the Body options will only list values present in the chosen mechanism, each with its count across the whole file, and the Type options will follow the same rule. If the mechanism changes and the current Body no longer applies, I'll reset it. For the year range, I'm deciding how the From and To selects default to the earliest and latest years, and swapping them if From ends up later than To.

I'm laying out the overview tiles: a total count for all records with a per-type breakdown, plus documents and years, then one tile per mechanism showing its records, documents, latest year and share of the filtered set. The UPR tile gets a link that opens the list of States in place, and the Type filter stays in the rail.

I'm sorting out the first overview tile: it reads the filtered set, so it shows the count of matching records out of the total, with a per-type breakdown that adds up to that headline number. The mechanism tiles follow the same filtered counts and shares, and every mechanism in the file gets a tile, even when it shows zero. Next I'll set up the top-ten themes bar chart, drawing each value at the end of its bar with a small inline plugin, since the datalabels plugin isn't available.

I'm moving on to the second figure, a stacked bar chart of records per year split by mechanism, and I'm making sure every year between the earliest and latest in the filtered set appears so gaps show up.

I'm weighing whether to put a short note under each tile and figure, or just one under the tile row, and I'm leaning toward a brief monospace note per element so each stays self-explaining.

I'm settling how the State list works: it'll show the ten States with the most recommendations to Kenya under the current filter, with counts, and if the mechanism filter excludes UPR the list will simply say it's empty. The link in the UPR tile will open that list in place, and I'm deciding whether the panel sits inside the tile or directly beneath the tile grid.

I'm settling the layout for the second tab: a search field, a caption, and a table of matching records with a "show 50 more" control. The columns will be date, body, symbol, paragraph, the recommending State for UPR rows, and first line, with the State column placed after the paragraph number.

I'm setting the results table to wrap rather than use fixed column widths, since the first-line column has the most text. Each row will expand into a detail row spanning all six columns when activated, using tabindex and aria-expanded, and I'm keeping the symbol link from toggling the row.

Now I'm writing the keyword highlighting helper, which will split the raw text on the search words and escape each piece before wrapping matches in marks.

I'm building the keyword highlighter: it splits the raw text on the search words, escapes each piece, and wraps the matches in marks. Next I'll settle how the first-line snippet is cut at 120 characters.

I'm writing the expanded detail view for each row: the paragraph number in red, the full text, the labels and recommending States, and two buttons for copying a citation and opening the UN document. The copy button falls back to a hidden textarea if the clipboard is blocked, and shows "Copied" for two seconds.

I'm checking the sort and filter logic against the whole file, and I'm planning a set of checks that cover record counts, partitions, links, paragraph numbers, State values, and duplicates. The chart numbers will get their own check: I'll recompute the top-ten theme counts a second way and compare them with the values the chart actually drew.

I'm weighing how the sample check should behave when the filter changes: either it redraws on its own, or it clears and asks the user to draw again. I'm leaning toward clearing it so the verdicts never describe a filter that's no longer on screen.

I'm settling the sample check: the initial draw will use a random seed shown in the seed box, and the "Draw again" and "Draw with this seed" controls will come up once the cards are on screen.

I'm working out the sample check's seeded draw: a shuffle-based selection of ten from the filtered records, so the same filter and seed always give the same ten. Next I'll lay out the ten cards as single lines, one expanded at a time.

I'm working out the tally line for the sample check, counting how many of the ten cards are marked as fitting, not fitting, or unsure, and checking that the three numbers add up to the ten judged.

I'm settling the checks on the partitions: the records by mechanism, by body and by year should each add up to the total, so I'm comparing those sums against the record count.

I'm setting up the consistency checks now: the chart's top-ten theme counts get recomputed and compared against the values actually drawn.

I'm listing the record links to check that each one points to the UN document page for its symbol, comparing them case-insensitively after decoding. Records that fail will be shown inline, capped at around twenty with a count of any remainder.

I'm going through the data-quality checks now: a per-mechanism paragraph-number share where UPR should be complete, and a list of UPR records missing a recommending State, showing each one's symbol and the last 80 characters of its text. I'll cap that list at fifteen and mark missing States as a warning rather than a failure, then add the duplicate and "not labelled" counts and the sample check, with a red or pass mark on each line.

I'm setting the Method tab's content: a short note on the approach, plus a Download CSV button and a Copy summary button. I'll put the data source, a line saying the licence isn't stated in the file so the reader should check the source page, and the build date at the bottom, naming OHCHR's UHRI as the origin. For the CSV, I'm planning a few comment lines with the country and export details, then a header row with date, body, mechanism, type, symbol, paragraph, recommending States, section, text, themes and SDGs.

I'm writing the Method tab's CSV and summary exports now: the CSV gets a few comment lines and a header row with the record fields and an escaped, pipe-joined themes column, and the summary is plain text covering counts, breakdowns and filters. Next I'll set up the header label and page title, with the source link and the basic record and document totals.

I'm laying out the Method tab next, with the data source, a note that the file doesn't state a licence so the reader should check the source page, and the build date at the bottom. The footer will show the record count and the source link, and the rail on the last two tabs will keep only the number, bar and chips.

I'm setting up the year-range, SDG, and body filters now: bodies listed by count within the chosen mechanism, states ranked by UPR count, and SDG goals labelled by number and name. For the top ten themes, I'll count them with a map and sort by count, then alphabetically. Next I'm working out the earliest and latest year for each theme among the filtered records.

I'm wrapping up the theme section: a hint under the table says a wide or old year range can point to a legacy label, so the reader should check a sample on tab 03. I'm also weighing click-a-bar-to-filter and the "Theme: X ×" chips, and the chart needs care because it sits on a hidden tab.

I'm deciding where the chart gets drawn: only when the overview tab is active, with its own render on tab switch. The rail and the other tabs can re-render every time, but the table-versus-chart check can't read the DOM from tab 03 unless the overview has already been rendered, so I'll store the values it needs instead.

I'm weighing whether the chart and its matching table can be checked against each other. Reading the table from the DOM fails on tab 03 unless the overview has already been drawn, so I'll keep the chart values stored when it renders, and render the chart only while the overview tab is active.

I'm deciding how the chart gets drawn: I'll build the overview stats and table on every update, but only draw the charts while the overview tab is active. Since a hidden canvas starts at zero size, I'll call resize on the charts after switching tabs to be safe.

I'm wiring up the event loop around a global state object, with `update()` recomputing the filtered records and re-rendering the rail and sections, and a 300ms debounce on the keyword field. For the checks, I'll recount the chart values from the stored chart data with a second pass and parse the theme table rows from the DOM, then compare the two.

I'm settling the small helpers now: a number formatter using British grouping, an escape function for the output, and a fixed colour for each mechanism with a neutral fallback. Last, I'm counting distinct symbols to get the document total.

I'm setting up the Method tab's layout and accessibility: the tab buttons get roving tabindex with arrow, Home and End keys, the panels take the tabpanel role, and I'll add a clear focus ring plus a hidden-attribute rule so hidden sections stay out of view. For the page grid, I'm planning a 260px rail beside a wide main column, collapsing to a single column below 820px, with the rail's position still to be settled.

I'm writing the Method tab's layout with the rail on the left and the main column beside it, plus the markup for the header, tabs and filter rail.

I'm setting up the filter rail: a clear-all link, the live match count and its bar, the active filter chips, and three collapsible facet sections, with the main panels beside them.

I'm setting up the overview panel next: a headline question about the country, a row of summary tiles, and then the charts and table. The panel is built on every update, but the charts only get drawn while that tab is active.

I'm laying out the overview's headline tiles, the mechanism breakdown and the state panel, with a note under each. The first figure gets a chart and a matching theme table, both built from the same filtered records.

I'm now wiring the overview's second figure: a bar chart of the mechanism breakdown with a matching theme table, drawn from the same filtered records, with value labels added by a small plugin.

I'm setting the chart's value labels to appear at the end of each bar, with extra right padding so they fit, and hiding the x-axis ticks to keep it clean. For the long theme names on the y-axis, I'll truncate the labels to about 38 characters, with the full name kept elsewhere.

I'm settling the overview's second figure, a stacked bar chart by year and mechanism, with its theme-free table and a legend that uses point styles.

I'm defining the theme statistics: each record's themes are counted once per record, and for each theme I track how many records carry it along with its earliest and latest year, then sort by count and then alphabetically.

I'm writing the parsing step now: each record gets its paragraph number pulled from the start of its text, and for UPR records I'll scan the text for state names.

I'm finishing the parsing step: the paragraph number is pulled from the start of each record's text, and for UPR records I scan for state names inside the matched group, keeping only short names without commas. Next I'm working out the symbol totals for each record.

I'm building the filter function now: it takes the search words and checks each record's lowercased text and symbol separately, so a match can't span the boundary between them.

I'm writing the filter logic now: the mechanism, year range, SDG and theme checks, and the keyword match, with the year selects swapped if they're reversed and the active state kept as plain numbers.

Writing the sorting helper now, with the newest records first by default.

I'm now setting the table row markup: each row is focusable, carries its record index, and tracks an expanded state, with the document link, paragraph number and state names in their own cells.

I'm making the table rows expandable: in-place, a click toggles a detail row, and I'll keep focus on the row so it isn't lost when the table changes.

I'm adding a copy-citation button to each row, which builds a citation from the document symbol and paragraph number, or just the symbol when no paragraph is found. I'll also add a link that opens the UN document in a new tab.

I'm now laying out the detail panel for each row: a definition list covering themes, SDGs and targets, affected persons, section, type and recommending state, with "not labelled" shown in muted italics wherever a field is missing. I'm also building the header tiles for records, documents and years, and the mechanism tiles with their coloured dots.

I'm working out the mechanism tiles' share figures and the Universal Periodic Review tile's "see the States" toggle, which reveals a list of the ten States that made the most recommendations, with a note on records where no State was found. After that I'll write the check tab, where each count gets verified against the total.

I'm setting up the check tab: a list of self-checks that each show a pass or fail, followed by a sample section where the user can judge the UN's labels themselves. The check results don't depend on the filter, so I'm considering caching them rather than recomputing on every update.

I'm wiring up the filter-change handler so that it resets the visible row count and the sample, then re-renders the views. The UI-only changes, like the states toggle and sort direction, will just re-render the affected parts.

I'm writing the check functions now, starting with a record-count comparison against the declared total in the file header.

I'm writing the count checks now: the record total against the declared count in the file header, then each mechanism, body and year value tallied so the sums can be compared to the record count.

I'm writing the check functions: first a comparison of the record count against the total declared in the file header, then a tally of mechanism, body and year values so each set of counts can be summed and checked against the number of records.

Checking the chart labels against the table comes next, and I'm confirming the largest bar never exceeds the filtered record count.

I'm also validating the document links: each must be a UN docs URL that ends with the record's symbol.

I'm wrapping up the checks with the state coverage: I'll count how many UPR records have a State found, flag any that don't, and show the distinct state count. Then I'll flag duplicate ids and duplicate texts, and count the records with no themes.

Writing the mulberry32 seeded random generator for the sample draw.

I'm drawing the sample with a seeded random generator, shuffling the filtered record indices and taking the first ten, with the seed rounded to a whole number.

I'm now setting up the sample section so that the controls, the cards and the tally each live in their own container. That way a verdict click only redraws the cards and tally, and the seed input keeps whatever value was typed. I'll also restore focus to the verdict button after each re-render so keyboard users don't lose their place.

Now I'm writing the CSV export helper, which escapes each value before joining the rows.

Now I'm writing the CSV export helper: values get quoted and escaped when they contain commas, quotes or line breaks, and the file is built with a download link.

I'm now styling the headline tiles and mechanism markers in the stylesheet, using a warm paper palette with a red accent and serif, mono and sans type.

I'm styling the buttons and the tab bar next, with outlined buttons that invert on hover and tabs marked by a red underline on the selected one.

I'm now adding the rail and tab keyword inputs, keeping them in sync with a short debounce so both drive the same filter. I'm also setting a result caption that states the shown and matching counts.

I'm adding the table's date header as a button that reverses the sort order, and a "Show more" button that disappears once every row is shown.

Writing the tab switcher now, so that selecting a tab updates which panel is visible and moves focus with it.

I'm finishing the tab switcher, which hides the other panels and shows the keyword filters only on the first two tabs. Then the main render function reapplies the filters, sorts the records and redraws every view in turn, with the chart drawing done only for the overview tab.

I'm building the chip list for the active filters, with each chip's remove handler stored so a click can clear that one filter. After any removal I'll sync the controls and re-run the filter.

I'm setting up the select options with a small helper that escapes each label, and I'll guard against a current value that isn't in the list. Next I'm building the mechanism, body and type dropdowns, with the counts for each option.

I'm setting the mechanism, body and type options so each count reflects the current filters. If the chosen body or type no longer appears, I'll clear it. The State dropdown lists each state with how many records it covers, and I'll hide that group when no state was found. The SDG options use the goal names from the data. Then the select changes need to update the filters and rebuild the dependent dropdowns.

I'm setting up the accordion so that opening one section closes the others. Next I'm working out the chart title, which reads from the filtered count and shows "No records match" when nothing is left. For the year chart I'm building a dataset per mechanism that has at least one filtered record, so the legend stays free of empty entries.

I'm writing the Kenya summary text now, as a short paragraph built from the same filtered figures.

I'm writing the Kenya summary as copyable plain text, covering the file date, active filters, matching counts, breakdowns by type and mechanism, and the top themes. Then I'll add the copy helper, which tries the clipboard API first and falls back to a hidden textarea.

Now I'm wiring the tab switch so the active tab is marked selected and its panel shows, with focus moving along when a tab is picked.

Next I'm writing the render functions, with the UPR detection in the tile section.

Now I'm working out the keyboard handling for the tabs: arrow keys step through the four tabs, while Home and End jump to the first and last.

Now I'm wiring the keyboard controls for the tabs, so the arrow keys step through the four tabs and Home and End jump to the first and last.

Continuing the render path, I'm now writing the record table so it draws only the first batch of rows, with a "Show more" control to add the next fifty. Each row gets an expandable detail view, and the date header toggles the sort direction.

Now I'm finishing the record table and the chart code, keeping the chart drawing separate from the table render.

Still writing the chart configuration...

I'm writing the chart configuration now, with a fixed height for each chart box and footer text giving the source and record count. I'll make sure the overview breakdown is populated before writing out the final code.

