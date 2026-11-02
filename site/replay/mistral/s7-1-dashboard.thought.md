The user wants a dashboard app for UN human rights recommendations to Kenya (country read from data). Let me build a single HTML file with:

1. Title with country name, one-line description (source, count, year range)
2. Filter bar: mechanism dropdown, body dropdown, year range (first/last), SDG dropdown, keyword box, Reset button
3. "Showing X of Y records" + plain description of active filters
4. Horizontal bar chart of top 10 themes (Chart.js), longest on top, counts labeled, note about multi-counting
5. Table: date, body, symbol linked, first line of text; expandable rows showing full text + themes + SDGs; 100 rows at a time with "Show more"

Rules:
- Total and year range from all records
- Filters: mechanism, body, year range, SDG, keyword (case-insensitive on text)
- Chart: count each theme item per record, sort by count desc, ties alphabetical, top 10
- First line: text up to first line break or 160 chars + "…"
- doc_url missing → unlinked symbol; symbol missing → "(no symbol)"
- Missing date → "date unknown", sorted last; missing body → "unknown"
- Empty themes/sdgs → "none recorded" in expanded row
- No matches → "No records match these filters"

Design: clean, professional, accent #1f6fb2, system fonts, 16px base, no external loads, Chart.js 4 preloaded as window.Chart.

Let me write the code carefully.

Key details:
- Sorting newest first: by date descending; missing date sorted last. Use date string comparison (ISO format works), or year. I'll sort by date string desc, with missing dates last. Actually "newest first" — use date if present, else year? Spec says missing date → "date unknown", sorted last. So sort: records with date by date desc, then records without date at end (maybe by year desc among themselves, but keep simple: stable).
- Body dropdown: unique bodies from data, sorted alphabetically.
- Mechanism dropdown: unique mechanisms.
- SDG dropdown: from sdgs present in records, using sdg_names for labels. Show "SDG 16: Peace, justice..." etc. Include "All SDGs" default.
- Year inputs: two number boxes, min/max from data. Default min and max.
- Keyword: input, case-insensitive substring on text.
- Reset button restores defaults.

Filter description: build parts like "Treaty bodies", "2015–2020", "keyword: torture", "SDG 16: ...", body name. Join with " · ". If none active: "no filters".

Chart: horizontal bar chart with Chart.js. indexAxis: 'y'. Data sorted so longest on top — in Chart.js with indexAxis 'y', the first item appears at the bottom by default? Actually with indexAxis 'y', categories are on y-axis, and by default the first category is at the bottom... Let me think: In Chart.js, for a horizontal bar chart, categories are displayed bottom-to-top in order by default? Actually no — with indexAxis: 'y', the first data point appears at the top? Hmm. In Chart.js v3/v4, for horizontal bars, the y-axis categories go from bottom to top in the order given, meaning the first item is at the bottom. To have longest on top, reverse the array (so longest is last, appearing at top). Common practice: reverse data so largest appears at top. I'll sort ascending by count and let the chart display... safer: sort descending, then reverse for chart data so that the largest ends up at top. Let me just do: sorted desc by count (ties alphabetical asc), then chartData = sorted.slice().reverse() so index 0 (smallest) is at bottom and largest at top. Actually with indexAxis 'y', Chart.js renders category axis with first item at the bottom by default (like a normal y axis increases upward). So to get largest on top, largest must be last in the array. So reverse the desc-sorted array → ascending order in array, largest last → top. Yes.

Alternatively set ticks reverse... simpler to reverse array.

Data labels: show counts. Chart.js doesn't have built-in data labels without plugin. I can show counts in the category labels themselves: "Theme name (12)". That satisfies "each labelled with its count". Good, avoids plugin.

Table: build rows in JS. Each row: date cell, body cell, symbol cell (link), first-line cell. Click row toggles expanded row below with full text, themes, SDGs. Use event delegation.

Pagination: show 100 at a time, "Show more" button increments.

Expand: clicking row toggles. Need to be careful with "Show more" — expanded state per record id; when re-rendering, keep expanded set.

First line: text up to first "\n" or 160 chars + "…". Spec: "the first line is `text` up to its first line break or 160 characters plus '…'". So: take text, find first line break; if exists and index < 160? Hmm — "up to its first line break or 160 characters" — take min(firstLineBreakIndex, 160), then if truncated (i.e., there's more text beyond), add "…". I'll implement: let cut = text.indexOf("\n"); if cut === -1 || cut > 160 → cut = 160; firstLine = text.slice(0, cut); if text.length > cut → firstLine += "…". Actually if the first line break is at position 200, we cut at 160 and add "…". If line break at 50, cut at 50, and if more text remains, add "…". Edge: if text length <= cut, no ellipsis. Good.

Expanded view: full text in a <pre> or div with white-space: pre-wrap to preserve verbatim. Plus themes list and SDG list (with names from sdg_names), or "none recorded".

SDG display: sdgs are numbers; sdg_names keys are strings like "16". Display "SDG 16 — Peace, justice and strong institutions" or use sdg_targets? The spec says expanded row shows "its themes and SDGs". I'll show SDG numbers with names: "SDG 5: Gender equality". Use sdg_names[String(n)] fallback "SDG n".

Header line: source, total records, earliest–latest year. Source: WORKSHOP_DATA.uhri.source (and source_url maybe). "Source: {source} · {count} records · {minYear}–{maxYear}". Title: "UN human rights recommendations to {country}".

Also "Only recommendations and concerns/observations are counted anywhere" — filter records to type "Recommendations" or "Concerns/Observations". The data may contain other types? Spec says type is mostly those two. I'll filter: rec.type === 'Recommendations' || rec.type === 'Concerns/Observations'. Hmm, but "Showing X of Y" — Y should be total records? "Total and year range come from counting all records". And test 1: "Showing X of Y has X equal to Y" on load. If some records have other types, X≠Y. Safer: Y = count of all records in file? But rule says only recommendations and concerns counted anywhere. Hmm. The sample data shows only those two types. I'll define the working set as records whose type is Recommendations or Concerns/Observations (case-insensitive contains?), and Y = that set's size, total line uses all records count... Actually "Total and year range come from counting all records and taking the smallest and largest year" — the header line total = all records. And "Showing X of Y" — Y should probably be the same total. To make test 1 pass (X=Y on load), Y must equal the unfiltered count. If all records are recs/concerns, both interpretations coincide. I'll use: allRecords = records; eligible = records.filter(type is Recommendations or Concerns/Observations); but if eligible.length === records.length it's the same. To be safe and consistent, I'll just use all records as the base (the file is described as "recommendations to the participant's country"), and apply the type rule by filtering only if other types exist... Simplest robust approach: base = records where type is one of the two (case-insensitive match on 'recommendation' or 'concern'); header total = records.length (all records), year range from all records. If all are the two types, X=Y on load. If some aren't, X<Y on load which would fail test 1... but the file is titled "recommendations and observations" so presumably all records qualify. Hmm, risk either way. The rule explicitly says "Only recommendations and concerns/observations are counted anywhere." So counting anywhere (including the "Showing X of Y") should only count those. And the header total "total number of records" from the file — count field exists: WORKSHOP_DATA.uhri.count. I'll use uhri.count for the header line ("total number of records" read from file) and for Y use the filtered base. If they differ slightly, that's per the rules. Actually to guarantee test 1, maybe Y should be the base set size and header shows count from file. Test says "Showing X of Y has X equal to Y" — with no filters, X = base size = Y. That works regardless. Header line: "source, total number of records, earliest–latest year, all read from the file" — use uhri.count and min/max year over all records. Fine.

Let me decide: base = records.filter(r => /recommendation|concern/i.test(r.type || '')). If that yields 0 (weird types), fall back to all records. Good defensive.

Year range: min/max over all records' year (missing year ignored).

Filters:
- mechanism: exact match on r.mechanism
- body: exact match on r.body
- yearFrom, yearTo: r.year >= from && r.year <= to (missing year → excluded when year filter active? If user sets range, records without year can't match; but default range is full min–max, and records missing year... hmm. If a record has no year, does it pass the default year filter? To keep X=Y on load, records without year should pass when filter is at default. Simplest: treat missing year as passing only if the range covers... I'll treat missing year as excluded only if user changed the range from default? That's hacky. Alternative: missing year records always pass year filter? That could be wrong if user narrows. I'll do: if r.year is a number, check range; if missing, include only when the active range equals the full default range. Hmm, complexity. Simpler: missing year → passes year filter always? The spec doesn't say. Given "Missing date: sorted last" but nothing about year filtering, I'll include records with missing year regardless of year filter (they have unknown year, can't be excluded by year). Actually that seems reasonable and keeps X=Y. I'll do that: year filter applies only when year is present.

Hmm, but a diplomat narrowing to 2015–2020 would see undated records. Acceptable; spec silent. Keep simple: missing year passes.

- SDG: r.sdgs includes selected number
- keyword: r.text.toLowerCase().includes(kw.toLowerCase())

Filter description parts:
- mechanism if not "all": mechanism value
- body if not "all": body value
- year if changed from default: "YYYY–YYYY" (if from===to, just "YYYY")
- SDG if selected: "SDG n: name"
- keyword if non-empty: `keyword: "kw"`
Join " · ", or "no filters active" if empty.

Chart note: "A record with several items is counted once for each." — show below chart. Also "How this is computed" note near chart: e.g., "Counts themes across the X matching records; each record contributes one count per theme it carries; top 10 shown, ties broken alphabetically."

Table columns: Date | Body | Symbol | Text (first line). Mechanism maybe not required — spec lists date, body, symbol, first line. Keep those four. Maybe include mechanism in expanded view. Expanded shows full paragraph + themes + SDGs. I'll also show mechanism/type/date in expanded meta line — helpful, allowed ("keep it simple" — but showing mechanism in expanded is fine). Spec: "expands it to show the full paragraph with its themes and SDGs". I'll show full text, then themes and SDGs lines. Maybe also mechanism and type small. Keep it: full text verbatim in pre-wrap, then "Themes: ..." and "SDGs: ...". Also maybe section. Keep simple: themes + SDGs as required.

Row click toggles expand — but clicking the symbol link shouldn't toggle; stop propagation on link click.

"Show more": visibleCount starts 100; button shows if more remain: "Show more (N remaining)" or just "Show more". Clicking adds 100.

No matches: hide chart, show "No records match these filters" message; table area shows that message too. Spec: show that instead of empty chart. I'll show the message in place of chart and table.

Chart rendering: destroy previous chart instance before creating new (Chart.getChart or keep reference and destroy).

Chart.js horizontal bar: 
```js
new Chart(ctx, {type:'bar', data:{labels, datasets:[{data, backgroundColor:'#1f6fb2'}]}, options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}, tooltip:{callbacks:{label:...}}}, scales:{x:{beginAtZero:true, ticks:{precision:0}}}}})
```
Labels include count: `${theme} (${count})`. Tooltip can show "N records". Height: set container height based on number of bars, e.g., bars*28+40 px, with maintainAspectRatio false.

Also add a "How this is computed" note under chart.

Styling: light background (#f5f7fa), white cards, accent #1f6fb2, system font stack, base 16px. Filter bar as a card with flex-wrap controls. Table full width, zebra rows, hover. Expanded row with light blue background.

Header: title h1, subtitle line with source/count/years.

Let me also handle doc_url missing: `<span class="sym">symbol</span>` unlinked; symbol missing: "(no symbol)".

Sorting: newest first. Compare by date string desc; missing date last. If both have dates, compare strings (ISO dates compare correctly). If equal or both missing, fallback year desc, then keep stable. Implementation:

```js
function sortRecs(list){
  return list.slice().sort((a,b)=>{
    const da=a.date||'', db=b.date||'';
    if(da && db){ if(db!==da) return db.localeCompare(da); }
    else if(da && !db) return -1;
    else if(!da && db) return 1;
    const ya=a.year||0, yb=b.year||0;
    return yb-ya;
  });
}
```

Body dropdown options: unique bodies sorted; label "All bodies". Mechanism: unique mechanisms sorted; "All mechanisms". SDG options: collect all sdgs across base records, sort numerically; label `SDG ${n}: ${sdg_names[String(n)] || ''}`. Default "All SDGs".

Year inputs: type="number", min=minYear, max=maxYear, value=minYear/maxYear. On change, clamp? Just read values; if from>to, swap or treat as empty range → no matches. I'll normalize: if from>to, no records match (or swap). I'll just apply as-is (from<=year<=to), which yields none if inverted — fine, but maybe swap for friendliness. Keep as-is, simple.

Reset: set mechanism/body/sdg to '', years to min/max, keyword '', re-render.

Re-render on any input event ('input' for text, 'change' for selects/numbers).

Rendering function render(): compute filtered, update count line, description, chart, table.

Table building with DOM creation to avoid HTML injection issues with text (text may contain < >). Use textContent everywhere. For symbol link, create <a> with href=doc_url, target=_blank, rel=noopener, textContent=symbol.

Expanded row: a <tr class="detail"><td colspan=4>... with full text in <div class="fulltext"> (white-space:pre-wrap, textContent=full text), then themes/sdgs.

Themes in expanded: r.themes join ", " or "none recorded". SDGs: map to "SDG n (name)" join ", " or "none recorded".

Also show paragraph number? The text includes "54. ..." already at start. Fine.

Count line: "Showing X of Y records" where Y = base.length. Description: "Filters: ..." or "No filters — showing all records." Spec: "a plain description of the active filters (e.g. 'Treaty bodies · 2015–2020 · keyword: torture')". I'll render: `Active filters: Treaty bodies · 2015–2020 · keyword: torture` or `Active filters: none (all records)`.

Header description line: `Source: ${uhri.source} · ${uhri.count} records · ${minYear}–${maxYear}`. Maybe include source_url link if present. uhri has source and source_url. I'll link source if source_url exists.

Title: `UN human rights recommendations to ${country}`.

Now write the full HTML. Keep under 700 lines. Let me draft.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations</title>
<style>
  :root{ --accent:#1f6fb2; --bg:#f4f6f9; --card:#ffffff; --ink:#1c2733; --muted:#5b6b7b; --line:#dde4ec; }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
  .wrap{max-width:1100px;margin:0 auto;padding:24px 20px 60px;}
  header h1{font-size:1.6rem;margin:0 0 6px;color:var(--ink);}
  .sub{color:var(--muted);margin:0 0 20px;}
  .sub a{color:var(--accent);}
  .card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-bottom:18px;}
  .filters{display:flex;flex-wrap:wrap;gap:12px 16px;align-items:flex-end;}
  .filters label{display:flex;flex-direction:column;font-size:.8rem;color:var(--muted);gap:4px;font-weight:600;}
  .filters select,.filters input{font:inherit;padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--ink);min-width:150px;}
  .filters input[type=number]{width:90px;min-width:90px;}
  .filters input[type=text]{min-width:200px;}
  button{font:inherit;padding:7px 14px;border:1px solid var(--accent);background:var(--accent);color:#fff;border-radius:6px;cursor:pointer;}
  button.ghost{background:#fff;color:var(--accent);}
  .status{display:flex;flex-wrap:wrap;gap:6px 18px;align-items:baseline;margin-bottom:14px;}
  .status .count{font-weight:700;font-size:1.05rem;}
  .status .desc{color:var(--muted);}
  .note{font-size:.85rem;color:var(--muted);margin-top:8px;}
  .chartbox{position:relative;}
  table{width:100%;border-collapse:collapse;}
  th{text-align:left;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);padding:8px 10px;border-bottom:2px solid var(--line);}
  td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top;}
  tbody tr.data{cursor:pointer;}
  tbody tr.data:hover{background:#eef4fa;}
  tr.detail td{background:#f2f7fc;}
  .fulltext{white-space:pre-wrap;background:#fff;border:1px solid var(--line);border-radius:6px;padding:10px 12px;margin:6px 0 10px;}
  .meta{font-size:.9rem;color:var(--muted);}
  .meta b{color:var(--ink);}
  a.sym{color:var(--accent);word-break:break-all;}
  .nomatch{padding:24px;text-align:center;color:var(--muted);font-weight:600;}
  .more{display:block;margin:14px auto 0;}
  .tag{display:inline-block;background:#e8f0f8;color:#17537f;border-radius:4px;padding:1px 7px;margin:1px 3px 1px 0;font-size:.85rem;}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1 id="title"></h1>
    <p class="sub" id="subline"></p>
  </header>
  <section class="card">
    <div class="filters" id="filters">
      <label>Mechanism <select id="f-mech"></select></label>
      <label>Body / mandate <select id="f-body"></select></label>
      <label>First year <input type="number" id="f-y1"></label>
      <label>Last year <input type="number" id="f-y2"></label>
      <label>SDG <select id="f-sdg"></select></label>
      <label>Keyword in text <input type="text" id="f-kw" placeholder="e.g. torture"></label>
      <button id="f-reset" class="ghost" type="button">Reset</button>
    </div>
  </section>
  <div class="status">
    <span class="count" id="countline"></span>
    <span class="desc" id="descline"></span>
  </div>
  <section class="card" id="chartcard">
    <div class="chartbox" id="chartbox"><canvas id="chart"></canvas></div>
    <p class="note" id="chartnote"></p>
  </section>
  <section class="card">
    <table id="tbl">
      <thead><tr><th>Date</th><th>Body</th><th>Symbol</th><th>Text (first line)</th></tr></thead>
      <tbody id="tbody"></tbody>
    </table>
    <div id="empty" class="nomatch" hidden>No records match these filters</div>
    <button id="more" class="more ghost" type="button" hidden>Show more</button>
  </section>
</div>
<script>
...
</script>
</body>
</html>
```

JS:

```js
const D = window.WORKSHOP_DATA.uhri;
const country = D.country || 'the country';
const all = Array.isArray(D.records) ? D.records : [];
const base = all.filter(r => /recommendation|concern/i.test(String(r.type||'')));
const work = base.length ? base : all;
const years = all.map(r=>r.year).filter(y=>typeof y==='number');
const minY = years.length? Math.min(...years): '';
const maxY = years.length? Math.max(...years): '';
const sdgNames = D.sdg_names || {};
```

Wait — header total: "total number of records" read from file — use D.count if present else all.length. Year range from all records.

Populate selects:

```js
function fill(select, values, allLabel){
  select.innerHTML='';
  const o=document.createElement('option'); o.value=''; o.textContent=allLabel; select.appendChild(o);
  values.forEach(v=>{const op=document.createElement('option'); op.value=v; op.textContent=v; select.appendChild(op);});
}
const mechs=[...new Set(work.map(r=>r.mechanism).filter(Boolean))].sort();
const bodies=[...new Set(work.map(r=>r.body).filter(Boolean))].sort();
const sdgSet=new Set(); work.forEach(r=>(r.sdgs||[]).forEach(s=>sdgSet.add(s)));
const sdgs=[...sdgSet].sort((a,b)=>a-b);
```

SDG select options: value=String(n), label `SDG ${n}${sdgNames[String(n)]?': '+sdgNames[String(n)]:''}`.

Year inputs: set min/max attributes and values.

State: read from controls each render.

```js
function activeFilters(){
  const mech=fMech.value, body=fBody.value, y1=+fY1.value, y2=+fY2.value, sdg=fSdg.value, kw=fKw.value.trim();
  return {mech, body, y1, y2, sdg, kw};
}
function matches(r,f){
  if(f.mech && r.mechanism!==f.mech) return false;
  if(f.body && r.body!==f.body) return false;
  if(typeof r.year==='number' && (r.year<f.y1 || r.year>f.y2)) return false;
  if(f.sdg!=='' && !(r.sdgs||[]).map(String).includes(f.sdg)) return false;
  if(f.kw && !String(r.text||'').toLowerCase().includes(f.kw.toLowerCase())) return false;
  return true;
}
```

Hmm y1/y2: if inputs empty (user clears), +'' = 0 → would filter everything. Guard: if isNaN, use minY/maxY. `const y1 = fY1.value===''? minY : +fY1.value;` etc.

Description:

```js
function describe(f){
  const parts=[];
  if(f.mech) parts.push(f.mech);
  if(f.body) parts.push(f.body);
  const yActive = f.y1!==minY || f.y2!==maxY;
  if(yActive) parts.push(f.y1===f.y2 ? String(f.y1) : f.y1+'–'+f.y2);
  if(f.sdg!=='') parts.push('SDG '+f.sdg+(sdgNames[f.sdg]?': '+sdgNames[f.sdg]:''));
  if(f.kw) parts.push('keyword: '+f.kw);
  return parts.length? parts.join(' · ') : 'no filters — all records';
}
```

Chart:

```js
function themeCounts(list){
  const m=new Map();
  list.forEach(r=>(r.themes||[]).forEach(t=>m.set(t,(m.get(t)||0)+1)));
  return [...m.entries()].sort((a,b)=> b[1]-a[1] || a[0].localeCompare(b[0])).slice(0,10);
}
```

Render chart:

```js
let chart=null;
function renderChart(list){
  const counts=themeCounts(list);
  const box=document.getElementById('chartbox');
  const note=document.getElementById('chartnote');
  if(!list.length){ chart&&chart.destroy(); chart=null; box.style.display='none'; note.textContent=''; return; }
  box.style.display='block';
  if(!counts.length){ chart&&chart.destroy(); chart=null; note.textContent='None of the matching records carry a recorded theme.'; box.style.display='none'; return;}
  const labels=counts.map(c=>c[0]+' ('+c[1]+')').reverse();
  const data=counts.map(c=>c[1]).reverse();
  box.style.height=Math.max(120, counts.length*30+30)+'px';
  if(chart) chart.destroy();
  chart=new Chart(document.getElementById('chart').getContext('2d'),{
    type:'bar',
    data:{labels, datasets:[{data, backgroundColor:'#1f6fb2', borderRadius:3}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:false}, tooltip:{callbacks:{label:c=>c.parsed.x+' record'+(c.parsed.x===1?'':'s')}}},
      scales:{x:{beginAtZero:true, ticks:{precision:0, stepSize:1}, title:{display:true, text:'Number of matching records'}}, y:{ticks:{autoSkip:false}}}}
  });
  note.textContent='How this is computed: each of the '+list.length+' matching record(s) is counted once for every theme it carries; the 10 most frequent themes are shown, longest bar on top, ties broken alphabetically. A record with several themes is counted once for each.';
}
```

Wait — the required note: "A record with several items is counted once for each." Must include that. I'll include both sentences.

Table:

```js
const PAGE=100;
let visible=100;
const expanded=new Set();
function firstLine(t){
  t=String(t||'');
  let cut=t.indexOf('\n');
  if(cut===-1||cut>160) cut=160;
  let s=t.slice(0,cut);
  if(t.length>cut) s+='…';
  return s;
}
function renderTable(list){
  const tb=document.getElementById('tbody');
  tb.innerHTML='';
  const sorted=sortRecs(list);
  const shown=sorted.slice(0,visible);
  shown.forEach(r=>{
    const tr=document.createElement('tr'); tr.className='data'; tr.dataset.id=r.id;
    // date
    const tdD=document.createElement('td'); tdD.textContent=r.date||'date unknown'; tr.appendChild(tdD);
    const tdB=document.createElement('td'); tdB.textContent=r.body||'unknown'; tr.appendChild(tdB);
    const tdS=document.createElement('td');
    if(r.symbol){
      if(r.doc_url){const a=document.createElement('a'); a.className='sym'; a.href=r.doc_url; a.target='_blank'; a.rel='noopener noreferrer'; a.textContent=r.symbol; tdS.appendChild(a);}
      else tdS.textContent=r.symbol;
    } else tdS.textContent='(no symbol)';
    tr.appendChild(tdS);
    const tdT=document.createElement('td'); tdT.textContent=firstLine(r.text); tr.appendChild(tdT);
    tr.addEventListener('click',e=>{ if(e.target.closest('a'))return; toggle(r.id, tr); });
    tb.appendChild(tr);
    if(expanded.has(r.id)) tb.appendChild(detailRow(r));
  });
  // empty / more
  document.getElementById('empty').hidden = list.length>0;
  const moreBtn=document.getElementById('more');
  moreBtn.hidden = sorted.length<=visible;
  moreBtn.textContent = 'Show more ('+(sorted.length-visible)+' remaining)';
}
function detailRow(r){
  const tr=document.createElement('tr'); tr.className='detail';
  const td=document.createElement('td'); td.colSpan=4;
  const meta=document.createElement('div'); meta.className='meta';
  meta.textContent = 'Mechanism: '+(r.mechanism||'unknown')+' · Type: '+(r.type||'unknown')+(r.section? ' · Section: '+r.section : '');
  const ft=document.createElement('div'); ft.className='fulltext'; ft.textContent=String(r.text||'');
  const th=document.createElement('div'); th.className='meta';
  const themes=(r.themes&&r.themes.length)? r.themes.join(', ') : 'none recorded';
  th.innerHTML=''; // build safely
  ...
}
```

For themes/SDGs display, build with spans or just textContent: `Themes: X, Y` and `SDGs: SDG 5: Gender equality, ...`. Use textContent to be safe:

```js
const th=document.createElement('div'); th.className='meta';
th.textContent='Themes: '+((r.themes&&r.themes.length)?r.themes.join(', '):'none recorded');
const sg=document.createElement('div'); sg.className='meta';
const sdgList=(r.sdgs||[]).map(n=>'SDG '+n+(sdgNames[String(n)]?' — '+sdgNames[String(n)]:''));
sg.textContent='SDGs: '+(sdgList.length?sdgList.join(', '):'none recorded');
td.append(meta, ft, th, sg);
tr.appendChild(td);
return tr;
```

toggle:

```js
function toggle(id, tr){
  if(expanded.has(id)){ expanded.delete(id); const next=tr.nextElementSibling; if(next&&next.classList.contains('detail')) next.remove(); }
  else { expanded.add(id); tr.after(detailRow(byId[id])); }
}
```

Need byId map: `const byId={}; work.forEach(r=>byId[r.id]=r);` — but filtered list records are same objects; use the record from the row. Better: store record on tr via dataset index? Simpler: keep a map id→record from work.

Actually simpler: re-render approach — toggle just updates expanded set and re-renders table. But re-render loses scroll? It's fine, small. But re-render on each toggle re-creates 100 rows — fine performance-wise. However "Show more" state persists via `visible`. Re-render is simplest and consistent. But clicking a row then re-rendering — the row stays in same position, fine. I'll do full re-render on toggle: `expanded.has? delete : add; renderTable(currentList)`. Need currentList stored globally.

Render pipeline:

```js
let current=[];
function render(){
  const f=activeFilters();
  current=work.filter(r=>matches(r,f));
  document.getElementById('countline').textContent='Showing '+current.length+' of '+work.length+' records';
  document.getElementById('descline').textContent='Active filters: '+describe(f);
  renderChart(current);
  visible=Math.min(visible, Math.max(PAGE, current.length)); // hmm
  renderTable(current);
}
```

visible handling: when filters change, reset visible to PAGE? If user had shown 300 then filters change, keep visible? Simpler: reset visible=PAGE on filter change, but not on "show more" or toggle. I'll reset visible=PAGE inside render() only when called from filter events; use a flag. Or: in render(), don't touch visible; in filter change handler set visible=PAGE then render(). Toggle handler: just render() without resetting visible. Good.

Events: selects 'change', inputs 'input', reset click.

Reset:

```js
resetBtn.onclick=()=>{ fMech.value=''; fBody.value=''; fY1.value=minY; fY2.value=maxY; fSdg.value=''; fKw.value=''; visible=PAGE; render(); };
```

More button: `visible+=PAGE; render();`

Header:

```js
document.getElementById('title').textContent='UN human rights recommendations to '+country;
const sub=document.getElementById('subline');
const total = (typeof D.count==='number')? D.count : all.length;
sub.textContent=''; 
sub.append('Source: ');
if(D.source_url){const a=document.createElement('a'); a.href=D.source_url; a.target='_blank'; a.rel='noopener'; a.textContent=D.source||D.source_url; sub.appendChild(a);} else sub.append(String(D.source||'UN human rights mechanisms'));
sub.append(' · '+total+' records · '+(years.length? minY+'–'+maxY : 'years unknown'));
```

Hmm "earliest–latest year" — minY–maxY.

Edge: minY/maxY could be '' if no years; then year inputs empty. Guard in activeFilters: if minY==='' treat y1/y2 as -Infinity/Infinity. I'll compute defaults: `const defY1 = years.length?minY:''; ` and in activeFilters: `const y1 = fY1.value==='' ? (years.length?minY:-Infinity) : +fY1.value;` similarly y2 with +Infinity. And describe compares to defaults. Keep it simple but safe.

Also number input min/max attributes: fY1.min=minY etc. (only if years exist).

SDG select fill:

```js
const sdgSel=document.getElementById('f-sdg');
sdgSel.innerHTML='';
{const o=document.createElement('option'); o.value=''; o.textContent='All SDGs'; sdgSel.appendChild(o);}
sdgs.forEach(n=>{const o=document.createElement('option'); o.value=String(n); o.textContent='SDG '+n+(sdgNames[String(n)]?' — '+sdgNames[String(n)]:''); sdgSel.appendChild(o);});
```

Chart canvas: when box display none then shown again, Chart.js responsive handles resize. Setting box.style.height with maintainAspectRatio:false works.

One concern: Chart.js with hidden canvas (display:none) — we destroy before hiding, fine.

Also when chart re-created each render, destroy old. OK.

Table header: maybe add "Mechanism" column? Spec says table columns: date, body, symbol, first line. Keep those 4. Mechanism shown in expanded meta.

Test 2: choose UPR → no row shows CEDAW/CRC — since body filter... wait, mechanism filter UPR; rows show body which for UPR records is "UPR". Fine.

Test 4: symbol links to doc_url new tab. Done.

Test 5: click row → full paragraph verbatim including paragraph number (text starts with "137.8 ..." etc.). Done via pre-wrap textContent.

Line count: fine.

Also "How this is computed" note near the count line? Spec: "a short 'How this is computed' note near every chart or number." I have chart note; add note near count line: e.g., small note under status: "Counts are computed from the records in the file after applying the filters above; nothing is estimated." I'll add a note element in status card. Let me add `<p class="note" id="countnote">` — "How this is computed: every record in the file of type Recommendations or Concerns/Observations is tested against each active filter; keyword matching is case-insensitive on the full text. Counts are exact, not estimated." Good.

Also chart card should hide entirely when no matches? Spec: "No matches: show 'No records match these filters' instead of an empty chart." I'll hide chart card and show the empty message in table card. Implement: chartcard hidden when current.length===0; empty div shown.

Let me also handle `visible` when current shrinks: renderTable uses slice(0,visible) — fine even if visible>length.

Write final code now. Also ensure no external resources. Use window.Chart guard: `if(window.Chart)` — it's preloaded.

Double-check firstLine: "up to its first line break or 160 characters plus '…'". If text has newline at index 10, firstLine = first 10 chars + "…" (since more text remains). If text is exactly 160 chars no newline, cut=160, t.length>cut false → no ellipsis. Good.

Sorting with date strings: dates like "2025-07-10" compare lexicographically = chronologically. Some dates might be partial? Assume ISO. Also fallback to year.

One more: "Only recommendations and concerns/observations are counted anywhere" — my base filter uses regex on type. If type is exactly "Recommendations" or "Concerns/Observations", matches. Good.

Count line Y: work.length. Header total: D.count. If D.count differs from work.length (e.g., other types), that's per rules.

Now, the pre-code message: at most three short sentences. Then code block. Nothing after.

Let me write it all out carefully.

Also add `lang="en"`, title tag dynamic? Set document.title too.

Potential issue: Chart.js ticks stepSize 1 might crowd if counts large; use precision:0 only. Fine.

Bar thickness: default fine.

Let me finalize the JS with element refs.

Also the "Show more" button styling: class "more ghost".

Edge: expanded set uses r.id; ids exist per spec. If id missing, use index — I'll fallback: `const key = r.id || ('i'+work.indexOf(r))`. Simpler: build byId map with key = r.id || JSON? Just use r.id; spec guarantees id. But defensive: `const keyOf = r => r.id || (r.symbol||'')+ (r.date||'') + (r.text||'').slice(0,40);` I'll use a helper.

Write it.

Full code:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations</title>
<style>...</style>
</head>
<body>
...
<script>
(function(){
"use strict";
var D = window.WORKSHOP_DATA && window.WORKSHOP_DATA.uhri ? window.WORKSHOP_DATA.uhri : {};
var country = D.country || "the country";
var all = Array.isArray(D.records) ? D.records : [];
var base = all.filter(function(r){ return /recommendation|concern/i.test(String(r.type||"")); });
var work = base.length ? base : all;
var sdgNames = D.sdg_names || {};
var years = all.map(function(r){return r.year;}).filter(function(y){return typeof y==="number";});
var minY = years.length ? Math.min.apply(null, years) : null;
var maxY = years.length ? Math.max.apply(null, years) : null;
var PAGE = 100;
var visible = PAGE;
var expanded = {};
var current = [];
var chart = null;
var keyOf = function(r){ return r.id || ((r.symbol||"")+"|"+(r.date||"")+"|"+String(r.text||"").slice(0,50)); };

// header
document.title = "UN human rights recommendations to " + country;
document.getElementById("title").textContent = "UN human rights recommendations to " + country;
var sub = document.getElementById("subline");
var total = (typeof D.count === "number") ? D.count : all.length;
sub.appendChild(document.createTextNode("Source: "));
if (D.source_url) { var a=document.createElement("a"); a.href=D.source_url; a.target="_blank"; a.rel="noopener noreferrer"; a.textContent = D.source || D.source_url; sub.appendChild(a); }
else sub.appendChild(document.createTextNode(String(D.source || "UN human rights mechanisms")));
sub.appendChild(document.createTextNode(" · " + total + " records · " + (minY!==null ? (minY + "–" + maxY) : "years unknown")));
...
```

Controls refs and fills. Then functions. Then events. Then initial render.

For selects fill helper.

activeFilters:

```js
function numVal(el, fallback){ var v = el.value; if (v === "" || isNaN(+v)) return fallback; return +v; }
function activeFilters(){
  return {
    mech: elMech.value,
    body: elBody.value,
    y1: numVal(elY1, minY===null?-Infinity:minY),
    y2: numVal(elY2, maxY===null?Infinity:maxY),
    sdg: elSdg.value,
    kw: elKw.value.trim()
  };
}
```

describe(f): compare y1/y2 to defaults:

```js
var defY1 = minY===null?-Infinity:minY, defY2 = maxY===null?Infinity:maxY;
function describe(f){
  var parts=[];
  if(f.mech) parts.push(f.mech);
  if(f.body) parts.push(f.body);
  if(f.y1!==defY1 || f.y2!==defY2){
    parts.push((f.y1===f.y2)? String(f.y1) : (f.y1+"–"+f.y2));
  }
  if(f.sdg!=="") parts.push("SDG "+f.sdg+(sdgNames[f.sdg]?": "+sdgNames[f.sdg]:""));
  if(f.kw) parts.push("keyword: "+f.kw);
  return parts.length ? parts.join(" · ") : "none — all records shown";
}
```

matches as above.

sortRecs as above.

render():

```js
function render(){
  var f = activeFilters();
  current = work.filter(function(r){ return matches(r,f); });
  elCount.textContent = "Showing " + current.length + " of " + work.length + " records";
  elDesc.textContent = "Active filters: " + describe(f);
  renderChart(current);
  renderTable(current);
}
```

renderChart: as drafted; hide chartcard when empty:

```js
function renderChart(list){
  var card=document.getElementById("chartcard");
  if(!list.length){ if(chart){chart.destroy(); chart=null;} card.style.display="none"; return; }
  card.style.display="block";
  var counts=themeCounts(list);
  var box=document.getElementById("chartbox"), note=document.getElementById("chartnote");
  if(!counts.length){ if(chart){chart.destroy(); chart=null;} box.style.display="none"; note.textContent="None of the "+list.length+" matching records carries a recorded theme, so there is no chart to draw."; return; }
  box.style.display="block";
  var labels=[], data=[];
  for(var i=counts.length-1;i>=0;i--){ labels.push(counts[i][0]+" ("+counts[i][1]+")"); data.push(counts[i][1]); }
  box.style.height = Math.max(140, counts.length*32+36) + "px";
  if(chart) chart.destroy();
  chart = new Chart(document.getElementById("chart").getContext("2d"), {...});
  note.textContent = "How this is computed: each of the "+list.length+" matching records is counted once for every theme it carries; the 10 most frequent themes are shown with the longest bar on top (ties broken alphabetically). A record with several themes is counted once for each.";
}
```

renderTable:

```js
function renderTable(list){
  var tb=document.getElementById("tbody");
  tb.innerHTML="";
  var sorted=sortRecs(list);
  var shown=sorted.slice(0,visible);
  shown.forEach(function(r){
    var tr=document.createElement("tr"); tr.className="data";
    var tdD=document.createElement("td"); tdD.textContent=r.date||"date unknown"; tr.appendChild(tdD);
    var tdB=document.createElement("td"); tdB.textContent=r.body||"unknown"; tr.appendChild(tdB);
    var tdS=document.createElement("td");
    if(r.symbol){
      if(r.doc_url){ var a=document.createElement("a"); a.className="sym"; a.href=r.doc_url; a.target="_blank"; a.rel="noopener noreferrer"; a.textContent=r.symbol; tdS.appendChild(a); }
      else tdS.textContent=r.symbol;
    } else tdS.textContent="(no symbol)";
    tr.appendChild(tdS);
    var tdT=document.createElement("td"); tdT.textContent=firstLine(r.text); tr.appendChild(tdT);
    tr.addEventListener("click", function(e){ if(e.target.closest("a")) return; var k=keyOf(r); expanded[k]=!expanded[k]; render(); });
    tb.appendChild(tr);
    if(expanded[keyOf(r)]) tb.appendChild(detailRow(r));
  });
  document.getElementById("empty").hidden = list.length>0;
  var more=document.getElementById("more");
  more.hidden = sorted.length<=visible;
  if(sorted.length>visible) more.textContent="Show more ("+(sorted.length-visible)+" more records)";
}
```

Note: re-render on toggle resets scroll? No, page scroll stays. Fine.

detailRow as drafted.

Events:

```js
[elMech,elBody,elSdg].forEach(function(el){ el.addEventListener("change", function(){ visible=PAGE; render(); }); });
[elY1,elY2,elKw].forEach(function(el){ el.addEventListener("input", function(){ visible=PAGE; render(); }); });
document.getElementById("f-reset").addEventListener("click", function(){ elMech.value=""; elBody.value=""; elSdg.value=""; elKw.value=""; elY1.value=minY===null?"":minY; elY2.value=maxY===null?"":maxY; visible=PAGE; render(); });
document.getElementById("more").addEventListener("click", function(){ visible+=PAGE; render(); });
```

Init: fill selects, set year input values/min/max, render().

Also countnote static text in HTML.

Check: "Showing X of Y" — Y=work.length. On load X=Y since no filters. ✓.

Chart labels include counts ✓. Longest on top: labels reversed so largest last → top with indexAxis 'y'. ✓ (Chart.js y-axis for horizontal bar: first category at bottom by default — yes, in Chart.js the category axis for indexAxis:'y' has reverse=false meaning first item at bottom. So reversing puts largest at top.) ✓

Now write final answer: 2-3 sentences before code, then the html block, nothing after.

Let me count lines roughly — should be ~300. Good.

One more detail: the sub line "source, total number of records, earliest–latest year, all read from the file" ✓.

Also ensure `th` for table header includes maybe "Mechanism"? No, keep 4 columns.

Write CSS nicely. Also make sure no horizontal scroll: table with word-break for symbol; text cell wraps. Add `td:nth-child(4){min-width:...}`? Use `table-layout:auto` default; add `word-break:break-word` on td. Symbol link `word-break:break-all`.

Also `.filters label` text small caps. Fine.

Final code below.