Let me plan this tool carefully.

Requirements:
- Compare how two States vote at the HRC.
- Pick two States — only those that were Council members for at least one vote (i.e., appear in `votes` of at least one record).
- Show: number of recorded votes both took part in, how often they voted the same way, timeline by year.
- List votes where they differed: resolution title, date, both votes, link.
- Switch between resolutions, amendments, or both (filter by `kind`).
- Where official totals (yes/no/abstain) differ from roll call counts, show a small warning on that row.

Data: `WORKSHOP_DATA.hrc` with `records`, `countries` (ISO3 → name), `vote_codes`.

Design:
- Header: title, description with source, n, years.
- Two dropdowns (select) for State A and State B, populated from countries that appear in at least one `votes` map. Default: pick two sensible defaults (e.g., first two countries alphabetically, or maybe pick two that differ often — but deterministic: just pick first two by name, or maybe pick two with most overlap? Simpler: default to first two alphabetically by name). Actually a nicer default: pick the two states with the most joint participation? That requires computation — fine, deterministic. But simpler and predictable: alphabetical first two. Hmm, maybe pick two that have disagreements so the list isn't empty. Let me compute: for each pair? That's O(n²) over countries (~60 countries → 1770 pairs, each pair checking records... could be heavy but records count maybe a few hundred; 1770 × 300 = 531k operations, fine). But simpler: just default to first two alphabetically. The user can switch. I'll default to the first two countries alphabetically by name — deterministic and simple. Actually, to make the demo interesting, maybe pick the pair with the most disagreements among pairs with ≥ some joint votes. That's a nice touch but adds complexity. Let me do: default selection = the pair (among all pairs) with the maximum number of differing votes, tie-break by most joint votes, then alphabetical. That's deterministic and shows the tool working. Cost: countries list maybe ~60; pairs ~1770; for each pair iterate records once — better: precompute per record the votes map; for pair comparison, iterate records and check both ISO codes present. 1770 × N records. If N = 500, that's ~885k checks — fine in JS.

Actually simpler approach: build for each country a map recordId → vote. Then for each pair, intersect keys. Still O(pairs × records). Fine.

But maybe keep it simpler: default to first two alphabetically. Hmm. The workshop user will pick anyway. I'll do the "most disagreements" default since it makes the tool immediately illustrative, but cap: if no pair has disagreements, fall back to alphabetical first two. Actually let me just do alphabetical first two to keep code lean... The prompt says "Pick two States" — the user picks. Default just needs to be valid. I'll do the max-disagreement default; it's ~15 lines. Actually, let me reconsider performance: countries could be up to 47 members × many terms... The `countries` map maps ISO3 of the 47 Council members — but over years, membership changes, so maybe ~70-80 countries. Pairs ~3000. Records maybe 300-800. 3000×800 = 2.4M simple checks — fine (<100ms).

Hmm, but I can do it smarter: for each record, for each pair of countries present in that record's votes... that's per record C(k,2) where k≤47 → ~1081 pairs per record × 800 records = 864k pair-increments. Similar. Either way fine. I'll do the per-country map approach:

```js
const byCountry = {}; // iso -> Map(recordId -> vote)
records.forEach(r => { for (const [iso, v] of Object.entries(r.votes||{})) { (byCountry[iso] ||= new Map()).set(r.id, v); } });
```

Then pair loop over country keys.

- Stats: joint votes count (both present in `votes`), same count (votes equal), same % , different count. Also maybe breakdown Y/N/A agreement? Keep it: "voted the same way X of Y times (Z%)". Maybe also show agreement split: both Y, both N, both A counts. Nice touch.

- Timeline by year: Chart.js bar or line chart, x = year, showing per year: joint votes, same votes (or % same). Maybe grouped bars: "both took part" and "voted the same". Or a line of % agreement with bars of counts. I'll do a bar chart with two datasets: "Votes both took part" and "Voted the same", per year. Plus maybe a line for % same? Keep two bar datasets; the % can be in tooltip. Or stacked? Grouped bars fine. Chart.js is preloaded.

Actually a line chart of agreement % could be nice but with low counts percentages jump. I'll do grouped bars: total joint votes and same votes per year. Tooltip shows %.

- Filter: segmented control or select: "Both (resolutions + amendments)", "Resolutions only", "Amendments only". Recompute everything on change.

- Differing votes list: table rows: date, year, kind badge, title (linked to doc_url if present else record_url), symbol, State A vote, State B vote, warning icon if totals mismatch roll call. Sort by date descending (or ascending? descending recent first — I'll do descending, with a note). Each row expandable? The requirement: "List the votes where they differed, with the resolution title, date, both votes and a link." Also rule: "Every row that shows a document has its symbol, linked to doc_url in a new tab." So symbol link to doc_url (if doc_url empty, fall back to record_url; if both empty, no link). Also show record_url link maybe ("vote record"). I'll link symbol → doc_url (new tab) when doc_url non-empty; also a small "record" link to record_url.

- Warning: compute roll call counts from `votes`: count Y, N, A. Compare to `yes`, `no`, `abstain`. If any differ, show warning badge "official totals ≠ roll call" with details (e.g., "totals say 29/16/1, roll call gives 28/16/2"). Show on rows in the differing list. Should the warning also appear elsewhere? The requirement says "show a small warning on that row" — rows of the differing list. Maybe also in a full votes table? The user only asked for differing list. But maybe also show all joint votes? The ask: "Show on how many recorded votes both took part, how often they voted the same way, and a timeline by year. List the votes where they differed". So the list is only differing votes. I could add a toggle to show all joint votes too — optional. Keep scope: differing list only, but maybe add a checkbox "show all joint votes" — could be nice but adds complexity. I'll add a toggle: "Differing only / All joint votes" — actually the user asked specifically for differing; adding "all" is a small bonus. Hmm, keep it focused but a toggle is easy: same table, filter differs. I'll include a small toggle since it helps verify counts. Actually, let me include it — "Show: differing votes only | all joint votes". In "all" mode, show both votes and a "same/different" marker. Warning still shown on mismatch rows. This makes the tool more useful and honest. OK.

- Vote display: Y/N/A with labels: "Yes", "No", "Abstain" and colors (green/red/grey) — but keep professional: small badges. Accent color #1f6fb2. Use muted colors for badges: yes = green (#2e7d32 bg light), no = red-ish, abstain = grey. That's fine for a data portal.

- "How this is computed" notes near each chart/number.

- Header description: source = WORKSHOP_DATA.hrc.title, n = count of records, years range from records (min–max year). Country = participant's country? The uhri country is the participant's country; for HRC tool maybe highlight it? Not required. Could preselect the participant's country as State A if present in hrc countries — nice touch: if WORKSHOP_DATA.uhri.country's ISO3... but we don't have name→ISO3 mapping directly; hrc.countries maps ISO3→name, so we can find ISO3 by matching name === uhri.country. If found and appears in votes, default State A = that. That's a nice personalized touch. I'll do that: State A default = participant's country if it's a Council member in the data, else alphabetical first. State B default = country with most disagreements with A (or alphabetical). Hmm, that's good: pick B as the state with most differing votes vs A (tie-break: most joint votes, then name). Deterministic.

- Only states that were Council members for at least one vote: populate selects from keys of byCountry (i.e., ISO codes appearing in at least one votes map), sorted by name. Note: `hrc.countries` may include countries never in votes? Possibly; filter by presence in byCountry. Also handle a country in votes but missing from countries map (use ISO code as label fallback).

- Handle empty: if no records or no countries, show message.

- Kind filter: 'all' | 'resolution' | 'amendment'. Note kind values are "resolution"/"amendment". Filter records by kind when computing. Show counts of each kind in the filter options maybe: "Resolutions (n)", "Amendments (n)". Compute from data.

- Timeline chart: rebuild on changes. Use Chart.js bar chart. Years sorted ascending. Datasets: "Both took part" (accent #1f6fb2), "Voted the same" (lighter, e.g., #9ec7e8 or a green). Tooltip: show % same. Also maybe a line dataset for % same on secondary axis — could be nice: "Same %" line. Let me add it as a line on secondary y-axis (0–100%). That's informative. Three datasets: bars for counts, line for %. Chart.js mixed chart is fine.

Actually keep it clean: grouped bars (joint, same) + line (% same, right axis). Good.

- Summary numbers: big stat cards: "Recorded votes both took part in: N", "Voted the same: X (Y%)", "Differed: Z". Plus breakdown: both Yes / both No / both Abstain counts. And note about filter applied.

- Also maybe show per-vote-code agreement: e.g., "When A voted Yes, B voted Yes in x%..." — too much. Skip.

- The differing list rows: date, kind, title, symbol link, A vote badge, B vote badge, warning. Title text: record.title; link: doc_url if present else record_url. Requirement says symbol linked to doc_url in new tab. I'll make the symbol the link to doc_url (new tab), and title linked to record_url if doc_url empty... Let me do: title is a link to doc_url || record_url (new tab); symbol also linked to doc_url if present. To satisfy "every row that shows a document has its symbol, linked to doc_url in a new tab": symbol anchor href=doc_url target=_blank. If doc_url empty (like the amendment sample), link symbol to record_url instead, or leave unlinked with title "no document link". I'll link to doc_url if non-empty else record_url if non-empty else no link.

- Warning details: compute roll = {Y: count, N: count, A: count} from votes; official = {yes, no, abstain}. Mismatch if roll.Y !== yes || roll.N !== no || roll.A !== abstain. Warning text: "Official totals (Y/N/A: yes/no/abstain) differ from the roll call (Y/N/A: roll counts)." Show as small ⚠ badge with title tooltip, and maybe expandable detail. I'll render a small inline warning with the numbers, e.g. "⚠ totals 29/16/1 vs roll call 28/16/2". Keep small.

- Sorting of list: by date descending; ties by symbol. Add note "sorted by date, most recent first".

- Also show count of differing votes above list: "X votes where they differed (of Y joint votes)".

- Layout: header, controls (two selects + kind segmented + show toggle), stat cards, chart, list. Responsive, max-width ~1100px, no horizontal scroll. Table on small screens: use table with wrapping; ensure no overflow — use `table-layout: fixed`? Titles can be long; allow wrapping. Use div-based rows maybe simpler for responsive. I'll use a table with `word-break` and width 100%; on narrow screens it still fits since columns wrap. Vote badges fixed width. Should be fine.

- "How this is computed" notes: under stats: "Counts are computed from the roll-call `votes` of each record where both selected States appear; filtered to {kind label}. Same = identical vote code (Y/N/A)." Under chart: "One bar per year; line shows the share of joint votes where both voted the same." Under list: "Rows show every recorded vote in the current filter where the two States' votes differ (or all joint votes when toggled); ⚠ marks records where official totals differ from the roll call."

- Years in header: min–max of record years.

- Also mention source: `WORKSHOP_DATA.hrc.title` and source? hrc object has `title`, `count`, `countries`, `vote_codes`, `records`. No `source` field mentioned; title likely like "Human Rights Council recorded votes". I'll write: "Source: {hrc.title} — {count} recorded votes, {yearMin}–{yearMax}." Also mention vote codes meaning: Y/N/A from vote_codes map? vote_codes: {Y,N,A} — probably labels like {"Y": "Yes", ...}. I'll use it if present for labels: `vote_codes.Y` etc. Fallback "Yes"/"No"/"Abstain".

Let me check: `vote_codes: {Y,N,A}` — ambiguous; could be {"Y":"Yes","N":"No","A":"Abstention"}. I'll use `voteCodes[code] || fallback`.

- Edge cases: records with missing votes ({}), missing kind, missing year. Handle: kind filter uses r.kind; year from r.year (fallback parse from date). Missing date → display "—". Sorting with missing dates: put at end.

- Also "both took part" means both ISO codes present in votes object (regardless of value Y/N/A — all values are participation). Yes.

- Same way: votes equal.

- Also maybe show agreement rate among only differing? No.

- Switching states: on change, recompute. Also disable same-state selection? If user picks same state for both, show message "Pick two different States" and clear results. Handle gracefully.

- The selects: label "State A" and "State B". Options: name (ISO3). Sorted by name.

Implementation plan (JS):

```js
const HRC = window.WORKSHOP_DATA.hrc || {};
const records = Array.isArray(HRC.records) ? HRC.records : [];
const countryNames = HRC.countries || {};
const voteCodes = HRC.vote_codes || {};
```

Build byCountry: Map iso -> Map(id -> vote). Also set of member ISOs.

memberList = Object.keys(byCountry).map(iso => ({iso, name: countryNames[iso] || iso})).sort by name.

Defaults: 
```js
const uhriCountry = (window.WORKSHOP_DATA.uhri && window.WORKSHOP_DATA.uhri.country) || "";
let isoA = memberList.find(m => m.name === uhriCountry)?.iso;
if (!isoA) isoA = memberList[0]?.iso;
// pick B: max disagreements with A among others, tie-break joint count desc, then name
```
Compute pair stats function:

```js
function pairStats(isoA, isoB, kindFilter) {
  const mapA = byCountry.get(isoA), mapB = byCountry.get(isoB);
  let joint=0, same=0, bothY=0, bothN=0, bothA=0;
  const diffs=[]; const all=[];
  for (const r of records) {
    if (kindFilter!=='all' && r.kind!==kindFilter) continue;
    const va = mapA?.get(r.id), vb = mapB?.get(r.id);
    if (va===undefined || vb===undefined) continue;
    joint++;
    const row = {r, va, vb, same: va===vb};
    all.push(row);
    if (va===vb){ same++; if(va==='Y')bothY++; else if(va==='N')bothN++; else bothA++; }
    else diffs.push(row);
  }
  return {joint, same, diffs, all, bothY, bothN, bothA};
}
```

Wait — mapA.get(r.id) returns vote; but what if vote value could be something else? vote_codes keys Y,N,A. Fine. Note: `undefined` check works since Map.get returns undefined when absent. But careful: a vote value could never be undefined. OK.

Year for chart: group joint & same by year:

```js
const years = new Map(); // year -> {joint, same}
for (const row of all) { const y = row.r.year ?? parseYear(row.r.date); ... }
```

parseYear: `(r.date||'').slice(0,4)` parseInt.

Roll call check:

```js
function rollCall(r){ const c={Y:0,N:0,A:0,other:0}; for (const v of Object.values(r.votes||{})) { if (v in c) c[v]++; else c.other++; } return c; }
function mismatch(r){ const c=rollCall(r); return !(c.Y===r.yes && c.N===r.no && c.A===r.abstain); }
```

Careful with missing yes/no/abstain (undefined): if r.yes is undefined, treat mismatch only if defined? If official totals missing, can't compare — treat as no warning? Or warning "totals missing"? I'll only warn when all three official numbers are numbers and differ from roll call. If some missing, skip. Actually if yes is undefined and roll has Y count, that's a mismatch too... but safer: compare only when typeof r.yes==='number' etc. If any is not a number, no warning (can't verify). Hmm, but the spec says show warning where they differ. I'll do: if all three are numbers and any differs → warning. Else no warning.

Warning text: `⚠ official totals ${yes}/${no}/${abstain} ≠ roll call ${c.Y}/${c.N}/${c.A}` (Y/N/A order).

Render list rows:

```html
<tr>
  <td class="date">2023-10-13</td>
  <td><span class="kind amendment">Amendment</span></td>
  <td class="title"><a href=...>title</a> <span class="sym"><a href=doc_url target=_blank>symbol</a></span> warning</td>
  <td><span class="vote Y">Yes</span></td>
  <td><span class="vote N">No</span></td>
</tr>
```

Columns: Date | Kind | Vote / title | State A | State B. Maybe: Date | Kind | Title & symbol | A | B. Header row shows state names dynamically ("Kenya (KEN)").

Also in "all" mode add a "Same?" column? Could add a small ✓/✗. I'll add a column "Match" showing "same"/"differs" only in all-mode... simpler: always show a dot: green ✓ if same, red ✗ if differs; in differs-only mode all are ✗. Fine, keep column "Same?" with ✓/✗.

Chart: 

```js
new Chart(ctx, {type:'bar', data:{labels: years, datasets:[{type:'bar', label:'Votes both took part', data: jointArr, backgroundColor:'#1f6fb2'}, {type:'bar', label:'Voted the same', data: sameArr, backgroundColor:'#a8cbe8'}, {type:'line', label:'% voted the same', data: pctArr, yAxisID:'y1', borderColor:'#2e7d32', ...}]}, options:{scales:{y:{beginAtZero:true, title:{display:true,text:'Number of votes'}}, y1:{position:'right', min:0, max:100, title:{display:true,text:'% same'}, grid:{drawOnChartArea:false}}}, plugins:{tooltip:{callbacks:{label: ...}}}}});
```

Destroy previous chart on update (`chart.destroy()`).

Tooltip label: for bar datasets show count; for line show pct% and maybe "x of y". I'll compute in callback using datasetIndex and index: for line: `${pct}% (${same} of ${joint})`.

If no data (joint=0), show message instead of chart ("No recorded votes in this filter where both States took part.") and skip chart.

Stats cards: 
- "Joint recorded votes" = joint
- "Voted the same" = same + pct
- "Differed" = joint - same
Plus small line: "Both Yes: x · Both No: y · Both Abstain: z".

Kind filter UI: three buttons (segmented) or a select. I'll use a `<select>`: "Resolutions and amendments (all)", "Resolutions only (n)", "Amendments only (n)". Counts computed from records. Or segmented buttons look nicer. I'll do segmented buttons with counts: All (n) · Resolutions (n) · Amendments (n). Buttons with aria-pressed.

Show toggle: select "Differing votes only" / "All joint votes". Or a checkbox "Show all joint votes (not only differences)". I'll do a select or checkbox. Checkbox simple.

Header description: `Source: ${HRC.title} · ${records.length} recorded votes (${minYear}–${maxYear}) · roll-call votes by the 47 Council members; official totals shown where they differ from the roll call.` Also mention participant country? Not needed.

Also note: "States listed are those that appear in the roll call of at least one recorded vote."

Now the "How this is computed" notes:
- Stats: "Computed from the roll call (`votes`) of every record in the current filter where both selected States appear. 'Same' means identical vote code (Y/N/A)."
- Chart: "Bars: recorded votes per year in the current filter where both States took part, and how many of those were the same. Line: share of joint votes that were the same (right axis)."
- List: "Every recorded vote in the current filter where the two States' votes differ (or all joint votes if 'show all' is on), most recent first. ⚠ = the official totals (yes/no/abstain) differ from counting the roll call."

Vote badge labels: use voteCodes map: `label(code)` = voteCodes[code] || {Y:'Yes',N:'No',A:'Abstain'}[code] || code.

Colors: .vote.Y green, .vote.N red, .vote.A grey. Kind badge: resolution = accent outline, amendment = different (e.g., purple/grey). Keep subtle.

Now defaults for B: compute for each other member: disagreements with A across all records (kind 'all'). Pick max disagreements; tie-break by joint desc; then name asc. If all zero disagreements, pick the one with max joint. Implementation:

```js
function pickDefaultB(isoA){
  const mapA = byCountry.get(isoA);
  let best=null;
  for (const m of memberList){
    if (m.iso===isoA) continue;
    const mapB = byCountry.get(m.iso);
    let joint=0, diff=0;
    for (const r of records){ const va=mapA.get(r.id); const vb=mapB.get(r.id); if(va!==undefined&&vb!==undefined){joint++; if(va!==vb)diff++; } }
    const score = {diff, joint, name:m.name};
    if (!best || diff>best.diff || (diff===best.diff && joint>best.joint) || (diff===best.diff&&joint===best.joint&&m.name<best.name)) best={...score, iso:m.iso};
  }
  return best?.iso;
}
```

Fine.

Also handle: if memberList.length < 2 → show message "Not enough Council members in the data to compare."

If user selects same state for both: show notice and hide results.

Now write the HTML. Structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HRC vote comparison — ...</title>
<style>...</style>
</head>
<body>
<header>
  <h1>Comparing two States' votes at the Human Rights Council</h1>
  <p class="desc" id="sourceLine"></p>
</header>
<main>
  <section class="controls">
    <div class="field"><label for="selA">State A</label><select id="selA"></select></div>
    <div class="field"><label for="selB">State B</label><select id="selB"></select></div>
    <div class="field"><label>Votes shown</label><div class="seg" id="kindSeg">buttons</div></div>
    <div class="field"><label for="showAll">List</label><select id="showAll"><option value="diff">Differing votes only</option><option value="all">All joint votes</option></select></div>
  </section>
  <p class="note" id="membersNote"></p>
  <section id="results">
    <div class="cards">3 cards + breakdown</div>
    <p class="how" id="howStats"></p>
    <h2>Timeline by year</h2>
    <div class="chartWrap"><canvas id="chart"></canvas></div>
    <p class="how" id="howChart"></p>
    <h2 id="listTitle">Votes where they differed</h2>
    <p class="how" id="howList"></p>
    <table id="votesTable">...</table>
    <p id="emptyList"></p>
  </section>
  <p id="sameStateMsg" hidden>...</p>
</main>
<script>...</script>
</body>
</html>
```

CSS: system font stack, background #f5f7fa, cards white, accent #1f6fb2. Base font 16px. Max width 1080px, padding. Table full width, borders light. Badges.

Let me be careful about line count (<700). Should be fine, ~450 lines.

Chart.js usage: `window.Chart`. Guard `if (window.Chart)`.

Now details for rendering list rows. Build with DOM creation or innerHTML with escaping. Text from data must be escaped — write `esc()` function for HTML injection safety.

```js
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
```

Row HTML:

```js
function rowHtml(row, showMatch){
  const r = row.r;
  const docLink = r.doc_url || r.record_url || '';
  const sym = r.symbol ? (docLink ? `<a href="${esc(docLink)}" target="_blank" rel="noopener">${esc(r.symbol)}</a>` : esc(r.symbol)) : '—';
  const titleLink = docLink ? `<a href="${esc(docLink)}" target="_blank" rel="noopener">${esc(r.title || '(untitled)')}</a>` : esc(r.title || '(untitled)');
  const warn = mismatch(r) ? `<span class="warn" title="...">⚠ totals ${r.yes}/${r.no}/${r.abstain} vs roll call ${c.Y}/${c.N}/${c.A}</span>` : '';
  ...
}
```

Wait: symbol should link to doc_url specifically per rules ("its symbol, linked to doc_url in a new tab"). If doc_url empty, fall back to record_url (still a link to the document record). Fine.

Date display: r.date || '—'. Kind badge: r.kind || '—' capitalized.

Vote cell: `<span class="vote ${va}">${esc(label(va))}</span>` plus maybe code: "Yes (Y)". I'll show label with code: `Yes · Y`? Keep "Yes (Y)". Hmm, badges small: show label only, with title attr showing code. I'll show `${label} (${code})`? That's clearer. Let me show label and code: e.g. "Yes (Y)". OK.

Match column: `✓ same` green / `✗ differs` red — only meaningful in all mode; in diff mode all differ. Keep column always, header "Same?".

Table header: Date | Kind | Vote (title + symbol + warning) | `${nameA}` | `${nameB}` | Same?

Column widths: date 90px, kind 90px, votes flexible, each state 110px, same 80px.

Warning placement: inside the title cell after symbol, small.

Also add record_url link? The doc link covers it. If doc_url empty and record_url present, symbol links to record_url. Good.

Sorting: diffs sorted by date desc, then symbol asc. Dates as strings compare fine (ISO). Missing dates last: use `(r.date||'9999')`.

Chart years: ascending.

Now the header source line: 

```js
const years = records.map(r=>r.year).filter(y=>typeof y==='number');
const minY = Math.min(...years), maxY = Math.max(...years);
sourceLine.textContent = `Source: ${HRC.title || 'Human Rights Council recorded votes'} — ${records.length} recorded votes, ${minY}–${maxY}. Roll-call votes (Y/N/A) of Council members; only States that appear in at least one roll call are offered below.`;
```

Handle empty records: show message.

Members note: `States offered: ${memberList.length} (those present in at least one roll call).`

Kind counts: resolutions = records.filter(r=>r.kind==='resolution').length etc. If kind values differ (e.g., other values), count "other"? The spec says kind is "resolution" or "amendment". I'll count those two; the "All" option includes everything.

Segmented buttons: build three buttons with data-kind="all|resolution|amendment", labels: `All (${records.length})`, `Resolutions (${nRes})`, `Amendments (${nAmd})`. If nAmd===0, still show with 0? Show anyway; selecting yields empty state message. Fine.

State change handler: recompute. Kind change: recompute. showAll change: re-render list only (but stats unchanged) — just re-render list; simpler to recompute all.

Also update list title: "Votes where A and B differed (n)" or "All joint votes (n)".

Stat cards markup:

```html
<div class="cards">
  <div class="card"><div class="num" id="statJoint"></div><div class="lbl">recorded votes both took part in</div></div>
  <div class="card"><div class="num" id="statSame"></div><div class="lbl">voted the same way</div></div>
  <div class="card"><div class="num" id="statDiff"></div><div class="lbl">differed</div></div>
</div>
<p class="breakdown" id="breakdown"></p>
```

statSame: `X (Y%)`. breakdown: `Both Yes: a · Both No: b · Both Abstain: c — of ${joint} joint votes in the current filter (${kindLabel}).`

Percent: joint>0 ? Math.round(100*same/joint) : 0.

How-this-is-computed texts set once (static) but include dynamic filter mention — I'll set them in render with current kind label.

Edge: joint===0 → hide cards/chart/list, show message "No recorded votes in this filter where both States took part."

Same-state selection: if isoA===isoB → show message, hide results.

Now CSS. Let me write it:

```css
:root{--accent:#1f6fb2;--ink:#1c2733;--muted:#5b6b7b;--line:#d9e2ec;--bg:#f4f7fa;--card:#fff;}
*{box-sizing:border-box}
body{margin:0;font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);}
header{background:#fff;border-bottom:1px solid var(--line);padding:20px 24px;}
header h1{margin:0 0 6px;font-size:1.45rem;color:var(--accent);}
...
```

Wrap: `.wrap{max-width:1080px;margin:0 auto;padding:0 20px;}` Apply to header inner and main.

Controls: flex wrap, gap. Selects styled: padding 8px, border, radius 6px, font inherit, background #fff, max-width 260px.

Segmented: buttons inline, border, active = accent bg white text.

Cards: grid 3 columns (auto-fit minmax(180px,1fr)), white bg, border, radius 8px, padding 14px; .num font-size 1.8rem accent bold.

Chart wrap: white card padding, canvas height ~320px. Set `maintainAspectRatio:false` with fixed height container.

Table: width 100%, border-collapse, th small caps muted, td padding 8px 10px, border-top. Row hover. `.vote` badge: inline-block padding 2px 8px radius 999px font-size .85rem. Y: bg #e3f2e5 color #1e6b2f; N: bg #fbe4e4 color #a02121; A: bg #eceff3 color #55606c. Kind badge: resolution: bg #e8f1fa color accent; amendment: bg #f3e9f7 color #6b3fa0. Warn: color #b26a00, font-size .8rem, cursor help.

.how: font-size .85rem color muted, margin.

h2: font-size 1.1rem margin-top 28px.

Note about no horizontal scroll: table with long titles — set `td.title{max-width:...}`? Tables can overflow if content long unbreakable; titles have spaces so they wrap. Add `overflow-wrap:anywhere` on title cell. Set `table{width:100%;table-layout:auto}` fine.

Responsive: on narrow, controls stack (flex-wrap). Table might be tight but wraps. OK.

Now JS full:

```js
(function(){
"use strict";
const DATA = window.WORKSHOP_DATA || {};
const HRC = DATA.hrc || {};
const records = Array.isArray(HRC.records) ? HRC.records : [];
const countryNames = HRC.countries || {};
const voteCodes = HRC.vote_codes || {};
const esc = ...;
const $ = id => document.getElementById(id);

// build member index
const byCountry = new Map();
records.forEach(r => {
  const v = r.votes || {};
  for (const iso in v) { if (Object.prototype.hasOwnProperty.call(v, iso)) { if(!byCountry.has(iso)) byCountry.set(iso, new Map()); byCountry.get(iso).set(r.id, v[iso]); } }
});
const members = [...byCountry.keys()].map(iso => ({iso, name: countryNames[iso] || iso}))
  .sort((a,b)=> a.name.localeCompare(b.name));
```

Wait: r.id may be missing? Assume present. If missing, use index. I'll use `r.id != null ? r.id : 'idx'+i`. Let me just use record object reference instead of id in maps — simpler: map iso -> Map(record -> vote) using the record object as key. Objects as keys work in Map. 

```js
records.forEach(r => { const v = r.votes||{}; for (const iso in v){... byCountry.get(iso).set(r, v[iso]); } });
```

Then pairStats uses mapA.get(r) — record object identity. 

voteLabel:

```js
const FALLBACK = {Y:'Yes', N:'No', A:'Abstain'};
function voteLabel(code){ return (voteCodes && voteCodes[code]) || FALLBACK[code] || code; }
```

kindLabel: {resolution:'resolutions', amendment:'amendments', all:'resolutions and amendments'}.

rollCall & mismatch as above.

yearOf(r): `typeof r.year==='number' ? r.year : (parseInt((r.date||'').slice(0,4),10) || null)`.

render():

```js
let chart = null;
let currentKind = 'all';

function compute(){
  const isoA = selA.value, isoB = selB.value;
  ...
}
```

Populate selects:

```js
function fillSelect(sel, selected){
  sel.innerHTML = '';
  members.forEach(m => { const o=document.createElement('option'); o.value=m.iso; o.textContent = m.name + ' (' + m.iso + ')'; if(m.iso===selected) o.selected=true; sel.appendChild(o); });
}
```

Default A: participant country match:

```js
const uhriCountry = (DATA.uhri && DATA.uhri.country) || '';
let defA = members.find(m => m.name === uhriCountry);
if(!defA) defA = members[0];
```

Default B: as described.

Then fillSelect(selA, defA.iso); fillSelect(selB, defB); then render().

render():

```js
function render(){
  const isoA = selA.value, isoB = selB.value;
  const nameA = (countryNames[isoA]||isoA), nameB = (countryNames[isoB]||isoB);
  if(!isoA || !isoB){ showEmpty('Choose two States to compare.'); return; }
  if(isoA===isoB){ results.hidden = true; sameMsg.hidden=false; sameMsg.textContent = 'State A and State B are the same — pick two different States.'; return; }
  sameMsg.hidden = true; results.hidden = false;
  const mapA = byCountry.get(isoA), mapB = byCountry.get(isoB);
  const rows = [];
  for (const r of records){
    if (currentKind!=='all' && r.kind!==currentKind) continue;
    const va = mapA.get(r), vb = mapB.get(r);
    if (va===undefined || vb===undefined) continue;
    rows.push({r, va, vb, same: va===vb});
  }
  const joint = rows.length;
  const same = rows.filter(x=>x.same).length;
  const diff = joint - same;
  const both = {Y:0,N:0,A:0};
  rows.forEach(x=>{ if(x.same && both[x.va]!==undefined) both[x.va]++; });
  // stats
  statJoint.textContent = joint;
  statSame.textContent = joint ? `${same} (${Math.round(100*same/joint)}%)` : '0';
  statDiff.textContent = diff;
  breakdown.textContent = `Both Yes: ${both.Y} · Both No: ${both.N} · Both Abstain: ${both.A} — counted from the roll call of each record in the current filter (${kindLabel(currentKind)}) where both States appear.`;
  howStats.textContent = 'How this is computed: for every recorded vote in the current filter, we look up each State’s roll-call vote (Y/N/A). “Both took part” = both States appear in that roll call; “same” = identical code. Counts are exact, not estimated.';
  // chart
  renderChart(rows);
  // list
  renderList(rows, nameA, nameB, isoA, isoB);
}
```

renderChart(rows):

```js
function renderChart(rows){
  const byYear = new Map();
  rows.forEach(x=>{ const y = yearOf(x.r); if(y==null) return; if(!byYear.has(y)) byYear.set(y,{joint:0,same:0}); const e=byYear.get(y); e.joint++; if(x.same) e.same++; });
  const years = [...byYear.keys()].sort((a,b)=>a-b);
  const jointArr = years.map(y=>byYear.get(y).joint);
  const sameArr = years.map(y=>byYear.get(y).same);
  const pctArr = years.map(y=>{const e=byYear.get(y); return e.joint? Math.round(100*e.same/e.joint): null;});
  if (chart){ chart.destroy(); chart=null; }
  const canvas = $('chart');
  if (!years.length || !window.Chart){ $('chartEmpty').hidden = years.length>0; canvas.style.display = years.length? '':'none'; ... }
```

Simpler: if no years, hide chartWrap and show chartEmpty message; else show and create chart.

```js
  if(!years.length){ chartWrap.style.display='none'; chartEmpty.hidden=false; return; }
  chartWrap.style.display=''; chartEmpty.hidden=true;
  chart = new Chart(canvas.getContext('2d'), {
    type:'bar',
    data:{ labels: years.map(String), datasets:[
      {type:'bar', label:'Votes both took part', data: jointArr, backgroundColor:'#1f6fb2', borderRadius:3},
      {type:'bar', label:'Voted the same', data: sameArr, backgroundColor:'#a9cdea', borderRadius:3},
      {type:'line', label:'% voted the same', data: pctArr, yAxisID:'y1', borderColor:'#2e7d32', backgroundColor:'#2e7d32', tension:.25, pointRadius:3, fill:false}
    ]},
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{
        tooltip:{ callbacks:{ label(ctx){ const i=ctx.dataIndex; if(ctx.datasetIndex===2){ const e=byYear.get(years[i]); return `% same: ${pctArr[i]}% (${e.same} of ${e.joint})`; } return `${ctx.dataset.label}: ${ctx.parsed.y}`; } } },
        legend:{position:'bottom'}
      },
      scales:{
        y:{beginAtZero:true, title:{display:true, text:'Number of recorded votes'}, ticks:{precision:0}},
        y1:{position:'right', min:0, max:100, title:{display:true, text:'% voted the same'}, grid:{drawOnChartArea:false}, ticks:{callback:v=>v+'%'}}
      }
    }
  });
}
```

Note: byYear captured in closure — fine.

renderList(rows, ...):

```js
function renderList(rows, nameA, nameB){
  const showAll = showAllSel.value==='all';
  const list = showAll ? rows.slice() : rows.filter(x=>!x.same);
  list.sort((a,b)=> (b.r.date||'').localeCompare(a.r.date||'') || String(a.r.symbol||'').localeCompare(String(b.r.symbol||'')));
  listTitle.textContent = showAll ? `All joint votes (${list.length})` : `Votes where ${nameA} and ${nameB} differed (${list.length})`;
  howList.textContent = `How this is computed: every recorded vote in the current filter (${kindLabel(currentKind)}) where both States appear in the roll call${showAll?'':' and their votes differ'}, most recent first. ⚠ marks records where the official totals (yes/no/abstain) do not match counting the roll call.`;
  // header cells
  thA.textContent = nameA; thB.textContent = nameB;
  const tb = $('tbody'); tb.innerHTML='';
  list.forEach(x=> tb.appendChild(buildRow(x, nameA, nameB)));
  emptyList.hidden = list.length>0;
  if(!list.length) emptyList.textContent = 'No votes to show in the current filter.';
}
```

buildRow:

```js
function buildRow(x, nameA, nameB){
  const r = x.r;
  const tr = document.createElement('tr');
  const docUrl = r.doc_url || '';
  const recUrl = r.record_url || '';
  const link = docUrl || recUrl;
  const sym = r.symbol ? (link ? `<a href="${esc(link)}" target="_blank" rel="noopener">${esc(r.symbol)}</a>` : esc(r.symbol)) : '—';
  const title = r.title ? (link ? `<a href="${esc(link)}" target="_blank" rel="noopener">${esc(r.title)}</a>` : esc(r.title)) : '(untitled vote)';
  let warn = '';
  const mm = mismatchInfo(r);
  if (mm) warn = ` <span class="warn" title="Official totals (yes/no/abstain) ${r.yes}/${r.no}/${r.abstain} differ from counting the roll call: ${mm.Y}/${mm.N}/${mm.A}. Both are shown; neither is silently preferred.">⚠ totals ${r.yes}/${r.no}/${r.abstain} ≠ roll call ${mm.Y}/${mm.N}/${mm.A}</span>`;
  const kind = r.kind ? `<span class="kind ${esc(r.kind)}">${esc(r.kind==='amendment'?'Amendment':'Resolution')}</span>` : '';
  tr.innerHTML = `<td class="date">${esc(r.date || '—')}</td>
    <td>${kind}</td>
    <td class="titlecell">${title}<br><span class="sym">${sym}</span>${warn}</td>
    <td>${voteBadge(x.va)}</td>
    <td>${voteBadge(x.vb)}</td>
    <td class="match">${x.same ? '<span class="ok">✓ same</span>' : '<span class="no">✗ differs</span>'}</td>`;
  return tr;
}
function voteBadge(code){ return `<span class="vote ${esc(code)}" title="Roll-call vote ${esc(code)}">${esc(voteLabel(code))} (${esc(code)})</span>`; }
```

mismatchInfo(r):

```js
function rollCall(r){ const c={Y:0,N:0,A:0}; const v=r.votes||{}; for(const k in v){ if(c[v[k]]!==undefined) c[v[k]]++; } return c; }
function mismatchInfo(r){
  if (typeof r.yes!=='number'||typeof r.no!=='number'||typeof r.abstain!=='number') return null;
  const c = rollCall(r);
  if (c.Y===r.yes && c.N===r.no && c.A===r.abstain) return null;
  return c;
}
```

Kind label for other kinds: if r.kind is something else, show raw capitalized. `r.kind==='amendment'?'Amendment': r.kind==='resolution'?'Resolution': r.kind`. Fine.

Kind segmented buttons:

```js
const kinds = [['all','All'],['resolution','Resolutions'],['amendment','Amendments']];
const nRes = records.filter(r=>r.kind==='resolution').length;
const nAmd = records.filter(r=>r.kind==='amendment').length;
```

Build buttons in JS or static HTML with counts filled by JS. I'll build in JS into #kindSeg.

```js
function buildKindSeg(){
  const seg = $('kindSeg'); seg.innerHTML='';
  [['all',`All (${records.length})`],['resolution',`Resolutions (${nRes})`],['amendment',`Amendments (${nAmd})`]].forEach(([k,label])=>{
    const b=document.createElement('button'); b.type='button'; b.textContent=label; b.dataset.kind=k;
    b.className = k===currentKind?'active':'';
    b.setAttribute('aria-pressed', k===currentKind?'true':'false');
    b.addEventListener('click', ()=>{ currentKind=k; [...seg.children].forEach(c=>{c.classList.toggle('active', c.dataset.kind===k); c.setAttribute('aria-pressed', c.dataset.kind===k?'true':'false');}); render(); });
    seg.appendChild(b);
  });
}
```

kindLabel(k): k==='all' ? `all recorded votes (resolutions and amendments)` : k==='resolution' ? 'resolutions only' : 'amendments only'.

Events: selA/selB change → render; showAll change → render.

Init:

```js
if (!records.length){ document body message } 
```

Handle: if members.length<2 → show a notice in membersNote and hide controls? I'll set membersNote text and if <2, disable selects and show message. Simple: if members.length < 2, replace results area with message. Let me handle: 

```js
if (members.length < 2){ $('controls').style.display='none'; $('results').hidden=true; $('fatal').hidden=false; $('fatal').textContent = 'The data contains fewer than two States in any roll call, so no comparison is possible.'; return; }
```

Wrap init in function main().

Also years for header: compute min/max from records' year (or date). If none, omit.

Header title: "How two States vote at the Human Rights Council". Description line: `Source: ${HRC.title} — ${records.length} recorded votes (${minY}–${maxY}), roll-call votes Y/N/A. Only States that appear in at least one roll call are offered below.` If HRC.title missing, fallback 'Human Rights Council recorded votes'.

Also mention vote code meanings: `Y = ${voteLabel('Y')}, N = ..., A = ...` maybe in note. Add to membersNote: `Vote codes: Y = Yes, N = No, A = Abstain (as in the source).` Use voteLabel.

Now, "How this is computed" near every chart or number — I have howStats under cards, howChart under chart, howList under list. Good.

Also the requirement "Show on how many recorded votes both took part" — stat card. "how often they voted the same way" — card with %. "timeline by year" — chart. Good.

Let me also double check the "both took part" definition: both appear in votes map. Yes.

One more consideration: the selects should only include states that were Council members for at least one vote — that's exactly byCountry keys. Good. Note in UI: membersNote explains.

Now write final CSS carefully, professional look.

Let me now also think about the chart container height: `.chartWrap{background:#fff;border:1px solid var(--line);border-radius:8px;padding:16px;height:360px;}` canvas inside with maintainAspectRatio:false fills. Good.

Table container: white card too: `.tableWrap{background:#fff;border:1px solid var(--line);border-radius:8px;padding:8px 16px 16px;overflow-x:auto;}` — overflow-x auto as safety (though we aim no horizontal scroll; auto only kicks in if needed). Fine.

Now assemble everything. Also `<html lang="en">`. Title tag: "HRC vote comparison".

Let me write the code now, mindful of length.

Also: after code block, nothing. Before code block: ≤3 short sentences.

Potential pitfall: `selA.value` when options built — ensure selected set. fillSelect sets o.selected for match; also set sel.value after.

Default B computation needs records; fine.

Edge: uhri country name might match multiple? find first. OK.

Let me also make sure I don't call studio.ask — not needed.

Write the mismatch warning also maybe in stats? Not required.

One more: "Let me switch between resolutions, amendments, or both." — segmented control does that. Good.

Also list should include "both votes" — columns A and B show each state's vote. Header shows state names. Good.

Now write out the full HTML.

Also careful: in template literals inside script, I use `${...}` — fine in HTML file.

Escape function for attribute hrefs: esc handles quotes. URLs from data — fine.

Let me write:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Comparing two States' votes at the Human Rights Council</title>
<style>
:root{
  --accent:#1f6fb2; --accent-soft:#e8f1fa; --ink:#1d2833; --muted:#5c6b7a;
  --line:#d8e1ea; --bg:#f4f7fa; --card:#ffffff;
  --yes-bg:#e2f1e4; --yes-ink:#1e6b2f;
  --no-bg:#fbe3e3; --no-ink:#a02121;
  --abs-bg:#eceff3; --abs-ink:#55606c;
  --warn:#9a6200;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--bg)}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
header.top{background:var(--card);border-bottom:1px solid var(--line);padding:22px 0 18px}
h1{margin:0 0 6px;font-size:1.5rem;line-height:1.25;color:var(--accent)}
p.desc{margin:0;color:var(--muted);max-width:70ch}
main{padding:20px 0 48px}
h2{font-size:1.12rem;margin:30px 0 6px;color:var(--ink)}
.controls{display:flex;flex-wrap:wrap;gap:16px 24px;align-items:flex-end;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-top:18px}
.field{display:flex;flex-direction:column;gap:6px}
.field>label{font-size:.85rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
select,button{font:inherit}
select{padding:8px 10px;border:1px solid var(--line);border-radius:7px;background:#fff;color:var(--ink);max-width:300px}
.seg{display:flex;border:1px solid var(--line);border-radius:7px;overflow:hidden}
.seg button{border:0;background:#fff;padding:8px 14px;cursor:pointer;color:var(--ink);border-right:1px solid var(--line)}
.seg button:last-child{border-right:0}
.seg button.active{background:var(--accent);color:#fff}
.seg button:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
p.note{color:var(--muted);font-size:.9rem;margin:10px 2px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-top:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card .num{font-size:1.9rem;font-weight:700;color:var(--accent);line-height:1.15}
.card .lbl{color:var(--muted);font-size:.92rem;margin-top:2px}
p.breakdown{margin:10px 2px 0;color:var(--ink);font-size:.95rem}
p.how{color:var(--muted);font-size:.86rem;margin:8px 2px 0;max-width:90ch}
.chartWrap{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px 8px;margin-top:10px;height:380px}
.tableWrap{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:6px 16px 14px;margin-top:10px;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.93rem}
th{ text-align:left;font-size:.78rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);padding:10px 10px 8px;border-bottom:2px solid var(--line);white-space:nowrap}
td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:hover{background:#f7fafd}
td.date{white-space:nowrap;color:var(--muted)}
td.titlecell{overflow-wrap:anywhere;min-width:260px}
.sym{color:var(--muted);font-size:.85rem}
.sym a{color:var(--accent)}
a{color:var(--accent)}
.kind{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.78rem;font-weight:600;white-space:nowrap}
.kind.resolution{background:var(--accent-soft);color:var(--accent)}
.kind.amendment{background:#f1e8f8;color:#6b3fa0}
.vote{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.82rem;font-weight:600;white-space:nowrap}
.vote.Y{background:var(--yes-bg);color:var(--yes-ink)}
.vote.N{background:var(--no-bg);color:var(--no-ink)}
.vote.A{background:var(--abs-bg);color:var(--abs-ink)}
.match .ok{color:var(--yes-ink);font-weight:600;white-space:nowrap}
.match .no{color:var(--no-ink);font-weight:600;white-space:nowrap}
.warn{display:inline-block;margin-left:8px;color:var(--warn);font-size:.78rem;font-weight:600;cursor:help;white-space:normal}
.msg{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-top:18px;color:var(--muted)}
[hidden]{display:none !important}
footer{color:var(--muted);font-size:.85rem;padding:0 0 32px}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <h1>Comparing two States’ votes at the Human Rights Council</h1>
  <p class="desc" id="sourceLine"></p>
</div></header>
<main><div class="wrap">
  <section class="controls" id="controls" aria-label="Comparison settings">
    <div class="field"><label for="selA">State A</label><select id="selA"></select></div>
    <div class="field"><label for="selB">State B</label><select id="selB"></select></div>
    <div class="field"><label id="kindLabel">Votes included</label><div class="seg" id="kindSeg" role="group" aria-labelledby="kindLabel"></div></div>
    <div class="field"><label for="showAll">List below</label><select id="showAll">
      <option value="diff">Differing votes only</option>
      <option value="all">All joint votes</option>
    </select></div>
  </section>
  <p class="note" id="membersNote"></p>
  <p class="msg" id="fatal" hidden></p>
  <p class="msg" id="sameMsg" hidden></p>

  <section id="results" hidden>
    <div class="cards">
      <div class="card"><div class="num" id="statJoint">0</div><div class="lbl">recorded votes both States took part in</div></div>
      <div class="card"><div class="num" id="statSame">0</div><div class="lbl">of those, votes where they voted the same</div></div>
      <div class="card"><div class="num" id="statDiff">0</div><div class="lbl">votes where they differed</div></div>
    </div>
    <p class="breakdown" id="breakdown"></p>
    <p class="how" id="howStats"></p>

    <h2>Timeline by year</h2>
    <div class="chartWrap" id="chartWrap"><canvas id="chart" aria-label="Timeline of joint votes by year"></canvas></div>
    <p class="msg" id="chartEmpty" hidden>No recorded votes in the current filter where both States took part, so there is no timeline to draw.</p>
    <p class="how" id="howChart"></p>

    <h2 id="listTitle"></h2>
    <p class="how" id="howList"></p>
    <div class="tableWrap">
      <table>
        <thead><tr>
          <th>Date</th><th>Kind</th><th>Vote (title &amp; symbol)</th>
          <th id="thA">State A</th><th id="thB">State B</th><th>Same?</th>
        </tr></thead>
        <tbody id="tbody"></tbody>
      </table>
      <p class="msg" id="emptyList" hidden></p>
    </div>
  </section>
  <footer>All counts, filters and charts on this page are computed in your browser from the loaded dataset; nothing is estimated and no data leaves the page.</footer>
</div></main>
<script>
...
</script>
</body>
</html>
```

Wait: emptyList inside tableWrap but outside table — fine, but it's a `<p>` after table; ok.

Now the script:

```js
(function(){
"use strict";
var DATA = window.WORKSHOP_DATA || {};
var HRC = DATA.hrc || {};
var records = Array.isArray(HRC.records) ? HRC.records : [];
var countryNames = HRC.countries || {};
var voteCodes = HRC.vote_codes || {};

function $(id){ return document.getElementById(id); }
function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
var FALLBACK_VOTES = {Y:'Yes', N:'No', A:'Abstain'};
function voteLabel(code){ return (voteCodes && voteCodes[code]) || FALLBACK_VOTES[code] || code; }
function yearOf(r){ if (typeof r.year === 'number') return r.year; var m = /^(\d{4})/.exec(r.date||''); return m ? +m[1] : null; }
function kindLabel(k){ return k==='all' ? 'all recorded votes (resolutions and amendments)' : (k==='resolution' ? 'resolutions only' : 'amendments only'); }
function kindBadge(r){ var k = r.kind || ''; var label = k==='resolution' ? 'Resolution' : k==='amendment' ? 'Amendment' : (k || '—'); return '<span class="kind ' + esc(k) + '">' + esc(label) + '</span>'; }
function rollCall(r){ var c={Y:0,N:0,A:0}; var v=r.votes||{}; for (var iso in v){ if (Object.prototype.hasOwnProperty.call(v,iso) && c[v[iso]]!==undefined) c[v[iso]]++; } return c; }
function mismatchInfo(r){ if (typeof r.yes!=='number'||typeof r.no!=='number'||typeof r.abstain!=='number') return null; var c=rollCall(r); if (c.Y===r.yes && c.N===r.no && c.A===r.abstain) return null; return c; }

// index: iso -> Map(record -> vote)
var byCountry = new Map();
records.forEach(function(r){ var v = r.votes || {}; for (var iso in v){ if (!Object.prototype.hasOwnProperty.call(v,iso)) continue; if (!byCountry.has(iso)) byCountry.set(iso, new Map()); byCountry.get(iso).set(r, v[iso]); } });
var members = Array.from(byCountry.keys()).map(function(iso){ return {iso:iso, name: countryNames[iso] || iso}; })
  .sort(function(a,b){ return a.name.localeCompare(b.name); });
```

Then main():

```js
var selA=$('selA'), selB=$('selB'), showAllSel=$('showAll'), results=$('results');
var currentKind='all', chart=null;

function fillSelect(sel, selectedIso){
  sel.innerHTML='';
  members.forEach(function(m){ var o=document.createElement('option'); o.value=m.iso; o.textContent=m.name+' ('+m.iso+')'; if (m.iso===selectedIso) o.selected=true; sel.appendChild(o); });
  if (selectedIso) sel.value=selectedIso;
}
```

Default picks:

```js
function defaultA(){ var uc = (DATA.uhri && DATA.uhri.country) || ''; var m = members.find(function(x){ return x.name===uc; }); return (m || members[0] || {}).iso; }
function defaultB(isoA){
  var mapA = byCountry.get(isoA); var best=null;
  members.forEach(function(m){
    if (m.iso===isoA) return;
    var mapB = byCountry.get(m.iso), joint=0, diff=0;
    records.forEach(function(r){ var va=mapA.get(r), vb=mapB.get(r); if (va!==undefined && vb!==undefined){ joint++; if (va!==vb) diff++; } });
    if (!best || diff>best.diff || (diff===best.diff && joint>best.joint) || (diff===best.diff && joint===best.joint && m.name<best.name)) best={iso:m.iso, diff:diff, joint:joint, name:m.name};
  });
  return best ? best.iso : (members[1]||{}).iso;
}
```

Header:

```js
function fillHeader(){
  var ys = records.map(yearOf).filter(function(y){ return y!=null; });
  var range = ys.length ? Math.min.apply(null,ys)+'–'+Math.max.apply(null,ys) : 'n/a';
  $('sourceLine').textContent = 'Source: ' + (HRC.title || 'Human Rights Council recorded votes') + ' — ' + records.length + ' recorded votes, ' + range + '. Each record is a recorded vote (resolution or amendment) with the roll call of the Council members (Y/N/A = ' + voteLabel('Y') + '/' + voteLabel('N') + '/' + voteLabel('A') + '). Only States that appear in at least one roll call are offered below.';
}
```

Hmm voteLabel('Y') might be "Yes" etc. Good.

membersNote:

```js
$('membersNote').textContent = members.length + ' States appear in at least one roll call and can be compared. “Both took part” means both States appear in a vote’s roll call.';
```

Kind seg build as planned.

render():

```js
function render(){
  var isoA=selA.value, isoB=selB.value;
  if (!isoA || !isoB){ results.hidden=true; return; }
  var nameA=countryNames[isoA]||isoA, nameB=countryNames[isoB]||isoB;
  if (isoA===isoB){ results.hidden=true; var sm=$('sameMsg'); sm.hidden=false; sm.textContent='State A and State B are the same State ('+nameA+'). Pick two different States to compare.'; return; }
  $('sameMsg').hidden=true; results.hidden=false;
  var mapA=byCountry.get(isoA), mapB=byCountry.get(isoB);
  var rows=[];
  records.forEach(function(r){
    if (currentKind!=='all' && r.kind!==currentKind) return;
    var va=mapA.get(r), vb=mapB.get(r);
    if (va===undefined || vb===undefined) return;
    rows.push({r:r, va:va, vb:vb, same: va===vb});
  });
  var joint=rows.length, same=0, both={Y:0,N:0,A:0};
  rows.forEach(function(x){ if (x.same){ same++; if (both[x.va]!==undefined) both[x.va]++; } });
  var diff=joint-same;
  $('statJoint').textContent=joint;
  $('statSame').textContent= joint ? same+' ('+Math.round(100*same/joint)+'%)' : '0';
  $('statDiff').textContent=diff;
  $('breakdown').textContent='Of the '+joint+' joint votes: both Yes '+both.Y+', both No '+both.N+', both Abstain '+both.A+'. Filter: '+kindLabel(currentKind)+'.';
  $('howStats').textContent='How this is computed: for every recorded vote in the current filter, each State’s roll-call code (Y/N/A) is looked up. “Both took part” = both States appear in that roll call; “same” = identical code. These are exact counts of the loaded records, not estimates.';
  renderChart(rows);
  renderList(rows, nameA, nameB);
}
```

renderChart as planned; note closure over byYear for tooltip.

renderList as planned.

buildRow as planned.

Events:

```js
selA.addEventListener('change', render);
selB.addEventListener('change', render);
showAllSel.addEventListener('change', render);
```

Init:

```js
function main(){
  if (!records.length){ $('fatal').hidden=false; $('fatal').textContent='The loaded dataset contains no recorded votes, so there is nothing to compare.'; $('controls').style.display='none'; return; }
  fillHeader();
  if (members.length<2){ $('fatal').hidden=false; $('fatal').textContent='Fewer than two States appear in any roll call in the loaded data, so no comparison is possible.'; $('controls').style.display='none'; return; }
  var a=defaultA(), b=defaultB(a);
  fillSelect(selA,a); fillSelect(selB,b);
  buildKindSeg();
  $('membersNote').textContent = ...;
  render();
}
main();
```

Also if b undefined (only one member) — handled by members.length<2 check.

renderChart details:

```js
function renderChart(rows){
  var byYear=new Map();
  rows.forEach(function(x){ var y=yearOf(x.r); if(y==null) return; if(!byYear.has(y)) byYear.set(y,{joint:0,same:0}); var e=byYear.get(y); e.joint++; if(x.same) e.same++; });
  var years=Array.from(byYear.keys()).sort(function(a,b){return a-b;});
  if (chart){ chart.destroy(); chart=null; }
  if (!years.length || !window.Chart){ $('chartWrap').style.display='none'; $('chartEmpty').hidden=false; return; }
  $('chartWrap').style.display=''; $('chartEmpty').hidden=true;
  var jointArr=years.map(function(y){return byYear.get(y).joint;});
  var sameArr=years.map(function(y){return byYear.get(y).same;});
  var pctArr=years.map(function(y){var e=byYear.get(y); return e.joint? Math.round(100*e.same/e.joint): null;});
  chart = new Chart($('chart').getContext('2d'), {
    type:'bar',
    data:{ labels: years.map(String), datasets:[
      {type:'bar', label:'Votes both took part', data:jointArr, backgroundColor:'#1f6fb2', borderRadius:3, maxBarThickness:42},
      {type:'bar', label:'Voted the same', data:sameArr, backgroundColor:'#a9cdea', borderRadius:3, maxBarThickness:42},
      {type:'line', label:'% voted the same', data:pctArr, yAxisID:'y1', borderColor:'#2e7d32', backgroundColor:'#2e7d32', fill:false, tension:.25, pointRadius:3}
    ]},
    options:{
      responsive:true, maintainAspectRatio:false,
      interaction:{mode:'index', intersect:false},
      plugins:{
        legend:{position:'bottom'},
        tooltip:{ callbacks:{ label:function(ctx){ if(ctx.datasetIndex===2){ var e=byYear.get(years[ctx.dataIndex]); return '% voted the same: '+pctArr[ctx.dataIndex]+'% ('+e.same+' of '+e.joint+')'; } return ctx.dataset.label+': '+ctx.parsed.y; } } }
      },
      scales:{
        y:{beginAtZero:true, title:{display:true,text:'Recorded votes'}, ticks:{precision:0}},
        y1:{position:'right', min:0, max:100, title:{display:true,text:'% voted the same'}, grid:{drawOnChartArea:false}, ticks:{callback:function(v){return v+'%';}}}
      }
    }
  });
  $('howChart').textContent='How this is computed: one group of bars per year (from each record’s year), counting only votes in the current filter where both States appear in the roll call; the green line is the share of those joint votes that were the same (right axis).';
}
```

renderList:

```js
function renderList(rows, nameA, nameB){
  var showAll = showAllSel.value==='all';
  var list = showAll ? rows.slice() : rows.filter(function(x){ return !x.same; });
  list.sort(function(a,b){ var da=a.r.date||'', db=b.r.date||''; if (da!==db) return da<db?1:-1; return String(a.r.symbol||'').localeCompare(String(b.r.symbol||'')); });
  $('listTitle').textContent = showAll ? 'All joint votes ('+list.length+')' : 'Votes where '+nameA+' and '+nameB+' differed ('+list.length+')';
  $('howList').textContent = 'How this is computed: every recorded vote in the current filter ('+kindLabel(currentKind)+') where both States appear in the roll call'+(showAll?'':' and their codes differ')+', most recent first. The symbol links to the UN document in a new tab. ⚠ marks records where the official totals (yes/no/abstain) do not match counting the roll call — both figures are shown, neither is silently preferred.';
  $('thA').textContent = nameA; $('thB').textContent = nameB;
  var tb=$('tbody'); tb.innerHTML='';
  list.forEach(function(x){ tb.appendChild(buildRow(x)); });
  $('emptyList').hidden = list.length>0;
  if (!list.length) $('emptyList').textContent = 'No votes to show for this combination of States and filter.';
}
```

buildRow:

```js
function voteBadge(code){ return '<span class="vote '+esc(code)+'" title="Roll-call code '+esc(code)+'">'+esc(voteLabel(code))+' ('+esc(code)+')</span>'; }
function buildRow(x){
  var r=x.r;
  var link = r.doc_url || r.record_url || '';
  var sym = r.symbol ? (link ? '<a href="'+esc(link)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>' : esc(r.symbol)) : '—';
  var title = r.title ? (link ? '<a href="'+esc(link)+'" target="_blank" rel="noopener">'+esc(r.title)+'</a>' : esc(r.title)) : '(untitled vote)';
  var warn='';
  var mm=mismatchInfo(r);
  if (mm) warn=' <span class="warn" title="Official totals (yes/no/abstain) are '+r.yes+'/'+r.no+'/'+r.abstain+', but counting the roll call gives '+mm.Y+'/'+mm.N+'/'+mm.A+'. Both are shown; neither is silently preferred.">⚠ totals '+r.yes+'/'+r.no+'/'+r.abstain+' ≠ roll call '+mm.Y+'/'+mm.N+'/'+mm.A+'</span>';
  var tr=document.createElement('tr');
  tr.innerHTML='<td class="date">'+esc(r.date||'—')+'</td>'
    +'<td>'+kindBadge(r)+'</td>'
    +'<td class="titlecell">'+title+'<br><span class="sym">'+sym+'</span>'+warn+'</td>'
    +'<td>'+voteBadge(x.va)+'</td>'
    +'<td>'+voteBadge(x.vb)+'</td>'
    +'<td class="match">'+(x.same?'<span class="ok">✓ same</span>':'<span class="no">✗ differs</span>')+'</td>';
  return tr;
}
```

Note: symbol should link to doc_url specifically; if doc_url empty we fall back to record_url — acceptable and noted. Actually rule says "linked to doc_url in a new tab" — when doc_url exists we use it. Good.

buildKindSeg:

```js
function buildKindSeg(){
  var nRes=records.filter(function(r){return r.kind==='resolution';}).length;
  var nAmd=records.filter(function(r){return r.kind==='amendment';}).length;
  var seg=$('kindSeg'); seg.innerHTML='';
  [['all','All ('+records.length+')'],['resolution','Resolutions ('+nRes+')'],['amendment','Amendments ('+nAmd+')']].forEach(function(pair){
    var k=pair[0], label=pair[1];
    var b=document.createElement('button'); b.type='button'; b.textContent=label; b.dataset.kind=k;
    b.className = (k===currentKind)?'active':''; b.setAttribute('aria-pressed', k===currentKind?'true':'false');
    b.addEventListener('click', function(){ currentKind=k; Array.prototype.forEach.call(seg.children, function(c){ var on=c.dataset.kind===k; c.classList.toggle('active',on); c.setAttribute('aria-pressed', on?'true':'false'); }); render(); });
    seg.appendChild(b);
  });
}
```

Init main as above; also set membersNote.

Check: `members.find` — Array.prototype.find fine.

One concern: defaultB loops members × records — members maybe ~80, records maybe ~1000 → 80k×... wait members.forEach with inner records.forEach → 80 × 1000 = 80k iterations, trivial.

Also note: `mapA.get(r)` — r is record object; Map keyed by object identity — records array elements, same references. Good.

Potential issue: duplicate record objects? No.

Also `selA.value` after fillSelect — set. If defaultA undefined (no members) — handled earlier.

Now double-check the header description includes n and years — yes.

"How this is computed" near every chart or number — stats have howStats, chart howChart, list howList. The breakdown line is part of stats. Good.

Also the requirement "Every row that shows a document has its symbol, linked to doc_url in a new tab" — done.

"Where the official totals differ from the roll call, show a small warning on that row" — done in list rows. Should the warning also appear somewhere else? Only rows exist in list. Fine.

Also maybe show warning count in list header note — the howList mentions it. OK.

Now, one more nuance: "Pick two States (only those that were Council members for at least one vote)" — our selects only include such states, and note says so. Good.

Check no external loads: only inline. Chart.js from window.Chart. Good.

Line count: let's estimate ~380 lines. Fine.

Also ensure `interaction:{mode:'index'}` works in Chart.js 4 — yes.

Edge: pctArr with null when joint 0 — can't happen since year only added when row exists (joint≥1). Fine.

Edge: records with kind other than resolution/amendment — included in 'all', excluded from both specific filters. kindBadge shows raw kind. Fine.

Also the `title` attribute on warn span contains numbers — fine.

One more: the `esc` in class attribute for kind: `class="kind '+esc(k)+'"` — k like "resolution" safe.

Also `voteBadge` class `vote Y` — code could be other letter; class safe after esc.

Let me also add `rel="noopener"` on links — done.

Also add `<meta name="color-scheme" content="light">`? Not necessary.

Font base 16px — body font 16px. Good.

Now, the intro sentences before code: "I built an HRC vote-comparison tool..." Keep ≤3 sentences.

Let me also double check the tooltip callback uses `years` and `byYear` from closure — defined in renderChart before chart creation. Yes.

One thing: when chart destroyed and re-created on same canvas — Chart.js 4 handles destroy properly. Good.

Also when results hidden (same state), chart remains but hidden — fine.

Also initial `results` has `hidden` attribute; render() unhides.

Also `showAllSel` default value 'diff'.

Write membersNote: `members.length + ' States appear in at least one roll call (i.e. were Council members for at least one recorded vote) and can be picked above. Vote codes: Y = ' + voteLabel('Y') + ', N = ' + voteLabel('N') + ', A = ' + voteLabel('A') + '.'`

Hmm voteLabel uses voteCodes which might be like {"Y":"Yes","N":"No","A":"Abstain"} — good.

Now finalize. Also add `lang="en"`.

Also consider: the user said "Show on how many recorded votes both took part" — maybe also show total records in filter? The breakdown mentions filter. Fine.

Let me write the final file carefully and completely.

Also small detail: `header.top` uses class wrap inside. main uses wrap.

Check the `p.msg` inside tableWrap for emptyList — style ok.

Also `footer` inside wrap.

Double-check: no `fetch`, no external. Yes.

One more improvement: in the stats, maybe also show "agreement" wording. Fine as is.

Also the list title when showAll: "All joint votes (n)" — includes same/diff marker column. Good.

Potential subtle bug: `fillSelect` sets `o.selected` then `sel.value=selectedIso` — fine.

In `defaultB`, if mapA undefined (isoA not in byCountry — can't happen since defaultA from members). OK.

Also `records.forEach` inside defaultB uses mapA.get(r) — mapA exists.

Alright, also handle `HRC.vote_codes` possibly mapping to longer labels — used.

Now write it all out. I'll aim for clean formatting.

Also: the h1 uses a typographic apostrophe — fine.

Let me count roughly and write final answer. Also ensure the code block starts with `<!doctype html>`.

One more check on requirement: "Show ... how often they voted the same way" — card shows count + %. Good.

"timeline by year" — chart. Good.

"List the votes where they differed, with the resolution title, date, both votes and a link." — table. Good.

"Let me switch between resolutions, amendments, or both." — segmented. Good.

"Where the official totals differ from the roll call, show a small warning on that row." — ⚠ badge. Good.

Also "The app itself must explain what it shows" — how-notes everywhere. Good.

Write final.