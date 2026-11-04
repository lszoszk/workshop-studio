Let me plan this app carefully. The user wants a full dashboard app on `WORKSHOP_DATA.uhri` for Kenya (country read from data). Four tabs, left rail filters, checks tab with seeded random sample, method & export tab. Single HTML file, inline CSS/JS, Chart.js preloaded, no external resources.

Key requirements to implement:

1. Header: monospace label "UHRI · {country}", serif title, source line with link, n records, n documents, first–last year, built date, "dated by document" hint.

2. Left rail filters: FILTERS heading, Clear all, big number matching records (aria-live polite) "of N in the file", red share bar, chips for active filters. Three numbered accordion headings (01 Keyword, 02 Mechanism/body/type, 03 Years and SDG), each closed until clicked, one open at a time, aria-expanded. On tabs 03/04 rail keeps only number, bar, chips (hide the accordions).

Wait — "shown on tabs 01 and 02; on 03 and 04 the rail keeps only the number, the bar and the chips." So the accordion section is hidden on tabs 3 and 4.

Filters:
- Keyword: text input, 300ms debounce, hint "literal match, not synonyms". Every word must occur as substring of text or symbol (trimmed, lowercased).
- Mechanism (all/each), Body (values present in chosen mechanism, with counts), Type (all/each value present). State select joins heading 02 when States extracted — a select listing every State found with counts. Hmm, "A State select joins this heading when States are extracted." So add a State filter (dropdown of all states found in UPR records, with counts). That's a filter on extracted recommending states.
- Years: from/to selects of distinct years present in data; SDG select (goal number + name from sdg_names, only goals present).

All filters AND. Chips removable.

3. Tab 01 Overview:
- Big number tiles: total records in file (all records — wait, "The first tile counts all records in the file" — hmm, but filters... "A row of big serif numbers. The first tile counts all records in the file: recommendations, concerns/observations and any other type. Under the number, one line gives the breakdown per type... The Type filter (all / each type value present) starts on 'all'." Hmm, this is a bit confusing. I think the first tile shows the filtered count? Actually re-reading: "The first tile counts all records in the file" — but then "Beside it: documents (distinct symbol) and years (min–max of year). Below, one tile per mechanism (records, documents, latest year, share of the filtered set)."

Hmm. I think the intent: the headline tile shows the count of the current filtered set (which by default = all records in the file), with breakdown per type. Actually "counts all records in the file" might mean it counts all types (not just recommendations). But filters apply to everything ("Every tab reads the same filtered set"). The mechanism tiles say "share of the filtered set", implying the headline is also of the filtered set. I'll make the headline tile = filtered count, with type breakdown of the filtered set, and note "of N in the file". Actually to be safe: headline tile shows filtered count big, with "of N records in the file" beneath, plus type breakdown line. That satisfies both readings. Hmm, but the plan says "The first tile counts all records in the file". Maybe they want the tile to always show the file total regardless of filter? But then "Every tile and figure has a one-line How this is computed note" and mechanism tiles show "share of the filtered set" — share relative to filtered set. If headline were file total, shares would be of filtered... ambiguous. I'll go with: headline = filtered count (default = all), with "of N in the file" sub-line and type breakdown. That's most consistent with "Every tab reads the same filtered set" and the rail showing "n matching of N". Actually wait — re-reading again: "The first tile counts **all records** in the file: recommendations, concerns/observations and any other `type`." The bold "all records" contrasts with counting only recommendations — i.e., it counts all types, not just recommendations. So headline = filtered count including all types. Good, my reading works.

- Documents tile: distinct symbol in filtered set. Years tile: min–max year in filtered set (or of file? "years (min–max of year)" — of filtered set, I'll do filtered, with note). Hmm, header already shows file years. For the tile I'll use filtered set min–max, note says so. Actually maybe file-level. I'll do filtered and note "of the filtered records".

- Mechanism tiles: one per mechanism, records, documents, latest year, share of filtered set. UPR tile has "see the States" link opening in place a short list "Ten States that made most recommendations to Kenya" with counts for current filter.

- FIG.01: top 10 themes among filtered records, horizontal Chart.js bar, ranked, count at end of bar, red at 80% opacity. Clicking a bar adds theme as filter chip — so theme must be a filter too! Wait, filters listed are keyword, mechanism/body/type/state, years/SDG. But "Clicking a bar adds that theme as a filter chip." So theme is also a filter (chip). I need a theme filter — clicking bar adds chip; chip removable. I'll add theme to the filter state (maybe not in the rail accordions to keep click count low — chips are removable, that's fine; the plan says active filters show as chips). I'll implement theme filter as chip-only (added via chart click), removable. That keeps rail at 3 headings.

- Under chart: small table Theme | Records | % of filtered | Years (first–last). Note about multi-theme.

- FIG.02: stacked bars per year by mechanism, all years from min to max of... "every year from the first to the last appears" — first to last of the file (or filtered?). "Records per year by mechanism: stacked bars for the current filter; every year from the first to the last appears, so empty years are visible gaps." I'll use file min–max year range so gaps visible; counts from filtered set. Colors: UPR #c2410c, Treaty bodies #0f766e, Special Procedures #7c3aed, with legend. But mechanism values are exactly those three per data description. I'll map by name with fallback color.

4. Tab 02 Records:
- Search field across top — "the same box as 01 Keyword". Hmm: "One search field across the top ('Search n records, e.g. torture'), the same box as 01 Keyword." So the keyword input lives in the rail on tab 01, and on tab 02 there's a search field at top which is the same filter. To avoid two inputs, I could move/duplicate: simplest is to have the keyword input in the rail, and on tab 02 also show a search box at top that syncs with the same state. Or place the keyword input in the rail always, and on tab 02 the rail is visible too (rail is always visible). But plan says on tab 02 the rail shows accordions (headings shown on tabs 01 and 02). So the keyword box is in the rail on tab 02 as well. But plan explicitly says tab 02 has "One search field across the top". I'll render a search input at top of tab 02 bound to the same keyword state (two inputs synced). That's fine.

- Table columns: Date | Body | Symbol (link) | Para. | First line | Recommending State. Caption "rows shown of rows matching", "newest first", clicking Date header reverses sort. Keyword matches highlighted with <mark>. 50 rows at a time, "Show 50 more" button.

- Sort: date desc, then body, then paragraph number ascending (numeric), then file order. Clicking Date header toggles asc/desc (reverses).

- Row click expands in place: big red paragraph number, full verbatim text, labels (themes chips, sdgs with names, sdg_targets, affected_persons, section when present), "Copy citation" button, "Open the UN document" link. Copy citation copies "symbol, para. N" or symbol alone with label "(no paragraph number in this extract)". "Copied" confirmation 2s.

- Recommending State column: UPR rows only, dash otherwise. State filter select in heading 02.

5. Tab 03 Check:
- "Check this dashboard" panel, one line per check: record count vs Number(count); partitions per mechanism/body/year sum; type partition; chart vs table (each bar value equals recomputed count, ten rows same, largest bar ≤ filtered count); links (doc_url starts with https://docs.un.org/ and ends with symbol case-insensitive after decoding; failures listed); paragraph numbers share per mechanism, UPR expected 100%, lower = warning; states found (UPR records with ≥1 state vs total UPR, list those without); duplicates & gaps (distinct id == count; duplicate texts count; records with no themes/sdgs/affected_persons as "not labelled").
- Random sample: "Check 10 at random" button draws 10 cards from current filter with mulberry32 seeded, seed box default 1, "Draw again", "Draw with this seed", tally. Cards listed one line each, one open at a time (accordion). Each card: symbol linked, paragraph number, full verbatim text, themes as chips, three buttons Fits / Doesn't fit / Unsure. Line above: "This is your judgement of the UN's labels; nothing is sent anywhere." Tally: "Themes: x fit, y don't, z unsure of 10 judged" with seed.

6. Tab 04 Method & export:
- 5-6 plain sentences on how numbers computed.
- Download CSV button: visible columns + full text + labels, comment lines with country, source, build date, filters applied, row count; Blob URL.
- Copy summary: plain-text paragraph with headline numbers and ten themes.
- Data source, licence line, build date.

7. Footer: "Built on OHCHR UHRI data · n records · source link" + Credits line if shelf code used. I'm not using shelf code, but the sources consulted... The instruction says add Credits line if code/wording from Reference shelf excerpts with open licence. I'm not using any, so maybe skip, but footer spec says "plus a 'Credits' line if any shelf code was used". I didn't use shelf code. But I could add a small credits line naming the guidance sources? The rule: "If you use code or wording from a 'Reference shelf excerpts' page that has an open licence... add a small Credits line". I'm not using such code. I'll include a modest credits line anyway? Safer to include one naming the consulted guidance (UK Analysis Function etc.) — those are sources consulted, not code. I'll add a small credits line mentioning design guidance sources; harmless. Actually the footer spec says "plus a 'Credits' line if any shelf code was used" — since none used, I can omit. But the plan lists "Sources consulted". I'll add a small credits line in footer area on tab 04 listing the guidance consulted. Fine.

Design: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335. Serif Georgia for title/big numbers/figure titles; monospace uppercase letter-spaced 11-12px for labels/tabs/figure numbers; sans 16px body. Focus ring red. No horizontal scroll. [hidden]{display:none!important}.

Tabs: role="tablist", arrow-key navigation, buttons role="tab" aria-selected, panels role="tabpanel". Max 5 tabs — we have 4.

Click budget: tabs (4) + filter headings (3) + Clear all + maybe show-more + tab-internal buttons... "no view shows more than about seven things to click (tabs, filter headings and buttons together, not counting table rows)". Hmm, tab 01: 4 tabs + 3 filter headings + clear all = 8. Plus "see the States" link = 9. Hmm, "about seven" — it's approximate. The plan itself mandates these elements, so follow the plan. The plan is authoritative; "about seven" is a guideline. I'll keep it lean: on tab 01, tabs 4 + headings 3 + clear all = 8 clickable, plus states link. It's what the plan asks. Fine.

Chart.js: window.Chart preloaded. FIG.01 horizontal bar: indexAxis 'y', ranked descending (Chart.js plots first item at... with indexAxis y, first data point at top? Actually in Chart.js v4, for horizontal bar, the first category appears at the top? By default, y-axis categories go bottom-to-top? In Chart.js, category axis for horizontal bars: the first item is at the top when... hmm. In Chart.js, for indexAxis:'y', categories are drawn with the first at the top? Let me recall: In Chart.js 3/4, with indexAxis 'y', the x-axis is value (bottom), y-axis is category (left). Category labels order: by default the axis displays categories in order from bottom to top? Actually I recall that in Chart.js horizontal bar charts, the first data element appears at the top... Let me think. In Chart.js v2 with horizontalBar, first item was at top. In v3+, I believe the category axis is reversed by default for indexAxis 'y'? Hmm. Testing memory: many examples show `indexAxis: 'y'` and data [a,b,c] renders a at top. Actually I recall that in v3, they changed so that the first item is at the bottom for vertical bars (x axis left-to-right), and for horizontal bars the y axis goes... The y category axis in horizontal bar: values increase upward by default, so first category at bottom. Many people add `reverse: true`... Hmm, I genuinely recall that in Chart.js 3+, horizontal bar charts show the first item at the top by default? Let me think of the classic example: chartjs.org docs "Horizontal Bar Chart" sample: data labels ['Red','Blue',...] — the rendered image shows Red at top. Yes, I'm fairly confident the docs sample shows the first label at the top for indexAxis:'y'. Actually in v3 migration notes: "the default for horizontal bar charts changed so the first item is at the top"? There was a change: in v3, `indexAxis: 'y'` charts have the category axis reversed compared to v2? The v3 migration guide says: "In v3, the bar chart with indexAxis 'y' now draws the first category at the top" — I believe yes, v3 changed so bars read top-to-bottom like a ranked list. To be safe, I'll set `reverse: false` explicitly? If default already puts first at top, fine; if not, ranked order would be bottom-to-top which is still "ranked" but less ideal. I'll explicitly handle: set scales.y.reverse = true if needed... Risky either way. Safest: after building labels array ranked descending (largest first), set `scales: { y: { reverse: false } }`... I can't test. Alternative: avoid ambiguity by ordering labels so that whichever orientation, it looks ranked: if first-at-top is default, labels[0]=largest gives largest at top. If first-at-bottom, largest at bottom — still ranked visually (just ascending from top). Hmm.

Let me recall concretely: Chart.js v4 docs, Bar Chart with indexAxis 'y': sample code labels: ['January',...]. The image... I remember vertical bar charts have January leftmost. For horizontal, I believe January is at top in v3+ (they made it consistent reading order). Yes — v3 migration guide: "In v3, the default order of the y-axis in horizontal bar charts was changed so that the first item appears at the top." I'm fairly confident. I'll go with labels ranked descending and no reverse flag. Even if flipped, it's still ranked.

Bar click: chart onClick handler → get element at event → add theme filter.

FIG.02 stacked: labels = years from fileMin to fileMax, datasets per mechanism with stack 's', colors mapped. Legend shown. Tooltip default fine.

Data computation:

```js
const D = window.WORKSHOP_DATA.uhri;
const records = D.records;
const country = D.country;
```

Precompute per record: para number via regex `/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/` on text; states for UPR via the regexes; firstLine.

State extraction:
```js
function extractStates(text){
  const m = text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
  if(!m) return [];
  const groups = m[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
  const out = [];
  for(const g of groups){
    const inner = g.slice(1,-1).trim();
    if(inner.includes(',') || inner.length > 60){ out.push('State not found'); }
    else out.push(inner);
  }
  return out;
}
```
Wait: "A group is accepted as a State only if it has no comma and at most 60 characters; otherwise the record gets 'State not found'." So if any group fails, the record gets "State not found"? Or that group becomes "State not found"? "otherwise the record gets 'State not found'" — the record gets it. Hmm, if multiple groups and one fails... I'll mark: if any group fails the rule, the record's state list = ['State not found']? Or include valid ones plus? The plan: "One group may hold a nested name...; several groups mean several States, and the record counts once for each. A group is accepted as a State only if it has no comma and at most 60 characters; otherwise the record gets 'State not found'." I'll implement: for each group, if fails rule → push 'State not found' for that group? "the record gets" suggests record-level. Simplest consistent: if any group fails, record states = ['State not found']; else all groups. Hmm, but a record with "(Cabo Verde) (Slovenia) (Togo);" all valid → three states. A record ending "(art. 15)." — wait that's treaty body, not UPR. UPR ending with non-state parenthesis e.g. "(see para. 12)" — has no comma, ≤60 chars... would be accepted as "see para. 12" wrongly. The plan acknowledges: "A few UPR texts end with a parenthesis that is not a State... The comma-and-length rule catches most; the check panel lists the rest." OK so just implement the rule as stated. I'll do per-group: failed group → 'State not found' replaces... Let me just do: states = groups.map(g => inner).filter? No — plan says record gets "State not found". I'll implement: if any group fails, the record's state list is ['State not found']; else the list of groups. Actually maybe better: each failing group contributes 'State not found' and valid ones contribute their names? "the record gets 'State not found'" — record-level. I'll go record-level: any failure → ['State not found']. Hmm, but then a record "(Cabo Verde) (list of things, with comma)" loses Cabo Verde. Edge case; follow plan literally: record gets "State not found". Actually re-reading once more: "A group is accepted as a State only if it has no comma and at most 60 characters; otherwise the record gets 'State not found'." Yes — if a group is not accepted, the record gets "State not found". I'll implement: if any group fails → states = ['State not found'], else states = accepted groups. And "States found" check counts UPR records with at least one State found — meaning at least one state that isn't 'State not found'? "Number of UPR records with at least one State found, against the number of UPR records; the records without one are listed". I'll count records where states.length>0 && !states.includes('State not found')... or where at least one accepted state. I'll define found = states.some(s => s !== 'State not found').

Filter state:
```js
let filters = { keyword:'', mechanism:'all', body:'all', type:'all', state:'all', theme:'all', yearFrom:null, yearTo:null, sdg:'all' };
```
Year from/to: selects of distinct years present in data (sorted). Default = min and max (i.e., all). Reversed range swapped on apply.

Keyword: words = keyword.trim().toLowerCase().split(/\s+/); every word must be substring of (text + ' ' + symbol).toLowerCase().

applyFilters(): loop records, check all. Returns array of records (with precomputed fields). Also compute derived: theme counts, year counts, etc. — recompute on each filter change; fine for ~2-3k records.

Rendering: I'll re-render tab content on filter change. Keep it simple: functions renderRail(), renderOverview(), renderRecords(), renderCheck(), renderMethod(). On filter change, re-render everything (or current tab + rail). Simpler: re-render all tabs' dynamic content each time; but tab 03 sample verdicts would reset... The sample tally is reader judgement — if filters change, redraw resets verdicts; acceptable? "updated as the reader clicks" — if user changes filter after judging, sample redraws. To preserve, store verdicts keyed by record id + seed. I'll store verdicts in a map keyed by `${seed}:${recordId}` so they persist across re-renders. Good.

Also expanded rows state — keep simple, reset on re-render is fine, but maybe preserve by id set. I'll keep a Set of expanded ids.

Sorting: default date desc, body asc, para asc (numeric compare: parse "144.43" as float), then original index. Toggle date asc when clicking Date header (reverse whole order? "clicking the Date header reverses it" — reverses the sort, i.e., date asc with same tiebreaks? I'll just flip a flag that reverses the comparator result... simplest: sortDir = 'desc'|'asc', comparator uses -date or +date, tiebreaks same). Fine.

Paragraph numeric compare: parseFloat(num) — "144.43" → 144.43, "71" → 71. Records without number → treat as Infinity (sort last) or -1? "then paragraph number ascending (numeric, so 10 follows 9)" — for missing, put after? I'll use Infinity so numbered first. Hmm within same date+body. Fine.

Highlight keyword in first line and full text: wrap matches of each word in <mark>. Need HTML-escaping first. Implement esc() then highlight: for each word, replace occurrences (case-insensitive) in the escaped string — careful: escaping may alter text (& → &amp;) so word matching on escaped text could mismatch if word contains & etc. Simpler: highlight on raw text with case-insensitive regex per word, building HTML with escaped segments. Implement:

```js
function highlight(text, words){
  if(!words.length) return esc(text);
  // build regex of escaped words
  const rx = new RegExp('(' + words.map(w=>w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|') + ')','gi');
  return esc(text).replace(...)  // problem: esc changes text
}
```
Better: split raw text by the combined regex, escape each piece, wrap matched pieces in <mark>. Use text.split(rx) — with capture group, split includes the matches. Then map: if piece matches rx (case-insensitive test) → `<mark>${esc(piece)}</mark>` else esc(piece). But a word could appear as substring across... fine.

Edge: words with regex chars — escape them. Also words could be empty after trim — filter out.

First line: up to 120 chars, cut at last space before limit, plus '…'. If text shorter, whole text (no ellipsis? plan: "the first-line column may then be the whole text" — so no ellipsis if ≤120). Implement: if text.length<=120 → text; else cut = text.slice(0,120); lastSpace = cut.lastIndexOf(' '); if lastSpace>0 cut=cut.slice(0,lastSpace); return cut+'…'.

CSV export: comment lines starting with '#': country, source, source_url, built, filters applied, row count. Then header row: Date, Body, Mechanism, Type, Symbol, Doc URL, Paragraph, Recommending States, Section, Themes, SDGs, SDG targets, Affected persons, Text. Quote fields properly (escape " as ""). Blob download.

Copy summary: navigator.clipboard.writeText with fallback (textarea execCommand). Summary text: e.g. `Kenya — UN human rights recommendations and observations (UHRI, built {built}): {n} records from {docs} documents, {yearMin}–{yearMax}. Types: ... Top themes: ... (source: {source_url})`. Include current filter note.

Clipboard: "the clipboard write is the only thing that leaves the page" — use navigator.clipboard.writeText with fallback.

Checks (tab 03): compute on render:
1. Record count: records.length vs Number(D.count) → pass/fail.
2. Partitions: mechanism counts sum, body counts sum, year counts sum — each equals records.length.
3. Type partition sum.
4. Chart vs table: recompute theme counts with second loop; compare to chart data; check ten rows equal; largest ≤ filtered count. Since I generate both from same computation, the check is somewhat tautological but plan wants "recomputed by a second loop" — I'll literally run a separate function recomputeThemes() and compare.
5. Links: every record doc_url starts with 'https://docs.un.org/' and ends with symbol (case-insensitive, decodeURIComponent both). List failures.
6. Paragraph numbers: share per mechanism with number found; UPR expected 100%, lower → warning (amber/red text "warning").
7. States found: UPR records with ≥1 state vs UPR total; list records without (symbol + what the parentheses held — show the matched trailing run or 'none').
8. Duplicates/gaps: distinct id count vs records.length; duplicate text count (count of texts appearing more than once — number of duplicate values or extra records? "the number of duplicate text values" — I'll count records whose text appears more than once, or number of duplicated values; I'll show "x texts appear more than once (y extra records)"); records with no themes / no sdgs / no affected_persons counts labelled "not labelled".

Each check line: "what was compared — value A vs value B — ✓ pass" or red "check failed".

Random sample: mulberry32:
```js
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
```
Draw 10: seeded shuffle of filtered records indices, take 10 (or fewer if filtered <10 — handle: draw min(10, n)). Seed input default 1. "Draw again" = new random seed (Math.floor(Math.random()*1e9)) put in box and draw. "Draw with this seed" = use box value. Cards: one line each (button) expanding one at a time (accordion). Card content: symbol link, para number, full text verbatim, themes chips, three verdict buttons. Verdict stored in map key `${seed}|${id}`. Tally line: "Themes: x fit, y don't, z unsure of 10 judged · seed 1". Note line: "This is your judgement of the UN's labels; nothing is sent anywhere."

Tab 04 method: 5-6 sentences. Export buttons. Source/licence/build.

Header source line: `source` linked to `source_url`, n records (Number(count) vs records.length — show records.length), n documents, first–last year, built, "dated by document".

Rail: FILTERS + Clear all button; big number filtered count aria-live polite + "of N in the file"; red share bar (width %); chips container. Accordions: three sections with buttons aria-expanded, one open at a time (opening one closes others). On tabs 03/04 hide the accordion wrapper (keep number/bar/chips). Implement via body class or hidden attribute on the accordion container when activeTab is 3 or 4.

Accordion contents:
- 01 KEYWORD: input + hint "literal match, not synonyms" (monospace small). Debounce 300ms.
- 02 MECHANISM, BODY, TYPE: three selects (Mechanism, Body, Type) + State select. Body options depend on chosen mechanism (values present in that mechanism within... whole file or filtered? "Body or mandate (body values present in the chosen mechanism, each with its count)" — counts within chosen mechanism, from full file I think; but if other filters active, counts could be of filtered... simpler: counts within mechanism in the full file. Hmm, but rail number reflects all filters. I'll compute body counts within mechanism from the full file (stable), and note. Actually to be consistent, compute from records filtered by all filters except body? That's nicer but more complex. Keep simple: counts from full file within chosen mechanism. The plan says "body values present in the chosen mechanism, each with its count" — ambiguous; full-file counts fine. Actually, let me compute counts from the set filtered by everything except body — that's more useful and still simple since I compute filtered set anyway... but filtered set depends on body filter. I'll compute "partial" set ignoring body filter for the body select counts. Similarly type select counts from set ignoring type filter. Mechanism select lists all mechanisms in file. State select lists all states found in UPR records (full file) with counts. That's reasonable.

Hmm wait, click budget: heading 02 contains 4 selects — selects aren't "things to click" in the same sense? The budget counts "tabs, filter headings and buttons together". Selects are dropdowns... I'll not over-worry; plan mandates them.

- 03 YEARS AND SDG: Year from select, Year to select (distinct years in file), SDG select (goals present in data with names from sdg_names). SDG options: for each goal number present in any record's sdgs, label `${g}: ${sdg_names[String(g)] || ''}`. sdg_names keys are strings.

Chips: for each active filter (keyword, mechanism≠all, body≠all, type≠all, state≠all, theme≠all, yearFrom≠min or yearTo≠max, sdg≠all) show chip with label + × button. Clear all resets.

Theme filter: added by clicking FIG.01 bar. Chip "Theme: X". Only one theme at a time (theme:'all' or value) — clicking another bar replaces. Fine.

State filter: record matches if its extracted states include the selected state.

Now the "see the States" link in UPR tile on tab 01: toggles an in-place list "Ten States that made most recommendations to {country}" with counts for current filter (count of filtered UPR records where states include that state). Ranked top 10.

Layout: header full width; below, a grid: rail ~260px + main. Tabs row under header (always visible). Footer fixed? Just at bottom, always visible — put footer at end of page; "always visible" loosely — I'll make it position sticky bottom? Simpler: normal footer at bottom; but "always visible, one line" — I'll make it sticky bottom with background. That's nice: `position:sticky; bottom:0`. OK.

Tabs: role=tablist with 4 buttons: "01 OVERVIEW", "02 RECORDS", "03 CHECK", "04 METHOD & EXPORT". Arrow key navigation: left/right moves focus & activates (I'll activate on arrow per common pattern, or just move focus and require Enter? Plan says arrow-key navigation — I'll implement roving tabindex with activation on arrow). Panels: role=tabpanel, hidden when inactive.

Charts: create on render of tab 01; must destroy previous chart instances when re-rendering (Chart.getChart(canvas)?.destroy()). Since re-render replaces DOM, old canvas gone; but Chart keeps registry — call destroy on old chart before removing. I'll keep references and destroy.

FIG.01 click → add theme filter: chart options onClick: (evt, elements) => { if(elements.length){ const i = elements[0].index; const theme = chart.data.labels[i]; setFilter('theme', theme); } }.

Chart styling: no gridlines clutter — keep light ticks; bar color rgba(155,35,53,0.8); value at end of bar: use a plugin to draw datalabels? Chart.js without datalabels plugin can't show values at bar end easily. I can write a small inline plugin that draws the value text after each bar using ctx.fillText. That's allowed (inline plugin). Implement:

```js
const valueLabels = {
  id:'valueLabels',
  afterDatasetsDraw(chart){
    const {ctx} = chart;
    const meta = chart.getDatasetMeta(0);
    ctx.save();
    ctx.font = '12px ui-monospace, Menlo, Consolas, monospace';
    ctx.fillStyle = '#1d1b18';
    meta.data.forEach((bar, i)=>{
      const v = chart.data.datasets[0].data[i];
      const x = bar.x + 6; // bar.x is the end (right edge) for horizontal bars
      const y = bar.y;
      ctx.textBaseline='middle';
      ctx.fillText(String(v), x, y);
    });
    ctx.restore();
  }
};
```
For horizontal bar, bar.x is the right edge (value end). Good. Need padding on x max so labels fit: set suggestedMax or compute max*1.12.

FIG.02 stacked: datasets per mechanism, colors map:
```js
const MEC_COLORS = {'Universal Periodic Review':'#c2410c','Treaty bodies':'#0f766e','Special Procedures':'#7c3aed'};
```
fallback '#6b6459'. Legend display true, labels use dataset labels. Stacked: scales x stacked true, y stacked true.

Empty filter: chart area shows "No records match" text — if filtered.length===0, skip chart and show a div with that text.

Table rendering: build rows; 50 at a time; "Show 50 more" button below. Row = <tr> clickable (tabindex=0, role="button"? Better: make the row a button-like: I'll add tabindex="0" and keydown Enter/Space toggles). Expanded row: a following <tr class="detail"> with colspan. Use <tbody> per record? Simpler: each record renders two <tr>s (main + detail hidden). Detail content built when expanded.

Columns: Date | Body | Symbol | Para. | First line | Recommending State. Symbol cell: <a href=doc_url target=_blank rel=noopener>symbol</a>. Para: number or '—'. State: joined states or '—' (dash for non-UPR; 'State not found' shown as such for UPR failures).

Caption: "Showing X of Y matching records · newest first" (or oldest first when reversed). Also "No records match" case.

Search field on tab 02 top: input synced with filters.keyword (on input, debounce, update rail input too).

Copy citation: button in expanded row; copies `symbol, para. N` or symbol; label includes "(no paragraph number in this extract)" when none. Show "Copied" for 2s (change button text or a span).

Open the UN document: link in expanded row.

Labels in expanded row: themes as chips (small bordered spans), sdgs as "SDG 16: Peace, justice..." list, sdg_targets list, affected_persons list, section when present. Missing → show "not labelled" for that category? Plan: "missing labels shown as missing" — I'll show "—" or "not labelled" text. I'll show e.g. "Themes: not labelled" when empty.

Now the checks panel details:

- Links check: `doc_url` starts with "https://docs.un.org/" and ends with symbol case-insensitively after decoding: 
```js
const ok = r.doc_url.startsWith('https://docs.un.org/') && decodeURIComponent(r.doc_url).toLowerCase().endsWith(encodeURIComponent? ...)
```
"ends with its symbol (compared case-insensitively after decoding)" — decode both: `decodeURIComponent(r.doc_url).toLowerCase().endsWith(r.symbol.toLowerCase())`. decodeURIComponent may throw on malformed — wrap try/catch. List failures (symbol + doc_url), cap list at like 10 with "and x more".

- Paragraph share per mechanism: count with para found / count per mechanism. UPR expected 100%; if <100% show warning (not error). Others informational.

- States found: UPR records with ≥1 accepted state vs UPR total; list those without: symbol + trailing parenthesis run (or "no trailing parentheses").

- Duplicates: distinct ids vs length; duplicate texts: group by text, count values with >1; "not labelled" counts: no themes, no sdgs, no affected_persons.

Check line format: monospace-ish small text with ✓ (pass) in normal ink or red "CHECK FAILED". Warning in red? Plan: "a pass mark or a red 'check failed' with the values, never a hidden failure" and UPR para lower → "shown as a warning, not an error". I'll use "✓" for pass, "⚠" warning (maybe styled red), "✗ CHECK FAILED" red for fail.

Random sample cards: "listed as one line each, one open at a time" — accordion of 10 buttons, each showing "symbol · para N" line; expanded shows full card. Verdict buttons inside. Tally above/below.

Seed handling: state sampleSeed (default 1), sampleDrawn (array of record ids) — recompute when draw clicked or filter changes? "draws the cards" from current filter. If filter changes after drawing, cards stale — I'll redraw automatically on filter change if a sample was drawn (keeping seed). Simpler: sample is drawn from current filtered set at draw time; on filter change, if sample exists, redraw with same seed. I'll do that.

Verdicts map keyed seed|id persists.

Tally: count verdicts among the 10 drawn.

Now method tab text (5-6 sentences):
1. Every number on this page is a loop over the records in the attached UHRI file in your browser; nothing is estimated and no outside service is called.
2. The headline count is records.length; documents are distinct symbol values; years are the min and max of year.
3. Filters combine with AND: keyword words must each appear in the text or symbol (literal substring), mechanism/body/type match exactly, years are inclusive, SDG matches when the goal number is in the record's sdgs list, theme and State match the labels extracted as described.
4. Paragraph numbers come from the first number at the start of the text; UPR recommending States come from the trailing parentheses of UPR records only.
5. Theme counts count each theme once per record, so they add up to more than the record count.
6. The CSV export contains the filtered records with the same columns you see, generated in the browser.

Export CSV columns: Date, Body, Mechanism, Type, Symbol, Document URL, Paragraph, Recommending State(s), Section, Themes, SDGs, SDG targets, Affected persons, Text.

Comment lines: `# Country: Kenya`, `# Source: ... (url)`, `# Built: ...`, `# Filters: keyword=..., mechanism=..., ...`, `# Rows: n`.

Copy summary text:
```
{country}: {n} UN recommendations and observations ({types breakdown}) from {docs} documents, {ymin}–{ymax}, dated by document. Top themes: 1) X (a), 2) ... Source: OHCHR UHRI ({source_url}), built {built}. Filters: ...
```

Footer: `Built on OHCHR UHRI data · {n} records · <a>source</a>` small monospace, sticky bottom.

Header label: `UHRI · {country}` monospace.

Title: "UN human rights recommendations and observations: {country}" serif large.

Sub-line: source linked, n records, n documents, first–last year, built, "dated by document".

Now sizes: file under 1500 lines. This will be a big file, maybe 900-1200 lines. OK.

Let me now think about structure of the JS:

```js
const D = window.WORKSHOP_DATA.uhri;
const RECS = D.records.map((r,i)=>{
  const para = (r.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/)||[])[1] || null;
  const states = r.mechanism==='Universal Periodic Review' ? extractStates(r.text) : [];
  return {...r, _i:i, _para:para, _states:states, _first:firstLine(r.text)};
});
```

Wait — spread {...r} copies; fine.

State extraction regex on text: `/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/`. Note texts end with ";" sometimes: "(Cabo Verde) (Slovenia) (Togo);" — the regex allows trailing [;.]? after the run. Good.

Filters object + helpers:

```js
const state = {
  tab: 0,
  filters: {keyword:'', mechanism:'all', body:'all', type:'all', state:'all', theme:'all', yf: null, yt: null, sdg:'all'},
  sortAsc: false,
  shown: 50,
  expanded: new Set(),
  openAcc: null, // which rail accordion open: 'kw'|'mech'|'yr'|null
  sampleSeed: 1,
  sampleIds: null,
  verdicts: {}, // key seed|id -> 'fit'|'no'|'unsure'
  sampleOpen: null,
};
```

years list: distinct years sorted asc. yf/yt default = first/last.

filtered(): 
```js
function filtered(){
  const f = state.filters;
  const words = f.keyword.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const yf = Math.min(f.yf ?? years[0], f.yt ?? years[years.length-1]);
  const yt = Math.max(...);
  return RECS.filter(r=>{
    if(f.mechanism!=='all' && r.mechanism!==f.mechanism) return false;
    if(f.body!=='all' && r.body!==f.body) return false;
    if(f.type!=='all' && r.type!==f.type) return false;
    if(f.state!=='all' && !r._states.includes(f.state)) return false;
    if(f.theme!=='all' && !(r.themes||[]).includes(f.theme)) return false;
    if(f.sdg!=='all' && !(r.sdgs||[]).includes(Number(f.sdg))) return false;
    if(r.year < yf || r.year > yt) return false;
    if(words.length){
      const hay = (r.text+' '+r.symbol).toLowerCase();
      if(!words.every(w=>hay.includes(w))) return false;
    }
    return true;
  });
}
```

Note: year filter — if user picks from>to, swap (plan: "the from/to selects reject a reversed range by swapping it"). I'll swap at apply time.

Rendering approach: I'll write render() that updates rail + current tab. On filter change: recompute, render rail, render active tab (and charts if tab 0). Keep other tabs rendered lazily when opened (render on tab switch). Simplest: render all four tab bodies on each change? Tab 03 checks are cheap; tab 02 table with 50 rows fine. But charts need canvas present — if tab 01 hidden, canvas has zero size; Chart.js may misrender. So render charts only when tab 0 active; on switching to tab 0, (re)build charts. I'll do: renderAll() renders rail + all tabs' static content, but charts built in renderOverview() only if tab===0; when switching to tab 0 call renderOverview() again. Manage chart instances: keep `let chart1, chart2;` destroy before rebuild.

Simpler robust approach: on any state change, call `render()` which:
- renders rail (number, bar, chips, accordion contents)
- renders tab panels: for each tab, call its renderer; renderers for tab 0 include charts only if state.tab===0 else mark charts pending; when tab switches to 0, call renderOverview().

I'll just call renderTab(i) for active tab only, and on tab switch call renderTab(new). Rail always re-rendered. Tab 02's "shown" resets to 50 on filter change (keep shown as is? reset to 50 on filter change is fine).

Debounce keyword: both inputs (rail + tab02 search) — I'll have one input in rail; on tab 02 also an input at top. Both call setKeyword with debounce; sync values.

Accordion behavior: clicking a heading button toggles; opening one closes others (state.openAcc). aria-expanded accordingly.

Chips: render list; each chip button "×" removes that filter (reset to default). Chip labels: `Keyword: "torture"`, `Mechanism: UPR`, `Body: CEDAW`, `Type: Recommendations`, `State: France`, `Theme: Reservations`, `Years: 2010–2020`, `SDG: 16`.

Clear all: reset filters to defaults, keyword inputs cleared, re-render.

Now tab 01 details:

Tiles row: 
- Tile 1: big number = filtered.length, sub: "of N records in the file · dated by document"? The header already says dated by document. Sub-line: breakdown per type: "Recommendations 1,791 · Concerns/Observations 471 · Other 2" computed from filtered set. Plus "How this is computed" note: "Count of records in the current filter; every type included."
- Tile 2: documents = distinct symbols in filtered; note "Distinct symbol values among the filtered records."
- Tile 3: years = min–max year of filtered; note.
- Mechanism tiles: for each mechanism value present in file (or in filtered? "one tile per mechanism" — I'll show all mechanisms present in the file, with 0 if filtered excludes; share of filtered set = mechCount/filtered.length). Each tile: mechanism name, big-ish number records, "x documents · latest year Y · z% of filtered". UPR tile gets "see the States" link (button) toggling states list. Note per tile: "Records with mechanism = X in the current filter."

Hmm click budget on tab 01: 4 tabs + 3 accordion headings + clear all + states link = 9. "about seven" — the plan mandates all these; I'll keep. Maybe put "see the States" inside UPR tile as small link — still a click. It's per plan; fine.

FIG.01: title "FIG.01 · Ten most frequent themes among {n} filtered records" serif; source line "Source: UHRI records, current filter · a record can carry several themes, so counts add up to more than {n}". Chart canvas + table below (Theme | Records | % of filtered | Years). Table rows clickable? Plan says clicking a bar adds filter; table rows not necessarily clickable. Keep table static. Note under chart about multi-theme.

Bar click adds theme chip → setFilter('theme', theme).

FIG.02: "FIG.02 · Records per year by mechanism · {n} filtered records" stacked bars, years fileMin..fileMax, legend. Source line.

Tab 02: search input top ("Search {n} records, e.g. torture" placeholder), table, show more.

Table header: Date (button to toggle sort, with arrow indicator), Body, Symbol, Para., First line, Recommending State. Caption: `Showing {shown} of {matching} matching records · newest first` (or "oldest first"). If 0: "No records match the current filters."

Row: date (YYYY-MM-DD), body, symbol link, para or '—', first line (highlighted), states joined ' · ' or '—' for non-UPR; UPR with no states → 'State not found'.

Expanded detail row: 
```
<tr class="detail"><td colspan=6>
  <div class="para-num">para. 144.43</div> (red serif big) or "no paragraph number in this extract"
  <p class="fulltext">highlighted full text</p>
  labels block: Section (if present), Themes chips, SDGs (with names), SDG targets, Affected persons
  buttons: Copy citation | Open the UN document (link)
</td></tr>
```

Copy citation: text = para ? `${symbol}, para. ${para}` : symbol; button label: para ? 'Copy citation' : 'Copy citation (no paragraph number in this extract)'. On click → clipboard → show "Copied ✓" 2s.

Tab 03: 
- Panel "HOW THE APP CHECKS ITSELF" heading + list of check lines (each a div). 
- Sample section: heading "RANDOM-SAMPLE LABEL CHECK", line "This is your judgement of the UN's labels; nothing is sent anywhere." Controls: button "Check 10 at random", seed input (number, default 1), button "Draw with this seed", button "Draw again" (new random seed). Tally line: "Themes: x fit · y don't fit · z unsure · of 10 judged · seed N". Cards list: 10 accordion buttons "symbol · para N" — one open at a time; open card shows full text, themes chips, verdict buttons (Fits / Doesn't fit / Unsure) with active state.

If filtered < 10: draw all, note "only n records match".

Tab 04:
- "HOW EACH NUMBER IS COMPUTED" — 6 sentences list.
- Export: button "Download CSV of the current filter" → builds CSV with comments; button "Copy summary".
- Source block: source text + link, licence line ("OHCHR Universal Human Rights Index — see source page for terms of use"? I shouldn't invent licence. The data description doesn't give a licence. Plan says "The data source, licence line and build date." Hmm — I don't know the licence. UHRI is OHCHR; I shouldn't invent. I'll write "Licence: see the source page (OHCHR UHRI terms of use)" — that's safe-ish, pointing to source rather than inventing. Or "Terms of use: as stated on the source page." I'll phrase: "Licence / terms of use: as stated on the source page linked above." That avoids inventing.
- built date.

Footer sticky: `Built on OHCHR UHRI data · {n} records · <a href=source_url>source</a>` + credits line: "Design guidance: UK Government Analysis Function (data visualisation: charts, tables); citation practice: Dag Hammarskjöld Library Ask DAG; OHCHR HRBA guidance note." — these are the sources consulted; fine as a credits line. The system prompt says credits line only if shelf code used; adding a sources line is harmless and matches plan's footer spec ("plus a 'Credits' line if any shelf code was used" — none used, but plan's tab 04 asks for source/licence/build). I'll include a small credits line in footer anyway naming guidance — it's informative, not code. OK.

Now, careful with details:

- Number formatting: thousands separators via toLocaleString('en-US')? Use `n.toLocaleString('en-GB')` — gives commas. Fine.
- Percent: one decimal: `(100*c/n).toFixed(1)`.
- Theme year range: min–max year of filtered records carrying theme.
- Ties alphabetical: sort by count desc, then localeCompare.

- Sorting records table: 
```js
const sorted = [...matching].sort((a,b)=>{
  const d = state.sortAsc ? a.date.localeCompare(b.date) : b.date.localeCompare(a.date);
  if(d) return d;
  const b2 = a.body.localeCompare(b.body); if(b2) return b2;
  const pa = a._para?parseFloat(a._para):Infinity, pb = b._para?parseFloat(b._para):Infinity;
  if(pa!==pb) return pa-pb;
  return a._i-b._i;
});
```
"clicking the Date header reverses it" — toggles sortAsc.

- Highlight function:
```js
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function hi(text){
  const words = state.filters.keyword.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if(!words.length) return esc(text);
  const rx = new RegExp('('+words.map(w=>w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')','gi');
  return text.split(rx).map(p=> rx.test(p) ? '<mark>'+esc(p)+'</mark>' : esc(p)).join('');
}
```
Careful: rx.test with 'g' flag has lastIndex statefulness — since split consumes... Using the same regex object for test after split: split resets? Safer: create fresh regex for test or use p.toLowerCase().includes check per word: `words.some(w=>p.toLowerCase().includes(w))`. Simpler and safe. Do that.

- CSV:
```js
function csvCell(v){ v=String(v==null?'':v); return '"'+v.replace(/"/g,'""')+'"'; }
```
Comment lines start with '#'. Build array of lines. Blob type 'text/csv;charset=utf-8'. a.download = `uhri-${country}-recommendations.csv`. Click, revoke.

- Copy summary: navigator.clipboard?.writeText fallback to textarea+execCommand('copy'). Show "Copied" feedback on button.

- Clipboard for citation same helper.

- mulberry32 as above. Draw:
```js
function drawSample(){
  const arr = filtered();
  const rnd = mulberry32(state.sampleSeed>>>0);
  const idx = arr.map((_,i)=>i);
  for(let i=idx.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[idx[i],idx[j]]=[idx[j],idx[i]];}
  state.sampleIds = idx.slice(0, Math.min(10, idx.length)).map(i=>arr[i].id);
  state.sampleOpen = null;
  render();
}
```
"Check 10 at random" button: sets seed to... default 1? Plan: seed box default 1; "Check 10 at random" draws the cards (with current seed? then "Draw again" and "Draw with this seed"). I'll make "Check 10 at random" draw with the seed currently in the box (default 1) — first click draws seed 1. "Draw again" = random new seed, update box, draw. "Draw with this seed" = use box value. Good.

- Verdict buttons: set state.verdicts[`${seed}|${id}`]=v; re-render tally + card button states. I'll re-render tab 03 only (renderTab(2)) but keep sampleIds. Since render() re-renders active tab, and verdict click happens on tab 03, call renderTab(2) after updating — but render() also re-renders rail; fine, call render() but that resets shown rows etc. — acceptable? shown reset only on filter change; I'll keep shown persistent across renders (don't reset in render). OK: render() doesn't reset shown; only filter changes reset shown=50.

Let me structure:

```js
function setFilter(key, value){ state.filters[key]=value; if(key==='keyword'){} state.shown=50; render(); }
function render(){ renderRail(); renderTabs(); }
function renderTabs(){ renderTab(state.tab); }
function renderTab(i){ if(i===0) renderOverview(); else if(i===1) renderRecords(); else if(i===2) renderChecks(); else renderMethod(); }
function switchTab(i){ state.tab=i; update tab buttons/panels hidden; renderRail(); renderTab(i); }
```

Rail accordion visibility: on tabs 2,3 (03 CHECK, 04 METHOD) hide accordions: in renderRail, `accWrap.hidden = (state.tab>=2)`.

Charts: in renderOverview, destroy existing, build if filtered.length>0 else show "No records match".

Chart.js config FIG.01:
```js
chart1 = new Chart(ctx1, {
  type:'bar',
  data:{labels: top10.map(t=>t.theme), datasets:[{data: top10.map(t=>t.count), backgroundColor:'rgba(155,35,53,0.8)', borderWidth:0, barPercentage:0.75}]},
  options:{
    indexAxis:'y',
    responsive:true, maintainAspectRatio:false,
    onClick:(e,els)=>{ if(els.length){ const t=top10[els[0].index].theme; setFilter('theme', t); } },
    scales:{
      x:{ beginAtZero:true, suggestedMax: max*1.15, grid:{color:'#e5ded0'}, ticks:{font:{family:'ui-monospace, Menlo, Consolas, monospace', size:11}, color:'#1d1b18'}, border:{color:'#d9d2c3'} },
      y:{ grid:{display:false}, ticks:{font:{size:13, family:'sans-serif'}, color:'#1d1b18'}, border:{color:'#d9d2c3'} }
    },
    plugins:{ legend:{display:false}, tooltip:{callbacks:{label:(c)=>` ${c.parsed.x} records`}} }
  },
  plugins:[valueLabelsPlugin]
});
```
Canvas container height ~ 320px.

FIG.02:
```js
const yearsAll = range(fileMin, fileMax);
const mechs = distinct mechanisms in file (order: as encountered or fixed order ['Universal Periodic Review','Treaty bodies','Special Procedures'] filtered to present).
datasets = mechs.map(m=>({label:m, data: yearsAll.map(y=> count of filtered with year y and mechanism m), backgroundColor: MEC_COLORS[m]||'#6b6459', stack:'s'}));
options: scales x stacked, y stacked beginAtZero, ticks int (stepSize 1? counts may be large; use precision:0).
```

Legend: display true, position 'bottom', labels usePointStyle maybe. Fine.

Now checks implementation:

```js
function runChecks(){
  const checks = [];
  const n = RECS.length;
  // 1 record count
  checks.push({name:'Record count', detail:`records.length = ${n} vs Number(count) = ${Number(D.count)}`, pass: n===Number(D.count)});
  // 2 partitions
  const sum = obj => Object.values(obj).reduce((a,b)=>a+b,0);
  const byMech = countBy(RECS, r=>r.mechanism);
  const byBody = countBy(RECS, r=>r.body);
  const byYear = countBy(RECS, r=>r.year);
  checks.push({name:'Partitions: mechanism, body, year', detail:`sums ${sum(byMech)}, ${sum(byBody)}, ${sum(byYear)} vs ${n}`, pass: sum(byMech)===n && sum(byBody)===n && sum(byYear)===n});
  const byType = countBy(RECS, r=>r.type);
  checks.push({name:'Type partition', detail:`sum ${sum(byType)} vs ${n}`, pass: sum(byType)===n});
  // 4 chart vs table — recompute themes second loop
  const f = filtered();
  const themesA = themeCounts(f); // used by chart
  const themesB = {}; for(const r of f){ for(const t of (r.themes||[])) themesB[t]=(themesB[t]||0)+1; }
  const same = JSON.stringify(Object.entries(themesA).sort())===JSON.stringify(Object.entries(themesB).sort());
  const top = topThemes(f,10);
  const largestOk = top.length===0 || top[0].count <= f.length;
  checks.push({name:'Chart against table', detail:`FIG.01 bars recomputed by a second loop: ${same?'identical':'DIFFER'}; ten table rows same values; largest bar ${top[0]?top[0].count:'–'} ≤ ${f.length} filtered: ${largestOk}`, pass: same && largestOk});
  // 5 links
  const bad = RECS.filter(r=>{ try{ const u=decodeURIComponent(r.doc_url).toLowerCase(); return !(r.doc_url.startsWith('https://docs.un.org/') && u.endsWith(r.symbol.toLowerCase())); }catch(e){ return true; } });
  checks.push({name:'Links', detail:`${RECS.length-bad.length} of ${RECS.length} doc_url values start with https://docs.un.org/ and end with the symbol`, pass: bad.length===0, list: bad.slice(0,10).map(r=>`${r.symbol} → ${r.doc_url}`), more: bad.length-10});
  // 6 paragraph numbers per mechanism
  const paraByMech = {}; for(const r of RECS){ const m=r.mechanism; paraByMech[m]=paraByMech[m]||{tot:0,found:0}; paraByMech[m].tot++; if(r._para) paraByMech[m].found++; }
  const upr = paraByMech['Universal Periodic Review'];
  const uprOk = upr && upr.found===upr.tot;
  checks.push({name:'Paragraph numbers', detail: Object.entries(paraByMech).map(([m,v])=>`${m}: ${v.found}/${v.tot} (${pct})`).join(' · ') + (uprOk?'':' — UPR below 100%: warning'), pass:true, warn: !uprOk});
  // 7 states
  const uprRecs = RECS.filter(r=>r.mechanism==='Universal Periodic Review');
  const withState = uprRecs.filter(r=>r._states.some(s=>s!=='State not found'));
  const noState = uprRecs.filter(r=>!r._states.some(s=>s!=='State not found'));
  checks.push({name:'Recommending States found', detail:`${withState.length} of ${uprRecs.length} UPR records have at least one State`, pass: noState.length===0, list: noState.slice(0,10).map(r=>`${r.symbol} — trailing text: ${tail(r.text)}`), more:...});
  // 8 duplicates & gaps
  const ids = new Set(RECS.map(r=>r.id));
  const textCounts = countBy(RECS, r=>r.text);
  const dupTexts = Object.values(textCounts).filter(c=>c>1).length;
  const noThemes = RECS.filter(r=>!(r.themes||[]).length).length;
  const noSdgs = RECS.filter(r=>!(r.sdgs||[]).length).length;
  const noPers = RECS.filter(r=>!(r.affected_persons||[]).length).length;
  checks.push({name:'Duplicates and gaps', detail:`distinct id ${ids.size} vs ${n}; duplicate text values ${dupTexts}; not labelled — themes ${noThemes}, sdgs ${noSdgs}, affected persons ${noPers}`, pass: ids.size===n});
  return checks;
}
```

tail(r.text): last 80 chars.

Render check lines: `<div class="check"><span class="mark">✓</span> name — detail</div>`; fail: red "✗ CHECK FAILED"; warn: "⚠ warning".

Sample cards: for each id in sampleIds, find record (map id→rec). Card button line: `${symbol} · para ${para||'—'}`. Open card: full text (esc, no highlight needed — or highlight keyword? keep plain esc), themes chips, verdict buttons. Verdict buttons show active state (aria-pressed).

Tally: count verdicts for current sampleIds: fit/don't/unsure.

Now HTML skeleton:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UHRI · {country} — UN recommendations dashboard</title>
<style>...</style>
</head>
<body>
<header>
  <div class="kicker" id="kicker">UHRI · KENYA</div>
  <h1 id="title"></h1>
  <p class="meta" id="meta"></p>
</header>
<nav class="tabs" role="tablist" aria-label="Sections">
  <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 OVERVIEW</button>
  ...
</nav>
<div class="layout">
  <aside class="rail" id="rail">...</aside>
  <main>
    <section role="tabpanel" id="panel-0" aria-labelledby="tab-0"></section>
    ...
  </main>
</div>
<footer id="footer"></footer>
<script>...</script>
</body>
</html>
```

Title set via JS with country (never hard-code). Since it's one file, I can also just leave placeholders filled by JS.

CSS: paper bg, ink, rules; layout grid: `grid-template-columns: 280px 1fr; gap: 2rem;` max-width 1200px margin auto; padding. Rail sticky top? `position:sticky; top:1rem; align-self:start;`. Tabs: monospace uppercase letter-spacing, border-bottom rule, active red with red underline. Focus ring: `:focus-visible{outline:3px solid #9b2335; outline-offset:2px}`.

Big numbers: `.big{font-family:Georgia,serif; font-size:48px;}`.

mark: background rgba(155,35,53,.25)? Use `background:#f3d9a4`? Keep accent: `mark{background:rgba(155,35,53,.22); color:inherit; padding:0 1px;}`.

Chips: small monospace bordered pills with × button.

Accordion: heading buttons full-width with number + label + chevron (aria-expanded). Content div hidden when closed.

Tables: full width, th monospace small uppercase, td sans 15-16px, numbers right-aligned (Records, % columns), caption monospace small, borders bottom thin.

Buttons: quiet — monospace uppercase small, border 1px #d9d2c3, background transparent, hover border ink. Primary (export) maybe red border.

Detail row: background slightly different (#efe9dd?) with left red border? "thin rules instead of boxes" — use a top/bottom rule and red paragraph number. OK.

Now write the code. I must be careful about length but completeness matters more. Let me draft the full file.

Also remember: before code block, at most three short sentences; after, nothing.

Let me also handle: `sdg_names` — `D.sdg_names` maps string goal → name. SDG select options: goals present = distinct sdgs values across RECS (numbers). Label: `${g} — ${D.sdg_names[String(g)]||'SDG '+g}`.

Body select: when mechanism changes, reset body to 'all' (since body list depends on mechanism). Body options: distinct body values among RECS with mechanism===selected (or all if 'all'), with counts (from full file). Type options: distinct type values in file with counts. State options: distinct states across UPR records (excluding 'State not found'? include it? The select lists "every State found" — I'll exclude 'State not found' from the select but the check lists records with it). Counts from full file.

Year selects: distinct years sorted; default from=years[0], to=years[last]. On change, if from>to swap (set both selects accordingly).

Keyword inputs: rail input id kw1, tab02 input id kw2; sync.

Debounce: 
```js
let kwTimer;
function onKw(v){ clearTimeout(kwTimer); kwTimer=setTimeout(()=>{ state.filters.keyword=v; state.shown=50; render(); },300); }
```
And sync the other input's value without triggering.

Chips removal: setFilter(key, default).

Theme chip from chart click: setFilter('theme', theme).

"see the States" toggle: state.showStates bool; renders list under UPR tile (or under tiles row). Compute top 10 states among filtered UPR records: count records per state (a record counts once per state). Title: `Ten States that made most recommendations to ${country}` — with counts for current filter. Toggle link text "see the States"/"hide".

Now the overview tiles: "A row of big serif numbers. The first tile counts all records..." then "Beside it: documents and years". Then "Below, one tile per mechanism". Layout: `.tiles{display:flex; flex-wrap:wrap; gap:2.5rem}` each tile min-width. Mechanism tiles below in own row.

Type breakdown line under first tile: entries of byType of filtered: `${type}: ${count}` joined ' · '.

How-this-is-computed notes: small monospace under each tile/figure: e.g. "How this is computed: count of records in the current filter, all types included."

FIG titles: serif ~22px: "FIG.01 · Ten most frequent themes among 2,264 filtered records". Source line under: monospace 11px: "Source: UHRI records (current filter) · themes counted once per record, so counts exceed n".

Table under FIG.01: caption "FIG.01 data — same ten rows as the chart". Columns Theme | Records | % of filtered | Years. Records right-aligned.

FIG.02 title: "FIG.02 · Records per year by mechanism · 2,264 filtered records". Source line: "Source: UHRI records (current filter) · every year from {min} to {max} shown, empty years are gaps · dated by document".

Records tab: search input full width top with hint. Table. Show more button.

Method tab content as planned.

Footer: sticky bottom, monospace 11px, border-top rule, bg paper: `Built on OHCHR UHRI data · 2,264 records · <a>OHCHR Universal Human Rights Index</a>` plus credits span: ` · Credits: chart/table practice after UK Government Analysis Function; citation form after Dag Hammarskjöld Library Ask DAG`.

Hmm the footer spec: "Built on OHCHR UHRI data · n records · source link", plus Credits line if shelf code used. I'll include the credits as part of footer second line or same line. Keep one line + small credits line. "one line, small monospace" — I'll do one line with source link, and a second tiny line for credits. Acceptable.

Edge: `D.count` string → Number(D.count). Header shows `n records` = RECS.length (and check compares). Header line: `{source linked} · {n} records · {docs} documents · {ymin}–{ymax} · built {built} · dated by document`.

Now, potential pitfall: Chart.js preloaded as window.Chart — use `new Chart(...)`. Guard `if(window.Chart)`.

Canvas heights: wrap in div with fixed height (e.g., 340px for FIG.01 with 10 bars; FIG.02 height 300px). maintainAspectRatio:false.

Value label plugin: ensure it doesn't overflow — suggestedMax max*1.15.

Also FIG.01 click: after setFilter, render() re-renders overview — chart destroyed and rebuilt. Good.

One more: "Clicking a bar adds that theme as a filter chip" — chip appears in rail. Good.

Table row keyboard: tr tabindex=0, role? I'll add `role="button"` maybe not on tr... Use keydown Enter/Space → toggle. aria-expanded on tr is odd but allowed? I'll set aria-expanded attribute on the tr. Fine.

Show 50 more: button below table; hidden when shown>=matching.

Now write everything. I'll aim for clean, complete code.

Let me write the CSS carefully:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--rule);text-underline-offset:2px}
a:hover{text-decoration-color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header{padding:28px 0 10px}
.kicker{font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--red)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:34px;line-height:1.15;margin:10px 0 8px;max-width:60ch}
.meta{font:12px/1.6 ui-monospace,Menlo,Consolas,monospace;color:#57534a;margin:0}
.meta a{color:inherit}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin-top:14px;flex-wrap:wrap}
.tabs [role=tab]{font:12px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;background:none;border:none;border-bottom:3px solid transparent;padding:12px 14px 10px;cursor:pointer;color:#57534a}
.tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.layout{display:grid;grid-template-columns:270px minmax(0,1fr);gap:36px;align-items:start;padding:22px 0 60px}
.rail{position:sticky;top:16px}
...
```

Rail:
```css
.rail h2 / .railhead{display:flex;justify-content:space-between;align-items:baseline;font:11px ...;letter-spacing:.14em;color:#57534a}
#clearAll{...small button}
.matchnum{font-family:Georgia,serif;font-size:52px;line-height:1;margin:10px 0 2px}
.matchsub{font:11px monospace;color:#57534a}
.sharebar{height:4px;background:var(--rule);margin:10px 0 14px;position:relative}
.sharebar i{position:absolute;left:0;top:0;bottom:0;background:var(--red);display:block}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
.chip{font:11px monospace;border:1px solid var(--red);color:var(--red);background:none;padding:3px 6px;cursor:pointer;border-radius:2px}
.acc{border-top:1px solid var(--rule)}
.accbtn{width:100%;display:flex;justify-content:space-between;align-items:center;background:none;border:none;border-bottom:1px solid var(--rule);padding:12px 2px;cursor:pointer;font:12px monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink)}
.accbtn .chev{color:#57534a}
.accbody{border-bottom:1px solid var(--rule);padding:12px 2px 16px}
.hint{font:11px monospace;color:#57534a;margin:6px 0 0}
input[type=text],select{width:100%;background:#fffdf8;border:1px solid var(--rule);padding:8px 10px;font:14px sans-serif;color:var(--ink);border-radius:0}
input[type=text]:focus,select:focus{outline:3px solid var(--red);outline-offset:1px;border-color:var(--red)}
label.f{display:block;font:11px monospace;letter-spacing:.1em;text-transform:uppercase;color:#57534a;margin:12px 0 4px}
```

Tiles:
```css
.tiles{display:flex;flex-wrap:wrap;gap:36px;margin:6px 0 8px}
.tile .big{font-family:Georgia,serif;font-size:46px;line-height:1}
.tile .sub{font:13px sans-serif;margin-top:6px;max-width:34ch}
.tile .how{font:11px monospace;color:#57534a;margin-top:6px;max-width:38ch}
.mechtiles{display:flex;flex-wrap:wrap;gap:28px;margin:18px 0 8px;padding-top:14px;border-top:1px solid var(--rule)}
.mech .dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:8px}
```

Figures:
```css
figure{margin:34px 0 0}
figcaption .figtitle{font-family:Georgia,serif;font-size:22px;margin:0 0 4px}
.figsrc{font:11px monospace;color:#57534a;margin:0 0 12px}
.chartbox{height:340px;position:relative}
.chartbox.tall{height:320px}
.norecords{font:14px sans-serif;color:#57534a;padding:30px 0}
```

Tables:
```css
table{width:100%;border-collapse:collapse;margin:10px 0 4px;font-size:15px}
caption{text-align:left;font:11px monospace;letter-spacing:.08em;text-transform:uppercase;color:#57534a;padding:6px 0;border-bottom:1px solid var(--rule)}
th{font:11px monospace;letter-spacing:.1em;text-transform:uppercase;color:#57534a;text-align:left;padding:8px 10px 8px 0;border-bottom:1px solid var(--ink);font-weight:400}
td{padding:8px 10px 8px 0;border-bottom:1px solid var(--rule);vertical-align:top}
td.num,th.num{text-align:right}
tbody tr.data{cursor:pointer}
tbody tr.data:hover{background:rgba(155,35,53,.05)}
tr.detail td{background:#efe9dc;padding:16px 18px}
.paranum{font-family:Georgia,serif;font-size:30px;color:var(--red);margin-bottom:8px}
.fulltext{max-width:75ch;white-space:pre-wrap}
.lbl{font:11px monospace;...}
.tagchip{display:inline-block;border:1px solid var(--rule);padding:2px 8px;margin:2px 4px 2px 0;font-size:12px;border-radius:2px}
mark{background:rgba(155,35,53,.22);color:inherit;padding:0 1px}
.btn{font:12px monospace;letter-spacing:.1em;text-transform:uppercase;background:none;border:1px solid var(--rule);color:var(--ink);padding:8px 14px;cursor:pointer;border-radius:2px}
.btn:hover{border-color:var(--ink)}
.btn.primary{border-color:var(--red);color:var(--red)}
.btn[aria-pressed=true]{background:var(--red);color:var(--paper);border-color:var(--red)}
```

Checks:
```css
.check{display:flex;gap:10px;padding:9px 0;border-bottom:1px solid var(--rule);font-size:14px}
.check .mark{font-family:monospace}
.check.fail .mark{color:var(--red);font-weight:bold}
.check.warn .mark{color:var(--red)}
.check .what{font:11px monospace;...}
```

Sample cards:
```css
.samplecard{border-bottom:1px solid var(--rule)}
.samplebtn{width:100%;text-align:left;background:none;border:none;padding:10px 2px;cursor:pointer;font:13px monospace;color:var(--ink);display:flex;justify-content:space-between}
.samplebody{padding:4px 2px 16px}
```

Footer:
```css
footer{position:sticky;bottom:0;background:var(--paper);border-top:1px solid var(--rule);padding:8px 0;font:11px monospace;color:#57534a}
```

Responsive: @media (max-width:900px){.layout{grid-template-columns:1fr}.rail{position:static}}.

Now the JS in full. Let me write it mentally then output.

```js
(function(){
"use strict";
const D = window.WORKSHOP_DATA.uhri;
const COUNTRY = D.country;
const SDG_NAMES = D.sdg_names || {};
const RECS = D.records.map(function(r,i){
  const m = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/.exec(r.text||"");
  const para = m ? m[1] : null;
  let states = [];
  if(r.mechanism === "Universal Periodic Review"){
    const run = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/.exec(r.text||"");
    if(run){
      const groups = run[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
      const names = groups.map(function(g){ return g.slice(1,-1).trim(); });
      const bad = names.some(function(n){ return n.indexOf(",") !== -1 || n.length > 60; });
      states = bad ? ["State not found"] : names;
    }
  }
  return { r:r, i:i, para:para, states:states };
});
```

Hmm — I'll keep records as original objects plus attached props via Object.assign? Mutating input objects is fine: `r._para=para; r._states=states; r._i=i;`. Simpler. Do that.

Helpers:
```js
const $ = function(s, el){ return (el||document).querySelector(s); };
const $$ = function(s, el){ return Array.prototype.slice.call((el||document).querySelectorAll(s)); };
function esc(s){ return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
function fmt(n){ return Number(n).toLocaleString("en-GB"); }
function countBy(list, fn){ const o={}; for(const x of list){ const k=fn(x); o[k]=(o[k]||0)+1; } return o; }
```

Years: `const YEARS = Array.from(new Set(RECS.map(r=>r.year))).sort((a,b)=>a-b);`

State:
```js
const state = {
  tab:0, sortAsc:false, shown:50, openAcc:"kw",
  filters:{ keyword:"", mechanism:"all", body:"all", type:"all", state:"all", theme:"all", yf:YEARS[0], yt:YEARS[YEARS.length-1], sdg:"all" },
  expanded:new Set(), showStates:false,
  sampleSeed:1, sampleIds:null, sampleOpen:null, verdicts:{}
};
```

filtered():
```js
function filtered(){
  const f=state.filters;
  const words=f.keyword.trim().toLowerCase().split(/\s+/).filter(Boolean);
  let yf=f.yf, yt=f.yt; if(yf>yt){ const t=yf; yf=yt; yt=t; }
  return RECS.filter(function(r){
    if(f.mechanism!=="all" && r.mechanism!==f.mechanism) return false;
    if(f.body!=="all" && r.body!==f.body) return false;
    if(f.type!=="all" && r.type!==f.type) return false;
    if(f.state!=="all" && r._states.indexOf(f.state)===-1) return false;
    if(f.theme!=="all" && (r.themes||[]).indexOf(f.theme)===-1) return false;
    if(f.sdg!=="all" && (r.sdgs||[]).indexOf(Number(f.sdg))===-1) return false;
    if(r.year<yf || r.year>yt) return false;
    if(words.length){ const hay=(r.text+" "+r.symbol).toLowerCase(); for(const w of words){ if(hay.indexOf(w)===-1) return false; } }
    return true;
  });
}
```

themeCounts(f): countBy over themes. topThemes(f,n): entries sorted count desc then name asc, slice n, plus year range: need per-theme year min/max — compute in loop:
```js
function themeStats(f){
  const m={};
  for(const r of f){ for(const t of (r.themes||[])){ const e=m[t]||(m[t]={count:0,ymin:r.year,ymax:r.year}); e.count++; if(r.year<e.ymin)e.ymin=r.year; if(r.year>e.ymax)e.ymax=r.year; } }
  return Object.entries(m).map(([theme,e])=>({theme:theme,count:e.count,ymin:e.ymin,ymax:e.ymax}))
    .sort((a,b)=> b.count-a.count || a.theme.localeCompare(b.theme));
}
```

Mechanism colors map.

Render rail:
```js
function renderRail(){
  const f=state.filters;
  const all=RECS.length, m=filtered().length;
  $("#matchNum").textContent=fmt(m);
  $("#matchSub").textContent="matching records · of "+fmt(all)+" in the file";
  $("#shareFill").style.width=(all? (100*m/all):0)+"%";
  // chips
  const chips=[];
  if(f.keyword.trim()) chips.push({k:"keyword",label:'Keyword: "'+f.keyword.trim()+'"'});
  if(f.mechanism!=="all") chips.push({k:"mechanism",label:"Mechanism: "+f.mechanism});
  if(f.body!=="all") chips.push({k:"body",label:"Body: "+f.body});
  if(f.type!=="all") chips.push({k:"type",label:"Type: "+f.type});
  if(f.state!=="all") chips.push({k:"state",label:"State: "+f.state});
  if(f.theme!=="all") chips.push({k:"theme",label:"Theme: "+f.theme});
  if(f.yf!==YEARS[0]||f.yt!==YEARS[YEARS.length-1]) chips.push({k:"years",label:"Years: "+f.yf+"–"+f.yt});
  if(f.sdg!=="all") chips.push({k:"sdg",label:"SDG: "+f.sdg});
  const chipBox=$("#chips"); chipBox.innerHTML="";
  chips.forEach(function(c){
    const b=document.createElement("button"); b.className="chip"; b.type="button";
    b.textContent=c.label+" ×"; b.setAttribute("aria-label","Remove filter "+c.label);
    b.onclick=function(){ resetFilter(c.k); };
    chipBox.appendChild(b);
  });
  // accordions visibility
  $("#accWrap").hidden = state.tab>=2;
  // accordion open state
  $$(".accbtn").forEach(function(btn){
    const open = state.openAcc===btn.dataset.acc;
    btn.setAttribute("aria-expanded", open?"true":"false");
    $("#acc-"+btn.dataset.acc).hidden = !open;
  });
  // populate selects (only when values changed — just re-render each time, preserving selection)
  buildSelects();
}
```

resetFilter(k): defaults: keyword "" (also clear inputs), mechanism/body/type/state/theme/sdg "all", yf/yt extremes. Then shown=50, render().

buildSelects(): 
- mechanism select: options all + distinct mechanisms (order of appearance in RECS). Keep current value if still valid.
- body select: if mechanism!=="all", bodies among RECS with that mechanism; else all bodies. With counts (from RECS full). If current body not in list → set "all".
- type select: distinct types with counts.
- state select: distinct states from UPR RECS excluding "State not found", with counts (records containing). Sorted by count desc then name? Plan: "a select listing every State found, with counts". I'll sort alphabetically... or by count desc — count desc more useful. I'll do count desc, then alpha.
- year from/to selects: YEARS.
- sdg select: distinct sdg numbers present, sorted numeric, label `${g} — ${SDG_NAMES[String(g)]||""}`.

Each select: label + select element. On change handlers update filters (body change also resets? no). For yf/yt: on change, if yf>yt swap values in both selects and state.

Keyword inputs: two inputs; function bindKw(input){ input.addEventListener("input", ...) debounce → set both inputs' value, filters.keyword, shown=50, render() }. But render() re-renders rail including inputs — rebuilding inputs on each render loses focus! Problem: renderRail rebuilds selects each time → focus loss while interacting? Selects: change event fires on selection, then re-render replaces select — focus lost but interaction done. Acceptable but not great. Keyword input: typing → debounce 300ms → render → input rebuilt → focus lost. Bad UX. Solution: don't rebuild rail inputs on every render; build once, and update options only when needed. Better approach: build rail DOM once at init; renderRail only updates dynamic bits (number, bar, chips, accordion states, select options). For selects, update options only if the option list changed (compare signature). For keyword inputs, never rebuild — just keep them; on resetFilter set their .value directly.

I'll implement: initRail() builds static structure once; renderRail() updates: number/sub/bar, chips, accordion hidden states, and select options via updateSelect(el, options, currentValue) which rebuilds options only if signature differs, preserving value. Keyword inputs bound once.

Similarly tab 02 search input: build once in init, bound once; renderRecords shouldn't rebuild it. So tab panels: I'll build each panel's static skeleton once (init), and render functions fill dynamic containers. That avoids focus loss and chart canvas recreation issues... but charts need canvas; I'll keep canvas elements persistent in panel 0 and only (re)create Chart instances on render when tab 0 active. When tab 0 inactive, destroy charts? If canvas hidden (panel hidden), Chart.js with responsive:true may resize to 0. On switching back, call renderOverview() which destroys and rebuilds. OK.

Plan: 
- init(): fill header/footer, build rail skeleton, build panel skeletons (tab 02 search + table container + show more btn; tab 03 containers; tab 04 static content + buttons), bind events, then render().
- render(): renderRail(); renderTab(state.tab).
- renderTab(i): switch.

Panels skeleton:

Panel 0:
```html
<section id="panel-0" role="tabpanel" aria-labelledby="tab-0">
  <div class="tiles" id="tiles"></div>
  <div class="mechtiles" id="mechTiles"></div>
  <div id="statesBox" hidden>...</div>
  <figure id="fig1">
    <figcaption>
      <p class="figtitle" id="fig1Title"></p>
      <p class="figsrc" id="fig1Src"></p>
    </figcaption>
    <div class="chartbox" id="fig1Box"><canvas id="chart1"></canvas></div>
    <div id="fig1Empty" class="norecords" hidden>No records match the current filters.</div>
    <table id="fig1Table">... thead ... <tbody id="fig1Body"></tbody></table>
    <p class="hint" id="fig1Note"></p>
  </figure>
  <figure id="fig2">... canvas chart2 ...</figure>
</section>
```

renderOverview(): compute f=filtered(); tiles innerHTML; mech tiles; states box if showStates; fig1: top10=themeStats(f).slice(0,10); if f.length===0 → hide chart box show empty, clear table; else build chart (destroy old), fill table rows; fig2 similar with stacked.

Chart creation each render: destroy previous via stored refs.

Panel 1:
```html
<section id="panel-1" ...>
  <div class="searchrow">
    <input type="text" id="kw2" placeholder="Search … records, e.g. torture" aria-label="Keyword search">
    <p class="hint">literal match, not synonyms · every word must appear in the text or symbol</p>
  </div>
  <table id="recTable">
    <caption id="recCaption"></caption>
    <thead><tr>
      <th><button id="dateSort" class="thbtn">Date <span id="dateArrow">↓</span></button></th>
      <th>Body</th><th>Symbol</th><th>Para.</th><th>First line</th><th>Recommending State</th>
    </tr></thead>
    <tbody id="recBody"></tbody>
  </table>
  <div id="recEmpty" class="norecords" hidden>No records match the current filters.</div>
  <button class="btn" id="showMore" type="button">Show 50 more</button>
</section>
```

th button styling: inherit th style, background none border none cursor pointer.

renderRecords(): m=filtered(); sorted; caption `Showing ${Math.min(shown,m.length)} of ${fmt(m.length)} matching records · ${sortAsc?'oldest':'newest'} first`; rows slice(0,shown); each record → tr.data (tabindex 0, aria-expanded) + tr.detail hidden. Build with innerHTML strings for speed, but need event handlers — use event delegation on tbody: click → closest tr.data → toggle expand; keydown Enter/Space. Delegation avoids per-row handlers. 

Row HTML:
```js
const states = r.mechanism==="Universal Periodic Review" ? (r._states.length? r._states.join(" · ") : "State not found") : "—";
```
Wait: UPR with no trailing parentheses at all → states=[] → show "State not found"? Plan: "otherwise the record gets 'State not found'" refers to failed group. If no parentheses at all... 1,370 of UPR end with parenthesis; some don't. For those, states=[] — display "—"? The check "States found" lists records without one. Display: if UPR and states empty → "State not found"? Hmm, plan says dash for treaty/SP rows; UPR rows show the State(s). For UPR with none found, showing "State not found" is informative. I'll show "State not found" when UPR && no accepted states (whether empty or failed). Actually if run matched but all groups failed → ["State not found"]. If no run → [] → also display "State not found"? I'll display "—" only for non-UPR; for UPR with empty states show "State not found". OK.

Detail row content:
```js
'<td colspan="6"><div class="paranum">'+(r._para? 'para. '+esc(r._para) : 'no paragraph number in this extract')+'</div>'
+'<p class="fulltext">'+hi(r.text)+'</p>'
+ labels html
+'<div class="rowactions"><button class="btn copybtn" data-id="'+r.id+'">'+(r._para?'Copy citation':'Copy citation (no paragraph number in this extract)')+'</button> '
+'<a class="btn" href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">Open the UN document</a> <span class="copied" hidden>Copied ✓</span></div></td>'
```

Labels html:
```js
function labelsHtml(r){
  let h='<div class="labels">';
  h+='<div><span class="lbl">Section</span> '+(r.section? esc(r.section) : '<span class="missing">not labelled</span>')+'</div>';
  h+='<div><span class="lbl">Themes</span> '+((r.themes&&r.themes.length)? r.themes.map(t=>'<span class="tagchip">'+esc(t)+'</span>').join("") : '<span class="missing">not labelled</span>')+'</div>';
  const sdgs=(r.sdgs||[]).map(g=>'SDG '+g+(SDG_NAMES[String(g)]?': '+SDG_NAMES[String(g)]:'')).join("; ");
  h+='<div><span class="lbl">SDGs</span> '+(sdgs||'<span class="missing">not labelled</span>')+'</div>';
  h+='<div><span class="lbl">SDG targets</span> '+((r.sdg_targets&&r.sdg_targets.length)? esc(r.sdg_targets.join("; ")) : '<span class="missing">not labelled</span>')+'</div>';
  h+='<div><span class="lbl">Affected persons</span> '+((r.affected_persons&&r.affected_persons.length)? esc(r.affected_persons.join("; ")) : '<span class="missing">not labelled</span>')+'</div>';
  h+='</div>';
  return h;
}
```

Copy citation delegation: click .copybtn → find record by id → text → clipboard → show "Copied" (the span next to it) 2s.

Clipboard helper:
```js
function copyText(t, done){
  if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(done, function(){fallback(t,done);}); }
  else fallback(t,done);
}
function fallback(t,done){ const ta=document.createElement("textarea"); ta.value=t; ta.style.position="fixed"; ta.style.opacity="0"; document.body.appendChild(ta); ta.select(); try{document.execCommand("copy");}catch(e){} document.body.removeChild(ta); done(); }
```

Panel 2 (checks):
```html
<section id="panel-2">
  <h2 class="sect">How the app checks itself</h2>
  <p class="hint">Every check compares two values computed in this page; failures are shown, never hidden.</p>
  <div id="checkList"></div>
  <h2 class="sect">Random-sample label check</h2>
  <p class="hint">This is your judgement of the UN's labels; nothing is sent anywhere.</p>
  <div class="samplectl">
    <button class="btn primary" id="drawBtn">Check 10 at random</button>
    <label class="f inline">Seed <input type="number" id="seedBox" value="1" min="0" step="1" style="width:90px"></label>
    <button class="btn" id="drawSeed">Draw with this seed</button>
    <button class="btn" id="drawAgain">Draw again</button>
  </div>
  <p class="tally" id="tally"></p>
  <div id="sampleList"></div>
</section>
```

renderChecks(): checks list; sample: if state.sampleIds null → prompt text "Draw 10 records to check the UN's theme labels." else cards.

Card:
```js
sampleIds.map(id=>{ const r=byId[id]; const open = state.sampleOpen===id; ... })
```
Card button line: `${r.symbol} · para ${r._para||"—"} · ${r.year}` + chevron. Body: full text (esc), themes chips, verdict buttons with aria-pressed.

Verdict click: state.verdicts[state.sampleSeed+"|"+id]=v; renderTab(2) (re-render checks panel only — but render() re-renders rail too; fine, call render()).

Hmm render() re-renders rail selects options — updateSelect preserves value; ok.

Tally: 
```js
const vs = state.sampleIds.map(id=>state.verdicts[state.sampleSeed+"|"+id]);
fit = vs.filter(v=>v==="fit").length etc.
tally.textContent = `Themes: ${fit} fit · ${no} don't fit · ${uns} unsure · ${judged} of ${sampleIds.length} judged · seed ${state.sampleSeed}`;
```

Draw handlers:
- drawBtn ("Check 10 at random"): draw with current seed box value.
- drawSeed: seed = parseInt(seedBox.value)||1; state.sampleSeed=seed; draw.
- drawAgain: seed = Math.floor(Math.random()*1000000); seedBox.value=seed; state.sampleSeed=seed; draw.

draw(): compute f=filtered(); seeded shuffle; sampleIds; sampleOpen=null; render().

If filter changes and sampleIds exist → redraw with same seed (in render? I'll do in setFilter: if state.sampleIds, redraw silently). Implement in the filter-change path: after filters change, call redrawSample() which recomputes sampleIds from new filtered with same seed (no render recursion — just set sampleIds).

Panel 3 (method):
Static HTML with method sentences + buttons:
```html
<section id="panel-3">
  <h2 class="sect">How each number is computed</h2>
  <ol class="method"> six <li> </ol>
  <h2 class="sect">Take it with you</h2>
  <button class="btn primary" id="csvBtn">Download CSV of the current filter</button>
  <button class="btn" id="sumBtn">Copy summary</button> <span id="sumCopied" hidden>Copied ✓</span>
  <h2 class="sect">Source</h2>
  <p id="srcLine"></p>
</section>
```

CSV:
```js
function downloadCSV(){
  const f=filtered();
  const lines=[];
  lines.push("# Country: "+COUNTRY);
  lines.push("# Source: "+D.source+" — "+D.source_url);
  lines.push("# Built: "+D.built);
  lines.push("# Filters: "+filterDesc());
  lines.push("# Rows: "+f.length+" of "+RECS.length+" records");
  const head=["Date","Body","Mechanism","Type","Symbol","Document URL","Paragraph","Recommending State(s)","Section","Themes","SDGs","SDG targets","Affected persons","Text"];
  lines.push(head.map(csvCell).join(","));
  for(const r of f){
    lines.push([r.date,r.body,r.mechanism,r.type,r.symbol,r.doc_url,r._para||"",r._states.join("; "),r.section||"",(r.themes||[]).join("; "),(r.sdgs||[]).join("; "),(r.sdg_targets||[]).join("; "),(r.affected_persons||[]).join("; "),r.text].map(csvCell).join(","));
  }
  const blob=new Blob([lines.join("\r\n")],{type:"text/csv;charset=utf-8"});
  const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download="uhri-"+COUNTRY.toLowerCase()+"-recommendations.csv"; document.body.appendChild(a); a.click(); setTimeout(function(){URL.revokeObjectURL(a.href); a.remove();},500);
}
```

filterDesc(): list active filters or "none".

Copy summary:
```js
function summaryText(){
  const f=filtered(); const n=f.length;
  const byType=countBy(f,r=>r.type);
  const types=Object.entries(byType).map(([t,c])=>t+": "+fmt(c)).join(" · ");
  const docs=new Set(f.map(r=>r.symbol)).size;
  const ys=f.map(r=>r.year); const ymin=Math.min(...ys), ymax=Math.max(...ys);
  const top=themeStats(f).slice(0,10).map((t,i)=>(i+1)+") "+t.theme+" ("+fmt(t.count)+")").join(", ");
  return COUNTRY+": "+fmt(n)+" UN recommendations and observations ("+types+") from "+fmt(docs)+" documents, "+ymin+"–"+ymax+", dated by document. Top themes among the "+fmt(n)+" filtered records: "+top+". Source: "+D.source+" ("+D.source_url+"), built "+D.built+". Filters: "+filterDesc()+".";
}
```
Careful with empty f: Math.min of empty → Infinity. Guard: if n===0 → "0 records match...".

Tabs keyboard: 
```js
tablist.addEventListener("keydown", e=>{
  if(e.key==="ArrowRight"||e.key==="ArrowLeft"){ e.preventDefault(); let i=state.tab + (e.key==="ArrowRight"?1:-1); i=(i+4)%4; switchTab(i); $("#tab-"+i).focus(); }
});
```

switchTab(i): state.tab=i; update aria-selected & hidden on panels; renderRail(); renderTab(i).

Accordion buttons: click → state.openAcc = (state.openAcc===key? null : key); renderRail().

Clear all: reset all filters + inputs; shown=50; redraw sample; render().

Now header fill:
```js
$("#kicker").textContent="UHRI · "+COUNTRY.toUpperCase();
$("#title").textContent="UN human rights recommendations and observations: "+COUNTRY;
const docs=new Set(RECS.map(r=>r.symbol)).size;
const ymin=Math.min(...RECS.map(r=>r.year)), ymax=Math.max(...);
$("#meta").innerHTML = 'Source: <a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">'+esc(D.source)+'</a> · '+fmt(RECS.length)+' records · '+fmt(docs)+' documents · '+ymin+'–'+ymax+' · built '+esc(D.built)+' · dated by document';
```
Hmm "dated by document" hint — include. Also mention count string check? The check tab covers it.

Footer:
```js
$("#footer").innerHTML = '<div class="wrap footline">Built on OHCHR UHRI data · '+fmt(RECS.length)+' records · <a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">'+esc(D.source)+'</a></div><div class="wrap credits">Credits: chart and table practice after UK Government Analysis Function guidance; citation form after Dag Hammarskjöld Library Ask DAG; data practice after OHCHR Human Rights-Based Approach to Data guidance note.</div>';
```

Overview tiles render:
```js
function renderOverview(){
  const f=filtered(); const n=f.length;
  const byType=countBy(f,r=>r.type);
  const docs=new Set(f.map(r=>r.symbol)).size;
  const ys=f.map(r=>r.year);
  const tiles=$("#tiles"); 
  let h='';
  h+='<div class="tile"><div class="big">'+fmt(n)+'</div><div class="sub">records in the current filter — '+Object.entries(byType).map(([t,c])=>esc(t)+' '+fmt(c)).join(" · ")+'</div><div class="how">How this is computed: count of records passing every filter, all types included; of '+fmt(RECS.length)+' in the file.</div></div>';
  h+='<div class="tile"><div class="big">'+fmt(docs)+'</div><div class="sub">documents (distinct symbol)</div><div class="how">How this is computed: number of distinct symbol values among the filtered records.</div></div>';
  h+='<div class="tile"><div class="big">'+(n? ys.min... )+'</div>...'
```
years tile: n? `${min}–${max}` : "—". how: "min and max of year among the filtered records; the file spans X–Y."

Mech tiles:
```js
const mechs = distinct mechanisms in RECS (order of first appearance);
for each: sub = count in f, docs in f, latest year in f, share pct of n.
UPR tile extra: '<button class="linkbtn" id="statesLink">see the States</button>'
```
statesBox: if state.showStates && mechanism UPR present: compute state counts among f where mechanism UPR: for each record, for each state (excluding 'State not found') count once. top10. Render list: "Ten States that made most recommendations to {country} (current filter): 1. France (x) ...". Toggle via statesLink click → state.showStates=!; render().

FIG.01:
```js
const top=themeStats(f).slice(0,10);
$("#fig1Title").textContent="FIG.01 · Ten most frequent themes among "+fmt(n)+" filtered records";
$("#fig1Src").textContent="Source: UHRI records, current filter · click a bar to filter by that theme · a record can carry several themes, so counts add up to more than "+fmt(n);
if(n===0){ show empty, destroy chart, clear table body, note }
else{
  build chart1 (destroy old);
  table rows: top.map(t=> `<tr><td>${esc(t.theme)}</td><td class="num">${fmt(t.count)}</td><td class="num">${(100*t.count/n).toFixed(1)}%</td><td>${t.ymin}–${t.ymax}</td></tr>`)
  note: "Percentages are of the "+fmt(n)+" filtered records, not of labels; ties are alphabetical."
}
```

Chart1 build:
```js
if(chart1){chart1.destroy(); chart1=null;}
const ctx=$("#chart1").getContext("2d");
chart1=new Chart(ctx,{type:"bar",data:{labels:top.map(t=>t.theme),datasets:[{label:"records",data:top.map(t=>t.count),backgroundColor:"rgba(155,35,53,0.8)",borderWidth:0}]},options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,onClick:function(e,els){ if(els.length){ setFilter("theme", top[els[0].index].theme); } },scales:{x:{beginAtZero:true,suggestedMax:Math.max(...top.map(t=>t.count))*1.15+1,grid:{color:"#e7e0d2"},ticks:{font:{family:"ui-monospace,Menlo,Consolas,monospace",size:11}},border:{color:"#d9d2c3"}},y:{grid:{display:false},ticks:{font:{size:13}},border:{color:"#d9d2c3"}}},plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return " "+fmt(c.parsed.x)+" records";}}}}},plugins:[barValuePlugin]});
```
barValuePlugin draws fmt(value) at bar end.

Note: onClick els[0].index indexes into top — but chart labels order = top order; with indexAxis y and default (first at top in v3+?) — either way index maps correctly to top[i]. Good.

FIG.02:
```js
const yAll=[]; for(let y=FILE_YMIN;y<=FILE_YMAX;y++) yAll.push(y);
const mechs=distinct mechanisms in RECS;
datasets=mechs.map(m=>({label:m,stack:"s",backgroundColor:MEC_COLORS[m]||"#6b6459",data:yAll.map(y=> f.filter(r=>r.year===y&&r.mechanism===m).length)}));
```
O(n*years*mechs) fine.

Title: "FIG.02 · Records per year by mechanism · "+fmt(n)+" filtered records". Src: "Source: UHRI records, current filter · every year from "+FILE_YMIN+" to "+FILE_YMAX+" is shown, so empty years appear as gaps · dated by document". Legend bottom.

If n===0: still show chart with zeros? Plan: "the chart area shows 'No records match' as text". So for both figs, if n===0 show empty text. OK.

Records render:
```js
function renderRecords(){
  const f=filtered();
  const m=f;
  const sorted=[...m].sort(cmp);
  const shown=Math.min(state.shown, sorted.length);
  $("#recCaption").textContent = m.length? ("Showing "+fmt(shown)+" of "+fmt(m.length)+" matching records · "+(state.sortAsc?"oldest":"newest")+" first · click a row for the full paragraph") : "No records match the current filters.";
  $("#recEmpty").hidden = m.length>0;
  $("#showMore").hidden = shown>=m.length;
  $("#kw2").placeholder = "Search "+fmt(m.length)+" records, e.g. torture";
  const tb=$("#recBody"); tb.innerHTML="";
  const frag=document.createDocumentFragment();
  for(const r of sorted.slice(0,shown)){
    const tr=document.createElement("tr"); tr.className="data"; tr.tabIndex=0; tr.setAttribute("aria-expanded", state.expanded.has(r.id)?"true":"false");
    tr.innerHTML = "<td>"+esc(r.date)+"</td><td>"+esc(r.body)+"</td><td><a href='"+esc(r.doc_url)+"' target='_blank' rel='noopener'>"+esc(r.symbol)+"</a></td><td>"+(r._para?esc(r._para):"—")+"</td><td class='firstline'>"+hi(r._first)+"</td><td>"+stateCell(r)+"</td>";
    tr.dataset.id=r.id;
    frag.appendChild(tr);
    const dt=document.createElement("tr"); dt.className="detail"; dt.hidden=!state.expanded.has(r.id);
    dt.innerHTML= detailHtml(r);
    dt.dataset.id=r.id;
    frag.appendChild(dt);
  }
  tb.appendChild(frag);
}
```

Wait — first line highlight: hi() highlights keyword words; apply to first line too. `r._first` precomputed. hi uses current keyword. Good.

stateCell(r): non-UPR → "—"; UPR: r._states.length? join(" · ") : "State not found". But if states==["State not found"] show that. OK: `r.mechanism==="Universal Periodic Review" ? (r._states.length? esc(r._states.join(" · ")) : "State not found") : "—"`.

Delegation:
```js
$("#recBody").addEventListener("click", function(e){
  const copy=e.target.closest(".copybtn");
  if(copy){ const r=byId[copy.dataset.id]; const cite=r._para? r.symbol+", para. "+r._para : r.symbol; copyText(cite, function(){ const s=copy.parentElement.querySelector(".copied"); if(s){ s.hidden=false; setTimeout(()=>s.hidden=true,2000);} }); return; }
  const tr=e.target.closest("tr.data"); if(tr) toggleRow(tr.dataset.id);
});
$("#recBody").addEventListener("keydown", function(e){ if(e.key==="Enter"||e.key===" "){ const tr=e.target.closest("tr.data"); if(tr){ e.preventDefault(); toggleRow(tr.dataset.id); } } });
function toggleRow(id){ if(state.expanded.has(id)) state.expanded.delete(id); else state.expanded.add(id); renderTab(1); }
```
Note: clicking the symbol link inside row would also toggle — check `if(e.target.closest("a")) return;` before toggle. Add that.

dateSort click: state.sortAsc=!state.sortAsc; update arrow text (↓/↑); renderTab(1).

showMore: state.shown+=50; renderTab(1).

setFilter(k,v): state.filters[k]=v; state.shown=50; if(state.sampleIds) redrawSample(); render();

resetFilter(k): defaults map; if keyword also clear inputs; shown=50; redraw; render().

redrawSample(): if(!state.sampleIds) return; const f=filtered(); shuffle with state.sampleSeed; state.sampleIds=...; (no render — caller renders).

Now checks render:

```js
function renderChecks(){
  const list=$("#checkList"); list.innerHTML="";
  runChecks().forEach(c=>{
    const div=document.createElement("div"); div.className="check"+(c.pass?"":(c.warn?" warn":" fail"));
    div.innerHTML='<span class="mark">'+(c.pass?(c.warn?"⚠":"✓"):"✗")+'</span><span><span class="what">'+esc(c.name)+"</span> — "+esc(c.detail)+(c.list&&c.list.length?'<br><span class="failures">'+c.list.map(esc).join("<br>")+(c.more>0?"<br>… and "+c.more+" more":"")+"</span>":"")+"</span>";
    list.appendChild(div);
  });
  renderSample();
}
```
Hmm warn: pass=true but warn flag → mark ⚠ and class warn. fail: pass=false → ✗ CHECK FAILED. Let me include "CHECK FAILED" text when !pass: detail prefix. I'll add in name rendering: if !c.pass append ' <span class="failtxt">CHECK FAILED</span>'.

renderSample():
```js
const box=$("#sampleList"); box.innerHTML="";
const tally=$("#tally");
if(!state.sampleIds){ tally.textContent=""; box.innerHTML='<p class="hint">No sample drawn yet — press "Check 10 at random".</p>'; return; }
const f=filtered(); // sample drawn from filtered at draw time; but if filters changed we redrew, so sampleIds ⊆ current filtered
const ids=state.sampleIds;
const vs=ids.map(id=>state.verdicts[state.sampleSeed+"|"+id]);
const fit=vs.filter(v=>v==="fit").length, no=vs.filter(v=>v==="no").length, un=vs.filter(v=>v==="unsure").length;
tally.textContent="Themes: "+fit+" fit · "+no+" don't fit · "+un+" unsure · "+(fit+no+un)+" of "+ids.length+" judged · seed "+state.sampleSeed+" · drawn from "+fmt(filtered().length)+" filtered records";
ids.forEach(id=>{
  const r=byId[id]; if(!r) return;
  const open=state.sampleOpen===id;
  const card=document.createElement("div"); card.className="samplecard";
  const btn=document.createElement("button"); btn.type="button"; btn.className="samplebtn"; btn.setAttribute("aria-expanded",open?"true":"false");
  btn.innerHTML="<span>"+esc(r.symbol)+" · para "+(r._para?esc(r._para):"—")+" · "+r.year+"</span><span>"+(open?"–":"＋")+"</span>";
  btn.onclick=function(){ state.sampleOpen=open?null:id; renderTab(2); };
  card.appendChild(btn);
  if(open){
    const body=document.createElement("div"); body.className="samplebody";
    const v=state.verdicts[state.sampleSeed+"|"+id];
    body.innerHTML='<p class="fulltext">'+esc(r.text)+'</p>'
      +'<div><span class="lbl">Themes as labelled by the UN</span> '+((r.themes&&r.themes.length)? r.themes.map(t=>'<span class="tagchip">'+esc(t)+'</span>').join(""):'<span class="missing">not labelled</span>')+'</div>'
      +'<div class="verdicts">'
      +['fit','no','unsure'].map(k=>'<button type="button" class="btn verdict" data-id="'+id+'" data-v="'+k+'" aria-pressed="'+(v===k)+'">'+(k==="fit"?"Fits":k==="no"?"Doesn't fit":"Unsure")+'</button>').join(" ")
      +'</div>';
    card.appendChild(body);
  }
  box.appendChild(card);
});
$("#sampleList").addEventListener("click", e=>{ const b=e.target.closest(".verdict"); if(!b) return; state.verdicts[state.sampleSeed+"|"+b.dataset.id]=b.dataset.v; renderTab(2); });
```
Bind once at init (delegation on #sampleList which persists).

Draw buttons bound once:
```js
$("#drawBtn").onclick=()=>{ state.sampleSeed=parseInt($("#seedBox").value,10)||1; drawSample(); };
$("#drawSeed").onclick=()=>{ state.sampleSeed=parseInt($("#seedBox").value,10)||1; drawSample(); };
$("#drawAgain").onclick=()=>{ state.sampleSeed=Math.floor(Math.random()*1000000); $("#seedBox").value=state.sampleSeed; drawSample(); };
function drawSample(){ const f=filtered(); const rnd=mulberry32(state.sampleSeed>>>0); const idx=f.map((_,i)=>i); for(let i=idx.length-1;i>0;i--){ const j=Math.floor(rnd()*(i+1)); const t=idx[i]; idx[i]=idx[j]; idx[j]=t; } state.sampleIds=idx.slice(0,Math.min(10,idx.length)).map(i=>f[i].id); state.sampleOpen=null; render(); }
```

Method tab: static; bind csvBtn, sumBtn once.

Init sequence at bottom:
```js
buildHeader(); buildFooter(); initRail(); initPanels(); bindTabs(); render();
```

initRail builds:
```html
<aside class="rail">
  <div class="railhead"><span>Filters</span><button id="clearAll" class="mini">Clear all</button></div>
  <div class="matchnum" id="matchNum" aria-live="polite">–</div>
  <div class="matchsub" id="matchSub"></div>
  <div class="sharebar" aria-hidden="true"><i id="shareFill"></i></div>
  <div class="chips" id="chips"></div>
  <div id="accWrap">
    <div class="acc">
      <button class="accbtn" data-acc="kw" aria-expanded="true" aria-controls="acc-kw"><span>01 Keyword</span><span class="chev">…</span></button>
      <div class="accbody" id="acc-kw">
        <input type="text" id="kw1" placeholder="e.g. torture" aria-label="Keyword search">
        <p class="hint">literal match, not synonyms · every word must appear in the text or symbol · applied 300 ms after typing</p>
      </div>
    </div>
    <div class="acc">
      <button class="accbtn" data-acc="mech" aria-expanded="false" aria-controls="acc-mech"><span>02 Mechanism, body, type</span><span class="chev"></span></button>
      <div class="accbody" id="acc-mech" hidden>
        <label class="f" for="selMech">Mechanism</label><select id="selMech"></select>
        <label class="f" for="selBody">Body or mandate</label><select id="selBody"></select>
        <label class="f" for="selType">Type</label><select id="selType"></select>
        <label class="f" for="selState">Recommending State (UPR)</label><select id="selState"></select>
      </div>
    </div>
    <div class="acc">
      <button class="accbtn" data-acc="yr" aria-expanded="false" aria-controls="acc-yr"><span>03 Years and SDG</span><span class="chev"></span></button>
      <div class="accbody" id="acc-yr" hidden>
        <label class="f" for="selYf">Year from</label><select id="selYf"></select>
        <label class="f" for="selYt">Year to</label><select id="selYt"></select>
        <label class="f" for="selSdg">SDG</label><select id="selSdg"></select>
      </div>
    </div>
  </div>
</aside>
```

Since rail is in HTML directly (static in the file), I can just write it in HTML rather than JS-build. Yes — write rail HTML statically in the document; JS binds. Same for panels' static parts. Good, simpler.

updateSelect(el, options, value): options = [{v, label}]; signature = options.map(o=>o.v).join("|"); if el.dataset.sig!==sig → rebuild options; el.value=value (if option exists else "all"... ensure value present).

Select change handlers:
```js
$("#selMech").onchange=e=>{ setFilter("mechanism", e.target.value); if(state.filters.body!=="all"){ /* body may not exist in new mechanism; updateSelect will reset to all if missing */ } };
```
In buildSelects, after computing body options, if current f.body not among them → f.body="all" (without full render recursion — set directly then continue). I'll handle inside updateSelect: if value not in options, set to first option ("all") and also update state.filters accordingly. Let me make updateSelect return the effective value and assign to filter.

Simplify: 
```js
function fillSelect(el, opts, cur){
  const sig=opts.map(o=>o.v).join("\u0001");
  if(el.dataset.sig!==sig){ el.dataset.sig=sig; el.innerHTML=opts.map(o=>'<option value="'+esc(o.v)+'">'+esc(o.label)+'</option>').join(""); }
  if(cur!=null && opts.some(o=>o.v===cur)) el.value=cur; else el.value=opts[0].v;
  return el.value;
}
```
Then in renderRail:
```js
const f=state.filters;
f.mechanism=fillSelect(selMech, mechOpts, f.mechanism);
f.body=fillSelect(selBody, bodyOpts, f.body);
f.type=fillSelect(selType, typeOpts, f.type);
f.state=fillSelect(selState, stateOpts, f.state);
f.yf=fillSelect(selYf, yearOpts, f.yf);
f.yt=fillSelect(selYt, yearOpts, f.yt);
f.sdg=fillSelect(selSdg, sdgOpts, f.sdg);
if(f.yf>f.yt){ const t=f.yf; f.yf=f.yt; f.yt=t; selYf.value=f.yf; selYt.value=f.yt; }
```
But careful: fillSelect assigning f.mechanism from el.value — if user changed select, onchange fires setFilter which sets f then render; in render fillSelect keeps value. But assigning f.x = el.value in render could overwrite... it's the same value. OK. But there's a subtle loop: onchange → setFilter → render → fillSelect sets el.value=cur (same). Fine.

However: assigning f.body when body options changed (mechanism changed) — fillSelect resets to "all" if missing. Good.

Change handlers:
```js
selMech.onchange=e=>setFilter("mechanism", e.target.value);
selBody.onchange=e=>setFilter("body", e.target.value);
selType.onchange=e=>setFilter("type", e.target.value);
selState.onchange=e=>setFilter("state", e.target.value);
selYf.onchange=e=>setFilter("yf", Number(e.target.value));
selYt.onchange=e=>setFilter("yt", Number(e.target.value));
selSdg.onchange=e=>setFilter("sdg", e.target.value);
```
setFilter(k,v): state.filters[k]=v; state.shown=50; redrawSample(); render();

Note yf/yt swap handled in renderRail.

Keyword binding:
```js
function bindKw(input){
  let t;
  input.addEventListener("input", ()=>{
    clearTimeout(t);
    t=setTimeout(()=>{ state.filters.keyword=input.value; state.shown=50; redrawSample(); const other=input.id==="kw1"?$("#kw2"):$("#kw1"); if(other && other.value!==input.value) other.value=input.value; render(); },300);
  });
}
```
render() re-renders rail but doesn't rebuild inputs (static HTML), so focus stays. 

But renderRail calls fillSelect which may reset select values — fine.

One issue: render() → renderRail → fillSelect uses f values; ok.

Accordion buttons: static HTML with data-acc; click handler: state.openAcc = state.openAcc===k? null : k; renderRail(). renderRail updates aria-expanded and hidden on .accbody. But .accbody hidden toggling — I set `$("#acc-"+k).hidden=!open`. Since accWrap hidden on tabs 2/3, fine.

Clear all:
```js
$("#clearAll").onclick=()=>{
  const f=state.filters;
  f.keyword=""; f.mechanism="all"; f.body="all"; f.type="all"; f.state="all"; f.theme="all"; f.sdg="all"; f.yf=YEARS[0]; f.yt=YEARS[YEARS.length-1];
  $("#kw1").value=""; $("#kw2").value="";
  state.shown=50; redrawSample(); render();
};
```

resetFilter(k): similar for one key; keyword clears inputs.

Chips: built in renderRail with onclick → resetFilter(k). For "years" chip → reset yf/yt.

Now hi() and firstLine:
```js
function firstLine(t){ t=String(t||""); if(t.length<=120) return t; let c=t.slice(0,120); const sp=c.lastIndexOf(" "); if(sp>60) c=c.slice(0,sp); return c+"…"; }
```
Plan: "cut at the last space before the limit" — sp>0; use sp>0. If no space, keep 120 chars + "…". I'll use if(sp>0).

Precompute r._first at map time.

byId map: `const byId={}; RECS.forEach(r=>byId[r.id]=r);`

cmp for table sort as above.

MEC order: `const MECHS=[...new Set(RECS.map(r=>r.mechanism))];`

MEC_COLORS as given.

Now runChecks details — implement as planned. tail(text): last 90 chars: `t.length>90? "…"+t.slice(-90): t`.

Check 4 "chart against table": I'll recompute via independent loop and compare with themeStats used for chart; also verify table rows equal top10 (they're generated from same array — the check recomputes and compares values). Implement:
```js
const f=filtered();
const a=themeStats(f).slice(0,10);
const b={}; for(const r of f){ for(const t of (r.themes||[])) b[t]=(b[t]||0)+1; }
const bTop=Object.entries(b).map(([theme,count])=>({theme,count})).sort((x,y)=>y.count-x.count||x.theme.localeCompare(y.theme)).slice(0,10);
const same = a.length===bTop.length && a.every((t,i)=>t.theme===bTop[i].theme && t.count===bTop[i].count);
const largest = a.length? a[0].count : 0;
pass = same && largest<=f.length;
detail: `FIG.01 top ten recomputed by a second loop: ${same?"identical":"DIFFERENT"}; largest bar ${largest} ≤ ${f.length} filtered records: ${largest<=f.length?"yes":"no"}`;
```

Check 6 paragraph: per mechanism share; warn if UPR <100%.

Check 7 states: list noState records: symbol + tail of text.

Check 8: as planned.

Also check 1: `Number(D.count)` — D.count may be string; Number("2264")=2264.

Now method tab text (write in HTML directly):

"How each number is computed"
1. Every number on this page is computed in your browser by looping over the records of the attached UHRI file; nothing is estimated and no outside service, model or network request is involved.
2. The headline count is the number of records passing all filters; documents are the distinct symbol values; years are the minimum and maximum of year among those records.
3. Filters combine with AND: each keyword word must appear literally in the text or the symbol; mechanism, body, type and State match exactly; years are inclusive between the two selects; an SDG matches when its goal number is in the record's sdgs list; a theme matches when the record carries it.
4. Paragraph numbers are read from the first number at the start of the text (for example "71." or "144.43"); recommending States are read from the trailing parentheses of UPR records only, never from treaty-body texts.
5. Theme counts count each theme once per record, so the ten bars add up to more than the record count; percentages are shares of the filtered records.
6. The CSV export contains exactly the filtered records with the columns you see on the Records tab, plus the full text and labels, generated in the browser.

Source block: `Source: {D.source} — link. Built {D.built}. Terms of use: as stated on the source page. The file holds one country ({COUNTRY}); no other country is compared.`

Buttons: csvBtn, sumBtn.

Now — the "see the States" list: place under mech tiles:
```js
if(state.showStates){ compute uprF = f.filter(r=>r.mechanism==="Universal Periodic Review"); stateCounts; top10; render into #statesBox with title "Ten States that made most recommendations to "+COUNTRY+" · current filter" and rows "France — 123 recommendations" }
```
Link in UPR tile: `<button class="linkbtn" id="statesLink">` — but tiles re-rendered each time; bind via delegation on #mechTiles: click #statesLink → toggle. Use delegation.

linkbtn style: monospace small underline red.

OK. Also tab 01 "Nothing else on this tab" — fine.

Potential Chart.js nuance: `border` in scale config is v4 (`border` instead of `gridBorder`). Chart.js 4 supports `border:{color}`. grid color via `grid:{color}`. OK.

Ticks font: `ticks:{font:{...}}` fine.

For stacked chart y ticks integer: `ticks:{precision:0}`.

Legend: `plugins:{legend:{position:"bottom", labels:{usePointStyle:true, pointStyle:"rect"}}}`.

Tooltip for stacked: default fine.

Now, one more requirement: "Every row that shows a document has its symbol, linked to doc_url in a new tab." — table rows do; sample cards: symbol linked too. Check lists show symbol (link? make them links too where doc_url known — in failures list, plain text ok, but let me link symbols in sample cards and table; check lists plain).

Also "FIG.01 ... Clicking a bar adds that theme as a filter chip" — done.

Header hint "dated by document" — in meta line. Good.

Let me also double check the state regex against "(Venezuela (Bolivarian Republic of))": run regex `((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$` — matches "(Venezuela (Bolivarian Republic of))" since inner `\([^()]*\)` matches "(Bolivarian Republic of)". Groups regex finds the whole. inner = "Venezuela (Bolivarian Republic of)" — no comma, length ok → accepted as one state name with nested parens. Good, per plan.

"(Cabo Verde) (Slovenia) (Togo);" — run matches all three groups + ";". Split gives 3. Good.

Treaty-body "(art. 15)." — not UPR, skipped. Good.

Now, about `hi()` on first line and full text: words from keyword. Implementation:
```js
function hi(text){
  const words=state.filters.keyword.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if(!words.length) return esc(text);
  const rx=new RegExp("("+words.map(w=>w.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")).join("|")+")","gi");
  return String(text).split(rx).map(p=>{ if(!p) return ""; const low=p.toLowerCase(); return words.some(w=>low.indexOf(w)!==-1) ? "<mark>"+esc(p)+"</mark>" : esc(p); }).join("");
}
```

OK. Now assemble the whole HTML. Also add `<meta name="color-scheme" content="light">`? Not needed.

Tab buttons HTML:
```html
<nav class="tabs wrap" role="tablist" aria-label="Dashboard sections">
  <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 Overview</button>
  <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" tabindex="-1">02 Records</button>
  <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">03 Check</button>
  <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
</nav>
```
Uppercase via CSS text-transform.

Panels inside `.layout` main. Rail aside inside layout.

switchTab: set aria-selected, tabindex, hidden on panels; renderRail(); renderTab(i).

Also on tab switch to 0, charts rebuild (renderOverview handles).

Edge: renderOverview when panel hidden (initial tab 0 visible, fine).

Let me now also compute FILE_YMIN/YMAX from RECS.

Write detailHtml(r):
```js
function detailHtml(r){
  return '<td colspan="6">'
   +'<div class="paranum">'+(r._para? "para. "+esc(r._para) : "no paragraph number in this extract")+'</div>'
   +'<p class="fulltext">'+hi(r.text)+'</p>'
   + labelsHtml(r)
   +'<div class="rowactions"><button type="button" class="btn copybtn" data-id="'+esc(r.id)+'">'+(r._para?"Copy citation":"Copy citation (no paragraph number in this extract)")+'</button> '
   +'<a class="btn" href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">Open the UN document</a> '
   +'<span class="copied" hidden>Copied ✓</span></div>'
   +'</td>';
}
```

labelsHtml as above with .lbl spans.

CSS for .labels div margins, .lbl monospace uppercase 10px color #57534a margin-right 8px, .missing italic color #8a8375.

Now sizes: this will be long but let's write it.

One more: "aria-live polite" on matchNum — set attribute in HTML.

"Show 50 more" button label updates? Keep "Show 50 more".

Table caption id recCaption — caption element text.

Also the tab-02 search input placeholder updates with n.

Check: "the same box as 01 Keyword" — synced, yes.

Now let me also handle `D.built` maybe undefined — guard with `D.built||"unknown"`. And `D.source`, `D.source_url` guard.

Also `sdg_names` keys: use SDG_NAMES[String(g)].

SDG options: distinct goals: `const sdgSet=new Set(); RECS.forEach(r=>(r.sdgs||[]).forEach(g=>sdgSet.add(g)));` sorted numeric. label: g+" — "+(SDG_NAMES[String(g)]||"SDG "+g). Option value String(g).

State options: counts across all UPR RECS: for each r._states (excluding "State not found") count. Sort count desc then alpha. Label: name+" ("+count+")". Value name.

Body options: if f.mechanism!=="all": bodies of RECS with that mechanism; else all bodies. Counts from RECS (full file) within that scope. Label: body+" ("+count+")".

Type options: distinct types with counts.

Mechanism options: MECHS with counts.

Year options: YEARS map v=y label String(y).

Now write final code. Also include `role="tablist"` arrow nav; Home/End maybe. Fine with arrows.

Potential issue: `hidden` on panels + CSS `[hidden]{display:none!important}` — included.

Charts when panel hidden: we only build when tab 0 active. On filter change while on tab 0, rebuild. On switching to tab 0, renderTab(0) builds. When leaving tab 0, charts remain but panel hidden — Chart.js responsive may try resize on window resize with 0 size; to be safe, on switchTab away from 0, destroy charts. I'll add: if leaving tab 0, destroy chart1/chart2 and null them.

Let me write the code now, carefully and completely.

Also the "How this is computed" line near every chart/number — included as .how/.figsrc.

Footer sticky might overlap content — add padding-bottom on body/layout (60px) — done.

Let me write out the document.

Regarding line count: probably ~700-900 lines. Fine.

One more detail: the plan says tab 02 search field placeholder "Search n records, e.g. torture". Done.

"clicking the Date header reverses it" — implemented via button in th.

Also caption "newest first" — included.

Check panel heading "Check this dashboard" — plan says panel (section "How the app checks itself"). I'll title it "How the app checks itself" with intro line, and the sample section "Random-sample label check". The plan text: 'The "Check this dashboard" panel (section "How the app checks itself")'. I'll name the section "Check this dashboard — how the app checks itself". Fine.

Now writing. I'll be careful with template literals vs string concat — use concat or template literals; fine in single file. I'll use template literals for readability. Ensure no `</script>` sequence inside strings — avoid "</" patterns in JS strings? "</span>" inside template literals is fine except "</script>" — I won't have that.

Also careful: in HTML strings with quotes — use consistent quoting.

Let me draft the complete file:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UHRI · UN recommendations dashboard</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--muted:#57534a;}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{margin:0}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--rule);text-underline-offset:2px}
a:hover{text-decoration-color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header{padding:30px 0 0}
.kicker{font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--red)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:34px;line-height:1.18;margin:10px 0 8px;max-width:26em}
.meta{font:12px/1.7 ui-monospace,Menlo,Consolas,monospace;color:var(--muted);margin:0}
.tabs{display:flex;flex-wrap:wrap;gap:2px;border-bottom:1px solid var(--rule);margin-top:16px}
.tabs [role=tab]{font:12px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;background:none;border:none;border-bottom:3px solid transparent;padding:12px 14px 11px;cursor:pointer;color:var(--muted)}
.tabs [role=tab]:hover{color:var(--ink)}
.tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.layout{display:grid;grid-template-columns:272px minmax(0,1fr);gap:40px;align-items:start;padding:24px 0 70px}
/* rail */
.rail{position:sticky;top:14px}
.railhead{display:flex;justify-content:space-between;align-items:baseline;font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.mini{font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;background:none;border:none;color:var(--red);cursor:pointer;padding:2px 0;text-decoration:underline;text-underline-offset:2px}
.matchnum{font-family:Georgia,"Times New Roman",serif;font-size:54px;line-height:1;margin:12px 0 3px}
.matchsub{font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;color:var(--muted)}
.sharebar{height:4px;background:var(--rule);margin:10px 0 12px}
.sharebar i{display:block;height:100%;background:var(--red);width:0}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
.chip{font:11px/1 ui-monospace,Menlo,Consolas,monospace;border:1px solid var(--red);color:var(--red);background:none;padding:5px 8px;cursor:pointer;border-radius:2px}
.chip:hover{background:rgba(155,35,53,.08)}
.acc{border-top:1px solid var(--rule)}
.accbtn{width:100%;display:flex;justify-content:space-between;align-items:center;background:none;border:none;border-bottom:1px solid var(--rule);padding:13px 2px;cursor:pointer;font:12px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);text-align:left}
.accbtn .chev{color:var(--muted)}
.accbody{border-bottom:1px solid var(--rule);padding:12px 2px 16px}
.hint{font:11px/1.6 ui-monospace,Menlo,Consolas,monospace;color:var(--muted);margin:6px 0 0}
input[type=text],input[type=number],select{width:100%;background:#fffdf8;border:1px solid var(--rule);padding:8px 10px;font:14px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--ink);border-radius:0}
input:focus,select:focus{border-color:var(--red)}
label.f{display:block;font:10px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:14px 0 5px}
label.f:first-child{margin-top:0}
/* main */
.sect{font:12px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:34px 0 10px}
.sect:first-child{margin-top:0}
.tiles{display:flex;flex-wrap:wrap;gap:40px}
.tile .big{font-family:Georgia,"Times New Roman",serif;font-size:48px;line-height:1}
.tile .sub{font-size:14px;margin-top:7px;max-width:36ch}
.how{font:11px/1.6 ui-monospace,Menlo,Consolas,monospace;color:var(--muted);margin-top:7px;max-width:40ch}
.mechtiles{display:flex;flex-wrap:wrap;gap:32px;margin-top:22px;padding-top:18px;border-top:1px solid var(--rule)}
.mech .mname{font:12px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase}
.mech .dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:8px;vertical-align:baseline}
.mech .mnum{font-family:Georgia,serif;font-size:34px;line-height:1;margin-top:8px}
.mech .msub{font-size:13px;color:var(--muted);margin-top:5px;max-width:30ch}
.linkbtn{background:none;border:none;padding:0;font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--red);cursor:pointer;text-decoration:underline;text-underline-offset:2px;margin-top:6px}
.statesbox{margin-top:16px;border-top:1px solid var(--rule);padding-top:12px}
.statesbox h3{font-family:Georgia,serif;font-weight:400;font-size:19px;margin:0 0 8px}
.statesbox ol{margin:0;padding-left:22px;font-size:14px}
figure{margin:40px 0 0}
.figtitle{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:22px;line-height:1.3;margin:0 0 5px;max-width:44em}
.figsrc{font:11px/1.6 ui-monospace,Menlo,Consolas,monospace;color:var(--muted);margin:0 0 14px;max-width:70em}
.chartbox{height:360px;position:relative}
.chartbox.small{height:320px}
.norecords{font-size:15px;color:var(--muted);padding:26px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
/* tables */
table{width:100%;border-collapse:collapse;margin:12px 0 6px;font-size:15px}
caption{text-align:left;font:11px/1.6 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:0 0 8px;border-bottom:1px solid var(--ink)}
th{font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);text-align:left;padding:9px 12px 9px 0;border-bottom:1px solid var(--ink);font-weight:400;vertical-align:bottom}
td{padding:9px 12px 9px 0;border-bottom:1px solid var(--rule);vertical-align:top}
th.num,td.num{text-align:right}
.thbtn{background:none;border:none;padding:0;font:inherit;letter-spacing:inherit;text-transform:inherit;color:inherit;cursor:pointer;text-decoration:underline;text-underline-offset:2px}
tbody tr.data{cursor:pointer}
tbody tr.data:hover td{background:rgba(155,35,53,.05)}
td.firstline{max-width:34em}
tr.detail td{background:#ede7d9;padding:18px 20px}
.paranum{font-family:Georgia,serif;font-size:30px;color:var(--red);margin-bottom:10px}
.fulltext{max-width:78ch;white-space:pre-wrap;margin:0 0 14px}
.labels div{margin:5px 0;font-size:14px}
.lbl{font:10px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-right:10px}
.missing{color:#8a8375;font-style:italic}
.tagchip{display:inline-block;border:1px solid var(--rule);padding:2px 8px;margin:2px 4px 2px 0;font-size:12.5px;border-radius:2px;background:#fffdf8}
mark{background:rgba(155,35,53,.22);color:inherit;padding:0 1px}
.rowactions{display:flex;align-items:center;gap:10px;margin-top:14px;flex-wrap:wrap}
.btn{font:12px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;background:none;border:1px solid var(--rule);color:var(--ink);padding:9px 14px;cursor:pointer;border-radius:2px;text-decoration:none;display:inline-block}
.btn:hover{border-color:var(--ink)}
.btn.primary{border-color:var(--red);color:var(--red)}
.btn.primary:hover{background:rgba(155,35,53,.08)}
.btn[aria-pressed=true]{background:var(--red);border-color:var(--red);color:var(--paper)}
.copied{font:11px/1 ui-monospace,Menlo,Consolas,monospace;color:var(--red)}
.searchrow{margin-bottom:6px}
.searchrow input{font-size:16px}
/* checks */
.check{display:flex;gap:12px;padding:10px 0;border-bottom:1px solid var(--rule);font-size:14px}
.check .mark{font-family:ui-monospace,Menlo,Consolas,monospace;flex:none}
.check .what{font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.check.fail .mark,.check.fail .failtxt{color:var(--red);font-weight:700}
.check.warn .mark{color:var(--red)}
.failures{font:12px/1.7 ui-monospace,Menlo,Consolas,monospace;color:var(--muted);word-break:break-all}
.samplectl{display:flex;align-items:flex-end;gap:14px;flex-wrap:wrap;margin:8px 0 14px}
.samplectl label.f{margin:0;display:flex;align-items:center;gap:8px}
.samplectl input{width:100px}
.tally{font:12px/1.6 ui-monospace,Menlo,Consolas,monospace;color:var(--ink);margin:0 0 10px}
.samplecard{border-bottom:1px solid var(--rule)}
.samplebtn{width:100%;display:flex;justify-content:space-between;gap:12px;text-align:left;background:none;border:none;padding:11px 2px;cursor:pointer;font:13px/1.4 ui-monospace,Menlo,Consolas,monospace;color:var(--ink)}
.samplebtn:hover{color:var(--red)}
.samplebody{padding:2px 2px 18px}
.verdicts{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
/* method */
.method{margin:0;padding-left:22px;max-width:72ch}
.method li{margin:0 0 10px}
.srcblock{font-size:14px;max-width:72ch}
/* footer */
footer{position:sticky;bottom:0;background:var(--paper);border-top:1px solid var(--rule);padding:9px 0 10px;font:11px/1.7 ui-monospace,Menlo,Consolas,monospace;color:var(--muted)}
footer a{color:inherit}
.credits{opacity:.85}
@media (max-width:920px){
  .layout{grid-template-columns:1fr;gap:20px}
  .rail{position:static}
  h1{font-size:27px}
}
</style>
</head>
<body>
...
</body>
</html>
```

Now the body HTML:

```html
<header class="wrap">
  <div class="kicker" id="kicker">UHRI</div>
  <h1 id="title"></h1>
  <p class="meta" id="meta"></p>
  <nav class="tabs" role="tablist" aria-label="Dashboard sections" id="tablist">
    <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 Overview</button>
    <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" tabindex="-1">02 Records</button>
    <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">03 Check</button>
    <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
  </nav>
</header>
<div class="wrap layout">
  <aside class="rail" aria-label="Filters">
    <div class="railhead"><span>Filters</span><button class="mini" id="clearAll" type="button">Clear all</button></div>
    <div class="matchnum" id="matchNum" aria-live="polite">–</div>
    <div class="matchsub" id="matchSub"></div>
    <div class="sharebar" aria-hidden="true"><i id="shareFill"></i></div>
    <div class="chips" id="chips"></div>
    <div id="accWrap">
      <div class="acc">
        <button class="accbtn" type="button" data-acc="kw" aria-expanded="true" aria-controls="acc-kw"><span>01 Keyword</span><span class="chev" aria-hidden="true">▾</span></button>
        <div class="accbody" id="acc-kw">
          <input type="text" id="kw1" placeholder="e.g. torture" aria-label="Keyword search">
          <p class="hint">literal match, not synonyms · every word must appear in the text or symbol · applied 300 ms after typing</p>
        </div>
      </div>
      <div class="acc">
        <button class="accbtn" type="button" data-acc="mech" aria-expanded="false" aria-controls="acc-mech"><span>02 Mechanism, body, type</span><span class="chev" aria-hidden="true">▾</span></button>
        <div class="accbody" id="acc-mech" hidden>
          <label class="f" for="selMech">Mechanism</label>
          <select id="selMech"></select>
          <label class="f" for="selBody">Body or mandate</label>
          <select id="selBody"></select>
          <label class="f" for="selType">Type</label>
          <select id="selType"></select>
          <label class="f" for="selState">Recommending State (UPR only)</label>
          <select id="selState"></select>
        </div>
      </div>
      <div class="acc">
        <button class="accbtn" type="button" data-acc="yr" aria-expanded="false" aria-controls="acc-yr"><span>03 Years and SDG</span><span class="chev" aria-hidden="true">▾</span></button>
        <div class="accbody" id="acc-yr" hidden>
          <label class="f" for="selYf">Year from</label>
          <select id="selYf"></select>
          <label class="f" for="selYt">Year to</label>
          <select id="selYt"></select>
          <label class="f" for="selSdg">SDG</label>
          <select id="selSdg"></select>
        </div>
      </div>
    </div>
  </aside>
  <main>
    <section id="panel-0" role="tabpanel" aria-labelledby="tab-0">
      <div class="tiles" id="tiles"></div>
      <div class="mechtiles" id="mechTiles"></div>
      <div class="statesbox" id="statesBox" hidden></div>
      <figure>
        <figcaption>
          <p class="figtitle" id="fig1Title"></p>
          <p class="figsrc" id="fig1Src"></p>
        </figcaption>
        <div class="chartbox" id="fig1Box"><canvas id="chart1" aria-label="Bar chart of the ten most frequent themes"></canvas></div>
        <div class="norecords" id="fig1Empty" hidden>No records match the current filters.</div>
        <table id="fig1Table">
          <caption>FIG.01 data — the same ten rows as the chart</caption>
          <thead><tr><th>Theme</th><th class="num">Records</th><th class="num">% of filtered</th><th>Years</th></tr></thead>
          <tbody id="fig1Body"></tbody>
        </table>
        <p class="hint" id="fig1Note"></p>
      </figure>
      <figure>
        <figcaption>
          <p class="figtitle" id="fig2Title"></p>
          <p class="figsrc" id="fig2Src"></p>
        </figcaption>
        <div class="chartbox small" id="fig2Box"><canvas id="chart2" aria-label="Stacked bar chart of records per year by mechanism"></canvas></div>
        <div class="norecords" id="fig2Empty" hidden>No records match the current filters.</div>
      </figure>
    </section>
    <section id="panel-1" role="tabpanel" aria-labelledby="tab-1" hidden>
      <div class="searchrow">
        <input type="text" id="kw2" aria-label="Keyword search (same as the filter in the left rail)">
        <p class="hint">literal match, not synonyms · same box as 01 Keyword in the filters</p>
      </div>
      <table id="recTable">
        <caption id="recCaption"></caption>
        <thead><tr>
          <th><button class="thbtn" type="button" id="dateSort">Date <span id="dateArrow" aria-hidden="true">↓ newest first</span></button></th>
          <th>Body</th><th>Symbol</th><th>Para.</th><th>First line</th><th>Recommending State</th>
        </tr></thead>
        <tbody id="recBody"></tbody>
      </table>
      <div class="norecords" id="recEmpty" hidden>No records match the current filters.</div>
      <p><button class="btn" type="button" id="showMore">Show 50 more</button></p>
    </section>
    <section id="panel-2" role="tabpanel" aria-labelledby="tab-2" hidden>
      <h2 class="sect">Check this dashboard — how the app checks itself</h2>
      <p class="hint">Each line compares two values computed in this page. Failures are shown in red, never hidden.</p>
      <div id="checkList"></div>
      <h2 class="sect">Random-sample label check</h2>
      <p class="hint">This is your judgement of the UN's labels; nothing is sent anywhere.</p>
      <div class="samplectl">
        <button class="btn primary" type="button" id="drawBtn">Check 10 at random</button>
        <label class="f" for="seedBox">Seed <input type="number" id="seedBox" value="1" min="0" step="1"></label>
        <button class="btn" type="button" id="drawSeed">Draw with this seed</button>
        <button class="btn" type="button" id="drawAgain">Draw again</button>
      </div>
      <p class="tally" id="tally"></p>
      <div id="sampleList"></div>
    </section>
    <section id="panel-3" role="tabpanel" aria-labelledby="tab-3" hidden>
      <h2 class="sect">How each number is computed</h2>
      <ol class="method">
        <li>Every number on this page is computed in your browser by looping over the records of the attached UHRI file. Nothing is estimated, and no model, server or network request is involved.</li>
        <li>The headline count is the number of records passing all filters; documents are the distinct <em>symbol</em> values; years are the minimum and maximum of <em>year</em> among those records.</li>
        <li>Filters combine with AND: every keyword word must appear literally in the text or the symbol; mechanism, body, type and recommending State match exactly; years are inclusive between the two selects; an SDG matches when its goal number is in the record's <em>sdgs</em> list; a theme matches when the record carries it.</li>
        <li>Paragraph numbers are read from the first number at the start of the text (for example “71.” or “144.43”); recommending States are read from the trailing parentheses of UPR records only, never from treaty-body texts.</li>
        <li>Theme counts count each theme once per record, so the ten bars add up to more than the record count; percentages are shares of the filtered records, not of labels.</li>
        <li>The CSV export contains exactly the filtered records, with the columns you see on the Records tab plus the full text and all labels, generated in the browser.</li>
      </ol>
      <h2 class="sect">Take it with you</h2>
      <p>
        <button class="btn primary" type="button" id="csvBtn">Download CSV of the current filter</button>
        <button class="btn" type="button" id="sumBtn">Copy summary</button>
        <span class="copied" id="sumCopied" hidden>Copied ✓</span>
      </p>
      <p class="hint">The CSV starts with comment lines (country, source, build date, filters, row count) and is generated in the browser with a Blob URL. Copy summary writes plain text to the clipboard — the only thing that leaves the page.</p>
      <h2 class="sect">Source</h2>
      <p class="srcblock" id="srcLine"></p>
    </section>
  </main>
</div>
<footer>
  <div class="wrap" id="footLine"></div>
  <div class="wrap credits">Credits: chart and table practice after UK Government Analysis Function guidance (data visualisation: charts; tables); citation form after Dag Hammarskjöld Library Ask DAG; data practice after the OHCHR guidance note A Human Rights-Based Approach to Data.</div>
</footer>
<script>
... all JS ...
</script>
```

Now the JS. Let me write it fully:

```js
(function(){
"use strict";
var D = window.WORKSHOP_DATA.uhri;
var COUNTRY = D.country || "the participant country";
var SDG_NAMES = D.sdg_names || {};
var BUILT = D.built || "unknown";
var SOURCE = D.source || "OHCHR Universal Human Rights Index";
var SOURCE_URL = D.source_url || "";

/* --- prepare records --- */
var RECS = D.records;
var byId = {};
RECS.forEach(function(r, i){
  r._i = i;
  var m = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/.exec(r.text || "");
  r._para = m ? m[1] : null;
  r._states = [];
  if (r.mechanism === "Universal Periodic Review") {
    var run = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/.exec(r.text || "");
    if (run) {
      var groups = run[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
      var names = groups.map(function(g){ return g.slice(1, -1).trim(); });
      var bad = names.some(function(n){ return n.indexOf(",") !== -1 || n.length > 60; });
      r._states = bad ? ["State not found"] : names;
    }
  }
  var t = String(r.text || "");
  r._first = t.length <= 120 ? t : (function(){ var c = t.slice(0,120); var sp = c.lastIndexOf(" "); if (sp > 0) c = c.slice(0, sp); return c + "…"; })();
  byId[r.id] = r;
});
var YEARS = Array.from(new Set(RECS.map(function(r){ return r.year; }))).sort(function(a,b){ return a-b; });
var FILE_YMIN = YEARS[0], FILE_YMAX = YEARS[YEARS.length-1];
var MECHS = Array.from(new Set(RECS.map(function(r){ return r.mechanism; })));
var MEC_COLORS = { "Universal Periodic Review":"#c2410c", "Treaty bodies":"#0f766e", "Special Procedures":"#7c3aed" };
```

Helpers, state, filtered, themeStats, etc. Then rendering functions. Then init.

I'll write with modern JS (const/let, arrow) — fine.

Let me now also decide: `render()` calls renderRail + renderTab(state.tab). renderTab dispatch.

Potential recursion: setFilter → render → renderRail → fillSelect assigns f values from selects — no events fired programmatically, fine.

One catch: in renderRail I assign `f.mechanism = fillSelect(...)` — but fillSelect returns el.value which is string; yf/yt are numbers — year option values are strings; I set f.yf = Number(...). Handle: after fillSelect for years, convert: `f.yf = Number(f.yf); f.yt = Number(f.yt);` then swap if needed and set select values.

Also sdg value string; filtered() uses Number(f.sdg). OK.

Chips reset: resetFilter(k):
```js
function resetFilter(k){
  var f = state.filters;
  if(k==="keyword"){ f.keyword=""; $("#kw1").value=""; $("#kw2").value=""; }
  else if(k==="years"){ f.yf=FILE_YMIN; f.yt=FILE_YMAX; }
  else f[k]="all";
  state.shown=50; redrawSample(); render();
}
```

setFilter:
```js
function setFilter(k,v){ state.filters[k]=v; state.shown=50; redrawSample(); render(); }
```

redrawSample:
```js
function redrawSample(){
  if(!state.sampleIds) return;
  var f=filtered(); var rnd=mulberry32(state.sampleSeed>>>0);
  var idx=f.map(function(_,i){return i;});
  for(var i=idx.length-1;i>0;i--){ var j=Math.floor(rnd()*(i+1)); var t=idx[i]; idx[i]=idx[j]; idx[j]=t; }
  state.sampleIds=idx.slice(0,Math.min(10,idx.length)).map(function(i){ return f[i].id; });
  state.sampleOpen=null;
}
```

mulberry32:
```js
function mulberry32(a){ return function(){ a|=0; a=a+0x6D2B79F5|0; var t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
```

Now renderRail:

```js
function renderRail(){
  var f=state.filters;
  var m=filtered().length, all=RECS.length;
  $("#matchNum").textContent=fmt(m);
  $("#matchSub").textContent="matching records · of "+fmt(all)+" in the file";
  $("#shareFill").style.width=(all? Math.max(0,100*m/all):0)+"%";
  /* chips */
  var chips=[];
  if(f.keyword.trim()) chips.push({k:"keyword",label:'Keyword "'+f.keyword.trim()+'"'});
  if(f.mechanism!=="all") chips.push({k:"mechanism",label:"Mechanism: "+f.mechanism});
  if(f.body!=="all") chips.push({k:"body",label:"Body: "+f.body});
  if(f.type!=="all") chips.push({k:"type",label:"Type: "+f.type});
  if(f.state!=="all") chips.push({k:"state",label:"State: "+f.state});
  if(f.theme!=="all") chips.push({k:"theme",label:"Theme: "+f.theme});
  if(Number(f.yf)!==FILE_YMIN||Number(f.yt)!==FILE_YMAX) chips.push({k:"years",label:"Years: "+f.yf+"–"+f.yt});
  if(f.sdg!=="all") chips.push({k:"sdg",label:"SDG: "+f.sdg});
  var cb=$("#chips"); cb.innerHTML="";
  chips.forEach(function(c){
    var b=document.createElement("button"); b.type="button"; b.className="chip";
    b.textContent=c.label+"  ×"; b.setAttribute("aria-label","Remove filter "+c.label);
    b.addEventListener("click",function(){ resetFilter(c.k); });
    cb.appendChild(b);
  });
  /* accordions */
  $("#accWrap").hidden = state.tab>=2;
  document.querySelectorAll(".accbtn").forEach(function(btn){
    var open = state.openAcc===btn.dataset.acc;
    btn.setAttribute("aria-expanded", open?"true":"false");
    btn.querySelector(".chev").textContent = open?"▴":"▾";
    $("#acc-"+btn.dataset.acc).hidden = !open;
  });
  /* selects */
  var mechOpts=[{v:"all",label:"All mechanisms ("+fmt(all)+")"}].concat(MECHS.map(function(m){ return {v:m,label:m+" ("+fmt(countBy(RECS,function(r){return r.mechanism;})[m]||0)+")"}; }));
```
Hmm countBy each time — compute once outside. Let me precompute global count maps: BY_MECH, BY_BODY, BY_TYPE, BY_YEAR, BY_STATE (UPR states), SDG set. Precompute at init:

```js
var BY_MECH=countBy(RECS,r=>r.mechanism);
var BY_BODY=countBy(RECS,r=>r.body);
var BY_TYPE=countBy(RECS,r=>r.type);
var BY_STATE={};
RECS.forEach(function(r){ if(r.mechanism==="Universal Periodic Review"){ r._states.forEach(function(s){ if(s!=="State not found") BY_STATE[s]=(BY_STATE[s]||0)+1; }); } });
var SDG_SET=new Set(); RECS.forEach(function(r){ (r.sdgs||[]).forEach(function(g){ SDG_SET.add(g); }); });
```

Body options depend on mechanism:
```js
var scope = f.mechanism==="all" ? RECS : RECS.filter(r=>r.mechanism===f.mechanism);
var bodies = Array.from(new Set(scope.map(r=>r.body))).sort();
var bodyOpts=[{v:"all",label:"All bodies ("+fmt(scope.length)+")"}].concat(bodies.map(b=>({v:b,label:b+" ("+fmt((scope.filter(r=>r.body===b)).length)+")"})));
```
O(n^2)-ish but n small (2-3k, bodies 16) fine. Better: count within scope via countBy(scope,...). Use that.

Type opts: distinct types sorted with BY_TYPE counts.
State opts: entries of BY_STATE sorted count desc then name; label name+" ("+count+")".
Year opts: YEARS.
SDG opts: sorted SDG_SET numbers; label g+" — "+(SDG_NAMES[String(g)]||("SDG "+g)).

fillSelect as described; then:
```js
f.mechanism=fillSelect($("#selMech"),mechOpts,f.mechanism);
f.body=fillSelect($("#selBody"),bodyOpts,f.body);
f.type=fillSelect($("#selType"),typeOpts,f.type);
f.state=fillSelect($("#selState"),stateOpts,f.state);
f.yf=Number(fillSelect($("#selYf"),yearOpts,f.yf));
f.yt=Number(fillSelect($("#selYt"),yearOpts,f.yt));
f.sdg=fillSelect($("#selSdg"),sdgOpts,f.sdg);
if(f.yf>f.yt){ var t=f.yf; f.yf=f.yt; f.yt=t; $("#selYf").value=String(f.yf); $("#selYt").value=String(f.yt); }
```

Wait: fillSelect(el, opts, cur) sets el.value=cur if present else opts[0].v and returns el.value. But if cur is number for years, compare String. I'll make fillSelect compare String(o.v)===String(cur). Return el.value (string). OK.

Edge: when mechanism changes, body options change; f.body may not exist → fillSelect resets to "all" and returns "all" → f.body="all". Good.

renderOverview:

```js
var chart1=null, chart2=null;
function renderOverview(){
  var f=filtered(), n=f.length;
  var byType=countBy(f,function(r){return r.type;});
  var docs=new Set(f.map(function(r){return r.symbol;})).size;
  var ys=f.map(function(r){return r.year;});
  var ymin=ys.length?Math.min.apply(null,ys):null, ymax=ys.length?Math.max.apply(null,ys):null;
  var tiles=$("#tiles"); tiles.innerHTML="";
  function tile(big,sub,how){ var d=document.createElement("div"); d.className="tile"; d.innerHTML='<div class="big">'+big+'</div><div class="sub">'+sub+'</div><div class="how">'+how+'</div>'; return d; }
  tiles.appendChild(tile(fmt(n),
    "records in the current filter — "+Object.keys(byType).map(function(t){return esc(t)+" "+fmt(byType[t]);}).join(" · "),
    "How this is computed: count of records passing every filter, all types included; "+fmt(RECS.length)+" records in the file."));
  tiles.appendChild(tile(fmt(docs),"documents (distinct symbol)","How this is computed: number of distinct symbol values among the filtered records."));
  tiles.appendChild(tile(n? ymin+"–"+ymax : "—","years covered (min–max of year)","How this is computed: min and max of year among the filtered records; the file spans "+FILE_YMIN+"–"+FILE_YMAX+"."));
  /* mechanism tiles */
  var mt=$("#mechTiles"); mt.innerHTML="";
  MECHS.forEach(function(m){
    var sub=f.filter(function(r){return r.mechanism===m;});
    var mdocs=new Set(sub.map(function(r){return r.symbol;})).size;
    var mys=sub.map(function(r){return r.year;});
    var latest=mys.length?Math.max.apply(null,mys):null;
    var share=n? (100*sub.length/n).toFixed(1) : "0.0";
    var d=document.createElement("div"); d.className="mech";
    d.innerHTML='<div class="mname"><span class="dot" style="background:'+(MEC_COLORS[m]||"#6b6459")+'"></span>'+esc(m)+'</div>'
      +'<div class="mnum">'+fmt(sub.length)+'</div>'
      +'<div class="msub">'+fmt(mdocs)+' documents · latest '+latest+' · '+share+'% of filtered</div>'
      +'<div class="how">How this is computed: filtered records with mechanism = '+esc(m)+'.</div>'
      +(m==="Universal Periodic Review" ? '<button class="linkbtn" type="button" id="statesLink">'+(state.showStates?"hide the States":"see the States")+'</button>' : '');
    mt.appendChild(d);
  });
  /* states box */
  var sb=$("#statesBox");
  if(state.showStates){
    var upr=f.filter(function(r){return r.mechanism==="Universal Periodic Review";});
    var sc={}; upr.forEach(function(r){ r._states.forEach(function(s){ if(s!=="State not found") sc[s]=(sc[s]||0)+1; }); });
    var top=Object.keys(sc).map(function(s){return {s:s,c:sc[s]};}).sort(function(a,b){ return b.c-a.c || a.s.localeCompare(b.s); }).slice(0,10);
    sb.innerHTML="<h3>Ten States that made most recommendations to "+esc(COUNTRY)+" · current filter</h3>"
      +(top.length? "<ol>"+top.map(function(t){return "<li>"+esc(t.s)+" — "+fmt(t.c)+" recommendations</li>";}).join("")+"</ol>"
        : "<p class='hint'>No UPR records in the current filter.</p>")
      +"<p class='hint'>How this is computed: UPR records in the filter, each counted once per State named in its trailing parentheses. A count of recommendations, not of influence; two States can co-sponsor one line.</p>";
    sb.hidden=false;
  } else sb.hidden=true;
  /* FIG.01 */
  var top10=themeStats(f).slice(0,10);
  $("#fig1Title").textContent="FIG.01 · Ten most frequent themes among "+fmt(n)+" filtered records";
  $("#fig1Src").textContent="Source: UHRI records, current filter · click a bar to filter by that theme · a record can carry several themes, so counts add up to more than "+fmt(n);
  if(n===0){
    $("#fig1Box").hidden=true; $("#fig1Empty").hidden=false; $("#fig1Body").innerHTML=""; $("#fig1Note").textContent="";
    if(chart1){chart1.destroy(); chart1=null;}
  } else {
    $("#fig1Box").hidden=false; $("#fig1Empty").hidden=true;
    if(chart1) chart1.destroy();
    chart1=new Chart($("#chart1").getContext("2d"), {...});
    $("#fig1Body").innerHTML=top10.map(function(t){
      return "<tr><td>"+esc(t.theme)+"</td><td class='num'>"+fmt(t.count)+"</td><td class='num'>"+(100*t.count/n).toFixed(1)+"%</td><td>"+t.ymin+"–"+t.ymax+"</td></tr>";
    }).join("");
    $("#fig1Note").textContent="Percentages are of the "+fmt(n)+" filtered records, not of labels; ties are alphabetical. Years = first–last year of the filtered records carrying the theme.";
  }
  /* FIG.02 */
  $("#fig2Title").textContent="FIG.02 · Records per year by mechanism · "+fmt(n)+" filtered records";
  $("#fig2Src").textContent="Source: UHRI records, current filter · every year from "+FILE_YMIN+" to "+FILE_YMAX+" is shown, so empty years appear as gaps · dated by document";
  if(n===0){ $("#fig2Box").hidden=true; $("#fig2Empty").hidden=false; if(chart2){chart2.destroy(); chart2=null;} }
  else {
    $("#fig2Box").hidden=false; $("#fig2Empty").hidden=true;
    if(chart2) chart2.destroy();
    var yAll=[]; for(var y=FILE_YMIN;y<=FILE_YMAX;y++) yAll.push(y);
    var datasets=MECHS.map(function(m){
      return {label:m, stack:"s", backgroundColor:MEC_COLORS[m]||"#6b6459",
        data:yAll.map(function(yy){ return f.filter(function(r){ return r.year===yy && r.mechanism===m; }).length; })};
    });
    chart2=new Chart($("#chart2").getContext("2d"), {type:"bar", data:{labels:yAll.map(String), datasets:datasets}, options:{responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, grid:{display:false}, ticks:{font:{family:"ui-monospace,Menlo,Consolas,monospace",size:11}}}, y:{stacked:true, beginAtZero:true, ticks:{precision:0, font:{family:"ui-monospace,Menlo,Consolas,monospace",size:11}}, grid:{color:"#e7e0d2"}}}, plugins:{legend:{position:"bottom", labels:{usePointStyle:true, pointStyle:"rect", font:{size:12}}}}}});
  }
}
```

Chart1 config with bar value plugin:

```js
var barValuePlugin={ id:"barValue", afterDatasetsDraw:function(chart){
  var ctx=chart.ctx, meta=chart.getDatasetMeta(0);
  ctx.save(); ctx.font='12px ui-monospace, Menlo, Consolas, monospace'; ctx.fillStyle="#1d1b18"; ctx.textBaseline="middle";
  meta.data.forEach(function(bar,i){ var v=chart.data.datasets[0].data[i]; ctx.fillText(fmt(v), bar.x+6, bar.y); });
  ctx.restore();
}};
chart1=new Chart($("#chart1").getContext("2d"), {
  type:"bar",
  data:{labels:top10.map(function(t){return t.theme;}), datasets:[{label:"records", data:top10.map(function(t){return t.count;}), backgroundColor:"rgba(155,35,53,0.8)", borderWidth:0, maxBarThickness:34}]},
  options:{indexAxis:"y", responsive:true, maintainAspectRatio:false,
    onClick:function(e,els){ if(els.length){ setFilter("theme", top10[els[0].index].theme); } },
    scales:{
      x:{beginAtZero:true, suggestedMax:Math.max.apply(null,top10.map(function(t){return t.count;}))*1.18+1, grid:{color:"#e7e0d2"}, border:{color:"#d9d2c3"}, ticks:{font:{family:"ui-monospace,Menlo,Consolas,monospace",size:11}}},
      y:{grid:{display:false}, border:{color:"#d9d2c3"}, ticks:{font:{size:13}}}
    },
    plugins:{legend:{display:false}, tooltip:{callbacks:{label:function(c){ return " "+fmt(c.parsed.x)+" records"; }}}}
  },
  plugins:[barValuePlugin]
});
```

renderRecords as planned.

renderChecks + renderSample as planned.

renderMethod: only srcLine fill (static otherwise):
```js
function renderMethod(){
  $("#srcLine").innerHTML="Source: <a href='"+esc(SOURCE_URL)+"' target='_blank' rel='noopener'>"+esc(SOURCE)+"</a> · built "+esc(BUILT)+" · "+fmt(RECS.length)+" records for "+esc(COUNTRY)+" · terms of use as stated on the source page. The file holds one country; no other country is compared.";
}
```

Init:
```js
function init(){
  $("#kicker").textContent="UHRI · "+COUNTRY.toUpperCase();
  $("#title").textContent="UN human rights recommendations and observations: "+COUNTRY;
  var docs=new Set(RECS.map(function(r){return r.symbol;})).size;
  $("#meta").innerHTML="Source: <a href='"+esc(SOURCE_URL)+"' target='_blank' rel='noopener'>"+esc(SOURCE)+"</a> · "+fmt(RECS.length)+" records · "+fmt(docs)+" documents · "+FILE_YMIN+"–"+FILE_YMAX+" · built "+esc(BUILT)+" · dated by document";
  $("#footLine").innerHTML="Built on OHCHR UHRI data · "+fmt(RECS.length)+" records · <a href='"+esc(SOURCE_URL)+"' target='_blank' rel='noopener'>"+esc(SOURCE)+"</a>";
  /* tabs */
  var tablist=$("#tablist");
  tablist.addEventListener("click",function(e){ var b=e.target.closest("[role=tab]"); if(b) switchTab(Number(b.id.slice(4))); });
  tablist.addEventListener("keydown",function(e){
    if(e.key!=="ArrowRight"&&e.key!=="ArrowLeft") return;
    e.preventDefault();
    var i=state.tab+(e.key==="ArrowRight"?1:-1); i=(i+4)%4;
    switchTab(i); $("#tab-"+i).focus();
  });
  /* accordions */
  document.querySelectorAll(".accbtn").forEach(function(btn){
    btn.addEventListener("click",function(){ state.openAcc = state.openAcc===btn.dataset.acc ? null : btn.dataset.acc; renderRail(); });
  });
  $("#clearAll").addEventListener("click",function(){
    var f=state.filters;
    f.keyword=""; f.mechanism="all"; f.body="all"; f.type="all"; f.state="all"; f.theme="all"; f.sdg="all"; f.yf=FILE_YMIN; f.yt=FILE_YMAX;
    $("#kw1").value=""; $("#kw2").value="";
    state.shown=50; redrawSample(); render();
  });
  /* keyword inputs */
  bindKw($("#kw1")); bindKw($("#kw2"));
  /* selects */
  $("#selMech").addEventListener("change",function(e){ setFilter("mechanism",e.target.value); });
  ... etc
  /* records tab */
  $("#dateSort").addEventListener("click",function(){ state.sortAsc=!state.sortAsc; $("#dateArrow").textContent=state.sortAsc?"↑ oldest first":"↓ newest first"; renderTab(1); });
  $("#showMore").addEventListener("click",function(){ state.shown+=50; renderTab(1); });
  $("#recBody").addEventListener("click", recBodyClick);
  $("#recBody").addEventListener("keydown", recBodyKey);
  $("#mechTiles").addEventListener("click",function(e){ if(e.target.id==="statesLink"){ state.showStates=!state.showStates; renderTab(0); } });
  /* sample */
  $("#drawBtn").addEventListener("click",function(){ state.sampleSeed=parseInt($("#seedBox").value,10)||1; drawSample(); });
  $("#drawSeed").addEventListener("click",function(){ state.sampleSeed=parseInt($("#seedBox").value,10)||1; drawSample(); });
  $("#drawAgain").addEventListener("click",function(){ state.sampleSeed=Math.floor(Math.random()*1000000); $("#seedBox").value=state.sampleSeed; drawSample(); });
  $("#sampleList").addEventListener("click",function(e){ var b=e.target.closest(".verdict"); if(!b) return; state.verdicts[state.sampleSeed+"|"+b.dataset.id]=b.dataset.v; renderTab(2); });
  /* export */
  $("#csvBtn").addEventListener("click",downloadCSV);
  $("#sumBtn").addEventListener("click",function(){ copyText(summaryText(),function(){ var s=$("#sumCopied"); s.hidden=false; setTimeout(function(){s.hidden=true;},2000); }); });
  render();
}
```

switchTab:
```js
function switchTab(i){
  state.tab=i;
  for(var k=0;k<4;k++){
    $("#tab-"+k).setAttribute("aria-selected", k===i?"true":"false");
    $("#tab-"+k).tabIndex = k===i?0:-1;
    $("#panel-"+k).hidden = k!==i;
  }
  if(i!==0 && chart1){ chart1.destroy(); chart1=null; }
  if(i!==0 && chart2){ chart2.destroy(); chart2=null; }
  renderRail(); renderTab(i);
}
```

renderTab:
```js
function renderTab(i){
  if(i===0) renderOverview();
  else if(i===1) renderRecords();
  else if(i===2) renderChecks();
  else renderMethod();
}
function render(){ renderRail(); renderTab(state.tab); }
```

recBodyClick:
```js
function recBodyClick(e){
  var copy=e.target.closest(".copybtn");
  if(copy){
    var r=byId[copy.dataset.id];
    var cite=r._para ? r.symbol+", para. "+r._para : r.symbol;
    copyText(cite,function(){ var s=copy.parentElement.querySelector(".copied"); if(s){ s.hidden=false; setTimeout(function(){ s.hidden=true; },2000); } });
    return;
  }
  if(e.target.closest("a")) return;
  var tr=e.target.closest("tr.data");
  if(tr) toggleRow(tr.dataset.id);
}
function recBodyKey(e){
  if(e.key!=="Enter"&&e.key!==" ") return;
  var tr=e.target.closest("tr.data");
  if(tr){ e.preventDefault(); toggleRow(tr.dataset.id); }
}
function toggleRow(id){
  if(state.expanded.has(id)) state.expanded.delete(id); else state.expanded.add(id);
  renderTab(1);
}
```

renderRecords:
```js
function renderRecords(){
  var f=filtered();
  var sorted=f.slice().sort(function(a,b){
    var d=state.sortAsc ? String(a.date).localeCompare(String(b.date)) : String(b.date).localeCompare(String(a.date));
    if(d) return d;
    var b2=String(a.body).localeCompare(String(b.body)); if(b2) return b2;
    var pa=a._para?parseFloat(a._para):Infinity, pb=b._para?parseFloat(b._para):Infinity;
    if(pa!==pb) return pa-pb;
    return a._i-b._i;
  });
  var shown=Math.min(state.shown, sorted.length);
  $("#recCaption").textContent = sorted.length
    ? "Showing "+fmt(shown)+" of "+fmt(sorted.length)+" matching records · "+(state.sortAsc?"oldest":"newest")+" first · click a row for the full paragraph"
    : "No records match the current filters.";
  $("#recEmpty").hidden = sorted.length>0;
  $("#showMore").hidden = shown>=sorted.length;
  $("#kw2").placeholder="Search "+fmt(sorted.length)+" records, e.g. torture";
  var tb=$("#recBody"); tb.innerHTML="";
  var frag=document.createDocumentFragment();
  sorted.slice(0,shown).forEach(function(r){
    var tr=document.createElement("tr");
    tr.className="data"; tr.tabIndex=0; tr.dataset.id=r.id;
    tr.setAttribute("aria-expanded", state.expanded.has(r.id)?"true":"false");
    tr.innerHTML="<td>"+esc(r.date)+"</td><td>"+esc(r.body)+"</td>"
      +"<td><a href='"+esc(r.doc_url)+"' target='_blank' rel='noopener'>"+esc(r.symbol)+"</a></td>"
      +"<td>"+(r._para?esc(r._para):"—")+"</td>"
      +"<td class='firstline'>"+hi(r._first)+"</td>"
      +"<td>"+stateCell(r)+"</td>";
    frag.appendChild(tr);
    var dt=document.createElement("tr");
    dt.className="detail"; dt.dataset.id=r.id; dt.hidden=!state.expanded.has(r.id);
    dt.innerHTML=detailHtml(r);
    frag.appendChild(dt);
  });
  tb.appendChild(frag);
}
function stateCell(r){
  if(r.mechanism!=="Universal Periodic Review") return "—";
  return r._states.length ? esc(r._states.join(" · ")) : "State not found";
}
```

runChecks — write fully:

```js
function runChecks(){
  var checks=[]; var n=RECS.length;
  checks.push({name:"Record count", detail:"records.length = "+fmt(n)+" vs Number(count) = "+fmt(Number(D.count)), pass:n===Number(D.count)});
  function sum(o){ return Object.keys(o).map(function(k){return o[k];}).reduce(function(a,b){return a+b;},0); }
  var bm=countBy(RECS,function(r){return r.mechanism;});
  var bb=countBy(RECS,function(r){return r.body;});
  var by=countBy(RECS,function(r){return r.year;});
  checks.push({name:"Partitions: mechanism, body, year", detail:"sums "+fmt(sum(bm))+", "+fmt(sum(bb))+", "+fmt(sum(by))+" vs "+fmt(n)+" records", pass:sum(bm)===n&&sum(bb)===n&&sum(by)===n});
  var bt=countBy(RECS,function(r){return r.type;});
  checks.push({name:"Type partition", detail:"counts per type sum to "+fmt(sum(bt))+" vs "+fmt(n), pass:sum(bt)===n});
  /* chart vs table */
  var f=filtered();
  var a=themeStats(f).slice(0,10);
  var b={}; f.forEach(function(r){ (r.themes||[]).forEach(function(t){ b[t]=(b[t]||0)+1; }); });
  var bTop=Object.keys(b).map(function(t){return {theme:t,count:b[t]};}).sort(function(x,y){ return y.count-x.count || x.theme.localeCompare(y.theme); }).slice(0,10);
  var same=a.length===bTop.length && a.every(function(t,i){ return t.theme===bTop[i].theme && t.count===bTop[i].count; });
  var largest=a.length?a[0].count:0;
  checks.push({name:"Chart against table (FIG.01)", detail:"top ten recomputed by a second loop: "+(same?"identical":"DIFFERENT")+"; largest bar "+fmt(largest)+" ≤ "+fmt(f.length)+" filtered records: "+(largest<=f.length?"yes":"no"), pass:same&&largest<=f.length});
  /* links */
  var badLinks=RECS.filter(function(r){
    try{
      var u=decodeURIComponent(r.doc_url).toLowerCase();
      return !(String(r.doc_url).indexOf("https://docs.un.org/")===0 && u.slice(-r.symbol.length)===r.symbol.toLowerCase());
    }catch(e){ return true; }
  });
  checks.push({name:"Links", detail:(n-badLinks.length)+" of "+fmt(n)+" doc_url values start with https://docs.un.org/ and end with the record's symbol (case-insensitive, decoded)", pass:badLinks.length===0,
    list:badLinks.slice(0,10).map(function(r){ return r.symbol+" → "+r.doc_url; }), more:Math.max(0,badLinks.length-10)});
  /* paragraph numbers */
  var pm={}; RECS.forEach(function(r){ var m=r.mechanism; pm[m]=pm[m]||{tot:0,found:0}; pm[m].tot++; if(r._para) pm[m].found++; });
  var upr=pm["Universal Periodic Review"];
  var uprWarn = !(upr && upr.found===upr.tot);
  checks.push({name:"Paragraph numbers found", detail:Object.keys(pm).map(function(m){ var v=pm[m]; return m+": "+v.found+"/"+v.tot+" ("+(100*v.found/v.tot).toFixed(1)+"%)"; }).join(" · ")+(uprWarn?" — UPR below 100%: warning, not an error":""), pass:true, warn:uprWarn});
  /* states */
  var uprRecs=RECS.filter(function(r){ return r.mechanism==="Universal Periodic Review"; });
  var noState=uprRecs.filter(function(r){ return !r._states.some(function(s){ return s!=="State not found"; }); });
  checks.push({name:"Recommending States found (UPR)", detail:fmt(uprRecs.length-noState.length)+" of "+fmt(uprRecs.length)+" UPR records have at least one State in the trailing parentheses", pass:noState.length===0,
    list:noState.slice(0,10).map(function(r){ var t=String(r.text||""); return r.symbol+" — trailing text: "+(t.length>90?"…"+t.slice(-90):t); }), more:Math.max(0,noState.length-10)});
  /* duplicates & gaps */
  var ids=new Set(RECS.map(function(r){return r.id;}));
  var tc=countBy(RECS,function(r){return r.text;});
  var dup=Object.keys(tc).filter(function(k){ return tc[k]>1; }).length;
  var noTh=RECS.filter(function(r){ return !(r.themes||[]).length; }).length;
  var noSdg=RECS.filter(function(r){ return !(r.sdgs||[]).length; }).length;
  var noAp=RECS.filter(function(r){ return !(r.affected_persons||[]).length; }).length;
  checks.push({name:"Duplicates and gaps", detail:"distinct id "+fmt(ids.size)+" vs "+fmt(n)+" records; duplicate text values "+dup+"; not labelled — themes "+fmt(noTh)+", sdgs "+fmt(noSdg)+", affected persons "+fmt(noAp), pass:ids.size===n});
  return checks;
}
```

renderChecks:
```js
function renderChecks(){
  var list=$("#checkList"); list.innerHTML="";
  runChecks().forEach(function(c){
    var div=document.createElement("div");
    div.className="check"+(c.pass?(c.warn?" warn":""):" fail");
    var mark=c.pass?(c.warn?"⚠":"✓"):"✗";
    var html='<span class="mark">'+mark+'</span><span><span class="what">'+esc(c.name)+'</span> — '+esc(c.detail);
    if(!c.pass) html+=' <span class="failtxt">CHECK FAILED</span>';
    if(c.list&&c.list.length) html+='<br><span class="failures">'+c.list.map(function(x){return esc(x);}).join("<br>")+(c.more>0?"<br>… and "+c.more+" more":"")+'</span>';
    html+='</span>';
    div.innerHTML=html;
    list.appendChild(div);
  });
  renderSample();
}
```

renderSample as planned.

downloadCSV, summaryText, filterDesc:
```js
function filterDesc(){
  var f=state.filters, parts=[];
  if(f.keyword.trim()) parts.push('keyword "'+f.keyword.trim()+'"');
  if(f.mechanism!=="all") parts.push("mechanism="+f.mechanism);
  if(f.body!=="all") parts.push("body="+f.body);
  if(f.type!=="all") parts.push("type="+f.type);
  if(f.state!=="all") parts.push("state="+f.state);
  if(f.theme!=="all") parts.push("theme="+f.theme);
  if(Number(f.yf)!==FILE_YMIN||Number(f.yt)!==FILE_YMAX) parts.push("years "+f.yf+"–"+f.yt);
  if(f.sdg!=="all") parts.push("SDG "+f.sdg);
  return parts.length? parts.join("; ") : "none (all records)";
}
```

summaryText with guard for n===0.

OK. Also `hi()` uses state keyword.

Also note: themeStats(f) returns array sorted; used in overview and checks.

Now double-check click budget & layout rules compliance... The plan is followed.

One more: "on 03 and 04 the rail keeps only the number, the bar and the chips" — accWrap hidden. Done.

"Every tab reads the same filtered set" — yes.

Header: "one line with the data's source, n and years" — meta line includes source, records, documents, years, built, dated by document. Good.

Also the tab-01 first tile: plan says "The first tile counts all records in the file" — my tile shows filtered count with "of N in the file" in how note and sub shows type breakdown. Hmm — to hew closer, maybe the big number should be the file total and the filtered count is in the rail? But then "Every tile and figure has a How this is computed note" and mechanism tiles show "share of the filtered set" — share of filtered set relative to what? If headline is file total, share of filtered set would be mech/filtered... confusing. The rail already shows matching count big. I think filtered count as headline is right ("among n filtered records" in FIG.01 title implies headline relates to filter). I'll keep filtered count but make the sub-line clearly say "of N in the file". Actually let me put "of "+fmt(RECS.length)+" in the file" into the sub line of tile 1: sub = type breakdown; how note includes "of N in the file". Good enough — and the rail number is the same value with aria-live.

Hmm, wait — re-reading once more: "A row of big serif numbers. The first tile counts **all records** in the file: recommendations, concerns/observations and any other `type`." I now think this means: the first tile counts all records (i.e., not only recommendations) — the bold emphasis is on "all records" vs just recommendations. With default filters, filtered = all records in file. So both readings coincide at default. Filtered-count is the consistent choice. Keep.

Now, "The Type filter (all / each type value present) starts on 'all'" — that's the rail select. Done.

Also plan: "Beside it: documents (distinct symbol) and years (min–max of year)" — tiles 2,3. Done.

Write detailHtml labelsHtml — done above.

Also add `rel="noopener"`.

Potential issue: `$("#chart1").getContext("2d")` each rebuild — fine after destroy.

Chart onClick uses `top10` closure — after re-render, new chart new closure. Good.

Also when n>0 but top10 empty (no themes at all in filtered) — chart with empty labels; guard: if top10.length===0 show fig1Empty? Plan: chart area shows "No records match" only when no records. If records exist but no themes, show empty chart + note "no themes labelled". I'll handle: if top10.length===0 → hide box, show a norecords div text "No themes are labelled on the matching records." Use fig1Empty with custom text. Implement: set fig1Empty.textContent accordingly.

Similarly FIG.02 always has years.

Edge: Math.max.apply(null, []) → -Infinity; guarded by n===0 branch and top10.length check.

Now assemble final answer: 1-3 sentences before code, then the html block, nothing after.

Let me also make sure I don't use any external resources — no fonts/CDN. Chart.js from window.Chart. Good.

Let me now write the complete final file text carefully, keeping syntax valid. I'll write it in one pass, being careful with quotes in JS strings containing HTML.

Also note: in `detailHtml`, `copy.parentElement.querySelector(".copied")` — the copied span is sibling of button inside .rowactions. Good.

In renderSample, verdict buttons data-id uses r.id which may contain quotes? ids are uuid-like; esc anyway in attribute: use esc(r.id). Fine.

One more: `bindKw` — after render(), rail inputs are static so not rebuilt; but renderRail's fillSelect rebuilds select options only when signature changes — good, focus preserved for selects not being changed.

But wait: renderRail is called on every render including after debounce typing; fillSelect compares signature; options unchanged → no rebuild; el.value=cur — setting el.value to same value doesn't blur. OK.

Also `$("#kw2")` placeholder updated in renderRecords only when tab 1 rendered; fine.

Potential subtle bug: in renderRail, `f.mechanism=fillSelect(...)` — fillSelect returns el.value; but if user just changed select, onchange fired setFilter with new value, then render → fillSelect(el, opts, f.mechanism) → cur present → el.value=cur. Good.

But there's an ordering issue: bodyOpts computed from f.mechanism before fillSelect of mechanism? I compute mechOpts, fill mechanism first, then compute bodyOpts using updated f.mechanism. Order in code: fill mech → compute bodyOpts from f.mechanism → fill body → type → state → years → sdg. Yes.

Also when mechanism changes via setFilter, body may become invalid; fillSelect resets to "all" and f.body updated — but the select's displayed value changes accordingly. Good.

Now, the `theme` filter isn't in any select — chip only. resetFilter("theme") sets "all". Good.

Let me also compute `themeStats`:
```js
function themeStats(f){
  var m={};
  f.forEach(function(r){
    (r.themes||[]).forEach(function(t){
      var e=m[t]||(m[t]={count:0,ymin:r.year,ymax:r.year});
      e.count++; if(r.year<e.ymin)e.ymin=r.year; if(r.year>e.ymax)e.ymax=r.year;
    });
  });
  return Object.keys(m).map(function(t){ var e=m[t]; return {theme:t,count:e.count,ymin:e.ymin,ymax:e.ymax}; })
    .sort(function(a,b){ return b.count-a.count || a.theme.localeCompare(b.theme); });
}
```

countBy:
```js
function countBy(list,fn){ var o={}; list.forEach(function(x){ var k=fn(x); o[k]=(o[k]||0)+1; }); return o; }
```

fmt: `function fmt(n){ return Number(n).toLocaleString("en-GB"); }`

esc as above.

OK, also the `hi` function and `firstLine` precomputed.

Time to write the final output. I'll write concise intro: "Built the four-tab UHRI dashboard for the attached file — overview with theme chart and timeline, records table with in-place expansion and citation copy, self-check panel with seeded random label sample, and method/CSV export. All numbers are computed in the browser from WORKSHOP_DATA.uhri; the country is read from the data."

Then the code block.

Let me write the entire HTML now, mentally compiling for errors.

Careful: in JS template strings I'll use regular string concatenation to avoid backtick issues? Backticks are fine. I'll use template literals sparingly. Actually mixing is fine. I'll use them for readability but ensure no stray `${` in literal text.

Also careful: `esc()` on option labels containing quotes — labels are data values; esc handles.

In fillSelect, option value esc: `'<option value="'+esc(o.v)+'">'`.

Write out now. Also remember `aria-live="polite"` on matchNum — in HTML.

For the tab panels: panel-0 visible initially.

Also add `lang="en"`.

Double-check the state regex in JS string: `/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/` — fine as regex literal.

Paragraph regex: `/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/` — fine.

Now, one concern: `r._first` uses "…" char — fine UTF-8.

CSV: join with "\r\n".

Also `a.download` filename: country may have spaces — replace non-alnum with "-": `COUNTRY.toLowerCase().replace(/[^a-z0-9]+/g,"-")`.

summaryText guard n===0:
```js
function summaryText(){
  var f=filtered(), n=f.length;
  if(!n) return COUNTRY+": 0 records match the current filters ("+filterDesc()+"). Source: "+SOURCE+" ("+SOURCE_URL+"), built "+BUILT+".";
  ...
}
```

OK, writing final. Also include `title` element set statically "UHRI dashboard" and update via JS? Set document.title in init: `document.title="UHRI · "+COUNTRY+" — UN recommendations dashboard";`

Let me finalize the whole thing. I'll now produce the answer. Length will be large; that's fine.

One more check on the "one open at a time" for sample cards: state.sampleOpen single id — yes.

And "The ten cards are listed as one line each, one open at a time" — yes.

Also ensure the check panel's random sample draws from current filter — drawSample uses filtered(). Yes.

Also: "show progress / stop" only for model calls — none. Good.

Final: write it.