Build the full app per plan. One HTML file, under ~1500 lines. Let me write it carefully but compactly.

Key components:
- header, tabs (4), left rail filters (3 collapsible headings, keyword, mech/body/type/state, years/SDG), chips, share bar.
- Tab 01: tiles (all records + type breakdown, documents, years, mechanism tiles), FIG.01 chart + table, FIG.02 stacked bar.
- Tab 02: search box, table with expand rows, states column, pagination.
- Tab 03: checks panel + random sample.
- Tab 04: method, CSV export, copy summary.

Data: WORKSHOP_DATA.uhri. Note plan says only uhri attached — use only uhri.

Let me write the code. I'll keep it organized. Aim ~900 lines.

Design: off-white #f4f0e8, ink #1d1b18, rules #d9d2c3, red #9b2335. Mechanism colors: UPR #c2410c, TB #0f766e, SP #7c3aed.

Tab structure: role tablist with arrow keys. Filter rail hidden on tabs 3/4 (keep number/bar/chips). Actually plan: on 03/04 the rail keeps only the number, the bar and the chips. So hide the filter headings on tabs 3&4.

State extraction regex per plan.

Paragraph number regex: /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/.

Checks: implement each.

Random sample: mulberry32, seed box, draw 10, cards with themes chips, three buttons Fits/Doesn't fit/Unsure, tally.

CSV export with comment lines. Copy summary.

Let me write it now.

Filter state object: {keyword, mechanism, body, type, state, yearFrom, yearTo, sdg}. Chips removable.

Table sorting: date desc default, toggle via Date header click.

I'll write the whole file.

Details for tab 02 table columns: Date | Body | Symbol | Para. | First line | Recommending State. Row click expands in place with full detail. Keyboard Enter.

Pagination: 50 rows + "Show 50 more" button.

Search field on tab 02 same as keyword filter — I'll have one input in rail; tab 02 also shows a search field at top. To keep simple: the tab-02 search input syncs with the keyword filter (two inputs, both update same state). Simpler: render one input in tab 02 that mirrors rail input. I'll have both inputs and sync values.

Checks list: computed on full file (not filtered). Records without paragraph per mechanism etc.

Links check: url starts with https://docs.un.org/ and ends with symbol after decoding, case-insensitive.

CSV: visible columns + full text + labels; comment lines starting with #.

Copy summary: headline numbers + top ten themes, plain text.

Let me count clickable things: rail: 3 filter headings (one open at a time → open one shows its controls: keyword input; mech/body/type/state selects — that's 4 selects but they're within one panel, fine-ish; plan says it). Tabs 4. OK.

Write code now. Use Chart.js from window.Chart.

I'll produce the file, ~1000 lines. Keep it tight.

Edge: filters change → recompute filtered, render current tab.

Let me write.

Structure:

```html
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>...</title><style>...</style></head>
<body>
<header>...</header>
<nav tabs>
<div id="app">
  <aside id="rail">
    <div>FILTERS ... Clear all</div>
    <div class="bignum" id="matchCount" aria-live="polite"></div>
    <div class="bar"><i id="shareBar"></i></div>
    <div id="chips"></div>
    <div id="filterHeadings">
      heading 01 keyword (panel: input)
      heading 02 mechanism body type state (panel: 4 selects)
      heading 03 years sdg (panel: 4 selects)
    </div>
  </aside>
  <main>
    <section id="tab1">tiles, fig01 (canvas+table), fig02</section>
    <section id="tab2">search, table</section>
    <section id="tab3">checks, sample</section>
    <section id="tab4">method, export</section>
  </main>
</div>
<footer>
<script>...</script>
```

Filters render: body select depends on chosen mechanism. State select built from extracted states (counts). SDG select from sdg_names filtered to present goals. Year selects distinct years sorted.

Note: sdg_names keys — in data description "16": "..." — keys are strings of goal numbers. Present goals from records' sdgs arrays.

Keyword: every word must occur in text or symbol.

Render tiles: mechanism colors dots.

FIG.01: horizontal bar, top 10 themes, click bar → add theme filter? Wait — plan says clicking a bar adds that theme as a filter chip. But there's no theme filter heading... Hmm. "Clicking a bar adds that theme as a filter chip." So theme filter exists as a chip (not in a heading). OK: filter state has `themes` set; chips removable. Fine.

Chart click: Chart.js onClick getElementsAtEventForMode.

FIG.02: stacked bar per year per mechanism, all years from min to max.

Number formatting: toLocaleString.

Paragraph display in table: number or "—".

Row expand: detail div inside a tr? Use a second tr with colspan. Rows clickable (click on tr toggles). Use tabindex=0 on tr, Enter toggles.

Copy citation: navigator.clipboard.writeText, fallback textarea. Show "Copied" 2s.

Checks: build array of {label, ok, detail}. Render lines.

Sample: seed input, draw again (increment seed? "Draw again" draws a new random seed), draw with this seed. Cards: one open at a time? Plan: "The ten cards are listed as one line each, one open at a time." So cards are collapsed lines; clicking opens the card showing full text + themes + verdict buttons. Implement like accordion.

Verdict buttons record tally.

Tally line: "Themes: x fit, y don't, z unsure of 10 judged".

CSV export: Blob download.

Copy summary: clipboard plain text.

Let me write everything now carefully.

Time to write. I'll be disciplined about length.

For the sort: date desc, then body, then para asc, then file order. Clicking Date header reverses date order (asc). I'll implement `sortAsc` toggle.

Highlight keyword matches in first line with <mark>: escape HTML then wrap occurrences of each word (case-insensitive).

Escape function needed.

State extraction:

```js
function states(r){
  if(r.mechanism!=="Universal Periodic Review") return null;
  const m = r.text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
  if(!m) return ["State not found"];
  const groups = m[1].match(/\((?:[^()]|\([^()]*\))*\)/g)||[];
  const out = groups.map(g=>g.slice(1,-1).trim()).filter(g=>g.length&&g.length<=60&&!g.includes(","));
  return out.length?out:["State not found"];
}
```
Cache per record via map.

Year selects swap if reversed: on change, if from > to, swap values.

Chips: show keyword, mechanism, body, type, state, years, sdg, themes. Each removable.

Rail on tabs 3/4: hide #filterHeadings.

OK writing now. Also hidden attribute CSS rule.

"see the States" link in UPR tile on tab 01: toggles in-place list of ten states with counts.

Let me draft the code.

For check "Chart against table": recompute counts with second loop, compare — trivially same code; I'll write a second independent count loop.

Duplicate texts: count of text values appearing >1 times → number of extra records? Plan: "the number of duplicate `text` values". I'll count values with >1 occurrences.

Let me finalize and write the HTML.