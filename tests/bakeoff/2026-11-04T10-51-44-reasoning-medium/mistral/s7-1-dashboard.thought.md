Let me plan this app carefully. The user wants a full dashboard on `WORKSHOP_DATA.uhri` with four tabs, filters rail, checks, export. This is a big build. I need to write one complete HTML file, under ~1500 lines, all inline, Chart.js preloaded.

Key requirements:
- Header: monospace label "UHRI · {country}", serif title, one line with source (linked), n records, n documents, first–last year, built date, "dated by document" hint.
- Left rail filters: FILTERS heading + Clear all; big serif number matching records with aria-live, "of N in the file", red share bar; chips; three numbered accordion headings (01 KEYWORD, 02 MECHANISM/BODY/TYPE, 03 YEARS & SDG), one open at a time, aria-expanded. On tabs 03/04 rail keeps only number, bar, chips (hide the accordions).
- Tab 01 Overview: big number tiles (total records with type breakdown, documents, years), one tile per mechanism (records, documents, latest year, share of filtered set). FIG.01 top-10 themes horizontal bar chart (Chart.js), click bar adds theme filter chip; table under with Theme | Records | % | Years. FIG.02 stacked records per year by mechanism. "see the States" link in UPR tile opening in-place list of top 10 States.
- Tab 02 Records: search field (same as keyword), table with Date | Body | Symbol | Para. | First line | Recommending State; sorted date desc, body, para numeric asc, file order; click Date header reverses; mark highlights; 50 rows + "Show 50 more"; row expand in place with full text, labels, Copy citation, Open UN document.
- Tab 03 Check: self-check panel lines; random sample of 10 with seeded mulberry32, seed box default 1, Draw again, Draw with this seed, cards one open at a time, Fits/Doesn't fit/Unsure buttons, tally line.
- Tab 04 Method & export: method sentences, Download CSV (Blob), Copy summary, source/licence/build.
- Footer one line monospace.

State extraction: regex on UPR only. Paragraph number regex `/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/`.

Checks: record count vs Number(count); partitions per mechanism/body/year sum; type partition; chart vs table recompute; links doc_url starts with https://docs.un.org/ and ends with symbol (case-insensitive after decoding); paragraph share per mechanism, UPR expected 100%; states found count vs UPR count, list failures; distinct id == count, duplicate texts, missing labels counts.

Filters: keyword (300ms debounce, every word substring of text or symbol, lowercased trimmed), mechanism, body, type, state, year from/to, sdg. All AND. Chips removable. Clear all.

Theme filter: clicking a bar adds theme chip — so there must be a theme filter too. The plan says filters are three headings: keyword, mechanism/body/type (+state), years & SDG. Theme chip added from chart click — chips area shows it; need a way to remove (chip ×). But also maybe theme should be in a filter heading? The plan says three numbered headings only; theme chip appears as removable chip. But then how to add theme filter other than chart click? That's fine — chip appears when bar clicked. But chips need to be removable and the filter state must include theme. I'll keep a `theme` filter (single? or multiple?). Plan says "Clicking a bar adds that theme as a filter chip" — could be multiple themes ANDed? Simpler: allow multiple theme chips, AND semantics (record must carry all selected themes). Hmm, or single theme. I'll allow multiple, AND — chips removable. Actually to keep simple: theme filter is a set; record matches if it includes all selected themes. Fine.

Wait — "no view shows more than about seven things to click (tabs, filter headings and buttons together)". Tabs = 4, filter headings = 3, Clear all = 1 → 8. Hmm, that's slightly over 7 but "about seven". The plan explicitly requires 4 tabs + 3 headings + clear all. I'll follow the plan; it says "about seven". Fine.

On tabs 03/04, rail shows only number, bar, chips — hide accordion headings (and keyword box? The keyword box is inside heading 01). Yes hide the whole accordion container on tabs 3/4.

Layout: header, then a flex row: left rail (narrow, ~240px) + main content with tablist and panels.

Tab navigation: role="tablist", buttons role="tab" aria-selected, panels role="tabpanel", arrow keys left/right.

Charts: FIG.01 horizontal bar (indexAxis: 'y'), Chart.js 4. Bars red at 80% opacity: 'rgba(155,35,53,0.8)'. Click handler on chart: get element index → theme → add chip. Value labels at end of bar: use a plugin to draw values, or just rely on ticks. Plan says "count at the end of each bar" — implement a small plugin drawing the value text after the bar end.

FIG.02 stacked bar per year, datasets per mechanism with colors UPR #c2410c, Treaty bodies #0f766e, Special Procedures #7c3aed. Years from min to max of full file (or filtered? "every year from the first to the last appears" — first to last of the file presumably; I'll use file min–max so gaps visible; but if year filter applied, maybe use filtered range? Plan: "Records per year by mechanism: stacked bars for the current filter; every year from the first to the last appears, so empty years are visible gaps." I'll use the full file's year range so gaps are visible regardless; actually if filtered, years outside filter show 0 — that's fine and shows gaps. Use file min–max.)

Chart re-render on filter change: destroy and recreate, or update data. I'll create once and update.

Table: build rows via JS. 50 at a time, "Show 50 more" button. Row click toggles expanded detail row (a second <tr> with colspan). Keyboard: rows as <tr tabindex="0"> with Enter handler. aria-expanded on the row? Plan says expandable rows are buttons with aria-expanded — I'll make the first cell content a button? Simpler: make the row focusable and set aria-expanded on the row element. Acceptable.

Highlight keyword matches with <mark> in first line and expanded text.

Copy citation: navigator.clipboard.writeText with fallback (execCommand). Show "Copied" for 2s.

CSV export: comment lines starting with # : country, source, build date, filters applied, row count; then header row: Date, Body, Mechanism, Type, Symbol, Doc URL, Paragraph, Recommending State(s), Section, Themes, SDGs, SDG targets, Affected persons, Text. Blob download.

Copy summary: plain text with headline numbers and top ten themes.

Random sample: mulberry32 seeded; draw 10 distinct records from filtered set. Seed box default 1. "Draw again" (new random seed? or same seed redraw — same set; better: Draw again increments seed or picks random seed and shows it). Plan: "Draw again" and "Draw with this seed", seed box and tally. I'll do: Draw again → seed = random integer, redraw; Draw with this seed → use seed in box. Cards listed one line each, one open at a time (accordion). Each card: symbol link, para number, full verbatim text, theme chips, three verdict buttons. Tally: "Themes: x fit, y don't, z unsure of 10 judged · seed N". Verdicts stored in memory (per draw). One verdict per card — clicking again changes? "One verdict per card" — I'll allow re-click to change, tally recomputed. Simpler: store verdict per card id; clicking sets it.

Self-check panel lines: compute all checks at load (and they don't depend on filter except chart-vs-table which uses filtered set — recompute on filter change? The plan says chart against table check recomputes over filtered records. I'll recompute checks on each filter change for the chart check; others are file-level. Simpler: run all checks on load and re-run the chart check on filter change. Actually just re-run all checks on filter change — cheap enough (2264 records). Fine.

Link check: doc_url starts with "https://docs.un.org/" and ends with symbol case-insensitively after decoding (decodeURIComponent, compare lowercase). List failures.

Paragraph share per mechanism: share with number found; UPR expected 100%, lower → warning.

States found: UPR records with ≥1 state vs UPR total; list those without (symbol + maybe trailing text snippet).

Duplicates: distinct id count vs record count; duplicate text values count (number of records whose text appears more than once? "the number of duplicate text values" — count of texts occurring >1 time, or extra records? I'll show "n texts occur more than once (m extra records)". Keep simple: count of duplicate text values = number of distinct texts with count>1. Hmm "the number of duplicate `text` values" — I'll report distinct duplicated texts and total records involved.

Missing labels: records with no themes, no sdgs, no affected_persons — "each shown as 'not labelled'".

Now sizes: 2264 records, table rendering 50 rows fine.

Sorting: date desc (string compare works for ISO dates), then body asc, then paragraph numeric asc (parse "144.43" → 144.43; no number → Infinity? Plan: "then paragraph number ascending (numeric, so 10 follows 9), then the order in the file". Records without number — put after? I'll use numeric value or Infinity), then file order (index).

Date header click reverses sort (toggle asc/desc), caption says "newest first" or "oldest first".

First line: up to 120 chars, cut at last space before limit, plus "…". If text shorter, whole text.

Para column: number or "—".

State column: UPR → states joined ", " or "State not found"; others "—".

State select filter: list every State found with counts (in current... counts computed over file or filtered-by-other-filters? Simplest: counts over the file, or over records matching other filters? To keep deterministic and simple, compute over the whole file; but nicer over current filter minus state. I'll compute over records matching all filters except state. That's fine.)

Body select: values present in chosen mechanism (with counts) — counts over file within mechanism.

Year selects: distinct years present in file (sorted). From/to; if from > to swap.

SDG select: goals present in data with names from sdg_names. sdg_names keys are strings "16". Record sdgs are numbers. Match Number.

Keyword: words split on whitespace; each word lowercase substring of (text + " " + symbol).toLowerCase().

Debounce 300ms.

Chips: for each active filter (keyword, mechanism, body, type, state, theme(s), year range if not full, sdg) show chip with × removing it.

Share bar: width % = matching/N*100, red.

Mechanism tiles: for each mechanism value in data: records (in filtered set), documents (distinct symbols in filtered), latest year (max year in filtered), share of filtered set. Plus "see the States" link in UPR tile → toggles a small list "Ten States that made most recommendations to {country}" with counts for current filter (UPR records in filtered set).

Wait — the UPR tile is per mechanism; the States link only in the UPR tile. Mechanism value is "Universal Periodic Review".

Header line: source linked to source_url, n records (records.length), n documents, first–last year, built, "dated by document".

Footer: "Built on OHCHR UHRI data · n records · source link".

Credits line: sources consulted — the plan lists sources; those are references, not code with licence. "add a small Credits line at the bottom of the app naming the source and its licence" — only if code/wording from shelf excerpts with open licence. We didn't use shelf code. But I can add a credits line naming data source. The footer covers it. I'll add a small credits line in tab 04: "Data: OHCHR Universal Human Rights Index (UHRI). Design guidance: UK Government Analysis Function (Open Government Licence); citation practice: UN Dag Hammarskjöld Library Ask DAG." That's fine.

Now, code structure. Let me write it.

HTML skeleton:

```
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
<div class="layout">
  <aside id="rail">...</aside>
  <main>
    <div role="tablist" id="tabs">4 buttons</div>
    <section id="panel-0" role="tabpanel">...</section>
    ...
  </main>
</div>
<footer>...</footer>
<script>...</script>
</body>
</html>
```

CSS: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335. Fonts: Georgia serif for title/numbers; ui-monospace for labels; system sans 16px body.

Let me now write the JS carefully.

Data access:
```js
const U = window.WORKSHOP_DATA.uhri;
const records = U.records;
const country = U.country;
const sdgNames = U.sdg_names || {};
```

Precompute per record: para number, states (UPR), firstLine, lower text.

```js
const PARA_RE = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
function paraOf(t){ const m = String(t||"").match(PARA_RE); return m ? m[1] : null; }
const STATE_RUN_RE = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const STATE_GROUP_RE = /\((?:[^()]|\([^()]*\))*\)/g;
function statesOf(r){
  if (r.mechanism !== "Universal Periodic Review") return null;
  const m = String(r.text||"").match(STATE_RUN_RE);
  if(!m) return [];
  const groups = m[1].match(STATE_GROUP_RE) || [];
  const out = [];
  for(const g of groups){
    const name = g.slice(1,-1).trim();
    if(name.includes(",") || name.length > 60){ return ["State not found"]; }
    out.push(name);
  }
  return out.length ? out : ["State not found"];
}
```

Hmm — "A group is accepted as a State only if it has no comma and at most 60 characters; otherwise the record gets 'State not found'." So if any group fails, whole record → "State not found"? Reading: "otherwise the record gets 'State not found'". Yes, if a group fails the rule, the record gets State not found. I'll implement: if any group invalid → return ["State not found"]. Actually maybe just that group is rejected... but plan says record gets "State not found". Follow plan.

Wait, but nested "Venezuela (Bolivarian Republic of)" has no comma, length fine → accepted as "Venezuela (Bolivarian Republic of)". Good.

Filter state:
```js
const F = { keyword:"", mechanism:"all", body:"all", type:"all", state:"all", theme:new Set(), yearFrom:null, yearTo:null, sdg:"all" };
```
yearFrom/yearTo default = min/max year of file (so "all"). Chip shown only when narrowed.

matching(r):
```js
function matches(r){
  if(F.mechanism!=="all" && r.mechanism!==F.mechanism) return false;
  if(F.body!=="all" && r.body!==F.body) return false;
  if(F.type!=="all" && r.type!==F.type) return false;
  if(F.state!=="all" && !(r._states && r._states.includes(F.state))) return false;
  for(const t of F.theme){ if(!r.themes || !r.themes.includes(t)) return false; }
  if(r.year < F.yearFrom || r.year > F.yearTo) return false;
  if(F.sdg!=="all" && !(r.sdgs && r.sdgs.map(Number).includes(Number(F.sdg)))) return false;
  if(F.keyword){ const hay = (r.text+" "+r.symbol).toLowerCase(); for(const w of F.keyword.toLowerCase().split(/\s+/).filter(Boolean)){ if(!hay.includes(w)) return false; } }
  return true;
}
```

Precompute r._para, r._states, r._hay.

Filtered = records.filter(matches). Recompute on each filter change → renderAll().

Rendering: I'll write render functions: renderRail (count, bar, chips), renderOverview, renderRecords, renderChecks, renderMethod. To keep it manageable, full re-render of active panel on filter change; table keeps its own state (visibleCount, sortDir, expanded set) — I'll keep expanded rows keyed by id across re-renders? Simpler: on filter change, reset visibleCount to 50 and clear expanded. Acceptable.

Actually re-rendering the table on every keystroke (debounced 300ms) resets scroll of table... fine.

Chart handling: create charts lazily when tab 01 first shown; update on filter change if exists. Chart.js bar click: 

```js
options: { onClick: (e, els) => { if(els.length){ const t = themeData[els[0].index].theme; addTheme(t); } } }
```

Value labels plugin:
```js
const valueLabels = { id:'valueLabels', afterDatasetsDraw(chart, args, opts){ ... } };
```
For horizontal bar, draw text at x = meta.data[i].x + 4, y = ... Use chart.ctx. Only register on FIG.01.

FIG.02 stacked: type 'bar', options scales x stacked, y stacked.

Tabs: buttons with data-tab index; arrow key nav; show/hide panels; on tab 3/4 hide rail accordions (add class to rail). Also when tab 02 shown, focus? no.

Accordion headings: three buttons in rail; clicking toggles; only one open (close others). aria-expanded.

Keyword input: input event → debounce 300ms → F.keyword = value.trim(); applyFilters().

Records tab search field: same as keyword — "the same box as 01 Keyword". Two inputs synced: I'll have one input in rail (inside heading 01) and one at top of tab 02; sync values both ways. Both update F.keyword.

Table build:
```js
function renderTable(){
  const rows = filtered.slice().sort(cmp);
  ...
}
```
cmp with sortDir: date desc default; if reversed, asc. Then body, para numeric, index.

Para numeric: parseFloat(para) or Infinity.

Build HTML string for rows; attach event delegation on tbody: click on tr[data-id] toggles expand; keydown Enter/Space.

Expanded row: `<tr class="detail"><td colspan="6">...` with para big red, full text (with mark highlight), labels, buttons Copy citation / Open document. Buttons inside detail row: stopPropagation.

Copy citation: 
```js
function citation(r){ return r._para ? `${r.symbol}, para. ${r._para}` : r.symbol; }
```
Button label: "Copy citation" or "Copy citation (no paragraph number in this extract)".

Clipboard: navigator.clipboard?.writeText fallback textarea+execCommand. Show "Copied ✓" for 2s on the button.

Highlight: escape HTML then wrap keyword words with <mark>. Need escaping function. Words: split keyword; for each word, regex escape, replace in escaped text? Careful: escape first, then mark — but escaping changes chars (& → &amp;) and keyword words are plain; if keyword contains "&" it wouldn't match escaped text. Edge case, acceptable. Better: do highlighting on raw text with mark, then escape? Then marks get escaped. Approach: split raw text by regex of words, escape each piece, join with <mark>escaped word</mark>. Implement:

```js
function highlight(text){
  const words = F.keyword.toLowerCase().split(/\s+/).filter(Boolean);
  if(!words.length) return esc(text);
  const re = new RegExp("(" + words.map(escRe).join("|") + ")", "gi");
  return text.split(re).map(p => re.test(p) ? "<mark>"+esc(p)+"</mark>" : esc(p)).join("");
}
```
Note re.test with /g advances lastIndex — use a fresh non-global test or use match. Use `p.match(re)`? Simpler: since split with capture group, odd indices are matches. `text.split(re)` with capture → matched separators at odd indices. So map: i%2===1 → mark. But if keyword empty handled. Good.

First line: 
```js
function firstLine(t){ t=String(t||""); if(t.length<=120) return t; let cut=t.slice(0,120); const sp=cut.lastIndexOf(" "); if(sp>0) cut=cut.slice(0,sp); return cut+"…"; }
```

Theme counts:
```js
function themeCounts(list){ const m=new Map(); for(const r of list){ for(const t of (r.themes||[])) m.set(t,(m.get(t)||0)+1); } return [...m.entries()].map(([theme,count])=>({theme,count, years: yearRange of records carrying})).sort((a,b)=> b.count-a.count || a.theme.localeCompare(b.theme)); }
```
Year range per theme: need min/max year of filtered records carrying theme — compute in same pass: track {count, min, max}.

Top 10 = slice(0,10).

FIG.01 chart data: labels themes, data counts. Table under: same 10 rows.

Click bar → addTheme(theme): F.theme.add; applyFilters (chip appears). But if already present, ignore.

Mechanism tiles: for each mechanism value (sorted by count desc? or fixed order?). Values: "Treaty bodies", "Universal Periodic Review", "Special Procedures". I'll order by count desc. Tile: mechanism name, big number records, line: "n documents · latest YYYY · NN% of filtered". UPR tile gets "see the States" button toggling states list.

States list: top 10 states by count among filtered UPR records: count per state (record counts once per state). "Ten States that made most recommendations to {country}".

Overview tiles row: 
- Tile 1: big number = filtered.length? Wait: "The first tile counts all records in the file" — hmm: "A row of big serif numbers. The first tile counts **all records** in the file: recommendations, concerns/observations and any other type. Under the number, one line gives the breakdown per type". But filters... "Beside it: documents (distinct symbol) and years (min–max of year). Below, one tile per mechanism (records, documents, latest year, share of the filtered set)."

Ambiguity: first tile counts all records in file, or filtered? The mechanism tiles reference "share of the filtered set", implying tiles respond to filter. I think the first tile should show the filtered count (the dashboard's headline = matching), with type breakdown of the filtered set. But plan says "counts all records in the file". Hmm. The rail already shows matching count. The overview first tile: I'll show filtered count with type breakdown of filtered set, and note "of N in the file" — that satisfies both readings and is more useful. Actually re-reading: "The first tile counts all records in the file: recommendations, concerns/observations and any other type. Under the number, one line gives the breakdown per type, spelled as in the data. The Type filter (all / each type value present) starts on 'all'." The mention of the Type filter starting on "all" suggests the tile responds to the type filter. I'll make the first tile = filtered count, breakdown per type of filtered set, with "of N in the file" sub-line. Documents and years tiles: of the filtered set (documents distinct symbol in filtered; years min–max of filtered). Hmm but "years (min–max of year)" — of filtered. OK.

Each tile has "How this is computed" note.

FIG.02: years from fileMin..fileMax, datasets per mechanism present in data (all three, with 0s). Colors mapping: mechanism → color; unknown mechanisms get fallback gray. Legend built-in (Chart.js legend) plus labels. Plan: "Mechanism colours only on the tile dots and in FIG.02 ... always with a label or legend." Chart.js legend shows labels. Tile dots: small colored dot before mechanism name.

Tab 03 checks: build lines array of {label, detail, status: pass/warn/fail}. Render as list. Checks:

1. Record count: records.length vs Number(U.count) → pass/fail.
2. Partitions: mechanism counts sum, body counts sum, year counts sum == records.length.
3. Type partition sums.
4. Chart vs table: recompute top-10 theme counts with second loop; compare to chart data; largest bar ≤ filtered count. (Run on current filter.)
5. Links: every doc_url starts with "https://docs.un.org/" (case-insensitive?) and ends with symbol (decodeURIComponent both, lowercase). List failing symbols.
6. Paragraph numbers: share per mechanism with para found; UPR expected 100%, lower → warning.
7. States: UPR with ≥1 state (not "State not found") vs UPR total; list records without (symbol + last 60 chars of text).
8. Duplicates/gaps: distinct id count vs records.length; duplicate texts count; missing themes/sdgs/affected_persons counts labelled "not labelled".

Random sample: 
```js
function mulberry32(a){ return function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; } }
```
Draw 10 distinct indices from filtered: use rng, pick floor(rng()*n), dedupe. If filtered < 10, draw all (say "only n available"). Seed box input value default "1". Buttons: "Check 10 at random" (initial draw with seed 1), "Draw again" (random seed), "Draw with this seed" (parse box). Cards: list of details/summary? "listed as one line each, one open at a time" — use button + panel accordion like rail. Each card line: "symbol · para N" button; panel: full text, theme chips, three verdict buttons. Tally line above: "Themes: x fit, y don't, z unsure of 10 judged · seed N · your judgement, nothing is sent anywhere".

Verdict storage: Map cardId→verdict. Tally recompute.

Tab 04: method sentences (5-6), CSV download button, copy summary button, source/licence/build lines.

CSV: 
```
# Country: Kenya
# Source: OHCHR UHRI ... (U.source, U.source_url)
# Built: U.built
# Filters: keyword=..., mechanism=..., ...
# Rows: n of N
Date,Body,Mechanism,Type,Symbol,Document URL,Paragraph,Recommending State(s),Section,Themes,SDGs,SDG targets,Affected persons,Text
```
CSV escaping: wrap in quotes if contains , " \n; double quotes.

Blob: `new Blob([csv], {type:"text/csv"})`, a.download = "uhri-kenya-filtered.csv" (country slug). Click.

Copy summary: text with headline numbers + top 10 themes; clipboard; "Copied" feedback.

Footer: "Built on OHCHR UHRI data · {n} records · <a>source</a>".

Now the "How this is computed" lines: near each chart/number.

Let me also handle: on tabs 03/04 rail keeps only number, bar, chips → add class `rail-min` to aside when tab index 2 or 3: CSS `.rail-min .acc { display:none }`.

Chips: container in rail under bar. Chip: `<button class="chip" data-k="mechanism">Mechanism: X ×</button>` click removes.

Clear all: resets F to defaults, syncs inputs, applyFilters.

Year selects: options = distinct years sorted asc; from default min, to default max. On change: if from>to swap (set both). Chip "Years: 2010–2020" when narrowed.

SDG select: options from goals present: collect set of sdgs across records (numbers), map to name via sdgNames[String(g)] || "SDG g". Option value = g. Chip when not all.

State select: appears in heading 02 when states extracted (always, since UPR exists). Options: all states found in file with counts (over file? over current non-state filters — I'll compute over records matching all filters except state). Rebuild options on each applyFilters (cheap). Keep selected if still present.

Body select: options = bodies within F.mechanism (if mechanism all → all bodies) with counts over file. If F.body not in options after mechanism change → reset to all.

Type select: types present in file (or within current mechanism/body? plan: "Type (all / each value present)" — present in data; I'll compute within current mechanism+body filter for usefulness... simpler: all types in file. Hmm "each value present" — in the data. I'll do within current mechanism/body selection to be more useful; but keep simple: all values present in file. Actually if mechanism=UPR, type options still show all three — fine, AND semantics handle it. Keep file-level.)

Mechanism select: all values present.

Now counts in selects: counts over file (or over other filters?). Keep file-level counts for mechanism/type; body counts within mechanism. Fine.

Rendering performance: applyFilters → recompute filtered, render rail, render active panel, update charts if exist, re-run checks (tab 03) — checks include chart-vs-table over filtered; run always but only render if tab 3 active. 2264 records loops — trivial.

Table render: only when tab 02 active. But caption "rows shown of rows matching" — fine.

Let me make render functions idempotent: renderAll() calls renderRail(); renderOverview() if tab0; renderRecords() if tab1; renderChecks() if tab2; method is static except maybe counts — render once.

Charts: create on first render of overview; update data on subsequent. Chart.js: `chart.data.labels=...; chart.data.datasets[0].data=...; chart.update()`. For FIG.02 update datasets. Click handler uses current themeData variable.

Value label plugin for FIG.01:

```js
const endLabels = {
  id: 'endLabels',
  afterDatasetsDraw(chart){
    const meta = chart.getDatasetMeta(0);
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = '12px ui-monospace, Menlo, monospace';
    ctx.fillStyle = '#1d1b18';
    meta.data.forEach((bar, i) => {
      const v = chart.data.datasets[0].data[i];
      ctx.fillText(String(v), bar.x + 6, bar.y + 4);
    });
    ctx.restore();
  }
};
```
Register via plugins array on that chart only.

Chart.js bar horizontal: `indexAxis: 'y'`. Bars red: backgroundColor 'rgba(155,35,53,0.8)'. Ticks: font monospace small. Grid: minimal — display false for x? Keep light.

FIG.02: labels years as strings; datasets per mechanism; stacked true; colors map:
```js
const MEC_COLORS = { "Universal Periodic Review": "#c2410c", "Treaty bodies": "#0f766e", "Special Procedures": "#7c3aed" };
```
fallback '#6b6459'.

Legend: display true, labels usePointStyle.

Now write checks details.

Link check:
```js
function linkCheck(){
  const bad=[];
  for(const r of records){
    let ok = /^https:\/\/docs\.un\.org\//i.test(r.doc_url||"");
    if(ok){
      let url; try{ url = decodeURIComponent(r.doc_url); }catch(e){ url = r.doc_url; }
      let sym; try{ sym = decodeURIComponent(r.symbol); }catch(e){ sym = r.symbol; }
      ok = url.toLowerCase().endsWith(sym.toLowerCase());
    }
    if(!ok) bad.push(r.symbol);
  }
  return bad;
}
```

Paragraph share per mechanism: group by mechanism: total, withPara.

States: UPR records: r._states includes "State not found" or empty → fail list with symbol and trailing snippet: text.slice(-70).

Duplicates: map text→count; dupTexts = entries with count>1; report "n texts appear more than once (m records involved)". Distinct ids: new Set(records.map(r=>r.id)).size vs records.length.

Missing labels: no themes (empty/missing), no sdgs, no affected_persons.

Chart-vs-table check: recompute theme counts via independent loop (I'll just recompute with a different code path — e.g., using reduce) and compare with what's displayed (themeTop variable). Also largest ≤ filtered.length. Status pass/fail.

Now the sample cards: draw from filtered. Card content: symbol link (doc_url, new tab), para (or "no paragraph number in this extract"), full text verbatim (esc), theme chips (buttons? just spans), verdict buttons. "one open at a time" — accordion: clicking a card header closes others.

Tally: "Themes: 4 fit · 3 don't fit · 3 unsure of 10 judged — seed 1. This is your judgement of the UN's labels; nothing is sent anywhere."

Buttons per card: Fits / Doesn't fit / Unsure — clicking sets verdict, marks button active, updates tally. One verdict per card (re-click changes).

Now write the method text (tab 04), 5-6 sentences:
- Every number on this page is a loop over the records in the attached file; nothing is estimated and no model is called.
- The headline count is records.length; documents are distinct symbols; years are min–max of the year field.
- Filters combine with AND: mechanism, body and type match the field exactly; years are inclusive; SDG matches if the record lists the goal; the keyword requires every word to appear literally in the text or symbol.
- Paragraph numbers are read from the start of the text with a fixed pattern; UPR recommending States are read from the parentheses at the end of UPR texts only.
- The CSV export contains the filtered rows with the full text and labels, generated in your browser; the only thing that can leave the page is the clipboard write when you press Copy.

CSV columns: Date, Body, Mechanism, Type, Symbol, Document URL, Paragraph, Recommending State(s), Section, Themes, SDGs, SDG targets, Affected persons, Text.

Copy summary text:
```
UN human rights recommendations and observations: Kenya — {n} records from {d} documents ({y0}–{y1}), {type breakdown}. Top themes: 1. X (n), ... Source: OHCHR UHRI, built {built}. Filters: ...
```

Now header:
```
<div class="kicker">UHRI · KENYA</div>  (monospace, uppercase)
<h1>UN human rights recommendations and observations: Kenya</h1>
<p class="meta"><a href=source_url>source</a> · n records · n documents · y0–y1 · built {built} · dated by document</p>
```
Country from data; title uses country as-is: `UN human rights recommendations and observations: ${country}`.

Kicker: `UHRI · ${country.toUpperCase()}`.

Now CSS. Let me write it compactly but complete.

```css
:root{ --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335; }
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
header{padding:20px 28px 14px;border-bottom:1px solid var(--rule)}
.kicker{font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--red)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:34px;margin:8px 0 6px}
.meta{font-size:13px;color:#4a463f;margin:0}
.meta a{color:var(--ink)}
.layout{display:flex;align-items:flex-start;gap:0}
aside{width:250px;flex:0 0 250px;border-right:1px solid var(--rule);padding:16px 18px;position:sticky;top:0;max-height:100vh;overflow:auto}
main{flex:1;min-width:0;padding:16px 28px 40px}
...
```

Tabs:
```css
.tabs{display:flex;gap:2px;border-bottom:1px solid var(--rule);margin-bottom:18px}
.tab{font:12px ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;background:none;border:none;border-bottom:2px solid transparent;padding:8px 12px;cursor:pointer;color:#4a463f}
.tab[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
```

Rail:
```css
.rail-h{display:flex;justify-content:space-between;align-items:baseline}
.rail-h .lbl{font:11px ui-monospace...;letter-spacing:.14em;color:var(--red)}
#clearAll{background:none;border:none;font:11px ui-monospace;cursor:pointer;text-decoration:underline;color:#4a463f}
.bignum{font-family:Georgia,serif;font-size:52px;line-height:1;margin:10px 0 2px}
.of{font:11px ui-monospace;color:#4a463f}
.sharebar{height:4px;background:var(--rule);margin:8px 0 10px}
.sharebar i{display:block;height:100%;background:var(--red)}
.chips{display:flex;flex-wrap:wrap;gap:4px;margin:6px 0 10px}
.chip{font:11px ui-monospace;background:#fff;border:1px solid var(--rule);border-radius:10px;padding:2px 8px;cursor:pointer}
.chip b{color:var(--red);font-weight:400}
.acc-btn{width:100%;text-align:left;background:none;border:none;border-top:1px solid var(--rule);padding:10px 0;font:12px ui-monospace;letter-spacing:.08em;cursor:pointer;display:flex;justify-content:space-between;color:var(--ink)}
.acc-btn .n{color:var(--red)}
.acc-panel{padding:4px 0 12px}
```

Filter controls styling: selects full width, labels small monospace.

Tiles:
```css
.tiles{display:flex;flex-wrap:wrap;gap:0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-bottom:22px}
.tile{padding:14px 22px 12px 0;margin-right:22px;border-right:1px solid var(--rule)} last no border
.tile .num{font-family:Georgia,serif;font-size:46px;line-height:1}
.tile .cap{font:11px ui-monospace;letter-spacing:.1em;text-transform:uppercase;color:#4a463f;margin-top:4px}
.tile .sub{font-size:13px;color:#4a463f}
.how{font:11px ui-monospace;color:#6b6459;margin-top:6px}
```

Figures:
```css
.fig{margin:26px 0}
.figtitle{font-family:Georgia,serif;font-size:20px;margin:0 0 2px}
.figno{font:11px ui-monospace;color:var(--red);letter-spacing:.12em}
.src{font:11px ui-monospace;color:#6b6459;margin-top:8px}
canvas{max-width:100%}
```

Tables:
```css
table{border-collapse:collapse;width:100%;font-size:14px}
caption{text-align:left;font:11px ui-monospace;color:#4a463f;padding:6px 0}
th{font:11px ui-monospace;letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:1px solid var(--ink);padding:6px 8px;cursor:default}
th.sortable{cursor:pointer}
td{border-bottom:1px solid var(--rule);padding:6px 8px;vertical-align:top}
td.num,th.num{text-align:right}
tbody tr.data{cursor:pointer}
tbody tr.data:hover{background:#ece6d8}
tr.detail td{background:#efe9dc;padding:14px 18px}
.para-big{font-family:Georgia,serif;font-size:40px;color:var(--red);line-height:1}
mark{background:#f3d9a4;padding:0 1px}
```

Buttons:
```css
.btn{font:12px ui-monospace;background:none;border:1px solid var(--ink);padding:6px 12px;cursor:pointer;color:var(--ink)}
.btn:hover{background:#e9e2d2}
```

Check panel:
```css
.checkline{display:flex;gap:10px;padding:7px 0;border-bottom:1px solid var(--rule);font-size:14px}
.checkline .st{margin-left:auto;font:11px ui-monospace;white-space:nowrap}
.pass{color:#0f766e}.warn{color:#b45309}.fail{color:var(--red)}
```

Sample cards:
```css
.sample-head{...}
.card{border-bottom:1px solid var(--rule)}
.card-btn{width:100%;text-align:left;background:none;border:none;padding:8px 0;cursor:pointer;font:13px ui-monospace;display:flex;gap:8px}
.card-panel{padding:4px 0 14px 12px;border-left:2px solid var(--red);margin:2px 0 10px;padding-left:14px}
.verdict-btns button{...}
.vbtn.on{background:var(--red);color:#fff;border-color:var(--red)}
```

OK. Now the JS in full. Let me be careful with details and write the final file. Target under 1500 lines — should be fine (~900-1100 lines).

Let me draft the script section by section.

```js
(function(){
"use strict";
const U = window.WORKSHOP_DATA.uhri;
const records = U.records || [];
const country = U.country || "the country";
const sdgNames = U.sdg_names || {};
const N = records.length;
const docCount = new Set(records.map(r=>r.symbol)).size;
const yearsAll = records.map(r=>r.year).filter(y=>typeof y==="number");
const Y0 = Math.min(...yearsAll), Y1 = Math.max(...yearsAll);
```

Careful: Math.min(...yearsAll) with 2264 elements fine.

Precompute:
```js
const PARA_RE = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
const STATE_RUN_RE = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const STATE_GROUP_RE = /\((?:[^()]|\([^()]*\))*\)/g;
records.forEach((r,i)=>{
  r._i = i;
  const m = String(r.text||"").match(PARA_RE);
  r._para = m ? m[1] : null;
  r._paraNum = m ? parseFloat(m[1]) : Infinity;
  r._hay = (String(r.text||"")+" "+String(r.symbol||"")).toLowerCase();
  r._states = null;
  if(r.mechanism === "Universal Periodic Review"){
    const run = String(r.text||"").match(STATE_RUN_RE);
    let out = [];
    if(run){
      const groups = run[1].match(STATE_GROUP_RE) || [];
      let bad = false;
      for(const g of groups){
        const name = g.slice(1,-1).trim();
        if(name.includes(",") || name.length > 60){ bad = true; break; }
        out.push(name);
      }
      if(bad || !out.length) out = ["State not found"];
    } else out = ["State not found"];
    r._states = out;
  }
});
```

Wait: if no run match → "State not found"? Plan: "the records without one are listed" — records where no state found. If no trailing parentheses, states = [] → counts as not found. I'll set out=[] when no run, and treat empty as not found. Let me: if(!run) out=[]; else process; if bad → ["State not found"]. Then "has state" = out.length>0 && out[0]!=="State not found". Display: out.join(", ") or "State not found" if empty/bad. Hmm if empty, display "State not found" too. OK.

Filters & state:

```js
const F = { keyword:"", mechanism:"all", body:"all", type:"all", state:"all", themes:new Set(), y0:Y0, y1:Y1, sdg:"all" };
let filtered = records.slice();
```

matches as above (year compare: r.year could be missing? assume present; guard: if typeof r.year!=="number" and year filter active → exclude? Keep simple: use r.year||0).

applyFilters():
```js
function applyFilters(){
  filtered = records.filter(matches);
  renderRail();
  renderActive();
  runChecks(); // updates check panel if visible; store results
}
```

Actually runChecks computes and stores `checkResults`, renders if tab 2 active. Chart check uses current filtered & themeTop.

renderActive(): switch(tabIdx){0:renderOverview();1:renderRecords();2:renderChecks();3:renderMethodCounts?}

Tab switching:
```js
let tabIdx = 0;
function setTab(i){ tabIdx=i; update tab buttons aria-selected & panels hidden; rail.classList.toggle('rail-min', i>=2); renderActive(); }
```

Keyboard on tablist: ArrowRight/Left.

Rail build (static HTML with dynamic parts):

```html
<aside id="rail">
  <div class="rail-h"><span class="lbl">FILTERS</span><button id="clearAll">Clear all</button></div>
  <div class="bignum" id="matchNum" aria-live="polite">0</div>
  <div class="of" id="ofNum"></div>
  <div class="sharebar"><i id="shareFill"></i></div>
  <div class="chips" id="chips"></div>
  <div class="acc" id="acc">
    <button class="acc-btn" data-acc="0" aria-expanded="false"><span><span class="n">01</span> KEYWORD</span><span>▾</span></button>
    <div class="acc-panel" id="accp0" hidden>
      <input id="kw" type="search" placeholder="e.g. torture" style="width:100%">
      <div class="hint">literal match, not synonyms · applied after 300 ms</div>
    </div>
    ... acc 1: mechanism select, body select, type select, state select
    ... acc 2: year from, year to, sdg select
  </div>
</aside>
```

Accordion behavior: clicking acc-btn toggles; close others.

Selects:
```html
<label class="fl">Mechanism
<select id="fMech"></select></label>
```
Populate options in JS.

Keyword inputs: two (rail #kw, records tab #kw2). Sync.

renderRail():
```js
matchNum.textContent = filtered.length (with thousands separator? big number — use toLocaleString('en-US')? Plan says thousands separators in tables. For big number, plain or locale — I'll use locale string.)
ofNum: "of N in the file"
shareFill.style.width = (N? filtered.length/N*100:0)+"%"
chips: build
```

Chips builder:
```js
function chipList(){
  const c=[];
  if(F.keyword) c.push({k:'keyword', label:'Keyword: “'+F.keyword+'”'});
  if(F.mechanism!=="all") c.push({k:'mechanism', label:'Mechanism: '+F.mechanism});
  if(F.body!=="all") c.push({k:'body', label:'Body: '+F.body});
  if(F.type!=="all") c.push({k:'type', label:'Type: '+F.type});
  if(F.state!=="all") c.push({k:'state', label:'State: '+F.state});
  for(const t of F.themes) c.push({k:'theme:'+t, label:'Theme: '+t});
  if(F.y0!==Y0||F.y1!==Y1) c.push({k:'years', label:'Years: '+F.y0+'–'+F.y1});
  if(F.sdg!=="all") c.push({k:'sdg', label:'SDG: '+F.sdg+(sdgNames[F.sdg]?' '+sdgNames[F.sdg]:'')});
  return c;
}
```
Chip click: remove that filter (theme: delete from set; years: reset y0/y1; keyword: clear both inputs).

Overview render:

```js
function renderOverview(){
  // tiles
  const typeCounts = {}; filtered.forEach(r=>{ typeCounts[r.type]=(typeCounts[r.type]||0)+1; });
  const docsF = new Set(filtered.map(r=>r.symbol)).size;
  const yrsF = filtered.map(r=>r.year); const fy0 = yrsF.length?Math.min(...yrsF):null; ...
  tileTotal: num = filtered.length, cap "records in view", sub: breakdown per type: Object.entries sorted desc: "1,791 Recommendations · 471 Concerns/Observations · 2 Other" + "of N in the file". how: "How this is computed: count of records passing the filters in the left rail; the type breakdown counts each record once, using the UN's own type labels."
  tileDocs: docsF, cap "documents", sub "distinct symbols", how...
  tileYears: fy0–fy1, cap "years", sub "dated by document", how...
  mechanism tiles: for each mechanism (sorted by count in file desc): count in filtered, docs in filtered, latest year in filtered, share = count/filtered.length. dot color. UPR tile: button "see the States" toggling #statesList.
  // FIG.01
  themeTop = topThemes(filtered, 10);
  update chart1; render table under.
  // FIG.02
  update chart2.
}
```

topThemes:
```js
function topThemes(list, k){
  const m = new Map();
  for(const r of list){
    for(const t of (r.themes||[])){
      let e = m.get(t); if(!e){ e={theme:t,count:0,y0:r.year,y1:r.year}; m.set(t,e); }
      e.count++; if(r.year<e.y0)e.y0=r.year; if(r.year>e.y1)e.y1=r.year;
    }
  }
  return [...m.values()].sort((a,b)=> b.count-a.count || (a.theme<b.theme?-1:a.theme>b.theme?1:0)).slice(0,k);
}
```

Chart1 creation:
```js
let chart1=null, chart2=null, themeTop=[];
function ensureCharts(){
  if(chart1) return;
  const c1 = document.getElementById('fig1');
  chart1 = new Chart(c1, { type:'bar', data:{labels:[],datasets:[{data:[],backgroundColor:'rgba(155,35,53,0.8)',borderWidth:0}]}, options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false? ... plugins:{legend:{display:false}, tooltip:{callbacks:{label: c=>' '+c.parsed.x+' records'}}}, onClick:(e,els)=>{ if(els.length){ const t=themeTop[els[0].index].theme; if(t && !F.themes.has(t)){ F.themes.add(t); applyFilters(); } } }, scales:{ x:{beginAtZero:true, ticks:{font:{family:mono,size:11}}}, y:{ticks:{font:{family:mono,size:11}}} } }, plugins:[endLabels] });
  ...
}
```
Canvas height: wrap in div with height e.g. 320px; maintainAspectRatio:false.

Chart2:
```js
chart2 = new Chart(c2,{type:'bar',data:{labels:[],datasets:[]},options:{responsive:true,maintainAspectRatio:false,scales:{x:{stacked:true,...},y:{stacked:true,beginAtZero:true}},plugins:{legend:{position:'top',labels:{usePointStyle:true,font:{family:mono,size:11}}}}}});
```
Datasets: for each mechanism in MEC order (all mechanisms present in file): {label, data, backgroundColor}.

Update:
```js
function updateCharts(){
  if(!chart1) return;
  chart1.data.labels = themeTop.map(t=>t.theme);
  chart1.data.datasets[0].data = themeTop.map(t=>t.count);
  chart1.update();
  // fig2
  const yrs=[]; for(let y=Y0;y<=Y1;y++) yrs.push(String(y));
  const mechs = [...new Set(records.map(r=>r.mechanism))];
  const byM = new Map(mechs.map(m=>[m,new Map()]));
  for(const r of filtered){ const mm=byM.get(r.mechanism); mm.set(r.year,(mm.get(r.year)||0)+1); }
  chart2.data.labels = yrs;
  chart2.data.datasets = mechs.map(m=>({label:m, data: yrs.map(y=> (byM.get(m).get(Number(y))||0) ), backgroundColor: MEC_COLORS[m]||'#6b6459'}));
  chart2.update();
}
```

FIG.01 table under chart: build rows: Theme | Records | % of filtered | Years. % = (count/filtered.length*100).toFixed(1). Note under: "A record can carry several themes, so the bars add up to more than n." plus "How this is computed: each theme of each filtered record counts once; ties alphabetical." Source line: "Source: WORKSHOP_DATA.uhri, themes field of n filtered records."

Records tab:

```html
<section id="panel1">
  <div class="searchrow"><input id="kw2" type="search" placeholder="Search ..."><span class="hint">same as 01 Keyword · literal match</span></div>
  <table id="rectab">
    <caption id="reccap"></caption>
    <thead><tr>
      <th class="sortable" id="thDate">Date</th><th>Body</th><th>Symbol</th><th>Para.</th><th>First line</th><th>Recommending State</th>
    </tr></thead>
    <tbody id="recbody"></tbody>
  </table>
  <button class="btn" id="moreBtn">Show 50 more</button>
</section>
```

renderRecords():
```js
let visible=50, sortAsc=false, expanded=new Set();
function sortedFiltered(){
  const arr = filtered.slice();
  arr.sort((a,b)=>{
    let c = sortAsc ? String(a.date).localeCompare(String(b.date)) : String(b.date).localeCompare(String(a.date));
    if(c) return c;
    c = String(a.body).localeCompare(String(b.body)); if(c) return c;
    c = a._paraNum - b._paraNum; if(c) return c;
    return a._i - b._i;
  });
  return arr;
}
```
Wait plan: sorted by date desc, then body, then para asc, then file order. Date header click reverses (date asc). OK.

Build rows up to visible:
```js
const rows = sortedFiltered();
const shown = rows.slice(0, visible);
reccap: `${shown.length} of ${rows.length} matching records shown · newest first` (or oldest first).
```
Row html:
```html
<tr class="data" data-id tabindex="0" aria-expanded="false">
 <td>2025-07-10</td><td>CEDAW</td><td><a href=doc_url target=_blank rel=noopener>symbol</a></td><td>54</td><td>firstline highlighted</td><td>states or —</td>
</tr>
```
If expanded has id, insert detail row after.

Detail row:
```html
<tr class="detail"><td colspan="6">
 <div class="para-big">54</div> or <div class="para-big none">—</div>
 <p class="fulltext">highlighted full text</p>
 <div class="labels"> themes chips, sdgs with names, sdg_targets, affected_persons, section </div>
 <button class="btn copybtn">Copy citation</button> <a class="btn" href=doc_url target=_blank>Open the UN document</a>
</td></tr>
```

Labels rendering:
```js
function labelsHtml(r){
  let h='';
  if(r.section) h+= `<div><span class="ll">SECTION</span> ${esc(r.section)}</div>`;
  h+= `<div><span class="ll">THEMES</span> ${(r.themes||[]).map(esc).join(' · ') || '<span class="missing">not labelled</span>'}</div>`;
  const sdgs=(r.sdgs||[]).map(g=> esc(g + (sdgNames[String(g)]? ' '+sdgNames[String(g)]:'') )).join(' · ');
  h+= `<div><span class="ll">SDGS</span> ${sdgs || '<span class="missing">not labelled</span>'}</div>`;
  if(r.sdg_targets&&r.sdg_targets.length) h+=`<div><span class="ll">SDG TARGETS</span> ${r.sdg_targets.map(esc).join(' · ')}</div>`;
  h+= `<div><span class="ll">AFFECTED PERSONS</span> ${(r.affected_persons||[]).map(esc).join(' · ') || '<span class="missing">not labelled</span>'}</div>`;
  return h;
}
```

Event delegation on tbody:
```js
recbody.addEventListener('click', e=>{
  const tr = e.target.closest('tr.data'); if(!tr) return;
  if(e.target.closest('a')) return; // let link open
  toggleRow(tr.dataset.id);
});
recbody.addEventListener('keydown', e=>{ if((e.key==='Enter'||e.key===' ') && e.target.matches('tr.data')){ e.preventDefault(); toggleRow(e.target.dataset.id); } });
```
toggleRow: expanded add/delete; renderRecords() (keeps visible). But re-render loses focus... acceptable; or re-render and refocus. Keep simple.

Copy button delegation: click on .copybtn → find record by id → clipboard.

moreBtn: visible+=50; renderRecords().

thDate click: sortAsc=!sortAsc; renderRecords().

Checks tab:

```html
<section id="panel2">
 <h2 class="ptitle">Check this dashboard</h2>
 <p class="hint">How the app checks itself — every check compares two values computed by separate loops; nothing is hidden.</p>
 <div id="checks"></div>
 <h2 class="ptitle">Check the UN's labels on a random sample</h2>
 <p class="hint">This is your judgement of the UN's labels; nothing is sent anywhere.</p>
 <div class="sample-controls">
   <button class="btn" id="drawBtn">Check 10 at random</button>
   <button class="btn" id="drawAgain">Draw again</button>
   <label>seed <input id="seedBox" type="number" value="1" style="width:90px"></label>
   <button class="btn" id="drawSeed">Draw with this seed</button>
 </div>
 <div id="tally" class="tally"></div>
 <div id="cards"></div>
</section>
```

runChecks(): compute array of {name, detail, status}. Render into #checks if tab 2 active (or always render — cheap; render always so it's ready).

Check lines:
1. "Record count — records.length vs the file's own count field" → `${N} vs ${Number(U.count)}` pass/fail.
2. "Partitions — counts per mechanism, per body and per year each sum to the record count" → detail "mechanism Σ=…, body Σ=…, year Σ=…" pass if all equal N.
3. "Type partition — counts per type sum to the headline total" → pass/fail.
4. "Chart against table — each FIG.01 bar recomputed by a second loop over the n filtered records; the ten table rows show the same values; the largest bar ≤ n" → pass/fail. Implement: recompute topThemes via alternative loop (e.g., using forEach and object) and deep-compare with themeTop; largest = themeTop[0]? themeTop[0].count <= filtered.length.
5. "Links — every doc_url starts with https://docs.un.org/ and ends with its symbol (case-insensitive, decoded)" → pass or fail listing up to 5 symbols + "and k more".
6. "Paragraph numbers — share of records with a number found, per mechanism" → detail per mechanism "UPR 100% · Treaty bodies 30% · Special Procedures 12%"; UPR <100% → warn "UPR below 100% — shown as a warning, not an error"; else pass.
7. "States found — UPR records with at least one State vs all UPR records" → "1,370 of 1,372" pass if equal else warn listing symbols (up to 8) with trailing snippet.
8. "Duplicates and gaps — distinct id vs record count; duplicate texts; records not labelled" → detail.

Sample draw:
```js
let sampleSeed=1, sampleIds=[], verdicts=new Map();
function drawSample(seed){
  sampleSeed=seed;
  const rng=mulberry32(seed>>>0 || 1);
  const pool=filtered; const n=pool.length;
  const k=Math.min(10,n);
  const idx=new Set();
  while(idx.size<k){ idx.add(Math.floor(rng()*n)); }
  sampleIds=[...idx].map(i=>pool[i]._i);
  verdicts=new Map();
  renderCards();
}
```
mulberry32 with seed 0 → a=0 loop... seed>>>0||1 handles 0. Fine.

renderCards(): tally: counts of verdicts among sampleIds: fit/dont/unsure; "Themes: x fit · y don't fit · z unsure of 10 judged · seed N — your judgement of the UN's labels; nothing is sent anywhere." Cards: for each id: button line `${symbol} · para ${para||'—'}`; panel hidden; open one at a time (click toggles, closes others). Panel: link, para big? Keep: full text, theme chips, verdict buttons.

Verdict buttons: data-v="fit|dont|unsure"; click → verdicts.set(id,v); renderCards() (or just update tally + button states — simpler re-render cards).

Tab 04:

```html
<section id="panel3">
 <h2>How this was made</h2>
 <ol class="method"> 6 sentences </ol>
 <h2>Take it with you</h2>
 <button id="csvBtn" class="btn">Download CSV of the current filter</button>
 <button id="sumBtn" class="btn">Copy summary</button>
 <div id="exportNote" class="hint"></div>
 <h2>Source</h2>
 <p>...</p>
 <p class="credits">Credits: ...</p>
</section>
```

CSV:
```js
function csvEscape(v){ v=String(v==null?"":v); return /[",\n]/.test(v) ? '"'+v.replace(/"/g,'""')+'"' : v; }
function buildCSV(){
  const lines=[];
  lines.push("# Country: "+country);
  lines.push("# Source: "+U.source+" — "+U.source_url);
  lines.push("# Built: "+U.built);
  lines.push("# Filters: "+(chipList().map(c=>c.label).join("; ")||"none"));
  lines.push("# Rows: "+filtered.length+" of "+N);
  const head=["Date","Body","Mechanism","Type","Symbol","Document URL","Paragraph","Recommending State(s)","Section","Themes","SDGs","SDG targets","Affected persons","Text"];
  lines.push(head.map(csvEscape).join(","));
  for(const r of filtered){
    lines.push([r.date,r.body,r.mechanism,r.type,r.symbol,r.doc_url,r._para||"", (r._states? r._states.join("; ") : ""), r.section||"", (r.themes||[]).join("; "), (r.sdgs||[]).join("; "), (r.sdg_targets||[]).join("; "), (r.affected_persons||[]).join("; "), r.text||""].map(csvEscape).join(","));
  }
  return lines.join("\n");
}
```
Download:
```js
csvBtn.onclick=()=>{ const blob=new Blob([buildCSV()],{type:"text/csv;charset=utf-8"}); const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download="uhri-"+country.toLowerCase().replace(/[^a-z0-9]+/g,"-")+"-filtered.csv"; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(a.href),1000); note("CSV downloaded: n rows..."); };
```

Copy summary:
```js
function summaryText(){
  const tc={}; filtered.forEach(r=>tc[r.type]=(tc[r.type]||0)+1);
  const tb = themeTop.length? themeTop : topThemes(filtered,10);
  return "UN human rights recommendations and observations: "+country+" — "+filtered.length+" of "+N+" records from "+docCount+" documents ("+Y0+"–"+Y1+"), "+Object.entries(tc).map(([t,c])=>c+" "+t).join(", ")+". Top themes: "+tb.map((t,i)=>(i+1)+". "+t.theme+" ("+t.count+")").join("; ")+". Source: "+U.source+" (built "+U.built+"). Filters: "+(chipList().map(c=>c.label).join("; ")||"none")+".";
}
```
Copy with clipboard fallback; note "Copied to clipboard".

Clipboard helper:
```js
function copyText(t, done){
  if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(()=>done(true),()=>fallback(t,done)); }
  else fallback(t,done);
}
function fallback(t,done){ const ta=document.createElement("textarea"); ta.value=t; ta.style.position="fixed"; ta.style.opacity="0"; document.body.appendChild(ta); ta.select(); let ok=false; try{ ok=document.execCommand("copy"); }catch(e){} ta.remove(); done(ok); }
```

Method tab static content + maybe dynamic counts. Fine static with a couple of dynamic numbers.

Footer:
```html
<footer><span>Built on OHCHR UHRI data · {N} records · <a href=source_url>source</a></span></footer>
```
Set via JS or hardcode with JS fill. I'll fill via JS into #foot.

Now heading structure for panels: each panel gets an h2? The tabs already label. Add small section titles inside.

Also "see the States" list in UPR tile:
```js
function topStates(list,k){ const m=new Map(); for(const r of list){ if(r._states) for(const s of r._states){ if(s!=="State not found") m.set(s,(m.get(s)||0)+1); } } return [...m.entries()].map(([state,count])=>({state,count})).sort((a,b)=>b.count-a.count||a.state.localeCompare(b.state)).slice(0,k); }
```
UPR tile button toggles #statesBox: "Ten States that made most recommendations to {country} (n UPR records in view)" list "State — n".

Now the accordion in rail: build options.

```js
function fillSelects(){
  const mechs=[...new Set(records.map(r=>r.mechanism))].sort();
  fMech.innerHTML = '<option value="all">all mechanisms</option>' + mechs.map(m=>`<option value="${esc(m)}">${esc(m)}</option>`).join("");
  ...
}
```
Body options depend on mechanism: recompute in renderRail or on mech change:
```js
function bodyOptions(){
  const src = F.mechanism==="all" ? records : records.filter(r=>r.mechanism===F.mechanism);
  const counts=new Map(); src.forEach(r=>counts.set(r.body,(counts.get(r.body)||0)+1));
  return [...counts.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));
}
```
On mechanism change: F.body="all"; refill body select; applyFilters.

Type options: all types in file with counts.
State options: states over records matching all filters except state — compute in renderRail? That requires matchesWithout('state'). Implement matches(r, skip) with skip param. Then state options counts over records.filter(r=>matches(r,'state')). Keep selected value if still in list else "all".

Year selects: distinct years sorted; from/to.
SDG options: goals present: set of Number(g) for r.sdgs; label `${g} ${sdgNames[String(g)]||""}`.

Events:
- fMech change → F.mechanism, F.body="all", refill body, applyFilters.
- fBody change → F.body, applyFilters.
- fType, fState, fSdg change → applyFilters.
- fY0/fY1 change → let a=+fY0.value,b=+fY1.value; if(a>b){[a,b]=[b,a]; set selects} F.y0=a;F.y1=b; applyFilters.
- kw inputs: debounce.

Debounce:
```js
let kwT; function onKw(v){ clearTimeout(kwT); kwT=setTimeout(()=>{ F.keyword=v.trim(); kw1.value=v; kw2.value=v; applyFilters(); },300); }
```
Sync both inputs.

Clear all: reset F, reset inputs/selects, applyFilters.

Now checks rendering:

```js
function runChecks(){
  const res=[];
  // 1
  const cnt = Number(U.count);
  res.push({name:"Record count", detail:`records.length = ${N} · file's count field = ${U.count} (as number: ${cnt})`, status: N===cnt?"pass":"fail"});
  // 2 partitions
  const sum = fn => { const m={}; records.forEach(r=>m[fn(r)]=(m[fn(r)]||0)+1); return Object.values(m).reduce((a,b)=>a+b,0); };
  const sm=sum(r=>r.mechanism), sb=sum(r=>r.body), sy=sum(r=>r.year);
  res.push({name:"Partitions", detail:`per mechanism Σ=${sm}, per body Σ=${sb}, per year Σ=${sy} — all should equal ${N}`, status:(sm===N&&sb===N&&sy===N)?"pass":"fail"});
  // 3 type
  const st=sum(r=>r.type);
  res.push({name:"Type partition", detail:`counts per type sum to ${st} (headline ${N})`, status: st===N?"pass":"fail"});
  // 4 chart vs table
  const alt = {}; filtered.forEach(r=>{(r.themes||[]).forEach(t=>alt[t]=(alt[t]||0)+1);});
  const altTop = Object.entries(alt).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,10);
  let ok4 = themeTop.length===altTop.length && themeTop.every((t,i)=>t.theme===altTop[i][0] && t.count===altTop[i][1]);
  const largest = themeTop.length? themeTop[0].count : 0;
  ok4 = ok4 && largest <= filtered.length;
  res.push({name:"Chart against table", detail:`FIG.01 bars recomputed by a second loop over the ${filtered.length} filtered records match the ten table rows; largest bar ${largest} ≤ ${filtered.length}`, status: ok4?"pass":"fail"});
  // 5 links
  const bad=[]; records.forEach(r=>{ ... if(!ok) bad.push(r.symbol); });
  res.push({name:"Links", detail: bad.length? `records whose doc_url does not start with https://docs.un.org/ or end with the symbol: ${bad.slice(0,6).join(", ")}${bad.length>6?` (+${bad.length-6} more)`:""}` : `all ${N} doc_url values start with https://docs.un.org/ and end with their symbol (case-insensitive, decoded)`, status: bad.length?"fail":"pass"});
  // 6 para share
  const pm={}; records.forEach(r=>{ const m=r.mechanism; pm[m]=pm[m]||{t:0,p:0}; pm[m].t++; if(r._para) pm[m].p++; });
  const det6 = Object.entries(pm).map(([m,v])=>`${m}: ${(100*v.p/v.t).toFixed(0)}% with a number`).join(" · ");
  const upr = pm["Universal Periodic Review"];
  const warn6 = upr && upr.p < upr.t;
  res.push({name:"Paragraph numbers", detail: det6, status: warn6?"warn":"pass", note: warn6? "UPR below 100% — shown as a warning, not an error":""});
  // 7 states
  const uprRecs = records.filter(r=>r.mechanism==="Universal Periodic Review");
  const noState = uprRecs.filter(r=>!r._states || !r._states.length || r._states[0]==="State not found");
  res.push({name:"States found", detail: `${uprRecs.length-noState.length} of ${uprRecs.length} UPR records have at least one State` + (noState.length? ` — without one: ${noState.slice(0,6).map(r=>r.symbol+" (“…"+String(r.text).slice(-50)+"”)").join("; ")}${noState.length>6?` (+${noState.length-6} more)`:""}`:""), status: noState.length?"warn":"pass"});
  // 8 dup/gaps
  const ids=new Set(records.map(r=>r.id));
  const tm=new Map(); records.forEach(r=>tm.set(r.text,(tm.get(r.text)||0)+1));
  const dups=[...tm.entries()].filter(([,c])=>c>1);
  const noTh=records.filter(r=>!r.themes||!r.themes.length).length;
  const noSdg=records.filter(r=>!r.sdgs||!r.sdgs.length).length;
  const noAp=records.filter(r=>!r.affected_persons||!r.affected_persons.length).length;
  res.push({name:"Duplicates and gaps", detail:`distinct id = ${ids.size} of ${N} · duplicate texts: ${dups.length} texts appear more than once (${dups.reduce((a,[,c])=>a+c-1,0)} extra records) · not labelled: ${noTh} without themes, ${noSdg} without SDGs, ${noAp} without affected persons`, status: ids.size===N && dups.length===0 ? "pass":"warn"});
  checkResults=res;
  if(tabIdx===2) renderChecks();
}
```

Hmm status for 8: duplicates exist in sample data (2 texts) → warn is fine ("shown, not hidden"). Use "warn" when dups or ids mismatch; pass otherwise. Actually distinct id should equal N; if not → fail. I'll do: ids.size!==N → fail; else dups.length? warn : pass.

renderChecks(): build HTML lines:
```html
<div class="checkline"><span class="cname">Record count</span><span class="cdetail">...</span><span class="st pass">✓ pass</span></div>
```
fail: "✗ check failed". warn: "⚠ warning".

Now sample cards render:

```js
function renderCards(){
  const tallyEl=document.getElementById('tally');
  let f=0,d=0,u=0;
  sampleIds.forEach(id=>{ const v=verdicts.get(id); if(v==='fit')f++; else if(v==='dont')d++; else if(v==='unsure')u++; });
  const judged=f+d+u;
  tallyEl.textContent = `Themes: ${f} fit · ${d} don't fit · ${u} unsure of ${sampleIds.length} judged (seed ${sampleSeed}) — your judgement of the UN's labels; nothing is sent anywhere.`;
  const box=document.getElementById('cards');
  box.innerHTML = sampleIds.map(id=>{
    const r=records.find(x=>x._i===id); // better: store refs
    ...
  }).join("");
}
```
Better store sampleRecs array of record refs. Use that.

Card:
```html
<div class="card">
 <button class="card-btn" data-id aria-expanded="false"><span class="cn">▸</span> symbol · para N</button>
 <div class="card-panel" hidden>
   <p class="fulltext">text</p>
   <div class="themechips">themes as spans</div>
   <div class="vbtns">
     <button data-v="fit" class="vbtn">Fits</button>
     <button data-v="dont" class="vbtn">Doesn't fit</button>
     <button data-v="unsure" class="vbtn">Unsure</button>
   </div>
 </div>
</div>
```
Delegation on #cards: click .card-btn toggles its panel, closes others; click .vbtn sets verdict, re-render cards (keeps open state? re-render closes all — annoying). Instead update in place: set verdicts, then update tally and button classes without full re-render. I'll do: on vbtn click → verdicts.set; update tally text; toggle .on classes among siblings. On card-btn click → toggle panels.

Draw buttons:
- drawBtn ("Check 10 at random"): drawSample(Number(seedBox.value)||1) — initial.
- drawAgain: seed = Math.floor(Math.random()*100000)+1; seedBox.value=seed; drawSample(seed).
- drawSeed: drawSample(Number(seedBox.value)||1).

Initial: draw once on first render of tab 2 with seed 1? Plan: "Check 10 at random" draws the cards — so draw on button click; but also nice to draw initially. I'll draw initially when tab 2 first opened (seed from box). And button redraws with box seed. Fine.

Now overview HTML skeleton:

```html
<section id="panel0" role="tabpanel">
  <div class="tiles" id="tiles"></div>
  <div class="fig">
    <div class="figno">FIG.01</div>
    <h3 class="figtitle" id="fig1title"></h3>
    <div class="chartwrap" style="height:340px"><canvas id="fig1"></canvas></div>
    <table id="fig1tab">...</table>
    <div class="how">How this is computed: ...</div>
    <div class="src">Source: ...</div>
  </div>
  <div class="fig">
    <div class="figno">FIG.02</div>
    <h3 class="figtitle" id="fig2title"></h3>
    <div class="chartwrap" style="height:300px"><canvas id="fig2"></canvas></div>
    <div class="how">...</div>
    <div class="src">...</div>
  </div>
</section>
```

fig1title: `Ten most frequent themes among ${filtered.length} filtered records` — if filtered 0: "No records match". Chart area shows "No records match" text: if themeTop empty, hide canvas wrap and show a div. I'll toggle.

Tiles HTML built in renderOverview:

```js
tiles.innerHTML = `
 <div class="tile"><div class="num">${fmt(filtered.length)}</div><div class="cap">records in view</div><div class="sub">${typeBreakdown} · of ${fmt(N)} in the file</div><div class="how">How this is computed: count of records passing the left-rail filters; each record counted once, split by the UN's own type label.</div></div>
 <div class="tile"><div class="num">${fmt(docsF)}</div><div class="cap">documents</div><div class="sub">distinct symbols</div><div class="how">How this is computed: number of distinct symbol values among the filtered records.</div></div>
 <div class="tile"><div class="num">${fy0? fy0+"–"+fy1 : "—"}</div><div class="cap">years</div><div class="sub">dated by document</div><div class="how">How this is computed: minimum and maximum of the year field among the filtered records.</div></div>
 ` + mechTiles;
```

mechTiles: mechs sorted by file count desc:
```js
const mechCounts = {}; records.forEach(r=>mechCounts[r.mechanism]=(mechCounts[r.mechanism]||0)+1);
const mechs=[...Object.keys(mechCounts)].sort((a,b)=>mechCounts[b]-mechCounts[a]);
mechs.map(m=>{
  const sub=filtered.filter(r=>r.mechanism===m);
  const docs=new Set(sub.map(r=>r.symbol)).size;
  const latest=sub.length?Math.max(...sub.map(r=>r.year)):"—";
  const share=filtered.length? Math.round(100*sub.length/filtered.length):0;
  const dot=`<i class="dot" style="background:${MEC_COLORS[m]||'#6b6459'}"></i>`;
  const statesBtn = m==="Universal Periodic Review" ? `<button class="linkbtn" id="statesToggle">see the States</button><div id="statesBox" hidden></div>` : "";
  return `<div class="tile"><div class="cap">${dot} ${esc(m)}</div><div class="num">${fmt(sub.length)}</div><div class="sub">${fmt(docs)} documents · latest ${latest} · ${share}% of filtered</div><div class="how">How this is computed: records with mechanism = “${esc(m)}” among the filtered set; share = count ÷ ${filtered.length}.</div>${statesBtn}</div>`;
}).join("")
```
statesToggle handler: delegation on tiles: if e.target.id==='statesToggle' → toggle statesBox, fill with topStates(filtered UPR,10): `Ten States that made most recommendations to ${country} — counts over the ${n} UPR records in view` + rows `State — n`.

Note: tile order — plan says first tile counts all records, beside it documents and years, below one tile per mechanism. My flex-wrap row does that.

FIG.01 table:
```html
<caption>Same ten themes as the bars above</caption>
<thead><tr><th>Theme</th><th class="num">Records</th><th class="num">% of filtered</th><th>Years</th></tr></thead>
<tbody> rows: theme (button? clicking row adds filter — plan says clicking a bar adds chip; table rows not required clickable. Keep plain.) </tbody>
```
Note under: "A record can carry several themes, so the bars add up to more than ${n}."

FIG.02 title: `Records per year by mechanism — ${filtered.length} filtered records, ${Y0}–${Y1}`. How: "How this is computed: records per year and mechanism in the filtered set; every year ${Y0}–${Y1} appears, so empty years show as gaps." Source line.

Now, "no view shows more than about seven things to click": tab 01 has 4 tabs + 3 accordion + clear all + states toggle + chart bars (not counted? "not counting table rows or chart bars") = 8 clickable. OK "about seven".

Tab 02: 4 tabs + 3 acc + clear + date header + show more = 9... hmm. "about seven" — the plan itself mandates these; I'll not obsess.

Now write everything. Also `fmt` = n=>n.toLocaleString("en-US").

esc function:
```js
function esc(s){ return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"); }
```

highlight:
```js
function highlight(text){
  const words = F.keyword.toLowerCase().split(/\s+/).filter(Boolean);
  const raw = String(text==null?"":text);
  if(!words.length) return esc(raw);
  const re = new RegExp("("+words.map(escRe).join("|")+")","gi");
  return raw.split(re).map((p,i)=> i%2===1 ? "<mark>"+esc(p)+"</mark>" : esc(p)).join("");
}
```

firstLine:
```js
function firstLine(t){
  t=String(t==null?"":t);
  if(t.length<=120) return t;
  let cut=t.slice(0,120); const sp=cut.lastIndexOf(" ");
  if(sp>40) cut=cut.slice(0,sp);
  return cut+"…";
}
```

Now assemble the full HTML. Also add `<meta>` and title with country — set via JS: document.title = "UHRI · "+country.

Tab buttons:
```html
<div class="tabs" role="tablist" aria-label="Dashboard sections">
 <button class="tab" role="tab" id="tab0" aria-controls="panel0" aria-selected="true">01 Overview</button>
 <button class="tab" role="tab" id="tab1" aria-controls="panel1" aria-selected="false" tabindex="-1">02 Records</button>
 <button class="tab" role="tab" id="tab2" aria-controls="panel2" aria-selected="false" tabindex="-1">03 Check</button>
 <button class="tab" role="tab" id="tab3" aria-controls="panel3" aria-selected="false" tabindex="-1">04 Method & export</button>
</div>
```
Arrow keys: on keydown in tablist, move focus & select.

Panels: role="tabpanel" aria-labelledby.

Rail-min CSS: `#rail.rail-min .acc{display:none}`.

Also on tab 2/3, keyword box hidden with acc — fine, chips still show keyword chip.

Edge: filtered empty → overview tiles show 0, "—"; fig1 area: show "No records match the current filters." text instead of chart; fig2 all zeros (chart shows empty bars — fine, or also message). Table caption "0 of 0 matching records". runChecks chart check with empty: themeTop empty, altTop empty, largest 0 ≤ 0 → pass. OK.

Records table with 0 rows: tbody shows a row "No records match the current filters." colspan 6.

Now, the "How this is computed" for rail number: add hint under bignum: "How this is computed: records passing all filters (AND)". Put as .how line.

Let me now also handle `U.count` string: Number(U.count).

Write final code. I'll aim for clean, complete implementation. Let me write it out now, carefully, keeping line count reasonable.

One more detail: "Copy citation" button label when no para: "Copy citation (no paragraph number in this extract)". Implement in detail row.

Detail row buttons: copy + open doc link. Delegation: recbody click on .copybtn → id from closest tr.detail? Put data-id on detail row too. I'll give both rows data-id.

Also stop row toggle when clicking buttons inside detail: detail rows aren't tr.data so fine; but copy button inside detail — closest('tr.data') null → return. Good. Link in symbol cell: e.target.closest('a') → return (don't toggle). Good.

Show more button: hidden when shown>=rows.length.

Caption: `${shown} of ${rows.length} matching records shown · ${sortAsc?"oldest first":"newest first"} · click Date to reverse`.

Now tab 04 method list (6 items):
1. Every number on this page is computed by loops over the records in the attached file (WORKSHOP_DATA.uhri); nothing is estimated and no language model is called.
2. The headline count is the number of records passing the filters; documents are distinct symbols; years are the min and max of the year field, which is the document's date, not the date a recommendation was made.
3. Filters combine with AND: mechanism, body, type and State match the field exactly; years are inclusive; SDG matches when the record lists the goal; the keyword requires every typed word to appear literally in the text or the symbol ("torture" will not find "ill-treatment").
4. Paragraph numbers are read from the start of each text with a fixed pattern (e.g. "71." or "144.43"); recommending States are read only from the parentheses at the end of UPR texts.
5. The CSV export is generated in your browser from the filtered rows, with the full text and labels; the only thing that can leave this page is the clipboard write when you press a Copy button.
6. Theme counts count each theme of each record once, so they add up to more than the record count; the app never removes, renames or re-labels a UN label.

Source block: source + link, built, count, licence line: "Data: OHCHR Universal Human Rights Index (UHRI)." Credits line: "Design guidance: UK Government Analysis Function, Data visualisation: charts and tables (Open Government Licence v3.0). Citation practice: UN Dag Hammarskjöld Library, Ask DAG. Data-handling approach: OHCHR, A Human Rights-Based Approach to Data." These are references consulted — fine to include as credits.

Footer: `Built on OHCHR UHRI data · 2,264 records · <a>OHCHR Universal Human Rights Index</a>` — dynamic.

Now write the whole file. Let me count structure and write.

Also remember: before code block, at most three short sentences; after, nothing.

Let me write the code now in final form.

Careful with template literals inside the HTML — fine.

Chart.js font family const: `const MONO='ui-monospace, Menlo, Consolas, monospace';`

endLabels plugin: for horizontal bar, meta.data[i].x is the end of bar (right edge). Draw at bar.x+6, bar.y+4 (bar.y is center). Good.

Also chart onClick: Chart.js v4 onClick(e, elements, chart). elements[0].index. Good.

For FIG.02 tooltip default fine.

Potential issue: Chart.js preloaded as window.Chart — use `new Chart(...)`. Guard `if(window.Chart)`.

Now writing renderRecords with expanded persistence across re-render: expanded Set of ids; renderRecords rebuilds; fine.

visible reset on filter change: in applyFilters set visible=50, expanded.clear()? Keep expanded? Clear to avoid confusion. I'll reset visible=50 and keep expanded (harmless). Actually if filter changes, expanded ids may not be in filtered — detail rows only rendered for shown rows, so fine. Keep.

Let me write the code.

Also the state select should join heading 02 "when States are extracted" — always show if any UPR records exist. I'll always render it; if no states found at all, options just "all States".

matches with skip:
```js
function matches(r, skip){
  if(skip!=="mechanism" && F.mechanism!=="all" && r.mechanism!==F.mechanism) return false;
  if(skip!=="body" && F.body!=="all" && r.body!==F.body) return false;
  if(skip!=="type" && F.type!=="all" && r.type!==F.type) return false;
  if(skip!=="state" && F.state!=="all" && !(r._states && r._states.indexOf(F.state)>-1)) return false;
  if(skip!=="theme"){ for(const t of F.themes){ if(!r.themes || r.themes.indexOf(t)<0) return false; } }
  if(skip!=="year"){ if(typeof r.year!=="number" || r.year<F.y0 || r.year>F.y1) return false; }
  if(skip!=="sdg" && F.sdg!=="all" && !(r.sdgs && r.sdgs.map(Number).indexOf(Number(F.sdg))>-1)) return false;
  if(skip!=="keyword" && F.keyword){ for(const w of F.keyword.toLowerCase().split(/\s+/).filter(Boolean)){ if(r._hay.indexOf(w)<0) return false; } }
  return true;
}
```

State options counts: over records.filter(r=>matches(r,"state")) — but that includes year/theme filters etc. Fine.

Body options: over records with mechanism filter only (skip others): records.filter(r=>matches(r,"body"))? That applies all other filters — could shrink list oddly. Plan: "Body or mandate (body values present in the chosen mechanism, each with its count)". So filter only by mechanism: records.filter(r=>F.mechanism==="all"||r.mechanism===F.mechanism). Counts over that. Good.

Type options: all types in file with counts (file-level). Mechanism options file-level.

Now writing final answer. Also ensure `[hidden]{display:none!important}` in CSS.

Let me write out the document fully now, mentally compiling for errors.

Structure of script:

```js
(function(){
"use strict";
const U=window.WORKSHOP_DATA.uhri;
... helpers ...
... precompute ...
... state ...
... rail DOM refs ...
... build selects ...
... events ...
... render functions ...
... init ...
})();
```

DOM refs by id. Let me define the HTML body first, then script referencing ids:

Header:
```html
<header>
 <div class="kicker" id="kicker"></div>
 <h1 id="title"></h1>
 <p class="meta" id="meta"></p>
</header>
```

Layout:
```html
<div class="layout">
 <aside id="rail" aria-label="Filters">
  <div class="rail-h"><span class="lbl">FILTERS</span><button id="clearAll" type="button">Clear all</button></div>
  <div class="bignum" id="matchNum" aria-live="polite">–</div>
  <div class="of" id="ofNum"></div>
  <div class="sharebar" aria-hidden="true"><i id="shareFill"></i></div>
  <div class="chips" id="chips"></div>
  <div class="acc" id="accWrap">
    <button type="button" class="acc-btn" data-acc="0" aria-expanded="false" aria-controls="accp0"><span><span class="n">01</span> KEYWORD</span><span class="arr">▾</span></button>
    <div class="acc-panel" id="accp0" hidden>
      <input type="search" id="kw1" placeholder="e.g. torture" aria-label="Keyword filter">
      <div class="hint">literal match, not synonyms · every word must appear in the text or symbol · applied 300 ms after typing</div>
    </div>
    <button ... data-acc="1" ...>02 MECHANISM · BODY · TYPE</button>
    <div class="acc-panel" id="accp1" hidden>
      <label class="fl">Mechanism<select id="fMech"></select></label>
      <label class="fl">Body / mandate<select id="fBody"></select></label>
      <label class="fl">Type<select id="fType"></select></label>
      <label class="fl">Recommending State (UPR)<select id="fState"></select></label>
    </div>
    <button ... data-acc="2">03 YEARS & SDG</button>
    <div class="acc-panel" id="accp2" hidden>
      <div class="yrow"><label class="fl">Year from<select id="fY0"></select></label><label class="fl">to<select id="fY1"></select></label></div>
      <label class="fl">SDG<select id="fSdg"></select></label>
    </div>
  </div>
  <div class="how">How this is computed: records passing every filter above (AND).</div>
 </aside>
 <main>
  <div class="tabs" role="tablist" id="tablist"> 4 buttons </div>
  <section id="panel0" role="tabpanel" aria-labelledby="tab0"> ... </section>
  <section id="panel1" role="tabpanel" aria-labelledby="tab1" hidden> ... </section>
  <section id="panel2" role="tabpanel" aria-labelledby="tab2" hidden> ... </section>
  <section id="panel3" role="tabpanel" aria-labelledby="tab3" hidden> ... </section>
 </main>
</div>
<footer id="foot"></footer>
```

Panel 0:
```html
<div class="tiles" id="tiles"></div>
<div class="fig" id="fig1block">
 <div class="figno">FIG.01</div>
 <h3 class="figtitle" id="fig1title"></h3>
 <div class="chartwrap" id="fig1wrap"><canvas id="fig1"></canvas></div>
 <div class="nomatch" id="fig1none" hidden>No records match the current filters.</div>
 <table id="fig1tab"></table>
 <div class="how" id="fig1how"></div>
 <div class="src" id="fig1src"></div>
</div>
<div class="fig">
 <div class="figno">FIG.02</div>
 <h3 class="figtitle" id="fig2title"></h3>
 <div class="chartwrap" id="fig2wrap"><canvas id="fig2"></canvas></div>
 <div class="how" id="fig2how"></div>
 <div class="src" id="fig2src"></div>
</div>
```

Panel 1:
```html
<div class="searchrow">
 <input type="search" id="kw2" placeholder="Search the filtered records, e.g. torture" aria-label="Search records">
 <span class="hint">same box as 01 Keyword · literal match, not synonyms</span>
</div>
<table id="rectab">
 <caption id="reccap"></caption>
 <thead><tr>
  <th><button type="button" class="thbtn" id="thDate">Date ▾</button></th>
  <th>Body</th><th>Symbol</th><th>Para.</th><th>First line</th><th>Recommending State</th>
 </tr></thead>
 <tbody id="recbody"></tbody>
</table>
<button type="button" class="btn" id="moreBtn">Show 50 more</button>
```
Date header as button for a11y (click reverses). Arrow indicator updates.

Panel 2:
```html
<h2 class="ptitle">How the app checks itself</h2>
<p class="hint">Each line compares two values computed by separate loops over the file. Nothing is hidden; a red line is a failed check.</p>
<div id="checks"></div>
<h2 class="ptitle">Check the UN's labels on a random sample</h2>
<p class="hint">Ten records drawn from the current filter with a seeded generator, so a colleague can draw the same ten. This is your judgement of the UN's labels; nothing is sent anywhere.</p>
<div class="sample-controls">
 <button type="button" class="btn" id="drawBtn">Check 10 at random</button>
 <button type="button" class="btn" id="drawAgain">Draw again</button>
 <label class="fl seedlbl">seed <input type="number" id="seedBox" value="1" min="1"></label>
 <button type="button" class="btn" id="drawSeed">Draw with this seed</button>
</div>
<div class="tally" id="tally"></div>
<div id="cards"></div>
```

Panel 3:
```html
<h2 class="ptitle">How this was made</h2>
<ol class="method" id="methodList"></ol>
<h2 class="ptitle">Take it with you</h2>
<div class="btnrow">
 <button type="button" class="btn" id="csvBtn">Download CSV of the current filter</button>
 <button type="button" class="btn" id="sumBtn">Copy summary</button>
</div>
<div class="hint" id="exportNote"></div>
<h2 class="ptitle">Source</h2>
<p class="src" id="srcBlock"></p>
<p class="credits">Credits: data — OHCHR Universal Human Rights Index (UHRI). Design guidance — UK Government Analysis Function, “Data visualisation: charts” and “Data visualisation: tables” (Open Government Licence v3.0). Citation practice — UN Dag Hammarskjöld Library, Ask DAG. Data approach — OHCHR, “A Human Rights-Based Approach to Data”.</p>
```

Method list items filled in JS or static HTML — static HTML fine with dynamic numbers? Keep static text (no numbers needed except maybe). I'll write static <li>s.

Now the script. Writing it fully:

```js
(function(){
"use strict";
var U=window.WORKSHOP_DATA.uhri;
var records=U.records||[];
var country=U.country||"the participant's country";
var sdgNames=U.sdg_names||{};
var N=records.length;
var MONO='ui-monospace, Menlo, Consolas, monospace';
var MEC_COLORS={"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
var PARA_RE=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
var STATE_RUN_RE=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
var STATE_GROUP_RE=/\((?:[^()]|\([^()]*\))*\)/g;

function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}
function escRe(s){return s.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");}
function fmt(n){return Number(n).toLocaleString("en-US");}
function $(id){return document.getElementById(id);}

var yearsAll=records.map(function(r){return r.year;}).filter(function(y){return typeof y==="number";});
var Y0=yearsAll.length?Math.min.apply(null,yearsAll):null;
var Y1=yearsAll.length?Math.max.apply(null,yearsAll):null;
var docCount=new Set(records.map(function(r){return r.symbol;})).size;

records.forEach(function(r,i){
 r._i=i;
 var m=String(r.text||"").match(PARA_RE);
 r._para=m?m[1]:null;
 r._paraNum=m?parseFloat(m[1]):Infinity;
 r._hay=(String(r.text||"")+" "+String(r.symbol||"")).toLowerCase();
 r._states=null;
 if(r.mechanism==="Universal Periodic Review"){
  var run=String(r.text||"").match(STATE_RUN_RE);
  var out=[];
  if(run){
   var groups=run[1].match(STATE_GROUP_RE)||[];
   var bad=false;
   for(var g=0;g<groups.length;g++){
    var name=groups[g].slice(1,-1).trim();
    if(name.indexOf(",")>-1||name.length>60){bad=true;break;}
    out.push(name);
   }
   if(bad) out=["State not found"];
  }
  r._states=out;
 }
});
```

Filters:
```js
var F={keyword:"",mechanism:"all",body:"all",type:"all",state:"all",themes:new Set(),y0:Y0,y1:Y1,sdg:"all"};
var filtered=records.slice();
function matches(r,skip){...}
```

State vars: tabIdx, visible, sortAsc, expanded, themeTop, checkResults, sampleSeed, sampleRecs, verdicts, charts.

Render rail:
```js
function chipList(){...}
function renderRail(){
 $("matchNum").textContent=fmt(filtered.length);
 $("ofNum").textContent="of "+fmt(N)+" in the file";
 $("shareFill").style.width=(N?filtered.length/N*100:0)+"%";
 var c=chipList(), h="";
 c.forEach(function(ch){
  h+='<button type="button" class="chip" data-k="'+esc(ch.k)+'" title="remove filter">'+esc(ch.label)+' <b>×</b></button>';
 });
 $("chips").innerHTML=h;
 // state select options refresh
 fillStateOptions();
}
```
Chips click delegation on #chips:
```js
$("chips").addEventListener("click",function(e){
 var b=e.target.closest(".chip"); if(!b) return;
 var k=b.getAttribute("data-k");
 if(k==="keyword"){F.keyword="";$("kw1").value="";$("kw2").value="";}
 else if(k==="mechanism"){F.mechanism="all";$("fMech").value="all";F.body="all";fillBodyOptions();}
 else if(k==="body"){F.body="all";$("fBody").value="all";}
 else if(k==="type"){F.type="all";$("fType").value="all";}
 else if(k==="state"){F.state="all";$("fState").value="all";}
 else if(k==="years"){F.y0=Y0;F.y1=Y1;$("fY0").value=String(Y0);$("fY1").value=String(Y1);}
 else if(k==="sdg"){F.sdg="all";$("fSdg").value="all";}
 else if(k.indexOf("theme:")===0){F.themes.delete(k.slice(6));}
 applyFilters();
});
```

fillSelects:
```js
function fillMechOptions(){
 var counts={}; records.forEach(function(r){counts[r.mechanism]=(counts[r.mechanism]||0)+1;});
 var opts='<option value="all">all ('+fmt(N)+')</option>';
 Object.keys(counts).sort().forEach(function(m){opts+='<option value="'+esc(m)+'">'+esc(m)+' ('+fmt(counts[m])+')</option>';});
 $("fMech").innerHTML=opts;
}
function fillBodyOptions(){
 var src=F.mechanism==="all"?records:records.filter(function(r){return r.mechanism===F.mechanism;});
 var counts={}; src.forEach(function(r){counts[r.body]=(counts[r.body]||0)+1;});
 var opts='<option value="all">all bodies</option>';
 Object.keys(counts).sort(function(a,b){return counts[b]-counts[a]||a.localeCompare(b);}).forEach(function(b){opts+='<option value="'+esc(b)+'">'+esc(b)+' ('+fmt(counts[b])+')</option>';});
 $("fBody").innerHTML=opts; $("fBody").value=F.body==="all"?"all":F.body;
}
```
Careful: if F.body not in new options, value assignment fails silently → select shows first option but F.body stale. Guard: after setting innerHTML, if F.body!=="all" and no option with that value, reset F.body="all". Implement check.

```js
function fillTypeOptions(){ counts over file; }
function fillStateOptions(){
 var src=records.filter(function(r){return matches(r,"state");});
 var counts={}; src.forEach(function(r){ if(r._states) r._states.forEach(function(s){ if(s!=="State not found") counts[s]=(counts[s]||0)+1; }); });
 var opts='<option value="all">all States</option>';
 Object.keys(counts).sort(function(a,b){return counts[b]-counts[a]||a.localeCompare(b);}).forEach(function(s){opts+='<option value="'+esc(s)+'">'+esc(s)+' ('+fmt(counts[s])+')</option>';});
 $("fState").innerHTML=opts;
 if(F.state!=="all" && counts[F.state]) $("fState").value=F.state; else {F.state="all";}
}
function fillYearOptions(){
 var ys=[]; var seen={}; records.forEach(function(r){ if(typeof r.year==="number"&&!seen[r.year]){seen[r.year]=1;ys.push(r.year);} });
 ys.sort(function(a,b){return a-b;});
 var o0='<option value="'+Y0+'">'+Y0+'</option>', o1='';
 ys.forEach(function(y){o0+='<option value="'+y+'">'+y+'</option>'; o1+='<option value="'+y+'">'+y+'</option>';});
 $("fY0").innerHTML=o0; $("fY1").innerHTML=o1;
 $("fY0").value=String(F.y0); $("fY1").value=String(F.y1);
}
function fillSdgOptions(){
 var goals={}; records.forEach(function(r){(r.sdgs||[]).forEach(function(g){goals[Number(g)]=1;});});
 var opts='<option value="all">all SDGs</option>';
 Object.keys(goals).map(Number).sort(function(a,b){return a-b;}).forEach(function(g){
  var nm=sdgNames[String(g)]||"";
  opts+='<option value="'+g+'">SDG '+g+(nm?' — '+esc(nm):'')+'</option>';
 });
 $("fSdg").innerHTML=opts; $("fSdg").value=F.sdg==="all"?"all":String(F.sdg);
}
```

Events wiring, accordion:
```js
document.querySelectorAll(".acc-btn").forEach(function(b){
 b.addEventListener("click",function(){
  var i=b.getAttribute("data-acc");
  var open=b.getAttribute("aria-expanded")==="true";
  document.querySelectorAll(".acc-btn").forEach(function(x){x.setAttribute("aria-expanded","false");});
  document.querySelectorAll(".acc-panel").forEach(function(x){x.hidden=true;});
  if(!open){b.setAttribute("aria-expanded","true");$("accp"+i).hidden=false;}
 });
});
```

Keyword debounce:
```js
var kwT=null;
function onKw(v){
 clearTimeout(kwT);
 kwT=setTimeout(function(){
  F.keyword=v.trim();
  if($("kw1").value!==v)$("kw1").value=v;
  if($("kw2").value!==v)$("kw2").value=v;
  applyFilters();
 },300);
}
$("kw1").addEventListener("input",function(){onKw(this.value);});
$("kw2").addEventListener("input",function(){onKw(this.value);});
```

Select events:
```js
$("fMech").addEventListener("change",function(){F.mechanism=this.value;F.body="all";fillBodyOptions();applyFilters();});
$("fBody").addEventListener("change",function(){F.body=this.value;applyFilters();});
$("fType").addEventListener("change",function(){F.type=this.value;applyFilters();});
$("fState").addEventListener("change",function(){F.state=this.value;applyFilters();});
$("fSdg").addEventListener("change",function(){F.sdg=this.value;applyFilters();});
$("fY0").addEventListener("change",function(){
 var a=Number(this.value),b=Number($("fY1").value);
 if(a>b){var t=a;a=b;b=t;$("fY0").value=String(a);$("fY1").value=String(b);}
 F.y0=a;F.y1=b;applyFilters();
});
$("fY1").addEventListener("change",function(){ same });
$("clearAll").addEventListener("click",function(){
 F.keyword="";F.mechanism="all";F.body="all";F.type="all";F.state="all";F.themes.clear();F.y0=Y0;F.y1=Y1;F.sdg="all";
 $("kw1").value="";$("kw2").value="";
 fillMechOptions();fillBodyOptions();fillTypeOptions();fillYearOptions();fillSdgOptions();fillStateOptions();
 applyFilters();
});
```
Note fillStateOptions uses matches which uses F — after reset fine. But fillStateOptions resets F.state if not found — ok.

Order in clearAll: set F first then fills (fillBodyOptions uses F.mechanism). fillStateOptions sets select value. Also set $("fMech").value="all" etc. — after innerHTML refill, value defaults to first option ("all") anyway. OK.

Tabs:
```js
var tabIdx=0;
var tabBtns=[...document.querySelectorAll(".tab")];
function setTab(i,focus){
 tabIdx=i;
 tabBtns.forEach(function(b,j){
  b.setAttribute("aria-selected",j===i?"true":"false");
  b.tabIndex=j===i?0:-1;
  $("panel"+j).hidden=j!==i;
 });
 $("rail").classList.toggle("rail-min",i>=2);
 if(focus)tabBtns[i].focus();
 renderActive();
}
tabBtns.forEach(function(b,i){
 b.addEventListener("click",function(){setTab(i,false);});
 b.addEventListener("keydown",function(e){
  if(e.key==="ArrowRight"){setTab((i+1)%4,true);e.preventDefault();}
  else if(e.key==="ArrowLeft"){setTab((i+3)%4,true);e.preventDefault();}
  else if(e.key==="Home"){setTab(0,true);e.preventDefault();}
  else if(e.key==="End"){setTab(3,true);e.preventDefault();}
 });
});
```

renderActive:
```js
function renderActive(){
 if(tabIdx===0)renderOverview();
 else if(tabIdx===1)renderRecords();
 else if(tabIdx===2){renderChecks();renderSample();}
 else renderMethod();
}
```

applyFilters:
```js
function applyFilters(){
 filtered=records.filter(function(r){return matches(r);});
 visible=50;
 renderRail();
 renderActive();
 runChecks();
}
```
runChecks after renderActive — runChecks renders checks if tabIdx===2; but renderActive already called renderChecks with old checkResults... reorder: runChecks() before renderActive? runChecks uses themeTop (from overview) — themeTop computed in renderOverview. Circular. Solution: compute themeTop inside runChecks independently? themeTop needed for chart check. Let me compute themeTop in applyFilters before renderActive: `themeTop = topThemes(filtered,10);` then renderActive uses it; runChecks compares. So:

```js
function applyFilters(){
 filtered=records.filter(...);
 themeTop=topThemes(filtered,10);
 visible=50;
 runChecks();      // stores checkResults, renders if tab 2
 renderRail();
 renderActive();
}
```
renderActive tab2 renderChecks uses checkResults — fine.

Init: fill selects, set header/footer, setTab(0), draw initial sample? Draw sample lazily on first tab2 visit: in renderActive tab2, if(!sampleDrawn){drawSample(seed)}. I'll draw on first render of tab 2.

renderOverview:
```js
function renderOverview(){
 // tiles
 var tc={}; filtered.forEach(function(r){tc[r.type]=(tc[r.type]||0)+1;});
 var tb=Object.keys(tc).sort(function(a,b){return tc[b]-tc[a]||a.localeCompare(b);}).map(function(t){return fmt(tc[t])+" "+t;}).join(" · ");
 var docsF=new Set(filtered.map(function(r){return r.symbol;})).size;
 var fy=filtered.map(function(r){return r.year;}).filter(function(y){return typeof y==="number";});
 var fy0=fy.length?Math.min.apply(null,fy):null, fy1=fy.length?Math.max.apply(null,fy):null;
 var mechCounts={}; records.forEach(function(r){mechCounts[r.mechanism]=(mechCounts[r.mechanism]||0)+1;});
 var mechs=Object.keys(mechCounts).sort(function(a,b){return mechCounts[b]-mechCounts[a]||a.localeCompare(b);});
 var tiles='';
 tiles+='<div class="tile"><div class="num">'+fmt(filtered.length)+'</div><div class="cap">records in view</div><div class="sub">'+esc(tb||"—")+' · of '+fmt(N)+' in the file</div><div class="how">How this is computed: count of records passing the left-rail filters; each record counted once and split by the UN’s own type label.</div></div>';
 tiles+='<div class="tile"><div class="num">'+fmt(docsF)+'</div><div class="cap">documents</div><div class="sub">distinct symbols</div><div class="how">How this is computed: number of distinct symbol values among the filtered records.</div></div>';
 tiles+='<div class="tile"><div class="num">'+(fy0?fy0+"–"+fy1:"—")+'</div><div class="cap">years</div><div class="sub">dated by document</div><div class="how">How this is computed: minimum and maximum of the year field among the filtered records.</div></div>';
 mechs.forEach(function(m){
  var sub=filtered.filter(function(r){return r.mechanism===m;});
  var d=new Set(sub.map(function(r){return r.symbol;})).size;
  var ly=sub.length?Math.max.apply(null,sub.map(function(r){return r.year;})):"—";
  var share=filtered.length?Math.round(100*sub.length/filtered.length):0;
  var dot='<i class="dot" style="background:'+(MEC_COLORS[m]||"#6b6459")+'"></i>';
  var extra=m==="Universal Periodic Review"?'<button type="button" class="linkbtn" id="statesToggle" aria-expanded="false">see the States</button><div id="statesBox" hidden></div>':'';
  tiles+='<div class="tile"><div class="cap">'+dot+' '+esc(m)+'</div><div class="num">'+fmt(sub.length)+'</div><div class="sub">'+fmt(d)+' documents · latest '+ly+' · '+share+'% of filtered</div><div class="how">How this is computed: filtered records with mechanism = “'+esc(m)+'”; share = count ÷ '+fmt(filtered.length)+'.</div>'+extra+'</div>';
 });
 $("tiles").innerHTML=tiles;
 // fig1
 $("fig1title").textContent = filtered.length? "Ten most frequent themes among "+fmt(filtered.length)+" filtered records" : "No records match the current filters";
 $("fig1wrap").hidden = !themeTop.length;
 $("fig1none").hidden = !!themeTop.length;
 if(themeTop.length){
  $("fig1tab").innerHTML = '<caption>The same ten themes as the bars above</caption><thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead><tbody>'+
   themeTop.map(function(t){
    return "<tr><td>"+esc(t.theme)+"</td><td class='num'>"+fmt(t.count)+"</td><td class='num'>"+(filtered.length?(100*t.count/filtered.length).toFixed(1):"0.0")+"%</td><td>"+t.y0+"–"+t.y1+"</td></tr>";
   }).join("")+"</tbody>";
  $("fig1how").textContent="How this is computed: each theme of each filtered record counts once, so the bars add up to more than "+fmt(filtered.length)+"; ties are alphabetical. Click a bar to filter by that theme.";
 } else {
  $("fig1tab").innerHTML="";
  $("fig1how").textContent="How this is computed: each theme of each filtered record counts once; no records match, so there is nothing to count.";
 }
 $("fig1src").textContent="Source: WORKSHOP_DATA.uhri, themes field of "+fmt(filtered.length)+" filtered records (of "+fmt(N)+").";
 updateCharts();
 // fig2 texts
 $("fig2title").textContent="Records per year by mechanism — "+fmt(filtered.length)+" filtered records, "+Y0+"–"+Y1;
 $("fig2how").textContent="How this is computed: records per year and per mechanism in the filtered set; every year from "+Y0+" to "+Y1+" appears, so empty years show as gaps.";
 $("fig2src").textContent="Source: WORKSHOP_DATA.uhri, year and mechanism fields of "+fmt(filtered.length)+" filtered records.";
}
```

Wait — fig1 title when filtered 0 but plan says title "Ten most frequent themes among n filtered records". OK.

updateCharts:
```js
var chart1=null,chart2=null;
var endLabels={id:"endLabels",afterDatasetsDraw:function(chart){
 var meta=chart.getDatasetMeta(0); if(!meta||!meta.data) return;
 var ctx=chart.ctx; ctx.save();
 ctx.font="11px "+MONO; ctx.fillStyle="#1d1b18"; ctx.textBaseline="middle";
 meta.data.forEach(function(bar,i){
  var v=chart.data.datasets[0].data[i];
  ctx.fillText(fmt(v),bar.x+6,bar.y);
 });
 ctx.restore();
}};
function ensureCharts(){
 if(chart1||!window.Chart) return;
 chart1=new Chart($("fig1"),{
  type:"bar",
  data:{labels:[],datasets:[{data:[],backgroundColor:"rgba(155,35,53,0.8)",borderWidth:0,maxBarThickness:26}]},
  options:{
   indexAxis:"y",responsive:true,maintainAspectRatio:false,
   onClick:function(e,els){ if(els.length){ var t=themeTop[els[0].index]; if(t&&!F.themes.has(t.theme)){F.themes.add(t.theme);applyFilters();} } },
   plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return " "+fmt(c.parsed.x)+" records";}}}},
   scales:{x:{beginAtZero:true,grid:{color:"#e4ddcd"},ticks:{font:{family:MONO,size:11}}},y:{grid:{display:false},ticks:{font:{family:MONO,size:11}}}}
  },
  plugins:[endLabels]
 });
 var mechs=Object.keys(MEC_COLORS).filter(function(m){return records.some(function(r){return r.mechanism===m;});});
 // include any other mechanism values too
 records.forEach(function(r){ if(mechs.indexOf(r.mechanism)<0) mechs.push(r.mechanism); });
 chart2=new Chart($("fig2"),{
  type:"bar",
  data:{labels:[],datasets:mechs.map(function(m){return {label:m,data:[],backgroundColor:MEC_COLORS[m]||"#6b6459"};})},
  options:{responsive:true,maintainAspectRatio:false,
   plugins:{legend:{position:"top",labels:{usePointStyle:true,boxWidth:8,font:{family:MONO,size:11}}}},
   scales:{x:{stacked:true,grid:{display:false},ticks:{font:{family:MONO,size:11}}},y:{stacked:true,beginAtZero:true,grid:{color:"#e4ddcd"},ticks:{font:{family:MONO,size:11}}}}
  }
 });
}
function updateCharts(){
 if(!chart1) return;
 chart1.data.labels=themeTop.map(function(t){return t.theme;});
 chart1.data.datasets[0].data=themeTop.map(function(t){return t.count;});
 chart1.update();
 var yrs=[]; for(var y=Y0;y<=Y1;y++) yrs.push(String(y));
 var byM={}; records.forEach(function(r){ (byM[r.mechanism]=byM[r.mechanism]||{})[r.year]=(byM[r.mechanism][r.year]||0)+1; });
 var fbyM={}; filtered.forEach(function(r){ (fbyM[r.mechanism]=fbyM[r.mechanism]||{})[r.year]=(fbyM[r.mechanism][r.year]||0)+1; });
 chart2.data.labels=yrs;
 chart2.data.datasets.forEach(function(ds){
  ds.data=yrs.map(function(ys){ return (fbyM[ds.label]&&fbyM[ds.label][Number(ys)])||0; });
 });
 chart2.update();
}
```
ensureCharts called in renderOverview before updateCharts.

States toggle delegation on #tiles:
```js
$("tiles").addEventListener("click",function(e){
 if(e.target.id!=="statesToggle") return;
 var box=$("statesBox"); var open=!box.hidden;
 box.hidden=open; e.target.setAttribute("aria-expanded",String(!open));
 if(!open){
  var upr=filtered.filter(function(r){return r.mechanism==="Universal Periodic Review";});
  var ts=topStates(upr,10);
  box.innerHTML='<div class="cap" style="margin:6px 0 2px">Ten States that made most recommendations to '+esc(country)+' — counts over the '+fmt(upr.length)+' UPR records in view</div>'+
   (ts.length? "<ol class='stateslist'>"+ts.map(function(s){return "<li>"+esc(s.state)+" — "+fmt(s.count)+"</li>";}).join("")+"</ol>" : "<div class='hint'>No States found in the current filter.</div>")+
   '<div class="how">How this is computed: parentheses at the end of each UPR text; a record counts once per State, so two States can co-sponsor one line.</div>';
 }
});
```

topStates:
```js
function topStates(list,k){
 var m={}; list.forEach(function(r){ if(r._states) r._states.forEach(function(s){ if(s!=="State not found") m[s]=(m[s]||0)+1; }); });
 return Object.keys(m).map(function(s){return {state:s,count:m[s]};}).sort(function(a,b){return b.count-a.count||a.state.localeCompare(b.state);}).slice(0,k);
}
```

renderRecords:
```js
var visible=50, sortAsc=false, expanded={};
function renderRecords(){
 var rows=filtered.slice().sort(function(a,b){
  var c=String(a.date||"").localeCompare(String(b.date||"")); if(sortAsc) c=-c; // wait
  ...
 });
}
```
Careful: default date desc: compare b.date vs a.date. If sortAsc, a vs b. Implement:
```js
var c = sortAsc ? String(a.date||"").localeCompare(String(b.date||"")) : String(b.date||"").localeCompare(String(a.date||""));
if(c) return c;
c=String(a.body||"").localeCompare(String(b.body||"")); if(c) return c;
c=a._paraNum-b._paraNum; if(c) return c;
return a._i-b._i;
```

Build:
```js
var shown=rows.slice(0,visible);
$("reccap").textContent=fmt(shown.length)+" of "+fmt(rows.length)+" matching records shown · "+(sortAsc?"oldest first":"newest first")+" · click Date to reverse";
$("thDate").textContent="Date "+(sortAsc?"▴":"▾");
var h="";
shown.forEach(function(r){
 var st = r._states? (r._states.length?r._states.join(", "):"State not found") : "—";
 h+='<tr class="data" data-id="'+esc(r.id)+'" tabindex="0" aria-expanded="'+(expanded[r.id]?"true":"false")+'">'
  +"<td>"+esc(r.date||"")+"</td><td>"+esc(r.body||"")+"</td>"
  +'<td><a href="'+esc(r.doc_url||"#")+'" target="_blank" rel="noopener">'+esc(r.symbol||"")+'</a></td>'
  +"<td>"+(r._para?esc(r._para):"–")+"</td>"
  +"<td>"+highlight(firstLine(r.text))+"</td>"
  +"<td>"+esc(st)+"</td></tr>";
 if(expanded[r.id]){
  h+='<tr class="detail" data-id="'+esc(r.id)+'"><td colspan="6">'
   +'<div class="para-big">'+(r._para?esc(r._para):"–")+'</div>'
   +'<p class="fulltext">'+highlight(r.text)+'</p>'
   +'<div class="labels">'+labelsHtml(r)+'</div>'
   +'<div class="btnrow"><button type="button" class="btn copybtn" data-id="'+esc(r.id)+'">'+(r._para?"Copy citation":"Copy citation (no paragraph number in this extract)")+'</button>'
   +'<a class="btn" href="'+esc(r.doc_url||"#")+'" target="_blank" rel="noopener">Open the UN document</a></div>'
   +'</td></tr>';
 }
});
if(!shown.length) h='<tr><td colspan="6" class="nomatch">No records match the current filters.</td></tr>';
$("recbody").innerHTML=h;
$("moreBtn").hidden = shown.length>=rows.length;
}
```

toggleRow:
```js
function toggleRow(id){
 if(expanded[id]) delete expanded[id]; else expanded[id]=1;
 renderRecords();
}
```

Delegation:
```js
$("recbody").addEventListener("click",function(e){
 var cp=e.target.closest(".copybtn");
 if(cp){ copyCitation(cp.getAttribute("data-id"),cp); return; }
 var a=e.target.closest("a"); if(a) return;
 var tr=e.target.closest("tr.data"); if(tr) toggleRow(tr.getAttribute("data-id"));
});
$("recbody").addEventListener("keydown",function(e){
 if((e.key==="Enter"||e.key===" ")&&e.target.classList&&e.target.classList.contains("data")){e.preventDefault();toggleRow(e.target.getAttribute("data-id"));}
});
$("thDate").addEventListener("click",function(){sortAsc=!sortAsc;renderRecords();});
$("moreBtn").addEventListener("click",function(){visible+=50;renderRecords();});
```

copyCitation:
```js
function copyCitation(id,btn){
 var r=records.filter(function(x){return x.id===id;})[0]; if(!r) return;
 var cite=r._para? r.symbol+", para. "+r._para : r.symbol;
 copyText(cite,function(ok){
  if(ok){ var old=btn.textContent; btn.textContent="Copied ✓"; setTimeout(function(){btn.textContent=old;},2000); }
 });
}
```

labelsHtml as planned.

Checks (runChecks + renderChecks) as planned.

renderChecks:
```js
function renderChecks(){
 $("checks").innerHTML=checkResults.map(function(c){
  var mark=c.status==="pass"?"✓ pass":c.status==="warn"?"⚠ warning":"✗ check failed";
  return '<div class="checkline"><span class="cname">'+esc(c.name)+'</span><span class="cdetail">'+esc(c.detail)+(c.note?' '+esc(c.note):'')+'</span><span class="st '+c.status+'">'+mark+'</span></div>';
 }).join("");
}
```

Sample:
```js
var sampleSeed=1, sampleRecs=[], verdicts={}, sampleDrawn=false, openCard=null;
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return ((t^t>>>14)>>>0)/4294967296;};}
function drawSample(seed){
 sampleSeed=seed>>>0||1;
 var rng=mulberry32(sampleSeed);
 var n=filtered.length, k=Math.min(10,n);
 var idx={}, list=[];
 while(list.length<k){ var j=Math.floor(rng()*n); if(!idx[j]){idx[j]=1;list.push(filtered[j]);} }
 sampleRecs=list; verdicts={}; openCard=null;
 renderSample();
}
function renderSample(){
 var f=0,d=0,u=0;
 sampleRecs.forEach(function(r){var v=verdicts[r.id]; if(v==="fit")f++; else if(v==="dont")d++; else if(v==="unsure")u++;});
 $("tally").textContent="Themes: "+f+" fit · "+d+" don't fit · "+u+" unsure of "+sampleRecs.length+" judged · seed "+sampleSeed+" — your judgement of the UN's labels; nothing is sent anywhere.";
 $("cards").innerHTML=sampleRecs.map(function(r){
  var open=openCard===r.id;
  var v=verdicts[r.id]||"";
  return '<div class="card">'
   +'<button type="button" class="card-btn" data-id="'+esc(r.id)+'" aria-expanded="'+open+'"><span class="arr">'+(open?"▾":"▸")+'</span> '+esc(r.symbol)+' · para '+(r._para?esc(r._para):"–")+'</button>'
   +'<div class="card-panel" '+(open?"":"hidden")+'>'
   +'<p class="fulltext">'+esc(r.text)+'</p>'
   +'<div class="themechips">'+(r.themes&&r.themes.length? r.themes.map(function(t){return "<span>"+esc(t)+"</span>";}).join("") : '<span class="missing">not labelled</span>')+'</div>'
   +'<div class="vbtns">'
   +'<button type="button" class="vbtn'+(v==="fit"?" on":"")+'" data-id="'+esc(r.id)+'" data-v="fit">Fits</button>'
   +'<button type="button" class="vbtn'+(v==="dont"?" on":"")+'" data-id="'+esc(r.id)+'" data-v="dont">Doesn\'t fit</button>'
   +'<button type="button" class="vbtn'+(v==="unsure"?" on":"")+'" data-id="'+esc(r.id)+'" data-v="unsure">Unsure</button>'
   +'</div></div></div>';
 }).join("");
}
$("cards").addEventListener("click",function(e){
 var vb=e.target.closest(".vbtn");
 if(vb){ verdicts[vb.getAttribute("data-id")]=vb.getAttribute("data-v"); renderSample(); return; }
 var cb=e.target.closest(".card-btn");
 if(cb){ var id=cb.getAttribute("data-id"); openCard=(openCard===id?null:id); renderSample(); }
});
$("drawBtn").addEventListener("click",function(){ drawSample(Number($("seedBox").value)||1); });
$("drawAgain").addEventListener("click",function(){ var s=Math.floor(Math.random()*100000)+1; $("seedBox").value=s; drawSample(s); });
$("drawSeed").addEventListener("click",function(){ drawSample(Number($("seedBox").value)||1); });
```

In renderActive tab2: `if(!sampleDrawn){sampleDrawn=true; drawSample(Number($("seedBox").value)||1);} else renderSample();` — drawSample calls renderSample. Also renderChecks.

Method tab: static; renderMethod fills srcBlock:
```js
function renderMethod(){
 $("srcBlock").innerHTML="Data: <a href='"+esc(U.source_url||"#")+"' target='_blank' rel='noopener'>"+esc(U.source||"OHCHR Universal Human Rights Index")+"</a> · "+fmt(N)+" records · "+docCount+" documents · "+Y0+"–"+Y1+" · built "+esc(U.built||"")+" · dated by document.";
}
```

CSV & summary:
```js
$("csvBtn").addEventListener("click",function(){
 var csv=buildCSV();
 var blob=new Blob([csv],{type:"text/csv;charset=utf-8"});
 var a=document.createElement("a");
 a.href=URL.createObjectURL(blob);
 a.download="uhri-"+String(country).toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"")+"-filtered.csv";
 document.body.appendChild(a); a.click(); a.remove();
 setTimeout(function(){URL.revokeObjectURL(a.href);},2000);
 $("exportNote").textContent="CSV downloaded: "+fmt(filtered.length)+" rows of "+fmt(N)+", with the full text and labels, generated in your browser. Nothing was sent anywhere.";
});
$("sumBtn").addEventListener("click",function(){
 copyText(summaryText(),function(ok){
  $("exportNote").textContent=ok?"Summary copied to the clipboard — the only thing that left this page.":"Copy failed — select the text manually.";
 });
});
```

Header/footer init:
```js
$("kicker").textContent="UHRI · "+String(country).toUpperCase();
$("title").textContent="UN human rights recommendations and observations: "+country;
$("meta").innerHTML='<a href="'+esc(U.source_url||"#")+'" target="_blank" rel="noopener">'+esc(U.source||"source")+'</a> · '+fmt(N)+' records · '+docCount+' documents · '+Y0+'–'+Y1+' · built '+esc(U.built||"")+' · dated by document';
$("foot").innerHTML='Built on OHCHR UHRI data · '+fmt(N)+' records · <a href="'+esc(U.source_url||"#")+'" target="_blank" rel="noopener">'+esc(U.source||"source")+'</a>';
document.title="UHRI · "+country+" — UN recommendations dashboard";
```

Init sequence:
```js
fillMechOptions(); fillBodyOptions(); fillTypeOptions(); fillYearOptions(); fillSdgOptions(); fillStateOptions();
setTab(0,false);
```
setTab calls renderActive → renderOverview → ensureCharts + updateCharts. runChecks needs themeTop — setTab doesn't call applyFilters. Let me init: themeTop=topThemes(records,10); checkResults=[]; runChecks(); then setTab(0). runChecks uses filtered (records) and themeTop — fine.

Also note: fillStateOptions called in renderRail each time — it rebuilds options; but it also may reset F.state — careful: fillStateOptions sets $("fState").value only if counts[F.state]; else F.state="all". During renderRail after user selected a state, counts computed with skip "state" so state still present → value kept. Good. But calling fillStateOptions inside renderRail rebuilds the select every filter change — fine.

Hmm, one issue: fillStateOptions is called in renderRail, which is called in applyFilters — but the state select's change event already set F.state; fillStateOptions preserves. OK.

Also body select: when mechanism changes we call fillBodyOptions; but renderRail doesn't refill body — body options depend on mechanism only, changed only via fMech handler. OK.

Edge: Y0/Y1 null (no years) — guard: if yearsAll empty, year selects empty; matches year filter would exclude all... If no years in data, set F.y0=-Infinity? Data has years; but handle: if Y0==null, skip year filter in matches (treat as no filter) and hide year selects? Keep simple: if Y0==null set F.y0=0,F.y1=0 and matches: if Y0==null skip year check. I'll add `if(skip!=="year" && Y0!=null){...}`.

Now checks code with details — write carefully.

Also note plan: "Paragraph numbers ... UPR is expected at 100%, and a lower figure is shown as a warning, not an error." Implemented.

Now CSS full. Let me write it:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mut:#5b564c;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--ink)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header{padding:22px 30px 16px;border-bottom:1px solid var(--rule)}
.kicker{font:11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--red)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:34px;line-height:1.15;margin:10px 0 8px;max-width:900px}
.meta{margin:0;font-size:13px;color:var(--mut)}
.layout{display:flex;align-items:flex-start}
aside#rail{width:260px;flex:0 0 260px;border-right:1px solid var(--rule);padding:18px 20px 30px;position:sticky;top:0;max-height:100vh;overflow:auto}
.rail-h{display:flex;justify-content:space-between;align-items:baseline}
.lbl{font:11px var(--mono);letter-spacing:.16em;color:var(--red)}
#clearAll{background:none;border:none;font:11px var(--mono);color:var(--mut);cursor:pointer;text-decoration:underline;padding:0}
.bignum{font-family:Georgia,serif;font-size:54px;line-height:1;margin:12px 0 2px}
.of{font:11px var(--mono);color:var(--mut)}
.sharebar{height:4px;background:var(--rule);margin:10px 0 4px}
.sharebar i{display:block;height:100%;background:var(--red);width:0}
.chips{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0 6px;min-height:4px}
.chip{font:11px var(--mono);background:#fbf8f1;border:1px solid var(--rule);border-radius:11px;padding:2px 8px;cursor:pointer;color:var(--ink)}
.chip b{color:var(--red);font-weight:400}
.acc-btn{width:100%;display:flex;justify-content:space-between;align-items:center;background:none;border:none;border-top:1px solid var(--rule);padding:11px 0 9px;font:12px var(--mono);letter-spacing:.1em;color:var(--ink);cursor:pointer;text-align:left}
.acc-btn .n{color:var(--red);margin-right:6px}
.acc-btn .arr{color:var(--mut)}
.acc-panel{padding:2px 0 14px}
.acc-panel input[type=search]{width:100%;padding:6px 8px;border:1px solid var(--rule);background:#fbf8f1;font:14px inherit;color:var(--ink)}
.hint{font:11px var(--mono);color:var(--mut);margin-top:5px;line-height:1.5}
.how{font:11px var(--mono);color:var(--mut);margin-top:8px;line-height:1.5}
.fl{display:block;font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mut);margin:10px 0 3px}
.fl select{display:block;width:100%;margin-top:3px;padding:5px 6px;border:1px solid var(--rule);background:#fbf8f1;font:13px -apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink)}
.yrow{display:flex;gap:8px}.yrow .fl{flex:1}
main{flex:1;min-width:0;padding:18px 30px 50px}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin-bottom:20px;flex-wrap:wrap}
.tab{background:none;border:none;border-bottom:2px solid transparent;padding:9px 13px;font:12px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--mut);cursor:pointer}
.tab[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
.tiles{display:flex;flex-wrap:wrap;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-bottom:8px}
.tile{padding:16px 26px 14px 0;margin-right:26px;border-right:1px solid var(--rule);min-width:170px}
.tile:last-child{border-right:none}
.num{font-family:Georgia,serif;font-size:46px;line-height:1}
.cap{font:11px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin-top:6px}
.sub{font-size:13px;color:var(--mut);margin-top:3px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.linkbtn{background:none;border:none;font:11px var(--mono);color:var(--red);text-decoration:underline;cursor:pointer;padding:0;margin-top:6px}
.stateslist{margin:6px 0;padding-left:20px;font-size:14px}
.fig{margin:30px 0 10px;max-width:860px}
.figno{font:11px var(--mono);letter-spacing:.16em;color:var(--red)}
.figtitle{font-family:Georgia,serif;font-weight:400;font-size:21px;margin:6px 0 12px}
.chartwrap{position:relative}
.src{font:11px var(--mono);color:var(--mut);margin-top:10px}
.nomatch{font:13px var(--mono);color:var(--mut);padding:18px 0}
table{border-collapse:collapse;width:100%;font-size:14px;margin-top:6px}
caption{text-align:left;font:11px var(--mono);color:var(--mut);padding:8px 0 4px}
th{font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:1px solid var(--ink);padding:6px 10px 6px 0;color:var(--ink)}
td{border-bottom:1px solid var(--rule);padding:7px 10px 7px 0;vertical-align:top}
th.num,td.num{text-align:right;padding-right:0}
.thbtn{background:none;border:none;font:inherit;letter-spacing:inherit;text-transform:inherit;color:inherit;cursor:pointer;padding:0}
tbody tr.data{cursor:pointer}
tbody tr.data:hover{background:#ece5d5}
tr.detail td{background:#efe9db;padding:16px 20px}
.para-big{font-family:Georgia,serif;font-size:42px;color:var(--red);line-height:1;margin-bottom:8px}
.fulltext{max-width:760px;margin:0 0 10px;white-space:pre-wrap}
.labels{font-size:13px;max-width:760px}
.labels .ll{font:10px var(--mono);letter-spacing:.12em;color:var(--red);margin-right:6px}
.labels>div{margin:3px 0}
.missing{color:var(--mut);font-style:italic}
mark{background:#f0d9a0;padding:0 1px}
.btn{display:inline-block;background:none;border:1px solid var(--ink);color:var(--ink);font:12px var(--mono);padding:7px 14px;cursor:pointer;text-decoration:none;margin:4px 8px 4px 0}
.btn:hover{background:#e9e2d1}
.btnrow{margin-top:10px}
.searchrow{display:flex;align-items:baseline;gap:12px;margin-bottom:8px;flex-wrap:wrap}
.searchrow input{flex:1;min-width:260px;padding:8px 10px;border:1px solid var(--rule);background:#fbf8f1;font:15px inherit;color:var(--ink)}
.ptitle{font-family:Georgia,serif;font-weight:400;font-size:22px;margin:26px 0 6px}
.checkline{display:flex;gap:14px;align-items:baseline;padding:8px 0;border-bottom:1px solid var(--rule);font-size:14px}
.cname{font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;color:var(--ink);min-width:150px}
.cdetail{flex:1;color:var(--mut)}
.st{font:11px var(--mono);white-space:nowrap}
.st.pass{color:#0f766e}.st.warn{color:#b45309}.st.fail{color:var(--red)}
.sample-controls{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:10px 0}
.seedlbl{margin:0}
.seedlbl input{width:90px;padding:5px 6px;border:1px solid var(--rule);background:#fbf8f1;font:13px var(--mono)}
.tally{font:12px var(--mono);color:var(--ink);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:8px 0;margin:8px 0 4px}
.card{border-bottom:1px solid var(--rule)}
.card-btn{width:100%;text-align:left;background:none;border:none;padding:9px 0;font:13px var(--mono);cursor:pointer;color:var(--ink)}
.card-btn .arr{color:var(--red);margin-right:6px}
.card-panel{border-left:2px solid var(--red);padding:2px 0 14px 16px;margin:0 0 12px}
.themechips{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0}
.themechips span{font:11px var(--mono);border:1px solid var(--rule);border-radius:10px;padding:2px 8px;background:#fbf8f1}
.vbtns{display:flex;gap:6px}
.vbtn{background:none;border:1px solid var(--rule);font:11px var(--mono);padding:5px 12px;cursor:pointer;color:var(--ink)}
.vbtn.on{background:var(--red);border-color:var(--red);color:#fff}
.method{max-width:760px;padding-left:20px}
.method li{margin:7px 0}
.credits{font:11px var(--mono);color:var(--mut);max-width:760px;line-height:1.6}
footer{border-top:1px solid var(--rule);padding:12px 30px;font:11px var(--mono);color:var(--mut)}
footer a{color:var(--ink)}
@media (max-width:900px){.layout{flex-direction:column}aside#rail{width:100%;flex:none;position:static;max-height:none;border-right:none;border-bottom:1px solid var(--rule)}main{padding:14px 18px 40px}header{padding:16px 18px 12px}}
```

Chart wrap heights: set inline style height on .chartwrap divs: fig1 340px, fig2 300px. With maintainAspectRatio:false, canvas fills wrap. Set `.chartwrap canvas{width:100%!important;height:100%!important}`? Chart.js with maintainAspectRatio:false uses parent size; parent needs explicit height. I'll set style="height:340px" on wrap. Good.

Note: when fig1wrap hidden and later shown, chart may need resize — Chart.js responsive handles via ResizeObserver; hidden→shown triggers resize. Should be OK.

One more: `runChecks` chart-vs-table check compares themeTop with alt recompute — but themeTop computed in applyFilters; at init I set themeTop=topThemes(records,10) before runChecks. Good.

Also plan wants check "the ten rows under the chart show the same values" — our table is built from themeTop, and check recomputes alt and compares — covers it.

Now, potential pitfall: `records.filter` in copyCitation — fine.

`highlight` on full text with keyword — good.

Also the "Recommending State" filter select label — plan: "A State select joins this heading when States are extracted." Always present is fine.

Let me also double check STATE_RUN_RE against "…(Croatia)." — text ends "...(Croatia)." → run matches "(Croatia)" then `\s*[;.]?\s*$` consumes ".". Good. Against treaty-body "(art. 15)." — only applied to UPR. Good. Nested "(Venezuela (Bolivarian Republic of))" — regex `\((?:[^()]|\([^()]*\))*\)` matches outer with one nesting level. Good. Multiple "(Cabo Verde) (Slovenia) (Togo);" — run group `((?:\s*\(...\))+)` matches all three. Good.

Edge: text ending with "..." no parenthesis → no run → out=[] → "State not found" display. Good.

Now the sample: "Check 10 at random" draws — initial draw when tab first opened. Also drawBtn redraws with seed box. Fine.

Also plan: cards "listed as one line each, one open at a time" — done via openCard.

Now assemble everything. Also add `lang="en"`.

Line count estimate ~700-800. Good.

One more requirement: "Every row that shows a document has its symbol, linked to doc_url in a new tab." — table rows do; sample cards: card button line shows symbol — make it a link? Card button contains symbol; add link inside panel: "Open the UN document" link in card panel. Add: `<a href=doc_url target=_blank>Open the UN document</a>` in card panel. Also make card-btn line include link? Button can't contain link cleanly; panel has it. Also checks list symbols — plain text fine (not rows showing documents per se). Table rows satisfy.

Also "Copy citation" copies `symbol, para. N` — done.

CSV comment lines: use "#" prefix — done.

Let me also handle `U.count` possibly missing: Number(undefined)=NaN → check fails gracefully: status N===cnt? NaN comparison false → fail with values shown. Fine, but display "undefined". Use `U.count` raw in detail. OK.

Write final. Also ensure no `fetch` etc. Clipboard only.

Double-check tablist arrow-key: buttons have keydown handler; also roving tabindex set in setTab.

Also initial aria: tab0 selected.

Potential issue: `renderActive` for tab 3 calls renderMethod each time — fine.

`runChecks` called in applyFilters before renderRail/renderActive; renderChecks inside runChecks only if tabIdx===2 — but renderActive also calls renderChecks for tab2; harmless duplication. I'll have runChecks only compute+store, and renderChecks separate; renderActive calls renderChecks when tab2. Simpler.

Let me finalize the checks function code:

```js
var checkResults=[];
function runChecks(){
 var res=[];
 var cntRaw=U.count, cnt=Number(U.count);
 res.push({name:"Record count",detail:"records.length = "+fmt(N)+" · the file's own count field = "+esc(String(cntRaw))+" (as a number: "+cnt+")",status:N===cnt?"pass":"fail"});
 function sumBy(fn){var m={};records.forEach(function(r){var k=fn(r);m[k]=(m[k]||0)+1;});return Object.keys(m).reduce(function(a,k){return a+m[k];},0);}
 var sm=sumBy(function(r){return r.mechanism;}), sb=sumBy(function(r){return r.body;}), sy=sumBy(function(r){return r.year;});
 res.push({name:"Partitions",detail:"counts per mechanism sum to "+fmt(sm)+", per body to "+fmt(sb)+", per year to "+fmt(sy)+" — each should equal "+fmt(N),status:(sm===N&&sb===N&&sy===N)?"pass":"fail"});
 var st=sumBy(function(r){return r.type;});
 res.push({name:"Type partition",detail:"counts per type sum to "+fmt(st)+" against the headline "+fmt(N),status:st===N?"pass":"fail"});
 var alt={}; filtered.forEach(function(r){(r.themes||[]).forEach(function(t){alt[t]=(alt[t]||0)+1;});});
 var altTop=Object.keys(alt).map(function(k){return [k,alt[k]];}).sort(function(a,b){return b[1]-a[1]||a[0].localeCompare(b[0]);}).slice(0,10);
 var ok4=themeTop.length===altTop.length;
 if(ok4){ for(var i=0;i<themeTop.length;i++){ if(themeTop[i].theme!==altTop[i][0]||themeTop[i].count!==altTop[i][1]){ok4=false;break;} } }
 var largest=themeTop.length?themeTop[0].count:0;
 ok4=ok4&&largest<=filtered.length;
 res.push({name:"Chart against table",detail:"each FIG.01 bar recomputed by a second loop over the "+fmt(filtered.length)+" filtered records matches the ten table rows; largest bar "+fmt(largest)+" ≤ "+fmt(filtered.length),status:ok4?"pass":"fail"});
 var bad=[]; records.forEach(function(r){
  var ok=/^https:\/\/docs\.un\.org\//i.test(String(r.doc_url||""));
  if(ok){ var u=String(r.doc_url), s=String(r.symbol); try{u=decodeURIComponent(u);}catch(e){} try{s=decodeURIComponent(s);}catch(e){} ok=u.toLowerCase().lastIndexOf(s.toLowerCase())===u.length-s.length && s.length>0; }
  if(!ok) bad.push(r.symbol);
 });
 res.push({name:"Links",detail:bad.length?("records whose doc_url does not start with https://docs.un.org/ or does not end with its symbol: "+bad.slice(0,6).join(", ")+(bad.length>6?" (+ "+(bad.length-6)+" more)":"")):("all "+fmt(N)+" doc_url values start with https://docs.un.org/ and end with their symbol (case-insensitive, decoded)"),status:bad.length?"fail":"pass"});
 var pm={}; records.forEach(function(r){var m=r.mechanism;pm[m]=pm[m]||{t:0,p:0};pm[m].t++;if(r._para)pm[m].p++;});
 var det6=Object.keys(pm).map(function(m){return m+": "+Math.round(100*pm[m].p/pm[m].t)+"% with a number";}).join(" · ");
 var upr=pm["Universal Periodic Review"];
 res.push({name:"Paragraph numbers",detail:det6,status:(upr&&upr.p<upr.t)?"warn":"pass",note:(upr&&upr.p<upr.t)?"UPR below 100% — a warning, not an error":""});
 var uprRecs=records.filter(function(r){return r.mechanism==="Universal Periodic Review";});
 var noState=uprRecs.filter(function(r){return !r._states||!r._states.length||r._states[0]==="State not found";});
 res.push({name:"States found",detail:fmt(uprRecs.length-noState.length)+" of "+fmt(uprRecs.length)+" UPR records have at least one State"+(noState.length?" — without one: "+noState.slice(0,6).map(function(r){return r.symbol+" (“…"+String(r.text||"").slice(-50)+"”)";}).join("; ")+(noState.length>6?" (+ "+(noState.length-6)+" more)":""):"") ,status:noState.length?"warn":"pass"});
 var ids={}; records.forEach(function(r){ids[r.id]=1;});
 var idc=Object.keys(ids).length;
 var tm={}; records.forEach(function(r){var t=String(r.text||"");tm[t]=(tm[t]||0)+1;});
 var dups=Object.keys(tm).filter(function(t){return tm[t]>1;});
 var extra=0; dups.forEach(function(t){extra+=tm[t]-1;});
 var noTh=records.filter(function(r){return !r.themes||!r.themes.length;}).length;
 var noSdg=records.filter(function(r){return !r.sdgs||!r.sdgs.length;}).length;
 var noAp=records.filter(function(r){return !r.affected_persons||!r.affected_persons.length;}).length;
 res.push({name:"Duplicates and gaps",detail:"distinct id = "+fmt(idc)+" of "+fmt(N)+" · duplicate texts: "+dups.length+" texts appear more than once ("+fmt(extra)+" extra records) · not labelled: "+fmt(noTh)+" without themes, "+fmt(noSdg)+" without SDGs, "+fmt(noAp)+" without affected persons",status:idc!==N?"fail":(dups.length?"warn":"pass")});
 checkResults=res;
}
```

Note `lastIndexOf(...)===u.length-s.length` — endsWith equivalent. Good.

Now write the final file. Also the method list items (static in HTML):

```html
<ol class="method">
 <li>Every number on this page is computed by loops over the records in the attached file (<span class="mono">WORKSHOP_DATA.uhri</span>); nothing is estimated and no language model is called.</li>
 <li>The headline count is the number of records passing the filters in the left rail; documents are distinct <span class="mono">symbol</span> values; years are the minimum and maximum of <span class="mono">year</span>, which is the document's date, not the date a recommendation was made or accepted.</li>
 <li>Filters combine with AND: mechanism, body, type and recommending State match the field exactly; years are inclusive between the two selects; an SDG matches when the record lists that goal; the keyword requires every typed word to appear literally in the text or the symbol — "torture" will not find "ill-treatment".</li>
 <li>Paragraph numbers are read from the start of each text with a fixed pattern ("71." or "144.43"); recommending States are read only from the parentheses at the end of UPR texts, and a group with a comma or over 60 characters is rejected as "State not found".</li>
 <li>Theme counts count each theme of each record once, so they add up to more than the record count; the app never removes, renames or re-labels a UN label — the year range per theme and the random sample let you judge them.</li>
 <li>The CSV export is generated in your browser from the filtered rows, with the full text and all labels; the only thing that can leave this page is the clipboard write when you press a Copy button.</li>
</ol>
```
.mono class: font mono small.

OK, writing the final answer now. Keep pre-code text to ≤3 sentences.

One more check on the tab labels: "01 OVERVIEW · 02 RECORDS · 03 CHECK · 04 METHOD & EXPORT" — use those.

Also ensure the rail on tabs 3/4 keeps number/bar/chips: `.rail-min .acc, .rail-min .how{display:none}` — keep the "How this is computed" hidden too? Plan: "the rail keeps only the number, the bar and the chips." So hide acc and the how line and FILTERS header? Keep header+clear all? "keeps only the number, the bar and the chips" — I'll hide .acc and .how, keep header row (Clear all is a button... it says only number/bar/chips; but Clear all is useful; keep it — "about seven things" tolerance). I'll hide .acc and .rail .how via `.rail-min .acc,.rail-min .how{display:none}`.

Also chips container remains.

Now, fig1 chart click adds theme chip — after applyFilters, chart updates. Good.

Also add title attribute on bars? tooltip covers.

Final check on Chart.js v4 API: `new Chart(ctx, config)` where ctx can be canvas element. onClick in options: `(event, elements, chart)`. elements have `.index`. OK. Tooltip callbacks label: `c.parsed.x` for horizontal bar. OK.

Stacked: scales x/y stacked:true. OK.

Write it.