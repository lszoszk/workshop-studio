I'm sketching out a single HTML file of roughly 1500 lines and planning it step by step. The main pieces are loading the records, a query parser, matching on normalized text, highlighting, filters for committee, year and document, and tabs starting with Overview and Paragraphs.

I'm setting out the remaining pieces: the Check & method tab, the Chart.js bar, copy and draft with a localStorage fallback, checks, and known quirks. I also want to keep the left rail limited to about seven clickables per view, and I'm mapping the ten committee codes to their full names, with the raw code as a fallback. For symbols like CAT/OP, I need to make sure the parser picks CAT-OP rather than matching CAT alone.

I'm making the parser handle the CAT/OP case by rewriting it to CAT-OP before matching, with that code listed first in the regex so it isn't split into CAT alone. I'm also adding the committee field into each record's set of codes, and treating a record as joint when it has more than one committee.

I'm checking how symbols map to committees: a symbol like CAT/OP gets rewritten to CAT-OP before matching so it isn't read as CAT alone, and the committee field gets folded into each record's set of codes. A record counts as shared when that set holds more than one committee. For the document name, I'm trimming the title at the first colon or at " on", so a General Recommendation title keeps just its number.

I'm working out how to label each record's pinpoint: paragraph 0 becomes "preamble", a lettered start like "(b)" becomes "subpara. (b)", and anything else becomes "para. N". I'm still deciding whether to check the lettered label first or the preamble case, since sub-paragraphs are numbered too.

I'm working out the exact pattern for the lettered and numbered labels, and whether a leading number in the text matches the paragraph number. The check runs against the text with the marks removed and trimmed. Where the leading number and the paragraph number disagree, the record gets flagged, and where they agree, the leading number gets dropped from the quotation copy.

I'm settling how the copied quotation gets built: the shown text with the marks removed, wrapped in curly quotes and followed by the citation. Drafts will be deduplicated by id and kept in localStorage with an in-memory fallback, storing the copied text, the stored text, and the citation for each item.

I'm working on the text normalisation step now: removing the footnote marks and collapsing the whitespace, and deciding how to handle curly quotes and dashes so matching isn't thrown off.

I'm settling how the query parser reads its input: quoted phrases in straight or curly quotes are taken whole, and an unclosed quote becomes an error. Parentheses are handled as separate tokens, and anything else is read as a word that stops at whitespace, a parenthesis, or a quote.

I'm settling the query parser's handling of a leading minus: a "-" at the start of a token followed by a term becomes a NOT, while a hyphen inside a word like "non-State" stays part of the word. I'm also weighing how to treat a lone "-" and how AND, OR and NOT are recognised when they appear as whole words, along with trailing wildcards.

I'm settling the regex boundaries for matching, so a term only counts when it isn't part of a longer word. For a trailing wildcard I'm allowing any run of letters or digits after the stem, using a Unicode-aware class rather than plain `\w` so accented letters are covered.

I'm writing out the grammar for the query parser, starting with a top-level expression that is an OR of AND-groups, and I'm wrapping up how phrases become whitespace-tolerant patterns.

I'm defining the query grammar as OR over AND-groups, with NOT binding tightest and parentheses for grouping. I'm also planning the error messages for unbalanced parentheses and for operators left dangling at the start or end, and I'm working out how to echo each parsed term back in plain English.

I'm working out how the query grammar's output gets described back in plain English, with a single word becoming "the word X", a trailing-star term becoming "words beginning with X", and each operator wrapped in its own phrasing. For nested OR groups I'm adding parentheses, and for NOT I'm settling on "not" followed by the description of the negated item.

I'm settling the evaluation step: each term's regex will be compiled once, non-global with the Unicode flag, so repeated tests don't carry state between paragraphs. Since a NOT-only query has no positive term to highlight anything, I'm falling back to a plain description of that case instead of a generic echo.

I'm working out how the highlight pattern handles the cleaned and as-stored views, since the marks only appear in the stored one. Removing a mark can leave a double space where it sat between two words, so the collapse step needs to handle that.

I'm now setting how the highlight pattern treats punctuation and spacing in each term, so the match tolerates curly quotes, various dashes, and runs of whitespace between phrase words.

I'm checking the highlight pattern for the as-stored view: the gap between phrase words has to tolerate footnote marks, and I'm worried a footnote sitting right between two words could leave the match without even one whitespace character to anchor on.

I'm carrying the highlight step forward: rendering escapes the HTML piece by piece, wrapping each match in a mark, and truncating long paragraphs at a word boundary near 700 characters before highlighting.

I'm adding a note for the case where the match sits past the 700-character cut, so the user is told to expand the paragraph. Then I'm setting the results list to show 25 rows at a time, each as an article with a heading, and working out what a click on a row should do.

I'm now deciding that clicking the row text itself toggles it too, on top of the heading button, while leaving links and selected text alone.

I'm settling how each row opens and closes: clicking the heading button or the row body toggles it, unless the click lands on a link, a button, or the context controls, or the user has text selected. I'm keeping sets for which rows are open, which show the full paragraph, and which show the stored text, and re-rendering just the one changed row so focus can stay put.

I'm settling how each paragraph finds its neighbours for context: I'll group records by title and sort them by paragraph, then take the entry just before and just after in that list. That handles duplicate paragraph numbers without needing a separate lookup map.

I'm planning the results list's copy actions: the citation and quotation buttons will use the clipboard API, falling back to a text box with a manual copy button if that fails. A live-region message will confirm what was copied, shown in a fixed status area at the bottom.

I'm weighing whether the closing dismiss control and the transient box are worth the extra clickable element, and I'm settling on a fallback textarea with a "Select and copy" button inside the same box whenever the clipboard write is refused.

I'm setting up the filter state: which committees are ticked, the year range, and the selected document, with the document dropdown grouped by committee and labelled with each title's short name. Active filters will show as removable chips, and "Clear all" will reset both the filters and the query.

I'm deciding how the committee checkboxes should show counts. If the hit counts only cover ticked committees, the bar chart would shrink to match the filter and a click on a bar couldn't bring the others back, so I'm leaning toward counting hits across all committees instead.

I'm weighing whether the bar chart should count hits across every committee or only the ticked ones, since the sums in my checks depend on that choice. Counting only ticked committees would hide the others, so a click on a bar could never bring them back, and I'm still deciding how a joint record should be split between committees.

I'm settling how the bar chart counts hits: each committee's bar will count the base records (matching the query and year and document filters) that belong to it, ticked or not. Unticked committees stay visible in grey and sit outside the sum, which is then checked against hits plus the joint extras.

I'm making the bar chart use Chart.js horizontal bars, with the value labels drawn by a small inline plugin since the datalabels plugin isn't available. If Chart.js isn't loaded, I'll fall back to just the table, and I'm turning off animations and keeping gridlines light.

I'm setting the bar chart's bar thickness and layout, sizing its container to the number of committees. I'll update the chart in place on filter changes and only draw it while the overview tab is showing, since a hidden canvas has no size. Then I'm building the state object, with the parsed query, the base set of matches, the per-committee hits, and the sorted counts.

I'm now settling the sort orders for the results list: newest first by year, then a document order by title and paragraph, and a most-matches option that counts occurrences in each paragraph.

I'm settling how the sort orders get computed: the match-count order only gets evaluated when it's selected, and the result is cached per search. Ties fall back to newest first.

The sort hint text under the dropdown will change to match whichever order is active. The summary line will show how many of the 7,304 paragraphs match, how many committees and years the hits cover, and a note when no search words were entered.

I'm now laying out the example list: a listbox under the search box that appears when the field is focused and empty, with the syntax notes and three clickable examples. Arrow keys will move through the options, Enter or a click will fill in and run the example, and Escape or typing will close it. I'm handling blur so the list doesn't vanish when focus moves into it.

I'm making the header show the committee label, title, and a source line that links out when the source is a URL or a source_url is present, and falls back to plain text otherwise. The rail hides on the draft tab, and the layout becomes a grid with a 300px rail that stacks on narrow screens.

I'm laying out the header's checks indicator: it will show a green dot with the passing count, or a red dot with the failing count, and that status also goes onto the tab. The checks themselves will be recomputed on each run, starting with whether the highlight marks put back into the stored text reproduce it exactly.

I'm checking the highlight marks by stripping them out with a regex to get the cleaned text, then reinserting the marks at their original positions to see whether the stored text comes back exactly.

I'm working out how to split the cleaned text back into pieces at the mark positions, so a stripping function can record each mark's offset and a rebuild can reinsert them to check the round trip.

I'm writing the consistency checks for the highlight marks: counting the marks against the stored text and confirming that reinserting them reproduces it exactly. I'm also planning a draft check that matches each item against its record, and a totals check that compares the sorted rows with the hits.

I'm now writing the remaining checks: the rendered article count against the visible total when the paragraphs tab has been drawn, and the bracketed committee counts for the ticked boxes, which should add up to the hits plus joint extras. I'm also planning a normalisation check for straight quotes, apostrophes, and hyphens in the raw query.

I'm working out a check for quote and hyphen normalisation: for straight apostrophes or inner hyphens in the positive terms, I want to count the hits that match only through their curly or other variant forms and not the straight spelling as written.

I'm checking that the numbering check flags hits where the leading number doesn't match, and that duplicate pinpoints are caught by title and paragraph, since lettered sub-paragraphs legitimately share a paragraph number.

I'm checking whether two pinpoints appear twice, using the title and paragraph as the key, and I'm weighing whether lettered sub-paragraphs should be included in that key.

I'm weighing whether to exclude preamble paragraphs from the duplicate check, since several preambles in one document would all share the same pinpoint, but I'm leaning toward keeping them in because that would be a genuine duplicate citation.

Now I'm writing the duplicate-pinpoint key as title plus paragraph plus any sub-paragraph letter, so a repeated preamble counts as a real ambiguity while separate lettered lists stay distinct. I'm also setting the row notes: a mismatched leading number, a lettered sub-paragraph, a shared pinpoint, and a joint hit.

I'm working out the known-quirks summary to show at load: a count of paragraph-zero records, symbols that several documents share, joint documents identified by having more than one committee, duplicated pinpoints, mismatched leading numbers, and lettered sub-paragraphs, with a plain-text example for each.

I'm wiring the document filter as a select grouped by committee and sorted by title with numeric-aware ordering, and I'm checking that a document outside the ticked committees simply yields zero hits. For the year inputs I'll clamp values to the bounds on change, reset invalid entries, and handle the case where the start year runs past the end year.

I'm settling the year inputs: each one clamps to its bounds on change, falls back to the bound if it's not a number, and swaps the two values if the start ends up past the end. Then I'm setting up the collapsible filter heading, closed by default, with only one section open at a time. For the page itself I'm laying out four tabs (overview, paragraphs, draft with its count, and check and method), with arrow-key navigation and roving focus.

I'm laying out the page structure: a header, a tab bar, and a two-column layout where the rail sits beside the main panels, with the rail hidden on the draft tab. On load I'll put focus in the search box. Searching will apply the current query and close the syntax list, with the echo line and any error message shown under the input, and a query error will leave the results empty and show up in the checks as a failure.

I'm laying out the search code's regex for footnote marks and checking how they get stripped before the highlight positions are recorded.

Writing the normalisation helper now: it strips the footnote markers, folds curly quotes and dashes to their plain forms, collapses whitespace, and lowercases the result.

I'm writing the record-level computations: a regex for the committee codes, then mapping each record to its cleaned text, its footnote mark count, and a check for a leading paragraph number.

I'm working out how to pull the document name out of each title: taking the text before the first colon or " on ", and falling back to the full title when neither appears. I'm also setting up the committee codes so each record gets its full set, including joint ones.

I'm checking how each citation is built: a shared symbol gets the committee and document name added, while a unique one is just the symbol and the pinpoint. I'm also noting that the document name should be ordered so titles like "General Recommendation No. 29" lead the citation.

I'm settling how each quotation gets built: the text with the leading paragraph number dropped when it matches the paragraph, then wrapped in curly quotes with the citation after it. I'll also mark a leading number as matching only when it equals the paragraph field.

I'm settling the lookup by id, falling back to the index when an id is missing, and I'm deciding that the title-to-records index should keep file order within each title rather than sorting by paragraph number, since the lettered sub-paragraphs don't follow a clean paragraph sequence.

I'm working out the search parser and how a query is split into terms before the matching begins.

I'm breaking the query lexer into its first pass, where whitespace is skipped and each character is checked in turn.

Still writing the query tokenizer...

Still writing the query tokenizer...

Still writing the query parser...

Still writing the query parser...

I'm writing the parser for the query now, where each term gets a normalised form and a flag for whether it has a trailing wildcard.

Building the regex for the search terms now, with word-boundary guards so a match has to start and end on a whole word, and escaping the regex-special characters before the term is inserted.

Still writing the query tokenizer...

Still writing the search highlight regex...

Still writing the query tokenizer...

Still writing the search echo helpers...

Next I'm filtering the records with the parsed query, so I'm computing the base set and checking each paragraph against the term tree.

Next I'm wiring the regex and parser for the search query, which turns each parsed term into a case-insensitive pattern with word boundaries.

I'm building the results rail so the committee checkboxes show counts only once a search is active, and those counts come from the base set across all committees. The year filter works independently of the committee ticks. Rather than rebuilding the rail on every change, I'll create it once and update the counts and checked states in place, so keyboard focus in the checkboxes isn't lost.

Still writing the overview chart and table...

Still writing the chart config...

Still writing the row markup...

Still writing the row markup, with the symbol linked to the document URL when one exists and plain text otherwise.

I'm making the truncation helper cut the text at 700 characters, backing up to a whitespace boundary and avoiding splitting a footnote marker, and adding an ellipsis. Long paragraphs also get a toggle to show the full text with a word count, and those buttons only appear for the long ones.

I'm adding the footnote note under each paragraph, showing how many marks were removed and a link to switch views. Then I'll give each open row context toggles for the previous and next paragraph in the same document, with their own pinpoints.

Still writing the draft handling and the action buttons, so each paragraph gets its own copy, add-to-draft, and context controls.

I'm wiring up the draft tab: a list of quotations with citations, a flag where the stored text no longer matches, and a remove control per item. Its toolbar will offer copy-all and download as .txt or .csv, and the draft's items will link their symbols to the document URL.

I'm setting up the draft's copy-all and download handling, so each saved item keeps its quotation, its citation, and the text as copied and as stored. Downloads will go through a temporary link, though the sandbox might block that.

I'm working out how the downloads should behave, with a fallback in case the sandbox blocks them, and I'm adding a hint that points to Copy all if that happens. The CSV export will start with a header row, double-quote every field, and pull each row from the record by its id, falling back to the stored values when the record is gone.

Still writing the checks and the health indicator...

I'm settling how the health checks get computed: the hit-based checks run once in compute() and get cached, while the draft check runs when the draft changes. I'm also weighing the rendered-rows check, which depends on a `renderedCount` value that renderList updates, since it could go stale if the panel isn't re-rendered.

I'm now defining the checks list, starting with whether the query is understood: an empty query passes with a note that every paragraph matching the filters is listed, a parse error fails with its message, and otherwise it passes with the echoed query and term count. Next comes a totals check, which compares the rows across all pages against the hit count.

I'm working through the numbering check next: a hit whose leading number differs from its paragraph will be flagged for the user, and the check will pass as long as those flags are shown on the rows rather than dropping any hits.

I'm working through the remaining checks now: the numbering quirks, the draft check, and an overall pass/fail count. For numbering, I'm listing hits that share a pinpoint with another record of the same title, plus the lettered ones, with a few example citations each. Then I'll write the brief "How this is computed" bullets for the Method tab and the footer credits.

Still writing the page styles, with a muted palette, a highlight color for matches, and a restrained amber for notes.

Still writing the page styles, with a muted palette, a highlight colour for matches, and a restrained amber for notes.

Still writing the HTML skeleton for the header, the tab bar, and the status line...

Still writing the HTML skeleton for the header, the tab bar, and the status line, then the filter rail with its search box.

I'm wiring up the search box and its suggestion list, then the help and echo lines that report the parsed query, and an error line for bad input. After that comes the committee, years, and document facet, collapsed by default, with the main results panel to follow.

I'm laying out the syntax help next: a plain list explaining how spaces, AND, OR, NOT and quotes work, kept separate from the clickable examples so the listbox semantics stay valid.

Still writing the filter options and the facet controls: the committee checkboxes with all/none links, the year range, and the document select.

Still writing the committee names and the data setup, with the code-to-name map and the year range.

I'm writing the compute step: it parses the query, then sets up the state for filtering and sorting the hits.

Still writing the compute step, with the filtered base set and the committee counts.

Still writing the sort order and the comparators, with titles compared in a numeric collator so that later editions sort correctly.

Still writing the sort order and the highlighting, so matched terms stand out in each paragraph.

Still writing the health indicator, which runs its checks through `getChecks()` on each render, so the cached results stay in step with the draft and the marks check.

Still writing the health checks: the marks check will use each record's precomputed count and rebuild the text with the marks stripped out.

Still writing the checks, starting with how the marks are counted and rebuilt from the stored text.

Still writing the checks: the normalisation and highlight checks come next, then the chart totals.

I'm wiring the health check for the chart totals: the bracketed counts shown next to each committee should add up to the hit count plus the joint hits, and I'll read them back from the stored data attributes. The chart data comes from a shared `chartRows()` helper, so I'll sum the ticked rows from that too. Last, I'm listing the numbering issues and tallying how many checks pass or fail for the health indicator.

I'm going over the quirks that get computed at load: the preamble paragraphs, shared symbols across titles, joint hits, duplicate pinpoints, leading-number mismatches, lettered citations, and footnote marks. Each gets a count and one example, and they'll show up as a table with a caption.

I'm now setting up the rail updates: the big match count with its "of 7,304" subline, the aria-live region, and the chips for committee, year range and document filters that appear only when they differ from the defaults.

I'm wiring the chart-total check to read the bracketed counts next to each committee and sum the ticked ones, comparing that against the hit count plus joint hits.

Still writing the overview tab: the chart figure with its per-committee table and the note that joint General Comments count under both committees.

I'm laying out the paragraphs panel now: a summary line, the sort control, a note that the page only reads the file, and a list with a "Show 25 more" button that reports how many are left.

Still wiring up the paragraph list's click handling: clicks on the row buttons and article body toggle the row, unless the user has text selected, and each action button routes to its own handler.

Still writing the code that copies text to the clipboard, and the message box that confirms it or falls back to a selectable textarea when copying fails.

Now I'm working out the copy box: the live message region has to exist in the DOM before any text is written to it, so screen readers pick up the announcement.

Still writing the draft handling: a helper that adds a paragraph to the draft unless its id is already there, then saves the draft and refreshes the tab count. Records without an id get a fallback key from their index.

Still writing the draft item cards: each one shows the quote, its citation, and the symbol, short title and year, with a Remove button.

Still writing the row renderer: it picks the stored or cleaned text, cuts long paragraphs at a word break, and highlights the matches.

Still writing the note strings for each record: a leading-number mismatch, a lettered sub-paragraph, and shared pinpoints, with the duplicate count spelled out.

Still writing the record notes: a leading-number mismatch, a lettered sub-paragraph, and shared pinpoints, with the duplicate count spelled out.

Now I'm summarizing the committee and year counts for the paragraph summary line, with a different hint depending on whether the search returns any hits.

Still wiring the search controls: Enter in the input runs the search, the rail's committee checkboxes recompute the results, and the initial state starts with an empty query on the first tab with focus in the input.

Still wiring up the search box's keyboard handling: Enter runs the search, arrow keys move through the syntax options, and Escape closes the list. Clicking an option fills in the query and reruns the search, and the list closes when focus leaves the input and its options.

Next I'm checking the list's focus behaviour: a mouse click on an option moves focus to it, so it stays inside the wrapper and the list remains open. Clicking the plain help text drops focus to the body, which closes the list as intended. The Search button behaves the same way, closing the list when clicked. On load the input gets focus and the list opens straight away; it sits in normal flow and pushes the heading below it down, which is acceptable.

Still wiring the document filter and year inputs, which are built from the record data at load. Next up is the chart click handler, which will select only the committee whose bar was clicked.

Still writing the chart value labels: a plugin that draws each bar's count just to the right of the bar.

Still writing the methods section: the query gets parsed into a tree, and each paragraph's normalised text is tested against it on whole words only.

Next I'm pinning down the rest of the method notes: a hit is any paragraph that passes the filters, and joint paragraphs count under both committees. The copied text drops the footnote marks, and the leading number only goes when it matches the paragraph. The citation is built only from the stored symbol and pinpoint, and the page has no model call, so nothing leaves the browser. Last, I'm making sure the search error shows in the error line and that the input gets `aria-invalid` when the query fails to parse.

Still writing the download helper: it wraps the content in a Blob, clicks a temporary link to save it, and reports success or falls back to the copy option if the download is blocked.

Still writing the checks function: it collects the query's parsed tree and hit counts into a list of validation messages, and the download helper will wrap it all in a Blob.

Still writing the checks function: I'm validating the parsed query and then counting the rows, splitting the sorted results into pages of 25.

Still writing the checks: I'm working out the total rows across the pages from the sorted results, with a unique-id check on them.

Still working on the validation checks: I'm building the Blob-free checks list, first confirming the query parses and then comparing the row total against the hit count. Next I'm verifying that each stored paragraph's footnote marks and clean text rebuild to the original.

Now I'm wiring up the validation checks: first confirming the query parses, then comparing the row total against the hit count, and checking that each stored paragraph's footnote marks and clean text rebuild to the original.

Still writing the normalisation check: I'm collecting the positive search terms that contain a straight quote, apostrophe or hyphen, so I can build a regex that matches the exact text.

Still wiring the validation checks: I'm writing the normalisation check next, collecting the positive search terms that contain a straight quote, apostrophe or hyphen so it can match them exactly against the cleaned text.

Still writing the Blob download helper and the validation checks, which list every row against its hit count.

Still writing the stylesheet: the body uses a warm background with a serif face for headings and a monospace face for labels, and buttons get a thin border with uppercase text.

Still writing the JavaScript for the page: a few helper functions for escaping text and formatting numbers.

Still writing the normalisation helper: it swaps curly quotes, apostrophes and dashes for their straight forms so the text can be matched.

Still wiring the validation checks: the row count gets compared to the hit count, and I'm confirming that each record's footnote marks and clean text rebuild to the original.

Still writing the code that builds each record: it pulls out the paragraph number, any list label, and the committee and treaty codes from the symbol.

Still working through the record setup: each row gets a joint list of committees and treaty codes from its symbol, and a pinpoint that reads as a subparagraph, a paragraph number, or "preamble".

Still working out the record setup: the pinpoint reads as a subparagraph, a paragraph number, or "preamble", and each row gets its joint list of committees and treaty codes from the symbol.

Still writing the code that builds the records, which pulls the committee and treaty codes from each symbol and works out the pinpoint.

Now I'm laying out the checks tab: each check gets a pass or failed label, its name and detail, and any extra items listed beneath it.

Still writing the list of checks: each one gets a pass or failed label, its name and detail, and up to six extra items beneath it.

Still writing the page's HTML: a faceted filter panel with committee checkboxes, a year range, and a document selector.

Still wiring up the checkbox list and the summary rail: each committee tick box shows its hit count, and the bigger number reflects the current results.

Still writing the chart code, which builds one row per committee from the current counts.

Still writing the chart rows: each committee gets its hit count, sorted by most hits, and the overview label lists them.

Still wiring the chart: I'm building the overview rows from the per-committee counts, sorted by most hits, and updating the chart when it's already there.

Still writing the sort helper: it orders the hits by most matches within each row when the search is set to that, and the rest keep the default order.

Now I'm finishing the paragraph list: a sort wrapper for the highlight counts, then the rendering function that shows the current page of results, the summary line, and the sort label.

Still writing the row rendering: each paragraph shows its stored or clean text, long ones get cut off with a toggle, and the highlights are applied to what's on screen.

Still writing the row markup: each paragraph gets a toggle header, a meta line with the symbol link, pinpoint and year, and a check for whether it's already in the draft.

Now I'm working out the paragraph context: each row can show the previous and next paragraph from the same document, with the context stored per row.

Now I'm writing the click handler for the paragraph list, so that a row's actions, like copying a citation or adding it to the draft, respond when clicked.

Still writing the click handler for the paragraph list: it works out which row was clicked, then runs the matching action, with toggling and copying the citation or quote, and adding to the draft.

Now I'm adding the draft panel rendering: the header shows how many quotations are in the draft, and the buttons turn off when the draft is empty.

Now I'm wiring up the download function, mapping each row's fields into the CSV columns, and adding a footer that shows the source, or "source not stated" if there isn't one.

Wrapping up the source line now: the count of paragraphs, the number of distinct General Comments, the committee count, and the year span, with a link to the source.

Still writing the regex escape helpers: each character is turned into a pattern that matches its curly, straight, or dash variants, and the rest gets escaped for the regex syntax.

Still working on the regex helpers: the word matcher escapes its characters and allows any letter or digit to follow, and the phrase matcher joins its words with whitespace.

Now I'm wiring up the chart's hover handler, setting the cursor so bars look clickable.

Now I'm writing the quirk checks: counting preambles filed as paragraph 0, symbols shared across documents, duplicate groups, leading-number mismatches, lettered paragraphs, and footnote marks, each with an example citation.

Wrapping up the page code now: the quirk checks, the summary line, and the CSV export, with the source and build date in the footer.

