I'm sketching out a full HTML app of around 1500 lines, aiming for care without bloat. The layout will be a header over a grid with a filter rail beside the main area, plus four numbered tabs. The rail will hold a keyword search, mechanism, body and type filters with a state option, and year and SDG filters, and I'm tallying how many clickable controls there are against a rough target of about seven at once.

Now I'm working out the app's state model: a set of filters covering keyword, mechanism, body, type, state, year range, SDG and a list of theme chips that combine together. I'm also settling how records get sorted, with date descending as the default and a header click that reverses the order, and planning to keep the rail and tab-two keyword inputs synced to the same state.

Now I'm laying out the tabs: a tile row with totals, a Chart.js bar chart that filters on click, a table, and a stacked bar, plus a link that opens the states list in place. Mechanism tiles will cover every mechanism in the file, showing filtered values. The type and other filters become compact selects in heading 02.

For the random checks tab, I'm drawing ten items from the filtered set with a seeded shuffle, showing each as a one-line card that expands on click, with verdicts stored per card and tallied at the end. The symbol link sits outside the toggle button so the two don't conflict.

Now I'm wiring up the random checks panel: it draws ten records from the filtered set with a seeded shuffle, lets the user redraw or reuse a seed, and clears the sample whenever a filter changes. Then I'm adding a link check that verifies each document URL points to the UN docs site and ends with the symbol, reporting the first ten failures. Finally I'm planning a second, independent pass over the data to confirm the chart and table counts match.

I'm getting the CSV export ready, with a header row of fields like date, body, mechanism, symbol, and text, and comment lines marked with a hash. I'll trigger the download through a temporary link, and the copy action will try the clipboard API first with a textarea fallback. For the expandable table rows, I'm making each row focusable so Enter or Space toggles it, and clicks on links inside it won't also toggle the row.

Now I'm settling the highlight helper: it escapes the text, splits on the search words so matches get wrapped, and escapes each remaining piece. Then I'm thinking through the timeline, which spans the filtered set's year range with stacked mechanism colours and grey for anything unrecognised, while the Chart.js instances get destroyed and rebuilt on every render with animation switched off.

Now I'm settling how the state labels get extracted from the UPR records: I match the pattern, then test each parenthesised group, keeping only those without commas and under 60 characters, with the outer parentheses stripped.

Now I'm settling how the state labels come out of the UPR records: each parenthesised group must be free of commas and under 60 characters to count, and if any group fails, that record gets no states at all. In the table, UPR rows show their states joined with semicolons, or a muted "State not found" when there are none, and other rows show a dash. The UPR tile gets a "see the States" link that opens a small hidden panel under the tiles with the top ten states for the current filter.

Next I'm wiring the SDG filter as a select built from the goals present, falling back to "SDG n" when names are missing, and I'm making the year selects swap automatically if the start ends up after the end. Each active filter, including a non-default year range, gets its own removable chip, and the accordion opens only one section at a time. Body options will follow the chosen mechanism, and changing the mechanism clears the body choice.

Now I'm settling the header and the notes: the title takes the country name, the source links out, and each element gets a short "how computed" line. For the summary copy I'm drafting plain text with the headline numbers and filter description, and the method note on tab 04 will run five or six sentences. Next is the sort key for paragraph numbers, read as number pairs with records lacking one placed last, and a comparator that orders by date descending, then body, paragraph and index, reversed when ascending.

Now I'm writing the checks panel as a list of labelled comparisons, covering record counts, partition totals by mechanism, body and year, and the type breakdown. The chart-versus-table check recomputes the top themes with a separate loop and compares them against the main calculation. I'm also verifying the document links and the paragraph-number coverage, and starting on a duplicate and gap check on the record ids and texts.

Now I'm building the checks panel as a list of labelled comparisons, with a warning or failure mark on each. Failing items like state-less records will sit in a collapsible list, and the chart-versus-table check runs on the filtered set. I'm starting on the HTML and CSS next, with a visible focus ring and a stacked layout below 800px.

I'm setting the chart bars to a deep red and putting the theme labels on the vertical axis, shortened to 40 characters where they run long. A small custom plugin will print each count at the end of its bar, and clicking a bar will add that theme as a filter. The theme names in the table below will be buttons too, so the same action is available from the keyboard.

Next I'm setting up the keyword search on tab 02, with its own input and a hint, and both search boxes will stay in sync after a short debounce. The filter selects get built once, while the body list is rebuilt whenever the mechanism changes, with counts shown for each option. Each mechanism tile will carry its colour, record and document counts, latest year, and share of the filtered set.

Now I'm writing the code for the data setup: it pulls the records from the workshop data, adds an index and paragraph key to each, and flags the UPR records so their state labels can be read out. The keyword matching lowercases the text and symbol and checks that every search word appears in it. Then I'm setting up the filter function and the defaults for the year range, guarding against an empty record set.

Next I'm laying out the timeline chart, with a message that replaces it when nothing matches, and a sampling panel where a seeded random draw of ten records can be checked.

Next I'm writing out the CSV export, with quoted fields and lists joined by pipes, plus a comment header, and then the full file. I'm aiming for about 600 lines.

