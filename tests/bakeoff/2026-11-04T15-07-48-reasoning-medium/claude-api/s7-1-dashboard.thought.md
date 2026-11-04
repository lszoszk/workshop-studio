I'm starting on a large single-file HTML build, aiming for under about 1500 lines while keeping it lean. The layout is a header, a left rail, a main area with tabs, and a footer, and I'm laying out the state I'll need to track: the filter fields, the open heading, the active tab, sort direction, shown count, seed, and verdicts. I also want to precompute a paragraph text and state list for each record.

I'm setting up the paragraph and state parsing for each record, along with the lowercase search text and index. Next I'm adding the theme filter from chart clicks with removable chips, and laying out the rail sections for keyword, mechanism and years/SDG.

I'm working out how to pull the state names out of each record's trailing parenthesised groups, accepting only groups without commas and under about 60 characters, and falling back to "State not found" when nothing valid remains. I'm also weighing whether the nested regex could backtrack badly on long text, and deciding it's an acceptable risk. Next I'm settling the keyword filter as a check that every word appears in the record's lowercase text, and sorting records by date descending, then body, then paragraph number.

I'm settling how the table sorts and expands: rows get a main line plus a hidden detail row, tracked by id, with a 50-row render batch and a visible count. For highlighting, I'm escaping the text and then wrapping matched keywords, while still working out how to escape the search words safely.

I'm wiring up the charts so they redraw on each update, with the bar chart's values drawn at the bar ends and clicks adding a theme filter. The stacked chart will span every year from the first to the last in the filtered set, and I'm only rendering the active tab, since Chart.js can't size canvases that are hidden.

I'm setting up the tab panels so each one persists, with the search input and table skeleton built once, and only the active panel's contents updated on each render. The charts will live in the first panel and be created once it's visible, and the sample tab will draw its sample from the current filtered set using the seed.

I'm setting up the sample tab to draw from the filtered set with a seeded shuffle, and each card will be a single header line that expands to show the full text, theme chips, and verdict buttons, with the symbol link placed alongside the header.

I'm weighing the checks for the sample tab, setting each one up as a name, a detail, and a pass, fail or warn status, and I'm computing them.

I'm listing the checks for the sample tab: the record count, the mechanism, body and year partitions, and the type partition. For the chart-versus-table check, I'll compute the top themes two different ways and compare them, then confirm the largest count doesn't exceed the filtered total. Last, I'll verify every doc link starts and ends with its symbol, reporting up to ten failures.

I'm laying out the checks for the sample tab that cover the state-count and missing-state cases, plus the paragraph share per mechanism, with UPR held to full coverage and anything short of that flagged as a warning. I'll show the states without a match in a collapsible list, and the duplicate and unlabelled counts alongside them. The main caching point is that everything except the chart comparison is computed once against the full file.

I'm settling the CSV export: a few comment lines first, then a header row with the date, mechanism, body, type, symbol, paragraph, state, section, text, themes, SDGs, targets, affected persons and document link. Quotes inside fields get escaped, and I'm adding a byte-order mark so accented characters open correctly in Excel. For the licence line, the data carries no licence field, so I'll point to the OHCHR source page instead of claiming one. Downloads go through a blob URL and a synthetic link click, and copying uses the clipboard API with a textarea fallback.

I'm laying out the rail sections: keyword input first, then the mechanism, body, type and state selects with counts from the whole file, and the year range and SDG selects after that. When the mechanism changes I'll reset the body if it no longer fits, and the state list will only show States that were actually found.

I'm laying out the overview tiles: a total record count with a type breakdown, the document count, and the year span. Below those, one tile per mechanism showing its records, documents, latest year and share of the filtered set, with a "see the States" link on the UPR tile to toggle the state list.

I'm settling how the theme table reports each theme's records, share and year range, and I'm adding a short static note that a theme's year span can point to legacy labels, to be checked on tab 03. I'll format the numbers with en-GB thousands separators and show the source line under each figure, with the count of filtered records.

I'm laying out the rest of the page: chips for each active filter, a header with the source link and record counts, and CSS for the tabs and a stacked layout below 900px. For the expanded row, I'm planning a colspan cell with the paragraph number, full text, labels, SDG names, targets, affected persons and section, plus copy-citation and document-link buttons, keyed by record index and toggled from one delegated click handler.

I'm settling the sample tab's row expansion: a click or Enter on a row toggles it, ignoring clicks on links. The copy-citation button will read differently when there's no paragraph number, and the caption will show filtered versus total matches, newest first, with the date header as a sort toggle.

I'm writing the data setup now: loading the records, plus helpers for escaping HTML, formatting numbers, and matching paragraph numbers.

I'm normalising each record's themes, SDGs, targets and affected persons into private fields, and pulling a paragraph number out of the start of each text.

I'm working out how to find which States a UPR record names, by pulling the parenthesised groups from the end of the text, keeping only the ones without commas and short enough to be a State name. Then I'm checking that the matching doesn't hit trouble on long texts.

I'm setting up the filter state object, with the keyword, the selects, the sort direction and the set of expanded rows, and I'm writing the filter function that narrows the records down.

I'm settling the year filter so the earliest and latest selections swap if they're reversed, and the rail's skeleton stays static so the selects keep focus when they change.

Setting up the rail controls now: the selects and keyword box get built once, with only the body options rebuilt when the mechanism changes, so focus stays put. Next I'm syncing control values from the state and adding the match counts and chips.

Still writing the theme-ranking helper, grouping records by theme with counts and year spans.

Writing the chart plugin that draws the values on the bars now...

Now I'm laying out the mechanism tiles, with the UPR tile carrying a "see the States" toggle that opens the list of states beneath them, ten at a time.

Now I'm setting up the sample tab's table: a skeleton with a search box and caption, the date header as a static sort button, and a tbody filled in on each render. A "Show 50 more" button sits below it, and the recommending State filter lives in the rail.

Next I'm wiring the sample tab's row expansion and the copy-citation button through delegated handlers, then moving on to the checks tab, which lists each check as a pass, fail or warning line.

I'm settling how the sample tab's draw buttons behave: "Check 10 at random" will use a random seed shown in the box, and once drawn, "Draw again" and "Draw with this seed" appear alongside the seed input.

Still writing the sample draw: a seeded shuffle that picks up to ten matching records and keeps the first ten as the sample.

Still writing the sample tally: counting how many of the drawn records are judged to fit, not fit, or are unsure, shown against the number judged.

I'm wiring up the sample tab's verdict cards, so each one can be opened, shows its theme chips and three verdict buttons, and keeps keyboard focus after a click. Then I'll set up the methods tab, filling in the summary text, the static method notes and the source line, and build a describeFilters helper that gives a plain list of the active filters for the chips and the CSV.

I'm wiring up the rail's chips and tab switching, with the accordion sections opening one at a time and the body hidden until clicked. The keyword inputs will be debounced and kept in sync, and the mechanism select will update the body options.

Next I'm setting up the rail's dropdowns: the mechanism, body, SDG goal, and record type selects, with the body list rebuilt only from the chosen mechanism's bodies and the counts taken over the whole file.

Next I'm finishing the CSS: a focus ring on interactive elements, a stacked layout below 900px, and styles for the tabs and expanded rows.

I'm writing the stylesheet now: the monospace labels, the serif headings, a two-column layout with a rail on the left, and the tab and tile styling.

Still writing the stylesheet: tab and table styling, plus the rules for the rail and filter chips. Next I'm wiring up the rail's rendering and the chip buttons.

Now I'm building the overview tab's content: a tile for the total count of filtered records, with a breakdown by record type, plus document and year-span figures. Each mechanism gets its own tile, grouped in a single pass over the filtered set, and a short note explains how the numbers are computed. Then I'll update the theme figure's heading to show how many filtered records it covers, and add a table of the top themes below.

I'm writing the verification checks now: a sum helper over each key, and a link check that decodes each document URL and compares it against the symbol.

I'm checking the mechanism figures: each one's share against the total, with UPR flagged as a warning if it falls below 100, and the rest shown as passes with their counts in one line. Then I'll run a chart check that recomputes the top themes fresh from the filtered records if the overview hasn't been rendered yet, counting each record once per theme.

Now I'm weighing how to keep the checks tab honest: if I recompute the chart and table values inside the checks, I can't rely on the overview having been rendered, and hidden canvases complicate redrawing. I'm leaning toward storing the last computed top-themes values in module-level variables so the check can compare them directly.

Now I'm working out how the checks tab should confirm the theme figures: rather than trusting the overview's last render, I'll recompute the top themes from the filtered records and compare them with the values the chart and table are drawn from.

Now I'm wiring the rail's state dropdown, which lists states from the whole file with their counts, sorted by count, and hides itself when there are none. The copy-citation button will swap its label to "Copied" for two seconds and then restore its original text.

Next I'm setting up the tab panels so only the active one shows, and building the three accordion sections in the rail, each with a collapsed body that opens on click.

