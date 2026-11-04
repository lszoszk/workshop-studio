Build a large single HTML app. Keep under ~1500 lines. Let me plan the structure and write it.

Key components:
- Header with title, country from data, source link, counts.
- Tabs: 01 Overview, 02 Records, 03 Check, 04 Method & export.
- Left rail with filters (shown on tabs 1&2; number/bar/chips only on 3&4).
- Filters: three collapsible headings: 01 Keyword, 02 Mechanism/body/type (+ State select), 03 Years and SDG.
- Overview: tiles (headline with type breakdown, documents, years; one tile per mechanism with "see the States" for UPR), FIG.01 theme bar chart with table, FIG.02 stacked per year.
- Records tab: search box, table with expandable rows, pagination 50, copy citation.
- Check tab: self checks list, random sample with seed, verdict buttons, tally.
- Method tab: method text, CSV export, copy summary, source/licence.

Deterministic computations. Let me write it carefully.

State: filters = {keyword, mechanism, body, type, state, yearFrom, yearTo, sdg, theme (chips)}.

Theme chips come from chart click. Chips removable.

Let me write the code.

Key functions:
- allRecords, applyFilters() → filtered.
- paragraphOf(text).
- statesOf(rec) → array.
- buildStateIndex: map state name → count (over recommendations only? plan says "count of recommendations" — count UPR records with that State, once per record). States extracted only from UPR records.

Filter by State: records where mechanism UPR and states include the state (or "State not found"?). Keep simple: state filter select lists states found, with counts; filter matches records whose states include the state. "State not found" option? Skip; only actual states.

Tabs: role tablist, arrow keys.

Charts: Chart.js 4, destroy/recreate on filter change.

Check panel: computed once (on whole file, and theme chart check against current filter — compute on render). I'll compute checks on render of tab 03.

CSV export: build string, Blob URL download.

Copy summary: clipboard write with fallback.

Let me count clickable things per view: tabs (4) + filter headings (3, one open; open heading reveals selects — mechanism/body/type/state are select elements within one heading; plan says count filter headings and buttons together). Fine.

Design: paper/ink palette, Georgia serif, monospace labels.

Write the code now, aiming for compactness but complete.

Highlighting keyword matches in first-line column with <mark>: need safe HTML — escape text then wrap matches. Words of keyword: highlight each word occurrence.

Sorting: date desc, body, paraNumber asc (numeric — parse "144.43" as float? plan: paragraph number ascending (numeric, so 10 follows 9)). Use parseFloat of para number; null → large? Use Infinity. Then file order. Date header click reverses (asc).

Pagination: show 50, "Show 50 more".

Expand row: details div, para number big red, full text, labels, copy citation button, open document link.

Random sample: mulberry32 seed; draw 10 from filtered (or fewer). Cards one-line collapsed, click to open (one open at a time), showing text, theme chips, three buttons. Tally stored.

Check list items: I'll compute and render lines with pass/fail.

Let me write it.

Structure of HTML:

```
<!doctype html><html><head><meta charset><meta viewport><title>...
<style>...</style></head>
<body>
<header>
  <div class="mono-label" id="hdr-label">UHRI · Kenya</div>
  <h1>...</h1>
  <p class="hdr-meta">...</p>
</header>
<nav role="tablist">4 buttons</nav>
<div class="layout">
  <aside id="rail">
    header row: FILTERS + Clear all
    big number + bar + chips
    <div id="filter-groups"> (hidden on tabs 3,4)
      3 collapsible sections
    </div>
  </aside>
  <main>
    <section id="tab1" role="tabpanel">...
    <section id="tab2">...
    <section id="tab3">...
    <section id="tab4">...
  </main>
</div>
<footer>...</footer>
<script>...</script>
```

CSS: ~150 lines. JS: ~700 lines. OK.

Let me write it in full.

Details:

Filter headings collapsible: button with aria-expanded, content div hidden. One open at a time: opening one closes others.

Mechanism filter: I'll use select elements (fewer clicks than radio buttons). Mechanism select "all" + values. Body select depends on mechanism chosen — "body values present in the chosen mechanism". Recompute body options when mechanism changes, preserving selection if still valid. Type select: values present (in chosen mechanism? plan: "each value present" — present in data, maybe filtered by mechanism too; I'll use present under current mechanism+body? Keep: present under chosen mechanism). Simpler: present in the whole file? Plan: "Type (all / each value present)". I'll use present under mechanism filter. Fine.

State select joins heading 02. States list: computed over UPR records (all file, or under current filters?). I'll compute over records matching keyword/mechanism etc. but excluding state filter itself — simpler: over all UPR records in file with counts, plus filter by state. Counts shown. Keep simple: all UPR records in file.

Actually let me compute state counts over the current filtered set excluding state filter — nice. But could be empty → disable. I'll just do: state options from all UPR records in file. Simple, deterministic.

Year selects: distinct years sorted. Swap reversed.

SDG select: goals present, "5 · Women & girls"? sdg_names keys are strings of numbers. Format "05 — name"? Use "5: name".

Theme filter chips from chart click; also chips for all active filters: keyword, mechanism, body, type, state, years (if not full range), sdg, theme(s). Each chip removable. Simplify: chips with data-key; click removes that filter (theme chip removes that theme).

Multiple theme chips allowed? Chart click adds theme as a filter chip — one theme filter at a time is enough; clicking another replaces it. I'll allow multiple themes with OR within themes? Plan says filters combine AND. Keep single theme slot; clicking new theme replaces.

Overview tiles: headline (filtered count, type breakdown), documents, years; per-mechanism tiles. That's 3 + 3 = 6 tiles. Fine.

"see the States" in UPR tile opens in-place list of ten states most recommendations.

FIG.01: chart with top 10 themes; click bar → theme filter. Table under.

FIG.02 stacked bars per year by mechanism with 3 colors.

Records tab table: caption, columns Date | Body | Symbol | Para. | First line | State. Row click expands. Buttons inside row for copy etc.

Check tab: run checks on demand? Compute when tab shown.

CSV: columns date, body, mechanism, type, symbol, doc_url, paragraph, recommending_states, section, themes (joined ;), sdgs, sdg_targets, affected_persons, text.

Copy summary: text paragraph.

Write the JS.

Helper: fmt(n) with thousands separator (toLocaleString('en-GB')? Use Intl or manual regex: n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") — but decimals... only ints here).

mulberry32:
```
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
```

Sample: seed from input (integer). Draw indices from filtered set: pick via rng.

Verdicts: store array of verdicts keyed by record id; tally counts fit/dont/unsure of judged. Reset on redraw.

Charts: keep refs, destroy before recreate. Only create when tab visible; call render on tab switch.

For bar click: onClick option in Chart.js: getElementsAtEventForMode.

Chart bar color #9b2335 at 80% alpha: 'rgba(155,35,53,0.8)'.

Stacked: datasets per mechanism, colors given.

Table under chart: ten rows.

Chart vs table check on tab 3: recompute counts with second loop and compare — trivially same function... do an actual second independent loop inline in check.

Link check: decodeURIComponent(url) lowercase endsWith symbol lowercase.

Paragraph share per mechanism.

States check: UPR records with ≥1 state; list those without (symbol + the trailing parens content? just symbol).

Duplicates: distinct ids, duplicate texts count.

Not labelled: counts.

OK, write it. Aim ~1100 lines.

Row expansion in table: each tr followed by hidden detail tr. Row is button-like: tabindex=0, keydown Enter/Space.

Let me write out the whole file.

Filtering function:

```
function applyFilters(){
  const kw = state.keyword.trim().toLowerCase();
  const words = kw? kw.split(/\s+/):[];
  return data.records.filter(r=>{
    if(state.mechanism && r.mechanism!==state.mechanism) return false;
    if(state.body && r.body!==state.body) return false;
    if(state.type && r.type!==state.type) return false;
    if(state.state && !(r.mechanism==='Universal Periodic Review' && statesOf(r).includes(state.state))) return false;
    if(state.yearFrom && r.year<state.yearFrom) return false;
    if(state.yearTo && r.year>state.yearTo) return false;
    if(state.sdg!=null && !(Array.isArray(r.sdgs)&&r.sdgs.includes(state.sdg))) return false;
    if(state.theme && !(Array.isArray(r.themes)&&r.themes.includes(state.theme))) return false;
    if(words.length){const hay=(r.text+' '+(r.symbol||'')).toLowerCase(); if(!words.every(w=>hay.includes(w))) return false;}
    return true;
  });
}
```

state.sdg stored as number.

statesOf with memo cache by record id.

State counts: iterate UPR records, for each state found (accepted), count record once.

Rendering: renderAll() on filter change: update rail, overview (if tab1 active), records table, and mark charts dirty. Simpler: render functions check active tab; render on tab switch too.

Table sorting: sortKey 'date' direction desc default; header click toggles.

sortRecords(list):
```
const d = state.sortAsc?1:-1;
list sorted by: date compare *d, then body localeCompare, then para asc, then index.
```
Wait: default date desc, body asc, para asc. Clicking Date reverses whole order (plan: "clicking the Date header reverses it"). I'll flip date direction only.

Para number: parseFloat(para) works for "144.43".

Highlight: escape HTML then wrap word matches with <mark>. Case-insensitive: use regex per word with 'gi' after escaping — careful escaping changes text; match on escaped string with escaped word. Words are plain text; escape them too.

Copy citation: navigator.clipboard.writeText with fallback textarea.

CSV: quote fields, escape quotes, prefix comment lines starting with "#".

Let me now write the final file.

Rail on tabs 3/4: hide filter groups (add [hidden]).

Accessibility: tabs with role=tab, aria-selected, panels role=tabpanel; arrow keys.

I'll write the code now, being careful but concise.

Tiles for mechanism: use filtered-set counts but mechanism tile shares... each mechanism tile: records (in filtered set? if a mechanism filter is on, others show 0 — that's fine and honest). Plan: "(records, documents, latest year, share of the filtered set)". OK.

Theme year range computed over filtered records carrying theme.

Percentage: count / filtered n, one decimal.

FIG.02: years from min to max of filtered (or full file? "every year from the first to the last appears" — use filtered min-max; if empty, show message). Use full file year range? If filter narrows years, showing empty years outside range is noise. Use filtered min–max.

Legend for FIG.02: Chart.js legend.

Check panel details — compute once per tab visit on current filter? Counts like "records with no themes" are file-level. Theme chart check uses current filtered set. I'll compute file-level checks each time (cheap) and chart check against current filtered set.

Sample seed box default 1, "Draw again" (increments? plan: draws cards, then "Draw again" and "Draw with this seed"). "Draw again" → new random seed? Keep: Draw again uses seed+1 and updates box. Draw with this seed reads box.

Let me write.

Estimate lines: fine.

One more: header "UHRI · Kenya" — country from data.

Footer: "Built on OHCHR UHRI data · n records · source link". Credits: analysis function sources? They're guidance documents consulted, not code. No shelf code used, so no Credits line needed. Plan says "plus a 'Credits' line if any shelf code was used" — none. But sources consulted listed in method tab as sources. Fine.

Write now.