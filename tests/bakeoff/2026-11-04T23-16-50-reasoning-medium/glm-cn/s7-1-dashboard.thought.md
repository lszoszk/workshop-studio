Build the full app. Need to be under ~1500 lines. Follow the plan carefully. Let me write the HTML.

Key features: header, tabs (3), left rail with filters (3 collapsible headings), overview tab with tiles, FIG.01 chart + table, FIG.02 stacked chart, checks panel; records tab with search, table, expandable rows, pagination; method tab with CSV export and copy summary; footer.

Let me write compactly but completely. I'll aim ~900 lines.

Data: WORKSHOP_DATA.uhri = {country, title, source, source_url, built, count, records}.

Filters state: keyword, mechanism, body, type, state, yearFrom, yearTo, sdg, theme (from chart click), and possibly type from tile? Plan says "The Type filter (all / each type value present) starts on 'all'." — that's in the heading 02? Actually tile breakdown per type — Type filter is in heading 02 Mechanism/body/type. OK.

Chips: removable, show active filters.

Tab 03 rail: only number, bar, chips — hide filter headings.

Implement:

- computeFiltered(): AND all.
- Paragraph extraction regex.
- UPR state extraction.
- Checks panel.
- CSV export with comment lines.
- Copy summary.
- Copy citation with clipboard fallback (textarea execCommand) since clipboard API may not work in sandbox? Use navigator.clipboard with fallback.

Charts: Chart.js 4 preloaded. FIG.01 horizontal bar, indexAxis 'y', click bar → add theme filter chip. FIG.02 stacked bar.

Row expansion: click row → expand details row.

Sorting: date desc, body asc, paragraph number asc, then file order. Click Date header reverses.

Pagination 50.

Keyboard: tablist arrows. Filter headings buttons aria-expanded, one open at a time.

Write code now.

Number formatting: toLocaleString.

Type filter in rail heading 02 lists type values present.

Body select shows bodies present in chosen mechanism with counts.

State select joins heading 02 when States extracted — since we extract states, show it.

FIG.01 percentages of filtered records; years range per theme.

"see the States" link in UPR tile opens in place a short list "Ten States that made most recommendations to Kenya" with counts for current filter.

Checks: implement as listed.

Let me write it.

Edge: empty filtered set — show "No records match".

CSV: columns date, body, mechanism, type, symbol, para, states, first line? "visible columns plus full text and labels". Include: date, body, mechanism, type, symbol, doc_url, paragraph, recommending_states, text, themes, sdgs, sdg_targets, affected_persons, section.

Copy summary: paragraph with headline numbers and ten themes.

Tabs: 01 OVERVIEW · 02 RECORDS · 03 METHOD & EXPORT.

Filters shown on tabs 01, 02; on 03 hide filter headings (keep count, bar, chips).

Write the file.