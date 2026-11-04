Build the full app per plan. Single HTML file, offline, Chart.js preloaded. Let me write carefully but efficiently.

Key components:
- Header, tabs (4), left rail filters (accordion: keyword, mech/body/type+state, years/SDG), chips.
- Tab 01: tiles, FIG.01 bar chart + table, FIG.02 stacked bar.
- Tab 02: search box (shared keyword), table with expand, copy citation.
- Tab 03: checks + sample.
- Tab 04: method, CSV export, copy summary, source.

Filters state: {keyword, mechanism, body, type, state, yearFrom, yearTo, sdg, themes:Set}. Theme filter via bar click chips.

State extraction precomputed for UPR records.

Sorting: date desc, body, para asc, file order. Date header click reverses.

Paragraph regex: /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/.

Let me write the code. Keep it structured. Aim ~1000 lines.

Data access: const U = WORKSHOP_DATA.uhri; records; country.

Filters logic as spec. Keyword: every word must occur in text or symbol, lowercase substring.

Rail visible headings only on tabs 01/02; on 03/04 hide filter headings (keep number, bar, chips). Chips removable.

CSV export: comment lines then columns: date, body, mechanism, type, symbol, para, state, text, themes (joined by "; "), sdgs, sdg_targets, affected_persons, section. Use Blob URL download.

Copy citation: navigator.clipboard.writeText with fallback.

Checks: implement all listed. Link check: url starts with "https://docs.un.org/" and ends with symbol (case-insensitive after decodeURIComponent).

Sample check: seeded mulberry32, draw 10 from filtered, cards with Fits/Doesn't fit/Unsure, tally.

Charts: destroy/recreate on filter change. Chart.js horizontal bar for themes (indexAxis y), stacked bar for years.

Mechanism colours map with fallback.

Tabs arrow-key navigation.

Let me write it.

Design: paper #f4f0e8, ink #1d1b18, rule #d9d2c3, accent #9b2335. Fonts per spec.

Structure HTML:

header
main: aside rail + section tabs panel
footer

Write code now. Careful with details:

- UPR states column: from precomputed states array or "State not found" or "–".
- "see the States" link in UPR tile on tab 01 → in-place list of top ten states with counts.
- Filters accordion: three headings, one open at a time.
- Rail hidden filter panels on tabs 3/4: hide the accordion container.
- Big count aria-live.
- Year from/to selects swap if reversed.
- SDG select with goal number + name.
- Show 50 more pagination.
- mark keyword highlight in first line and full text? Highlight matches — in table first line. For simplicity highlight in first line and expanded text too (using words, escaped regex). I'll highlight in both.
- CSV escaping.

Copy summary: paragraph with headline numbers and ten themes.

Let me write the whole file.

For chart click on theme bar: onclick get index → theme label → toggle theme filter chip.

Themes as filter chips set. Chips display with remove buttons.

Check panel: build list of check rows with pass/fail.

Duplicates: count duplicate texts.

Also "see the States" toggle.

Number formatting: toLocaleString.

Let me now write. I'll be concise in code but complete.