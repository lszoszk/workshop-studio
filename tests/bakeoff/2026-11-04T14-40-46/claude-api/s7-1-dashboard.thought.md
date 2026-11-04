I'm planning a single HTML file of under about 1500 lines, so I need to be careful with it. The interface should keep roughly seven clickable things per view, counting tabs, filter headings, and buttons together, and I'm checking whether the current plan of four tabs, three headings, and a Clear all button stays within that.

I'm now defining the data layer: pulling the records from the workshop dataset, and pre-computing each paragraph's sort key, its numeric parts, and its state tags. For the state tags I'm working out a regex that catches trailing parenthesized groups, and I'm checking that it won't backtrack badly on long text.

I'm working out how to derive the state labels from each paragraph's trailing parenthesized groups: keeping the ones without commas and under 60 characters, trimming spaces, and falling back to "State not found" when none qualify. Then I'm sketching the filter state object, covering keyword, mechanism, body, type, state, year range, SDG, and a set of theme tags that come from bar clicks and combine with the other filters.

I'm settling the filter panel: the left rail gets numbered headings for keyword, mechanism, body and type, plus years and SDG, and it stays visible only on the first two tabs. For the dropdowns I'm using select elements rather than radio buttons so the click count stays down, with the state filter also a select.

I'm settling how the filter state and rendering fit together: a single render pass that recomputes the filtered set, refreshes the rail's counts, chips and select options, and redraws the active tab. I'm keeping the search inputs out of that rebuild so typing doesn't lose focus, and only updating their values when they differ and aren't the one being edited, with a 300ms debounce on both.

I'm deciding how the tab 03 check panel gets its numbers: mostly from the whole dataset, with a chart view on top. Tabs will be rebuilt from scratch on each render, so the view matches whichever tab is active.

I'm working out how the tab 03 check panel gets its numbers, and it will be drawing a random sample of ten records from the current filter. If the filter changes, the sample gets redrawn automatically with the same seed, and the verdicts reset.

I'm settling the tab 03 sample: the box keeps the seed (default 1), and "Check 10 at random" draws with that seed. After a draw, the buttons become "Draw again" with a fresh random seed and "Draw with this seed" to reuse the box value.

I'm laying out the verdict buttons and how the open card is kept, so that clicking a verdict doesn't rebuild the whole sample list and collapse the card that's open.

I'm laying out the Tab 01 overview: the first tile shows the filtered record count against the total, broken down by type, with separate tiles for documents and years, followed by the mechanism breakdown.

I'm laying out the Tab 01 mechanism tiles, one per mechanism in the file showing record and document counts, the latest year, and its share of the filtered set. The UPR tile gets a "see the States" toggle that opens a top-ten list of states making recommendations to Kenya, counting each state once per record. For the Chart.js bar figure, I'm adding an inline plugin to draw the counts at the bar ends and destroying the previous chart on each render.

I'm setting the bar colour and adding a wrapping callback so the long theme labels fit on the y-axis, with the chart held at a fixed height. I'm also planning a "click a bar to filter" hint, and making each theme name in the table below a button so keyboard users can filter too.

I'm adding a short note under the theme table saying that a theme whose records all come from old documents may be a legacy label, to be checked on tab 03. For the stacked yearly chart, I'm using the filtered set's first-to-last year range, colouring each mechanism with its own colour and falling back to grey for unknown ones, and keeping the legend on.

I'm laying out Tab 02 now: a search box above a table with date, body, symbol, paragraph, first line, and recommending state columns, sorted by date newest first with a toggle on the Date header. Each row expands into a detail row when clicked or activated with Enter, so I'm working out how to make the rows keyboard-accessible with tabindex and aria-expanded.

I'm settling how a row expands: one detail row open at a time, toggled by a click or by Enter/Space on the row itself, while clicks on the symbol link are left alone. I'm also keeping the list to 50 rows at a time with a "Show 50 more" button, and planning to highlight search terms in the first line and the expanded text after escaping them.

I'm settling the highlight helper: it splits the raw text on the search words first and escapes each piece afterwards, so matches inside HTML entities can't break. Matches get wrapped in a mark element, and the symbol text gets the same treatment since it's cheap. For the first-line preview, I'm keeping text under 120 characters as it is and only adding an ellipsis when it gets cut.

I'm laying out the Tab 02 expansion details now: the expanded row shows the full paragraph text, its themes, SDGs and targets, affected persons, section and state, with a copy-citation button and a link to the UN document. I'm handling the case where no paragraph number exists, and I'm putting the copy action on the clipboard API with a fallback. Then I'll move on to the Tab 03 check panel and how each check's status gets shown.

I'm checking the tab 03 numbers against each other: the record count against the file's stated total, then the mechanism, body and year breakdowns, which should each sum back to the same figure. Next I'm comparing the type breakdown with the headline total, and then the chart's theme counts against a second, independent count over the filtered set, reading the values the chart actually holds.

I'm moving the chart and table to one shared theme computation that runs on every render, so the tab 03 check can compare the stored chart values against a second independent count over the filtered records. Destroying the chart only happens when tab 01 is rebuilt.

I'm wiring up the tab 03 checks: a headline record count against the file's stated total, then the mechanism, body and year partitions. Next I'm writing the link check, where each doc URL should start with the UN docs address and end with its symbol after decoding, and listing the first ten failures with a count. Then the paragraph-number share per mechanism, expecting 100% for UPR and a warning otherwise, and finally the states found among UPR records.

I'm deciding to list the failing links and the states found directly in each check line, showing up to eight items and a count of any remainder, rather than tucking them behind extra toggles.

I'm wrapping up the Tab 03 checks with the status marks, using a dark green for passes and red for failures, and I'm laying out the Tab 04 method notes, a CSV download, and copy-summary buttons, with the CSV's header lines prefixed by "#".

I'm deciding what goes into the CSV columns, settling on the visible fields plus the full text, themes, SDGs, targets, affected persons and section, and I'm leaning toward including the first line as well. I'll write the file with a byte-order mark so Excel reads the characters correctly.

I'm writing the CSV export with quoted fields, a byte-order mark, and comment lines at the top, then a download and a copy-summary button. Next I'm setting the header and footer, with the source link and the record count.

I'm setting the page layout as a left filter rail beside the main column, stacking the two on narrow screens, and hiding the rail on the check and method tabs. For the year filter, I'm using a from and to select over the years present in the file, swapping them if they cross, and only treating the filter as active when either end moves off the full range.

I'm setting the keyword filter so each search word has to appear in either the text or the symbol, and I'm building the year and SDG selects from the values actually present in the file, with the goal numbers compared as numbers.

I'm adding the chart title and source line under each figure, then working out the mechanism tiles from the file's distinct mechanisms, with records, documents, latest year and share of the filtered set. I'll format numbers with thousands separators.

I'm laying out the timeline next: the years run from the earliest to the latest in the filtered set, with one stacked series per mechanism present in the file so the legend stays stable. Empty results get a plain "No records match" message and zeroed tiles, and the chart gets a click handler that adds a theme as a filter and a pointer cursor on hover.

I'm setting up the value labels as an inline Chart.js plugin that draws each bar's formatted count just to the right of its end, and I'm limiting it to this chart. The chart will also need some right-side padding so the labels aren't clipped.

I'm setting the chart's x-axis to hidden with a minimum of zero and a maximum about ten percent above the largest value, so the bar labels fit at the ends. On the y-axis I'm wrapping long theme names onto multiple lines and turning off auto-skipping so every theme gets a label. Then I'll destroy any existing chart before the container is rebuilt on each render.

I'm laying out the tabs as a proper tablist with roving focus and arrow-key navigation, rendering each tab's content into one shared panel. Each tab heading gets a short serif italic question beneath it. Since the page is small, re-rendering on every keystroke is fine, but I still need to keep the search input from losing focus when the panel is rebuilt.

I'm settling on the search box and the results area as separate pieces, so that typing in the keyword field only refreshes the table and doesn't rebuild the input and drop focus. The shell for this tab gets built once when the tab opens, and later updates just fill the results region.

I'm laying out the rail so its filter sections are built once at startup, with only the select options, chips and counts refreshed on each update. The keyword inputs stay put, and I'll only copy the stored keyword back into them when they aren't focused, so typing doesn't get interrupted.

I'm settling the rail layout: each filter section gets a collapsible header with an expanded state, one section open at a time, and the rail hides on the check and method tabs. I'll keep "Clear all" available everywhere and make the active filters readable as a plain list for the CSV export.

I'm sorting the table by date, newest first, then by body, then by paragraph number, with a single flip for the date column so it can show oldest first, and the caption says which order is active.

I'm sizing the results table so it fits beside the rail at laptop width, with the symbol column wrapping long references and the first-line column taking the remaining space. Each row also gets an expandable detail line showing a large red count on one side and the text on the other.

I'm settling the state filter so it matches a record when its list of States includes the selected one, with an extra option for records where no State was found. For the UPR tile I'm working out a top-ten list of States by recommendation count, where a record naming several States counts toward each of them.

I'm laying out the UPR state list as a ranked block under the tile row, shown only when UPR records are present and at least one State was found. Tab 01 gets its records, documents and years tiles on one row and the mechanism tiles on a second. For the CSS I'm using the paper palette, a red focus ring, and muted text colour where the contrast check was still being worked out.

I'm writing a shared escape helper, then a `runChecks` function that compares record counts against the file's stated total and tallies each field's values.

I'm checking the file's own totals next: the type breakdown should add up to the filtered record count, and I'm comparing each field's values against the total, so I'm also doing a separate pass over the chart and table against the same numbers. Paragraph coverage per mechanism is worth a check too, flagging UPR as a warning if it falls short of full coverage. The last check looks at the states.

I'm writing the consistency checks now: each bar's value gets recounted with a plain loop and compared against the top-theme figures, and failures show in red with both numbers side by side. The question is whether the rows under the chart match what was actually drawn, since the table isn't in the DOM while the other tab is showing, so I'm storing the values written at render time to compare against.

I'm adding the duplicate-text check next: counting how many texts appear more than once, and how many extra records that makes, then flagging it as a warning.

Still writing the sample logic...

I'm wiring up the sample tally and the card list, where each row can be expanded and given a fit, doesn't-fit or unsure verdict.

I'm setting up event delegation on the document, with each control tagged by a data-act attribute so one handler covers accordions, chips, the states toggle, the sort, row expansion, citation copying, the sample draw and verdicts, and the CSV and summary exports.

I'm adding a copy action for citations: a small "Copied" note appears next to the button for two seconds, and if the clipboard API is blocked in the sandbox I fall back to a temporary textarea with execCommand, showing a manual-select message if that also fails. The summary copy will live on the fourth tab.

Still wiring the rail's result counts and export labels, and the Ten States heading will use the country name, falling back to a generic label when it's missing.

I'm working out the rail's selects: the mechanism choice drops the body if it no longer belongs, body options come from the chosen mechanism sorted by count, and the type select lists types with counts. The state select only appears in heading 02 when some states were found. Since the rail gets rebuilt on each update, I need to make sure the select being used doesn't lose focus when its options change.

Now I'm wrapping up the main update cycle: filtering the records, recalculating the derived counts and top themes, then re-rendering the rail and the active tab. I'm also adding a debounce so the keyword field doesn't trigger a rebuild on every keystroke.

I'm working through the remaining pieces of the HTML skeleton now, starting with the head and the document structure.

I'm writing the HTML skeleton now: a header with the label, title and source line, a row of tabs, and a two-column layout with the filter rail on the side.

I'm adding a keyword field, and the chip and theme buttons are handled by delegated clicks. Next I'm checking the rail's accordion and state toggle wiring.

Still writing the tab 01 overview markup...

I'm building the tab 01 overview now: a records tile with the filtered count, a breakdown by type, and a note on how the figures are computed. Next come the mechanism tiles, one per mechanism in the file, each showing its record count, distinct documents, latest year and share of the filtered set.

I'm laying out the tab 01 figure section: a chart with a table beneath it when records match, otherwise a plain "no records" message, and I'll draw the charts right after the markup is in place.

I'm adding a short summary label to the records table, then a search input and a table container, with a note that the search is a literal match, not a synonym search.

I'm sketching out the detail panel for each record: the paragraph number, the symbol, date, body and type, and the full text with the search terms highlighted.

I'm wiring the record rows so clicking one opens a detail box with its paragraph number, metadata, full text and labels, plus a copy-citation action and a link to the UN document.

I'm wiring up the CSV export, and the summary text will start with the country name and the filter values.

I'm writing the summary export next: a header line with the country and source, the filter values, the matching count against the total, and a breakdown by mechanism. After that comes the top ten themes with their counts and shares, and a note that the dates come from the documents and the labels are the UN's own.

Now I'm working through the filter state and the rail's accordion and state toggle, opening one section at a time.

I'm filtering each record against the active criteria: mechanism, body, type, state, year range, SDG, and themes, with every keyword word needing to match.

I'm writing the keyword-matching step: each word has to appear in the record's searchable text, and an unset year range skips records with no year rather than dropping them. Then I'm wiring the chip list, with each active filter getting its own removal action that rebuilds the view.

I'm writing the extractStates helper now, which pulls state names out of the parenthetical group at the end of a paragraph's text, skipping anything with commas or that's too long.

Still writing the summary export...

Still writing the highlight helper, which escapes the text and wraps any keyword matches in marks.

Still writing the CSS now, setting up the color variables and layout styles for the page.

Still writing the stylesheet: a two-column grid that collapses to one column on narrow screens, with tab buttons in small uppercase monospace and a red underline on the active one.

I'm settling on 16px for the body and tables, since the first line of each record has enough room to wrap without trouble.

I'm settling the method notes for the fourth tab: every figure is a plain loop over the records, with no estimates or model calls, and the filters combine by exact match with an inclusive year range.

I'm checking the data source block next: the source link, and a licence line noting the file doesn't state one, so the user should check OHCHR's terms. I'm also setting up the sample verdicts so each record can be marked as fit, no, or unsure, and I'm writing the check markup with its pass, fail, warning and note states.

Still writing the sample check section, setting up the seed input and its buttons as static markup so they stay put when the cards re-render.

Still writing the tab 03 panel: a seed field and draw buttons kept as static markup so they survive re-renders, with the sample cards rebuilt beneath them.

Still writing the chart helpers: a line-wrapping function that breaks long labels into lines no wider than a set character count.

Still writing the chart code: the bar chart's labels are wrapped to fit, and clicking a bar will add that theme as a filter.

Still writing the rail's render function: it sets the matching count and the progress bar, then rebuilds the chips and syncs the inputs.

Still writing the select builders: a helper that turns a list into options with an "all" entry, with the body list rebuilt whenever the mechanism changes.

Next I'm filling the state list from the whole file, plus the SDG options labelled with their names, then wiring the init step that sets up each select and hides the state filter when there are no states.

Still writing the sample draw function: it seeds a shuffle of the filtered records, takes the first ten, and resets the verdicts.

I'm writing the draw function, which seeds a shuffle of the filtered records and takes the first ten, then resets the verdicts.

Still writing the timeline tab: stacking each year's counts by mechanism, with the x-axis covering every year in the range.

Still writing the tab 01 summary cards: a count of the records, the unique documents, the year span, and a tile for each mechanism.

Still writing the tab 02 table: each row gets its date, body, and type, with the newest records shown first and the caption giving the count.

Writing the table headers now, with the date column sorted newest first.

