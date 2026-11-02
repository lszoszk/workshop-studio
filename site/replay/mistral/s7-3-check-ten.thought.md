The user wants to add a "Check 10 at random" feature to the existing dashboard. Requirements:

1. Button "Check 10 at random" — draws 10 random records from the current filter (currentList).
2. Shows for each: full text and the SDGs the UN index assigned (sdgs + sdg_targets, with names from sdg_names).
3. User marks each record's SDGs as right / wrong / arguable (per record — one mark per record, or per SDG? "For each record I mark the SDGs as right, wrong or arguable" — ambiguous. Could be per-record mark of the SDG assignment overall, or per-SDG. Simpler and defensible: mark per record (the SDG assignment as a whole). But "the SDGs" plural... Hmm. Let me think: "shows, for each, the full text and the SDGs the UN index assigned to it. For each record I mark the SDGs as right, wrong or arguable." I think marking per record is the natural reading — each record gets one of three marks. But could also be per SDG chip. To be safe and useful, I could allow marking per SDG chip? That complicates the agreement rate. The agreement rate = share marked "right". If per-record, agreement = right/10. I'll go per-record: each record has three buttons (Right / Wrong / Arguable). Actually, maybe per-SDG would be more granular... but "When all 10 are marked, show the agreement rate" — agreement rate over 10 records. Per-record marking is cleaner and matches "all 10 are marked". I'll do per-record marking with three buttons. Hmm, but "I mark the SDGs" — the SDGs of the record. Per-record mark of the SDG set. I'll note in the UI: "Mark the SDG assignment for this record". That's honest.

Actually, let me reconsider: allowing per-SDG marks would let agreement rate be computed per SDG tag. But "all 10 are marked" strongly implies 10 items = 10 records. Per-record it is.

4. When all 10 marked: show agreement rate (right count / 10, as %), plus lists of wrong and arguable examples (symbol + link + text snippet + assigned SDGs + mark).
5. Download CSV of the 10 records with marks. CSV columns: id, symbol, doc_url, date, year, body, mechanism, type, section, text, themes, sdgs, sdg_targets, affected_persons, countries, mark. Need proper CSV escaping (quotes, commas, newlines). Download via Blob + URL.createObjectURL + a.click(). That's offline-safe (no network).
6. "Draw again" button — redraws 10 random records, resetting marks.

Randomness: use Math.random() — that's fine, it's a draw, not an estimate. Should say "random draw" on screen. If fewer than 10 records in filter, draw all of them (min(10, n)) and say so.

Also handle records with no SDGs — still show them, mark as... they can still be marked right/wrong/arguable (e.g., "no SDG assigned" could be arguable). Show "No SDGs assigned by the index" note.

Where to place: a new card section between chart and table, or after the table? Probably after the chart, before the table — or as its own card after the table. I'll put it after the records table card, as "Spot-check 10 at random" card. Actually flow: filters → overview → chart → table → spot-check. Or spot-check before table? The user said "Add a button" — placement flexible. I'll add a new card after the table.

Design: card with button "Check 10 at random" and "Draw again" (hidden until first draw). Progress "3 of 10 marked". Each drawn record: a panel with symbol link, date, body, full text (in a box), assigned SDGs as chips (SDG n — name) and sdg_targets list, and three mark buttons: Right (green?), Wrong (red?), Arguable (amber?). Keep palette professional — accent #1f6fb2; use muted colors for marks: right = green (#2e7d32), wrong = #c0392b, arguable = #b26a00. That's fine.

When all marked: summary panel with agreement rate (e.g., "7 of 10 marked right — 70% agreement"), and sections listing wrong examples and arguable examples (each with symbol link, first line of text, SDGs). Plus "Download CSV" button.

CSV: build with proper escaping: wrap in quotes, double internal quotes. Include header row. Filename like "sdg-spotcheck-kenya-YYYYMMDD-HHMM.csv" — use country from data, sanitized. Include a column "mark" with values right/wrong/arguable. Also maybe include filter description? Keep it simple but informative: include columns for the filters applied? Could add "filters" column same for all rows. I'll include a "filters_applied" column. Fine.

Random draw: shuffle copy of currentList with Fisher-Yates using Math.random, take first 10. Note on screen: "10 records drawn at random from the N matching the current filters (Math.random; redraw gives a different sample)."

Also must re-draw when filters change? If user changes filters after drawing, the drawn sample is from old filter. I should either clear the spot-check section on filter change or note it. Simplest: when filters change and a draw exists, show a note "filters changed since this draw — draw again" or auto-clear. I'll auto-clear the spot-check panel on any filter change (update() calls resetSpotcheck if drawn). Actually update() is called on every input; clearing on each keystroke could be annoying if they typed keyword then want to draw. But the draw is from current filter at draw time; if they change filters afterwards, the sample no longer matches current filter. I'll clear the drawn sample when filters change, with a small note. Hmm, but update() is called on 'input' for keyword — if they draw, then type more, it clears. That's correct behavior (sample no longer from current filter). I'll clear silently but keep a note in the card: "The sample is drawn from the records matching the current filters; changing a filter clears it." Good.

Edge cases: currentList empty → button disabled or shows message "no records match current filters". If fewer than 10, draw all and say "only N records match — showing all N".

Line count: keep under ~700 lines total. Current file is maybe ~330 lines. Adding ~150-200 lines is fine.

Also the "How this is computed" note for the new section: explain random draw, agreement rate = right/total marked, CSV contents.

Let me now write the additions:

HTML: new card after the records table card:

```html
<section class="card" id="spotCard" aria-label="Random spot-check">
  <h2>Spot-check: 10 records at random</h2>
  <p class="note">How this works: the button draws 10 records at random (Math.random, no seed) from the records matching the current filters above, and shows each one's full text plus the SDGs the UN index assigned to it. Mark each record's SDG assignment as <em>right</em>, <em>wrong</em> or <em>arguable</em>. When all drawn records are marked, the agreement rate (share marked “right”) and the wrong / arguable examples appear, and you can download the records with your marks as CSV. Changing any filter clears the current draw.</p>
  <div class="btnrow" style="gap:10px">
    <button id="drawBtn" class="primary" type="button">Check 10 at random</button>
    <button id="redrawBtn" class="reset" type="button" hidden>Draw again</button>
  </div>
  <p id="spotStatus" class="note" style="margin-top:10px"></p>
  <div id="spotList"></div>
  <div id="spotSummary" hidden>
    <h3 style="...">Result</h3>
    <div id="agreeBox"></div>
    <div id="wrongBox"></div>
    <div id="argBox"></div>
    <button id="csvBtn" class="primary" type="button">Download CSV of the 10 records with my marks</button>
  </div>
</section>
```

Primary button style: accent background white text.

JS:

```js
var spot = { drawn: [], marks: {}, drawnAt: 0 };
function shuffle(a){ for(var i=a.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)); var t=a[i]; a[i]=a[j]; a[j]=t; } return a; }
function drawSpot(){
  var pool = currentList.slice();
  var n = Math.min(10, pool.length);
  shuffle(pool);
  spot.drawn = pool.slice(0, n);
  spot.marks = {};
  renderSpot();
}
```

renderSpot: builds list of panels. Each panel:

```html
<div class="spot-item" data-idx="i">
  <div class="spot-head">
    <span class="chip">#i+1 of n</span> <a symbol> <span date> <span body>
  </div>
  <div class="fulltext">text</div>
  <div class="sdgbox"><strong>SDGs assigned by the UN index:</strong> chips or "none assigned" + targets list</div>
  <div class="markrow">
    <span>Mark the SDG assignment:</span>
    <button data-mark="right">Right</button>
    <button data-mark="wrong">Wrong</button>
    <button data-mark="arguable">Arguable</button>
    <span class="markstate"></span>
  </div>
</div>
```

Mark buttons toggle: clicking sets mark; clicking same mark again could unmark? Keep simple: clicking sets; allow re-marking (change mark) until... allow anytime before all marked? Once all marked, summary shows; allow changing marks and summary updates? Simpler: allow re-marking anytime; summary recomputed on each mark; summary visible once all marked. If user unmarks (click active mark to clear?) — I'll allow clicking the active mark to clear it, hiding summary again. That's nice.

Agreement rate: right / drawn.length, as percentage with one decimal. Show "X of N marked right — Y% agreement". Also counts of wrong/arguable.

Wrong/arguable examples: list each with symbol link, first line, assigned SDG chips.

CSV: 

```js
function csvCell(v){
  var s = String(v==null?'':v);
  return '"' + s.replace(/"/g,'""') + '"';
}
function downloadCSV(){
  var rows = [];
  var header = ['id','symbol','doc_url','date','year','body','mechanism','type','section','text','themes','sdgs','sdg_targets','affected_persons','countries','mark','filters_applied'];
  rows.push(header.map(csvCell).join(','));
  var filtersDesc = $('filterDesc').textContent;
  spot.drawn.forEach(function(r){
    rows.push([
      r.id, r.symbol, r.doc_url, r.date, r.year, r.body, r.mechanism, r.type, r.section,
      r.text, arr(r.themes).join(' | '), arr(r.sdgs).join(' | '), arr(r.sdg_targets).join(' | '),
      arr(r.affected_persons).join(' | '), arr(r.countries).join(' | '),
      spot.marks[r.id] || '', filtersDesc
    ].map(csvCell).join(','));
  });
  var blob = new Blob([rows.join('\r\n')], {type:'text/csv;charset=utf-8'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'sdg-spotcheck-' + country.toLowerCase().replace(/[^a-z0-9]+/g,'-') + '-' + new Date().toISOString().slice(0,10) + '.csv';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
}
```

Note: marks keyed by r.id — ids should be unique; fallback to index if id missing. Use key = r.id || ('idx'+i). I'll use index-based keys to be safe: spot.marks[i]. Actually records have ids per spec, but be safe: key by index in drawn array.

Status text: "Drawn 10 of 47 matching records at random · 3 of 10 marked". If pool < 10: "Only N records match the current filters — showing all N."

Disable draw button when currentList empty: set disabled and status "No records match the current filters — nothing to draw."

On filter change (update()), if spot.drawn.length, clear: spot.drawn=[]; spot.marks={}; render empty state; hide summary. I'll call resetSpot() inside update() only if drawn — but update() runs at load too; guard.

Wait — careful: update() is called on every keystroke in keyword. If user drew and then edits keyword, clearing is intended. OK.

Also "Draw again" button: visible after first draw; calls drawSpot() again (new random sample, marks reset).

Mark buttons styling: .markbtn with data-mark; active state colored. Right: green bg when active; Wrong: red; Arguable: amber.

Summary rendering: function renderSummary() called after each mark; visible when all drawn have marks.

```js
function allMarked(){ return spot.drawn.length>0 && spot.drawn.every(function(_,i){ return !!spot.marks[i]; }); }
function renderSummary(){
  var box = $('spotSummary');
  if(!allMarked()){ box.hidden = true; return; }
  box.hidden = false;
  var n = spot.drawn.length;
  var right = spot.drawn.filter(function(_,i){ return spot.marks[i]==='right'; }).length;
  var wrong = ..., arguable = ...;
  var pct = (right/n*100);
  $('agreeBox').innerHTML = '<div class="agree-num">'+right+' of '+n+' marked right — '+pct.toFixed(1)+'% agreement</div>'
    + '<p class="note">Agreement rate = records you marked “right” ÷ all drawn records ('+n+'). Wrong: '+wrong+' · Arguable: '+arguable+'.</p>';
  $('wrongBox').innerHTML = wrongList('wrong','Wrong examples');
  $('argBox').innerHTML = wrongList('arguable','Arguable examples');
}
```

wrongList builds list of examples: symbol link + date + first line + SDG chips.

Example item HTML:

```html
<div class="ex"><a href=doc target=_blank>symbol</a> <span class="exdate">date</span><div class="extext">first line…</div><div>SDGs: chips</div></div>
```

If none: "None." 

Also note: records with no SDGs — in the SDG box show "No SDGs assigned by the index (empty list in the data)." They can still be marked (e.g., arguable that none were assigned). Fine.

Also show sdg_targets under SDGs.

Now CSS additions:

```css
button.primary{padding:9px 16px;font:inherit;font-size:.92rem;font-weight:600;border:1px solid var(--accent-dark);background:var(--accent);color:#fff;border-radius:7px;cursor:pointer}
button.primary:hover{background:var(--accent-dark)}
button.primary:disabled{background:#9db8cf;border-color:#9db8cf;cursor:not-allowed}
.spot-item{border:1px solid var(--line);border-radius:9px;padding:14px 16px;margin-top:14px;background:#fbfcfe}
.spot-head{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:baseline;font-size:.9rem;margin-bottom:8px}
.spot-head .sym a{font-weight:700}
.markrow{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px;font-size:.88rem;color:var(--muted)}
.markbtn{padding:6px 14px;font:inherit;font-size:.86rem;border:1px solid var(--line);background:#fff;border-radius:999px;cursor:pointer;color:var(--ink)}
.markbtn:hover{border-color:var(--accent)}
.markbtn.active[data-mark="right"]{background:#2e7d32;border-color:#2e7d32;color:#fff}
.markbtn.active[data-mark="wrong"]{background:#c0392b;border-color:#c0392b;color:#fff}
.markbtn.active[data-mark="arguable"]{background:#b26a00;border-color:#b26a00;color:#fff}
.markstate{font-weight:600}
.sdgbox{margin-top:8px;font-size:.9rem}
.agree-num{font-size:1.25rem;font-weight:700;color:var(--accent);margin:6px 0 2px}
.ex{border-left:3px solid var(--line);padding:6px 12px;margin:8px 0;font-size:.9rem}
.ex.wrong{border-color:#c0392b}
.ex.arg{border-color:#b26a00}
.extext{color:#33404d;margin:2px 0}
.exdate{color:var(--muted);font-size:.82rem}
h3.sub{font-size:1rem;margin:16px 0 4px}
```

Also the spot card placement: after the records table card, before footer.

Also need to make sure the draw button reflects current filter count: status text under buttons: "N records currently match the filters." Update in update().

Let me also handle: draw when currentList.length===0 → status message, no draw.

Now integrate into existing script. I need to modify update() to call refreshSpotControls() (status text + disabled state) and clear draw if filters changed. How to detect filter change? In update(), compare a signature of state with last applied signature; if changed and spot.drawn.length, clear. Simple: keep lastSig; in update compute sig = JSON.stringify(state); if sig!==lastSig { lastSig=sig; if(spot.drawn.length) clearSpot(); } then refresh controls.

But careful: update() is also called at initial load; lastSig init null → clears nothing (drawn empty). Fine.

Edge: drawSpot uses currentList which is set in update(). Good.

CSV download — no network, Blob is fine.

Also "let me download the 10 records with my marks as CSV" — only enabled when all marked? The summary (with CSV button) appears when all marked. But maybe allow CSV download anytime after draw (marks may be partial, empty cells). The requirement: "When all 10 are marked, show the agreement rate and the wrong and arguable examples, and let me download the 10 records with my marks as CSV." So CSV button in summary. I'll also allow downloading partial? Keep to spec: CSV button appears in summary when all marked. But maybe put CSV button also available once drawn... Spec says when all marked. I'll show summary block when all marked, containing agreement + examples + CSV button. Additionally, I could show a CSV button right after draw too — but stick to spec to avoid clutter. Actually, allowing download with partial marks is harmless and useful; but spec explicit — keep in summary only. Hmm, I'll put the CSV button in the summary only, per spec.

Let me now also double check "shows, for each, the full text and the SDGs the UN index assigned to it" — full text in .fulltext box (pre-wrap). SDGs: chips with names + targets list. Good.

One more: "For each record I mark the SDGs as right, wrong or arguable." — per record. I'll label the mark row: "Mark this record's SDG assignment:". Good.

Now write the full file. I must return the whole HTML document, not a diff. Keep under ~700 lines. Let me compose carefully.

Also update the intro sentences before code block: max three short sentences.

Let me write the complete file now, merging previous content plus additions.

Structure of script additions:
- after renderTable section, add spot-check code.
- modify update() to include spot control refresh + signature clearing.

Let me write out the code fully.

Also note: `currentList` is sorted list of filtered records. Draw from that.

Potential issue: `arr` helper exists. `esc` exists. `firstLine` exists — reuse for examples.

Write renderSpot():

```js
function sdgChips(r){
  var s = arr(r.sdgs);
  if(!s.length) return '<span class="chip">No SDG assigned</span>';
  return s.map(function(n){
    var nm = sdgNames[String(n)];
    return '<span class="chip">SDG '+esc(n)+(nm?' — '+esc(nm):'')+'</span>';
  }).join('');
}
function renderSpot(){
  var list = $('spotList'), status = $('spotStatus'), redraw = $('redrawBtn'), summary = $('spotSummary');
  if(!spot.drawn.length){
    list.innerHTML=''; summary.hidden=true; redraw.hidden=true;
    return;
  }
  redraw.hidden = false;
  var n = spot.drawn.length;
  var marked = spot.drawn.filter(function(_,i){ return spot.marks[i]; }).length;
  status.textContent = 'Drawn ' + n + ' of ' + currentList.length + ' matching records at random (Math.random — “Draw again” gives a different sample) · ' + marked + ' of ' + n + ' marked.';
  list.innerHTML = spot.drawn.map(function(r,i){
    var url = r.doc_url || '#';
    var sym = r.symbol || '(no symbol)';
    var targets = arr(r.sdg_targets).map(function(t){ return '<li>'+esc(t)+'</li>'; }).join('');
    var m = spot.marks[i];
    return '<div class="spot-item">'
      + '<div class="spot-head"><span class="chip">Record '+(i+1)+' of '+n+'</span>'
      + '<span class="sym"><a href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">'+esc(sym)+'</a></span>'
      + '<span class="exdate">'+esc(r.date || (typeof r.year==='number'?String(r.year):'—'))+' · '+esc(r.body||'—')+(r.mechanism?' · '+esc(r.mechanism):'')+'</span></div>'
      + '<div class="fulltext">'+esc(r.text||'(no text in this record)')+'</div>'
      + '<div class="sdgbox"><strong>SDGs assigned by the UN index:</strong> '+sdgChips(r)
      + (targets ? '<ul class="dlist">'+targets+'</ul>' : '')
      + (arr(r.sdgs).length===0 ? '<p class="note" style="margin:4px 0 0">This record has an empty SDG list in the data — you can still mark the assignment (e.g. “arguable” if you think an SDG should have been assigned).</p>' : '')
      + '</div>'
      + '<div class="markrow"><span>Mark this record’s SDG assignment:</span>'
      + ['right','wrong','arguable'].map(function(mk){
          return '<button type="button" class="markbtn'+(m===mk?' active':'')+'" data-i="'+i+'" data-mark="'+mk+'">'+mk.charAt(0).toUpperCase()+mk.slice(1)+'</button>';
        }).join('')
      + '<span class="markstate">'+(m?'Marked: '+m:'')+'</span></div>'
      + '</div>';
  }).join('');
  renderSummary();
}
```

Event delegation on spotList for mark buttons:

```js
$('spotList').addEventListener('click', function(e){
  var b = e.target.closest('.markbtn');
  if(!b) return;
  var i = parseInt(b.dataset.i,10), mk = b.dataset.mark;
  if(spot.marks[i] === mk){ delete spot.marks[i]; } else { spot.marks[i] = mk; }
  renderSpot();
});
```

renderSummary:

```js
function exampleList(mark, title){
  var items = [];
  spot.drawn.forEach(function(r,i){
    if(spot.marks[i] !== mark) return;
    var url = r.doc_url || '#';
    items.push('<div class="ex '+mark+'"><a href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">'+esc(r.symbol||'(no symbol)')+'</a> '
      + '<span class="exdate">'+esc(r.date||'')+'</span>'
      + '<div class="extext">'+esc(firstLine(r))+'</div>'
      + '<div>'+sdgChips(r)+'</div></div>');
  });
  return '<h3 class="sub">'+esc(title)+' ('+items.length+')</h3>' + (items.length ? items.join('') : '<p class="note">None.</p>');
}
function renderSummary(){
  var box = $('spotSummary');
  if(!spot.drawn.length || !allMarked()){ box.hidden = true; return; }
  box.hidden = false;
  var n = spot.drawn.length;
  var counts = {right:0, wrong:0, arguable:0};
  spot.drawn.forEach(function(_,i){ counts[spot.marks[i]] = (counts[spot.marks[i]]||0)+1; });
  var pct = (counts.right/n*100);
  $('agreeBox').innerHTML = '<div class="agree-num">'+counts.right+' of '+n+' marked “right” — '+pct.toFixed(1)+'% agreement</div>'
    + '<p class="note">Agreement rate = records marked “right” ÷ all '+n+' drawn records. Wrong: '+counts.wrong+' · Arguable: '+counts.arguable+'. Counted exactly from your marks above.</p>';
  $('wrongBox').innerHTML = exampleList('wrong','Wrong examples');
  $('argBox').innerHTML = exampleList('arguable','Arguable examples');
}
```

CSV:

```js
function csvCell(v){ var s = String(v==null?'':v); return '"'+s.replace(/"/g,'""')+'"'; }
$('csvBtn').addEventListener('click', function(){
  if(!spot.drawn.length) return;
  var header = ['id','symbol','doc_url','date','year','body','mechanism','type','section','text','themes','sdgs','sdg_targets','affected_persons','countries','my_mark','filters_applied'];
  var lines = [header.map(csvCell).join(',')];
  var fdesc = $('filterDesc').textContent;
  spot.drawn.forEach(function(r,i){
    lines.push([r.id,r.symbol,r.doc_url,r.date,r.year,r.body,r.mechanism,r.type,r.section,r.text,
      arr(r.themes).join(' | '), arr(r.sdgs).join(' | '), arr(r.sdg_targets).join(' | '),
      arr(r.affected_persons).join(' | '), arr(r.countries).join(' | '),
      spot.marks[i]||'', fdesc].map(csvCell).join(','));
  });
  var blob = new Blob([lines.join('\r\n')], {type:'text/csv;charset=utf-8'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'sdg-spotcheck-' + String(country).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'') + '-' + new Date().toISOString().slice(0,10) + '.csv';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(function(){ URL.revokeObjectURL(a.href); }, 2000);
});
```

Draw buttons:

```js
$('drawBtn').addEventListener('click', drawSpot);
$('redrawBtn').addEventListener('click', drawSpot);
function drawSpot(){
  if(!currentList.length){ $('spotStatus').textContent = 'No records match the current filters — nothing to draw.'; return; }
  var pool = currentList.slice();
  for(var i=pool.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)); var t=pool[i]; pool[i]=pool[j]; pool[j]=t; }
  var n = Math.min(10, pool.length);
  spot.drawn = pool.slice(0,n);
  spot.marks = {};
  renderSpot();
}
```

update() additions:

```js
var lastSig = null;
function update(){
  var sig = JSON.stringify(state);
  if(sig !== lastSig){
    lastSig = sig;
    if(spot.drawn.length){ spot.drawn=[]; spot.marks={}; renderSpot(); }
  }
  ... existing ...
  // spot controls
  $('drawBtn').disabled = currentList.length === 0;
  if(!spot.drawn.length){
    $('spotStatus').textContent = currentList.length
      ? currentList.length + ' record' + (currentList.length===1?'':'s') + ' currently match the filters — press “Check 10 at random” to draw a sample.'
      : 'No records match the current filters.';
    $('redrawBtn').hidden = true;
  }
}
```

Wait: renderSpot already handles empty drawn (clears list, hides summary, hides redraw). But status text set in update. Order: in update, after computing currentList, call a refreshSpotBar() that sets status/drawBtn disabled when no draw; if draw exists, renderSpot sets status. Let me restructure: in update():

```js
if(sig!==lastSig){ lastSig=sig; if(spot.drawn.length){ spot.drawn=[]; spot.marks={}; } }
...filter, chart, table...
$('drawBtn').disabled = !currentList.length;
if(spot.drawn.length){ renderSpot(); }
else { $('spotList').innerHTML=''; $('spotSummary').hidden=true; $('redrawBtn').hidden=true;
  $('spotStatus').textContent = currentList.length ? ... : 'No records match...'; }
```

But renderSpot also sets redraw.hidden=false and status. OK.

Note: renderSpot is called within update when drawn exists — but renderSpot calls renderSummary which needs allMarked — fine.

Careful: drawSpot is called from button; currentList is current. Good.

Also initial call update() at end — lastSig null → sets lastSig, drawn empty, fine.

One more detail: the note in the spot card should mention CSV columns. Add to note: "The CSV contains one row per drawn record: id, symbol, doc_url, date, body, full text, themes, SDGs, SDG targets, affected persons, countries, your mark, and the filters that were active."

Also mention agreement rate definition. Done in summary note.

Now, also the h2 for spot card: "Spot-check 10 at random". Button label exactly "Check 10 at random" and "Draw again".

Let me also double-check the mark buttons inside spotList re-render on each click — re-rendering whole list on each mark is fine (10 items).

Potential issue: clicking a symbol link inside spot-item — the spotList click handler only handles .markbtn, links work normally. Good.

Now assemble the whole file. Also keep line count reasonable. Let me write it.

Also small thing: `button.primary` disabled style. And `.btnrow` gap.

Also ensure no horizontal scroll: spot-head flex-wrap ok.

Write final HTML now. I'll keep the previous code intact and insert the new card + script parts.

Count lines roughly: previous ~340 lines + ~180 new = ~520. Fine.

One more consideration: "shows, for each, the full text and the SDGs the UN index assigned to it" — done. "When all 10 are marked, show the agreement rate and the wrong and arguable examples" — done in summary. "let me download the 10 records with my marks as CSV" — CSV button in summary. "Add a 'Draw again' button" — done.

Also if fewer than 10 match, we draw all — status says "Drawn N of M matching records" where N=M if <10; add note "fewer than 10 records match, so all of them were drawn". I'll include in status: if n < 10 && currentList.length < 10 → append " (fewer than 10 match, so all were drawn)". Actually n = min(10, len); if len<10 then n=len. Add conditional text.

Let me finalize the code.