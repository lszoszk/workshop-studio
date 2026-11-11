I'm planning a full standalone HTML app as a single document, keeping it compact but complete, with the header details for Kenya and the left-rail filters starting to take shape.

I'm now working through the rail's details: the Clear all control, the big number, the share bar, and the chips, with filter headings 01 to 03 that stay closed until opened, one at a time. On the Method & export tab, the rail narrows to just the number, bar, and chips.

I'm checking the tab-03 rail, which keeps only the number, bar, and chips, and I'm counting the clickable controls on the Overview view. Tabs, headings, Clear all, the States link, and the Every check button add up to nine, which is over my target of about seven. I'm deciding to accept that as approximately fine rather than cutting a required control. Last, I'm noting that the header date comes from the built field and the year range has to be computed from the data.

I'm going to write the chip-based theme filter into the same AND logic, so every active filter narrows the records together. For keyword search I'll split the query on whitespace and require each word to match the record's text or symbol, case-insensitively. The state filter lists states with counts and applies only to UPR records, and I'm sketching a trailing-parenthesis regex to pull the state names out of those entries.

I'm working out how to pull state names from the trailing parenthesized groups of UPR records, and how to split those groups apart. Records with nothing usable get marked "State not found". Last, I'm settling the sort order: date descending, then body, then numeric paragraph number, with missing numbers placed at the end.

I'm laying out the records table with its columns, highlighting keyword matches, and showing 50 more rows at a time. Clicking a row, or pressing Enter on it, expands a detail row beneath, and clicking the Date header reverses the order. Last, I'm setting up the horizontal Chart.js bars.

I'm checking the chart's click handling, which reads the clicked bar's index, and I'm working out how to tally the top ten themes by count with ties sorted alphabetically. Next I'm setting up the stacked year-by-mechanism bars, and last I'm planning a set of pass/fail checks that compare record totals and partition sums.

I'm checking the link check next, comparing each record's decoded document URL against its symbol, case-insensitively. I'm also noting that the sample URL points to a different symbol, so the check has to be written to match the Kenya file's URLs.

I'm working through the validation checks now: confirming the numbers of paragraph numbers per mechanism, flagging UPR records that yield no state names, and testing for duplicate IDs and text. I also want the year range and the mechanism tiles, including a states list behind the UPR tile's link, with counts over the currently filtered UPR records.

I'm weighing whether the first tile should count every record in the file or only the filtered set, since the spec seems to pull both ways. I'll show the file-wide total with its per-type breakdown, and keep the share against the filtered count.

Still writing the page markup and header...

Still writing the page markup, with the header, the rail, and the tab bar in place.

Now I'm wiring up the rail's filter groups, with the keyword box in section 01, the mechanism, body, type, and state selects in 02, and the year range and SDG select in 03, all set up as accordion sections.

Still writing the rail's accordion, with the tab-03 view hiding those headings, and I'm wiring up keyboard arrows for the tab bar.

I'm writing the match function, where each active filter has to hold for a record: keyword words all found in its text, plus the mechanism, body, type, state, year range, SDG, and theme checks.

Still wiring up the mechanism and body selects, with the body options limited to the chosen mechanism and their counts. Next I'm setting the type, year, and SDG options from what the file contains.

Still writing the rendering logic, with the filtered set driving the rail count, the bar, the chips, and the active tab. Next I'm building the theme tally, grouping records by theme with their counts and year spans, and sorting by count with ties in alphabetical order.

Still writing the theme tally logic, with the top ten themes feeding the chart and clicking a bar adding that theme as a filter. Next I'm planning the chips, the check that compares chart counts with the table, and the year timeline.

Still working out the records table, with the sort order and paging, and the detail rows that open beneath each entry.

Still writing the record sort, comparing dates first and then body, paragraph number, and original order, with the direction reversed when the Date header is clicked.

Still writing the record rows: each one gets its date, body, linked symbol, and paragraph number, with the first line highlighting keyword matches through an escaped helper.

Still writing the record detail rows, covering the paragraph number, full text, themes, SDG labels and targets, affected persons, and a copy-citation button.

I'm finishing the detail rows: the Open UN document link, and a copy-citation button that copies the symbol with the paragraph number when there is one, or the symbol alone with a note when there isn't. I'm also wiring up the clipboard with a fallback, and then the "Show 50 more" paging.

I'm finishing the export section: a Method & export tab with a CSV download built from escaped columns, and a button that copies a summary with the headline numbers and top themes.

I'm now setting up the header metadata, showing the source link, record count, document count, and year span. Then I'm planning the empty-state messages for when no records match, and the overview's caption and accessible theme table, before listing the validation checks.

I'm writing the validation checks now, comparing record counts, partition sums, and type totals against the file's own figures. Next I'm setting up a chart-versus-table check on the filtered set, confirming the top ten theme counts match the recomputed values.

I'm checking the validation list next: the link check that compares each decoded document URL against its symbol, the paragraph-number share per mechanism with UPR expected at full coverage, and the states check for UPR records that yield no state names. I'm also working out how to handle duplicate IDs and duplicate text.

Still writing the data prep, with each record's paragraph number pulled from the start of its text and the states extracted for the UPR records.

I'm setting up the data prep: each record gets its paragraph number from the start of its text and, for UPR records, the state names pulled from the trailing parentheses, deduplicated per record. I'm also building a lowercase search string from the symbol and text, and copying each record's fields onto a new object so the originals stay intact.

Still writing the data prep, with the state list deduplicated per record and a fixed mechanism order, plus the year range and SDG names pulled from the file.

Still writing the data prep, with each record's paragraph number and state list worked out, and the check list and CSV export laid out.

Still writing the page's base styles, with the CSS variables, the body font, and the header layout.

Still writing the page's rail and tab styles, with the focus ring and the tab bar layout.

Still writing the table and tile styles, with the mark highlight and a responsive single-column layout for narrow screens.

Still writing the data prep and state extraction, with the paragraph regex and trailing-parenthesis matcher feeding the record objects.

Still writing the record prep, pulling each paragraph number and the states out of the text.

Still writing the record prep, pulling each paragraph number and the state names out of the text, with the states deduplicated per record.

Still writing the record prep, deriving each record's year range, document count, and mechanism list for the header and filters.

Still writing the filter predicate, with the keyword match, mechanism, and body checks in place, and the type check next.

I'm writing the record filter predicate, checking keyword matches, mechanism, body, type, state, year range, SDG goal, and selected themes in turn. Next I'm setting up the chips list and the render step.

Still writing the rail controls, with the number, share bar, and chip list in place, and the year, mechanism, and SDG selects filled from the file's own values.

Still writing the table sort, with paging at fifty rows and the expanded detail set cleared whenever a filter changes.

Still writing the table rendering, with the sort applied and the caption showing how many rows match.

Still writing the table rows, with the caption counting matches and the state cell and link markup for each record.

Still writing the detail view, with the paragraph number line, full text, and a copy-citation button for each record.

Still writing the copy-citation handler, with the clipboard call and a fallback that uses a hidden textarea.

Still writing the overview tile, with the record count and the per-type totals next to the filtered count.

Still writing the overview tiles, with the file-wide document count and year span beside the filtered figures.

Still writing the overview tiles, now the per-mechanism cards with their counts, document totals, and latest year, plus the States toggle for the UPR card.

Still writing the overview's themes chart, with the bar labels and a plugin that draws each count at the end of its bar.

Still writing the chart setup, with the bar colors, the end-of-bar count labels, and a click handler that adds a clicked theme to the filters.

Still writing the chart code, with the timeline's stacked bars per mechanism across the year range and a message for when nothing matches.

I'm laying out the overview's data table beneath the themes chart, with the top ten themes, record counts, percentages of the filtered set, and each theme's year span. I'm also adding a source line and a note that records can carry several themes, and I'm planning the checks panel to recompute its values each time it renders.

Now I'm writing the checks, starting with a record-count check that compares the number of loaded records against the document's stated total.

Still writing the checks, with the record count, the mechanism, body, and year partitions, and the type breakdown each summing back to the total.

Still writing the checks, with the paragraph numbers, the states found in UPR records, the distinct ID count, and a duplicate-text tally each reported as its own check.

Still writing the checks, with the duplicate-text tally, and then the three not-labelled counts for themes, SDGs, and affected persons, each shown as its own line in the checks panel.

Still writing the CSV export, with the header comment lines for country, source, build date, and active filters, and the row count next.

Still writing the CSV export, with the Blob download and the file name built from the country slug.

Still writing the chip helpers, with the keyword, mechanism, body, state, year range, SDG, and theme labels each set to remove their own filter.

Still writing the chip sync and select population, with the keyword inputs and the filter dropdowns kept in step with the filter state.

Still writing the accordion and select setup, with the year range swapping when the bounds are reversed and the SDG options listing each goal with its name.

Still writing the share tiles for each mechanism, with each share computed against the filtered total.

Now I'm laying out the rest of the page: the three tabs, the overview with its timeline figure, and each panel's short question-style subtitle.

Still writing the rail's chip rendering, with a remove button for each active filter.

Still writing the chip list, with each active filter labelled and wired to clear its own value.

Still writing the chip removal logic, with a rule that drops a mechanism filter without touching the body filter, and the sync step that resets the controls from the filter state.

Still writing the render functions, with the overview and table rendering to follow.

Still writing the overview tiles, with the all-records count, the per-type totals, and the filtered document figures next.

Still writing the overview tiles, with the all-records count, the per-type totals, and the filtered figures for records and documents, followed by the year span and its distinct-year count.

Still writing the overview tiles, with the mechanism cards next, each showing its count, document total, and latest year.

Still writing the overview's state breakdown, counting Universal Periodic Review recommendations by state and listing the top ten.

Still writing the chart code: the themes bar chart gets its data from the filtered records, with an empty-state message when nothing matches, and the timeline counts records per year for each mechanism.

Still writing the chart code, with the theme and timeline charts initialised empty and the Chart.js colours set for each mechanism.

Still writing the tab handling, with the keyboard arrows moving between tabs and the panel shown for each selected tab.

Still writing the tab and accordion code, with the open panel tracked so only one section is expanded at a time and all start closed.

Still writing the search and debounce handling, with the keyword box and the search field each updating the filter after a short pause and keeping the other field in step without disturbing the one being typed in.

Still writing the chart code and the tab handling, with the rendered tables and the accordion setup lined up next.

Still writing the page's helpers, covering text truncation, highlighting search terms, and CSV escaping, plus the footer and a copy-summary button for the status note.

