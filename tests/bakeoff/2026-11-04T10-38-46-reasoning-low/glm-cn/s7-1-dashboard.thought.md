Build the full app per the plan. Need to be comprehensive but under ~1500 lines. Let me write the HTML.

Key components:
- Header with label, title, source line.
- Tabs: 01 Overview, 02 Records, 03 Check, 04 Method & export. role=tablist, arrow keys.
- Left rail filters: shown on tabs 01,02; on 03,04 only number/bar/chips. Three collapsible headings: 01 Keyword, 02 Mechanism/body/type (+State select when extracted), 03 Years and SDG.
- Filter state: keyword, mechanism, body, type, state, yearFrom, yearTo, sdg, theme (from chart clicks).
- Overview: tiles (all records + type breakdown, documents, years, per-mechanism tiles), FIG.01 chart + table, FIG.02 stacked bar by year.
- Records tab: search box (same as keyword), table with columns, expandable rows, show 50 more, date header sort toggle, mark highlights, State column, copy citation.
- Check tab: self-checks + random sample with mulberry32 seed, tally.
- Method tab: method text, CSV download, copy summary, source/licence/build date.
- Footer.

State extraction: only UPR, regex per plan.

Let me write the code carefully but compactly.

Design: paper/ink palette, accent red. Serif Georgia. Monospace labels.

Implementation notes:
- Data: const U = WORKSHOP_DATA.uhri; records = U.records.
- Precompute paragraph numbers, states per record.
- Filters combine AND.
- Theme filter chips from chart click.
- Chips removable.

Filter headings: buttons with aria-expanded, one open at a time.

Counting checks: compute per mechanism/body/year/type sums, links check, paragraph shares, states found, duplicates/gaps.

Random sample: seeded mulberry32, draw 10 from filtered set, cards, verdict buttons, tally.

CSV export: comment lines with # prefix? CSV comments - fine.

Copy summary: headline numbers + top ten themes.

Let me write it.

For the timeline chart: years min..max, stacked bars per mechanism.

Chart.js config: horizontal bar for FIG.01, indexAxis 'y', red color, value at end via custom plugin or just use datalabels? No datalabels plugin. I can draw values with a simple plugin. Write small inline plugin to draw value at end of bar.

FIG.02: stacked bar chart with three mechanism colors.

Handle empty filtered set: show "No records match".

Keep the tab panels rendered on demand; charts destroyed/recreated on filter change.

Table: rows rendered 50 at a time, expandable via click, keep it a button-like row. Use tr with tabindex=0.

Paragraph regex: /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/.

State extraction regexes per plan.

Sorting: date desc, then body, then paragraph number asc, then file order. Toggle on Date header click reverses (date asc... simplest: reverse whole sort order).

First line: 120 chars at word.

Copy citation: navigator.clipboard.writeText with fallback (execCommand). Sandbox may block clipboard; use try/catch and fallback to textarea copy. Show "Copied".

Checks on tab 03 render when opened (compute fresh).

Let me write the HTML now. Aim ~1000 lines.

Chips: keyword, mechanism, body, type, state, years, sdg, theme(s).

Rail visibility: on tabs 3/4 hide filter headings (set hidden on the sections container) but keep number, bar, chips, Clear all? Plan: "on 03 and 04 the rail keeps only the number, the bar and the chips." So hide the "FILTERS"/Clear all heading too? Keep Clear all maybe not. I'll hide the collapsible headings and Clear all; chips remain removable.

Actually plan says rail headed "FILTERS" with "Clear all" at the right. On tabs 03/04 keep only number, bar, chips. So hide the FILTERS/Clear all header too? Chips need removal but that's per-chip ×. I'll hide the whole filter controls including Clear all, keeping number/bar/chips.

Overview tiles: "one tile per mechanism (records, documents, latest year, share)". Plus a "see the States" link in the UPR tile that opens an in-place list "Ten States that made most recommendations to Kenya".

Type breakdown under first tile.

Let me now write everything. Numbers formatting: toLocaleString.

Write the code.

Keyword applies to text or symbol substring; every word must occur (in text or symbol, per word either field). "every word must occur as a substring of text or symbol" — I'll check word in (text+symbol combined? or either). Simplest: word must be substring of (text + ' ' + symbol). Fine.

Debounce 300ms.

Year selects: distinct years sorted; swap if reversed.

SDG select: goals present in data with names from sdg_names.

State select: states found with counts, only when any UPR records.

Filter counts for body shown within chosen mechanism.

Now the check computations:

1. records.length vs Number(U.count).
2. Partitions: sums per mechanism, body, year.
3. Type partition sum.
4. Chart vs table: recompute theme counts second loop — just recompute and compare; largest bar ≤ filtered count.
5. Links: doc_url starts with https://docs.un.org/ and ends with symbol (case-insensitive after decodeURIComponent). List failures.
6. Paragraph numbers share per mechanism; UPR 100% expected.
7. States found: UPR records with ≥1 state vs total UPR; list those without.
8. Duplicates/gaps: distinct id vs count; duplicate text count; records with no themes/sdgs/affected_persons.

Sample check: seeded draw, cards, Fits/Doesn't fit/Unsure, tally with seed.

Write code now. I'll be efficient.