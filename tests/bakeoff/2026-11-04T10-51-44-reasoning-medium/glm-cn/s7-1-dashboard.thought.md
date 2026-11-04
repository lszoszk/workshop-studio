Build the full app per plan. Need to be careful about size, but write one complete HTML. Let me write it efficiently.

Key components:
- Header, tabs (4), left rail with 3 filter headings (accordion), big count, chips.
- Tab 01: tiles (total+type breakdown, documents, years, mechanism tiles), FIG.01 chart + table, FIG.02 stacked bars, UPR tile "see the States" expandable list.
- Tab 02: search field, table with columns Date|Body|Symbol|Para|First line|State, expandable rows, copy citation, pagination 50.
- Tab 03: checks panel + random sample label check with cards, seed, tally.
- Tab 04: method text, CSV download, copy summary, source.

State: filters {kw, mechanism, body, type, state, yFrom, yTo, sdg, themes:Set}. Theme chips from chart clicks. Theme filter applies everywhere? Plan says clicking bar adds theme as filter chip — so themes filter too.

Filters AND combined. Rail on tabs 01/02 shows filter headings; on 03/04 only number/bar/chips.

Let me write the code. I'll keep it organized but complete. Aim ~1000 lines.

Data prep: records, states extraction for UPR, paragraph numbers computed.

Write CSS per design. Tabs with arrow keys.

CSV export with comment lines. Copy summary via clipboard.

Checks: as listed.

Sample: mulberry32 seeded.

Let me write.

Chips: active filters shown as removable chips. Represent filters as array of {key, label, remove}. I'll derive chips from state.

Controls per tab: tabs count as 4 clickable; rail headings 3 (accordions) — fine, plus within heading mechanism/body/type selects — that might exceed 7 per view but plan explicitly says so. OK.

Keyword: 300ms debounce applied to state.kw, and tab02 search box is the same box — meaning on tab 02 there's a search field at top mirroring rail keyword. I'll just have the rail keyword box, plus a search field on tab 02 that syncs. Simpler: one search input in rail; tab 02 has its own search box synced two-way.

Rendering: functions render() re-renders rail number, chips, current tab content. Charts destroyed/recreated.

Let me write code now.

Paragraph regex: /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/ — capture group.

State extraction regexes as given.

Table sort: date desc, body, para asc, then file order. Clicking Date header reverses (toggle sortDir).

Expand row: in place, details div.

Highlight keyword matches with <mark> in first line — escape HTML then wrap words.

Checks computed over full file (not filtered) mostly; chart-vs-table check uses filtered.

Sample tally stored in JS; verdicts per card.

Write everything. Keep under ~1500 lines.

Filter application:
```js
function applyFilters(){ return records.filter(r => matches) }
```
kw: every word substring of (text+symbol).lowercase.
mechanism exact, body exact, type exact, state: states(r).includes(state), year range, sdg includes, themes: record.themes includes all selected themes? Chip per theme; AND across themes.

Rail share bar: filtered/total *100%.

Year selects: swap if reversed.

Big number aria-live.

FIG.01: Chart.js horizontal bar, red bars at 80% opacity, value at end via custom plugin or just datalabels not available — write a small inline plugin drawing text after bar. I'll write a plugin:

```js
const valueLabels = {id:'vlabel', afterDatasetsDraw(chart){...}}
```
Draw value text at end of each bar.

FIG.02 stacked bars with mechanism colors.

Charts only on tab01; create when tab shown (or on render if tab active).

Table pagination: visibleCount, show 50 more.

Copy citation: navigator.clipboard.writeText with fallback textarea.

CSV: build with Blob, comment lines starting with #.

Let's write. Also footer.

Body select: bodies present in chosen mechanism with counts. When mechanism changes, reset body if not present.

Type select: values present in filtered-by-others? Keep simple: values present in chosen mechanism.

Now write the HTML.

For the "see the States" link in UPR tile: toggles a list in place "Ten States that made most recommendations to {country}" with counts for current filter.

Tab 03 checks — implement each:

1. count: records.length vs Number(uhri.count).
2. partitions per mechanism/body/year sum == count.
3. type partition.
4. chart vs table: recompute top themes second loop; check largest bar <= filtered count.
5. links: doc_url starts with https://docs.un.org/ and ends with symbol (case-insensitive after decodeURIComponent). List failures.
6. para share per mechanism; UPR <100% warning.
7. States found vs UPR count; list records without.
8. duplicates/gaps: distinct id, duplicate texts count, counts of missing themes/sdgs/affected_persons.
9. Random sample check with cards.

Sample cards: one open at a time (accordion), with Fits/Doesn't fit/Unsure buttons, tally line.

OK. Write.

I'll write compact but readable JS. Let's go.