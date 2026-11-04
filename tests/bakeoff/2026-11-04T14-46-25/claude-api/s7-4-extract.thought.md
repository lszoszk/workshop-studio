I'm planning the app's layout: a header, tabs, and a left rail that stays visible. I'm also checking the clickable-element limit, counting tabs, download options, and headings for each view to make sure none goes past about seven.

Still writing the data-parsing code...

I'm parsing the document's tables and paragraphs, marking the first table's rows as covered and listing any later tables as unclassified. I'm also normalising whitespace and matching the numbered paragraphs with a simple pattern.

I'm checking how the headings get labelled: a roman-numeral label marks a part, and a letter label marks a section. I'm also treating a label with no space after the dot as still valid, and building the part and section names from those labels and the heading text.

I'm working out how the path is built: the part name, then the section, shown together when they differ. A heading with no label gets used as the section as is, and anything before the first heading gets a placeholder. Next I'm setting up a sentence-spacing repair that inserts a space after a period when a lowercase letter runs straight into a capital.

I'm applying the repair rules in sequence: a space after a period before a capital, a space after a comma between letters, a space before an opening quote, and a space after an en dash. For each change I want to log the paragraph, the rule, and about twenty characters of context on either side, both before and after the replacement.

I'm settling on a single-pass repair: one combined pattern that finds each spot needing a space, so the inserted spaces can be tracked for marking in the expanded paragraph.

I'm settling on one combined pass for the repairs: a single pattern that finds each spot needing a space and inserts it at the match end, so the added spaces can be marked in the expanded paragraph later.

I'm building the text-repair step as one pass: a single pattern finds each spot needing a space, the space goes in at the match end, and I record the position so it can be marked in the expanded paragraph. For each match I'll note which rule fired and keep about twenty characters of context on either side for the log.

I'm building the repair so each restored space goes in at the end of its match, and I'll record its position so it can be highlighted in the expanded paragraph. For the log, I'll keep about twenty characters on either side of each insertion, showing the original and the repaired version.

I'm defining how each paragraph's first words get compared against the reference: both sides are normalized first, with curly quotes made straight and dashes and non-breaking characters converted. A paragraph with no reference entry gets marked as having no reference rather than as a match, and the check is skipped entirely when no first-words data exists. Next I'm moving on to the second tab's checks.

I'm moving on to the checks list: first the paragraph count against the reference, then whether the numbering runs exactly 1 to n with no gaps, duplicates or out-of-order entries, and then the first-words mismatches. I'm about to work out how to handle the footnote count, which depends on whether the reference lists any footnotes.

I'm settling on how to count footnotes: I'll compute the count from the document, using superscripts and footnote-style elements, and show that number, even though it may be off if other files have superscripts.

I'm adding a check that the repaired text matches the original once the inserted spaces are removed, and that all the spaces were logged. Next I'm looking at the heading checks: whether the counts of h2 and h3 look right, and whether every glued label has been split into its own label and heading text.

I'm checking the remaining verification items: the heading counts, that every heading was classified, and that nothing was lost. I'm also adding an export round-trip check and settling the status labels for the header line.

I'm settling the header status: a red dot with the failure count if any check fails, otherwise a green "n of m checks pass" line, with the source limit shown separately. I'm also deciding that a missing reference keeps the dot neutral rather than green, and I'm considering whether the failed-check link should jump somewhere useful, since the second tab has no filter.

Next I'm setting up the tab 02 table, with each row's number as a button that expands the paragraph, and I'm weighing whether the check panel's "see rows" link should open the first affected paragraph.

I'm laying out the tab 02 interactions: each row's number is a button that expands a detail row, with the row itself also clickable, and the headings box is a collapsed button that lists the headings with their paragraph counts.

I'm settling on the rail card: a monospace symbol next to a short title, which I'll take from the document's title by cutting it at " on " when that split works and falling back to a plain truncation otherwise.

I'm sizing the rail's stats too: paragraph count against the reference, shown in red when it doesn't match, plus footnotes and the checks summary.

I'm laying out the first tab: four tiles in a 2x2 grid, with the paragraph count shown in green when it matches the reference and red with the difference when it doesn't. A missing reference gets a plain note instead, and if no paragraphs were found at all, the tab says so and the exports are disabled.

I'm working out the export details: the JSON records will carry each paragraph's symbol, number, section, text, match status, citation and source link, with a note about the missing footnotes. Downloads will be named from the symbol, and the Markdown version will start with a front-matter block recording the counts and source.

I'm settling the Markdown export: front matter with the title, symbol, adoption date, source link and counts, with a note that no footnotes exist in this HTML version. Then headings in document order as ## and ###, and each paragraph as its bold number followed by the repaired text.

I'm finishing the footer and the header details, and I'm noting that the footer should only show the build date if the document provides one. Next I'm sketching the shared helpers: an escape function, today's date, the keyboard handling for the tabs with roving focus and hidden panels, and a toggle for the collapsible sections.

I'm setting the tab 02 and tab 01 tables with their captions and labels, plus a light-on-cream palette with a clear red focus ring that stays readable on the background.

I'm working out the detail panel for each paragraph: the full repaired text with restored spaces marked, a note that the raw text is in the JSON export, the section path, and a copy-citation button with a fallback for when the clipboard is blocked. The path will be built from the part label and heading, dropping the section when it is the part itself.

I'm working out how the path for each paragraph gets built: the part label and heading go first, dropped if they match the section, followed by the nearest section, joined with arrows. Next I'm thinking about how to tell part headings apart, treating an h2 with a Roman-numeral label as a part. Then I'm sketching the heading object itself, with its level, label, heading text, full text, and whether the label was glued to the heading.

I'm checking how to handle nonbreaking spaces: the heading text may contain them, and I want the whitespace collapse to keep the published wording, so I'm narrowing it to ordinary whitespace characters and leaving those alone.

I'm checking how the nonbreaking spaces in the headings get handled, so the whitespace collapse only touches ordinary spaces and the published wording stays intact. I'm also planning to count the paragraph classes (cover, title, heading, paragraph, committee) and to list any paragraphs or headings in extra tables as unclassified.

I'm defining the check objects with an id, name, a Given/when/expect story, the expected and actual values, a status, and the paragraph numbers each one touches. In the panel, failing checks will get a "see rows" button when they point at paragraphs, and a summary line will list every check with its compared values and status.

Still writing the JS helpers and the table logic...

Now I'm writing the paragraph-counting loop, tallying each element into its class (cover, title, heading, paragraph, committee) and flagging anything that falls outside those.

Now I'm parsing the document's paragraphs and headings, starting with the tag loop that sorts each element into its class.

Still writing the paragraph parser, splitting each numbered paragraph's text and recording the repairs it makes.

Still writing the heading parser, working out how to split each label from its heading text and whether the label was glued on.

Still writing the paragraph parser's helpers, normalizing quotes and dashes and taking the first six words for the reference check.

Still writing the checks, working out the numbering test: I'm collecting the paragraph numbers, flagging any duplicates or gaps, and marking the order check as failing if anything is out of sequence.

I'm writing the checks and the goToPara helper that jumps from a failing check to its paragraph rows, then the HTML skeleton with the header.

Still writing the HTML skeleton: a header with the title and status, a two-column layout with a rail and a tab bar, and a footer.

Still writing the CSS: tabs with a bottom accent on the active one, a two-column tile grid, large serif numbers, and tables with mono headers and right-aligned figures.

I'm wiring up the record builder and the JSON check, which only needs the paragraph records since the checks don't feed into it. I'm also settling the footnote line: the HTML version has no footnotes, so the note will just give the count from the reference, or say the number is unknown.

I'm wrapping up the header status and the progress bar in the rail: red when the paragraph count is short or over, green when it matches. The first tile will show the count found beside what the document says it has, with a note on whether it's equal, short, or over. The second tile will show how many first-word matches there are out of the total.

Now I'm wiring the repairs tile, the first-word differences list, and the export buttons, with a disabled state when there are no paragraphs.

Still writing the page helpers: an escape function for the HTML, and a short title for the rail taken from the document title, or a shortened fallback.

Still writing the helpers: the section column falls back to a dash when there's no section, and the first-line preview is cut at a word boundary near 120 characters.

Next I'm adding the marked-text builder, which wraps each restored space in a highlighted span.

Still writing the download helper, building a blob from the content and triggering a link click to save the file.

Now I'm wrapping up the download helper: it builds a blob from the content, triggers a link click to save the file, and then cleans up the object URL.

Still working through the status rendering and the three checks: footnotes come out as a limit when the count falls short, and the paragraph count and first-word checks each depend on whether a reference exists.

Now I'm wrapping up the status line and the rail: the header shows how many checks failed or pass, and the rail repeats the pass count out of the total.

Now I'm wiring up the result rendering and the tile markup, then attaching the click handlers for the check-panel links.

I'm settling the final answer format now, writing the code out in full with the escape helper, the title fallback, and the download and status logic.

