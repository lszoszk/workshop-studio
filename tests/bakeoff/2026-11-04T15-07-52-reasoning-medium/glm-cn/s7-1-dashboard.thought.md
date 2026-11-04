Build the full app in one HTML file. Must follow the plan closely but keep under ~1500 lines. Let me write it carefully.

Key components: header, tabs (4), left rail with filters, tab 01 overview (tiles, FIG.01 chart + table, FIG.02 stacked), tab 02 records table with expand, tab 03 checks + sample, tab 04 method & export.

Let me write compactly but complete. I'll write the code.

Plan the structure:

- CSS: paper look, accent red, serif/mono/sans.
- JS: state {keyword, mechanism, body, type, state (recommending state), yearFrom, yearTo, sdg}, chips, filtered().
- Filters rail shown on tabs 1-2 fully, tabs 3-4 reduced.

Write it. Careful with paragraph regex, state extraction.

Let me draft the code mentally and write it out.

Details:
- paragraph number: /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/
- state extraction per plan.
- CSV export with comments.
- Copy summary.
- Checks panel.
- Random sample with mulberry32, tally.
- Chart.js horizontal bars, click to filter theme; stacked bar per year by mechanism.

Filter headings: 01 Keyword, 02 Mechanism, body, type (and state select), 03 Years and SDG. Accordion, one open at a time. Active chips removable.

Note: theme filter — clicking a bar adds theme as filter chip. So state includes themes (array). Chips display.

Keep clickables under ~7 per view: tabs(4) + 3 filter headings + clear all = 8... plan says filter headings count; plan says it's fine per plan. Fine.

Write the file. I'll aim for a complete, working single file. Use delegation for table row clicks. Pagination 50.

Charts: destroy/recreate on update.

Escape HTML for texts.

Let me write.

Chart FIG.01: horizontal bars, ranked, count at end. Chart.js indexAxis 'y'. Click bar -> add theme filter.

FIG.02 stacked bar: years all from min to max (of file or filtered? "every year from the first to the last appears" — of filtered set's years range, plan says first to last; use filtered min-max). Actually gaps visible: use full file year range? "for the current filter; every year from the first to the last appears" — I'll use the file's full year range so gaps show. Hmm, "first to the last" ambiguous; use file range from data years, showing zeros — better shows gaps. I'll use min-max of file years.

Tabs 3-4: rail keeps only number, bar, chips.

Sample check: draw 10 from current filter with seed.

Checks: implement all listed.

CSV: visible columns + full text + labels, comment lines.

Copy citation: navigator.clipboard.writeText fallback.

Header: source linked, n, docs, years, built, "dated by document".

Footer.

Let me now write the code, aiming ~900-1100 lines.

Key functions:

```
const U = WORKSHOP_DATA.uhri;
const recs = U.records;
function paraNum(t){const m=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/.exec(t);return m?m[1]:null;}
function statesOf(r){ if(r.mechanism!=="Universal Periodic Review")return null;
 const m=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/.exec(r.text);
 if(!m)return [];
 const groups=m[0].match(/\((?:[^()]|\([^()]*\))*\)/g)||[];
 const out=[];for(const g of groups){const inner=g.slice(1,-1).trim();if(!inner.includes(",")&&inner.length<=60)out.push(inner);}
 return out; // empty means "State not found"
}
```
Cache states per record via map.

Filtering:
```
state = {kw:"", mech:"all", body:"all", type:"all", st:"all", yFrom:null,yTo:null, sdg:"all", themes:[]}
```
Year selects: default first/last.

filtered(): loop.

Render functions per tab; recompute on filter change.

Big-count aria-live.

Chips: keyword, mech (if not all), body, type, state, sdg, year range (if not full), each theme.

Ok, write it. Also body filter options depend on mechanism selection — when mechanism changes, reset body to all and re-render options with counts.

Table columns: Date | Body | Symbol | Para. | First line | State. Date header button toggles sort asc/desc.

Sort: date desc, body, para numeric asc, then index. Clicking Date reverses (date asc, rest same).

Expand row: details below in a row colspan.

Keyword highlight with <mark> in first line — escape first, then wrap matches for each word.

Export CSV: comment lines starting with #.

Copy summary: plain text paragraph.

Sample cards: one open at a time (details-like: buttons with aria-expanded). Each card: symbol link, para, full text, theme chips, three buttons Fits/Doesn't fit/Unsure. Tally line with seed.

Checks: compute at tab open (or on load, render into tab 3). Compute on demand when tab 3 shown, using current filter for nothing—checks are over whole file mostly. Do whole-file checks; fine.

Link check: doc_url starts with https://docs.un.org/ and ends with symbol (case-insensitive after decodeURIComponent). List failures.

Paragraph share per mechanism; UPR <100% warning.

States: count UPR records with ≥1 state vs UPR total; list those without, with symbol and the trailing parenthesis text (truncated).

Duplicates: distinct id, duplicate texts count, records with no themes/sdgs/affected_persons counts.

Chart vs table check: recompute via second loop.

Now write full HTML. Keep code tight.

For charts use Chart.js with minimal config, no gridlines. Colors: FIG.01 bars red 80% (#9b2335 at 0.8 alpha). FIG.02 stacked: colors by mechanism; legend.

Mechanism colors: map with fallbacks for other mechanisms.

FIG.01 table: theme | records | % | years range.

"see the States" link in UPR tile -> toggles inline list of top 10 states with counts for current filter.

Write code now.

For the rail on tabs 3/4: hide the accordion (hidden attr), show number+bar+chips. Use class.

Tabs with role=tablist and arrow keys: keydown handler.

Number formatting: toLocaleString.

Let me write the final document. I'll be careful with edit-free single file.

For the keyword input debounce 300ms, and the search field on tab 02 is the same box — I'll have the keyword input inside the rail; tab 02 also has a search field on top that mirrors it (same state). Plan says "One search field across the top ... the same box as 01 Keyword". Simpler: keep the rail's keyword box as the single one? Plan says a search field across the top of tab 02, same as 01 Keyword. I'll sync both inputs.

OK writing.

For copy confirmation: small span "Copied" for 2s.

CSV generation: escape quotes.

Also `hidden` CSS rule.

Time to write it out. I'll structure:

```
<!doctype html><html lang="en"><head>...<style>...</style></head>
<body>
header
nav tabs
div.layout: aside#rail, main sections (4)
footer
<script>...</script>
```

Write JS carefully. Estimate ~600 lines JS. Fine.

Some care: year selects reject reversed range by swapping — on change, if from > to, swap values.

Chips for year range show when not full range.

Let me write.