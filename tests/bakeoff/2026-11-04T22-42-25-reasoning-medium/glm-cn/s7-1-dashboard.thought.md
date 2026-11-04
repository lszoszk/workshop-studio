Build the full app. Single HTML file, four tabs, filters rail, charts, checks, export. Must be under ~1500 lines. Let me write carefully but compactly.

Key components:
- Header with UHRI · country, title, source line.
- Tabs 01–04 with role=tablist, arrow keys.
- Left rail with filters (3 collapsible headings, one open at a time), shown on tabs 01,02; on 03,04 only number/bar/chips.
- Filters: keyword (300ms debounce), mechanism/body/type/state, years from/to, SDG.
- Overview: tiles, FIG.01 bar chart clickable, table of top 10 themes, FIG.02 stacked bars per year.
- Records tab: search box, table with expandable rows, pagination 50.
- Check tab: self-checks panel, random sample of 10 with seed (mulberry32), cards with Fits/Doesn't fit/Unsure, tally.
- Method & export: text, CSV download with comment lines, copy summary.
- Footer.

Data details: paragraph regex, UPR state extraction regex, link check, etc.

Write code. Use Chart.js 4 as window.Chart. Colors per spec. Keep deterministic.

Let me write it. I'll aim for compact but complete.

Plan structure:

HTML skeleton:
- header
- main with rail aside + section panels (one per tab)
- footer

JS:
- state: filters {kw, mech, body, type, state, yFrom, yTo, sdg, theme}
- applyFilters() returns filtered records
- render() updates rail number, chips, and active tab content
- Tabs render: renderOverview, renderRecords, renderCheck, renderMethod

Charts: keep chart instances, destroy/recreate on render.

Records table: build rows, expand on click. Row expand is a second tr or details inside td? Use a hidden tr after each row containing expand content.

Pagination: shownCount variable, "Show 50 more".

Sort: date desc default; click Date header toggles.

Checks: computed on tab open.

Sample: seeded mulberry32, draw 10 from filtered, cards.

CSV export: build string with comment lines starting "#".

Copy summary: clipboard.

Escape HTML for text.

Let me write the file now. Keep it efficient.

For highlight keyword matches with <mark>: after escaping, wrap matches. Match each word case-insensitively.

State extraction: 
```js
function uprStates(text){
  const run = text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
  if(!run) return null;
  const groups = run[1].match(/\((?:[^()]|\([^()]*\))*\)/g)||[];
  const out=[];
  for(const g of groups){
    const inner=g.slice(1,-1).trim();
    if(!inner) continue;
    if(inner.includes(',')||inner.length>60){return ['__none__'];}
    out.push(inner);
  }
  return out.length?out:['__none__'];
}
```
Hmm, spec: "A group is accepted as a State only if it has no comma and at most 60 characters; otherwise the record gets 'State not found'." So if any group fails → 'State not found'. Actually if one group fails, mark whole record? Simpler: if any group has comma or >60, record gets "State not found". I'll do that.

Paragraph: `/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/`.

Filters chips: removable.

Rail collapse: buttons aria-expanded, panels with hidden.

Filter counts for body depend on chosen mechanism? Spec: "Body or mandate (`body` values present in the chosen mechanism, each with its count)". Counts within mechanism selection (or full data if "all").

Year selects: distinct years; reversed range swapped.

SDG select: goals present, with names from sdg_names.

State select: appears in heading 02 ("A State select joins this heading when States are extracted").

Theme filter via bar click: theme filter stored in state, chip shown. Apply: record.themes.includes(theme).

Chips: each active filter with remove button.

Header source line: source linked, n records, n docs, years, built, "dated by document".

Overview tiles: headline (total in file, breakdown per type), docs, years, then one tile per mechanism. Also UPR tile has "see the States" link opening in-place list of top 10 States.

FIG.01: top 10 themes, chart + table. Click bar adds theme filter.

FIG.02: stacked bars per year per mechanism.

Check tab: run checks list. Sample check.

Method tab: sentences, download CSV, copy summary, source, licence, build date.

Footer: built on OHCHR UHRI data · n records · source link. Credits? I used guidance sources but no shelf code — plan mentions credits "if any shelf code was used" — none. Add credits line? Not needed. Actually the sources consulted are guidance documents, not code. Skip credits or include a small line? I'll skip.

Number formatting: toLocaleString.

Let me now write the HTML. Careful with `Number(count)`.

Self-checks:
1. record count vs Number(uhri.count)
2. partitions: mechanism, body, year sums
3. type partition
4. chart vs table: recompute top theme counts with second loop; largest bar ≤ filtered count
5. links: doc_url starts with https://docs.un.org/ and ends with symbol (case-insensitive after decoding). Use try{decodeURIComponent(url)}.
6. paragraph share per mechanism; UPR expected 100% → warning if lower
7. States found: count UPR with ≥1 state; list records without (symbol + what parens held: the trailing run raw)
8. duplicates/gaps: distinct id, duplicate texts count, records with no themes/sdgs/affected_persons.

Sample: seed box default 1, Draw again (increment seed? spec: "Draw again" and "Draw with this seed" — draw again picks a new random seed maybe; I'll make Draw again use seed+1... Actually simpler: Draw again draws with a new seed (random) and updates the seed shown; Draw with this seed uses the box value). Tally x/y/z of judged.

Cards: one open at a time — use details or button expand. Use button aria-expanded, one open at a time. Actually "listed as one line each, one open at a time" — so each card is a collapsed line; clicking opens the full text.

OK. Write code.

Rendering approach: I'll re-render tab content on demand. Keep global state, renderRail() on every filter change, plus render current tab.

For charts, destroy old ones.

Search box on tab 02 is "the same box as 01 Keyword" — I'll sync two inputs (rail keyword and records search box) — update both values.

Also "click = filter" hint near chart.

Table sort: date desc default; clicking Date header toggles asc/desc. Sort: date, body, paragraph number ascending (numeric), then file order. Wait: "sorted by `date` descending, then `body`, then paragraph number ascending (numeric, so 10 follows 9), then the order in the file. ... clicking the Date header reverses it." Reverses → date ascending. Keep other keys same? Just flip date direction; I'll flip whole comparison? Simplest: toggle dir on date only.

Paragraph numeric: parse float.

Expand row: second <tr> with colspan, hidden until clicked. Put button role. Row click toggles; Enter key on row (tabindex=0).

Copy citation: navigator.clipboard.writeText; fallback textarea. Show "Copied" 2s. Button label with "(no paragraph number in this extract)" when no para.

Now, tab 03 and 04 rail: hide filter headings. I'll toggle a class on rail.

Limit clicks per view: tabs (4) + filter headings (3) + within heading a few buttons — headings closed by default, so fine.

Write the code. Aim ~1000 lines.

CSV: columns Date, Body, Mechanism, Type, Symbol, Para, Recommending States, Themes, SDGs, SDG targets, Affected persons, Section, Text. Comment lines starting with #? Actually comment lines starting "#" before header. CSV escape: quote fields, double quotes inside. BOM for Excel maybe. Use Blob.

Copy summary: plain text with headline numbers and ten themes.

Let me write it.

Careful: `hidden` attribute CSS rule included.

Chart config FIG.01: horizontal bars (indexAxis 'y'), red at 80% opacity ("#9b2335" with alpha .8), value at end via custom plugin or afterDatasetsDraw... Simpler: use datalabels? Not available. Use a small plugin drawing text at end of bars. I'll write a plugin inline.

FIG.02: stacked bar, per year, three datasets with colors. Legend shown. No gridlines clutter: set grid display false, but ticks keep.

Year axis: all years from min to max.

Sample generator: mulberry32.

Now write.

For the tally: "Themes: x fit, y don't, z unsure of 10 judged", with seed used.

Cards verdict buttons: Fits/Doesn't fit/Unsure, one per card (can change). Store verdicts in map by record id.

Check "States found" listing: records without state — show symbol and the trailing parentheses content. Show maybe limited list (first 20) to avoid huge; spec says "listed". I'll list all with symbols (could be many). Limit to 50 with note. Fine.

Also link check fails listed.

Let me write the whole document now.

Rail share bar: red thin bar width = filtered/total %.

Header data line: `${uhri.country}` etc.

Big number tiles on Overview: total records (all file — "The first tile counts all records in the file" — hmm, "counts all records in the file: recommendations, concerns... Under the number, one line gives the breakdown per type". But then filter? Plan says tiles reflect... "Every tab reads the same filtered set" for tiles it says "share of the filtered set" for mechanism tiles. For the first tile: "counts all records in the file" — I think it shows filtered count with breakdown of the filtered set? The spec literally: "The first tile counts **all records** in the file: recommendations, concerns/observations and any other `type`. Under the number, one line gives the breakdown per `type`". And "The Type filter (all / each `type` value present) starts on 'all'." Hmm — I'll make the first tile show the filtered count (which equals the file when no filter), with breakdown per type of filtered set, and note "of N in the file". That satisfies both mostly. Actually to be safe: big number = filtered count, note "How this is computed: records in the current filter; N in the whole file". Breakdown per type of filtered.

Type filter lives in heading 02.

Mechanism tiles: records, documents, latest year, share of filtered set. "share of the filtered set" — share = mech records / filtered count.

OK writing now. I'll be economical.

State select counts: count per state across... current other filters? Simpler: counts computed on data filtered by everything except state. Fine.

Let me write the final file.