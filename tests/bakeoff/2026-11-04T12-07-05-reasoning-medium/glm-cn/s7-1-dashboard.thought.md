Build the full app. Must be one complete HTML file, careful with all requirements. Let me write it compactly but complete: header, tabs, filter rail, four tabs, checks, export.

Key implementation points:
- Read uhri data, compute everything.
- Paragraph regex: /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/
- UPR states extraction regexes as specified.
- Tabs role=tablist arrow keys.
- Filters: keyword (300ms), mechanism/body/type select, year from/to, SDG. Filter headings collapsible, one open at a time (accordion-ish). Three headings: 01 KEYWORD, 02 MECHANISM,BODY,TYPE (+State select), 03 YEARS AND SDG.
- Chips removable.
- Tab 01: tiles, FIG.01 chart + table, FIG.02 stacked.
- Tab 02: table with expandable rows, pagination 50.
- Tab 03: checks panel + sample.
- Tab 04: method, CSV export, copy summary, source.

Rail on tabs 03/04: only number, bar, chips. On 01/02: full filters.

Keep under ~1500 lines. Let me write.

Design: warm off-white, thin rules, serif numbers, monospace labels, red accent. Mechanism colours.

Let me write the code now, carefully but efficiently.

Details:
- Header: "UHRI · Kenya" monospace (use country from data), title, meta line: source linked, n records, n docs, years, built, "dated by document".
- Footer: one line.

Checks:
1. record count vs Number(count)
2. partitions per mechanism/body/year sum
3. type partition
4. chart vs table: recompute via second loop
5. links: doc_url starts https://docs.un.org/ and ends with symbol (decodeURIComponent, case-insensitive)
6. paragraph share per mechanism; UPR <100% warning
7. states found: count with ≥1 state vs UPR count; list failures with symbol
8. duplicates/gaps: distinct id, duplicate texts, counts of no themes/sdgs/affected_persons
9. random sample: 10 cards, Fits/Doesn't fit/Unsure, tally, seed mulberry32.

CSV export: comment lines with country, source, built, filters, row count; columns: date, body, mechanism, type, symbol, doc_url, paragraph, recommending states, first line?, full text, themes, sdgs, sdg_targets, affected_persons, section. Escape CSV.

Copy summary: plain text with headline numbers and top ten themes.

Chart.js horizontal bar: indexAxis 'y', value at end via plugin or afterDatasets — I'll write a small plugin to draw value at bar end.

FIG.02 stacked bar per year per mechanism with all years.

Clicking bar in FIG.01 adds theme filter chip — theme filter isn't in the rail headings... chips need removable. I'll have a chips container; theme chip exists alongside. Fine.

Row expansion: click row (tr) toggles a detail row. Keyboard Enter.

Sort: date desc, body, paragraph asc, file order. Click Date header reverses (toggles asc).

Highlight keyword in first line with <mark> (escape HTML first).

Show "see the States" link in UPR tile on tab 01, opens in-place list of top ten States.

Rail filters visible on tabs 01/02; on 03/04 hide filter sections but keep number/bar/chips.

Accordions: each heading button toggles; only one open at a time.

Mechanism/body/type selects: Body options depend on chosen mechanism. State select under heading 02 with counts.

Let me count clickables on tab 01: 4 tabs + rail: Clear all + 3 headings + keyword input... ~8ish, acceptable ("about seven").

Write code now. I'll aim for solid, ~900 lines.

Number formatting: toLocaleString.

State filter: a select of all states with counts.

Filter state object: {kw, mech, body, type, state, y1, y2, sdg, theme}.

Theme chip: active theme filter.

Now the code.

For value-at-end plugin:

```js
const valueLabel = {id:'valueLabel', afterDatasetsLinks... }
```
Use afterDatasetsUpdate? Simpler: afterDatasetsDraw, draw text at bar end for datasets where meta dataset is bar horizontal. I'll apply only to fig1 chart.

Checks: compute once at load (link check over all records — fine, ~2k).

Paragraph extraction memo per record.

States memo per record.

Seeded sample: mulberry32(seed), pick 10 distinct indices from filtered set.

Escape HTML helper.

CSV download via Blob.

Let's write.

For the tabs: buttons with role tab, aria-selected, arrow key nav.

Pagination: visibleCount, "Show 50 more".

Copy citation: navigator.clipboard.writeText fallback with textarea; "Copied" confirmation 2s.

Now write whole file.

Filter logic function matches(rec).

Year selects: distinct years sorted; swap if reversed.

SDG select: goals present, sorted, with names from sdg_names.

Chips: for each active filter show removable chip (button ×).

Rail share bar: red width % of file.

Overview tiles:
- Tile 1: total records (filtered), type breakdown line.
- Tiles: documents, years, then one per mechanism (records, docs, latest year, share).
"How this is computed" lines.

Upr tile contains "see the States" link when UPR in filtered... "in the UPR tile". Yes.

FIG.01: top 10 themes chart + table.

OK writing.

Edge: mechanism values order — keep first-seen order.

Chart destroy/recreate on filter change — I'll keep chart instances and update data.

Time to write the final file.