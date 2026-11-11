I'm working through the request to build the app. The spec calls for a single complete HTML document in one html block, starting with the doctype, with at most three short sentences before it and nothing after. The file has to stay under about 1,500 lines, so I'll keep the inline CSS and JavaScript compact while still making it complete and functional.

I'm settling on the data layout now: the `WORKSHOP_DATA.gc` object carries a title, source, count, and records, and each record has an id, symbol, paragraph, committee, year, titles, a doc URL, text, and cited articles. The spec's `source_url` isn't in that shape, so I'll link the source only when that field exists and otherwise show it as plain text rather than inventing a URL. I'm also adding the Chart.js MIT credit line, since the library is preloaded and the credit does no harm.

Now I'm laying out the page structure: a header with the title and checks indicator, a left filter rail beside the main tabbed content, and a footer. The rail hides on the Draft tab, and the rail itself will hold the filter controls, the live match count, the search box with its examples dropdown, and the active filter chips.

I'm working out the committee names next: each code like CAT, CCPR, or CEDAW gets its full name shown beside a checkbox, with the hit count in brackets. The filter section also gets all/none controls and the year range inputs.

I'm mapping the committee codes to their full names, pulling codes from both the committee field and the symbols via a regex, and falling back to the raw code when a name isn't known. The Subcommittee on Prevention of Torture gets its own entry for CAT-OP.

Working out the committee codes next, I'm matching them from the symbols with a regex and making sure "CAT/OP" is recognised as its own code so it doesn't get counted as plain CAT.

I'm now matching committee codes from each record's symbols, treating "CAT/OP" as its own code and making sure plain CAT doesn't pick it up, and I'm checking whether a symbol names more than one committee to flag joint documents.

I'm working out how to tell which committees a record belongs to: the codes in its symbol, plus its committee field. A joint document carries more than one code in its symbol, so I'll flag it when the symbol holds two or more distinct codes, and I'll show both badges for those records.

I'm checking how to count joint records: a record with two committees adds to both bars, so the bar total runs above the hit count by the number of extra committee links.

I'm settling how the filter counts behave: the bars need to add up to the hits plus the extra committee credits from joint records, so I'll check that the sum equals the total committee links across the hits. The committee counts in brackets will reflect the current search and the year and document filters, but ignore the committee filter itself so the list stays usable.

I'm settling how the bracketed counts add up: with every committee ticked, each hit is counted once per committee it belongs to, so the bars should total the hits plus the extra credits from joint records.

I'm settling the bracketed counts so they describe only the search, year, and document filters, leaving out the committee filter itself. The per-committee counts should then add up to the total committee links across those hits, which means I'm comparing that sum against the joint records' extra credits instead of just the hit total.

Now I'm settling the matching engine, starting with a normalisation step that strips footnote markers and swaps curly quotes and the various dashes for plain ASCII equivalents.

I'm settling the normalisation step for the matching engine: footnote markers get stripped out, curly quotes and the various dashes become plain ASCII, and whitespace collapses to single spaces before lowercasing. Removing the markers entirely means a phrase can run across a footnote, so "state[[fn:1]]'s" reads as "state's".

I'm now checking how the footnote markers sit against neighbouring words, since a marker placed between "All." and "By" would change whether the phrase matches the stored text.

I'm writing the tokenizer for the query language now: whitespace gets skipped, quoted text becomes a phrase (with an error if the closing quote is missing), and parentheses are recognised as their own tokens. Words will be read as the runs of characters that aren't whitespace or parentheses.

I'm now handling the tokenizer's edge cases: a leading hyphen followed by a non-space character becomes a NOT token, and exact capitalised AND, OR, and NOT are treated as operators while lowercase words stay plain text, so hyphenated terms like "ill-treatment" remain intact.

I'm settling how a query term matches: word-like terms get boundaries that keep them from matching inside longer words, and a trailing star turns the term into a prefix match.

I'm working out how the query's quote and apostrophe forms should match, since the query is already normalised to straight characters but the highlight pass runs over the original text, so the pattern needs to accept the curly variants too.

I'm working out how the highlight pattern should treat the gap between phrase words and the case-insensitive flag, since the shown text has its footnote markers already removed.

I'm writing the highlight step so it matches on the raw displayed text and escapes each piece separately, which keeps straight and curly quote forms from being broken by HTML escaping. Each match gets wrapped in a mark element, and the surrounding text is escaped as usual.

I'm checking how the highlight pass handles terms: only positive terms count, so anything under a NOT gets skipped.

I'm checking the highlight step against the 700-character cut: if a match only appears after the cut, the full paragraph has to be available, so I'll count the marks on the complete shown text rather than the truncated snippet.

I'm adding a tweak so that a row auto-expands when its first highlighted match falls past the 700-character cut, which keeps every hit showing at least one mark.

I'm deciding on the row layout now: each hit becomes an article with a heading, the committee badges, a symbol link and pinpoint with the year, the paragraph text, the amber notes, and a grey line noting the removed footnote marks with a button to show the stored text.

I'm laying out each hit as an article with its heading, committee badges, symbol link and pinpoint, and the text, with the highlighted paragraph and amber notes below. I'm working out how a click on the row should open it in place, with the copy and draft buttons only appearing on the open row.

I'm laying out the context links now: the "previous" and "next" paragraphs come from the same title, and the preamble only gets a "next" link. To find them I'll index the records by title and paragraph number, then look up the neighbouring paragraphs.

I'm sorting out the pinpoint labels next: "para. N" for numbered paragraphs, "preamble" for paragraph 0, and a subparagraph label when the text opens with a lettered marker. The context lookup will work from the same title, using a per-title index that keeps the first record at each paragraph number.

I'm checking the pinpoint labels: paragraph 0 becomes "preamble", a lettered opening gives a subparagraph label, and everything else reads as a numbered paragraph.

Working out how the leading paragraph number gets pulled from the text, using the text with footnote markers removed and leading whitespace trimmed.

I'm working out the citation format next, starting with the symbol prefix before the pinpoint.

I'm checking how the shared-symbol citation is built: committee, then the short document name, then the symbol in parentheses, then the pinpoint. The document name is taken from the title before the first colon or " on", and whether a symbol counts as shared depends on whether it holds more than one distinct title, which gets worked out at load.

Next I'm settling how the draft gets saved: each item stores its quotation, citation, symbol, pinpoint, committee, short title, year, both text versions, and the document link, kept in local storage with a guard around it.

I'm laying out how the draft is handled: each saved item keeps its quotation, citation, and pinpoint, and copying all or downloading as text joins them with blank lines. For the CSV export I'm double-quoting every field, doubling any inner quotes, and adding a UTF-8 byte-order mark, with the columns citation, symbol, paragraph, pinpoint, committee and short title.

I'm laying out the checks panel now, with the totals check counting the rendered rows against the number of hits.

I'm checking the totals now: the sorted list should match the hit count with no row repeated, and the bar chart should sum to the same total across the hits.

I'm checking that the highlight step marks at least one match in every hit, and I'm working out how to count hits that have no marks in their full shown text. Since the search runs over several thousand records, I'm weighing whether computing marks for every hit on each query is fast enough. I'm also planning a check for hits that match only through the normalised forms, so the list can flag them as matched but not highlighted.

I'm checking the strict highlight option next, so that quote, apostrophe and dash characters match only their literal forms. That lets me count hits that only match through the curly or dash variants, and I'm weighing whether to count hits where all the positive terms hit that way.

I'm working out how a strict match should treat hits where the term only appears in curly or dash forms, and I'm settling on counting hits where no term matches in its straight form. For queries without quotes, apostrophes or hyphens, that check doesn't apply, and for hyphenated terms like "ill-treatment" I'm still sorting out how the dash variants should count.

I'm weighing whether the numbering checks should count as failures or just warnings, since a mismatch between the leading number and the paragraph isn't necessarily an error. I'm leaning toward showing them as informational counts with a few examples, and only marking the check as failed if something structural is wrong.

Now I'm settling how the numbering check reports its results: the leading number against the paragraph in each hit, with the mismatches flagged amber in the rows.

I'm settling the numbering check: a leading number that differs from the paragraph gets flagged amber in the rows, so that check counts as failed only when those mismatches appear among the hits. Next I'm planning the mark check, which splits each stored text at the footnote markers, confirms the count matches, and reinserts the markers in order to recover the original text exactly.

I'm wrapping up the checks: after the duplicate-id and totals checks, the highlight check will confirm each hit has a mark, and the numbering check will flag paragraphs whose leading number doesn't match. I'm also planning a known-quirks summary on the first tab, covering paragraph-zero records, shared symbols, joint documents, duplicate pinpoints and lettered sub-paragraphs, computed at load, with the header dot turning red if any check fails.

I'm laying out the load-time data check, confirming the stated record count matches the number of records loaded. Then I'm settling the idle checks: data count, query understood, totals, chart total, highlight, normalisation, numbering, marks and draft, nine lines in all, with the header showing how many pass.

Still setting up the chart: a horizontal bar chart with committees on the axis, sorted by count, where clicking a bar selects that committee. I'm adding a small inline plugin to print each value at the end of its bar, and I'm starting to set the grid and tick styling.

I'm configuring the chart's axes and bar spacing, with the grid kept light and the tick count capped. Next I'm making sure the chart refreshes on every filter change and copes with its tab being hidden at first.

I'm setting up the chart's ranking and empty-state handling, and I'm weighing whether to show every committee in the data, zeros included, or only those with hits.

I'm settling the filters now: committee checkboxes that default to all, with all and none buttons, and a joint General Comments record that keeps showing both badges, with a note under the chart that joint records count under both committees. The year range runs from and to inputs preset to the data's min and max, and I'm planning a short message for when from is later than to.

I'm choosing the document key for the select: symbol plus title, so two documents that share a short title stay distinct, with the short title as the visible label and each document grouped under its committee.

I'm sorting out the document dropdown next: each option keyed by symbol and title so duplicates stay distinct, labelled by short title and grouped under its committee. Then I'm covering the chips that show active committee, year and document filters and can each be cleared, and noting that the query only applies on Search or Enter.

I'm now working out how the search echo describes each part of the query, so a phrase in quotes reads as "the phrase" and a word with a trailing star reads as a prefix match.

I'm working out how the search echo should phrase the query tree: a single word or phrase reads as its term, and a combined query joins its parts with "and" or "or", with the grouping shown by parentheses.

I'm working out the describer for the search echo: a single term reads as its word or phrase, a negated term reads as "no" plus that term, and the recursion builds up the sentence from there.

I'm settling how the search echo describes the query tree: a NOT node reads as "not containing" its child, and AND and OR nodes join their two sides with "and" or "or".

I'm working out how the search echo should phrase a negated term nested inside an AND, so a leaf reads as "the word X" and a NOT reads as "not containing" its child. The describer will build the sentence from those pieces, so an AND with a NOT on one side comes out as "containing the phrase ... and not containing the word ...".

I'm settling how the search echo handles nesting: a composite child under a different operator gets wrapped in parentheses, and a top-level negation reads as "Paragraphs not containing" its term.

I'm settling the parser grammar next: an expression is a chain of AND-joined terms separated by OR, a NOT prefix binds to an atom, and two adjacent atoms with no operator between them read as an implicit AND. I'm also planning the parse error messages for unbalanced parentheses.

I'm writing the tokenizer now: it skips whitespace, emits parentheses as their own tokens, and reads quoted phrases using any of the curly or straight quote marks, throwing an error if a quote is never closed or the phrase is empty.

Writing the tokenizer loop: quoted phrases get pulled out as a single token, a leading minus becomes a NOT token, and everything else is split on whitespace and parentheses into words or the AND, OR and NOT keywords.

I'm getting the tokenizer to read the raw query before lowercasing, so that AND, OR and NOT stay recognisable as operators rather than being treated as ordinary words, and only then normalising each term's text.

I'm writing the tokenizer so that it reads the raw query first, keeping AND, OR and NOT recognisable as operators, and only then normalising the text of each word and phrase.

Now I'm writing the recursive descent parser, with the OR level calling into the AND level for each side and building the tree as it goes.

Still writing the parser's atom handling...

Still writing the parser's error handling...

Still writing the search parser's regex helpers...

Still writing the search matcher's pattern builder...

I'm putting together the phrase-matching pattern now, joining each word with whitespace and handling the gap rules for footnote markers.

I'm writing the search matcher's pattern builder now, with word and phrase regexes that treat letters and digits as word boundaries, and I'm caching each compiled term so it isn't rebuilt on every match.

Still working out how the search matcher compiles each term, with a case-insensitive regex that treats letters and digits as word boundaries, and caching the compiled patterns on the tree nodes.

I'm working out the hit test for each record: a record counts when it passes the committee, year and document filters and matches the query, and I'm checking that every query term has at least one letter or number so a bare star doesn't match everything.

Still working out the search matching: the sort order will be year descending, then title, then paragraph ascending, and the query-match results get computed once per query change rather than on every filter change.

Still working out how the matches get ordered: I'm settling on document order by title and then paragraph, and most matches first by counting the positive term hits in each record's normalised text.

I'm laying out the pagination and row rendering now: the list starts at 25 rows with a button to show 25 more, and only the open row keeps its details expanded.

Still writing the row markup...

Still writing the row markup and the action buttons...

I'm working out how long paragraphs get cut for display: anything up to 700 characters shows whole, and longer ones are trimmed back to a word boundary with a "Show the full paragraph" button that gives the word count.

I'm adding the expanded-paragraph toggle and the footnote-marks line, shown only when marks were removed, along with the amber notes for a leading number that doesn't match the paragraph and for lettered sub-paragraphs.

Now I'm sorting out the duplicate-pinpoint check, and the joint General Comment note, plus the case where a leading number doesn't match the paragraph and the quotation has to drop it.

Still working out how the draft stores each quotation and its citation, with the copied text minus any leading number.

Now I'm writing the copy helper: it tries the clipboard, announces what was copied, and if the clipboard isn't available it falls back to a textarea the user can select from.

I'm checking that the textarea fallback is in place for when the clipboard isn't available. I'm also planning an aria-live message near the top of the content that shows the exact string each copy sends, plus a live count. The draft will be saved in localStorage under its own key and validated when it loads, and the draft tab label will show its item count. Finally, I'm adding arrow, Home and End key handling to the tabs, using the standard tablist, tab and tabpanel roles.

I'm laying out the rail and the tabs now: four tabs with arrow, Home and End keys, the rail hidden on the Draft tab, and a grid with a 300px column beside the main panel that stacks on narrow screens. I'm also weighing whether the filter heading should start closed, since the committee checkboxes would then be hidden until opened.

I'm settling the rail's search box: the examples list opens when the box is focused while empty or on arrow down, hides once the user types, and hides on blur after a short delay so clicking an example still registers.

I'm settling the rail's examples list now: it appears when the search box is empty and focused, or on arrow down, and it disappears once the user types or leaves the box, with mousedown kept from stealing focus so clicks still register. I'm also listing the syntax reminders in plain words, covering spaces or AND for joining, OR, NOT or a leading minus, exact phrases in double quotes, parentheses for grouping, a trailing star for word endings, and operators written in capitals.

I'm adding the example buttons under the search box, each one filling the input and running the search, and I'm noting the hint line about whole words, quote and dash handling, and footnote marks. I'm also planning a paragraph-level error message under the box, announced with an alert role.

I'm checking how the summary line and the header counts should read: the number of paragraphs, the distinct General Comment titles, the committees, and the year span, with the source linked at the end.

Still preparing the per-record data: I'm precomputing the display text, the footnote-mark count and a normalised version of each paragraph for matching.

Still writing the per-record fields: each one gets a leading paragraph number and letter, a list of committee codes, a flag for joint documents, a document key, and the shared-symbol lookup.

Still writing the text normaliser: it strips footnote marks, unifies the curly and straight quote and apostrophe characters, and lower-cases everything for matching.

Still working out the per-record normalisation: I'm stripping footnote marks from the display text, counting how many marks each paragraph had, and building the matching version with the quotes, dashes and case unified.

I'm checking the totals next: the sorted list should have as many rows as there are hits, with no row listed twice, so I'll compare the lengths and look for duplicate ids.

I'm checking that the chart's bar values add up to the expected total across the hits, with the joint extras shown separately. Then I'm checking that the committee bracket counts over the base set sum to the same total, since that's the figure the checkboxes should reconcile to.

I'm checking the highlight logic next: for each hit, I'll count the marks in the shown text, and any hit with zero marks gets flagged, unless the query has only NOT terms, in which case the check doesn't apply.

I'm checking the highlight logic: for each hit, I'll count the marks in the shown text, and flag any hit with none, unless the query is NOT-only.

I'm checking the normalisation: for queries with straight quotes or hyphens, I'll count hits where the positive terms only match in the curly or dash forms, using a strict matcher that doesn't unify them.

I'm checking the numbering next: for hits with a leading paragraph number, I'll compare it with the stored paragraph, and I'll flag any hits that share a pinpoint with another record under the same title. I'm also counting the lettered sub-items, though those aren't treated as failures.

I'm moving on to the data checks: each draft item should match its record's text, and I'll count any item that isn't in the file. Then I'm adding a static check that the record count matches the expected total and that every record has a symbol and text.

I'm defining the status for each check as pass, fail or not applicable, so the header can show a red count when anything fails. I'm also marking the Draft tab with a red dot whenever a check fails.

I'm laying out how each check reports: a green "pass", a red "check failed", or a grey "not needed", with the header tallying the results. After that comes a short list of quirks in the file, covering preamble records, symbols shared by several documents, joint documents, and pinpoints that appear twice.

I'm noting the leading-number mismatches and the lettered sub-paragraphs as counted items, along with the line-break paragraphs and footnote marks, all computed from the data rather than hardcoded. I'm also planning a short "known quirks" section on the Draft tab, plus a method note and the Chart.js credit in the footer.

I'm laying out the rest of the Overview tab: the chart, the small table, the hint and the "How this is computed" note, plus the joint-document note. Then I'm setting up the Search tab with a summary line of hits, committees and year span, a select, the hint, a results list with a "Show 25 more" button, and a paging note.

I'm finishing the search tab: the summary line falls back to "no search words" when the query is empty, and the results still list every paragraph that passes the filters, paged. I'm also keeping track of which row is open and whether each one shows the previous or next context, and the draft checks for duplicates before adding anything. The clear-all button is what's left, resetting the query, the committee ticks, the year range and the document field.

I'm wiring up the filter controls next: the document field, the committee checkboxes with their all and none buttons, and the chart click that narrows the ticks to one committee. The committee labels will show their hit counts in brackets only once a search is applied.

I'm sorting the results by most matches, so I'll count how often each positive term appears in each hit's normalised text, caching the counts per search. The highlight regexes are built per term and are cheap enough for the 25 visible rows.

Writing the regex compiler...

Writing the regex helper that escapes each character and expands wildcards and punctuation variants...

Writing the regex escape helper, making sure special characters are escaped correctly for unicode mode.

Writing the regex escape helper...

Writing the phrase-matching helper next, so that a multi-word query can span line breaks and footnote markers in the shown text...

Still working out the regex helpers: the word and phrase matchers, with the show-mode punctuation variants and the lookbehind boundaries.

Writing the regex helpers for normal matching and show-mode punctuation variants next...

Writing the regex helpers for phrase and word matching now, so every query term goes through one function that works for single words and multi-word phrases alike.

Writing the term-matching regex builder now, with a separate compiled form for the normalised test, the global count, and the show-mode highlight.

Writing the search helpers now, turning each query term into a regex that handles punctuation variants in the displayed text.

I'm now setting up the search state: the parsed query tree, which terms are positive, and the Uint8Array that marks each record as matching or not. After that I'll filter the matching records by year range and document, then keep only those with a ticked committee.

I'm wiring the hits to recompute from the cached query match and the committee ticks, with the committee counts taken over the base set. Then I'll re-render the rail, chart, results, and checks together, since the work per update stays small. The results sort by match count, which I'll cache per query.

Now I'm sorting the results by title and paragraph number, then turning to the Overview chart, which ranks committees by hit count with ties broken by name.

Writing the Chart.js setup now: a horizontal bar chart with no legend, a dotted-monospace y-axis of committee codes, and a click handler that narrows the committee ticks to whichever bar was clicked.

Setting up the chart's value labels next, drawing each count just past the end of its bar.

Still writing the chart's value labels, drawing each count just past the end of its bar.

I'm wiring the chart's data: the labels, the values, and an upper bound on the x-axis so the value labels fit. The canvas height will scale with the number of committees, with a fallback message if Chart.js is missing, while the table beside it always stays visible.

Writing the committee name lookup next, mapping each code like CRC or CEDAW to its full title for the table and chart labels.

I'm mapping out how to pick the committee list from the records, the codes including CAT-OP, and checking that the symbol-to-code mapping handles that case.

Still writing the rendering code for the results list and the row-toggle handler, using a single delegated click listener on the results container.

I'm defining the row rendering: each visible result gets its index, whether it's open, and whether its stored or expanded state is set, with the body varying by those flags.

Now I'm deciding how the row body gets cut: long paragraphs get trimmed to about 700 characters unless the match sits beyond that point, in which case the full text shows.

Working out how to handle the long-paragraph cut: if the first match falls before the 700-character cut but would be split by it, I'll expand the row so the whole match shows.

Still working on the visible-text cut: if the first match ends past the 700-character limit, I'll extend the cut so the whole match stays visible, then back up to a word boundary.

I'm working out how to cut long paragraphs for display: if the first match would fall inside the 700-character cut, I'll extend the cut to just past that match, then stop at the next space so no word is split. I'll also store the first match's end position so the cut can use it.

Writing the row markup now: each row gets the symbol as a link when there's a document URL, plus badges for its committee codes and a note when it's a joint document.

Writing the row actions and the context box for the open row now, with citation, quotation, and draft buttons plus previous and next context links.

Now I'm deciding how to handle the paragraph context links: the previous and next paragraphs of the same title, shown inline in grey with their own pinpoint, and noting when a neighbour doesn't exist. I'll index all records by title and paragraph number so lookups stay quick, then wire up the copy actions for citation, quotation, and adding to the draft.

Writing the citation helper now: a shared record gets the committee, a short document name taken from the title, and the symbol in brackets before the pinpoint, while a non-shared record just uses the symbol and pinpoint.

I'm working out how to quote each paragraph: if the paragraph starts with its own number and that number matches the pinpoint, I'll strip the leading number, then wrap the trimmed text in curly quotes.

Still writing the download helper, building a Blob from the content and handing it off as a file.

Still working on the download helper: wrapping the content in a Blob, attaching a temporary link, and revoking the object URL after a second.

I'm setting up the local storage handling for the draft: a single key, with an in-memory fallback if the browser refuses storage, and a hint that says which mode is active. The draft list stays in memory either way, and I still need to add the checks section after this.

Now I'm laying out the filter rail, with a closed heading for committee, years, and document, and an empty search box whose examples stay hidden until it's used.

I'm wiring the search box's behavior now: the examples list hides once someone types, reappears when the box is focused while empty, and the arrow keys move through the examples, with Escape returning focus to the input. Clicking an example fills the box and runs the search. Then I'll add the syntax list and the four tabs, each tab tied to its panel.

Still writing the overview panel, laying out the coverage chart and its matching table with a short note on how the counts are made.

Now I'm laying out the results panel: a summary line, an order selector with three options, a short note that the page only retrieves and never edits, and a list that grows by 25 at a time.

I'm laying out the sort options for the results list, with newest first as the default, then document order and most matches first. The summary line will reflect whichever order is picked. Next I'm planning the Draft tab with its quotation list and copy and download buttons, then the Checks panel and the footer.

Laying out the page's header, the next block is the top bar with the title and a live message region, and I'm also adding a fallback copy box for when copying fails.

Still writing styles...

Still writing styles...

Still writing styles...

Still writing styles...

Still writing styles...

Still writing styles...

Still writing the lookup tables and the per-record setup now.

Still writing the record lookups and the per-record setup.

Still writing the record lookups and the per-record setup.

Still writing the record lookups and the per-record setup.

Still writing the record lookups and the per-record setup.

Still working on the record setup: I'm flagging each hit that shares a pinpoint with another record from the same title, plus any whose leading paragraph number doesn't match its pinpoint, and checking which committee codes each symbol carries.

Still working on the counts for the record checks: how many preambles there are, which symbols are shared across titles, how many joint records, and how many paragraphs share a pinpoint or have a mismatched leading number.

Still working on the query tokenizer, scanning the input character by character and handling quoted phrases and parentheses.

Still writing the query parser, handling quoted phrases, the NOT prefix, and the AND, OR, and parenthesis tokens.

Still writing the query parser's atom handling, checking that each word or phrase has at least one letter or digit.

Still writing the query pattern builder, turning each word into a regex that treats wildcards and punctuation variants correctly.

Still writing the query pattern builder, turning each word into a regex that handles wildcards and the different apostrophe and dash forms.

Still writing the regex for phrases, building the spacing between words so that a space in the query can match any run of whitespace or punctuation variant.

Still writing the regex for phrases, handling the spacing between words so a query space matches any run of whitespace or footnote marker.

Still writing the query compiler, building the regex for each term in its normal, highlight, and show forms.

Still writing the query evaluator and the positive-term collector.

Still working on the describe helper, deciding how to label term nodes: phrases get curly quotes, and words with a wildcard get a short note that they match any ending.

Next I'm settling how the describe helper labels a word that ends in a wildcard, and how it wraps nested groups in parentheses when it builds the summary of the query.

Still working on the describe helper, wrapping composite sub-expressions in parentheses so the echoed query stays unambiguous, and deciding how the top-level prefix reads when the whole query is a NOT.

Now I'm finishing the search flow: the query gets tokenized and parsed into a tree, and if that fails, the error is kept and the hit list stays empty.

Now I'm finishing the search flow: the filter state is set up with a ticked-items set, and the echo line gets worked out for the query.

Still writing the filter logic, collecting the paragraphs that pass the query, year range, and document filters, and checking each one's committee codes against the ticked set.

Still writing the committee counts, deciding how to tally each committee's matches across the filtered results.

I'm working out the committee bar counts now: each bracketed number counts a paragraph under every committee it carries, so joint records appear under both, even if only one box is ticked. I still need to check that the bracket totals reconcile with the hit totals.

Working through the committee tallies now: a joint record counts under each of its committees, so I'm treating any paragraph with more than one code as a joint hit, and I'll check that the bracketed totals line up with the hit count.

Still writing the rail's summary numbers, showing the matching paragraph count against the total and the joint-hit tally.

Still writing the rail's markup: the big match count with a live region, the filter chips for committees, years and document, and the committee list with its bracketed counts.

Still writing the rail's committee list: each row gets a checkbox and a count, built once and updated in place so clicking a box doesn't lose focus.

Still writing the summary line, showing how many paragraphs match against the total, the committee count, and the year span.

Still writing the sorting for the results: by document and paragraph order, or by how many matches each one has, falling back to recency.

Still working on the results ordering: the matches are sorted by document and paragraph order, or by how many hits each one has, with recency as the fallback.

Still writing the row renderer: rendering the visible slice of results, toggling the "show more" button, and working out the summary text and the empty-state message.

Still writing the highlight helper, combining every positive term into one regex and walking the text match by match so the matched spans get marked.

Still writing the highlight helper's loop, skipping empty matches and wrapping each matched span in a mark element while escaping the text around it.

Still writing the row renderer, building each paragraph's markup with its stored or shown text and the highlight marks.

Still writing the highlight cutoff for long paragraphs, picking a point just past the first match so the matched text stays visible.

Still writing the row renderer, working out how long paragraphs get cut at a word boundary past the first match and how the word count and notes are built.

Still writing the row renderer, deciding how each row's stored-versus-shown text toggle and footnote-mark note get built.

I'm writing the row markup now: each article gets a heading button with its badges and short title, plus a meta line below it.

Still writing the row markup, adding the link, pin, and year line under each heading, then the notes and the highlighted paragraph text.

Still writing the open-row actions: copy citation, copy quotation, and add to draft, plus the previous/next context links and a small state object tracking which context direction each row is showing.

Still writing the context toggle: each row remembers whether the previous or next paragraph was asked for, and the neighbour's text is looked up by its pinpoint and shown beneath the actions.

Still writing the copy helper, with a clipboard call that falls back if it fails.

Still writing the copy helper's last branches, and the add-to-draft action that follows.

Still writing the add-to-draft helper: each row becomes a draft item carrying its quotation, citation and pinpoint, and duplicates are skipped.

Still writing the draft view, rendering each item's quotation with a remove button, and flagging any item whose stored text no longer matches the file.

Still writing the draft list's remove buttons and the copy-all and download actions, plus the note on where the draft is kept.

Still writing the update checks: the query-parse check passes when there's no error and reports how many terms were understood, while a parse error fails it. The totals check compares the listed rows against the hit count, and also confirms the committee bracket counts add up to the base-set codes.

Still writing the verification checks: the static ones at load, the dynamic ones after each update, with each reporting pass, fail, or not needed.

Still writing the verification checks: the mark-consistency check compares each hit's stored text with its shown text and footnote marks, and the draft check flags any item whose stored text has changed.

Still writing the tab handling: the selector sets aria-selected and tabindex on each tab, hides the other panels, and hides the rail on the draft tab, with arrow keys moving between tabs.

Still wiring up the controls: the tick on each committee box and the all/none buttons, the year range inputs, the document dropdown, and a clear-all that resets everything.

Still wiring up the clear-all and chip removal, the Search button and form submit, and building the highlight regex from the positive terms.

Checking the normalisation case next: if the raw query has straight quotes or hyphens, I'll count the hits where none of the positive terms match the displayed text literally.

Still writing the verification checks: the normalisation check looks at whether a query with straight quotes or hyphens matched hits that only contain curly quotes or dashes, and counts those as informational passes. The highlight check counts hits that matched but got no mark, still listing them as matched and shown.

Next I'm writing the row-level note: if a hit has a query but no highlight marks in its shown text, the row gets a "matched, not highlighted" note, which I can count while building each row. Then I'm working out the overall check list, nine checks plus two static data checks. The numbering check fails when a hit's leading number doesn't match its paragraph or when pinpoints repeat, and I'm also listing the lettered hits as informational detail.

Now I'm finishing the verification checks: the numbering check fails when a hit's leading number doesn't match its paragraph or pinpoints repeat, and lettered sub-paragraphs get listed as informational detail.

Still writing the CSS: the base colours, typography, focus outline, and the top header styling.

Still writing the stylesheet: the header and status dot, the two-column shell that drops its rail on the draft tab, and the tab bar.

Still writing the stylesheet: the header and tab styling, the big serif figures, and the result rows with their borders and spacing.

Still writing the stylesheet: the button resets for result rows and the badge styling, plus the highlight colour for matched text.

Still writing the stylesheet: the filter headings, committee checkboxes, and table rules, with the caption and number cells aligned right.

Still writing the stylesheet: the chart layout that splits into two columns, the examples list, and the default button styling.

Still writing the stylesheet's header, the tab bar, and the result rows with their badges and highlight colour.

Still writing the stylesheet: the header and status dot, then the rail and main column shell.

Still writing the stylesheet's filter headings, committee checkboxes, and the examples list beneath the search box.

Still writing the HTML body: the year inputs and document dropdown, then the tab bar, the message line, and the start of the first panel.

Still writing the HTML body: the header and rail, then the tab bar, the feedback box, and the first panel markup.

Still writing the tab panel markup: a figure heading, the committee chart with its hint line, and the matching table beside it.

Still writing the stylesheet's button defaults and the link-style buttons, then the primary button colour.

Still writing the panel markup: the draft heading and list, then the copy button.

Still writing the page footer, with its mono line and credit.

Still writing the JavaScript setup: the data record list and the small helpers for lookups and escaping.

Still writing the JavaScript: the record list, plus helpers for escaping, number formatting, and the match patterns.

Still writing the record loader: the shown text with its footnote marks, and the per-symbol and per-pinpoint lookup maps.

Still wiring up the record loader: deriving the stored and shown text for each record, counting its footnote marks, and picking out its leading number and any lettered label.

Still wiring the record normalization: each entry gets a shown text with its footnote marks removed, a mark count, a normalized copy for matching, and a leading number and lettered label pulled from the start.

Still wiring up the state object and the tree that holds the applied filters.

Still wiring up the state object and the helpers it depends on, and noting that the year bounds fall back to zero when there are no records.

Still writing the parser: the OR level handles the lowest-precedence split, then the AND level chains together the terms that sit between OR and closing brackets.

Still writing the parser's AND level: it consumes an explicit AND and requires a word after it, then chains each following term into a combined node.

Still writing the parser's atom level: a plain word or quoted phrase becomes a term, provided it has at least one letter or figure, and an opening bracket starts a grouped sub-expression.

Still writing the parser's atom level: the bracketed group is parsed as a nested expression that must close with a matching parenthesis, and stray brackets or misplaced operators get a clear error.

Now I'm writing the search runner, which takes the parsed tree and checks each record against it.

Still writing the search runner: it resets the state, tokenizes and parses the query, then builds the highlight pattern from the positive terms.

Still writing the search runner: it resets the state and tokenizes the query, parses it, and checks each record against the tree.

Still writing the search helpers: the expression is turned into a readable echo line, with a special case for searches that only exclude words.

Now I'm writing the describe helper, which turns each node of the search tree into a readable phrase, using quotes for phrases and wrapping compound parts in parentheses.

Still writing the search helpers: the describe function turns each node of the tree into a readable phrase, with AND and OR children wrapped in parentheses.

Still writing the render code: the rail's big number and its matching-paragraph label, then the committee chips and the rest of the rail.

Still wiring up the render code: the committee counts, the year-range error, and the query error line, then the overview chart and table rows.

Still writing the overview: the tab labels with the draft count and the check-failure dot, then sorting the committees by hit count for the chart and table.

Still writing the overview chart: the table rows get the committee code, name, and paragraph count, then the chart's labels and values update along with its axis maximum.

Still writing the chart setup: the bar options for the committee chart, and the click handler that opens a committee's paragraphs.

Still writing the chart options: the bar axis setup, the value labels, and the click handler that opens a committee's paragraphs.

Still writing the chart options: the value-label plugin, the tooltip setting, and the gridline spacing, then the fallback text inside the canvas.

Still writing the Chart.js value labels: a plugin that draws each bar's count just past its end.

Still writing the table rendering: the rows are built from the ordered list, and the page cap sets how many show at once.

Still writing the table rows: an empty-state message for no matches, then the first page of rows, the show-more button, and the summary and sort notes.

Still writing the summary text: it returns an error message when the query fails, and otherwise counts the matching committees and the year span.

Still writing the summary text: it returns an error when the query fails, otherwise it counts the matching paragraphs, committees, and year span, with a different wording when there are no search words.

Still writing the sorting helper: the default order is newest first, with the document and paragraph order as ties.

Still writing the row markup: each row gets its paragraph's committee, title, and year, then the text with matched words highlighted.

Still writing the row markup: a function that builds each row's HTML, checking whether the paragraph is stored, expanded, or open, and locating the first highlighted match in the text.

Still writing the row markup: each row's text is cut at the first highlighted match, so long paragraphs stay short unless expanded.

Still writing the highlight helper: it collects the start and end positions of each match in the text, skipping any empty matches.

Still writing the highlight helper: the match spans become marked text, and the note list starts to note whether the row's matches are visible.

Still writing the row markup: each row's text is cut at its first highlighted match, and a note line is started to say whether a stored footnote-mark count applies.

