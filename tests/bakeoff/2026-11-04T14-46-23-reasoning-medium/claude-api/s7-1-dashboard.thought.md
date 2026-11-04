I'm planning the layout for a single-file app under about 1500 lines: a header, a left rail, a main area with tabs, and a footer. The filter state will track keyword, mechanism, body, type, state, year range, SDG, and theme selections from bar clicks, and only one filter heading will be open at a time. I'm also checking that no view presents more than about seven clickable items, counting the four tabs and three filter headings.

Now I'm checking the view limits and sorting out the data prep: parsing each record's paragraph number, extracting the state from the UPR text, and making the filter logic count within the chosen mechanism.

Now I'm laying out the tab 01 overview: summary tiles for totals, types, documents and years, plus per-mechanism tiles, a UPR link that toggles the state list in place, and a clickable bar chart with a stacked by-year chart beside it. Since Chart.js has no label plugin here, I'm adding a small inline one to draw values at the bar ends, and rebuilding the charts on each render with animation off.

I'm laying out the table columns for the table, with sorting that defaults to date descending and flips direction when the Date header is clicked, while the other keys keep their order as ties.

Now I'm wiring up the table rows, so each one can expand on click or Enter, with the symbol link not triggering the expand, and the full text shown below. I'm highlighting the search words in the first line and the expanded text, and adding a copy-citation button that falls back if the clipboard API isn't available. Next up is the checks tab, which mostly runs over the whole file.

I'm sorting out how the checks tab draws its sample: a seed box, a "Draw with this seed" button, and a "Check 10 at random" button that becomes "Draw again" once cards are showing, so there are only three buttons to manage.

Now I'm setting up the sample draw: the seed box and a seeded shuffle over the currently filtered records, with the three buttons toggling between "Check 10 at random" and "Draw again." Each card will show one line per record and open to reveal the full text, its themes, and three verdict buttons, with verdicts tallied and reset on each new draw.

Now I'm checking the link validity: each document URL needs to start with the UN docs domain and end with its symbol. I'm also tallying paragraph numbers per mechanism and flagging UPR coverage below 100%, then listing which UPR records are missing a state.

Now I'm wiring up the export tab: a method note, a CSV download with comment lines at the top and the record fields in order, and a copy-summary button, all via a temporary link for the download.

Next I'm handling the year range selects, which default to the full span and are swapped if the user sets the bounds backwards, plus the SDG select, built from the goals present in the data with a fallback if the name list is missing. Active filters will show as removable chips, the rail count will read the filtered total against the full file with a proportional bar, and the three filter headings will open one at a time, hidden entirely on the checks and export tabs. I'm also planning a separate theme-counting approach for the checks, so it doesn't share logic with the chart.

Now I'm working out the tab 01 chart axes: the by-year stacked chart will span the filtered records' year range, with a fallback message when nothing matches. Each mechanism gets a series even when its count is zero, a legend stays on, and numbers are formatted with en-GB thousands separators. The header will link the source, show record and document counts, the year span, and the build date, with a note that records are dated by their document.

Now I'm finishing the overview chart: the title takes the country name, the footer links the data source with the record count, and the bar colours are set to a red at 80% opacity. Clicking a bar will add that theme to the filters if it isn't already there, and the chart gets a small inline plugin to draw values at the bar ends, with extra right padding and long theme labels left unskipped at a 12px font.

Now I'm working out how the chart handles empty results and the source line under each figure. For the UPR tile, I'm adding a toggle that lists the States with counts from the current filter, and the state select will draw from every State in the UPR records, with records lacking a State marked as such. In the table, the State column shows the joined States for UPR rows, a "State not found" label where none exists, and a dash for everything else.

Now I'm settling the table's filter controls: the mechanism, body, type and state selects in the second panel, plus the from, to and SDG selects in the third. The keyword box is debounced at 300ms and kept in sync with the search box on the other tab. I'm noting that sorting over about 2,264 records is fine. Dates sort as ISO strings, newest first by default, and the caption reads either "newest first" or "oldest first", or "No records match the filters" when empty. Each expanded row will show the large red paragraph number, the highlighted full text, and a list of labels for themes and SDGs.

Now I'm writing out the expanded row details and the citation and document buttons, with the expanded state kept across re-renders. I'm also checking the chart's bar values against a fresh recount of the table rows, and making sure no theme total goes above the filtered count.

Now I'm setting up the render flow: each change recomputes the filtered records, and the top-theme data gets stored for both the chart and the checks tab even while tab 01 is hidden. The chart itself only gets drawn when that tab is active, so it isn't rendered at zero size.

Now I'm writing the overview data: a function computes the top themes for the filtered records, and the chart draws from it. The check tab will recount the same way, comparing the chart's actual values against a fresh pass over the records.

Now I'm defining the first-line helper for records, which will leave short text as it is and cut longer text at a set length.

Still writing the record helpers and search logic...

Now I'm laying out the mechanism tiles, one per mechanism, each showing its record count, distinct document count, latest year and share of the filtered set. The UPR tile gets an extra button to show the States.

Writing the record helpers and text highlighting for the search, plus the seeded sampling for the checks.

Now I'm getting the regex patterns in place for the paragraph numbers and the trailing parenthetical groups, and I'm watching for backtracking on the longer texts.

Now I'm wiring the filter state and the rail: the mechanism, body, type, state and year selects update one shared filter object, and the body and state options are refreshed from the counts as the mechanism changes. Each change then calls the same update routine, and the active filters appear as removable chips.

Now I'm writing the check section: the record count gets compared against the file's stated total, and each grouping is checked to make sure its counts add back up to the full set.

Now I'm checking the totals: the filtered record count against the file's stated total, and each grouping by type, mechanism and year, so the parts add back up. Missing values are counted separately so they show up as failures rather than disappearing. The chart and table counts get compared the same way, and then I'll check the source links, the paragraph shares per mechanism, the State coverage, and any duplicates or gaps.

Now I'm finishing the layout code: the timeline chart gets one dataset per mechanism with stacked bars, a bottom legend and a canvas label, with a note and source line under it. The table beneath it lists themes with their counts, percentages and year ranges, and the rows are handled through event delegation so each one can expand.

Next I'm setting up the date column header as a sortable button with its aria-sort state, and each expanded row will carry a copy button keyed to the record's index. The copy handler writes the text to the clipboard, falling back if that fails, and briefly switches the button label to "Copied ✓" before reverting it.

