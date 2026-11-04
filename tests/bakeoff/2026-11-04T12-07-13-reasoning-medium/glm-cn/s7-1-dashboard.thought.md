Build the full app. Single HTML file, four tabs, filters rail, charts, checks, export. Keep under ~1500 lines. Let me write carefully but efficiently.

Key components:
- Header with monospace label, title, source line.
- Left rail: FILTERS heading, clear all, big count, share bar, chips, three collapsible filter headings.
- Tabs 01-04 with role=tablist, arrow keys.
- Tab 01: tiles (total + type breakdown, docs, years, per-mechanism tiles), FIG.01 horizontal bar chart top 10 themes (click = filter), table under chart, FIG.02 stacked bars per year by mechanism.
- Tab 02: search box (same as keyword filter), table with Date, Body, Symbol, Para, First line, Recommending State; row expand with full details; copy citation; show 50 more; date sort toggle.
- Tab 03: checks panel + random sample label check with seed.
- Tab 04: method text, CSV download, copy summary, source.

Filters: mechanism, body, type, state, year from/to, SDG, keyword. All AND.

Data computations as specified. Paragraph number regex, state extraction regex for UPR only.

Note: rail on tabs 03/04 keeps only number, bar, chips — so hide filter headings there.

Credits: no shelf code used, so just footer.

Charts: destroy/recreate on filter change. Chart.js 4 preloaded.

Let me write the code.

Structure of JS:
- parse data, compute states per UPR record, paragraph numbers per record.
- state: filters object {keyword, mechanism, body, type, states:Set, yearFrom, yearTo, sdg, themes:Set}
- applyFilters() -> filtered array; render all.
- Debounce keyword 300ms.

Tab 01 tiles: total records with type breakdown; documents; years; one tile per mechanism with records, docs, latest year, share.

Theme chart: horizontal bars ranked, value at end. Click bar → add theme filter chip.

States: computed per UPR record; collect all states with counts for the filter select.

CSV export: comment lines then rows.

Copy summary: text with headline numbers and top 10 themes.

Sample check: mulberry32 seeded, draw 10 from filtered, cards with buttons Fits/Doesn't fit/Unsure, tally.

Checks panel: implement all listed checks.

Let me write it. Keep CSS calm editorial. Use hidden attribute with [hidden]{display:none!important}.

Rendering table rows: 50 at a time. Row is a button? Use tr with tabindex, click expands. Expanded row below shows details.

Let me draft the full HTML now. I'll aim for compactness while meeting requirements.

Key details:
- theme filter: clicking bar adds theme as filter chip. So themes filter exists (a Set) but no dedicated heading — chips come from chart clicks. Fine.
- Body select shows bodies present in chosen mechanism with counts.
- Type select: each type present.
- State select joins heading 02 when states extracted.
- Year selects: distinct years; swap if reversed.
- SDG: goal number and name, only goals present.

Chart clicks: onClick handler on FIG.01 gets index → theme name → toggle in themes set → re-render.

"see the States" link in UPR tile on tab 01 opens in place a short list "Ten States that made most recommendations to Kenya" with counts for current filter.

Copy citation: symbol, para. N; else symbol alone, button label "(no paragraph number in this extract)".

Copy to clipboard: navigator.clipboard.writeText with fallback? Sandboxed page may allow. Try/catch, use textarea fallback.

Let's write. I'll be careful with the check functions.

Checks:
1. Record count: records.length vs Number(uhri.count).
2. Partitions: counts per mechanism/body/year each sum to record count.
3. Type partition.
4. Chart vs table: recompute theme counts second loop; largest bar ≤ filtered count.
5. Links: doc_url starts with https://docs.un.org/ and ends with symbol (case-insensitive after decoding). List failures.
6. Paragraph numbers share per mechanism; UPR <100% warning.
7. States found: UPR records with ≥1 state vs total UPR; list failures with symbol.
8. Duplicates/gaps: distinct id count, duplicate text count, records with no themes/sdgs/affected_persons.

Random sample: seed box (default 1), Draw again (new random seed), Draw with this seed. Cards one line each, one open at a time (details-like). Each card: symbol linked, para number, full text, theme chips, three buttons, verdict. Tally line.

Mulberry32:
```js
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}
```

Draw 10 from filtered (if fewer, all).

Now write the file. Estimate ~1100 lines. Go.

Filter application:
```js
function matches(r){
 if(f.keyword){ for(const w of f.keyword) { if(!(r.text.toLowerCase().includes(w)||r.symbol.toLowerCase().includes(w))) return false; } }
 if(f.mechanism && r.mechanism!==f.mechanism) return false;
 if(f.body && r.body!==f.body) return false;
 if(f.type && r.type!==f.type) return false;
 if(f.states.size && !(r._states && r._states.some(s=>f.states.has(s)))) return false;
 if(f.yearFrom && r.year<f.yearFrom) return false;
 if(f.yearTo && r.year>f.yearTo) return false;
 if(f.sdg && !(r.sdgs||[]).includes(f.sdg)) return false;
 if(f.themes.size && !(r.themes||[]).some(t=>f.themes.has(t))) return false;
 return true;
}
```

Chips: show each active filter as removable.

Theme chip from bar click: toggle.

Render functions: renderRail, renderOverview (tiles, charts, theme table), renderTable, renderChecks (once + refresh counts?), renderMethod.

Checks should reflect current filter? The checks panel counts are about the file mostly; I'll compute on full file, with chart-vs-table check on filtered set. Simpler: run checks on full file, and chart check on filtered.

Rendering strategy: on any filter change, recompute filtered, render everything visible. Charts: destroy existing.

Table expansion: keep expandedIds Set; re-render table on filter change resets expansion (fine, keep simple—clear it).

Keyboard on rows: row tabindex=0, keydown Enter/Space toggles.

Escape HTML for text in HTML contexts: escapeHtml function.

Highlight keyword: wrap matches in <mark> in first-line column. Words are lowercased; do case-insensitive replace.

CSV: escape quotes, prepend comment lines starting with #.

Copy summary: plain text paragraph.

OK, writing now.

For FIG.02 stacked bars: labels = all years from min to max (of filtered? spec: "every year from the first to the last appears" for current filter — use min/max year of filtered, or of file? "Records per year by mechanism: stacked bars for the current filter; every year from the first to the last appears, so empty years are visible gaps." I'll use range of filtered years; if filtered empty, hide chart with "No records match".)

Colors: UPR #c2410c, Treaty bodies #0f766e, Special Procedures #7c3aed.

FIG.01 bars: red at 80% opacity: 'rgba(155,35,53,0.8)'.

Value at end of bar: use datalabels? Not available. Use a plugin? Simpler: custom inline plugin drawing text after bar. Write small plugin:
```js
const valueLabel={id:'val',afterDatasetsDraw(c){const{ctx}=c;c.data.datasets[0].data.forEach((v,i)=>{const m=c.getDatasetMeta(0).data[i];ctx.fillStyle='#1d1b18';ctx.font='12px Georgia';ctx.textBaseline='middle';ctx.fillText(String(v).replace(/\B(?=(\d{3})+(?!\d))/g,','),m.x+6,m.y);});}};
```
Only apply to FIG.01 (horizontal). Fine.

Index axis: use indexAxis:'y'.

Table under chart with same ten rows: Theme | Records | % of filtered | Years.

Tabs: buttons role=tab, aria-selected, arrow key nav.

Rail on tabs 3/4: hide headings container.

Search box on tab 02 is "the same box as 01 Keyword" — I'll have one keyword input in rail heading 01, and tab 02 has its own input synced to the same filter (two inputs, one state). Sync values.

Let me now write the whole file.

Tab 03 sample cards: "listed as one line each, one open at a time" — accordion. Each card: summary line (symbol, para, snippet) clickable; open shows full text, theme chips, three buttons. Verdict recorded.

Tally: "Themes: x fit, y don't, z unsure of N judged", with seed.

CSV columns: date, body, mechanism, type, symbol, para, recommending_states, first? "visible columns plus the full text and labels": Date, Body, Symbol, Para, Recommending State, Text, Themes, SDGs, SDG targets, Affected persons, Section, doc_url.

Write it.

Also "How this is computed" one-liners near each figure/number.

Footer: "Built on OHCHR UHRI data · n records · source link". No credits (no shelf code used).

Now produce code.