I need to work out the query parsing semantics: quoted phrases, implicit AND between words, OR with lower precedence joining groups, and NOT excluding terms, without support for bracketed expressions.

For rendering, I'm weighing whether to show all matches at once or paginate in batches of 50-100 with a "Show more" button, since the match count needs to stay accurate even with an empty query showing everything.

For matching whole words, I'm planning a Unicode-aware regex using lookaround boundaries so partial word matches don't count, applied case-insensitively.

For phrases in quotes, I'm treating them as an exact sequence of words joined with flexible whitespace, and normalizing curly quotes to straight ones. I'm tokenizing the query with a regex that separates quoted phrases from individual words, treating uppercase AND/OR/NOT as operators while stripping stray punctuation from plain word tokens.

Then I'm building parsing logic: grouping terms with OR creating new alternative groups, AND being implicit, and NOT marking the next term as negated — a document matches if any group has all positives present and no negatives present.

For highlighting, I plan to use the matching group's positive terms to build a combined regex and wrap matches in mark elements via safe DOM construction, preserving whitespace with pre-wrap styling.

For filters, I'm adding committee selection plus year-from/year-to dropdowns populated from distinct years in the data, treating unknown years as included only when both bounds are open, with any change re-running the filter.

For the chart, I'm using Chart.js to show a bar per committee with counts of matching paragraphs, sorting by count descending, labeling missing committees as "Unknown", and handling the case where Chart.js isn't loaded, with integer ticks and animations disabled.

For sorting, I'm ordering results newest-first by year with unknown years last, then by symbol, then by paragraph number ascending. The header line pulls the source and record count from the data and shows the year range, while the count line summarizes matches against active filters. For citations, I'm using the clipboard API with a textarea/execCommand fallback, showing "Copied" for two seconds, formatting as symbol plus paragraph number when available and omitting invented values, and linking symbols to doc_url when present while adding a "how computed" note near the chart.

Now I'm working through search behavior: I'll treat search as running on button click or Enter, with filter changes re-applying against the last submitted query rather than live-typing, to keep the display consistent. I'm writing a regex to match whole-word phrase sequences, escaping special characters and deciding how to handle separators between words—using whitespace boundaries for normal phrases but accounting for hyphenated terms where a strict `\s+` separator wouldn't match.

Still working out matching rules...

Now I'm setting flags on the regex (case-insensitive, unicode-aware), deciding to compile separate global and non-global versions for highlighting versus testing matches, and confirming lookbehind/lookahead with unicode property escapes will work correctly. Then I'm moving on to writing the CSS layout and the rendering logic for displaying the filtered results list with a visible-count mechanism.

I'm adding a "Show more" button that reveals more results and a line noting how many of the total matches are currently displayed, along with tracking which group matched each record so I can build a per-group highlight regex from its positive terms for coloring matched text in each card.

