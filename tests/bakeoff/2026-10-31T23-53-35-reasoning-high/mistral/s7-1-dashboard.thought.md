Let me plan this dashboard. The user wants:

1. Dashboard of UN human rights recommendations/observations addressed to Kenya (read country from WORKSHOP_DATA.uhri.country).
2. Top: count of records and years covered.
3. Filters: mechanism, treaty body/mandate (body), year range, SDG, keyword search.
4. Bar chart of 10 most frequent themes for current filter (Chart.js).
5. Table of matching records: date, body, symbol (linked to doc_url), first line of text; clicking row expands full text.

Design: clean NGO/UN style, accent #1f6fb2, light background, system fonts, base 16px. No external resources. Chart.js preloaded.

Key details:
- Read data from window.WORKSHOP_DATA.uhri. Handle empty lists, missing values.
- Years: min/max of year field; show range and maybe distinct years count.
- Filters: mechanism (select with distinct values), body (select distinct bodies), year range (two selects or min/max inputs — selects of years present are safer), SDG (select from sdg_names, only SDGs present in data), keyword search (input, matches text/themes/etc., case-insensitive).
- Theme bar chart: count themes across filtered records (a record can have multiple themes; count each theme once per record). Top 10. Horizontal bar chart (indexAxis: 'y') for readability. Show "How this is computed" note.
- Table: date, body, symbol link, first line of text (first sentence or first ~160 chars). Click row toggles full text expansion. Also show mechanism, type maybe. The user asked for date, body, symbol, first line. I can add mechanism/type/year columns lightly but keep to spec mostly — adding mechanism and type is helpful. Keep it clean.
- Every row shows symbol linked to doc_url in new tab.
- Show n of records for current filter, filter description.
- Handle empty results: show message.
- UPR recommending state: could extract but not required. Skip or maybe show in expanded row? Not required; keep simple but could add. The spec says regex on last parentheses for UPR recommendations. Not requested; skip to keep under line limit. Actually could be a nice touch in expanded view, but not needed.

Also "How this is computed" note near chart and numbers.

Sorting table: by date descending default.

Year range filter: two dropdowns "from year" and "to year" populated from distinct years in data. Or a dual range — selects are simpler and robust.

SDG filter: dropdown of SDGs present in the data with names from sdg_names. Value = goal number. Records match if sdgs includes it.

Keyword search: search in text, themes, section, symbol, body. Debounce slightly.

Chart: Chart.js bar, horizontal, top 10 themes. Colors accent. Update on filter change. Destroy/recreate or update data.

Layout: header with title, description line (source, n, years). Filter panel. Stats. Chart section. Table section.

Let me write the code carefully.

Structure:

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
<header>
  <h1>UN human rights recommendations & observations addressed to <span id="country"></span></h1>
  <p class="lede" id="lede"></p>
</header>
<section class="filters"> ... </section>
<section class="stats" id="stats"></section>
<section class="chart-card">
  <h2>Most frequent themes</h2>
  <p class="note">How this is computed...</p>
  <canvas id="themeChart"></canvas>
  <p id="chartEmpty"></p>
</section>
<section class="table-card">
  <h2>Matching records <span id="matchCount"></span></h2>
  <p class="note">...</p>
  <table>...</table>
  <p id="tableEmpty"></p>
</section>
<script>...</script>
</body>
</html>
```

JS:

```js
const D = window.WORKSHOP_DATA || {};
const uhri = D.uhri || {};
const records = Array.isArray(uhri.records) ? uhri.records : [];
const country = uhri.country || "the participant's country";
const sdgNames = uhri.sdg_names || {};
```

Helpers: `val(r, k)` returns r[k] if present else "".

Distinct values: mechanisms, bodies, years sorted, sdgs present (collect from records' sdgs arrays, map to names).

Filters state: mechanism ("all"), body ("all"), yearFrom, yearTo, sdg ("all"), keyword "".

applyFilters(): filter records:
- mechanism: r.mechanism === state.mechanism
- body: r.body === state.body
- year: r.year >= from && <= to (handle missing year: if year missing, exclude when range set? If from/to are "all" include. Default from=min year, to=max year, so missing-year records excluded — hmm. Better: treat missing year as passing only if range is full? Simpler: if r.year is a number, check range; if missing, include only when no range restriction... but range defaults to full min/max. I'll include records with missing year always? That could be confusing. Let me default from/to to "" (all) and populate selects with "All years" plus each year. Then filter: if from set and (typeof year !== number || year < from) exclude... Actually if from is set and year missing, exclude. If from not set, include. That's deterministic and explainable. Default: from="", to="" meaning all. But user asked "year range" filter — selects with all years present, default "all". Good.

Actually nicer: default from = min year, to = max year, and records missing year are included when from==min && to==max? Overcomplicating. Use "All" default.

- sdg: if set, (r.sdgs||[]).map(String).includes(String(sdg))
- keyword: lowercase search across text, themes joined, section, symbol, body, type, sdg_targets joined, affected_persons joined.

Theme counts: Map theme -> count, count each theme once per record. Sort desc, take 10. Chart labels = theme names (maybe truncated? Chart.js handles wrapping). Use horizontal bars.

Chart config:

```js
chart = new Chart(ctx, {
  type: 'bar',
  data: { labels, datasets: [{ label: 'Records', data, backgroundColor: '#1f6fb2' }] },
  options: {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false }, tooltip: {...} },
    scales: { x: { beginAtZero: true, ticks: { precision: 0 }, title: {display:true, text:'Number of records'} }, y: { ticks: { autoSkip: false } } }
  }
});
```

Update: chart.data.labels = ...; chart.data.datasets[0].data = ...; chart.update(). Wrap in try in case Chart missing? It's preloaded; still guard `if (window.Chart)`.

Container height: set canvas wrapper height based on number of bars, e.g., `Math.max(220, bars*34+40)` px, since maintainAspectRatio false.

Table rendering: build rows. Each row: `<tr class="rec">` with cells: date, body, mechanism+type maybe, symbol link, first line. Click toggles a detail row `<tr class="detail"><td colspan=...>` with full text, themes, sdgs, affected persons, section, countries, doc link. Use event delegation.

First line of text: take text, strip leading paragraph number? "first line" — I'll take the first sentence-ish: split at first ". " maybe, or first 200 chars. Simpler: first line = text up to first newline, or if single line, first ~180 chars + "…". Let me do: `const t = (r.text||'').trim(); const nl = t.indexOf('\n'); let first = nl>0 ? t.slice(0,nl) : t; if (first.length > 220) first = first.slice(0,220).trimEnd() + '…';` Also maybe strip leading "71. " number? Keep as is — it's the actual text.

Date display: r.date or year. Show date if present else year.

Symbol link: `<a href="${doc_url}" target="_blank" rel="noopener">${symbol}</a>` — escape HTML. Need escape function for all injected text.

Escape: 

```js
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
```

URL escaping for href: use esc too (quotes escaped). Fine.

Stats at top: total records, years range: `Math.min(...years)` – `Math.max(...)`, number of distinct years, mechanisms count, bodies count. Show: "N records · YYYY–YYYY (K distinct years) · M mechanisms · B treaty bodies/mandates". Source line: uhri.source + title? uhri has `source`, `source_url`, `title`, `built`, `count`. Lede: `${uhri.title || 'UN human rights recommendations'} — source: ${uhri.source}, ${records.length} records, years X–Y. Built ${uhri.built}.` Link source_url if present.

Filter note: "Showing X of N records" plus active filter description.

Also "How this is computed" notes:
- Stats: "Counts are computed in your browser from the N records in the dataset; no estimates."
- Chart: "Each record contributes 1 to each of its themes; top 10 themes among the X records currently matching the filters."
- Table: "Rows show the first line of the paragraph; click a row for the full text. Symbol links open the UN document in a new tab."

Empty states: if records empty entirely, show message. If filtered empty, show "No records match..." and clear chart.

Keyword input: `<input type="search">` with listener 'input'.

Year selects: options "All years" + sorted distinct years. From select and to select. On change, if from > to, swap or clamp — I'll auto-adjust: if from>to set to=from (or swap). Simple: when from changes and from>to, set to=from. When to changes and to<from, set from=to.

SDG select: options from SDGs present in data: value=number, label "SDG 16 — Peace, justice and strong institutions" using sdgNames[String(n)] fallback "SDG n".

Mechanism select: distinct mechanisms sorted. Body select: distinct bodies sorted (could be many; fine).

Also maybe a "Reset filters" button. Nice.

Sorting table: by date desc, fallback year desc, then symbol. Provide maybe a sort control? Not requested; default date desc. Keep simple.

Row count display: "Showing X of N records".

Let me also show in expanded detail: themes chips, SDG targets, affected persons, section, mechanism/type, countries, full text in a readable block, and link "Open UN document".

Line count: aim under 700. Fine.

CSS: 

```css
:root { --accent:#1f6fb2; --ink:#1c2733; --muted:#5b6b7b; --bg:#f5f7fa; --card:#fff; --line:#dfe6ee; }
* { box-sizing: border-box; }
body { margin:0; font-family: system stack; font-size:16px; color:var(--ink); background:var(--bg); line-height:1.5; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 24px 20px 64px; }
header ...
h1 { font-size: 1.6rem; }
.lede { color: var(--muted); }
.card { background: var(--card); border:1px solid var(--line); border-radius:10px; padding:18px 20px; margin-top:18px; }
.filters grid: display:grid; grid-template-columns: repeat(auto-fit, minmax(180px,1fr)); gap:12px;
label { font-size:.85rem; font-weight:600; color:var(--muted); display:block; margin-bottom:4px; }
select, input { width:100%; padding:8px 10px; border:1px solid var(--line); border-radius:6px; font:inherit; background:#fff; }
.stats { display:flex; flex-wrap:wrap; gap: 10px 28px; }
.stat b { font-size:1.4rem; color:var(--accent); }
.note { font-size:.85rem; color:var(--muted); }
table { width:100%; border-collapse:collapse; }
th { text-align:left; font-size:.8rem; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); border-bottom:2px solid var(--line); padding:8px 10px; }
td { border-bottom:1px solid var(--line); padding:10px; vertical-align:top; }
tr.rec { cursor:pointer; } tr.rec:hover { background:#eef4fb; }
tr.rec.open { background:#e8f1fa; }
.detail td { background:#f8fafd; }
.fulltext { white-space:pre-wrap; background:#fff; border:1px solid var(--line); border-radius:8px; padding:12px 14px; }
a { color: var(--accent); }
.chip { display:inline-block; background:#e8f1fa; color:#17517f; border-radius:999px; padding:2px 10px; font-size:.8rem; margin:2px 4px 2px 0; }
.chart-box { position:relative; }
button.reset { ... }
```

Chart canvas: wrap in div with id chartWrap, set style.height.

Now write JS fully.

```js
(function(){
  'use strict';
  const DATA = window.WORKSHOP_DATA || {};
  const U = DATA.uhri || {};
  const records = Array.isArray(U.records) ? U.records : [];
  const sdgNames = U.sdg_names || {};
  const country = U.country || 'the reviewed country';

  const $ = id => document.getElementById(id);
  const esc = s => String(s==null?'':s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const asArray = v => Array.isArray(v) ? v : (v==null||v==='' ? [] : [v]);

  // distinct helpers
  function distinct(key){ const s=new Set(); records.forEach(r=>{ const v=r[key]; if(v!=null && v!=='') s.add(String(v)); }); return [...s].sort(); }
  const mechanisms = distinct('mechanism');
  const bodies = distinct('body');
  const years = records.map(r=>r.year).filter(y=>typeof y==='number').sort((a,b)=>a-b);
  const yearMin = years.length?years[0]:null, yearMax = years.length?years[years.length-1]:null;
  const yearSet = [...new Set(years)].sort((a,b)=>a-b);
  const sdgSet = new Set();
  records.forEach(r=>asArray(r.sdgs).forEach(n=>sdgSet.add(String(n))));
  const sdgList = [...sdgSet].sort((a,b)=> (parseInt(a,10)||0)-(parseInt(b,10)||0));
```

State and elements. Build filter selects via JS to avoid hardcoding.

```js
  const state = { mechanism:'', body:'', from:'', to:'', sdg:'', q:'' };
```

Populate:

```js
  function fillSelect(el, options, allLabel){
    el.innerHTML = '<option value="">'+esc(allLabel)+'</option>' + options.map(o=>'<option value="'+esc(o.value)+'">'+esc(o.label)+'</option>').join('');
  }
  fillSelect($('fMechanism'), mechanisms.map(m=>({value:m,label:m})), 'All mechanisms');
  fillSelect($('fBody'), bodies.map(b=>({value:b,label:b})), 'All bodies / mandates');
  fillSelect($('fFrom'), yearSet.map(y=>({value:String(y),label:String(y)})), 'From (all)');
  fillSelect($('fTo'), yearSet.map(y=>({value:String(y),label:String(y)})), 'To (all)');
  fillSelect($('fSdg'), sdgList.map(n=>({value:n,label:'SDG '+n+(sdgNames[n]?' — '+sdgNames[n]:''})), 'All SDGs');
```

Filtering:

```js
  function matches(r){
    if(state.mechanism && String(r.mechanism||'')!==state.mechanism) return false;
    if(state.body && String(r.body||'')!==state.body) return false;
    const y = r.year;
    if(state.from){ if(typeof y!=='number' || y < +state.from) return false; }
    if(state.to){ if(typeof y!=='number' || y > +state.to) return false; }
    if(state.sdg){ if(!asArray(r.sdgs).map(String).includes(state.sdg)) return false; }
    if(state.q){
      const hay = [r.text, r.symbol, r.body, r.mechanism, r.type, r.section, ...asArray(r.themes), ...asArray(r.sdg_targets), ...asArray(r.affected_persons), ...asArray(r.countries)].join(' ').toLowerCase();
      if(!hay.includes(state.q)) return false;
    }
    return true;
  }
```

Theme counts:

```js
  function themeCounts(list){
    const m = new Map();
    list.forEach(r=>{ const seen=new Set(); asArray(r.themes).forEach(t=>{ const k=String(t); if(!seen.has(k)){ seen.add(k); m.set(k,(m.get(k)||0)+1); } }); });
    return [...m.entries()].sort((a,b)=> b[1]-a[1] || a[0].localeCompare(b[0])).slice(0,10);
  }
```

Render chart:

```js
  let chart = null;
  function renderChart(list){
    const data = themeCounts(list);
    const wrap = $('chartWrap');
    const empty = $('chartEmpty');
    if(!data.length){ if(chart){chart.destroy(); chart=null;} wrap.style.height='0px'; $('themeCanvas').style.display='none'; empty.hidden=false; empty.textContent = list.length? 'None of the matching records carry a theme tag.' : 'No records match the current filters.'; return; }
    empty.hidden = true;
    $('themeCanvas').style.display='block';
    wrap.style.height = Math.max(240, data.length*36 + 60) + 'px';
    const labels = data.map(d=>d[0]);
    const values = data.map(d=>d[1]);
    if(chart){ chart.data.labels=labels; chart.data.datasets[0].data=values; chart.update(); }
    else if(window.Chart){
      chart = new Chart($('themeCanvas').getContext('2d'), { type:'bar', data:{labels, datasets:[{label:'Records', data:values, backgroundColor:'#1f6fb2', borderRadius:4}]}, options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{ legend:{display:false}, tooltip:{ callbacks:{ label: c => ' '+c.parsed.x+' record'+(c.parsed.x===1?'':'s') } } }, scales:{ x:{ beginAtZero:true, ticks:{precision:0}, title:{display:true, text:'Matching records tagged with this theme'}, grid:{color:'#e6ecf2'} }, y:{ grid:{display:false}, ticks:{ autoSkip:false, font:{size:13} } } } } });
    }
  }
```

Table render:

```js
  function firstLine(r){
    const t = String(r.text||'').trim();
    if(!t) return '(no text)';
    const nl = t.search(/\n/);
    let line = nl>=0 ? t.slice(0,nl) : t;
    if(line.length>240) line = line.slice(0,240).replace(/\s+\S*$/,'') + ' …';
    return line;
  }
  function sortRecords(list){
    return [...list].sort((a,b)=>{
      const da = String(a.date||''), db = String(b.date||'');
      if(da!==db) return db.localeCompare(da);
      const ya=(typeof a.year==='number'?a.year:-1), yb=(typeof b.year==='number'?b.year:-1);
      if(ya!==yb) return yb-ya;
      return String(a.symbol||'').localeCompare(String(b.symbol||''));
    });
  }
  function renderTable(list){
    const tbody = $('recBody');
    const empty = $('tableEmpty');
    $('matchCount').textContent = 'Showing '+list.length+' of '+records.length+' records';
    if(!list.length){ tbody.innerHTML=''; empty.hidden=false; return; }
    empty.hidden=true;
    tbody.innerHTML = list.map((r,i)=>{
      const url = r.doc_url || '#';
      const sym = r.symbol || '(no symbol)';
      const date = r.date || (typeof r.year==='number'? String(r.year):'—');
      const meta = [r.mechanism, r.type].filter(Boolean).join(' · ');
      const detailId = 'd'+i;
      const themes = asArray(r.themes).map(t=>'<span class="chip">'+esc(t)+'</span>').join('');
      const sdgs = asArray(r.sdgs).map(n=>{ const nm = sdgNames[String(n)]; return '<span class="chip">SDG '+esc(n)+(nm?' — '+esc(nm):'')+'</span>'; }).join('');
      const persons = asArray(r.affected_persons).map(p=>'<span class="chip">'+esc(p)+'</span>').join('');
      const targets = asArray(r.sdg_targets).map(t=>'<li>'+esc(t)+'</li>').join('');
      return '<tr class="rec" data-i="'+i+'" aria-expanded="false">'+
        '<td class="cdate">'+esc(date)+'</td>'+
        '<td class="cbody">'+esc(r.body||'—')+'<div class="sub">'+esc(meta)+'</div></td>'+
        '<td class="csym"><a href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">'+esc(sym)+'</a></td>'+
        '<td class="ctext">'+esc(firstLine(r))+'</td>'+
      '</tr>'+
      '<tr class="detail" id="'+detailId+'" hidden><td colspan="4">'+
        (r.section?'<p class="dsec"><strong>Section:</strong> '+esc(r.section)+'</p>':'')+
        '<div class="fulltext">'+esc(r.text||'(no text)')+'</div>'+
        (themes?'<p class="dline"><strong>Themes:</strong> '+themes+'</p>':'')+
        (sdgs?'<p class="dline"><strong>SDGs:</strong> '+sdgs+'</p>':'')+
        (targets?'<p class="dline"><strong>SDG targets:</strong></p><ul class="dlist">'+targets+'</ul>':'')+
        (persons?'<p class="dline"><strong>Affected persons:</strong> '+persons+'</p>':'')+
        (asArray(r.countries).length?'<p class="dline"><strong>Countries:</strong> '+esc(asArray(r.countries).join(', '))+'</p>':'')+
        '<p class="dline"><a href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">Open the UN document ('+esc(sym)+') ↗</a></p>'+
      '</tr>';
    }).join('');
    // store current list for click handler
    currentList = list;
  }
```

Wait — data-i indexes into currentList; but I sorted a copy. Let me keep `currentList = sortRecords(filtered)` and render from that, so data-i maps correctly.

Click delegation:

```js
  let currentList = [];
  $('recBody').addEventListener('click', e=>{
    const tr = e.target.closest('tr.rec');
    if(!tr) return;
    // don't toggle when clicking the link
    if(e.target.closest('a')) return;
    const i = +tr.dataset.i;
    const det = document.getElementById('d'+i);
    const open = !det.hidden;
    det.hidden = open;
    tr.classList.toggle('open', !open);
    tr.setAttribute('aria-expanded', String(!open));
  });
```

Hmm, but if user re-renders, detail rows reset — fine.

Also clicking link inside row: e.target.closest('a') check prevents toggle. Good.

Update function:

```js
  function update(){
    const filtered = records.filter(matches);
    currentList = sortRecords(filtered);
    renderChart(filtered);
    renderTable(currentList);
    // active filter description
    const parts=[];
    if(state.mechanism) parts.push('mechanism: '+state.mechanism);
    if(state.body) parts.push('body/mandate: '+state.body);
    if(state.from||state.to) parts.push('years: '+(state.from||yearMin||'…')+'–'+(state.to||yearMax||'…'));
    if(state.sdg) parts.push('SDG '+state.sdg);
    if(state.q) parts.push('keyword “'+state.q+'”');
    $('filterDesc').textContent = parts.length ? 'Filters: '+parts.join('; ') : 'No filters applied — all records shown.';
  }
```

Header stats:

```js
  $('country').textContent = country;
  document.title = 'UN human rights recommendations — '+country;
  const srcBits = [];
  if(U.source) srcBits.push('Source: '+(U.source_url? '<a href="'+esc(U.source_url)+'" target="_blank" rel="noopener noreferrer">'+esc(U.source)+'</a>' : esc(U.source)));
  ...
```

Lede: `${U.title||'UN human rights recommendations and observations'} · ${records.length} records · years ${yearMin}–${yearMax} (${yearSet.length} distinct years) · ${mechanisms.length} mechanisms · ${bodies.length} bodies/mandates` plus source and built date. Use innerHTML for the link.

Stats cards: Total records (records.length), Years (min–max), Mechanisms (mechanisms.length), Bodies/mandates (bodies.length). Note: "Counted in your browser from the loaded dataset (n = X records); nothing is estimated."

Events:

```js
  $('fMechanism').addEventListener('change', e=>{ state.mechanism=e.target.value; update(); });
  ... body, sdg, q input ...
  $('fFrom').addEventListener('change', e=>{ state.from=e.target.value; if(state.from && state.to && +state.from > +state.to){ state.to = state.from; $('fTo').value = state.to; } update(); });
  $('fTo') similar.
  $('fQ').addEventListener('input', e=>{ state.q = e.target.value.trim().toLowerCase(); update(); });
  $('reset').addEventListener('click', ()=>{ state.mechanism=state.body=state.from=state.to=state.sdg=state.q=''; set select values ''; $('fQ').value=''; update(); });
```

Empty dataset handling: if records.length===0 show a notice in lede and stats zeros, chart/table empty messages. The code mostly handles it; guard yearMin null in lede.

Also handle U.count vs records.length: show records.length (actual). Maybe mention uhri.count if differs? The lede can say "n = records.length records loaded". Fine.

Chart note text: "How this is computed: each matching record adds 1 to every theme it carries (a record with 3 themes counts once in each); the 10 highest counts are shown. Counts are exact, computed in your browser from the filtered records."

Table note: "How this is computed: rows are the records that pass all filters above, sorted by date (newest first). The last column shows the first line of the paragraph; click any row to read the full text. The symbol links to the UN document (opens in a new tab)."

Now HTML skeleton with ids: country, lede, statsRow, fMechanism, fBody, fFrom, fTo, fSdg, fQ, reset, filterDesc, matchCount, chartWrap, themeCanvas, chartEmpty, recBody (tbody), tableEmpty.

Table head: Date | Body / mandate | Symbol | Text (first line). Add a small "▸" hint column? Could add a chevron cell. Keep 4 columns; add CSS `tr.rec td:first-child::before`? Simpler: add a narrow first column with "＋"? Let me add a 5th narrow column at end? Actually put chevron in the text cell? I'll add a small span in date cell? Keep simple: add `<td class="chev">▸</td>` as first column, rotate when open via CSS `tr.rec.open .chev{transform:rotate(90deg)}`. That requires colspan=5 in detail. Fine.

Let me now also double check: "Every row that shows a document has its symbol, linked to doc_url in a new tab." Done.

"the app itself must explain what it shows" — notes included.

Base font 16px, projector readable: h1 1.5rem+, table font 0.95rem ok.

Write final HTML. Keep under 700 lines — easily.

One more: mechanism values include "Universal Periodic Review" etc. Body select label "Treaty body / mandate". For UPR, body might be "OHCHR" or something — whatever data says.

Keyword search placeholder: "Search text, themes, symbols…".

Also add `aria` bits lightly.

Edge: `esc(url)` for href — if doc_url empty, use '#'. If url is '#', link still fine.

Chart.js tooltip callback: `label: ctx => ' ' + ctx.parsed.x + ' record(s)'`.

Also add datalabels? No plugin available; skip.

Let me write the whole file now.

Also the "How this is computed" near the top numbers: add note under stats.

Let me count columns: chev, date, body, symbol, text → 5. Detail colspan=5.

Write it.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations — Kenya</title>
<style>
:root{
  --accent:#1f6fb2; --accent-dark:#17517f; --ink:#1d2733; --muted:#5c6b7a;
  --bg:#f4f6f9; --card:#ffffff; --line:#dde4ec; --soft:#e8f1fa;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  font-size:16px; line-height:1.55; color:var(--ink); background:var(--bg);
}
.wrap{max-width:1100px;margin:0 auto;padding:28px 20px 72px}
header.top{padding:6px 2px 0}
h1{font-size:1.55rem;line-height:1.25;margin:0 0 6px;color:var(--ink)}
h1 .cc{color:var(--accent)}
.lede{margin:0 0 4px;color:var(--muted);font-size:.95rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-top:18px}
.card h2{font-size:1.12rem;margin:0 0 4px}
.note{font-size:.85rem;color:var(--muted);margin:4px 0 12px}
.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px 14px;align-items:end}
.field label{display:block;font-size:.8rem;font-weight:600;color:var(--muted);margin-bottom:4px;letter-spacing:.02em}
.field select,.field input{width:100%;padding:8px 10px;font:inherit;font-size:.92rem;border:1px solid var(--line);border-radius:7px;background:#fff;color:var(--ink)}
.field select:focus,.field input:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.btnrow{display:flex;align-items:flex-end}
button.reset{padding:8px 14px;font:inherit;font-size:.9rem;border:1px solid var(--line);background:#fff;color:var(--accent-dark);border-radius:7px;cursor:pointer}
button.reset:hover{background:var(--soft)}
#filterDesc{font-size:.88rem;color:var(--accent-dark);margin:12px 0 0;font-weight:600}
.stats{display:flex;flex-wrap:wrap;gap:14px 36px;margin-top:2px}
.stat .num{font-size:1.5rem;font-weight:700;color:var(--accent);line-height:1.1}
.stat .lbl{font-size:.82rem;color:var(--muted)}
.chart-box{position:relative;width:100%}
table{width:100%;border-collapse:collapse;margin-top:6px}
th{font-size:.76rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);text-align:left;padding:8px 10px;border-bottom:2px solid var(--line)}
td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top;font-size:.93rem}
tr.rec{cursor:pointer}
tr.rec:hover{background:#f0f6fc}
tr.rec.open{background:var(--soft)}
tr.detail td{background:#f8fafd}
.chev{width:22px;color:var(--accent);transition:none}
tr.rec.open .chev{font-weight:700}
.cdate{white-space:nowrap;font-variant-numeric:tabular-nums}
.cbody{white-space:nowrap}
.cbody .sub{font-size:.78rem;color:var(--muted);white-space:normal}
.csym a{color:var(--accent);text-decoration:none;font-weight:600}
.csym a:hover{text-decoration:underline}
.ctext{color:#33404d}
.fulltext{white-space:pre-wrap;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 14px;font-size:.92rem;margin:6px 0 10px}
.dline{margin:6px 0;font-size:.88rem}
.dsec{margin:2px 0 6px;font-size:.88rem;color:var(--muted)}
.dlist{margin:4px 0 8px;padding-left:20px;font-size:.86rem;color:#33404d}
.chip{display:inline-block;background:var(--soft);color:var(--accent-dark);border-radius:999px;padding:1px 10px;font-size:.78rem;margin:2px 4px 2px 0}
.empty{padding:18px;border:1px dashed var(--line);border-radius:8px;color:var(--muted);background:#fbfcfe;text-align:center}
a{color:var(--accent)}
footer{margin-top:26px;font-size:.82rem;color:var(--muted)}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <h1>UN human rights recommendations &amp; observations addressed to <span class="cc" id="country"></span></h1>
    <p class="lede" id="lede"></p>
  </header>

  <section class="card" aria-label="Filters">
    <h2>Filters</h2>
    <p class="note">Every chart and number below updates to the records that pass all filters. Counting and filtering are done exactly, in your browser, on the loaded dataset — nothing is estimated.</p>
    <div class="filters">
      <div class="field"><label for="fMechanism">Mechanism</label><select id="fMechanism"></select></div>
      <div class="field"><label for="fBody">Treaty body / mandate</label><select id="fBody"></select></div>
      <div class="field"><label for="fFrom">Year from</label><select id="fFrom"></select></div>
      <div class="field"><label for="fTo">Year to</label><select id="fTo"></select></div>
      <div class="field"><label for="fSdg">SDG</label><select id="fSdg"></select></div>
      <div class="field"><label for="fQ">Keyword search</label><input id="fQ" type="search" placeholder="text, theme, symbol…"></div>
      <div class="btnrow"><button class="reset" id="reset" type="button">Reset filters</button></div>
    </div>
    <p id="filterDesc"></p>
  </section>

  <section class="card" aria-label="Overview">
    <h2>Overview of the dataset</h2>
    <div class="stats" id="statsRow"></div>
    <p class="note">How this is computed: each figure is a plain count over the <span id="nNote"></span> records loaded in this page (mechanisms, bodies and years are the distinct values found in the data).</p>
  </section>

  <section class="card" aria-label="Themes chart">
    <h2>10 most frequent themes <span id="chartN"></span></h2>
    <p class="note">How this is computed: each matching record adds 1 to every theme it carries (a record with three themes counts once in each of them); the 10 highest counts are charted. Exact counts, no estimates.</p>
    <div class="chart-box" id="chartWrap"><canvas id="themeCanvas"></canvas></div>
    <p class="empty" id="chartEmpty" hidden></p>
  </section>

  <section class="card" aria-label="Records table">
    <h2>Matching records — <span id="matchCount"></span></h2>
    <p class="note">How this is computed: the rows below are exactly the records that pass the filters above, sorted by date (newest first). The last column shows the first line of the paragraph — click a row to read the full text. The symbol links to the UN document and opens in a new tab.</p>
    <table>
      <thead><tr><th></th><th>Date</th><th>Body / mandate</th><th>Symbol</th><th>Text (first line — click for full text)</th></tr></thead>
      <tbody id="recBody"></tbody>
    </table>
    <p class="empty" id="tableEmpty" hidden>No records match the current filters. Loosen a filter or reset them to see the full list.</p>
  </section>

  <footer id="foot"></footer>
</div>
<script>
...
</script>
</body>
</html>
```

JS final. Also footer: source info: `U.title`, source link, built date, and note "Data loaded locally in this page; no network requests."

Lede content: `${esc(U.title || 'UN human rights recommendations and observations')} · n = ${records.length} records · years ${yearMin}–${yearMax} · source: ...`. Build with innerHTML carefully.

Stats row: four stats: Records (records.length), Year span (yearMin–yearMax), Distinct years (yearSet.length), Mechanisms (mechanisms.length), Bodies/mandates (bodies.length). Maybe 5 stats fine.

Handle records.length===0: lede says "No records were loaded." stats show 0 / —. Guard yearMin null → '—'.

Now the script:

```js
(function(){
'use strict';
var DATA = window.WORKSHOP_DATA || {};
var U = DATA.uhri || {};
var records = Array.isArray(U.records) ? U.records : [];
var sdgNames = U.sdg_names || {};
var country = U.country || 'the reviewed country';

function $(id){ return document.getElementById(id); }
function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
function arr(v){ return Array.isArray(v)?v:(v==null||v===''?[]:[v]); }
function distinct(key){ var s={},out=[]; records.forEach(function(r){ var v=r[key]; if(v!=null&&v!==''){ v=String(v); if(!s[v]){s[v]=1;out.push(v);} } }); return out.sort(); }

var mechanisms = distinct('mechanism');
var bodies = distinct('body');
var yearSet = []; var seenY={};
records.forEach(function(r){ if(typeof r.year==='number' && !seenY[r.year]){ seenY[r.year]=1; yearSet.push(r.year); } });
yearSet.sort(function(a,b){return a-b;});
var yearMin = yearSet.length?yearSet[0]:null;
var yearMax = yearSet.length?yearSet[yearSet.length-1]:null;
var sdgSet={}; var sdgList=[];
records.forEach(function(r){ arr(r.sdgs).forEach(function(n){ var k=String(n); if(!sdgSet[k]){ sdgSet[k]=1; sdgList.push(k); } }); });
sdgList.sort(function(a,b){ return (parseInt(a,10)||0)-(parseInt(b,10)||0); });

var state = { mechanism:'', body:'', from:'', to:'', sdg:'', q:'' };
var currentList = [];
var chart = null;

function fillSelect(el, opts, allLabel){
  el.innerHTML = '<option value="">'+esc(allLabel)+'</option>'+opts.map(function(o){ return '<option value="'+esc(o.v)+'">'+esc(o.l)+'</option>'; }).join('');
}
fillSelect($('fMechanism'), mechanisms.map(function(m){return {v:m,l:m};}), 'All mechanisms');
fillSelect($('fBody'), bodies.map(function(b){return {v:b,l:b};}), 'All bodies / mandates');
fillSelect($('fFrom'), yearSet.map(function(y){return {v:String(y),l:String(y)};}), 'From (any)');
fillSelect($('fTo'), yearSet.map(function(y){return {v:String(y),l:String(y)};}), 'To (any)');
fillSelect($('fSdg'), sdgList.map(function(n){ return {v:n, l:'SDG '+n+(sdgNames[n]?' — '+sdgNames[n]:'')}; }), 'All SDGs');
```

Header:

```js
$('country').textContent = country;
document.title = 'UN human rights recommendations — '+country;
var lede = esc(U.title || 'UN human rights recommendations and observations addressed to '+country)
  + ' · n = ' + records.length + ' records'
  + (yearMin!=null ? ' · years ' + yearMin + '–' + yearMax + ' (' + yearSet.length + ' distinct years)' : ' · no year information');
if(U.source){ lede += ' · source: ' + (U.source_url ? '<a href="'+esc(U.source_url)+'" target="_blank" rel="noopener noreferrer">'+esc(U.source)+'</a>' : esc(U.source)); }
if(U.built){ lede += ' · dataset built ' + esc(U.built); }
$('lede').innerHTML = lede;
```

Stats:

```js
function stat(num, lbl){ return '<div class="stat"><div class="num">'+esc(num)+'</div><div class="lbl">'+esc(lbl)+'</div></div>'; }
$('statsRow').innerHTML =
  stat(records.length, 'records loaded') +
  stat(yearMin!=null ? yearMin+'–'+yearMax : '—', 'year range') +
  stat(yearSet.length, 'distinct years') +
  stat(mechanisms.length, 'mechanisms') +
  stat(bodies.length, 'bodies / mandates');
$('nNote').textContent = records.length;
$('foot').innerHTML = 'Data: ' + esc(U.title||'UHRI extract') + (U.source? ' ('+esc(U.source)+')':'') + '. All data was loaded into this page before it opened; the page makes no network requests. Symbols link to the UN documents (docs.un.org / undocs.org) and open in a new tab.';
```

Filtering + render as planned. matches():

```js
function matches(r){
  if(state.mechanism && String(r.mechanism==null?'':r.mechanism)!==state.mechanism) return false;
  if(state.body && String(r.body==null?'':r.body)!==state.body) return false;
  var y = r.year;
  if(state.from){ if(typeof y!=='number' || y < parseInt(state.from,10)) return false; }
  if(state.to){ if(typeof y!=='number' || y > parseInt(state.to,10)) return false; }
  if(state.sdg){ var ok=false; arr(r.sdgs).forEach(function(n){ if(String(n)===state.sdg) ok=true; }); if(!ok) return false; }
  if(state.q){
    var hay = [r.text,r.symbol,r.body,r.mechanism,r.type,r.section,r.doc_url].concat(arr(r.themes),arr(r.sdg_targets),arr(r.affected_persons),arr(r.countries)).join(' ').toLowerCase();
    if(hay.indexOf(state.q)===-1) return false;
  }
  return true;
}
```

themeCounts, renderChart, firstLine, sortRecords, renderTable, update as planned.

renderTable uses currentList indices; set currentList before renderTable.

```js
function update(){
  var filtered = records.filter(matches);
  currentList = sortRecords(filtered);
  renderChart(filtered);
  renderTable(currentList);
  var parts=[];
  if(state.mechanism) parts.push('mechanism = '+state.mechanism);
  if(state.body) parts.push('body/mandate = '+state.body);
  if(state.from||state.to) parts.push('years '+(state.from||(yearMin!=null?yearMin:'…'))+'–'+(state.to||(yearMax!=null?yearMax:'…')));
  if(state.sdg) parts.push('SDG '+state.sdg+(sdgNames[state.sdg]?' ('+sdgNames[state.sdg]+')':''));
  if(state.q) parts.push('keyword “'+state.q+'”');
  $('filterDesc').textContent = parts.length ? 'Active filters — '+parts.join('; ') : 'No filters applied: all '+records.length+' records are shown.';
  $('chartN').textContent = '· '+filtered.length+' matching record'+(filtered.length===1?'':'s');
}
```

Events wiring and initial update().

renderChart with chartN etc. Also when Chart missing, show fallback list? Guard: if no window.Chart, render theme list as HTML text. Add fallback: if(!window.Chart){ wrap.innerHTML = '<ol>...' } — but canvas inside wrap; simpler: if no Chart, set chartEmpty text listing themes. I'll add small fallback: build a simple HTML bar list. Keep it minimal: if no Chart, replace canvas with a `<div>` of rows with inline-block widths. Let me implement fallback quickly:

```js
if(!window.Chart){
  var max = data[0][1];
  $('chartWrap').innerHTML = data.map(function(d){ return '<div style="margin:4px 0"><div style="font-size:.85rem">'+esc(d[0])+'</div><div style="background:#e8f1fa;border-radius:4px;padding:2px 8px;width:'+Math.max(6, Math.round(d[1]/max*100))+'%;color:#17517f;font-size:.8rem">'+d[1]+'</div></div>'; }).join('');
  return;
}
```

But then re-render needs to restore canvas... Chart is preloaded per instructions, so fallback rarely triggers; but if it does and re-render happens, chartWrap innerHTML wiped canvas. To be safe, only fallback once and guard: if(!window.Chart){ ...; return; } and in update, if no Chart, always rebuild fallback. Since canvas would be gone, renderChart should check `if(!window.Chart){ fallback }` before touching canvas. And when Chart exists, ensure canvas visible: set display. OK — in fallback branch, don't destroy chart. Fine.

Actually simpler: keep canvas in DOM always; fallback writes into a separate div `#chartFallback` next to canvas, hiding canvas. Let me add `<div id="chartFallback"></div>` after canvas. In renderChart: if(!window.Chart){ canvas.style.display='none'; fallback.innerHTML=...; fallback.hidden=false; return; } else { fallback.hidden=true; canvas.style.display='block'; ... }.

Detail row colspan: 5 columns (chev, date, body, symbol, text).

Chevron cell: `<td class="chev">▸</td>`.

Also add `title` attr on rec row "Click to expand full text".

Escape in attributes: data-i numeric fine.

One more consideration: performance — records could be a few thousand; rendering all rows at once could be heavy but acceptable. Maybe cap? The spec says table of matching records; render all. If huge (e.g., 5000), innerHTML big but okay. Could add "show first 200 with a note"? That would violate "table of the matching records" completeness... I'll render all; datasets likely ≤ ~2000. Fine.

Also add per-row year in date cell if date missing.

Write final answer: 2-3 short sentences before code block, then the html block, nothing after.

Let me assemble the complete file carefully, ensuring all ids referenced exist.

Also `sortRecords` uses date string compare — ISO dates compare fine.

firstLine: handle text with leading number "71. The Committee..." — keep.

Detail row: include date/year/body/mechanism/type line at top? The row already shows those. Include section, full text, chips, links. Good.

Check the click handler: rows re-rendered each update, delegation on tbody persists. Good.

Reset button: set all selects to '' and input value ''.

Year from/to interplay: on from change, if to set and from>to → set to=from. On to change, if from set and to<from → from=to.

Write it all out now. Also ensure `hidden` attribute works with our CSS (default). `.empty[hidden]{display:none}` — hidden attribute default display:none unless overridden by display rule; `.empty` has no display property set (it's a p, block default) — hidden works since we don't set display on .empty. Good. For chartEmpty same.

Canvas display none initially? It'll be set by renderChart on load. Fine.

Line count ~ 380. Good.

Double-check esc used in option values — values are plain strings, fine.

One subtlety: `fillSelect` for fFrom/fTo allLabel 'From (any)' value '' meaning no lower bound. Good.

In filterDesc years display uses yearMin/yearMax fallback.

Now produce final output.