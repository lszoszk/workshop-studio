The user has provided a detailed plan and attached the Kenya UHRI file. I need to build a complete HTML app following the specification. Let me carefully work through the requirements.

Key structure:
- Header: monospace label "UHRI · [country]", title, source line with n, docs, years, built date, "dated by document" hint.
- Four tabs: 01 OVERVIEW, 02 RECORDS, 03 CHECK, 04 METHOD & EXPORT.
- Left rail with filters (shown on tabs 01 and 02; only number/bar/chips on 03 and 04).
- Footer.

Let me write the code carefully.

Data: `WORKSHOP_DATA.uhri` = {country, title, source, source_url, built, count, records}.

Filters:
- Keyword: text box, 300ms debounce, applied to text or symbol, every word must occur as substring (lowercase).
- Mechanism (all / each value), Body (values present in chosen mechanism, with counts), Type (all / each value present). State select joins this heading (02 heading) when States are extracted — actually the plan says "A State select joins this heading when States are extracted." So heading 02 "Mechanism, body, type" also holds the State select.
- Years (from/to selects of distinct years, swap if reversed), SDG (goal number and name from sdg_names, only goals present).

Rail structure: "FILTERS" heading with "Clear all" at right. Big serif number of matching records (aria-live), "of N in the file", thin red bar share. Chips for active filters. Three numbered collapsible headings, one open at a time (accordion). On tabs 03/04 the rail keeps only number, bar, chips.

Tab 01 Overview:
- Row of big serif numbers: first tile counts all records in file (with type breakdown), documents, years. Below, one tile per mechanism (records, documents, latest year, share of filtered set). Wait — "The first tile counts all records in the file" — but then "Every tab reads the same filtered set". Let me re-read.

"A row of big serif numbers. The first tile counts **all records** in the file: recommendations, concerns/observations and any other `type`. Under the number, one line gives the breakdown per `type`, spelled as in the data. The Type filter (all / each `type` value present) starts on 'all'."

Hmm, "The first tile counts all records in the file". But then tiles per mechanism show "records, documents, latest year, share of the filtered set". I think the headline tiles show file-level numbers (total records, documents, years) regardless of filter? Actually re-reading: "The first tile counts all records in the file". So the first tile is file total. Documents = distinct symbol (of the file? or filtered?). The plan says "Documents = number of distinct symbol. Years = minimum and maximum year" under "How every number is computed" — that's generic. Hmm.

Actually, I think it's cleaner: the headline row shows file-level totals (all records, documents, years) — these describe the file. Then "Below, one tile per mechanism (records, documents, latest year, share of the filtered set)". Mechanism tiles reflect the filtered set. Hmm, but if the first tile always shows the file total, it doesn't respond to filters, which is a bit odd but matches "counts all records in the file". Actually wait — maybe the first tile shows the filtered count and the breakdown per type of the filtered set? "The first tile counts all records in the file: recommendations, concerns/observations and any other type" — this says it counts ALL records in the FILE. The breakdown line gives counts per type. And "The Type filter... starts on 'all'". 

Hmm, but if you apply a type filter, the first tile should probably reflect it. Let me reconsider: maybe the intent is the first tile shows the count of all record types (i.e., not just recommendations) — i.e., it's the filtered count including all types, with the breakdown per type under it. "in the file" might just clarify it includes all types. But "counts all records in the file" is pretty explicit.

I'll interpret: first tile = number of records in the current filtered set (which starts as all records in the file), with breakdown per type of the filtered set. Hmm, but that contradicts "in the file".

Actually, let me think about what makes a better app. The rail already shows the filtered count. The overview tiles: if they never respond to filters, the tab is static except charts. If they respond, everything is consistent. The plan says "The filtered set feeds the tiles, both charts, the table and the export." — under "How every number is computed", Filters section. So the tiles DO read the filtered set. Then "The first tile counts all records in the file" must mean: the total tile counts records of all types (recommendations + concerns + other), i.e., the headline total = records.length (of filtered set, which by default = file). Under it, the breakdown per type.

Hmm, "**Headline total** = `records.length`." — that's the file length. OK so headline total is the file's record count. But tiles per mechanism show "share of the filtered set". This is ambiguous. Let me just make the tiles respond to the filter, with the first tile being the filtered count (which equals the file total when no filter), and the type breakdown of the filtered set. And documents/years tiles... "Beside it: documents (distinct symbol) and years (min–max of year)". If filtered, these would be of the filtered set too.

Actually wait, re-reading once more: "The first tile counts **all records** in the file: recommendations, concerns/observations and any other `type`." The bold "all records" emphasizes it includes all types. I'll make all tiles read the filtered set (which defaults to the whole file), since the plan explicitly says "The filtered set feeds the tiles, both charts, the table and the export." That's decisive. The first tile = filtered records count, breakdown per type below.

Hmm, but "documents (distinct symbol) and years (min–max of year)" — of the filtered set. OK. And mechanism tiles: records, documents, latest year, share of the filtered set. Good.

Wait, actually there's a subtlety: if you filter by mechanism, the other mechanism tiles would show 0. That's fine and informative.

Hmm, but actually maybe the headline row (first tile + documents + years) should be file-level always, and only mechanism tiles filtered? "The first tile counts all records in the file" — if it were filtered it would say "in the filtered set". Ugh. Let me go with: headline row = file-level (total records, documents, years) — always the same, describing the file, and mechanism tiles = filtered. Hmm, no...

Let me think about it from the user's perspective: "how much the UN mechanisms have said, about what, and when". The overview answers with the file stats, then the filter narrows the charts. But the plan says the filtered set feeds the tiles.

Decision: I'll make the first tile and its breakdown read the filtered set (so it responds to filters, consistent with "The filtered set feeds the tiles"), but the tile's caption will say "matching records" vs... no wait.

Actually, you know, let me just re-read the exact wording one final time:

"A row of big serif numbers. The first tile counts **all records** in the file: recommendations, concerns/observations and any other `type`. Under the number, one line gives the breakdown per `type`, spelled as in the data."

I think the safest reading: the first tile = total record count (which, when no filter, = the file). The app opens with no filter, so initially it shows the file total. When filtered... "The filtered set feeds the tiles" says it changes. OK final decision: tiles read the filtered set. First tile = count of filtered records (all types), breakdown per type of the filtered set. When no filter, this is "all records in the file". The Type filter default is "all". Good, consistent.

Hmm, wait, but actually there's a problem: if the type filter is set to "Recommendations", the first tile shows only recommendations, and the breakdown shows the counts. That's fine.

But "The first tile counts all records in the file" — with a type filter set, the first tile would NOT count all records in the file. Contradiction with "filtered set feeds the tiles". I'll go with filtered-set-driven, and add a "How this is computed" note: "Records in the current filter; the file holds N." That satisfies both transparency and responsiveness. Actually, let me add to the first tile note: "n of N in the file" style. Good.

Hmm, actually, let me reconsider once more. "The first tile counts all records in the file: recommendations, concerns/observations and any other type." — I now think this is explaining that the headline number is not just "recommendations" but all records (because UHRI exports often only have recommendations). The emphasis is on "all records" (all types), not "in the file". So the tile = filtered count, all types included. 

OK moving on.

FIG.01: top ten themes, horizontal bars, ranked, count at end of bar, red at 80% opacity. Clicking a bar adds theme as filter chip. Under chart, table: Theme | Records | % of filtered | Years (first–last). Note about multi-theme.

Wait — should themes also be a filter (clicking bar adds theme chip)? Yes: "Clicking a bar adds that theme as a filter chip." So there's a theme filter too, as a chip. But the rail has only three numbered headings (01 Keyword, 02 Mechanism/body/type, 03 Years and SDG). Where does the theme filter live? As a chip only — the plan says "Active filters show as small removable chips under the number". Clicking a bar adds a theme chip. So themes aren't in the rail headings; they're chip-only filters. OK. Similarly the State select: "A State select joins this heading when States are extracted" — the State select joins heading 02 (Mechanism, body, type). OK.

So filter state:
- keyword: string
- mechanism: null or value
- body: null or value
- type: null or value
- state: null or value (recommending State)
- yearFrom, yearTo: null or values
- sdg: null or number
- theme: null or value (from bar click chip)

All combine with AND. Chips show all active ones, removable.

Hmm wait, theme chip — but themes aren't in the rail as a heading. The chip appears under the number with an × to remove. Fine.

FIG.02: stacked bars per year by mechanism, colors: UPR #c2410c, Treaty bodies #0f766e, Special Procedures #7c3aed. All years from first to last of... the filtered set? "every year from the first to the last appears, so empty years are visible gaps" — first to last of the filtered set's years (or the file's?). If filtered to 2010–2015, show 2010–2015. If a year in between has 0, show gap. I'll use min–max of years present in filtered set. Hmm, but what if the filter has no records? Then no chart — show "No records match". Actually, maybe better to use the file's year range so gaps are always visible relative to the whole file? The plan says "Records per year by mechanism: stacked bars for the current filter; every year from the first to the last appears, so empty years are visible gaps." I think first–last of the current filter. Hmm, but if you filter keyword "torture" and it matches 2008 and 2020 only, showing all years 2008–2020 with gaps shows when nothing matched. That's the point. OK: min–max of filtered years; if empty set, hide chart, show "No records match".

Actually wait — maybe use the file's overall min–max always? "empty years are visible gaps" — in the file, 2007–2026 with no records in some years. If I use the file range, gaps in the file are visible. If I use filtered range, gaps in filter are visible. I think the intent is the file's range is important ("dated 2007–2026, with no records in some years" was noted in "What I found in the data"). Hmm. But with a year filter applied (say 2010–2015), showing 2007–2026 would be wasteful. Compromise: if year filter active, use its range; otherwise use file min–max. Actually simpler and defensible: use min–max of years present in the filtered set, but if the year filter is set, that's within it. Hmm, but with a keyword filter, gaps between matching years would show, which is fine.

Let me just use: year range = [min, max] of years present in filtered records; every integer year in that range gets a bar (possibly zero height). If the year filter is active, clamp to the filter range. Actually if year filter is 2010–2015 and matches are only 2012, 2014, showing 2012–2014 misses that 2013 is a gap and 2010, 2011, 2015 are gaps. Hmm. Better: when year filter active, use the filter range; otherwise use file min–max (not filtered min–max). That way gaps are always fully visible. Let me do that: chartYearRange = yearFilter ? [yearFrom, yearTo] : [fileMinYear, fileMaxYear]. Good.

Tab 02 Records:
- Search field at top (same as keyword filter — "the same box as 01 Keyword"). Hmm, the keyword filter is in the rail. But tab 02 has "One search field across the top... the same box as 01 Keyword". So there are two inputs? Or the rail one is the same? "the same box as 01 Keyword" — meaning it's the same filter, synced. I'll render a search input on tab 02 that syncs with the rail keyword input. Both update the same filter state. Simpler: the tab-02 search input is the primary; when typed, update state and the rail input value. And vice versa. OK.

Actually wait — on tab 02, is the rail visible? Yes: "shown on tabs 01 and 02". So both the rail keyword box and the tab-02 search field exist and sync. Fine.

- Table columns: Date | Body | Symbol (linked) | Para. | First line | Recommending State (UPR only; dash otherwise). Sorted by date desc, then body, then paragraph number asc (numeric), then file order. Caption: "newest first"; clicking Date header reverses. Hmm — "clicking the Date header reverses it" — toggles sort direction (asc/desc). I'll make the Date header a button that toggles dateAsc flag. When ascending: date asc, then body, then para asc, then file order.

- Keyword matches highlighted with <mark>. Where? In the first-line column presumably (and maybe symbol). I'll highlight in the first line (and in symbol if it matches). Careful with HTML escaping. I'll escape then wrap matches. Since keyword can be multiple words, highlight each word. Use case-insensitive. To be safe, I'll do highlighting on the escaped text via regex with escaped pattern per word.

- 50 rows at a time, "Show 50 more" button.

- Row click expands in place: paragraph number large red, full text verbatim, labels (themes, sdgs with names, sdg_targets, affected_persons, section when present), "Copy citation" button, "Open the UN document" link. Also keyboard: Enter on row (row is focusable, role button or the row itself with tabindex). I'll make each row a clickable tr with tabindex="0", and an expansion tr below when open. One row open at a time? Plan doesn't say; "Details open in place (a clicked row expands)". I'll allow one open at a time (simpler) — actually, allowing multiple is fine too. Let me allow one at a time to keep DOM small... Actually multiple is fine and more useful. Hmm, with "Show 50 more", rows re-render on filter changes; keep expandedIds as a Set of record ids, preserved across pagination. I'll allow multiple.

Actually, re-rendering the table on every filter change: keep it simple, re-render whole tbody. Expanded rows tracked by id in a Set; re-render preserves them.

- Recommending State extraction: only UPR mechanism. Regex on trailing parenthesised run: `/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/`, then split with `/\((?:[^()]|\([^()]*\))*\)/g`, strip outer parens, trim. Accept as State if no comma and ≤60 chars. Several groups = several States; record counts once for each. If a group fails, record gets "State not found". Hmm — "A group is accepted as a State only if it has no comma and at most 60 characters; otherwise the record gets 'State not found'." So if any group fails, the record is "State not found"? Or that group is discarded? I read: if groups exist but none pass (or a group fails), the record is marked "State not found". Let me implement: extract groups; accepted = groups.filter(g => !g.includes(',') && g.length <= 60). If accepted.length > 0 → states = accepted. Else if there were groups but none accepted → "State not found". If no groups at all → no states (also "State not found"? For the check: "Number of UPR records with at least one State found, against the number of UPR records; the records without one are listed"). So both cases count as "without a State". In the table column, show states joined by ", " or "—" or "State not found"? The plan says the record "gets 'State not found'". I'll show "State not found" (in a muted style) when groups existed but failed the rule, and "—" when no parenthesis at all? Hmm, simpler: if no states extracted, show "—" in table but the check panel lists UPR records without states. Actually the plan explicitly says the record gets "State not found". Let me show "State not found" for UPR rows where extraction failed (either no parens or failed rule), and "—" for non-UPR rows. Wait: "Treaty-body and Special Procedures rows show a dash in this column." So non-UPR = dash. UPR with states = the states. UPR without = "State not found". OK.

State filter: select listing every State found with counts (in heading 02 of the rail, "when States are extracted" — i.e., if any UPR records have states, show the select). Filtering by state: record's extracted states include the chosen state. Also "and as a filter (a select listing every State found, with counts)". Counts — of the current filter or the whole file? "every State found, with counts" — I'll compute counts within the currently filtered set excluding the state filter itself (to avoid self-emptying). Hmm, that's complex. Simpler: counts within the filtered set with the state filter removed (i.e., other filters applied). That's the standard faceted approach. Or just counts in the whole file. Let me do counts over records passing all filters except the state filter. Similarly for body counts: "Body or mandate (body values present in the chosen mechanism, each with its count)" — count within mechanism-filtered set (excluding body filter). And type: "each value present" — present in the filtered set (excluding type filter). I'll do consistent faceting: for each filter facet, compute options+counts over records passing all other filters.

On tab 01: "a small 'see the States' link in the UPR tile opens a short list in place ('Ten States that made most recommendations to Kenya') with counts for the current filter." — country name from uhri.country. Note this appears in the UPR mechanism tile. But if the mechanism filter excludes UPR... the tile still shows (with 0 records). The link shows the top-10 states among current filtered set's UPR records. OK.

Tab 03 Check:
- "Check this dashboard" panel: one line per check, pass/fail with values.
  Checks:
  1. Record count: records.length vs Number(uhri.count).
  2. Partitions: counts per mechanism sum to record count; per body; per year. (Three checks or one line each? "Counts per mechanism, per body and per year each sum to the record count." I'll show three lines or one combined line each. Let me do separate lines: "Mechanism counts sum", "Body counts sum", "Year counts sum".)
  3. Type partition sums.
  4. Chart against table: each bar's value equals recomputed count via second loop; largest bar ≤ filtered count. This is a check on the current filter. Show as lines.
  5. Links: every doc_url starts with "https://docs.un.org/" and ends with its symbol (case-insensitive after decoding). List failures. Hmm — "ends with its symbol (compared case-insensitively after decoding)". Decoding: decodeURIComponent the url. Sample data shows doc_url "https://docs.un.org/en/CEDAW/C/AFG/CO/4" and symbol "CEDAW/C/AFG/CO/4". Note the URL may have the symbol with slashes — endsWith should work after decode. But some symbols contain characters like "(" — e.g., none here. OK. I'll decode both url and symbol (try/catch decode). Also strip trailing slashes. Failures listed (maybe capped at some number, "and n more"). 
  6. Paragraph numbers: share with number found, per mechanism; UPR expected 100%, lower shown as warning. Show per-mechanism lines.
  7. States found: UPR records with ≥1 state vs total UPR; list records without (symbol + what the parentheses held, capped).
  8. Duplicates and gaps: distinct id == count (list duplicates if any); duplicate text values count; records with no themes / no sdgs / no affected_persons counts ("not labelled").
- Random-sample label check: "Check 10 at random" button draws 10 cards from current filter with seeded mulberry32; seed box (default 1), "Draw again" and "Draw with this seed"; tally line "Themes: x fit, y don't, z unsure of 10 judged" with seed. Cards: one line each, one open at a time (accordion). Each card: symbol linked, paragraph number, full verbatim text, themes as chips, three buttons Fits / Doesn't fit / Unsure. Verdict stored per card (by record id + seed? just record id within current draw). One verdict per card (clicking changes it). Line above: "This is your judgement of the UN's labels; nothing is sent anywhere."

"Draw again" — increments/randomizes seed? "Draw again" draws a new random seed (e.g., Math.floor(Math.random()*1e9))? But then reproducibility... "Draw with this seed" uses the seed box value. "Draw again" could also just redraw with a new random seed and update the seed box. I'll make "Draw again" pick a new random seed, put it in the box, and draw. "Draw with this seed" reads the box. The seed is shown so a colleague can reproduce. OK.

Tab 04 Method & export:
- How each number computed, 5–6 plain sentences.
- "Download CSV of the current filter": visible columns (date, body, symbol, para, first line, state) plus full text and labels (themes, sdgs, sdg_targets, affected_persons, section). Preceded by comment lines: country, source, build date, filters applied, row count. Blob URL download. CSV escaping: quote fields, double quotes inside. Comment lines start with "#".
- "Copy summary": plain-text paragraph with headline numbers and top ten themes, for pasting into notes. Uses clipboard write with "Copied" confirmation.
- Data source, licence line, build date. Licence line — the data source; plan says "The data source, licence line and build date". UHRI data — I don't know its licence; I'll show source link. Hmm "licence line" — maybe just say what the source is. I'll include source linked and built date; for licence, I can't invent — maybe skip or say "see source for terms". Actually the footer has "Built on OHCHR UHRI data". For tab 04: "The data source, licence line and build date." I'll write: Source: uhri.source (linked). Build date: uhri.built. Licence: "OHCHR Universal Human Rights Index data; see the source for terms of use." That's honest without inventing.

Footer: "Built on OHCHR UHRI data · n records · source link", plus Credits line if shelf code used. I didn't copy shelf code, so no credits needed. Actually the design follows Analysis Function guidance but that's not code. The plan mentions design follows those sources — should I add a Credits line? The instruction says: "If you use code or wording from a 'Reference shelf excerpts' page that has an open licence... add Credits". I'm not using shelf code. But the plan's "Sources consulted" could be cited on tab 04 as method references. I'll list them on tab 04 as "Method notes follow..." with links. Links to external sites are fine as <a href> (they just won't be clicked offline, but that's OK — they're links, not resources). Hmm, actually the app must not load anything from the internet — links are fine, only resources/fetch are banned.

Now design:
- Warm off-white #f4f0e8 bg, near-black #1d1b18 text, thin rules #d9d2c3, accent red #9b2335.
- Serif for title, big numbers, figure titles: Georgia.
- Monospace uppercase letter-spaced 11–12px for labels, tabs, figure numbers.
- Sans 16px body/tables.
- Focus ring red visible.
- Charts: Chart.js 4 preloaded as window.Chart. Horizontal bars ranked, one colour (red at 80% — "the bars of FIG.01 (at 80%)"), value at end of bar. No gridlines clutter. FIG.02 stacked bars with mechanism colours.

Chart.js horizontal bar with value at end: use datalabels? Not available. Instead, I can draw the value in the tick label or use a custom plugin via afterDatasetsDraw. I'll write a small inline plugin to draw values at bar ends. Also for FIG.01, theme labels are long — put them as y-axis ticks (category). Chart.js handles that. Ranked: sort desc.

For clicking a bar in FIG.01 to add a theme filter: use onClick on chart element.

For FIG.02 stacked: x = years (categories), datasets = mechanisms with colors, stacked: true for both axes. Legend shown (labels). Value labels? Not necessary for stacked; maybe skip end labels there (plan says value at end of bar for the ranked horizontal bars). Keep FIG.02 simple with legend.

Responsive: maintainAspectRatio false with fixed height containers. Charts need width; container widths fine. Destroy and recreate charts on filter change, or update data. I'll destroy/recreate (simpler, avoids stale). Actually recreating on every keystroke debounce is OK.

Accessibility: tabs role="tablist", arrow-key navigation. Filter headings: buttons with aria-expanded, one open at a time. Matching count aria-live="polite". Rows: buttons with aria-expanded? Rows expand — make the row clickable with tabindex 0, aria-expanded, Enter/Space toggles.

Layout: header, then tablist, then main content: grid with left rail (narrow, ~260px) + content. Rail hidden filters on tabs 03/04: keep number, bar, chips; hide the three headings. Use hidden attribute plus CSS [hidden]{display:none!important}.

Header content:
- monospace label: "UHRI · KENYA" (country uppercase).
- Title serif large: "UN human rights recommendations and observations: Kenya" — from data: "UN human rights recommendations and observations: " + country. The plan gives exact wording: "UN human rights recommendations and observations: Kenya". Use country from data.
- One line: source (linked to source_url), n records, n documents, first–last year, built date, hint "dated by document".

Footer: one line small monospace: "Built on OHCHR UHRI data · n records · source link".

Now let me think about numbers formatting: thousands separators (toLocaleString('en-GB') or similar). Percentages one decimal.

Paragraph number extraction: `/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/`. E.g., "71. The Committee..." → "71". "144.43 Abolish..." → "144.43". Note "144.43 Abolish" — the regex `^(\d{1,3}(?:\.\d{1,3})?)\.?\s` on "144.43 Abolish" — \d{1,3} matches "144", then optional (?:\.\d{1,3})? matches ".43", then \.? no, then \s matches space. Good. On "71. The" → "71", then ".": the \.? matches, \s matches. Good. On "(g) Develop" → no match. Good.

Sorting rows: date desc, body asc (alphabetical), paragraph number asc (numeric — parse float of the extracted number; records without number... where do they go? "then paragraph number ascending (numeric, so 10 follows 9)". Records without a number — put them after numbered ones? Or treat as 0? Hmm. I'll sort: records with numbers by numeric value ascending; records without numbers go last within same date+body? Or first? Unclear. I'll put no-number records after numbered ones (nulls last) — actually within a document, lettered items usually come after numbered intro... whatever. I'll do: paraNum == null → Infinity... hmm, that puts them last. Fine. Then "then the order in the file" — stable sort with index tiebreaker.

Date desc: string comparison works for ISO dates.

First line: text up to 120 chars cut at last space before limit + "…". If text ≤ 120, whole text (no ellipsis? plan says "the first 120 characters, cut at a word, with '…'" — if shorter, show whole). "Very short or chopped texts... the first-line column may then be the whole text." So if ≤120 chars, show as is.

Keyword search: trimmed, lowercased; every word must occur as substring of text or symbol. So split on whitespace, each word must appear in (text + " " + symbol).toLowerCase()? "every word must occur as a substring of `text` or `symbol`" — each word must occur in text or in symbol (either). I'll check word appears in text.toLowerCase() or symbol.toLowerCase().

Now the "Check" tab details:

Check computations (on the whole file, not the filtered set — these are about the data):
1. Record count: records.length === Number(uhri.count) → pass "n = n" or fail.
2. Mechanism partition: sum of counts per mechanism == records.length.
3. Body partition.
4. Year partition.
5. Type partition.
6. Links check: iterate all records, decode doc_url (decodeURIComponent with try), check startsWith("https://docs.un.org/") and lowercase endsWith lowercase decoded symbol... wait "ends with its symbol (compared case-insensitively after decoding)". Symbols like "CEDAW/C/AFG/CO/4" — url "https://docs.un.org/en/CEDAW/C/AFG/CO/4". decodeURIComponent(url).toLowerCase().endsWith(symbol.toLowerCase()). Some urls might be like "http://undocs.org/..." (hrc data had that, but this is uhri). Failures listed with symbol. Cap list at maybe 10 with "and k more".
7. Paragraph numbers: share per mechanism with number found. UPR expected 100%; lower → warning styling (amber? no—use text saying warning). Colors: only red accent... I can use a muted style and the word "warning". Show as "UPR: 99.2% (expected 100%) — warning". Others just informational.
8. States found: count UPR records with ≥1 state vs total UPR; list records without, with symbol and "what the parentheses held instead" — i.e., the trailing text? I'll show the last ~60 chars of text. Cap list.
9. Distinct id count == record count (duplicate ids listed). Duplicate texts: count of text values appearing more than once (number of duplicate records). Records with no themes / no sdgs / no affected_persons — counts, "not labelled".
10. Chart vs table check: computed on the current filter at time of viewing tab 03. "Each bar's value equals the count recomputed by a second loop over the filtered records; the ten rows under the chart show the same values; the largest bar is not larger than the filtered count." I'll implement as: recompute top-ten themes via a second independent loop, compare with the chart data, and check max ≤ filtered count. Show pass/fail.

Random sample: 10 records from current filter. If filtered < 10, draw all (say "n of 10"). mulberry32 seeded. Sampling: shuffle indices with seeded RNG, take first 10. Cards: one line each (collapsed shows symbol + para + maybe first bit), one open at a time. Card content when open: symbol linked, para number, full text, theme chips, three buttons. Verdict per card stored in a map keyed by record id (reset on new draw). Tally updates.

CSV export: columns: date, body, mechanism, type, symbol, doc_url, paragraph, first line? The plan: "the visible columns plus the full text and labels". Visible columns: Date, Body, Symbol, Para., First line, Recommending State. Plus full text and labels: themes, sdgs, sdg_targets, affected_persons, section. Also maybe mechanism and type — "labels" could include them. I'll add mechanism, type too. Comment lines: "# Country: Kenya", "# Source: ...", "# Built: ...", "# Filters: keyword=...; mechanism=... etc" or "none", "# Rows: n". Then header row. Filename: "uhri-kenya-<something>.csv" — country slug + maybe "filter". 

Blob download: URL.createObjectURL(new Blob([csv], {type:'text/csv'})), a.download click, revokeObjectURL. That's local, fine.

Copy summary: plain-text paragraph with headline numbers and ten themes. E.g.: "UN human rights recommendations and observations: Kenya. N records from D documents, YYYY–YYYY (OHCHR UHRI, built DATE). Current filter: ... . Most frequent themes: Theme1 (n), Theme2 (n), ... ." navigator.clipboard.writeText with fallback (execCommand). Show "Copied" for 2s.

Copy citation: `symbol, para. N` or symbol alone; button label says "(no paragraph number in this extract)" when no para. Actually: "When no paragraph number was found in the text, it copies the symbol alone and the button's label says '(no paragraph number in this extract)'." So the button label itself includes that parenthetical. I'll make button text "Copy citation (no paragraph number in this extract)" in that case, else "Copy citation". "Copied" confirmation for 2s.

Now, mechanism tiles on tab 01: per mechanism: records, documents, latest year, share of filtered set. With colored dot (mechanism colours). UPR tile also has "see the States" link.

Let me also handle "The Type filter (all / each type value present) starts on 'all'" — the type select in rail heading 02 defaults to all.

Rail headings:
- 01 KEYWORD: text input, hint "literal match, not synonyms".
- 02 MECHANISM, BODY, TYPE: mechanism select, body select, type select, state select (if states extracted). Each closed until clicked, one open at a time.
- 03 YEARS AND SDG: year from/to selects, SDG select (goal number and name from sdg_names, only goals present).

Wait — order of headings: 01 Keyword, 02 Mechanism/body/type, 03 Years and SDG. The plan lists them in that order. OK.

Body select options: body values present in the chosen mechanism, with counts. If mechanism = all, all bodies. Type select: each value present (in filtered-by-other set). State select: "A State select joins this heading when States are extracted" — when any UPR states found.

Year from/to: distinct years sorted; if from > to, swap.

SDG select: goals present in data (in the filtered-by-others set? or whole file? "only goals present in the data" — the file). I'll use goals present in the file, with names from sdg_names. Label: "SDG 16 — Peace, justice and strong institutions".

Chips: for each active filter, a chip "keyword: torture ×", "mechanism: UPR ×", etc. Theme chip: "theme: X ×". Click × removes.

Now counts of clickable things: tabs (4) + on tab 01: rail headings (3) + clear all... plus chart bars (not counted), "see the States" link. Tabs 4 + rail 3 headings + clear-all = 8? Hmm, "No view shows more than about seven things to click (tabs, filter headings and buttons together)". Tabs 4 + 3 filter headings = 7, plus "Clear all" button = 8. Hmm. "about seven" — 8 is close. Clear all only shows when filters active? I could show "Clear all" only when there are active filters. Then default view: 4 tabs + 3 headings = 7. Good. When filters active, +chips and clear all — acceptable ("about seven").

Tabs: 4 tabs: 01 OVERVIEW · 02 RECORDS · 03 CHECK · 04 METHOD & EXPORT.

Now the tab switching: role tablist with tabs, arrow keys. Panels with role="tabpanel". Manage aria-selected, tabindex (-1 except active), keydown for arrows (Left/Right/Home/End).

Rail on tabs 03/04: keep number, bar, chips; hide headings. Use a wrapper div for filter headings with hidden toggling.

Let me now think about implementation structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>...</title>
<style>...</style>
</head>
<body>
<header>...</header>
<nav role="tablist">...</nav>
<div id="layout">
  <aside id="rail">...</aside>
  <main>
    <section id="panel-overview" role="tabpanel">...</section>
    <section id="panel-records" role="tabpanel" hidden>...</section>
    <section id="panel-check" role="tabpanel" hidden>...</section>
    <section id="panel-method" role="tabpanel" hidden>...</section>
  </main>
</div>
<footer>...</footer>
<script>...</script>
</body>
</html>
```

CSS: 
```css
[hidden]{display:none!important}
:root colors...
body { background:#f4f0e8; color:#1d1b18; font-family: system stack; margin:0; }
```

Let me write the CSS carefully with the editorial look:
- Header: padding, bottom border thin. Label mono uppercase. Title serif 28-34px. Meta line mono small.
- Tablist: border-bottom thin; tabs are buttons, mono uppercase letter-spaced, padding, active = red text + red bottom border (2px).
- Layout: display:grid; grid-template-columns: 260px 1fr; gap. On narrow screens, rail stacks? "Works on a laptop screen without horizontal scrolling" — I'll add a media query for <900px making rail full width above content.
- Rail: right border thin. Big number serif 44px. Share bar: 4px tall, track #d9d2c3, fill red. Chips: small, border thin, × button.
- Filter headings: button full width, mono label, aria-expanded indicator (+/−). Content: selects/inputs full width.
- Tiles: grid of tiles with thin rules (border-top), big serif numbers 40-56px.
- Figures: figure with mono "FIG.01" label, serif title, chart container height ~340px, table under.
- Table: full width, th mono small uppercase, borders thin horizontal only, numbers right-aligned. Caption.
- Row expand: expanded content in a tr > td colspan.
- Buttons: quiet, border thin, background transparent; primary actions red text or red border.
- mark: background highlight — use a light red? mark { background: #f3d9dc; } fine, one accent family.
- Focus: :focus-visible { outline: 2px solid #9b2335; outline-offset: 2px; }

Charts: 
FIG.01 horizontal bar:
```js
new Chart(ctx, {type:'bar', data:{labels, datasets:[{data, backgroundColor:'rgba(155,35,53,0.8)', ...}]}, options:{indexAxis:'y', ...plugins legend none, tooltip, onClick}});
```
Value at end: custom plugin:
```js
const valueLabels = {
  id:'valueLabels',
  afterDatasetsDraw(chart){
    const {ctx} = chart;
    ctx.save();
    ctx.font = '12px ...mono';
    ctx.fillStyle = '#1d1b18';
    chart.getDatasetMeta(0).data.forEach((bar,i)=>{
      const v = chart.data.datasets[0].data[i];
      ctx.fillText(fmt(v), bar.x + 6, bar.y + 4 /* baseline */);
    });
    ctx.restore();
  }
};
```
Need to make sure x-axis max leaves room: set suggestedMax maybe max*1.1. Or layout padding right. I'll add layout.padding.right ~ 48 and x suggestedMax = max + a bit.

Hide gridlines: scales.x.grid.display=false, ticks display? Keep x ticks (counts) but light. Actually "no gridline clutter" — I'll show x axis line and ticks minimal, hide grid. y ticks: theme names, font 13px sans, autoSkip false. Long labels — Chart.js truncates? It wraps. Chart container height: 10 bars * ~34px + margins = ~380px.

Bar thickness ~20.

Click handler: elements[0].index → theme = labels[i] → set theme filter → chip → rerender.

FIG.02 stacked:
```js
type:'bar', data:{labels: years, datasets: mechanisms.map(m=>({label:m, data: counts, backgroundColor: color, stack:'s'}))}, options:{scales:{x:{stacked:true}, y:{stacked:true}}}
```
Legend: show, position bottom, labels boxWidth 10, usePointStyle. Colors mapped: "Universal Periodic Review"→#c2410c, "Treaty bodies"→#0f766e, "Special Procedures"→#7c3aed. Other mechanisms (unlikely) → fallback gray. 

Now the code volume. This is a big app. Let me be organized and write it cleanly. Target maybe 1000–1300 lines. Let me draft.

State object:
```js
const state = {
  keyword:'', mechanism:'', body:'', type:'', state:'', yearFrom:'', yearTo:'', sdg:'', theme:'',
  dateAsc:false, visibleRows:50, expanded:new Set(), tab:'overview',
  sampleSeed:1, sampleRecords:[], verdicts:{}, sampleDrawn:false
};
```

Derived:
- allRecords
- statesByRecord: Map id → array of states or null (computed once for UPR)
- paraByRecord: Map id → para string or null (computed once)
- filtered(): apply filters.

Filter application order note: theme filter, keyword, mechanism, body, type, state, years, sdg.

Faceted counts for selects: compute base = records passing all filters except the facet in question.

Render pipeline: on any filter change → update everything visible (rail count/bar/chips, tab 01 tiles+charts, tab 02 table, tab 03 chart-check line? The check panel is mostly static file-level; chart-vs-table check uses current filter — recompute when tab 03 shown. I'll recompute checks on each render but they're cheap (2,264 records, fine). Actually simpler: recompute the check panel on render too. But the random sample cards should persist across filter changes? If filter changes, the sample is from the old filter... The plan says "Ten records drawn from the current filter". On filter change, I could keep the drawn cards (they were drawn from a past filter) — safer to keep them until redrawn, but the tally says "of 10 judged". Hmm. I'll keep drawn cards across filter changes (they're records; the reader drew them). But "Draw with this seed" uses current filter. Fine. Actually simpler: when filters change, keep the sample display as is. OK.

visibleRows reset to 50 on filter change. expanded: keep? If filter removes records, their expansion just won't render. Keep the Set.

Rendering approach: functions renderRail(), renderOverview(), renderRecords(), renderCheck(), renderMethod(); call relevant ones on state change. Charts: destroy existing before recreate (keep refs chart1, chart2).

Header numbers (static): computed once.

Now details for tab 02 table structure:

```html
<table>
<caption>...rows shown of rows matching · newest first (click Date to reverse)</caption>
<thead><tr>
  <th><button id="sortDate">Date ▾</button></th>
  <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col">Para.</th>
  <th scope="col">First line</th><th scope="col">Recommending State</th>
</tr></thead>
<tbody id="rowsBody"></tbody>
</table>
```
Caption text updated. Date header is a button toggling sort; aria-sort on th maybe. Keep simple: button with arrow indicator.

Row rendering: for each visible record:
```html
<tr class="rec" tabindex="0" aria-expanded="false" data-id="...">
 <td>2025-07-10</td><td>CEDAW</td>
 <td><a href="doc_url" target="_blank" rel="noopener">CEDAW/C/AFG/CO/4</a></td>
 <td class="num">54</td>
 <td class="first">…<mark>torture</mark>…</td>
 <td>—</td>
</tr>
```
Click on row (but not on link) toggles expand. Expanded row:
```html
<tr class="detail"><td colspan="6">
  <div class="para-no">54</div> (large red serif) or "no paragraph number"
  <p class="fulltext">…verbatim…</p>
  <div class="labels">themes chips, sdgs chips with names, sdg_targets list, affected_persons chips, section</div>
  <button copy citation> <a open doc>
</td></tr>
```

Verbatim text: escape HTML. Keyword highlight in first line: escape, then wrap matched words. Implementation: 
```js
function highlightWords(escapedText, words){
  // words: escaped-lowercase list
  if(!words.length) return escapedText;
  const pattern = words.map(escapeRegExp).join('|');
  return escapedText.replace(new RegExp('('+pattern+')','gi'), '<mark>$1</mark>');
}
```
But escaping changes text (& → &amp;) which could break word matches spanning entities. Edge case, acceptable. Words with regex-special chars escaped. OK. Also don't highlight inside... fine.

First-line computation: 
```js
function firstLine(text){
  if(text.length <= 120) return text;
  const cut = text.slice(0,120);
  const sp = cut.lastIndexOf(' ');
  return (sp > 60 ? cut.slice(0, sp) : cut) + '…';
}
```
Plan: "the first 120 characters, cut at a word". If no space, just cut at 120. OK.

Show more button after table: "Show 50 more" (hidden if all shown).

Search field on tab 02: input synced with rail keyword input. On input, debounce 300ms, update state.keyword, render.

Rail keyword input same.

Now mechanism tiles:
```html
<div class="tiles">
  <div class="tile">
    <div class="big">2,264</div>
    <div class="tile-note">records in the current filter (all types: 1,791 Recommendations, 471 Concerns/Observations, 2 Other)</div>
    <div class="how">How computed: count of records matching all active filters; the file holds 2,264.</div>
  </div>
  <div class="tile"> documents …</div>
  <div class="tile"> years …</div>
</div>
<div class="mech-tiles"> one per mechanism </div>
```

Type breakdown line: "1,791 recommendations · 471 concerns/observations · 2 other" spelled as in data. Use type values verbatim joined: `${count} ${type}` joined by " · ".

Each tile and figure has one-line "How this is computed" note. I'll add a `.how` mono small muted line.

FIG.01 note: "A record can carry several themes, so the bars add up to more than n. Source: OHCHR UHRI (file), current filter."

FIG.02 title: "Records per year by mechanism" with filter note.

The "see the States" list in UPR tile: link toggles a div in place: "Ten States that made most recommendations to {country}" with counts (from current filter's UPR records; each record counts once per state). Note "count of recommendations, not of influence".

Now the check tab layout:

```html
<section>
 <h2>How the app checks itself</h2>
 <p class="hint">Every check compares two values computed independently…</p>
 <ul id="checkList"> lines </ul>
 
 <h2>Random-sample label check</h2>
 <p>This is your judgement of the UN's labels; nothing is sent anywhere.</p>
 <button id="drawBtn">Check 10 at random</button> (then Draw again / Draw with this seed + seed box + tally)
 <div id="cards"></div>
</section>
```

Check line format: 
```html
<li class="pass">✓ Record count — file has 2,264 records; uhri.count says "2264". Match.</li>
<li class="fail">✗ Links — 3 of 2,264 doc_urls do not end with their symbol: …</li>
```
Use "✓" / "✗" or "PASS"/"FAIL" mono. I'll use mono tag "PASS"/"FAIL"/"WARN" in red or muted.

Random sample cards: each card is a div with a button header (collapsed line: "A/HRC/... · para 144.43 · first ~60 chars"), expanding shows full. One open at a time. Card body: symbol link, para number, full verbatim text, themes chips, three buttons Fits/Doesn't fit/Unsure (selected one highlighted), verdict stored. Tally above/below: "Themes: x fit, y don't, z unsure of 10 judged · seed 1".

mulberry32:
```js
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}
```
Draw: indices of filtered, seeded shuffle, take first min(10, n).

Method & export tab:
```html
<h2>Method</h2>
<p>…five/six sentences…</p>
<h2>Export</h2>
<button>Download CSV of the current filter (n rows)</button>
<button>Copy summary</button>
<p class="how">…what the CSV contains…</p>
<h2>Source</h2>
Source link, built date, licence note.
<p>Method notes follow … links.</p>
```

Method sentences (5–6):
1. Every number on this page is a count of records in the attached file, made by JavaScript in your browser; nothing is estimated and no language model is called.
2. The headline counts records, documents (distinct symbols) and the year range; the type breakdown uses the UN's own type labels, spelled as in the file.
3. Filters combine with AND: keyword (every word must appear, literally, in the text or symbol), mechanism, body, type, recommending State, year range and SDG goal.
4. Theme counts count each theme once per record carrying it, so they sum to more than the record count; percentages are of records, not labels.
5. Paragraph numbers are read from the start of each text ("71." or "144.43"); recommending States are read from the parentheses at the end of UPR texts only.
6. Dates are document dates, not the date a recommendation was made or accepted.

Copy summary text:
"UN human rights recommendations and observations: Kenya. 2,264 records from 31 documents, 2007–2026 (source, built …). Current filter: none / keyword "…", … — 1,234 records. Most frequent themes: A (n), B (n), … (top ten). Generated in the UHRI dashboard; counts are of records, themes sum to more."

CSV: comment lines:
```
# UN human rights recommendations and observations: Kenya
# Source: <source> (<source_url>)
# Built: <built>
# Filters: keyword="torture"; mechanism=UPR; ... (or "none")
# Rows: 1234
```
Header: Date,Body,Mechanism,Type,Symbol,Doc URL,Para.,First line,Recommending State,Full text,Themes,SDGs,SDG targets,Affected persons,Section

CSV escape: wrap in quotes, double internal quotes. Newlines inside text → keep within quotes (valid CSV).

Filename: `uhri-` + country slug + `.csv`.

Copy to clipboard helper:
```js
async function copyText(t, btn){ try{ await navigator.clipboard.writeText(t);}catch(e){ /* fallback textarea */ } flash(btn,'Copied'); }
```
Fallback: create textarea, select, document.execCommand('copy'). In sandbox clipboard may fail; fallback needed.

Now, header line: "source (linked), n records, n documents, first–last year, built date, hint 'dated by document'". Format: "OHCHR Universal Human Rights Index · 2,264 records · 31 documents · 2007–2026 · built 2026-11-14 · dated by document". Mono small.

Footer: "Built on OHCHR UHRI data · 2,264 records · source". Credits line: not needed (no shelf code used). I'll skip credits. Hmm, but design guidance from Analysis Function — not shelf code. Skip.

Wait, actually — should I include "Credits"? The system prompt: "If you use code or wording from a 'Reference shelf excerpts' page that has an open licence (MIT, Apache, BSD, ISC, CC BY), add a small 'Credits' line". I haven't used shelf excerpts. The mulberry32 function is public-domain-ish common code, not from the shelf. Skip credits. Actually, to be safe I could credit nothing. Fine.

Now write the tab switching with arrow keys:

```js
const tabs = [...document.querySelectorAll('[role="tab"]')];
function selectTab(i){ ... }
tablist.addEventListener('keydown', e=>{ ArrowRight/ArrowLeft/Home/End });
```

Each tab button controls panel via aria-controls; panels hidden toggling.

Rail visibility per tab: rail headings wrapper `#railFilters` hidden when tab is check or method. Also on those tabs the rail keeps number, bar, chips.

Filter heading accordion: three buttons; clicking toggles; only one open. Initially all closed ("each closed until clicked"). Hmm — "Three numbered headings, each closed until clicked, one open at a time". So initially all closed. OK.

Chips: container `#chips`; each chip: `<span class="chip">keyword: torture <button aria-label="Remove keyword filter">×</button></span>`.

Clear all: button top-right of FILTERS heading, shown only when active filters exist (or always but disabled? I'll show only when active — keeps click count low).

Now let me think about "no more than about seven things to click" on tab 02: tabs 4 + rail 3 headings = 7 + search box (input, not button?) — inputs count? "tabs, filter headings and buttons together". Search input is an input... borderline. Plus "Show 50 more", Date sort button, rows (not counted), chips' ×. It's "about seven" — fine.

Tab 03: tabs 4 + rail (no headings) + draw button = ~6. Cards' buttons many but they're content. Fine.

Now compute per-record derived data once:

```js
const R = uhri.records;
const paraOf = new Map(); // id -> para string|null
const statesOf = new Map(); // id -> string[] | 'NOT FOUND' marker? 
```
For states: for UPR records, extract. Store array; empty array means none found. Non-UPR: null (meaning not applicable).

State extraction:
```js
function extractStates(text){
  const m = text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
  if(!m) return [];
  const groups = m[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
  const names = groups.map(g=>g.slice(1,-1).trim());
  const ok = names.filter(n=>!n.includes(',') && n.length<=60);
  return ok.length? ok : [];
}
```
Wait, "otherwise the record gets 'State not found'" — if groups existed but none pass. But also if some pass and some fail? E.g., "(Cabo Verde) (art. 15);" — unlikely in UPR. The rule: accepted states = passing groups. If zero passing → "State not found". I'll return {states, notFound:bool}? For the check panel, "records without one are listed with their symbol, so the reader can see what the parentheses held instead" — I need to know the trailing text. I'll store for UPR records: states array + raw trailing groups (for diagnostics). Let me store statesOf: Map id → {states:[], hadParens:bool, raw:groups joined}. For the check listing, show raw groups.

Hmm wait, treaty-body texts end with "(art. 15)." — but we only apply to UPR, fine.

Also note: some UPR texts end with several states "(Cabo Verde) (Slovenia) (Togo);" — regex trailing run captures all three. Nested "Venezuela (Bolivarian Republic of)" — the group regex `\((?:[^()]|\([^()]*\))*\)` matches the outer with nested. Good.

Edge: text ends with "...(Gambia)." — trailing run = "(Gambia)", then `[;.]?\s*$` matches ".". Good. What about "…(Nigeria) and (Spain);"? The run regex `(?:\s*\(...\))+` — "(Nigeria) and (Spain)" — "and" between groups isn't \s* so the run would only capture "(Spain);" → one state. Fine, acceptable per regex spec.

Paragraph: 
```js
function paraNum(text){ const m = text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/); return m? m[1] : null; }
```

Numeric para for sorting: parseFloat.

Now filtering:

```js
function passes(r){
  if(state.theme && !(r.themes||[]).includes(state.theme)) return false;
  if(state.keyword){
    const words = state.keyword.trim().toLowerCase().split(/\s+/).filter(Boolean);
    const hay = (r.text+' '+r.symbol).toLowerCase();
    if(!words.every(w=>hay.includes(w))) return false;
  }
  if(state.mechanism && r.mechanism!==state.mechanism) return false;
  if(state.body && r.body!==state.body) return false;
  if(state.type && r.type!==state.type) return false;
  if(state.stateSel){
    const s = statesOf.get(r.id);
    if(!s || !s.states.includes(state.stateSel)) return false;
  }
  if(state.yearFrom && r.year < +state.yearFrom) return false;
  if(state.yearTo && r.year > +state.yearTo) return false;
  if(state.sdg && !(r.sdgs||[]).includes(+state.sdg)) return false;
  return true;
}
```

Name state fields carefully: state.state for the recommending State filter (confusing with the state object). I'll name filter keys: fKeyword, fMech, fBody, fType, fState, fYearFrom, fYearTo, fSdg, fTheme. State object `S`.

Faceted option lists:
```js
function facet(fn){ return R.filter(r=>{ /* all filters except fn */ }); }
```
I'll write passes(r, skip) where skip is a facet key to ignore.

Body options: from records passing all filters except body AND constrained by mechanism? "Body or mandate (body values present in the chosen mechanism, each with its count)". If mechanism filter is set, body options are bodies in that mechanism. Since mechanism filter is applied in passes(except body), bodies from other mechanisms are excluded anyway. Good — faceting handles it.

Type options: "each value present" — present in filtered-minus-type set. Good.

State options: every State found — in the filtered-minus-state set? "a select listing every State found, with counts". I'll facet similarly.

Year options: "two selects of the distinct years" — distinct years in the file? Or filtered? If faceted, selecting yearFrom would shrink years for yearTo... Let me use distinct years of the file (static), and swap if reversed. Hmm, but if filtered to mechanism with fewer years, year selects showing all file years is fine — selecting an empty year yields 0 matches, which the app handles ("No records match"). I'll use file years for stability. Actually plan says "two selects of the distinct years" — ambiguous; file years is the natural reading of the whole plan section (rail describes the data). Go with file distinct years.

SDG options: "goal number and name from sdg_names, only goals present in the data" — the file. Static. Good.

Now the swap logic: on change of yearFrom/yearTo, if both set and from > to, swap values.

Render rail:
```js
function renderRail(){
  countEl.textContent = fmt(n);
  ofEl.textContent = 'of '+fmt(N)+' in the file';
  bar width = (n/N*100)+'%';
  chips...
  clearAll hidden = no active filters
  // update select options (facet counts)
}
```

Facet option refresh: rebuild body/type/state select options on each render (preserving selection if still valid). Mechanism select static (all values in file). Also the keyword inputs' values synced (don't overwrite while typing — the rail input triggers; the tab-02 search input: update only if different and not focused? If user types in tab-02 box, debounce updates state; then render syncs rail box value. If user types in rail box, sync tab-02 box. Since I set .value only when different, and typing sets it... it's fine to set both on render since the debounce fires after typing stops. But careful: setting input value while user types would reset cursor — only set if input.value !== S.fKeyword.)

Overview render:
- tiles: filtered set stats.
- type breakdown line.
- mechanism tiles: for each mechanism present in the FILE (all three), show records/docs/latest year/share. If mechanism filter set to one, others show 0? Show all mechanisms as in file (they're tiles describing each mechanism within current filter). Yes.
- UPR tile: "see the States" toggle.
- FIG.01 + table.
- FIG.02.

Empty filter: tiles show 0, chart area shows "No records match" text (replace chart canvas with message; destroy charts).

Chart heights: FIG.01 360px; FIG.02 300px.

Records render:
- caption: "Showing 50 of 1,234 matching records · newest first (click Date to reverse)". Plus filter context? The rail shows it. Caption: rows shown of rows matching. If filter matches nothing: "No records match the current filters."
- tbody rows.
- Show more button.

Sorting comparator:
```js
function cmp(a,b){
  const d = S.dateAsc ? (a.date<b.date?-1:a.date>b.date?1:0) : (a.date>b.date?-1:a.date<b.date?1:0);
  if(d) return d;
  if(a.body!==b.body) return a.body<b.body?-1:1;
  const pa = paraNumOf(a), pb = paraNumOf(b); // numeric or null
  const na = pa==null? Infinity:parseFloat(pa), nb = pb==null? Infinity:parseFloat(pa)... careful
  if(na!==nb) return na-nb;
  return idxOf a - idx b; // file order — keep original index map
}
```
Precompute index map id→i.

Expansion: row click handler on tbody (event delegation): if e.target closest('a') or button, ignore. Toggle id in expanded set, re-render tbody (or toggle DOM). Re-render tbody is simplest but loses scroll... toggling classes in DOM is better. I'll do DOM toggling: each rendered row pair exists; expanded ones rendered with detail row visible; toggle by inserting/removing detail row. With re-render on filter change, rebuild all. For toggle, I'll just re-render the tbody (2000 rows max but only 50 shown — fine) — but focus loss on the clicked row. Hmm, keyboard Enter on row: after re-render, refocus the row. I'll handle: after render, if lastToggledId, focus that row. Or simpler: toggle detail row in place without full re-render:

```js
function toggleDetail(tr){
  const id = tr.dataset.id;
  if(S.expanded.has(id)){ S.expanded.delete(id); tr.nextElementSibling?.remove(); tr.setAttribute('aria-expanded','false'); }
  else { S.expanded.add(id); tr.insertAdjacentHTML('afterend', detailHTML(rec)); tr.setAttribute('aria-expanded','true'); }
}
```
Detail row built from record. Good, no re-render needed. On full re-render, render detail rows for expanded ids.

aria: tr tabindex 0, role? Rows with aria-expanded — not standard on tr but acceptable; add keydown Enter/Space.

Copy citation button inside detail: event delegation on tbody for button.copy and check cards separately.

Now tab 03 checks — implement as list of {label, status, detail} computed by functions. Let me enumerate lines:

1. "Record count" — records.length vs Number(uhri.count).
2. "Mechanism counts sum to the record count" — sum vs total.
3. "Body counts sum" — sum vs total.
4. "Year counts sum".
5. "Type counts sum".
6. "Links" — every doc_url starts with https://docs.un.org/ and ends with symbol. Failures listed (cap 8, "and k more"). Note: doc_url might be empty in some records (hrc sample had empty). Handle: failure.
7. "Paragraph numbers" — per mechanism share; separate lines or one line with three shares. "Share of records with a number found, per mechanism; UPR is expected at 100%, and a lower figure is shown as a warning". I'll do three lines: "Paragraph numbers — Treaty bodies: 45.2% of records have a number at the start of the text." UPR line: warn if <100.
8. "States found" — "x of y UPR records name at least one State in parentheses"; list the ones without (cap 10): "A/HRC/…/… — parentheses held: '(art. 15)'".
9. "Duplicate ids" — distinct ids vs count.
10. "Duplicate texts" — n texts appear more than once (m records involved).
11. "Records not labelled" — no themes: n; no sdgs: n; no affected_persons: n. Three lines or one. "records with no themes, no sdgs, no affected_persons, each shown as 'not labelled'". I'll do one line each or combined. Let me do one line: "Missing labels — themes: n records; SDGs: n; affected persons: n." Hmm "one line per check". I'll make it three short lines under one heading? Keep one line: "Records not labelled — no themes: 15; no SDGs: 448; no affected persons: 408." Fine.
12. "Chart against table" (current filter) — recompute top themes with second loop; compare to chart data; and largest bar ≤ filtered count. Lines: "FIG.01 bars match a second, independent count" pass/fail; "Largest theme count (691) ≤ matching records (2,264)" pass/fail.

Pass mark: "✓ PASS" in green? Only one accent (red)... "a pass mark or a red 'check failed'". So pass is neutral (ink), fail is red. Use mono "PASS" muted / "FAIL" red / "WARN" maybe amber? Avoid extra colours: WARN in red too but worded as warning? The plan: "a lower figure is shown as a warning, not an error". I'll use text "warning" styled red but labelled warning. Hmm, red means failure... I'll use a middle tone: #8a6d1f? That adds a colour. Let me use the red for FAIL only, and WARN in the near-black with the word "warning". Actually let me just use muted ink for WARN with explicit word. Fine.

Sample cards: 

```html
<div class="card">
  <button class="card-head" aria-expanded>SYM · para 144.43 · first 60 chars…</button>
  <div class="card-body" hidden>
    <a>SYM</a> · para <span class="red">144.43</span> · date
    <p>full verbatim text</p>
    <div class="chips">themes</div>
    <div class="verdict"> Fits / Doesn't fit / Unsure buttons </div>
  </div>
</div>
```
One open at a time: opening one closes others.

Verdicts: S.verdicts[recordId] = 'fit'|'no'|'unsure'. Tally computed from sample records.

Tally: "Themes: x fit, y don't, z unsure of 10 judged · seed 1". Also note: "The tally is your judgement, not the app's; the UN's labels are unchanged."

Draw logic:
```js
function drawSample(seed){
  const list = filtered();
  const rng = mulberry32(seed);
  const idx = list.map((r,i)=>i);
  for(let i=idx.length-1;i>0;i--){ const j=Math.floor(rng()*(i+1)); [idx[i],idx[j]]=[idx[j],idx[i]]; }
  S.sampleRecords = idx.slice(0,10).map(i=>list[i]);
  S.verdicts = {};
  S.sampleSeed = seed; seedBox.value = seed;
  renderSample();
}
```
"Check 10 at random" initial button → after first draw, show "Draw again" (new random seed) + seed box + "Draw with this seed". I'll structure: seed input always visible with the two buttons after first draw; before first draw just the "Check 10 at random" button (which uses the seed box value, default 1? "the seed is shown in a box, default 1"). Hmm: "'Check 10 at random' draws the cards (then 'Draw again' and 'Draw with this seed', the seed box and the tally)". So initially: button "Check 10 at random". After drawing: buttons become "Draw again" and "Draw with this seed", seed box appears. "Check 10 at random" uses seed... default 1? Or random? I'll make "Check 10 at random" use the seed box default 1 — wait then "Draw with this seed" is same. Alternative: "Check 10 at random" picks a random seed. Hmm, "Draw again" should give a different sample — random seed. Let me do: "Check 10 at random" → random seed (stored, shown in box). "Draw again" → new random seed. "Draw with this seed" → parse box (integer). Default box value 1. That works and seed always shown for reproduction.

Hmm, but reproducibility of the FIRST draw: seed shown in box after draw, so a colleague can re-draw with that seed. Good.

Now the Method & export tab. CSV generation:

```js
function csvEsc(v){ v = v==null?'':String(v); return '"'+v.replace(/"/g,'""')+'"'; }
```
Comment lines start with "# " — not quoted.

Filters description for comments: build array of "key=value" for active filters.

Copy summary:

```js
function summaryText(){
  const n = filtered().length;
  const top = topThemes(10);
  ...
  return `UN human rights recommendations and observations: ${country}. ${fmt(N)} records from ${fmt(docs)} documents, ${minYear}–${maxYear} (source: ${source}, built ${built}). Current filter${desc}: ${fmt(n)} records. Types: ... . Ten most frequent themes: ${top.map(t=>`${t.theme} (${t.count})`).join('; ')}. A record can carry several themes. Counts made in the browser from the attached file; nothing estimated.`;
}
```

Now, some tricky bits:

Chart.js stacked with years including zero years: labels = range; data zeros. Bar shows nothing for zero — visible gap. Good.

FIG.01 clicking adds theme filter — but also the table under chart could have clickable rows? Plan says clicking a bar. Table rows not clickable. OK.

Colors on tiles: mechanism dot colored (UPR #c2410c etc.), always with label. Fine.

Legend for FIG.02: Chart.js legend displays labels. Good.

Number formatting: `fmt = n => n.toLocaleString('en-GB')`. Percent: `(100*x/y).toFixed(1)+'%'`.

Share bar: width % of file.

Focus ring: `:focus-visible{outline:2px solid #9b2335; outline-offset:2px}` plus for chart canvas? not needed.

Let me also handle the "hint" texts: mono small next to things:
- keyword: "literal match, not synonyms"
- matching count: "of N in the file"
- first-line column? no.
- caption: "newest first — click Date to reverse"
- charts: "How this is computed" lines.

Header hint "dated by document" — include in meta line.

Now, let me also double check the tab panels' content per plan:

Tab 01: headline tiles, mechanism tiles, FIG.01 + table, FIG.02. "Nothing else on this tab."

Tab 02: search field, table, show more.

Tab 03: check panel + sample check.

Tab 04: method text, export buttons, source/licence/build.

Footer.

Now — the rail on tab 02 shows filters, and the search field on tab 02 is "the same box as 01 Keyword". So on tab 02, the rail keyword heading exists AND a big search field on top. Both sync. OK.

One more consideration: "Fifty rows at a time with 'Show 50 more'". S.visibleRows increments by 50.

Also table caption should include filter context? "The caption gives rows shown of rows matching." OK.

Edge: keyword highlight in first line — highlight words from S.fKeyword.

Now write it all. Let me be careful with the amount of code and keep it organized. I'll write helper `el(html)` maybe. Mostly template strings + innerHTML.

Security/escaping: `esc = s => String(s).replace(/[&<>"']/g, c=>({...}[c]))`.

Let me now also design the tile "share of the filtered set": mechanism tile shows "n% of the matching records". With big number = record count of that mechanism in filtered set. Under: "d documents · latest YYYY · x% of matching records". How-computed note per tile — that's a lot of notes; plan says "Every tile and figure has a one-line 'How this is computed' note." I'll add a single note line per tile group or per tile. Per tile: small mono line. OK, do per tile but short: "records in this mechanism, current filter".

Actually to reduce clutter: one note line under the headline row ("Counts are of records matching all active filters; documents are distinct symbols; years are min–max of document dates."), and per mechanism tile small notes. The plan says every tile — I'll give each a short mono note.

Layout of tiles: CSS grid, tiles separated by border-top thin rules (editorial). Big numbers serif 40-48px.

Mechanism tiles: 3 columns row.

Let me now also handle mechanism colours map:
```js
const MECH_COLORS = {'Universal Periodic Review':'#c2410c','Treaty bodies':'#0f766e','Special Procedures':'#7c3aed'};
```
Fallback '#6b6459'.

FIG.01 bar color: 'rgba(155,35,53,0.8)' (red at 80%).

Value label plugin for FIG.01.

Chart fonts: Chart.defaults.font.family = sans; size 13.

Let me think about the FIG.01 y labels: long theme names — set ticks callback to truncate to ~48 chars? Chart.js wraps automatically? Category axis labels can be long; container height fixed 360px with 10 bars is fine; width — labels take left space. I'll truncate labels to 60 chars with "…" and show full name in table below (and tooltip). Actually plan wants table under chart with same rows — full names there. Truncation in chart acceptable? "horizontal text" required. Chart.js does not wrap; long labels get cut off or squeeze plot. I'll truncate at 44 chars. Hmm, theme names like "Minorities/ racial, ethnic, linguistic, religious or descent-based groups" (74 chars). Truncate to 40 + "…". Tooltip shows full. OK.

Now the "see the States" in-place list on tab 01:

```html
<button class="linkish" id="statesLink">see the States</button>
<div id="statesList" hidden>
  <h3 class="mono">TEN STATES THAT MADE MOST RECOMMENDATIONS TO KENYA</h3>
  <ol> State — n ... </ol>
  <p class="how">Count of UPR records in the current filter naming that State; a record naming two States counts once for each. A count of recommendations, not of influence.</p>
</div>
```
Compute top 10 states by count over filtered UPR records.

Note: the country name in heading — "Ten States that made most recommendations to {country}".

Also this heading says "TEN STATES..." but if fewer states exist, show what's there. Title as given.

Now — link check: "ends with its symbol (compared case-insensitively after decoding)". Some doc_urls might end with "/Add.1" while symbol "E/C.12/KEN/CO/1/Add.1" — fine. But URL might be "https://docs.un.org/en/CEDAW/C/AFG/CO/4" vs symbol "CEDAW/C/AFG/CO/4" — good. Possible mismatch: url ends with trailing slash → strip trailing "/". I'll normalize: `u = decodeURIComponent(url).replace(/\/+$/,'')`. And symbol decode too? Symbols rarely have %. Just lowercase both.

Hmm wait — what if doc_url contains the symbol but with different slash encoding? Keep simple.

Now let me count select options building:

Mechanism select (static): all + each mechanism in file with count? Plan: "Mechanism (all / each value)". No counts mentioned for mechanism; counts for body. I'll include counts for all for consistency? Plan only says body has counts. Keep mechanism without counts... adding counts is harmless but adds click-free info. I'll add counts to mechanism and type too — it's informative text in options, not extra clicks. Fine.

Actually careful: option label "CEDAW (214)" — when user selects body "CEDAW", filter state stores "CEDAW". Parsing value vs label: use value attribute = raw value, label text separate. `<option value="CEDAW">CEDAW — 214</option>`. Good.

Body options rebuilt per render (facet). Preserve selection: if current fBody not in options (e.g., 0 matches), keep it? If user selected body then set mechanism excluding it — body facet options would exclude it and filtered = 0. Hmm. Keep selection but option disappears from select → select shows blank. Better: when rebuilding, if fBody not among options, reset fBody to ''? That silently removes a filter... but avoids a broken state. Actually facet computation excludes the body filter itself, so fBody's own body always appears IF there are records of that body passing other filters (mechanism). If mechanism filter excludes that body, the body filter yields 0 matches — consistent. I'll include the currently-selected value in options even with count 0, to keep the chip accurate. Simpler: options = values with counts from facet; if fBody set and not present, append it with count 0. OK.

Same for type and state.

Year from/to selects: distinct file years. SDG select: goals in file with names.

Now: chips list build:
```js
function activeFilters(){
  const out=[];
  if(S.fKeyword) out.push(['keyword', 'keyword: “'+S.fKeyword+'”']);
  if(S.fMech) out.push(['mech','mechanism: '+S.fMech]);
  ...
  if(S.fTheme) out.push(['theme','theme: '+S.fTheme]);
  return out;
}
```
Chip remove: clears that filter, re-render.

Clear all: reset all filters (keep visibleRows? reset to 50; keep expanded).

Render flow: `applyFilters()` → recompute filtered cache → renderRail + renderOverview + renderRecords + update check chart line? The check tab's chart-vs-table check uses current filter; recompute when rendering tab 03 (on tab switch and on filter change if tab 03 active). I'll just recompute checks whenever renderCheck is called; call renderCheck on filter change only if check tab active (or always — it's cheap; but the checks list re-render would wipe... it has no interactive state except sample cards which I keep separate. Sample cards persist in their own container; renderCheck rebuilds only the checks list. Let me split: checksList container (rebuilt on render) and sampleSection (rebuilt only on draw/verdict). Verdict buttons update via delegation without full rebuild? Simpler: renderSample() rebuilds cards; verdict click updates S.verdicts then updates tally text and button states — I can re-render sample section (cheap, 10 cards) but that collapses open card... Keep open card id in S.openCard. Fine, re-render sample with open card preserved.

Actually simpler: on verdict click, just update classes on the three buttons and the tally line — no rebuild. I'll do targeted updates. And card open/close toggles hidden attributes. OK.

Now — one important thing: tab switching should (re)render the tab's content lazily for charts (Chart.js needs visible canvas for correct sizing? Chart.js handles hidden canvases poorly — rendering a chart in a hidden panel gives zero size). So create/refresh charts when tab 01 becomes visible. I'll call renderOverview() on tab switch to overview. Similarly on filter change: if overview tab active, renderOverview; else mark dirty and render on switch. Simpler: always renderOverview but skip chart creation if panel hidden, set a flag needsChart, and on tab switch render. Let me implement: renderOverview() updates tiles/tables always (cheap), and charts only if overview visible; on switching to overview, refresh charts. Similarly records table — can render while hidden fine (no canvas).

Implement `refreshCharts()` guard.

Also window resize: charts responsive true by default, Chart.js handles.

Now writing all the HTML skeleton with ids. Let me draft the full file.

Also remember: `[hidden]{display:none!important}` in CSS.

Language: English (the plan is English; user wrote in English).

Title: "UN human rights recommendations and observations: {country}" — computed; but <title> static-ish: set via JS `document.title`.

Let me write out the code now, section by section.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UHRI dashboard</title>
<style>
[hidden]{display:none!important}
:root{
  --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335;
  --muted:#6f675c;
  --serif:Georgia,"Times New Roman",serif;
  --mono:ui-monospace,Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--paper);color:var(--ink);font:16px/1.55 var(--sans)}
a{color:var(--red)} wait — links red? Accent is red; links in red is consistent. Yes a{color:var(--red);text-decoration:none;border-bottom:1px solid rgba(155,35,53,.35)} maybe underline. Keep: color red, underline.
```

Hmm links: "Every row that shows a document has its symbol, linked to doc_url in a new tab." Color — use ink with underline, or red. I'll use red text without underline but underline on hover... Contrast red #9b2335 on #f4f0e8: contrast ~7:1, fine. Use red with underline dotted? Simple: red, no underline, hover underline.

Focus: `:focus-visible{outline:2px solid var(--red);outline-offset:2px}`.

Now header:

```html
<header>
  <div class="mono label">UHRI · <span id="hCountry"></span></div>
  <h1 id="hTitle"></h1>
  <p class="mono metaline" id="hMeta"></p>
</header>
```

Tablist:
```html
<nav>
 <div class="tablist" role="tablist" aria-label="Dashboard sections">
  <button role="tab" id="tab-overview" aria-controls="panel-overview" aria-selected="true" class="mono">01 OVERVIEW</button>
  ...
 </div>
</nav>
```

Layout:
```html
<div class="layout">
 <aside class="rail" aria-label="Filters">
   <div class="rail-head mono">FILTERS <button id="clearAll" class="linkish mono" hidden>Clear all</button></div>
   <div class="bignum-wrap">
     <div class="bignum" id="matchCount" aria-live="polite">0</div>
     <div class="mono muted" id="matchOf"></div>
     <div class="bar"><div class="bar-fill" id="barFill"></div></div>
     <div class="mono muted" id="barNote"></div>
   </div>
   <div id="chips" class="chips"></div>
   <div id="railFilters">
     <div class="fgroup">
       <button class="fhead mono" aria-expanded="false" data-f="kw">01 KEYWORD</button>
       <div class="fbody" hidden>
         <input id="kwRail" type="search" placeholder="e.g. torture" aria-label="Keyword">
         <div class="mono hint">literal match, not synonyms</div>
       </div>
     </div>
     <div class="fgroup">
       <button class="fhead mono" aria-expanded="false" data-f="mbt">02 MECHANISM, BODY, TYPE</button>
       <div class="fbody" hidden>
         <label class="mono">Mechanism</label>
         <select id="selMech"></select>
         <label class="mono">Body or mandate</label>
         <select id="selBody"></select>
         <label class="mono">Type</label>
         <select id="selType"></select>
         <div id="stateWrap" hidden>
           <label class="mono">Recommending State</label>
           <select id="selState"></select>
         </div>
       </div>
     </div>
     <div class="fgroup">
       <button class="fhead mono" aria-expanded="false" data-f="ys">03 YEARS AND SDG</button>
       <div class="fbody" hidden>
         <label>Year from</label><select id="selFrom"></select>
         <label>Year to</label><select id="selTo"></select>
         <label>SDG</label><select id="selSdg"></select>
       </div>
     </div>
   </div>
 </aside>
 <main>... panels ...</main>
</div>
```

Accordion: only one open. data-f keys.

Panels:

Overview:
```html
<section id="panel-overview" role="tabpanel" aria-labelledby="tab-overview">
  <div class="tiles" id="headlineTiles"></div>
  <div class="tiles" id="mechTiles"></div>
  <figure>
    <div class="mono figno">FIG.01</div>
    <h2 class="figtitle" id="fig1Title"></h2>
    <div class="chart-box" id="fig1Box"><canvas id="fig1"></canvas></div>
    <p class="how" id="fig1How"></p>
    <table class="data" id="themeTable">...</table>
    <p class="source mono">Source: ...</p>
  </figure>
  <figure>
    <div class="mono figno">FIG.02</div>
    <h2 class="figtitle" id="fig2Title"></h2>
    <div class="chart-box"><canvas id="fig2"></canvas></div>
    <p class="how" id="fig2How"></p>
    <p class="source mono">Source: ...</p>
  </figure>
</section>
```

Records:
```html
<section id="panel-records" role="tabpanel" aria-labelledby="tab-records" hidden>
  <div class="searchbar">
    <input id="kwMain" type="search" aria-label="Search records">
    <span class="mono hint">literal match, not synonyms — same as the keyword filter</span>
  </div>
  <table class="records">
    <caption id="recCaption"></caption>
    <thead><tr>
      <th scope="col"><button id="sortDate" class="thsort">Date <span id="sortArrow">▾</span></button></th>
      <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th>
      <th scope="col">First line</th><th scope="col">Recommending State</th>
    </tr></thead>
    <tbody id="recBody"></tbody>
  </table>
  <button id="moreBtn" class="more">Show 50 more</button>
</section>
```

Check:
```html
<section id="panel-check" role="tabpanel" aria-labelledby="tab-check" hidden>
  <h2 class="serif">How the app checks itself</h2>
  <p class="mono hint">Each line compares two values computed independently. Nothing is hidden.</p>
  <ul id="checkList" class="checks"></ul>
  <h2 class="serif">Check the UN's labels on a random sample</h2>
  <p>The labels are the weakest part of this data. Draw ten records, read each paragraph, and judge whether its theme labels fit. This is your judgement of the UN's labels; nothing is sent anywhere.</p>
  <div class="sample-controls">
    <button id="drawBtn" class="btn">Check 10 at random</button>
    <span id="drawMore" hidden>
      <label class="mono">seed</label><input id="seedBox" type="number" value="1" min="0">
      <button id="drawAgain" class="btn">Draw again</button>
      <button id="drawSeed" class="btn">Draw with this seed</button>
    </span>
  </div>
  <p class="mono" id="tally" aria-live="polite"></p>
  <div id="cards"></div>
</section>
```

Method:
```html
<section id="panel-method" role="tabpanel" aria-labelledby="tab-method" hidden>
  <h2 class="serif">Method</h2>
  <p id="methodText"></p>
  <h2 class="serif">Export</h2>
  <button id="csvBtn" class="btn">Download CSV of the current filter</button>
  <button id="sumBtn" class="btn">Copy summary</button>
  <p class="how" id="csvNote"></p>
  <h2 class="serif">Source</h2>
  <p id="sourceNote"></p>
  <p class="mono muted">Method notes follow the UK Government Analysis Function guidance on charts and tables, the Dag Hammarskjöld Library's citation advice, and OHCHR's Human Rights-Based Approach to Data.</p>
</section>
```

Footer:
```html
<footer class="mono">Built on OHCHR UHRI data · <span id="fCount"></span> records · <a id="fSource" ...></a></footer>
```

Now JavaScript. Let me write it fully and carefully.

```js
(function(){
'use strict';
const U = window.WORKSHOP_DATA && window.WORKSHOP_DATA.uhri;
if(!U || !Array.isArray(U.records)){ document.getElementById('hTitle').textContent='No data attached.'; return; }
const R = U.records;
const N = R.length;
const COUNTRY = U.country || '—';
const SDG_NAMES = U.sdg_names || {};

// helpers
const $ = id => document.getElementById(id);
const esc = s => String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt = n => Number(n||0).toLocaleString('en-GB');
const pct1 = (a,b)=> b? (100*a/b).toFixed(1)+'%' : '0.0%';
const rxEsc = s => s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');

// derived per record
const idxOf = new Map(R.map((r,i)=>[r.id,i]));
function paraNum(t){ const m=String(t||'').match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/); return m?m[1]:null; }
const paraOf = new Map(), paraNumOf... 
```

Wait — the regex `^(\d{1,3}(?:\.\d{1,3})?)\.?\s` — on text "1. A clean..." fine. On "144.43 Abolish" → matches "144.43" then `\s`. But greedy: `\d{1,3}` = "144", `(?:\.\d{1,3})?` = ".43", `\.?` nothing, `\s` space. 

Careful: text "71. The" → `\d{1,3}`="71", optional group: next char "." then needs digits — ". The" → `\.\d` fails, so group not taken; `\.?` takes ".", `\s` space. 

But "10." style where text is "10. Text" fine. What about a text starting "2020. Something"? \d{1,3} max 3 digits "202" then `\.`? next char "0" not "."; optional group needs "."; fail... backtrack: \d{1,3} could match "202"? then fail; "20" then ". "? next char is "2"... Actually "2020. " — digits "202", then need optional `.` — next is "0", group fails, `\.?` optional no, `\s` — next "0" not space → fail; backtrack "20" → same issue; "2" → "0" not ./space → fail. No match. Good, per spec.

States extraction per plan:
```js
function extractStates(text){
  const m = String(text||'').match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
  const groups = m ? (m[1].match(/\((?:[^()]|\([^()]*\))*\)/g)||[]) : [];
  const names = groups.map(g=>g.slice(1,-1).trim()).filter(Boolean);
  const ok = names.filter(n=>!n.includes(',') && n.length<=60);
  return {states: ok, raw: names};
}
```
Store statesOf = Map(id → {states, raw}) for UPR only.

```js
const statesOf = new Map();
let anyStates = false;
for(const r of R){
  if(r.mechanism==='Universal Periodic Review'){
    const s = extractStates(r.text);
    statesOf.set(r.id, s);
    if(s.states.length) anyStates = true;
  }
}
const ALL_STATES = ... // counts over whole file: Map state->count
```
State list for select: sorted by count desc then alpha. Facet counts at render.

Filter state:
```js
const S = {
  fKeyword:'', fMech:'', fBody:'', fType:'', fState:'', fYearFrom:'', fYearTo:'', fSdg:'', fTheme:'',
  dateAsc:false, visible:50, expanded:new Set(),
  tab:'overview', statesOpen:false,
  sample:null, sampleSeed:1, verdicts:{}, openCard:null, drawn:false
};
```

filtered(skip):
```js
function passes(r, skip){
  if(skip!=='theme' && S.fTheme && !(r.themes||[]).includes(S.fTheme)) return false;
  if(skip!=='keyword' && S.fKeyword){
    const ws = S.fKeyword.toLowerCase().split(/\s+/).filter(Boolean);
    if(ws.length){
      const hay = (String(r.text||'')+' '+String(r.symbol||'')).toLowerCase();
      for(const w of ws) if(!hay.includes(w)) return false;
    }
  }
  if(skip!=='mech' && S.fMech && r.mechanism!==S.fMech) return false;
  if(skip!=='body' && S.fBody && r.body!==S.fBody) return false;
  if(skip!=='type' && S.fType && r.type!==S.fType) return false;
  if(skip!=='state' && S.fState){
    const st = statesOf.get(r.id);
    if(!st || !st.states.includes(S.fState)) return false;
  }
  if(skip!=='years'){
    if(S.fYearFrom!=='' && r.year < +S.fYearFrom) return false;
    if(S.fYearTo!=='' && r.year > +S.fYearTo) return false;
  }
  if(skip!=='sdg' && S.fSdg!=='' && !(r.sdgs||[]).includes(+S.fSdg)) return false;
  return true;
}
let cacheFiltered = null, cacheKey='';
function filtered(skip){
  if(skip) return R.filter(r=>passes(r,skip));
  const key = JSON.stringify([S.fKeyword,S.fMech,S.fBody,S.fType,S.fState,S.fYearFrom,S.fYearTo,S.fSdg,S.fTheme]);
  if(key!==cacheKey){ cacheKey=key; cacheFiltered = R.filter(r=>passes(r,null)); }
  return cacheFiltered;
}
```

Aggregations:
```js
function distinctSymbols(list){ return new Set(list.map(r=>r.symbol)).size; }
function yearRange(list){ if(!list.length) return null; let mn=list[0].year,mx=mn; for(const r of list){ if(r.year<mn)mn=r.year; if(r.year>mx)mx=r.year;} return [mn,mx]; }
function topThemes(list, k){
  const c = new Map();
  for(const r of list){ for(const t of (r.themes||[])){ c.set(t,(c.get(t)||0)+1); } }
  const arr = [...c.entries()].map(([theme,count])=>({theme,count}));
  arr.sort((a,b)=> b.count-a.count || (a.theme<b.theme?-1:a.theme>b.theme?1:0));
  return arr.slice(0,k);
}
function themeStats(list, theme){ // count + year range for table
  let n=0,mn=null,mx=null;
  for(const r of list){ if((r.themes||[]).includes(theme)){ n++; if(mn===null||r.year<mn)mn=r.year; if(mx===null||r.year>mx)mx=r.year; } }
  return {n,mn,mx};
}
```

Mechanisms in file (ordered by count desc for tiles):
```js
const mechCounts = countBy(R, r=>r.mechanism);
```

Header fill:
```js
$('hCountry').textContent = COUNTRY.toUpperCase(); // label "UHRI · KENYA"
$('hTitle').textContent = 'UN human rights recommendations and observations: '+COUNTRY;
document.title = same;
const docsTotal = distinctSymbols(R);
const [mnY,mxY] = yearRange(R)||[null,null];
$('hMeta').innerHTML = `<a href="${esc(U.source_url)}" target="_blank" rel="noopener">${esc(U.source)}</a> · ${fmt(N)} records · ${fmt(docsTotal)} documents · ${mnY}–${mxY} · built ${esc(U.built)} · dated by document`;
```
Hmm "built" might be a date string. esc fine. If years null (empty), guard.

Footer similar.

Rail selects init:
- selMech: '' all + mechanisms with counts (whole file counts? or facet? I said facet. Mechanism select — I'll use facet counts (filtered minus mech). Hmm, but body options depend on mechanism... The plan: mechanism options don't specify counts. Let me keep mechanism counts static from the whole file to avoid confusion, since it's the top of the hierarchy. Actually faceted counts everywhere is more consistent... but there's a subtlety: with keyword "torture", mechanism counts show matches per mechanism — useful. I'll do faceted counts for mechanism too. Fine — one function rebuildSelect(sel, options, currentValue).

Actually simpler to make everything facet-based except years and SDG (file-based, static-ish). Let me do:
- selMech: facet('mech') counts.
- selBody: facet('body') counts.
- selType: facet('type') counts.
- selState: facet('state') counts (states within UPR records passing others).
- selFrom/selTo: static file years.
- selSdg: static file goals with names.

Rebuild selects in renderRail each time. Careful not to destroy focus while user interacts — selects rebuild on change events (after selection), acceptable.

Keyword inputs: two inputs (rail + main). Both with debounce 300ms.

```js
let kwTimer=null;
function setKeyword(v, srcInput){
  S.fKeyword = v;
  // sync inputs
  for(const inp of [ $('kwRail'), $('kwMain') ]){ if(inp && inp.value!==v) inp.value=v; }
  onFilterChange();
}
function bindKeyword(inp){
  inp.addEventListener('input', ()=>{
    const v = inp.value;
    clearTimeout(kwTimer);
    kwTimer = setTimeout(()=> setKeyword(v), 300);
  });
}
```

onFilterChange():
```js
function onFilterChange(){
  cacheKey=''; // invalidate
  S.visible = 50;
  renderRail();
  renderOverview();
  renderRecords();
  if(S.tab==='check') renderChecks(); // chart-vs-table uses current filter
  updateCsvNote();
}
```
Hmm renderOverview charts only when visible; guard inside.

renderRail():
```js
function renderRail(){
  const list = filtered();
  $('matchCount').textContent = fmt(list.length);
  $('matchOf').textContent = 'matching records · of '+fmt(N)+' in the file';
  $('barFill').style.width = N? (100*list.length/N)+'%':'0%';
  // chips
  const chips = activeChips();
  $('chips').innerHTML = chips.map(([k,label])=>`<span class="chip">${esc(label)}<button data-clear="${k}" aria-label="Remove filter ${esc(label)}">×</button></span>`).join('');
  $('clearAll').hidden = chips.length===0;
  // selects
  rebuildSelect($('selMech'), facetOptions('mech', r=>r.mechanism), S.fMech);
  rebuildSelect($('selBody'), facetOptions('body', r=>r.body), S.fBody);
  rebuildSelect($('selType'), facetOptions('type', r=>r.type), S.fType);
  if(anyStates){
    $('stateWrap').hidden = false;
    const base = R.filter(r=>passes(r,'state'));
    const c = new Map();
    for(const r of base){ const st=statesOf.get(r.id); if(st) for(const s of st.states) c.set(s,(c.get(s)||0)+1); }
    const opts = [...c.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).map(([v,n])=>({v,label:v+' — '+n}));
    if(S.fState && !c.has(S.fState)) opts.push({v:S.fState,label:S.fState+' — 0'});
    rebuildSelect($('selState'), opts, S.fState);
  }
}
```

facetOptions(key, getter): base = R.filter(r=>passes(r,key)); count by getter; sort by count desc then label; return [{v,label:`${v} — ${n}`}]. Plus ensure current selection present.

rebuildSelect(sel, opts, cur):
```js
function rebuildSelect(sel, opts, cur){
  const all = opts.length + 1 <= 200 ? ... 
  let html = `<option value="">all</option>`; // or "all / each value"
  for(const o of opts) html += `<option value="${esc(o.v)}">${esc(o.label)}</option>`;
  sel.innerHTML = html;
  if(cur!=='' && !opts.some(o=>o.v===cur)){ sel.insertAdjacentHTML... add option with count 0 }
  sel.value = cur || '';
}
```
Hmm if cur not in opts, adding "cur — 0" option. Let me handle inside each caller or generically: pass cur and if missing append {v:cur,label:cur+' — 0'}. But for body with mechanism excluding — count 0 might be misleading (it IS 0 under other filters). Correct actually.

Wait, there's a subtlety with "all" label — for mechanism "all", body "all", type "all", state "all". OK.

Cap options? Bodies = 16 values, states maybe ~130 (recommending states). A select with 130 options is fine.

Year selects:
```js
const years = [...new Set(R.map(r=>r.year))].sort((a,b)=>a-b);
selFrom: <option value="">from</option> + years
selTo: <option value="">to</option> + years
```
On change: swap if reversed: if both set and from>to, swap the two select values.

SDG select:
```js
const goals = [...new Set(R.flatMap(r=>r.sdgs||[]))].sort((a,b)=>a-b);
options: '' → "all" + each `SDG ${g} — ${SDG_NAMES[g]||''}`.
```

Accordion:
```js
document.querySelectorAll('.fhead').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    const open = btn.getAttribute('aria-expanded')==='true';
    document.querySelectorAll('.fhead').forEach(b=>{ b.setAttribute('aria-expanded','false'); b.parentElement.querySelector('.fbody').hidden=true; });
    if(!open){ btn.setAttribute('aria-expanded','true'); btn.parentElement.querySelector('.fbody').hidden=false; }
  });
});
```

Tabs:
```js
const tabs = [...document.querySelectorAll('[role="tab"]')];
function selectTab(name){
  S.tab = name;
  tabs.forEach(t=>{
    const on = t.getAttribute('data-tab')===name;
    t.setAttribute('aria-selected', on?'true':'false');
    t.tabIndex = on?0:-1;
    $('panel-'+name).hidden = !on;
  });
  $('railFilters').hidden = (name==='check'||name==='method');
  if(name==='overview') renderOverview(true); // force charts
  if(name==='check') renderChecks();
}
tabs.forEach((t,i)=>{
  t.addEventListener('click',()=>{ selectTab(t.dataset.tab); t.focus(); });
});
tablist keydown: ArrowRight etc → selectTab + focus.
```

renderOverview(force):
```js
function renderOverview(force){
  const list = filtered();
  // headline tiles
  const typeCounts = countBy(list, r=>r.type);
  const breakdown = Object.entries... order: sort desc by count.
  tiles html...
}
```
Headline tiles:
1. Records tile: big = fmt(list.length); note under = breakdown "1,791 Recommendations · 471 Concerns/Observations · 2 Other"; how = "Count of records matching all active filters (of 2,264 in the file). The type labels are the UN's own."
2. Documents tile: big = distinctSymbols(list); how = "Distinct document symbols in the current filter."
3. Years tile: big = `${mn}–${mx}` (serif); how = "First to last year of document dates in the current filter; dates are document dates."

Mechanism tiles per mechanism (file mechanisms sorted by count desc):
- dot colored, label mono; big number records; line: "x documents · latest YYYY · z% of matching records"; UPR tile extra: "see the States" link.
- how: "Records from this mechanism in the current filter."

FIG.01:
```js
const top = topThemes(list,10);
fig1Title = `Ten most frequent themes among ${fmt(list.length)} filtered records`;
```
Hmm "filtered records" — or "matching records"? Plan: "Ten most frequent themes among n filtered records". Use that wording but with the count.

Chart build:
```js
if(chart1) chart1.destroy();
if(!list.length){ show fig1Box message; hide canvas? } 
```
For empty: fig1Box.innerHTML = '<p class="empty">No records match.</p>' — but canvas inside would be destroyed. I'll have fig1Box contain canvas; on empty, replace box content with message and on non-empty restore canvas. Let me structure: `<div class="chart-box" id="fig1wrap"></div>` and create canvas each time: `fig1wrap.innerHTML='<canvas id="fig1" ...></canvas>'` hmm — Chart.js attaches to canvas element. Recreating canvas each render is fine (destroy old chart first).

Chart1:
```js
chart1 = new Chart(canvas, {
 type:'bar',
 data:{ labels: top.map(t=>truncate(t.theme,44)), datasets:[{ data: top.map(t=>t.count), backgroundColor:'rgba(155,35,53,0.8)', borderColor:'#9b2335', borderWidth:0, barThickness:18 }]},
 options:{
  indexAxis:'y', responsive:true, maintainAspectRatio:false,
  layout:{padding:{right:56}},
  plugins:{ legend:{display:false}, tooltip:{callbacks:{title: items=> full theme name }} },
  scales:{
   x:{grid:{display:false}, border:{color:'#d9d2c3'}, ticks:{color:'#1d1b18', font:{family:mono? sans}}, suggestedMax: max*1.12 },
   y:{grid:{display:false}, ticks:{color:'#1d1b18', font:{size:12}, autoSkip:false}, border:{display:false}}
  },
  onClick:(e,els)=>{ if(els.length){ const i=els[0].index; S.fTheme = top[i].theme; onFilterChange(); } }
 },
 plugins:[endLabels]
});
```
endLabels plugin draws fmt(value) at bar.x+6, bar.y+4 (baseline center). font 12 mono. Only for horizontal single dataset — I'll register it just on chart1. The plugin receives chart; check chart.config.type==='bar' && options.indexAxis==='y' && one dataset.

Store full labels for tooltip: labels array holds truncated; keep fullNames array in closure; tooltip callback title: items=>fullNames[items[0].dataIndex].

Theme table under chart:
```html
<table class="data">
<caption>Same ten themes as FIG.01 — table form</caption>
<thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead>
<tbody> rows: theme | fmt(n) | pct1(n, list.length) | mn–mx of records carrying it </tbody>
</table>
<p class="how">A record can carry several themes, so counts sum to more than {n}. Percentages are of records, not of labels. Counts are of the current filter.</p>
<p class="source mono">Source: OHCHR UHRI file attached to this app; current filter.</p>
```
Wait, plan says the note under the chart and the table has same ten rows. Also clicking table rows? No, only bars. Maybe also make table theme cells clickable? Not in plan — skip.

FIG.02:
```js
const mechs = Object.keys(mechCountsAll); // all mechanisms in file
labels = all years in chart range;
datasets per mechanism.
chartYearRange: if year filter set use [from||fileMin, to||fileMax] else [fileMin, fileMax].
```
Wait, I decided: chartYearRange = yearFilter active ? [fYearFrom||minFile, fYearTo||maxFile] : [minFile, maxFile]. Actually if only from set: from→maxFile. Good.

fig2Title: "Records per year by mechanism". fig2How: "Count of records per document year and mechanism, current filter. Every year from first to last is shown, so gaps are visible; dates are document dates."

Legend: position 'bottom', usePointStyle true... mechanism colors.

Stacked: scales x stacked true, y stacked true. x type category labels years (as strings). barPercentage maybe 0.8.

Also add y axis title "records"? The title says it. Ticks fine. y grid: light? "no gridline clutter" — I'll keep y grid subtle (color #e8e2d5) for reading stacked totals, or hide. Analysis Function prefers minimal. I'll keep faint horizontal grid on y only for fig2. Hmm, "no gridline clutter" — a faint grid aids reading a stacked chart; keep very light. OK.

renderRecords():
```js
function renderRecords(){
  const list = filtered();
  const rows = sortRecords(list);
  const shown = rows.slice(0, S.visible);
  // caption
  $('recCaption').innerHTML = `${fmt(shown.length)} of ${fmt(list.length)} matching records shown · ${S.dateAsc?'oldest first':'newest first'} <span class="muted">(click Date to reverse)</span>`;
  if(!list.length){ recBody.innerHTML = ''; moreBtn.hidden = true; caption says 'No records match the current filters.'; return; }
  recBody.innerHTML = shown.map(rowHTML).join('');
  moreBtn.hidden = rows.length <= S.visible;
  moreBtn.textContent = `Show 50 more (${fmt(rows.length - Math.min(S.visible, rows.length))} remaining)`; // simple: 'Show 50 more'
}
```
Keep "Show 50 more" plain per plan.

sortRecords:
```js
function sortRecords(list){
  const arr = list.slice();
  arr.sort((a,b)=>{
    const da=a.date||'', db=b.date||'';
    if(da!==db) return S.dateAsc ? (da<db?-1:1) : (da>db?-1:1);
    if(a.body!==b.body) return a.body<b.body?-1:1;
    const pa=paraNum(a.text), pb=paraNum(b.text);
    const na=pa==null?Infinity:parseFloat(pa), nb=pb==null?Infinity:parseFloat(pb);
    if(na!==nb) return na-nb;
    return (idxOf.get(a.id)||0)-(idxOf.get(b.id)||0);
  });
  return arr;
}
```

rowHTML(r):
```js
const para = paraNum(r.text);
const st = statesOf.get(r.id);
let stateCell;
if(r.mechanism==='Universal Periodic Review'){
  stateCell = st && st.states.length ? esc(st.states.join(', ')) : '<span class="muted">State not found</span>';
}else stateCell = '<span class="muted">—</span>';
const open = S.expanded.has(r.id);
return `<tr class="rec" tabindex="0" data-id="${esc(r.id)}" aria-expanded="${open}">
 <td class="mono td-date">${esc(r.date)}</td>
 <td>${esc(r.body)}</td>
 <td><a href="${esc(r.doc_url)}" target="_blank" rel="noopener">${esc(r.symbol)}</a></td>
 <td class="num mono">${para?esc(para):'<span class="muted">—</span>'}</td>
 <td class="first">${highlight(esc(firstLine(r.text)))}</td>
 <td>${stateCell}</td>
</tr>` + (open? detailHTML(r):'');
```

highlight: applied to escaped first line with keyword words:
```js
function highlight(escaped){
  const ws = (S.fKeyword||'').toLowerCase().split(/\s+/).filter(Boolean);
  if(!ws.length) return escaped;
  const re = new RegExp('('+ws.map(rxEsc).join('|')+')','gi');
  return escaped.replace(re,'<mark>$1</mark>');
}
```
Note: keyword words are raw text; escaped string has entities — matching raw word inside entity possible (e.g. word "amp"). Edge, ignore.

detailHTML(r):
```js
const para = paraNum(r.text);
const st = statesOf.get(r.id);
let labels = '';
// themes chips
if((r.themes||[]).length) labels += `<div class="lab"><span class="mono">THEMES</span> ${r.themes.map(t=>`<span class="chip static">${esc(t)}</span>`).join('')}</div>`;
else labels += `<div class="lab"><span class="mono">THEMES</span> <span class="muted">not labelled</span></div>`;
// sdgs
if((r.sdgs||[]).length){
  const chips = r.sdgs.map(g=>`<span class="chip static">SDG ${g}${SDG_NAMES[g]?' · '+esc(SDG_NAMES[g]):''}</span>`).join('');
  labels += `<div class="lab"><span class="mono">SDGs</span> ${chips}</div>`;
  if((r.sdg_targets||[]).length) labels += `<div class="lab"><span class="mono">SDG TARGETS</span> ${r.sdg_targets.map(t=>`<span class="chip static">${esc(t)}</span>`).join('')}</div>`;
}else labels += `<div class="lab"><span class="mono">SDGs</span> <span class="muted">not labelled</span></div>`;
// affected persons
if((r.affected_persons||[]).length) labels += ...; else "not labelled";
// section
if(r.section) labels += `<div class="lab"><span class="mono">SECTION</span> ${esc(r.section)}</div>`;
```
Plus:
```html
<div class="para-big">${para?esc(para):'<span class="muted mono">no paragraph number</span>'}</div>
<p class="fulltext">${esc(r.text)}</p>
${labels}
<div class="actions">
 <button class="btn copy-cite" data-id="${esc(r.id)}">${para?'Copy citation':'Copy citation (no paragraph number in this extract)'}</button>
 <a class="btn link-btn" href="${esc(r.doc_url)}" target="_blank" rel="noopener">Open the UN document</a>
</div>
```
Structure: `<tr class="detail"><td colspan="6">…</td></tr>`.

Row events (delegation on recBody):
```js
recBody.addEventListener('click', e=>{
  if(e.target.closest('a')||e.target.closest('button')) return;
  const tr = e.target.closest('tr.rec');
  if(tr) toggleDetail(tr);
});
recBody.addEventListener('keydown', e=>{
  if(e.key==='Enter'||e.key===' '){
    const tr = e.target.closest('tr.rec');
    if(tr && e.target===tr){ e.preventDefault(); toggleDetail(tr); }
  }
});
```
toggleDetail:
```js
function toggleDetail(tr){
  const id = tr.dataset.id;
  const rec = R[idxOf.get(id)];
  if(S.expanded.has(id)){
    S.expanded.delete(id);
    const d = tr.nextElementSibling;
    if(d && d.classList.contains('detail')) d.remove();
    tr.setAttribute('aria-expanded','false');
  }else{
    S.expanded.add(id);
    tr.insertAdjacentHTML('afterend', detailHTML(rec));
    tr.setAttribute('aria-expanded','true');
  }
}
```

Copy citation:
```js
recBody.addEventListener('click', e=>{
  const b = e.target.closest('button.copy-cite');
  if(!b) return;
  const rec = R[idxOf.get(b.dataset.id)];
  const para = paraNum(rec.text);
  copyText(para? `${rec.symbol}, para. ${para}` : rec.symbol, b);
});
```
copyText with fallback and "Copied" flash:
```js
function copyText(text, btn){
  const done = ()=>{ const old=btn.textContent; btn.textContent='Copied'; btn.classList.add('copied'); setTimeout(()=>{btn.textContent=old;btn.classList.remove('copied');},2000); };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(done).catch(()=>fallbackCopy(text,done));
  } else fallbackCopy(text,done);
}
function fallbackCopy(text,done){
  const ta=document.createElement('textarea'); ta.value=text; ta.style.position='fixed'; ta.style.opacity='0';
  document.body.appendChild(ta); ta.select();
  try{ document.execCommand('copy'); done(); }catch(err){}
  ta.remove();
}
```

sortDate button:
```js
$('sortDate').addEventListener('click',()=>{ S.dateAsc=!S.dateAsc; $('sortArrow').textContent=S.dateAsc?'▴':'▾'; renderRecords(); });
```
Also th aria-sort.

moreBtn: S.visible += 50; renderRecords(); — but that re-renders; fine. Should not reset S.visible.

States link on overview:
```js
$('statesLink')... rendered inside mechTiles html with delegation on mechTiles container.
```
I'll render the UPR tile with `<button class="linkish" id="statesBtn">see the States</button><div id="statesList" hidden>…</div>`. Since tiles re-render on filter change, the statesList content should re-render too when open. renderOverview builds tiles; if S.statesOpen, include the list filled. Toggle: S.statesOpen flips, re-render overview. But re-render overview rebuilds charts — acceptable (destroy/create). Hmm, toggling states list re-creating charts is slightly wasteful but fine.

Actually careful: renderOverview creates charts each time; charts need visible panel. renderOverview called on filter change even when tab hidden — guard chart creation: only if panel-overview not hidden; else set flag S.chartsDirty. selectTab('overview') calls renderOverview.

Let me implement renderOverview(alwaysCharts):
```js
function renderOverview(){
  const list = filtered();
  // tiles...
  // charts only if visible
  const vis = !$('panel-overview').hidden;
  if(vis){ buildCharts(list); } else { chartsDirty = true; }
}
```
selectTab: if name==='overview'){ if(chartsDirty){ renderOverview(); chartsDirty=false; } }

Hmm simpler: selectTab('overview') always calls renderOverview(). Fine (rebuild charts on each tab entry — ok).

But careful: building Chart on a canvas that was just created inside a hidden container — we only build when visible. Good.

Check tab render:

```js
function renderChecks(){
  const list = filtered();
  const lines = [];
  const push=(status,label,detail)=>lines.push({status,label,detail});
  // 1 record count
  const declared = Number(U.count);
  push(N===declared?'pass':'fail', 'Record count', `The file holds ${fmt(N)} records; the file's own count field says ${fmt(declared)}.`);
  // partitions
  const sumCheck = (getter,name)=>{
    const c = countBy(R, getter);
    const sum = Object.values(c).reduce((a,b)=>a+b,0);
    push(sum===N?'pass':'fail', name, `Counts per ${name.toLowerCase()} sum to ${fmt(sum)}; the record count is ${fmt(N)}.`);
  };
```
Hmm names: "Mechanism partition", "Body partition", "Year partition", "Type partition". Detail wording: "Counts per mechanism sum to 2,264, equal to the record count." For fail: "...do not sum... (2,260 vs 2,264)".

```js
  // links
  const bad = R.filter(r=>{
    let u = String(r.doc_url||'');
    try{ u = decodeURIComponent(u); }catch(e){}
    u = u.replace(/\/+$/,'');
    let s = String(r.symbol||'');
    try{ s = decodeURIComponent(s); }catch(e){}
    return !/^https:\/\/docs\.un\.org\//.test(u) || !u.toLowerCase().endsWith(s.toLowerCase());
  });
  push(bad.length? 'fail':'pass','Document links', bad.length? `${fmt(bad.length)} of ${fmt(N)} records have a doc_url that does not start with https://docs.un.org/ or end with their symbol: ${bad.slice(0,8).map(r=>esc(r.symbol)).join(', ')}${bad.length>8?` … and ${fmt(bad.length-8)} more`:''}.` : `All ${fmt(N)} doc_urls start with https://docs.un.org/ and end with their symbol.`);
```

Paragraph numbers per mechanism:
```js
  for(const m of mechanismsInFile){
    const recs = R.filter(r=>r.mechanism===m);
    const withNum = recs.filter(r=>paraNum(r.text)!=null).length;
    const share = pct1(withNum, recs.length);
    const expect100 = m==='Universal Periodic Review';
    const status = expect100 ? (withNum===recs.length?'pass':'warn') : 'info';
    push(status, `Paragraph numbers — ${m}`, `${share} of records start with a paragraph number${expect100?'; UPR records are expected to have one':''}.`);
  }
```
Status 'info' — neutral line. Hmm "one line per check... a pass mark or a red 'check failed'". For informational, show "—" or "OK". I'll have statuses: pass ("PASS"), fail ("FAIL" red), warn ("WARNING"), info ("INFO" muted). OK.

States found:
```js
  const upr = R.filter(r=>r.mechanism==='Universal Periodic Review');
  const found = upr.filter(r=>{const s=statesOf.get(r.id);return s&&s.states.length;});
  const missing = upr.filter(r=>{const s=statesOf.get(r.id);return !(s&&s.states.length);});
  push(missing.length?'warn':'pass','Recommending States', `${fmt(found.length)} of ${fmt(upr.length)} UPR records name at least one State in parentheses.` + (missing.length? ` Without one: ${missing.slice(0,10).map(r=>`${esc(r.symbol)} (para. ${esc(paraNum(r.text)||'—')}) — parentheses held: ${esc((statesOf.get(r.id).raw||[]).join(' ')||'nothing')}`).join('; ')}${missing.length>10?` … and ${fmt(missing.length-10)} more`:''}.`:''));
```

Duplicates and gaps:
```js
  const ids = new Set(R.map(r=>r.id));
  push(ids.size===N?'pass':'fail','Record identifiers', `${fmt(ids.size)} distinct ids for ${fmt(N)} records.`);
  const textCounts = new Map();
  for(const r of R){ const t=String(r.text||''); textCounts.set(t,(textCounts.get(t)||0)+1); }
  const dupTexts = [...textCounts.values()].filter(v=>v>1).length;
  push(dupTexts? 'warn':'pass','Duplicate texts', dupTexts? `${fmt(dupTexts)} text${dupTexts>1?'s':''} appear in more than one record.` : `No text appears in more than one record.`);
  const noTheme = R.filter(r=>!(r.themes||[]).length).length;
  const noSdg = R.filter(r=>!(r.sdgs||[]).length).length;
  const noAff = R.filter(r=>!(r.affected_persons||[]).length).length;
  push('info','Records not labelled', `No themes: ${fmt(noTheme)}; no SDGs: ${fmt(noSdg)}; no affected persons: ${fmt(noAff)}.`);
```

Chart vs table (current filter):
```js
  const top = topThemes(list,10);
  // second independent loop
  const second = new Map();
  for(const r of list){ for(const t of (r.themes||[])) second.set(t,(second.get(t)||0)+1); }
  const okBars = top.every(t=>second.get(t.theme)===t.count);
  push(okBars?'pass':'fail','FIG.01 bars against a second count', okBars? `Each of the ten theme bars equals a count recomputed by a second, independent loop over the ${fmt(list.length)} matching records.` : `At least one bar differs from the second count.`);
  const maxBar = top.length? top[0].count : 0;
  push(maxBar<=list.length?'pass':'fail','Largest bar within the record count', `The largest theme count (${fmt(maxBar)}) is not larger than the number of matching records (${fmt(list.length)}).`);
```

Render lines:
```js
$('checkList').innerHTML = lines.map(l=>`<li class="check ${l.status}"><span class="mono status">${l.status.toUpperCase()}</span> <strong>${esc(l.label)}</strong> — ${l.detail}</li>`).join('');
```
Note detail may contain pre-escaped content (I esc where needed). I built detail with esc() inline for symbols. For plain numbers no esc needed. Careful to esc all record-derived strings. I did above.

Method text and export:

Method sentences — build with actual numbers? "How each number is computed, in five or six plain sentences." Write 6 sentences (static-ish, using country name):

1. "Every number on this page is counted in your browser from the attached file of {N} records; nothing is estimated, no language model is called, and nothing leaves the browser except the text you copy."
2. "The headline counts records (all types: {type breakdown spelled}), documents as distinct symbols, and the first and last year of document dates — dates are document dates, not the dates recommendations were made or accepted."
3. "Filters combine with AND: a keyword (every word must appear, literally, in the text or the symbol), mechanism, body or mandate, type, recommending State, year range and SDG goal; the theme filter is added by clicking a bar in FIG.01."
4. "Theme counts count each theme once per record that carries it, so they sum to more than the record count; percentages are of records, not of labels."
5. "Paragraph numbers are read from the start of each text ('71.' or '144.43'); recommending States are read only from the parentheses at the end of UPR texts, and a record naming two States counts once for each."
6. "The random-sample check draws ten records with a seeded generator (mulberry32), so the same seed draws the same ten; your verdicts are yours and change no UN label."

Good, 6 sentences.

CSV note: "The CSV contains the visible columns plus the full text and all labels, with comment lines naming the country, source, build date, filters applied and row count. Generated in your browser; nothing is uploaded."

csvBtn:
```js
$('csvBtn').addEventListener('click',()=>{
  const list = filtered();
  const rows = sortRecords(list);
  const f = filterDescription();
  let csv = '';
  csv += `# UN human rights recommendations and observations: ${COUNTRY}\n`;
  csv += `# Source: ${U.source} <${U.source_url}>\n`;
  csv += `# Built: ${U.built}\n`;
  csv += `# Filters: ${f||'none'}\n`;
  csv += `# Rows: ${rows.length}\n`;
  csv += 'Date,Body,Mechanism,Type,Symbol,Document URL,Para.,First line,Recommending State,Full text,Themes,SDGs,SDG targets,Affected persons,Section\n';
  for(const r of rows){
    const para = paraNum(r.text);
    const st = statesOf.get(r.id);
    csv += [r.date, r.body, r.mechanism, r.type, r.symbol, r.doc_url, para||'', firstLine(r.text), st? st.states.join('; '):'', r.text, (r.themes||[]).join('; '), (r.sdgs||[]).join('; '), (r.sdg_targets||[]).join('; '), (r.affected_persons||[]).join('; '), r.section||''].map(csvEsc).join(',')+'\n';
  }
  const blob = new Blob([csv], {type:'text/csv;charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href=url; a.download = 'uhri-'+COUNTRY.toLowerCase().replace(/[^a-z0-9]+/g,'-')+'-filter.csv';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(url), 5000);
});
```

filterDescription(): list active filters "keyword=\"x\"; mechanism=...; body=...; type=...; State=...; years=a–b; SDG=g; theme=..." or "none".

Copy summary:
```js
function summaryText(){
  const list = filtered();
  const top = topThemes(list,10);
  const types = Object.entries(countBy(list,r=>r.type)).sort((a,b)=>b[1]-a[1]).map(([t,n])=>`${fmt(n)} ${t}`).join(', ');
  const f = filterDescription();
  return `UN human rights recommendations and observations: ${COUNTRY}. ${fmt(list.length)} records${f?` (filter: ${f})`:''} of ${fmt(N)} in the file, from ${fmt(distinctSymbols(list))} documents, ${yearRangeText(list)}. Types: ${types||'none'}. Ten most frequent themes: ${top.map(t=>`${t.theme} (${fmt(t.count)})`).join('; ')||'none'}. A record can carry several themes. Source: ${U.source}, built ${U.built}. Counts made in the browser from the attached file; nothing estimated.`;
}
```
yearRangeText: mn–mx of filtered, or "no years".

Source note on tab 04:
```js
$('sourceNote').innerHTML = `Source: <a href=...>${esc(U.source)}</a> · ${fmt(N)} records · ${fmt(docsTotal)} documents · built ${esc(U.built)}. Licence: OHCHR Universal Human Rights Index data; see the source for its terms of use.`;
```
Hmm "licence line" — the plan says the tab shows "The data source, licence line and build date." I don't know the licence; saying "see the source for terms of use" is honest. Good.

Sample section rendering:

```js
function renderSample(){
  const wrap = $('cards');
  if(!S.sample){ wrap.innerHTML=''; $('tally').textContent=''; return; }
  wrap.innerHTML = S.sample.map((r,i)=>{
    const para = paraNum(r.text);
    const v = S.verdicts[r.id]||'';
    const open = S.openCard===r.id;
    return `<div class="card" data-id="${esc(r.id)}">
      <button class="card-head" aria-expanded="${open}" data-i="${i}">
        <span class="mono">${esc(r.symbol)}</span> · para. ${esc(para||'—')} · <span class="muted">${esc(truncate(r.text.replace(/^(?:\d{1,3}(?:\.\d{1,3})?)\.?\s/,''),70))}</span>
      </button>
      <div class="card-body" ${open?'':'hidden'}>
        <p class="mono card-meta"><a href="${esc(r.doc_url)}" target="_blank" rel="noopener">${esc(r.symbol)}</a> · ${esc(r.date)} · ${esc(r.body)} · para. <span class="red">${esc(para||'not numbered')}</span></p>
        <p class="fulltext">${esc(r.text)}</p>
        <div class="lab"><span class="mono">THEMES (UN LABELS)</span> ${(r.themes||[]).length? r.themes.map(t=>`<span class="chip static">${esc(t)}</span>`).join(''):'<span class="muted">not labelled</span>'}</div>
        <div class="verdict">
          <button class="btn vbtn ${v==='fit'?'sel':''}" data-v="fit" data-id="${esc(r.id)}">Fits</button>
          <button class="btn vbtn ${v==='no'?'sel':''}" data-v="no" data-id="${esc(r.id)}">Doesn't fit</button>
          <button class="btn vbtn ${v==='unsure'?'sel':''}" data-v="unsure" data-id="${esc(r.id)}">Unsure</button>
        </div>
      </div>
    </div>`;
  }).join('');
  renderTally();
}
function renderTally(){
  if(!S.sample) return;
  const fit = S.sample.filter(r=>S.verdicts[r.id]==='fit').length;
  const no = S.sample.filter(r=>S.verdicts[r.id]==='no').length;
  const un = S.sample.filter(r=>S.verdicts[r.id]==='unsure').length;
  const judged = fit+no+un;
  $('tally').textContent = `Themes: ${fit} fit, ${no} don't, ${un} unsure of ${judged} of ${S.sample.length} judged · seed ${S.sampleSeed}`;
}
```
Card events (delegation on #cards): click on .card-head toggles open (close others); click on .vbtn sets verdict, updates classes + tally without full re-render:
```js
$('cards').addEventListener('click', e=>{
  const head = e.target.closest('.card-head');
  if(head){
    const card = head.closest('.card');
    const id = card.dataset.id;
    const wasOpen = S.openCard===id;
    // close all
    document.querySelectorAll('#cards .card').forEach(c=>{
      c.querySelector('.card-body').hidden = true;
      c.querySelector('.card-head').setAttribute('aria-expanded','false');
    });
    if(!wasOpen){
      card.querySelector('.card-body').hidden=false;
      head.setAttribute('aria-expanded','true');
      S.openCard = id;
    } else S.openCard = null;
    return;
  }
  const vb = e.target.closest('.vbtn');
  if(vb){
    const id = vb.dataset.id;
    S.verdicts[id] = vb.dataset.v;
    const card = vb.closest('.card');
    card.querySelectorAll('.vbtn').forEach(b=>b.classList.toggle('sel', b===vb));
    renderTally();
  }
});
```

Draw:
```js
function drawSample(seed){
  const list = filtered();
  const sample = [];
  if(list.length){
    const rng = mulberry32(seed>>>0 || 1);
    const idx = list.map((_,i)=>i);
    for(let i=idx.length-1;i>0;i--){ const j = Math.floor(rng()*(i+1)); const t=idx[i]; idx[i]=idx[j]; idx[j]=t; }
    for(let i=0;i<Math.min(10,idx.length);i++) sample.push(list[idx[i]]);
  }
  S.sample = sample; S.sampleSeed = seed; S.verdicts = {}; S.openCard=null;
  S.drawn = true;
  $('drawBtn').hidden = true;
  $('drawMore').hidden = false;
  $('seedBox').value = seed;
  if(!list.length){ $('cards').innerHTML='<p class="muted">No records match the current filter; nothing to draw.</p>'; $('tally').textContent=''; return; }
  renderSample();
}
$('drawBtn').addEventListener('click', ()=> drawSample(randomSeed()));
$('drawAgain').addEventListener('click', ()=> drawSample(randomSeed()));
$('drawSeed').addEventListener('click', ()=>{ const v = parseInt($('seedBox').value,10); drawSample(Number.isFinite(v)? v : 1); });
function randomSeed(){ return Math.floor(Math.random()*1000000)+1; }
```
Hmm "Check 10 at random" with random seed vs default 1 in box... The plan: "the seed is shown in a box, default 1". Initially box=1. If "Check 10 at random" uses random seed, box updates to that seed. Then "Draw with this seed" with 1 reproduces the colleague's default... fine. Actually, maybe "Check 10 at random" should use the box's current seed (1 by default) for reproducibility from the very first draw? Then "Draw again" = new random. Hmm: "(then 'Draw again' and 'Draw with this seed', the seed box and the tally)" — the seed box appears after first draw. "Draw again" should give a different sample — random seed. I think random for both "Check 10 at random" and "Draw again" is most natural ("at random"), with the seed recorded. Go with random.

mulberry32 seed 0 → `seed>>>0||1` avoids 0? mulberry32(0) works fine actually. Keep `seed>>>0`.

Note "of 10 judged" — if fewer than 10 records in filter, sample.length < 10; tally shows "of x of y judged" — my format: "of {judged} of {total} judged". OK.

Also the tally line should note it's the reader's judgement: add sentence under tally: "The tally is your judgement, not the app's; the UN's labels are unchanged." I'll include in the intro paragraph or a small note. Plan: "The tally is the reader's judgement, labelled as such". Add mono note under tally.

Now — "Check 10 at random draws the cards" — from current filter. Good.

Also, an important accessibility bit: tabs arrow key nav:
```js
const tablistEl = document.querySelector('[role="tablist"]');
tablistEl.addEventListener('keydown', e=>{
  const i = tabs.findIndex(t=>t.tabIndex===0 || t.getAttribute('aria-selected')==='true');
  let j = null;
  if(e.key==='ArrowRight') j=(i+1)%tabs.length;
  else if(e.key==='ArrowLeft') j=(i-1+tabs.length)%tabs.length;
  else if(e.key==='Home') j=0;
  else if(e.key==='End') j=tabs.length-1;
  if(j!==null){ e.preventDefault(); selectTab(tabs[j].dataset.tab); tabs[j].focus(); }
});
```

Chips removal (delegation on #chips): data-clear values: 'keyword','mech','body','type','state','years','sdg','theme'. Clear mapping:
```js
$('chips').addEventListener('click', e=>{
  const b = e.target.closest('button[data-clear]');
  if(!b) return;
  const k = b.dataset.clear;
  if(k==='keyword'){ S.fKeyword=''; sync inputs; }
  else if(k==='mech') S.fMech='';
  ... 'years' clears both year filters; 'sdg' S.fSdg=''; 'theme' S.fTheme='';
  onFilterChange();
});
$('clearAll').addEventListener('click', ()=>{ reset all; onFilterChange(); });
```

Chips labels: 
- keyword: `keyword: “torture”`
- mech: `mechanism: UPR` — use actual value.
- body: `body: CEDAW`
- type: `type: Recommendations`
- state: `State: Gambia`
- years: `years: 2010–2015` (single: `years: from 2010` / `to 2015`)
- sdg: `SDG 5 — Women...`? Keep `SDG: 5`
- theme: `theme: ...`

Select change handlers:
```js
$('selMech').addEventListener('change', e=>{ S.fMech=e.target.value; onFilterChange(); });
... etc
$('selFrom')/: on change set, then swap:
function yearChange(){
  S.fYearFrom = $('selFrom').value; S.fYearTo = $('selTo').value;
  if(S.fYearFrom!=='' && S.fYearTo!=='' && +S.fYearFrom > +S.fYearTo){
    [S.fYearFrom, S.fYearTo] = [S.fYearTo, S.fYearFrom];
    $('selFrom').value=S.fYearFrom; $('selTo').value=S.fYearTo;
  }
  onFilterChange();
}
```

States link toggle:
```js
$('mechTiles').addEventListener('click', e=>{
  if(e.target.closest('#statesBtn')){ S.statesOpen = !S.statesOpen; renderOverview(); }
});
```
But renderOverview rebuilds tiles including the button; the list content when open:
```js
function statesListHTML(list){
  const upr = list.filter(r=>r.mechanism==='Universal Periodic Review');
  const c = new Map();
  for(const r of upr){ const st=statesOf.get(r.id); if(st) for(const s of st.states) c.set(s,(c.get(s)||0)+1); }
  const top = [...c.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,10);
  return `<div class="states-list" id="statesList">
    <div class="mono figtitle-sm">TEN STATES THAT MADE MOST RECOMMENDATIONS TO ${esc(COUNTRY.toUpperCase())}</div>
    ${top.length? `<ol class="states-ol">${top.map(([s,n])=>`<li><span class="serif bignum-sm">${fmt(n)}</span> ${esc(s)}</li>`).join('')}</ol>` : '<p class="muted">No UPR records with a recommending State in the current filter.</p>'}
    <p class="how">Count of UPR records in the current filter naming that State; a record naming two States counts once for each. A count of recommendations, not of influence.</p>
  </div>`;
}
```

Now on load: initialize header, selects (static ones), bind events, onFilterChange() initial render, selectTab('overview').

Also number formatting in charts: ticks callback fmt.

One more detail: "Fifty rows at a time" — initial S.visible=50.

The table under FIG.01 needs the year range per theme: themeStats(list, theme) gives n, mn, mx — but n should equal t.count (it does, same computation). Use recomputed (also serves as the "second loop" consistency). Years column: `${mn}–${mx}`.

Wait — plan for the theme table: "Theme | Records | % of filtered | Years (first–last year of the records carrying it)". Records = count (same as bar). Fine.

Also chart tooltip full name: keep fullTheme[i].

Now let me think about the FIG.01 when list is non-empty but no themes at all (all unlabelled): top = []; chart with no bars — show message "No themes in the matching records." Handle: if top.length===0 → message instead of chart.

FIG.02 when list empty → "No records match".

Let me also compute file-level mechanisms list order: sort by count desc.

Edge: `U.count` string — Number(). If U.count missing → NaN → check shows fail with "says NaN"? Guard: `const declared = U.count!=null? Number(U.count) : NaN;` detail: `the file's count field says "${U.count}"`. Compare N===declared.

Now CSS details. Let me write it.

```css
.mono{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
```
Careful: applying .mono to things like seed labels, tab names. Body text normal. But some mono spans contain sentences (hints) — uppercase letter-spaced sentences are hard to read. I'll make `.mono` not uppercase by default; add `.mono-up` for uppercase? The design says "small uppercase letter-spaced monospace for labels, tab names and figure numbers". So labels uppercase. Hints: keep mono small but normal case? "Short monospace hints" — the examples of hints like "click = filter", "literal match, not synonyms" — I'll keep those lowercase mono without letterspacing. Let me define:

```css
.mono{font-family:var(--mono);font-size:12px;}
.lab-up{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);}
```
I'll use class `lab` for uppercase labels and `mono` for small mono text. Fine — in HTML I'll pick appropriately.

Layout:

```css
header{padding:28px 32px 18px;border-bottom:1px solid var(--rule)}
h1{font-family:var(--serif);font-size:34px;line-height:1.15;margin:6px 0 8px;font-weight:600; max-width: 60ch}
.layout{display:grid;grid-template-columns:270px minmax(0,1fr);min-height:60vh}
.rail{border-right:1px solid var(--rule);padding:20px 20px;}
main{padding:24px 32px 48px;min-width:0}
footer{border-top:1px solid var(--rule);padding:12px 32px;color:var(--muted)}
@media (max-width:880px){ .layout{grid-template-columns:1fr} .rail{border-right:none;border-bottom:1px solid var(--rule)} }
```

Tablist:
```css
.tablist{display:flex;gap:0;border-bottom:1px solid var(--rule);padding:0 32px; overflow-x:auto}
[role="tab"]{font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;background:none;border:none;border-bottom:2px solid transparent;padding:12px 18px 10px;color:var(--muted);cursor:pointer;text-transform:uppercase}
[role="tab"][aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
[role="tab"]:hover{color:var(--ink)}
```

Rail big number:
```css
.bignum{font-family:var(--serif);font-size:46px;line-height:1;margin:14px 0 2px}
.bar{height:4px;background:var(--rule);margin:10px 0 4px}
.bar-fill{height:100%;background:var(--red);width:0%}
```

Chips:
```css
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 4px}
.chip{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--rule);border-radius:999px;padding:2px 10px;font-size:12.5px;background:#fdfbf6}
.chip button{background:none;border:none;color:var(--red);cursor:pointer;font-size:14px;line-height:1;padding:0}
.chip.static{background:none;border-color:var(--rule);color:var(--ink)}
```

Filter groups:
```css
.fgroup{border-top:1px solid var(--rule);margin-top:12px}
.fhead{width:100%;display:flex;justify-content:space-between;align-items:center;background:none;border:none;cursor:pointer;padding:10px 0 8px;font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;color:var(--ink);text-transform:uppercase}
.fhead::after{content:"+";color:var(--muted)}
.fhead[aria-expanded="true"]::after{content:"–";color:var(--red)}
.fbody{padding:0 0 14px;display:grid;gap:6px}
.fbody label{...mono small muted}
select,input[type=search],input[type=number]{width:100%;padding:7px 8px;font:inherit;font-size:14px;background:#fdfbf6;border:1px solid var(--rule);color:var(--ink);border-radius:2px}
.hint{color:var(--muted);font-family:var(--mono);font-size:11.5px}
```

Tiles:
```css
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0 36px;margin:6px 0 18px}
.tile{border-top:2px solid var(--ink);padding:10px 0 16px}
.tile .big{font-family:var(--serif);font-size:48px;line-height:1.05}
.tile .sub{font-size:13.5px;color:var(--ink);margin-top:6px}
.how{font-family:var(--mono);font-size:11.5px;color:var(--muted);margin-top:6px;line-height:1.45}
```
Mechanism tiles: similar with dot.

Figures:
```css
figure{margin:34px 0 0;border-top:1px solid var(--rule);padding-top:14px}
.figno{font-family:var(--mono);font-size:11px;letter-spacing:.14em;color:var(--red)}
.figtitle{font-family:var(--serif);font-size:21px;margin:6px 0 14px;font-weight:600}
.chart-box{position:relative;height:380px}
.chart-box.sm{height:300px}
.empty{font-family:var(--serif);font-size:18px;color:var(--muted);padding:30px 0}
.source{...mono muted}
```

Tables:
```css
table.data, table.records{width:100%;border-collapse:collapse;font-size:14.5px}
caption{caption-side:top;text-align:left;font-family:var(--mono);font-size:11.5px;color:var(--muted);padding:0 0 8px;letter-spacing:.04em}
th{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:1px solid var(--ink);padding:8px 10px 6px 0;color:var(--ink);font-weight:600}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
td{border-bottom:1px solid var(--rule);padding:8px 10px 8px 0;vertical-align:top}
tbody tr:last-child td{border-bottom:1px solid var(--rule)}
tr.rec{cursor:pointer}
tr.rec:hover td{background:#efe9dd}
td.first{max-width:520px}
td.td-date, .mono-td{font-family:var(--mono);font-size:12.5px;white-space:nowrap}
```

Detail rows:
```css
tr.detail td{background:#efe9dd;padding:18px 14px}
.para-big{font-family:var(--serif);font-size:38px;color:var(--red);line-height:1;margin-bottom:10px}
.fulltext{white-space:pre-wrap;max-width:900px;font-size:15.5px;margin:0 0 14px}
.lab{margin:6px 0;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.lab .lab-up{min-width:110px}
.actions{margin-top:14px;display:flex;gap:10px;flex-wrap:wrap}
.btn{font:inherit;font-size:13.5px;background:none;border:1px solid var(--ink);color:var(--ink);padding:7px 14px;cursor:pointer;border-radius:2px}
.btn:hover{border-color:var(--red);color:var(--red)}
.btn.copied{border-color:var(--red);color:var(--red)}
a.btn{display:inline-block;text-decoration:none}
.linkish{background:none;border:none;color:var(--red);cursor:pointer;font:inherit;font-size:13px;padding:0;text-decoration:underline}
mark{background:#f2d7db;color:inherit;padding:0 1px}
```

Checks:
```css
.checks{list-style:none;padding:0;margin:0}
.checks li{border-top:1px solid var(--rule);padding:10px 0;font-size:14.5px}
.status{display:inline-block;min-width:74px;font-weight:600}
.check.pass .status{color:#0f766e}? 
```
Hmm — colour policy: one accent red; other colours only where a category needs one. Mechanism colours exist. For check statuses: pass could be muted ink, fail red. Let me: pass → color var(--muted) "PASS"; fail → red "FAIL" and whole line maybe red-ish; warn → ink "WARNING"; info → muted "INFO". Actually a green for pass is conventional and helpful... but design says one accent. I'll use muted for pass, red for fail. OK.

Cards:
```css
.card{border-top:1px solid var(--rule)}
.card-head{width:100%;text-align:left;background:none;border:none;padding:10px 0;cursor:pointer;font:inherit;font-size:14px;display:flex;gap:8px;flex-wrap:wrap}
.card-head:hover{color:var(--red)}
.card-body{padding:4px 0 18px 0}
.verdict{margin-top:10px;display:flex;gap:8px}
.vbtn.sel{border-color:var(--red);color:var(--red);background:#f7e8ea}
```

Search bar on records tab:
```css
.searchbar{margin-bottom:14px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.searchbar input{max-width:420px}
```

Focus visible:
```css
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
```

Serif h2:
```css
h2.serif{font-family:var(--serif);font-size:24px;margin:26px 0 10px;font-weight:600}
```

OK. Now assemble everything. Also careful: the `mono` class with uppercase transform only for `lab-up`. Tab names: style in [role=tab] directly.

Meta line in header: mono small, mixed content (source link + numbers): use font mono 12px, no uppercase.

Footer: mono 11.5px muted.

One more check on the plan: "Header... A monospace label 'UHRI · Kenya'". Yes.

"Under it a big serif number, 'n matching records' (aria-live='polite', with 'of N in the file')" — I have the big number + "matching records · of N in the file". The big number element has aria-live. Put aria-live on a wrapper containing number + text? Put aria-live="polite" on the div containing the number and the "of" line. I'll wrap: `<div aria-live="polite"><div class="bignum">…</div><div class="hint">…</div></div>`.

Rail on tabs 03/04: hide #railFilters only. Chips still visible (they're above). Good — plan says rail keeps number, bar, chips.

Also: on tab 03/04, "Clear all" button — it's in rail head; keep it visible (it relates to chips). Fine.

Now — potential issue: `passes` uses S.fYearFrom!=='' comparisons; select values are strings like "2010". r.year is int. `r.year < +S.fYearFrom` fine.

SDG: S.fSdg string; +S.fSdg number; r.sdgs includes numbers. Good.

Another subtlety: keyword matching on symbol too — highlight only in first line. Fine.

"Show 50 more" resets? onFilterChange resets S.visible=50. Good.

Let me also add: table caption includes "· symbol links open the UN document in a new tab"? Not necessary.

Now — think about the "Records" tab caption when keyword active: "Showing 50 of 234 matching records". Good.

Let me now also double-check FIG.01 percentages in table: pct of filtered list length.

Now write the full file. I'll aim for clarity. Also must keep under ~1500 lines — should be around 1100–1300.

Let me also handle Chart.defaults:
```js
if(window.Chart){
  Chart.defaults.font.family = getComputedStyle(document.body).fontFamily; // sans
  Chart.defaults.font.size = 12.5;
  Chart.defaults.color = '#1d1b18';
}
```
Guard if Chart missing (shouldn't be).

End-labels plugin:
```js
const endLabelsPlugin = {
  id:'endLabels',
  afterDatasetsDraw(chart){
    if(!chart.options.plugins.endLabels) return;
    const {ctx} = chart;
    const meta = chart.getDatasetMeta(0);
    if(!meta.data.length) return;
    ctx.save();
    ctx.font = '12px ' + (window.Chart && Chart.defaults? '':'');
    ...
  }
};
```
Simpler: define plugin inline in chart config with closure. Chart.js v4: plugins array in config. I'll write:

```js
const valueAtEnd = {
  id:'valueAtEnd',
  afterDatasetsDraw(chart){
    const cfg = chart.options.plugins.valueAtEnd;
    if(!cfg || !cfg.on) return;
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = '600 12px ui-monospace, Menlo, Consolas, monospace';
    ctx.fillStyle = '#1d1b18';
    ctx.textBaseline = 'middle';
    const meta = chart.getDatasetMeta(0);
    meta.data.forEach((bar,i)=>{
      const v = chart.data.datasets[0].data[i];
      if(v==null) return;
      ctx.fillText(fmt(v), bar.x + 6, bar.y);
    });
    ctx.restore();
  }
};
```
Register per chart via plugins:[valueAtEnd] and options.plugins.valueAtEnd={on:true} for fig1 only. Chart.js merges plugin options by id. Good.

x suggestedMax: `suggestedMax: Math.max(...data)*1.15` or add ticks callback fmt.

Also y ticks font: 12px sans; label truncation.

Tooltip: show full theme + count. callbacks: title: items => fullThemes[items[0].dataIndex], label: item => fmt(item.parsed.x)+' records'.

FIG.02 tooltip: title year, label: `${dataset.label}: ${fmt(v)}`.

onClick bar → theme filter. Also maybe cursor pointer on hover: onHover set cursor. Add `onHover:(e,els)=>{e.native.target.style.cursor = els.length?'pointer':'default';}`.

Now — the initial render: call selectTab('overview') which calls renderOverview; but also renderRail and renderRecords must run. Order: build static selects, bind events, then onFilterChange() (renders rail, overview, records), selectTab('overview') to set visibility (already default in HTML: overview visible, others hidden; tabs aria-selected preset). I'll set initial HTML with overview selected, then call onFilterChange().

But charts need panel visible — overview is visible by default. OK.

Double-check: renderOverview called by onFilterChange; panel-overview hidden only when other tab selected; then chartsDirty flag; selectTab('overview') → renderOverview(). Implement:

```js
let chartsDirty=false;
function renderOverview(){
  ...tiles...
  const vis = !$('panel-overview').hidden;
  if(vis){ buildFig1(list); buildFig2(list); chartsDirty=false; }
  else chartsDirty=true;
}
selectTab: if(name==='overview' && chartsDirty) renderOverview();
```
Actually simpler: in selectTab, if name==='overview') renderOverview(); — always rebuild. Charts rebuild on every tab entry — slight flicker but fine, no animation delay. I'll do the chartsDirty approach to avoid unnecessary rebuilds: on selectTab overview, if chartsDirty renderOverview(). 

Hmm — but on filter change while overview hidden, tiles also need update when returning... renderOverview updates tiles AND charts; if I skip it when hidden, tiles stale. Solution: renderOverview always updates tiles; charts only when visible (chartsDirty flag). Let me structure renderOverview to always update tiles + theme table, and buildCharts conditionally. Good.

Same for renderRecords — DOM table fine while hidden.

renderChecks — run when check tab selected or filter change while check active. Also it's cheap; but the checks list includes record-level listing computations — all O(N), fine to run always. But rebuilding on every keystroke while on check tab is fine too. I'll run renderChecks in onFilterChange only if check tab active, and on selectTab check.

Now the header "documents" count and mechanism tiles — need countBy helper:
```js
function countBy(list, fn){
  const m = new Map();
  for(const r of list){ const k = fn(r); if(k==null||k==='') continue; m.set(k,(m.get(k)||0)+1); }
  return m;
}
```
Wait — for type breakdown, empty type strings skipped; sum check would then not sum to N if types empty. In the data type is always filled. For the partition checks, I count including everything (even empty) to make sums exact? The check: "Counts per mechanism... each sum to the record count". If some mechanism were empty string, skipping breaks sum. Data says mechanism always filled. I'll count all values including empty (key '' shown as "(blank)"). Use a separate countAll that doesn't skip:

```js
function countAll(list, fn){ const m=new Map(); for(const r of list){ const k=fn(r); m.set(k,(m.get(k)||0)+1); } return m; }
```
Use countAll everywhere; display '' as "(blank)" if it ever appears.

Type breakdown display order: sort desc count.

Mechanism tiles: iterate mechanisms from countAll(R, mechanism) sorted desc.

For each mech tile: records = countAll(list, mechanism).get(m)||0; docs = distinct symbols among list with that mechanism; latest = max year; share = pct of list.length. Colored dot.

Now — HTML escaping in tile innerHTML with template strings. Fine.

Also, the overview tiles' "How this is computed" notes:
- records tile: "Records matching all active filters; the file holds {fmt(N)}. Type labels are the UN's own."
- docs tile: "Distinct document symbols among the matching records."
- years tile: "First to last document year among the matching records; dated by document."
- mech tiles: "Records from this mechanism among the matching records; share is of the matching records."

FIG.01 how: "Each theme is counted once per record carrying it, so the bars sum to more than {n}; click a bar to filter by that theme. Source: the attached UHRI file, current filter."

FIG.02 how: as above.

Now let me write the final HTML file. I'll be careful about a few things:

- The `.first` column: firstLine + highlight.
- The detail row colspan=6.
- The sort arrow initial "▾" (newest first = date descending).
- `aria-sort` on date th: `${S.dateAsc?'ascending':'descending'}`.

Potential pitfall: innerHTML with huge table (2264 rows? No — only 50 shown). Good.

The theme table: 10 rows. Good.

States select options ~130 — fine.

Let me also handle: when fState filter is active and user is on tab 01, UPR tile share etc. all consistent through filtered().

Edge: extractStates on UPR text ending with "(Gambia)." — regex: `/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/`. Text "...(Gambia)." — the run captures "(Gambia)", then `\s*[;.]?\s*$` matches ".". Good. Text ending "...(Cabo Verde) (Slovenia) (Togo);" — run = "(Cabo Verde) (Slovenia) (Togo)" then ";". Good. Text ending "...(art. 15)." (treaty body — not applied). Text ending "...(Venezuela (Bolivarian Republic of));" — group regex matches "(Venezuela (Bolivarian Republic of))". slice(1,-1) → "Venezuela (Bolivarian Republic of)". No comma, length 36 → accepted. 

Edge: UPR text ends with a period after state: "(Nigeria)." fine. Ends without parens: "...children." → no match → states [] → "State not found".

Hmm wait — one more: some UPR texts might end with "(see A/HRC/...)". Contains "/" and maybe no comma → could be accepted wrongly as a State. Length ≤60, no comma → accepted. The plan acknowledges: "A few UPR texts end with a parenthesis that is not a State... The comma-and-length rule catches most; the check panel lists the rest." OK, accepted per spec.

Now, "the records without one are listed with their symbol, so the reader can see what the parentheses held instead" — for records with no parens at all, raw is empty; show "no parentheses at the end". My detail: `parentheses held: ${(raw.join(' ')||'nothing')}`.

Let me now also write the truncate helper:
```js
function truncate(s,n){ s=String(s||''); return s.length<=n? s : s.slice(0,n).replace(/\s+\S*$/,'')+'…'; }
```

Now — writing the final answer. Intro: at most three short sentences before code block, nothing after.

Let me write the complete file now, mentally checking as I go.

One more consideration on the tab names: "01 OVERVIEW · 02 RECORDS · 03 CHECK · 04 METHOD & EXPORT". 

Panel labels/headings inside: 
- overview: no big heading needed? Maybe small question heading: The tabs pose questions: "what the data shows, the records themselves, can I trust this, method and export". I could add an h2 per panel with the question. Nice editorial touch: 
  - 01: "What has the UN said, how much, and when?"
  - 02: "Which paragraph says it, and in which UN document?"
  - 03: "Can I trust these numbers?"
  - 04: "How was this made, and how do I take it with me?"
Add as serif h2 at top of each panel. Good.

Also the plan says tab 01 has "A row of big serif numbers" — with the h2 above, fine.

Now, mechanism select "all" default; type select "all" default. Body "all".

Writing code — I must be careful with quotes inside template literals in HTML attributes. Use consistent double quotes in HTML, template backticks in JS.

Also: `S.fState` naming vs state select id selState.

Let me define activeChips:
```js
function activeChips(){
  const out=[];
  if(S.fKeyword) out.push(['keyword','keyword: “'+S.fKeyword+'”']);
  if(S.fMech) out.push(['mech','mechanism: '+S.fMech]);
  if(S.fBody) out.push(['body','body: '+S.fBody]);
  if(S.fType) out.push(['type','type: '+S.fType]);
  if(S.fState) out.push(['state','State: '+S.fState]);
  if(S.fYearFrom||S.fYearTo) out.push(['years','years: '+(S.fYearFrom||'…')+'–'+(S.fYearTo||'…')]);
  if(S.fSdg!=='') out.push(['sdg','SDG '+S.fSdg]);
  if(S.fTheme) out.push(['theme','theme: '+S.fTheme]);
  return out;
}
```
Note: chips text gets esc() when rendered. Theme names may contain "&" — esc handles.

Clear chip mapping:
```js
const CLEAR = {
  keyword:()=>{S.fKeyword='';},
  mech:()=>{S.fMech='';},
  body:()=>{S.fBody='';},
  type:()=>{S.fType='';},
  state:()=>{S.fState='';},
  years:()=>{S.fYearFrom='';S.fYearTo='';},
  sdg:()=>{S.fSdg='';},
  theme:()=>{S.fTheme='';}
};
```
After clearing keyword, sync inputs.

clearAll: run all CLEAR fns.

Now onFilterChange full:
```js
function onFilterChange(){
  cacheKey='__invalidate__'; cacheFiltered=null;
  S.visible=50;
  renderRail();
  renderOverview();
  renderRecords();
  if(!$('panel-check').hidden) renderChecks();
  updateExportNote();
}
```
Hmm — my filtered() caching uses key compare; setting cacheKey to something impossible works.

updateExportNote: sets csvBtn label with count: `Download CSV of the current filter (${fmt(n)} rows)` and sumBtn context. Plan button label "Download CSV of the current filter". I'll keep the plain label and a note line with rows. Actually adding count to button is useful: "Download CSV of the current filter — 1,234 rows". Keep.

Copy summary button label "Copy summary".

Method text: include country.

Now write renderOverview:

```js
function renderOverview(){
  const list = filtered();
  // headline
  const types = [...countAll(list,r=>r.type).entries()].sort((a,b)=>b[1]-a[1]||String(a[0]).localeCompare(String(b[0])));
  const breakdown = types.map(([t,n])=>`${fmt(n)} ${t===''?'(blank)':esc(t)}`).join(' · ');
  const docs = distinctSymbols(list);
  const yr = yearRange(list);
  $('headlineTiles').innerHTML = `
   <div class="tile">
     <div class="tile-label lab">RECORDS</div>
     <div class="big">${fmt(list.length)}</div>
     <div class="sub">${breakdown||'no records match'}</div>
     <div class="how">Count of records matching all active filters, of every type; the file holds ${fmt(N)}. Type labels are the UN's own.</div>
   </div>
   <div class="tile">
     <div class="tile-label lab">DOCUMENTS</div>
     <div class="big">${fmt(docs)}</div>
     <div class="sub">distinct symbols</div>
     <div class="how">Distinct document symbols among the matching records.</div>
   </div>
   <div class="tile">
     <div class="tile-label lab">YEARS</div>
     <div class="big">${yr? yr[0]+'–'+yr[1] : '—'}</div>
     <div class="sub">document dates</div>
     <div class="how">First to last year of document dates among the matching records; dated by document.</div>
   </div>`;
```
Hmm "big" for years range might be long (2007–2026 = 9 chars) at 48px — ok, maybe 40px for that tile. I'll use a smaller class for the years number: big-sm (36px). Fine.

Mechanism tiles:
```js
  const mechAll = [...countAll(R,r=>r.mechanism).entries()].sort((a,b)=>b[1]-a[1]);
  $('mechTiles').innerHTML = mechAll.map(([m])=>{
    const recs = list.filter(r=>r.mechanism===m);
    const d = distinctSymbols(recs);
    const latest = recs.length? Math.max(...recs.map(r=>r.year||0)) : null;
    const dot = MECH_COLORS[m]||'#6b6459';
    const statesBtn = m==='Universal Periodic Review' ? `<button class="linkish" id="statesBtn">${S.statesOpen?'hide the States':'see the States'}</button>` : '';
    const statesList = (m==='Universal Periodic Review'&&S.statesOpen)? statesListHTML(list):'';
    return `<div class="tile mech">
      <div class="tile-label lab"><span class="dot" style="background:${dot}"></span>${esc(m)}</div>
      <div class="big">${fmt(recs.length)}</div>
      <div class="sub">${fmt(d)} documents · latest ${latest==null?'—':latest} · ${pct1(recs.length,list.length)} of matching records</div>
      ${statesBtn}${statesList}
      <div class="how">Records from this mechanism among the matching records.</div>
    </div>`;
  }).join('');
```

FIG.01 title & table & charts:
```js
  const top = topThemes(list,10);
  $('fig1Title').textContent = `Ten most frequent themes among ${fmt(list.length)} matching records`;
  $('fig1How').textContent = `Each theme is counted once per record carrying it, so the bars sum to more than ${fmt(list.length)}; click a bar to filter by that theme. Current filter; source: the attached UHRI file.`;
  // table
  const tb = top.map(t=>{
    const st = themeStats(list,t.theme);
    return `<tr><td>${esc(t.theme)}</td><td class="num">${fmt(st.n)}</td><td class="num">${pct1(st.n,list.length)}</td><td class="num">${st.mn==null?'—':st.mn+'–'+st.mx}</td></tr>`;
  }).join('');
  $('themeTableBody').innerHTML = tb || '<tr><td colspan="4" class="muted">No themes among the matching records.</td></tr>';
  $('themeTableCaption').textContent = `The same ten themes as FIG.01, in table form — themes of ${fmt(list.length)} matching records`;
```

Charts:
```js
  if(!$('panel-overview').hidden){ buildCharts(list, top); chartsDirty=false; } else chartsDirty=true;
```

buildCharts(list, top):
```js
function buildCharts(list, top){
  if(chart1){chart1.destroy();chart1=null;}
  if(chart2){chart2.destroy();chart2=null;}
  const box1 = $('fig1wrap');
  if(!list.length || !top.length){
    box1.innerHTML = '<p class="empty">'+(!list.length?'No records match.':'No themes among the matching records.')+'</p>';
  } else {
    box1.innerHTML = '<canvas></canvas>';
    const full = top.map(t=>t.theme);
    chart1 = new Chart(box1.querySelector('canvas'), {...});
  }
  const box2 = $('fig2wrap');
  if(!list.length){ box2.innerHTML='<p class="empty">No records match.</p>'; return; }
  box2.innerHTML = '<canvas></canvas>';
  // years range
  let a = minFileYear, b = maxFileYear;
  if(S.fYearFrom!=='') a = Math.min(a, +S.fYearFrom); // hmm
  ...
```
Wait, chart year range: if year filter active, use [from||minFile, to||maxFile]; else file range. Let me:
```js
  let y0 = minFileYear, y1 = maxFileYear;
  if(S.fYearFrom!=='') y0 = +S.fYearFrom;
  if(S.fYearTo!=='') y1 = +S.fYearTo;
  if(y0>y1){const t=y0;y0=y1;y1=t;}
  const labels = []; for(let y=y0;y<=y1;y++) labels.push(String(y));
  const mechs = [...countAll(R,r=>r.mechanism).keys()];
  const data = mechs.map(m=> labels.map(y=> list.filter(r=>r.mechanism===m && r.year===+y).length));
```
That's O(mechs*years*list) = 3*20*2264 ≈ 136k ops — fine. Better: precompute map. I'll do a nested loop counting.

chart2 config:
```js
  chart2 = new Chart(canvas2, {
    type:'bar',
    data:{labels, datasets: mechs.map(m=>({label:m, data: countsFor(m), backgroundColor: MECH_COLORS[m]||'#6b6459', barPercentage:0.85}))},
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{position:'bottom', labels:{boxWidth:10, boxHeight:10, usePointStyle:false}}, tooltip:{callbacks:{label: i=> i.dataset.label+': '+fmt(i.parsed.y)}}},
      scales:{x:{stacked:true, grid:{display:false}, border:{color:'#d9d2c3'}}, y:{stacked:true, grid:{color:'#eae4d6'}, border:{display:false}, ticks:{callback: v=>fmt(v)}}}
    }
  });
```

fig2 title: "Records per year by mechanism" + how line mentions filter and gaps.

Chart1 config:
```js
  const labels1 = top.map(t=>truncate(t.theme,42));
  const data1 = top.map(t=>t.count);
  chart1 = new Chart(c1, {
    type:'bar',
    data:{labels:labels1, datasets:[{data:data1, backgroundColor:'rgba(155,35,53,0.8)', hoverBackgroundColor:'#9b2335', barThickness:18}]},
    options:{
      indexAxis:'y', responsive:true, maintainAspectRatio:false,
      layout:{padding:{right:64}},
      plugins:{
        legend:{display:false},
        tooltip:{callbacks:{title:i=>full[i[0].dataIndex], label:i=>fmt(i[0].parsed.x)+' records'}},
        valueAtEnd:{on:true}
      },
      scales:{
        x:{grid:{display:false}, border:{color:'#d9d2c3'}, ticks:{callback:v=>fmt(v)}, suggestedMax: Math.max(...data1)*1.12},
        y:{grid:{display:false}, border:{display:false}, ticks:{font:{size:12}, color:'#1d1b18', autoSkip:false}}
      },
      onClick:(e,els)=>{ if(els.length){ S.fTheme = full[els[0].index]; onFilterChange(); } },
      onHover:(e,els)=>{ e.native.target.style.cursor = els.length?'pointer':'default'; }
    },
    plugins:[valueAtEnd]
  });
```

Note: `Math.max(...data1)*1.12` — fine.

Now renderRecords:

```js
function renderRecords(){
  const list = filtered();
  const rows = sortRecords(list);
  const shown = rows.slice(0,S.visible);
  const cap = $('recCaption');
  if(!list.length){
    cap.textContent = 'No records match the current filters.';
    $('recBody').innerHTML = '';
    $('moreBtn').hidden = true;
    return;
  }
  cap.innerHTML = `Showing ${fmt(shown.length)} of ${fmt(list.length)} matching records · ${S.dateAsc?'oldest first':'newest first'} · <span class="muted">click Date to reverse · click a row to read it in full</span>`;
  $('recBody').innerHTML = shown.map(rowHTML).join('');
  $('moreBtn').hidden = rows.length<=S.visible;
}
```

Search input on records tab placeholder: `Search ${fmt(N)} records, e.g. torture` — plan: 'Search n records, e.g. torture'. n = file total (or matching?). I'll use file total. Set once.

Now: renderChecks as designed. The mechanisms list for the paragraph check: use file mechanisms.

Now — one thing I should double check: the check "Chart against table" says "the ten rows under the chart show the same values". My table uses themeStats (second loop) and chart uses topThemes; comparing topThemes vs second-loop — that IS the check. Good.

mulberry32 implementation — standard.

Sample note line: "This is your judgement of the UN's labels; nothing is sent anywhere." — put above cards, per plan: "A line above the cards says...". I have it in intro paragraph; plan wants it above the cards. I'll place it right above #cards as mono hint. And also keep intro sentence. OK.

Tally note: after tally, small: "The tally is your judgement, not the app's; the UN's labels are unchanged." I'll append to tally line? Tally text: "Themes: x fit, y don't, z unsure of 10 judged · seed 12345 — your judgement; the UN's labels are unchanged." Slightly long; ok as mono line.

Now assemble. Also remember doc lang="en".

Let me make sure no external resources: no CDN, fonts system only. Chart.js preloaded as window.Chart — guard `typeof Chart!=='undefined'`.

Also `input[type=number]` for seed.

Write the "How this is computed" near every chart or number — done via .how lines.

Let me also handle the `sortDate` header markup:
```html
<th scope="col" id="thDate" aria-sort="descending"><button id="sortDate" class="thsort" aria-label="Reverse date sort">Date <span id="sortArrow" aria-hidden="true">▾</span></button></th>
```

Potential focus issue: after re-render on Date sort click, focus lost from button? renderRecords only rewrites tbody & caption — button in thead untouched. Good. But onFilterChange → renderRecords rewrites tbody; if focus was in a row, it's lost — acceptable.

moreBtn click: S.visible+=50; renderRecords();

Now — a critical detail: the "Records" tab search field and rail keyword both bound. Also the placeholder of main search should reflect... fine static.

Also: keyword applied 300ms after typing — implemented.

Now let me write out everything in final form. I'll write carefully to avoid JS syntax errors. Some long template literals — mind backticks and ${}.

Also — countAll returns Map; entries iteration.

distinctSymbols:
```js
function distinctSymbols(list){ const s=new Set(); for(const r of list) s.add(r.symbol); return s.size; }
```
(symbol could be undefined → Set counts undefined once; data says always filled.)

Let me also compute minFileYear/maxFileYear once.

For the year selects: include an empty "from"/"to" option. Labels: just the year. Also show counts? Not required; skip.

Wait, one more plan detail: "Years with no records ... are absent from the year selects" — distinct years only. Yes.

Also SDG select label "all".

Now, HTML for panels with figure structure. The theme table:

```html
<table class="data" id="themeTable">
  <caption id="themeTableCaption"></caption>
  <thead><tr>
    <th scope="col">Theme</th>
    <th scope="col" class="num">Records</th>
    <th scope="col" class="num">% of filtered</th>
    <th scope="col" class="num">Years</th>
  </tr></thead>
  <tbody id="themeTableBody"></tbody>
</table>
<p class="how" id="themeTableHow"></p>
<p class="source mono">Source: the attached UHRI file · current filter · themes are the UN's own labels</p>
```

themeTableHow: `A record can carry several themes, so the counts sum to more than ${n}; percentages are of records, not of labels. Year range = first to last document year of the matching records carrying the theme.`

FIG.02 source line similar.

Let me now also think about what happens on very narrow screens — table with 6 columns might overflow; add `.records{display:block;overflow-x:auto}`? "Works on a laptop screen without horizontal scrolling" — laptop fine. I'll add overflow-x auto on a wrapper for safety.

Time to write the final code. I'll number nothing; just write.

Also: the intro before the code block: "at most three short sentences saying what you built or changed. After it: nothing."

Let me draft final sentences: "Here's the four-tab dashboard for Kenya's UN recommendations, built entirely from the attached UHRI file: overview with theme and timeline charts, a records table with in-place expansion and citations, a self-check tab with a seeded random-sample label check, and method/export with CSV and copy-summary. Every number is counted in the browser and says how it was computed."

That's two sentences. Good.

Now — one careful re-read of tricky requirements to not miss:

✓ header label, title, meta line with "dated by document".
✓ tabs with role tablist + arrow keys.
✓ rail: FILTERS + Clear all (right), big number aria-live, "of N in the file", red share bar, chips, 3 accordion headings, one open at a time, initially closed.
✓ tabs 01/02 show rail filters; 03/04 keep number/bar/chips.
✓ keyword 300ms debounce, hint.
✓ mechanism/body/type selects + state select when states extracted.
✓ years from/to (swap on reverse), sdg select with names.
✓ Tab 01: headline tiles + type breakdown; docs; years; mechanism tiles with records/docs/latest/share; "see the States" in UPR tile; FIG.01 ranked horizontal bars red 80%, click bar = theme filter, count at bar end, table under with Theme|Records|%|Years; FIG.02 stacked per year with gaps.
✓ Tab 02: search field synced; table columns; recommending State column; sort date desc + body + para numeric + file order; caption "newest first", click Date reverses; mark highlights; 50 rows + Show 50 more; expand in place with big red para, verbatim text, labels, copy citation (with no-para label variant), open UN doc link.
✓ Tab 03: check panel lines; sample check with seed, tally, cards with Fits/Doesn't fit/Unsure.
✓ Tab 04: method 5-6 sentences; CSV download with comment lines; copy summary; source/licence/build.
✓ Footer: "Built on OHCHR UHRI data · n records · source link".

Also "Every row that shows a document has its symbol, linked to doc_url in a new tab" — check cards and sample cards too. ✓.

One more: on tab 01, the "Recommending State" column header says "Recommending State" — for the whole table. ✓.

"clicking the Date header reverses it" — done.

Also the plan says the search field caption: "The caption gives rows shown of rows matching." ✓.

Potential issue: `sortRecords` uses paraNum(a.text) each comparison — cache para per record: paraMap. I'll precompute paraMap = Map(id→para) once. Use in rowHTML, detailHTML, sorting, CSV.

Also numeric para for sorting: paraNumericMap or parseFloat on the fly — parseFloat cheap. Use paraMap.get(id).

Careful: records may share id? ids distinct (checked). idxOf Map fine.

Now, writing the final file. Let me write it as one continuous piece.

Also CSS for `.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px;vertical-align:baseline}`.

`.tile-label` with dot inside flex.

Buttons `thsort`: `background:none;border:none;font:inherit;font-family:var(--mono);...cursor:pointer;color:inherit;text-transform:uppercase;letter-spacing:.08em;font-size:11px;padding:0`.

Also ensure `td a` white-space nowrap for symbols? Symbols can be longish "CEDAW/C/KEN/CO/9/Add.1" — allow wrap. Fine.

mark styling.

Also `.muted{color:var(--muted)}`.

`.red{color:var(--red)}`.

Let me also set `body{-webkit-font-smoothing:antialiased}` optional.

Print? skip.

Now — write JS in one <script> at end of body.

Also — important: when the keyword input in rail re-renders? It doesn't (static HTML). Selects innerHTML rebuilt each renderRail — while user has select open? Change events fire after selection; rebuild happens then. OK.

One more: `rebuildSelect` with "all" first option label — for selFrom/selTo the empty label "from"/"to". I'll write those separately (static init, not rebuilt).

Year selects static init:
```js
(function initYearSelects(){
  const years = [...new Set(R.map(r=>r.year).filter(y=>y!=null))].sort((a,b)=>a-b);
  $('selFrom').innerHTML = '<option value="">from</option>'+years.map(y=>`<option value="${y}">${y}</option>`).join('');
  $('selTo').innerHTML = '<option value="">to</option>'+...
})();
```

SDG static:
```js
const goals = [...new Set(R.flatMap(r=>Array.isArray(r.sdgs)?r.sdgs:[]))].sort((a,b)=>a-b);
$('selSdg').innerHTML = '<option value="">all</option>'+goals.map(g=>`<option value="${g}">SDG ${g}${SDG_NAMES[g]?' — '+esc(SDG_NAMES[g]):''}</option>`).join('');
```

rebuildSelect generic:
```js
function rebuildSelect(sel, opts, cur, allLabel){
  let html = `<option value="">${allLabel||'all'}</option>`;
  for(const o of opts) html += `<option value="${esc(o.v)}">${esc(o.label)}</option>`;
  if(cur!=='' && cur!=null && !opts.some(o=>String(o.v)===String(cur))) html += `<option value="${esc(cur)}">${esc(cur)} — 0</option>`;
  sel.innerHTML = html;
  sel.value = (cur==null?'':String(cur));
}
```

facetOptions(key, getter, labelFn):
```js
function facetOptions(key, getter){
  const base = R.filter(r=>passes(r,key));
  const c = countAll(base, getter);
  return [...c.entries()].sort((a,b)=>b[1]-a[1]||String(a[0]).localeCompare(String(b[0])))
    .map(([v,n])=>({v:String(v), label:`${v===''?'(blank)':v} — ${fmt(n)}`}));
}
```
For state options: special (multi-value). Handled separately in renderRail.

Mechanism options label: value — count.

Now — the states select: `stateWrap` hidden until anyStates. "A State select joins this heading when States are extracted." If no UPR states at all, hidden.

Also, "Recommending State" label in rail.

Everything set. Let me also double check `passes` with skip for 'state' — when computing state facet, skip state. ✓.

Potential subtle bug: filtered() cache — skip param bypasses cache. ✓.

Initial S values all '' — filtered() = all.

Let me write `countAll` and use for sums in checks.

Check "Links": also handle empty doc_url → fails startsWith → listed. ✓.

Now — writing final HTML. Also include `<noscript>`? Not needed.

Line count estimate ~1200. OK.

One more think — the "How this is computed" line near the big matching number in rail: "matching records · of N in the file" plus bar note "share of the file". Add tiny note under bar: `${pct1(n,N)} of the file`. Good.

Let me also make the h2s of panels: class="question". Style serif 26px.

Also tabpanel needs tabindex? Not necessary.

Writing now. I'll be methodical about the script order:

1. Guard data.
2. Helpers.
3. Derived maps (para, states).
4. Constants (mechanisms, colors, years, goals, docsTotal, yearRange file).
5. State S.
6. Filter functions.
7. Aggregations.
8. Header/footer init.
9. Static selects init.
10. Render functions.
11. Event bindings.
12. Initial render.

Careful with `S.statesOpen` and re-render preserving open state — renderOverview reads S.statesOpen. ✓.

For the copy-cite button inside detail: label with no-para variant. ✓.

For CSV firstLine — reuse firstLine(r.text) which appends "…". The CSV "First line" column — maybe better full? Plan: "the visible columns plus the full text and labels" — visible columns include First line (truncated) and Full text separately. ✓.

CSV line endings \n. Fine.

Summary copy uses copyText with button flash "Copied".

updateExportNote:
```js
function updateExportNote(){
  const n = filtered().length;
  $('csvBtn').textContent = `Download CSV of the current filter (${fmt(n)} rows)`;
}
```

Method text with numbers filled from data:
```js
$('methodText').innerHTML = `...sentences with <strong>? plain text...`;
```
Plain sentences, no HTML needed except maybe none. Use textContent with template. Sentences reference type breakdown spelled: "1,791 Recommendations, 471 Concerns/Observations and 2 Other" — compute from file. Let me build: typesAll = countAll(R, type) sorted desc → "X Recommendations, Y Concerns/Observations and Z Other" — join with ", " and last "and". Simple join(', ').

OK, writing the final output now.

One thing on `aria-live` region: the count div. Rebuilding its textContent announces politely. ✓.

Also the tally has aria-live polite. ✓.

Also: filter heading buttons — ensure type="button" (no form anyway).

Chart canvas: `<canvas role="img" aria-label="...">`? Chart.js sets aria attributes? I'll add aria-label on canvas describing the chart. Nice-to-have; add.

Let me finalize the FIG.02 aria label: "Stacked bar chart: records per year by mechanism".

Also table `.records` wrapper: `<div class="tablewrap">`.

Final check on click counts on tab 01 default: tabs(4) + rail headings(3) = 7 clickable + chart bars + "see the States" (only in UPR tile, a linkish button — that's an 8th...). Hmm. "see the States" is one click deeper content... it's visible though. "No view shows more than about seven things to click" — about seven; 8 is borderline but the plan itself mandates these elements (3 headings + 4 tabs + states link + clear all hidden initially). The plan is the spec; follow it.

Now — sample card head: contains a link? No, the head is a button; the symbol link is inside the body. But plan says "Each card: symbol linked to doc_url" — in the body. The head shows symbol as text. Fine. Actually plan: "each as a card: symbol linked to doc_url, paragraph number, the full verbatim text" — inside card. ✓.

Check cards "one open at a time". ✓.

"Draw with this seed" — parse int; if invalid use 1.

Also the seed box: type=number value=1.

Sample drawing from "current filter" — if check tab visible, filters may be active; that's intended.

Edge: sample of fewer than 10: tally "of {judged} of {total} judged". The intro line says "Check 10 at random" — if fewer, cards show fewer; add note if list.length<10: "only {n} records match; drawing all of them." I'll add to tally or a note. Minor; include in drawSample: if sample.length<10 && list.length, note in tally line: `· only ${sample.length} records in the current filter`. OK.

Now — write it!

Actually one more: "Show 50 more" — after click, focus? fine.

And the detail row for the LAST shown row: insertAdjacentHTML after tr works fine.

Escape: rowHTML uses esc on all fields. doc_url attr esc ✓.

Let me also handle body values containing quotes — esc covers.

Potential issue: `filtered()` inside `passes` closure uses S — fine.

Also — `sortRecords` uses paraMap:
```js
function sortRecords(list){
  return list.slice().sort((a,b)=>{
    const da=String(a.date||''), db=String(b.date||'');
    if(da!==db) return S.dateAsc ? (da<db?-1:1) : (da>db?-1:1);
    const ba=String(a.body||''), bb=String(b.body||'');
    if(ba!==bb) return ba<bb?-1:1;
    const pa=paraMap.get(a.id), pb=paraMap.get(b.id);
    const na=pa==null?Infinity:parseFloat(pa), nb=pb==null?Infinity:parseFloat(pb);
    if(na!==nb) return na-nb;
    return (idxOf.get(a.id)||0)-(idxOf.get(b.id)||0);
  });
}
```

paraMap built: `for(const r of R) paraMap.set(r.id, paraNum(r.text));`

OK. Writing final code now. I'll write the complete document.

Let me also give the app a `<title>`: "UN human rights recommendations and observations: Kenya" set dynamically.

Also add `lang="en"`.

Let me write the checks list with proper statuses; statuses: pass/fail/warn/info. Class names on li.

Detail strings for checks — build carefully with esc for data-derived strings.

For the paragraph-number check lines: statuses for non-UPR mechanisms 'info'; the plan says share per mechanism shown (informational), UPR warn if <100 else pass.

Now, count of checks lines: 1 (record count) + 3 partitions + 1 type + 1 links + 3 para (per mech) + 1 states + 1 ids + 1 dup texts + 1 not labelled + 2 chart = 15 lines. Fine.

Write the summary and method text generators.

Also don't forget: "Nothing is estimated" claims. OK.

Final code writing time. I'll now produce it, being careful about syntax. I'll double-check bracket balance mentally per function.

Also, `Chart` may be undefined — guard `const HAS_CHART = typeof window.Chart==='function';` and if not, chart boxes show message "Chart.js is not available in this sandbox." — fallback. Add guard in buildCharts.

Hmm — Chart.js 4 is preloaded per instructions, but guard anyway cheaply.

One subtle Chart.js v4 API: `border` axis config: `scales.x.border.color` — in v4 it's `scales.x.border = {color}` ✓. grid.display ✓.

Tooltip callbacks title receives array of items ✓.

`onHover` event: `e.native.target` ✓.

For stacked chart ticks callback on y: `callback: v=>fmt(v)` — v may be non-integer ticks; fine.

Alright — also the valueAtEnd plugin: bar.x is pixel position of bar end (for horizontal). ✓ textBaseline middle, y = bar.y.

Also ensure the plugin doesn't run for fig2: options.plugins.valueAtEnd not set → cfg undefined → return. ✓ (plugin registered only on chart1 anyway).

Writing the whole thing now. For maintainable length, I'll compress some CSS but keep readability.

Let me also remember the studio requirement: "Before the code block: at most three short sentences saying what you built or changed. After it: nothing."

Proceed to final answer.