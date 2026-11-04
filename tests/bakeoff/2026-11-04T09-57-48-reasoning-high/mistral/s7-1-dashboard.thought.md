Let me plan this app carefully. The user wants a full dashboard on `WORKSHOP_DATA.uhri` with 4 tabs, filters rail, checks tab, export tab. I need to write one complete HTML file, under ~1500 lines, offline, Chart.js preloaded.

Key requirements:
- Header: monospace label "UHRI · {country}", serif title, one line with source (linked), n records, n documents, first–last year, built date, "dated by document" hint.
- Left rail: FILTERS heading + Clear all, big number matching, "of N in the file", red share bar, chips, three numbered collapsible headings (01 Keyword, 02 Mechanism/body/type, 03 Years and SDG), one open at a time, aria-expanded. On tabs 03/04 rail keeps only number, bar, chips (hide the filter headings).
- Tab 01 Overview: big number tiles (total with type breakdown, documents, years), one tile per mechanism (records, documents, latest year, share). FIG.01 top-10 themes bar chart (Chart.js horizontal bars, red at 80%), click bar adds theme chip filter, table under with Theme | Records | % | Years. FIG.02 stacked records per year by mechanism. UPR tile has "see the States" link opening in-place list of top 10 States.
- Tab 02 Records: search field (same as keyword), table with Date | Body | Symbol | Para. | First line | Recommending State. Sort by date desc, body, para numeric asc, file order; clicking Date header reverses. Highlight keyword with <mark>. 50 rows + "Show 50 more". Row expand: para number large red, full text, labels, Copy citation, Open UN document. State select filter joins heading 02 when States extracted.
- Tab 03 Check: check panel lines + random sample label check (10 cards, seeded mulberry32, seed box default 1, Draw again, Draw with this seed, Fits/Doesn't fit/Unsure buttons, tally).
- Tab 04 Method & export: method sentences, Download CSV (Blob), Copy summary, source/licence/build.
- Footer one line monospace.

Filters: keyword (300ms debounce, every word substring of text or symbol, case-insensitive), mechanism, body, type, state, year from/to, sdg. All AND. Chips removable.

Checks:
- record count vs Number(count)
- partitions per mechanism, body, year sum to total
- type partition sums
- chart vs table (recompute)
- links: doc_url starts with https://docs.un.org/ and ends with symbol (case-insensitive after decoding); list failures
- paragraph numbers share per mechanism; UPR expected 100%, lower = warning
- states found: UPR records with ≥1 state vs UPR total; list those without
- duplicates/gaps: distinct id == count; duplicate texts count; records with no themes/sdgs/affected_persons
- random sample: 10 cards from current filter, seeded mulberry32, seed shown, verdict buttons, tally

Paragraph regex: /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/ on text.

State extraction: only UPR. regex trailing run: /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/ then split /\((?:[^()]|\([^()]*\))*\)/g, strip parens, trim. Accept if no comma and ≤60 chars, else "State not found". Record counts once per state.

Citation: symbol + ", para. " + num or symbol alone; button label notes when no para.

First line: text up to 120 chars cut at last space before limit + "…".

Sorting: date desc, body asc, para numeric asc (parse "144.43" as float), then file index. Clicking Date header reverses (toggle asc/desc).

Chart.js: FIG.01 horizontal bar (indexAxis: 'y'), ranked, count at end of bar — I can use a plugin to draw value labels, or just tooltips + table. Requirement says "count at the end of each bar". I'll add a small plugin drawing text after bars. FIG.02 stacked vertical bars per year with mechanism colors, legend.

Clicking a bar adds theme filter chip — need chart onClick handler mapping index to theme, set filter theme, re-render.

Wait — theme filter: the plan mentions clicking a bar adds that theme as a filter chip, but the filter rail spec lists only Keyword, Mechanism/body/type, Years/SDG headings. So theme filter exists as a chip but no heading? The chip is removable. I'll add theme as a chip-only filter (set via chart click). Also maybe state select in heading 02. Chips show active filters including theme and state.

Hmm, "no view shows more than about seven things to click (tabs, filter headings and buttons together)". Tabs = 4, filter headings = 3, Clear all = 1 → 8. Hmm, that's slightly over 7 but "about seven". Plus search box isn't a click. The "see the States" link on tab 01 adds one. It says "about seven" so 8 is fine-ish. I'll keep it.

Layout: header, then a flex layout: left rail (narrow, ~240px) + main content with tablist and panels. On tabs 03/04, hide filter headings (keep number/bar/chips). Actually spec: "shown on tabs 01 and 02; on 03 and 04 the rail keeps only the number, the bar and the chips." So toggle a class on body when tab 3/4 active.

Tabs: role="tablist", buttons role="tab" aria-selected, arrow-key navigation (Left/Right/Home/End), panels role="tabpanel".

Let me think about structure and code size. This will be a big file, maybe 900-1200 lines. Keep it tight.

Data reading:
```js
const U = window.WORKSHOP_DATA.uhri;
const records = U.records;
const country = U.country;
const sdgNames = U.sdg_names || {};
```

Precompute per record: para (regex), states (UPR only), firstLine, year.

State extraction function:
```js
function extractStates(text){
  const m = text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
  if(!m) return [];
  const groups = m[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
  const out = [];
  for(const g of groups){
    const inner = g.slice(1,-1).trim();
    if(inner.includes(',') || inner.length > 60) return ['State not found']; // hmm
    out.push(inner);
  }
  return out;
}
```
Wait — "A group is accepted as a State only if it has no comma and at most 60 characters; otherwise the record gets 'State not found'." So if any group fails, the whole record gets "State not found"? I read it as: the record gets "State not found" (as its state value) if a group is rejected. I'll implement: if any group rejected → states = ["State not found"] (single value). Actually maybe better: accepted groups are states; if a group is rejected, mark record as "State not found". I'll do: if any group fails the rule, return ["State not found"].

Hmm, but nested "Venezuela (Bolivarian Republic of)" — inner after stripping outer parens is "Venezuela (Bolivarian Republic of)", no comma, length fine → accepted as one state name including nested parens. Good, keep as-is.

Filters state object:
```js
const F = { keyword:'', mechanism:'all', body:'all', type:'all', state:'all', theme:'all', yFrom:null, yTo:null, sdg:'all' };
```
Year selects: distinct years sorted; from/to default min/max. Reversed range swapped.

Keyword: trimmed lowercase split on whitespace; every word must be substring of (text+' '+symbol).toLowerCase().

filtered(): loop records, apply all.

Body select options depend on chosen mechanism: bodies present in that mechanism (of full file? "body values present in the chosen mechanism" — I'll compute from all records with that mechanism, with counts). When mechanism changes, reset body to 'all' if current body not in list.

SDG select: goals present in data (from all records), label "16 — Peace, justice and strong institutions" using sdgNames[String(goal)].

Theme filter: chip only, set from chart click. Also maybe allow clicking theme in table? Just chart.

State select: "joins this heading when States are extracted" — put in heading 02, listing every State found with counts (from full file? or filtered? counts of recommendations — I'll compute from all records, or from current filter minus state filter... simpler: from all records). I'll compute from all records.

Rendering approach: a single render() that recomputes filtered set and updates: rail number/bar/chips, and each tab panel's content. To keep simple, re-render each panel fully on filter change (panels are hidden except active, but render all anyway — fine for 2264 records).

Actually re-rendering the table with 50 rows each keystroke is fine.

Charts: Chart.js instances; on filter change, update data. Destroy/recreate or update. I'll keep references and update via chart.data + chart.update(). For FIG.01 click → set F.theme, render.

FIG.01 value labels at end of bars: plugin:
```js
const barLabel = { id:'barLabel', afterDatasetsDraw(chart){ const ctx=chart.ctx; ctx.save(); ctx.font='12px ui-monospace, monospace'; ctx.fillStyle='#1d1b18'; chart.data.datasets.forEach((ds,i)=>{ const meta=chart.getDatasetMeta(i); meta.data.forEach((bar,j)=>{ const v=ds.data[j]; ctx.fillText(String(v), bar.x+6, bar.y+4); }); }); ctx.restore(); } };
```
For horizontal bars (indexAxis 'y'), bar.x is the end. Good.

FIG.02 stacked: labels = all years min..max; datasets per mechanism with colors; stacked: {x:true,y:true} or scales stacked true.

Mechanism colors: UPR #c2410c, Treaty bodies #0f766e, Special Procedures #7c3aed. But mechanism values are exactly those three strings per data description. I'll map by name with fallback palette.

Table rows: build with DOM or innerHTML strings. Use template strings with escaping function. Highlight keyword in first line with <mark>: escape first, then wrap matches. Careful: escape HTML first, then apply mark on escaped text — keyword may contain chars that got escaped. Simpler: highlight on raw text then escape? Do: split firstLine by keyword words... Simplest: escape firstLine, then for each word, replace occurrences in escaped string with <mark> — but word may contain & etc. after escaping mismatch. Given keywords are simple words usually, I'll do case-insensitive replace on the escaped string using escaped word. Acceptable.

Row expansion: click on row toggles a detail row (or expands within the row). I'll render each record as a <tr class="rec"> plus a hidden <tr class="detail"> with colspan. Clicking row toggles. Keyboard: rows as buttons? Make the row have tabindex=0 and Enter/Space toggles, role="button"? Better: put a button in first cell? Spec says "Clicking a row (or pressing Enter on it) expands it in place". I'll make tr tabindex="0" role="button" aria-expanded, keydown Enter/Space.

Detail content: para number large red (or "no paragraph number"), full text verbatim in a <p> (white-space: pre-wrap), labels: themes chips, sdgs with names, sdg_targets list, affected_persons, section when present. Buttons: Copy citation, Open the UN document (link styled as button, target _blank).

Copy citation: navigator.clipboard.writeText with fallback (execCommand). Show "Copied" for 2s.

CSV export: comment lines starting with # : country, source, source_url, built, filters applied, row count. Then header row: Date, Body, Mechanism, Type, Symbol, Doc URL, Paragraph, Recommending States, Section, Themes, SDGs, SDG targets, Affected persons, Text. Quote fields properly. Blob download.

Copy summary: plain text with headline numbers + top ten themes.

Checks tab: compute checks on full file (not filtered? "Check this dashboard" — I'll run on the full file, since checks are about the data; but sample draws from current filter per spec: "Ten records drawn from the current filter"). Checks panel lines:

1. Record count: records.length vs Number(U.count) → pass/fail.
2. Partitions: mechanism counts sum, body counts sum, year counts sum → each equals total.
3. Type partition sums.
4. Chart vs table: recompute top-10 theme counts with second loop, compare to chart data; largest bar ≤ filtered count. (Run against current filter.)
5. Links: every doc_url starts with "https://docs.un.org/" and ends with symbol (case-insensitive, decodeURIComponent). List failures.
6. Paragraph numbers: share per mechanism; UPR expected 100%, lower → warning.
7. States: UPR with ≥1 state (excluding "State not found"? "Number of UPR records with at least one State found" — I'll count records where states.length>0 and not "State not found"... hmm, "State not found" means parentheses held something else. Count records with at least one accepted State; list records without one (including State not found ones) with symbol.
8. Duplicates/gaps: distinct ids == count; duplicate text count (texts appearing more than once — count of records whose text is duplicated? "the number of duplicate text values" — I'll count distinct texts with count>1, and maybe extra records). Records with no themes / no sdgs / no affected_persons counts.

Sample check: seeded mulberry32:
```js
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}
```
Draw 10 distinct records from filtered set using seed. Cards: one line each, one open at a time (accordion). Each card: symbol link, para, full text, theme chips, three buttons Fits / Doesn't fit / Unsure. Tally line: "Themes: x fit, y don't, z unsure of 10 judged · seed 1". Buttons toggle verdict per card (one verdict per card). Store verdicts in a map keyed by record id + seed? Keep simple: verdicts object keyed by record id; re-draw with same seed reproduces same records.

"Draw again" — new random seed (increment or random). "Draw with this seed" — use seed in box. Default seed 1. Show seed in a box (input). Draw again: seed = Math.floor(Math.random()*100000)? But then "a colleague can draw the same ten" via seed box. Draw again picks a new random seed and puts it in the box. Good.

Tab 04 method: 5-6 sentences. CSV download button, copy summary button. Source, licence, build date. Licence: UHRI data — OHCHR, the UHRI terms... I'll say "OHCHR Universal Human Rights Index (UHRI); see source_url" — don't invent licence. The footer: "Built on OHCHR UHRI data · n records · source link". Credits line only if shelf code used — I'm not using shelf code, but the plan lists "Sources consulted" (guidelines). Those aren't code. I could add a small credits line naming the guidance consulted? The rule says credits only if code/wording from Reference shelf excerpts with open licence. I'm not using any, so no credits line needed. But maybe mention sources consulted in method tab as text. Fine.

Now design tokens:
- bg #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335.
- Fonts: Georgia serif for title/big numbers/figure titles; ui-monospace 11-12px uppercase letter-spaced for labels/tabs/fig numbers; system sans 16px body.

Layout: 
```
header (label, h1, meta line)
<div class="layout"> <aside class="rail">…</aside> <main> tablist + panels </main> </div>
footer
```

Rail width ~230px, border-right thin rule. Main flex 1, padding.

Tabs styling: monospace uppercase, numbered "01 OVERVIEW" etc., active red with underline bar.

Filter headings: buttons with number "01 KEYWORD" etc., aria-expanded, chevron. Panels inside.

Chips: small removable buttons with ×.

Big number: serif 48px.

Share bar: div with inner red width %.

Tiles on tab 01: row of tiles — first tile total (with type breakdown lines), documents, years; then mechanism tiles. Use flex wrap, tiles separated by thin rules (border-left). Each tile: label monospace, big number, sub-lines, "How this is computed" note small.

FIG.01: canvas + table. FIG.02: canvas.

Tab 02: search input at top (same as keyword — two inputs synced; I'll have one input in rail heading 01 and one on tab 02; sync both). Actually spec: "One search field across the top ('Search n records…'), the same box as 01 Keyword." So they're the same filter; I'll have two inputs bound to same state, updating each other.

Table: caption with rows shown/matching. thead with Date (clickable button to toggle sort), Body, Symbol, Para., First line, Recommending State. tbody rows. "Show 50 more" button below.

Sorting: default date desc; click Date header toggles to asc; other clicks? Only Date header clickable per spec.

Para sort numeric: parseFloat(para) — "144.43" → 144.43; "71" → 71. Records without para → Infinity? Spec: "then paragraph number ascending (numeric, so 10 follows 9), then the order in the file". For no-para records, put them... use Infinity so they go last within same date/body. Fine.

Now, mechanism tiles on tab 01: "one tile per mechanism (records, documents, latest year, share of the filtered set)". Share of filtered set — of the current filter. And UPR tile has "see the States" link opening in-place list "Ten States that made most recommendations to Kenya" with counts for current filter. Country name from data.

Wait — "Ten States that made most recommendations to Kenya" — country from U.country. Only UPR records count.

Let me now also handle: on tabs 03/04, rail shows only number/bar/chips — I'll add class to rail via body dataset.tab.

Edge: filter matches nothing → tiles 0, chart area "No records match", table caption says so.

Year selects: options from distinct years of full file (spec: "two selects of the distinct years"; "Years with no records… are absent from the year selects"). From/to default to min/max. On change, if from>to swap.

SDG select: goals present in data (union over all records' sdgs), sorted numerically, label `${g} — ${sdgNames[String(g)] || ''}`.

Now the checks — "Chart against table": recompute top10 from filtered with independent loop and compare to what's displayed. Since same code computes both, it's a bit circular, but I'll write a separate function recomputeThemes() used by check, and compare with the chart's data array. Fine.

Links check: doc_url starts with "https://docs.un.org/" — sample shows "https://docs.un.org/en/...". Ends with symbol case-insensitive after decoding: decodeURIComponent(doc_url).toLowerCase().endsWith(symbol.toLowerCase()). List failures (symbol + doc_url).

Paragraph share per mechanism: count records where para found / total per mechanism. UPR expected 100%; if <100% show warning (amber/red text "warning").

States check: UPR records; found = states.length>0 && states[0] !== 'State not found'... Actually a record could have multiple groups where one fails → whole record "State not found". Count records with at least one accepted state. List UPR records without: symbol + maybe snippet of trailing parens.

Duplicates: distinct id count vs records.length; duplicate texts: group by text, count groups with >1 → "n duplicate text values (m extra records)". Missing labels: no themes, no sdgs, no affected_persons counts.

Now write the code. I'll aim for clean, compact JS. Let me draft.

HTML skeleton:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UHRI · <country> — UN recommendations dashboard</title>
<style>…</style>
</head>
<body>
<header>
  <div class="kicker" id="kicker">UHRI · <span id="countryLabel"></span></div>
  <h1 id="title"></h1>
  <p class="meta" id="metaLine"></p>
</header>
<div class="layout">
  <aside class="rail" id="rail">
    <div class="rail-head"><span class="lbl">FILTERS</span><button id="clearAll" class="linkbtn">Clear all</button></div>
    <div class="bignum" id="matchNum" aria-live="polite">0</div>
    <div class="ofline">matching records · of <span id="totalNum"></span> in the file</div>
    <div class="sharebar"><div id="shareFill"></div></div>
    <div class="chips" id="chips"></div>
    <div class="filters" id="filterBlocks">
      <section> <button class="fhead" aria-expanded="false" data-block="kw"><span>01 KEYWORD</span>…</button>
        <div class="fbody" hidden> input + hint </div></section>
      <section> 02 MECHANISM, BODY, TYPE: selects mechanism, body, type, state </section>
      <section> 03 YEARS AND SDG: year from, year to, sdg </section>
    </div>
  </aside>
  <main>
    <div class="tablist" role="tablist" id="tablist">
      <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 OVERVIEW</button>
      ... 02 RECORDS, 03 CHECK, 04 METHOD & EXPORT
    </div>
    <section role="tabpanel" id="panel-0" aria-labelledby="tab-0">…</section>
    ...
  </main>
</div>
<footer id="footer"></footer>
<script>…</script>
</body>
</html>
```

CSS: keep it editorial. Let me write it.

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
header{padding:28px 32px 18px;border-bottom:1px solid var(--rule);}
.kicker{font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--red);}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:34px;margin:10px 0 8px;max-width:900px;}
.meta{font-size:13px;color:#4a463f;margin:0;}
.meta a{color:var(--ink)}
.layout{display:flex;align-items:flex-start;}
.rail{width:250px;flex:0 0 250px;padding:20px 20px 40px 32px;border-right:1px solid var(--rule);position:sticky;top:0;max-height:100vh;overflow:auto;}
main{flex:1;min-width:0;padding:20px 32px 60px;}
...
```

Focus ring: `:focus-visible{outline:2px solid var(--red);outline-offset:2px}`.

Tabs:
```css
.tablist{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin-bottom:24px;}
.tablist [role=tab]{font:11px ui-monospace,...;letter-spacing:.14em;text-transform:uppercase;background:none;border:none;border-bottom:2px solid transparent;padding:10px 14px;cursor:pointer;color:#6b655b;}
.tablist [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red);}
```

Tiles:
```css
.tiles{display:flex;flex-wrap:wrap;gap:0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-bottom:28px;}
.tile{padding:18px 24px 14px 0;margin-right:24px;border-right:1px solid var(--rule);} last no border... use .tile+.tile{border-left...} hmm simpler: .tile{padding:16px 28px 12px 0;} .tile+.tile{border-left:1px solid var(--rule);padding-left:28px;}
.tile .lbl{...monospace}
.tile .num{font-family:Georgia,serif;font-size:52px;line-height:1;}
.tile .sub{font-size:13px;}
.tile .how{font-size:11px;color:#6b655b;font-family:monospace? } 
```
"How this is computed" line — small, maybe sans 12px italic? Keep sans 12px gray.

Figures:
```css
.fig{margin:28px 0;}
.fig .fighead{display:flex;justify-content:space-between;align-items:baseline;}
.figtitle{font-family:Georgia,serif;font-size:20px;}
.figno{font:11px monospace;color:var(--red);letter-spacing:.15em;}
.src{font-size:12px;color:#6b655b;margin-top:6px;}
canvas{max-width:100%;}
```

Table:
```css
table{border-collapse:collapse;width:100%;font-size:14px;}
caption{text-align:left;font-size:13px;color:#4a463f;padding:6px 0;}
th{font:11px monospace uppercase;letter-spacing:.1em;text-align:left;border-bottom:1px solid var(--ink);padding:8px 10px 8px 0;}
td{padding:8px 10px 8px 0;border-bottom:1px solid var(--rule);vertical-align:top;}
td.num,th.num{text-align:right;}
th button{sort button styling}
tr.rec{cursor:pointer}
tr.rec:hover{background:#ece6d9}
tr.detail td{background:#efe9dc;padding:16px 20px;}
mark{background:#f3d9a4? } hmm accent — mark with soft red? background:#f0c9cd; color inherit. Use rgba(155,35,53,.18).
```

Chips:
```css
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 16px;}
.chip{font:11px monospace;border:1px solid var(--red);color:var(--red);background:none;border-radius:999px;padding:3px 8px;cursor:pointer;}
```

Filter blocks:
```css
.fhead{display:flex;justify-content:space-between;width:100%;background:none;border:none;border-top:1px solid var(--rule);padding:12px 0;font:11px monospace;letter-spacing:.14em;cursor:pointer;color:var(--ink);text-transform:uppercase;}
.fhead .arrow{color:var(--red)}
.fbody{padding:4px 0 14px;}
select,input[type=text]{width:100%;background:#fff? } paper theme: background:#fbf8f1;border:1px solid var(--rule);padding:7px 8px;font:14px sans;color:ink;border-radius:0;margin-bottom:10px;
.hint{font:11px monospace;color:#6b655b;}
```

Share bar:
```css
.sharebar{height:4px;background:var(--rule);margin:8px 0 4px;}
#shareFill{height:100%;background:var(--red);width:0%;}
```

Big num: `.bignum{font-family:Georgia,serif;font-size:48px;line-height:1;margin-top:14px;}`

Buttons: `.btn{border:1px solid var(--ink);background:none;padding:8px 14px;font:12px monospace;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;} .btn:hover{background:var(--ink);color:var(--paper)}` and `.linkbtn{background:none;border:none;color:var(--red);font:11px monospace;cursor:pointer;text-decoration:underline;}`

Check panel lines: `.checkline{padding:8px 0;border-bottom:1px solid var(--rule);font-size:14px;display:flex;gap:10px;} .pass{color:#0f766e} .fail{color:var(--red);font-weight:600} .warn{color:#b45309}` — hmm "one accent" rule; pass marks... The design says one accent deep red; other colours only where a category needs one. Pass/fail semantics need distinction; I'll use red for fail, and ink with "✓ pass" for pass, amber for warning. Keep minimal: pass = "✓" in ink, fail = red "✗ check failed", warn = red-ish? Use "⚠ warning" in #b45309. Acceptable.

Sample cards: `.card{border:1px solid var(--rule);border-top:none? }` Use border-top rule per card, one open at a time: card header button (symbol + para + first 80 chars), body hidden with full text, chips, verdict buttons. Verdict buttons: `.vbtn` toggles active state (red border/fill).

Now JS. Let me write it carefully.

```js
(function(){
"use strict";
const U = window.WORKSHOP_DATA.uhri;
const RECS = U.records;
const COUNTRY = U.country;
const SDGN = U.sdg_names || {};
const TOTAL = RECS.length;

// precompute
const PARA_RE = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
RECS.forEach((r,i)=>{
  r._i = i;
  const m = (r.text||"").match(PARA_RE);
  r._para = m ? m[1] : null;
  r._paraNum = m ? parseFloat(m[1]) : Infinity;
  r._states = (r.mechanism === "Universal Periodic Review") ? extractStates(r.text||"") : null;
  r._first = firstLine(r.text||"");
});
```

extractStates:
```js
function extractStates(text){
  const m = text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
  if(!m) return [];
  const groups = m[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
  const out = [];
  for(const g of groups){
    const inner = g.slice(1,-1).trim();
    if(inner.includes(",") || inner.length > 60) return ["State not found"];
  }
  for(const g of groups){ out.push(g.slice(1,-1).trim()); }
  return out;
}
```

firstLine:
```js
function firstLine(t){
  if(t.length <= 120) return t;
  const cut = t.slice(0,120);
  const sp = cut.lastIndexOf(" ");
  return (sp > 0 ? cut.slice(0,sp) : cut) + "…";
}
```

Filters:
```js
const F = { kw:"", mech:"all", body:"all", type:"all", state:"all", theme:"all", yFrom:"", yTo:"", sdg:"all" };
const YEARS = [...new Set(RECS.map(r=>r.year))].sort((a,b)=>a-b);
F.yFrom = YEARS[0]; F.yTo = YEARS[YEARS.length-1];
```

keyword words:
```js
function kwWords(){ return F.kw.trim().toLowerCase().split(/\s+/).filter(Boolean); }
function matchKw(r, words){ if(!words.length) return true; const hay = (r.text+" "+r.symbol).toLowerCase(); return words.every(w=>hay.includes(w)); }
function filtered(){
  const words = kwWords();
  const yF = +F.yFrom, yT = +F.yTo;
  return RECS.filter(r =>
    (F.mech==="all" || r.mechanism===F.mech) &&
    (F.body==="all" || r.body===F.body) &&
    (F.type==="all" || r.type===F.type) &&
    (F.state==="all" || (r._states||[]).includes(F.state)) &&
    (F.theme==="all" || (r.themes||[]).includes(F.theme)) &&
    (F.sdg==="all" || (r.sdgs||[]).includes(+F.sdg)) &&
    r.year>=yF && r.year<=yT &&
    matchKw(r, words)
  );
}
```

Wait: state filter — a record with multiple states counts for each; includes works. "State not found" records: _states = ["State not found"], so selecting that in the select would match them. I'll include "State not found" in the select list too? Spec says select lists every State found. I'll list actual states plus "(State not found)" entry maybe. Keep: list all distinct state values including "State not found" labelled as such. Fine.

Body options depend on mechanism:
```js
function bodiesFor(mech){ const set = new Map(); RECS.forEach(r=>{ if(mech==="all"||r.mechanism===mech) set.set(r.body,(set.get(r.body)||0)+1); }); return [...set.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])); }
```

Mechanisms: distinct values sorted. Types: distinct. SDGs present: union sorted numeric.

Render functions:

renderRail(): matchNum = filtered.length, totalNum, shareFill width %, chips.

Chips: for each active filter (kw, mech, body, type, state, theme, yFrom/yTo if not default, sdg) a chip with label and × that clears it.

renderOverview(): tiles + charts + theme table + states list.

Tiles: 
- Tile 1: label "ALL RECORDS IN THE FILE"? Wait — "The first tile counts all records in the file" — hmm, but everything reads the filtered set... "The first tile counts **all records** in the file: recommendations, concerns/observations and any other type. Under the number, one line gives the breakdown per type". Hmm, ambiguous: does the first tile ignore filters? "Every tab reads the same filtered set" but the first tile "counts all records in the file". I think the first tile shows the file total (records.length) with type breakdown of the whole file, while mechanism tiles show filtered. Actually re-reading: "A row of big serif numbers. The first tile counts all records in the file... Beside it: documents (distinct symbol) and years (min–max of year). Below, one tile per mechanism (records, documents, latest year, share of the filtered set)." The mechanism tiles explicitly say "share of the filtered set", implying the first row is about the file. But then "The Type filter (all / each type value present) starts on 'all'" — there's a Type filter... in the rail heading 02. Hmm "The Type filter (all / each type value present) starts on 'all'" appears in the Overview description — maybe meaning the type breakdown line reflects... I'll interpret: first tile = total in file (records.length) with per-type breakdown of the whole file; documents and years of the whole file. Mechanism tiles use the filtered set. That matches "counts all records in the file". But then "Every tile and figure has a one-line How this is computed note" — the note will say "all records in the file, before filters" for tile 1 and "of the n filtered records" for mechanism tiles. Hmm, but that could confuse. Alternatively first tile = filtered count... but rail already shows matching count. The plan explicitly says "counts all records in the file", so file total. OK.

Actually wait, maybe safer: first tile shows file total; and I'll add in its "how" note "all records in the file, before filters; the filtered count is in the rail". Good.

- Documents tile: distinct symbols in file. Years tile: min–max year in file.
- Mechanism tiles: for each mechanism (of the file), records in filtered set with that mechanism, documents (distinct symbols among filtered with that mechanism), latest year (max year among filtered with that mechanism), share = count/filtered.length. UPR tile includes "see the States" link toggling a list.

FIG.01: top 10 themes among filtered. Compute counts; ties alphabetical. Chart horizontal bars red 80% (rgba(155,35,53,.8)). Click → F.theme = theme; render. Table under: Theme | Records | % of filtered | Years (first–last). Note about multi-theme.

FIG.02: years from min to max of file (or of filtered? "every year from the first to the last appears" — first to last of what? Probably of the file/data; I'll use file min..max so gaps visible; but if filter narrows... spec says "Records per year by mechanism: stacked bars for the current filter; every year from the first to the last appears, so empty years are visible gaps." I'll use file-wide min..max). Datasets per mechanism present in file, colors mapped, zeros for missing.

Chart creation: create once, update on render. If filtered empty → show "No records match" text instead of chart (hide canvas, show div).

renderRecords(): search input value sync, caption "Showing X of Y matching records (newest first)" — Y = filtered.length, X = shown count. Table rows: sorted copy of filtered. Sort: date desc (string compare works for ISO dates), body asc, _paraNum asc, _i asc. Toggle dateAsc on header click.

Rows: build HTML string. For each row: date, body, symbol link, para (or "—"), first line with mark highlight, states (join "; " or "—" for non-UPR).

Highlight: 
```js
function esc(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}
function markify(s, words){ let out = esc(s); for(const w of words){ if(!w) continue; const ew = esc(w); out = out.replace(new RegExp(ew.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"),"gi"), m=>"<mark>"+m+"</mark>"); } return out; }
```
Careful: escaping word then regex — esc(w) may contain &amp; etc; regex-escape it. OK.

Row click: event delegation on tbody; toggle detail row. I'll render detail row hidden after each record row; toggle hidden + aria-expanded on the tr. Detail content built lazily on first expand.

Detail: 
```html
<tr class="detail" hidden><td colspan="6">
  <div class="para-big">para. 54</div> or <div class="para-big none">no paragraph number in this extract</div>
  <p class="fulltext">…verbatim…</p>
  labels block: section (if), themes chips, sdgs (with names), sdg_targets, affected_persons
  <div class="rowbtns"><button class="btn copybtn">Copy citation</button> <a class="btn" href=doc_url target=_blank>Open the UN document</a></div>
</td></tr>
```

Copy citation: text = symbol + (para? ", para. "+para : ""). Button label: "Copy citation" or "Copy citation (no paragraph number in this extract)". On click, clipboard write, show "Copied ✓" 2s.

Clipboard: navigator.clipboard may fail in sandbox; fallback textarea+execCommand. Wrap in try.

Show 50 more: shownCount variable, reset to 50 on filter change; button shows remaining.

renderCheck(): compute checks, render lines. Sample: seed input (default 1), buttons Draw again (random seed), Draw with this seed. Cards drawn from current filtered set. mulberry32. Draw 10 distinct indices:
```js
function drawSample(seed, arr, n){
  const rnd = mulberry32(seed);
  const idx = [...arr.keys()];
  // Fisher-Yates partial
  for(let i=idx.length-1;i>0;i--){ const j = Math.floor(rnd()*(i+1)); [idx[i],idx[j]]=[idx[j],idx[i]]; }
  return idx.slice(0, Math.min(n, idx.length)).map(k=>arr[k]);
}
```

Verdicts: `const verdicts = {}` keyed by record id (per draw). Card: header button (aria-expanded) with symbol + para + snippet; body: full text, theme chips, three buttons. Clicking verdict sets verdicts[id] = 'fit'|'no'|'unsure', re-render tally and button states. Tally: "Themes: x fit, y don't, z unsure of 10 judged · seed N · drawn from the current filter (n records)". Line above cards: "This is your judgement of the UN's labels; nothing is sent anywhere."

renderMethod(): static text + buttons. CSV:

```js
function csvCell(s){ s = s==null?"":String(s); return /[",\n]/.test(s) ? '"'+s.replace(/"/g,'""')+'"' : s; }
function downloadCSV(){
  const rows = filtered();
  const lines = [];
  lines.push("# Country: "+COUNTRY);
  lines.push("# Source: "+U.source+" ("+U.source_url+")");
  lines.push("# Built: "+U.built);
  lines.push("# Filters: "+describeFilters());
  lines.push("# Rows: "+rows.length+" of "+TOTAL+" records");
  const head = ["Date","Body","Mechanism","Type","Symbol","Doc URL","Paragraph","Recommending State(s)","Section","Themes","SDGs","SDG targets","Affected persons","Text"];
  lines.push(head.map(csvCell).join(","));
  rows.forEach(r=>{ lines.push([r.date,r.body,r.mechanism,r.type,r.symbol,r.doc_url,r._para||"",(r._states||[]).join("; "),r.section||"",(r.themes||[]).join("; "),(r.sdgs||[]).join("; "),(r.sdg_targets||[]).join("; "),(r.affected_persons||[]).join("; "),r.text].map(csvCell).join(",")); });
  const blob = new Blob([lines.join("\n")], {type:"text/csv;charset=utf-8"});
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "uhri-"+COUNTRY.toLowerCase()+"-recommendations.csv"; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(a.href),1000);
}
```

Copy summary: navigator.clipboard.writeText(summaryText) with fallback; show confirmation.

Summary text: e.g.
```
UN human rights recommendations and observations: Kenya (OHCHR UHRI, built {built}).
{total} records from {docs} documents, {minYear}–{maxYear}: {rec} Recommendations, {conc} Concerns/Observations, ...
Top themes among {n} filtered records: 1. Reservations (691) ...
Filters applied: ...
```

Tab switching: buttons set active, panels hidden, body.dataset.tab = index; rail filter blocks hidden on tabs 2,3 (index 2,3). Arrow keys on tablist.

Filter heading accordions: one open at a time; clicking toggles; aria-expanded.

Keyword debounce 300ms on both inputs.

Now, "no view shows more than about seven things to click": tab 01 has 4 tabs + 3 filter headings + clear all = 8 clickable, plus chart bars (not counted), plus "see the States" link = 9. Hmm. "about seven" — tabs+filter headings+buttons together. 4+3+1=8, plus states link on tab 01 = 9. Slightly over. Could move "Clear all"... it's required. I think "about seven" tolerates 8-9. The spec itself mandates these elements, so follow the spec.

Let me also handle mechanism tile "see the States" — a link in UPR tile; clicking toggles a div under the tiles listing top 10 states with counts for current filter: "Ten States that made most recommendations to {country}".

Now checks details:

```js
function runChecks(){
  const lines = [];
  // 1 record count
  const declared = Number(U.count);
  lines.push({t:`Record count: records.length = ${TOTAL} vs count field = ${declared}`, ok: TOTAL===declared});
  // partitions
  const sum = obj => Object.values(obj).reduce((a,b)=>a+b,0);
  const byMech = countBy(RECS, r=>r.mechanism);
  ...
}
```

I'll write helper countBy.

Links check: 
```js
const badLinks = RECS.filter(r=>{ const u=r.doc_url||""; let ok = u.startsWith("https://docs.un.org/"); try{ ok = ok && decodeURIComponent(u).toLowerCase().endsWith((r.symbol||"").toLowerCase()); }catch(e){ ok=false; } return !ok; });
```
List up to, say, all failing symbols (could be many; cap at 20 with "and n more").

Paragraph share per mechanism: for each mechanism, share with _para. UPR expected 100% → if <1, warn.

States: upr = RECS.filter(r=>r.mechanism==="Universal Periodic Review"); found = upr.filter(r=>r._states && r._states.length && r._states[0]!=="State not found"); list upr without found (symbol + trailing snippet). Cap list.

Duplicates: distinct ids via Set; dupTexts: map text→count, count of texts with >1, and extra records = sum(count-1). Missing labels counts.

Chart vs table check: recompute top10 via separate loop over filtered, compare to displayed chart data (store last chart data in a var). Also largest ≤ filtered.length.

Render check lines with ✓ / ✗ / ⚠.

Now sizes: this is a lot but manageable. Let me be disciplined and write the final file. Target maybe 1000-1300 lines. Let me write it.

Also note: `count` is a string "2264" — Number(U.count).

Header meta line: `Source: <a href=source_url>OHCHR Universal Human Rights Index</a> · n records · n documents · 2007–2026 · built 2026-… · dated by document`. Source text: U.source. Use U.source as link text.

Footer: "Built on OHCHR UHRI data · {n} records · <a>source</a>".

Title: "UN human rights recommendations and observations: {country}".

Kicker: "UHRI · {country}".

Let me now also decide the tab names: "01 OVERVIEW", "02 RECORDS", "03 CHECK", "04 METHOD & EXPORT".

Panels:

Panel 0 (Overview):
```html
<div class="tiles" id="tiles"></div>
<div class="statesbox" id="statesBox" hidden>…</div>
<div class="fig" id="fig1">…canvas + table…</div>
<div class="fig" id="fig2">…canvas…</div>
```

Panel 1 (Records): search input, table, show more.

Panel 2 (Check): checks div + sample controls + cards + tally.

Panel 3 (Method): paragraphs, buttons, source info.

Now write JS render functions with template literals. Must be careful with quotes in text (escape everything user-data-derived).

For the theme table and chart: store `state.top10` for check comparison.

Chart.js config FIG.01:
```js
fig1Chart = new Chart(ctx, {
  type:"bar",
  data:{labels: themes, datasets:[{data: counts, backgroundColor:"rgba(155,35,53,.8)", borderWidth:0, barThickness: 18}]},
  options:{
    indexAxis:"y",
    responsive:true, maintainAspectRatio:false,
    onClick:(e, els)=>{ if(els.length){ const t = fig1Chart.data.labels[els[0].index]; setFilter('theme', t); } },
    plugins:{ legend:{display:false}, tooltip:{callbacks:{label:c=>c.parsed.x+" records"}} },
    scales:{ x:{beginAtZero:true, ticks:{precision:0}, grid:{color:"#e5dfd2"}}, y:{grid:{display:false}, ticks:{font:{size:13}}} }
  },
  plugins:[barValuePlugin]
});
```
Canvas height: set wrapper height ~ 320px.

barValue plugin draws counts at bar end:
```js
const barValue = { id:"barValue", afterDatasetsDraw(chart){ const {ctx} = chart; const meta = chart.getDatasetMeta(0); ctx.save(); ctx.font = "12px ui-monospace, Menlo, monospace"; ctx.fillStyle = "#1d1b18"; meta.data.forEach((bar,i)=>{ const v = chart.data.datasets[0].data[i]; ctx.fillText(String(v), bar.x + 6, bar.y + 4); }); ctx.restore(); } };
```

FIG.02:
```js
new Chart(ctx2, {type:"bar", data:{labels: yearsArr, datasets: mechs.map(m=>({label:m, data: counts, backgroundColor: colorFor(m), stack:"s"}))}, options:{responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, grid:{display:false}}, y:{stacked:true, beginAtZero:true, ticks:{precision:0}}}, plugins:{legend:{position:"top", labels:{usePointStyle:true, boxWidth:8}}}}});
```
Colors: map {"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"} fallback palette.

Update on render: set chart.data.labels/datasets then chart.update(). If filtered empty: hide canvas wrapper, show "No records match the current filters." div.

Mechanism tiles: for each mechanism in file order (sorted by count desc?). "one tile per mechanism" — order by count desc. Include records count in filtered, documents, latest year, share %. How note: "of the n filtered records".

Now the rail filter blocks content:

Block 01 KEYWORD: input#kwRail (text), hint "literal match, not synonyms · every word must appear in the text or symbol · applied 300 ms after typing". 

Block 02: 
- label MECHANISM + select#mechSel (all + values)
- label BODY OR MANDATE + select#bodySel (all + bodiesFor(F.mech) with counts)
- label TYPE + select#typeSel
- label RECOMMENDING STATE + select#stateSel (all + states with counts) — "joins this heading when States are extracted" — always present since UPR exists; if no states at all, hide.

Block 03:
- YEAR FROM select, YEAR TO select
- SDG select (all + goals present with names)

On mech change: rebuild body options; if F.body not in new list, set "all".

Year change: if from>to swap both.

Chips labels: e.g. `keyword: "torture"`, `mechanism: UPR`, `body: CEDAW`, `type: Recommendations`, `state: Cuba`, `theme: Reservations`, `years: 2010–2020`, `sdg: 16`. Chip click clears that filter (reset to default) and re-renders.

describeFilters() for CSV comments and summary.

Now tab keyboard nav:
```js
tablist.addEventListener("keydown", e=>{
  const tabs = [...tablist.querySelectorAll("[role=tab]")];
  let i = tabs.indexOf(document.activeElement);
  if(i<0) return;
  if(e.key==="ArrowRight") i=(i+1)%tabs.length;
  else if(e.key==="ArrowLeft") i=(i-1+tabs.length)%tabs.length;
  else if(e.key==="Home") i=0;
  else if(e.key==="End") i=tabs.length-1;
  else return;
  e.preventDefault(); tabs[i].focus(); tabs[i].click();
});
```

Row expansion: delegation:
```js
tbody.addEventListener("click", e=>{ const tr = e.target.closest("tr.rec"); if(tr) toggleRow(tr); });
tbody.addEventListener("keydown", e=>{ if(e.key==="Enter"||e.key===" "){ const tr = e.target.closest("tr.rec"); if(tr){ e.preventDefault(); toggleRow(tr);} } });
```
toggleRow: find next sibling tr.detail, toggle hidden, set aria-expanded on tr, build detail if not built.

Detail build function detailHTML(r).

Copy citation button inside detail: delegation on tbody for .copybtn click — but row click also fires; stopPropagation in copy handler.

Sort header: th contains button "Date" — click toggles state.dateAsc, re-render records panel, update caption "(newest first)"/"(oldest first)".

Show more: state.shown; on filter change reset to 50.

Search inputs: two (rail + tab02). Both input events → debounce 300ms → F.kw = value; sync other input; renderAll.

renderAll(): const f = filtered(); state.filtered = f; renderRail(f); renderOverview(f); renderRecords(f); renderCheck(f); (method static, but summary uses filter → renderMethod(f) too or just update on demand; I'll re-render method's dynamic bits lightly — actually method tab is static text + buttons; CSV/summary computed at click time from current filter. So no need to re-render.)

But checks use filtered for chart-vs-table and sample; re-render check each time is fine (2264 records, cheap).

Performance: renderRecords builds up to 50 rows + details lazily — fine. renderOverview loops filtered a few times — fine.

Now, sample cards "listed as one line each, one open at a time": card header is a button; opening one closes others.

Verdict buttons per card: three buttons; clicking sets verdict; active one gets red style. Tally updates.

Seed handling: state.seed = 1; input#seedInput value 1. "Draw again": state.seed = 1+Math.floor(Math.random()*99999); set input; draw. "Draw with this seed": state.seed = parseInt(input.value)||1; draw. Draw uses current filtered.

Edge: filtered empty → sample area shows "No records match the current filters."

Now write method text (5-6 sentences):
1. Every number on this page is computed in your browser by looping over the records in the attached file; nothing is estimated and no model is called.
2. The headline total is records.length; documents are distinct symbol values; years are the minimum and maximum of year.
3. Filters combine with AND: mechanism, body, type, recommending State and theme are exact matches; the year range is inclusive; the SDG filter keeps records whose sdgs list contains the goal; the keyword filter keeps records where every typed word appears in the text or the symbol (literal, case-insensitive).
4. Theme counts count each theme once per record, so they add up to more than the record count; percentages are of records.
5. Paragraph numbers are read from the start of the text with a regular expression; UPR recommending States are read from the parentheses at the end of UPR texts only.
6. The CSV export contains the filtered records with the full text and labels, generated in the browser as a Blob; the only thing that can leave the page is the clipboard write when you press Copy.

Source/licence/build: "Data: {U.source} ({U.source_url}), built {U.built}. The Universal Human Rights Index is published by OHCHR; check the source page for its terms of use." Don't invent licence.

Footer: `Built on OHCHR UHRI data · {TOTAL} records · <a href="{source_url}">{source}</a>`.

Now — the "How this is computed" notes:
- Tile 1: "All records in the file, before filters; the filtered count is the big number in the rail."
- Documents: "Distinct symbol values across all records in the file."
- Years: "Minimum and maximum of year across all records; dated by document."
- Mechanism tiles: "Records, distinct symbols and latest year among the n filtered records; share = tile count ÷ n."
- FIG.01: "Each theme counts once per filtered record that carries it; ties alphabetical; click a bar to filter."
- FIG.02: "Records per year and mechanism in the filtered set; years with no records appear as gaps."

Table caption tab 02: "Showing {shown} of {n} matching records · newest first" (or oldest first).

OK. Also the "see the States" list: heading "Ten States that made most recommendations to {country} (current filter)" with rows State | Recommendations. Counts: for filtered UPR records, each state counts once.

Let me now write the whole file. I'll be careful about escaping in template literals (backticks inside? avoid). Use functions returning strings.

One more detail: `aria-live="polite"` on matchNum. Chips removable: button with aria-label "Remove filter X".

Also `[hidden]{display:none!important}` rule included.

Let me write CSS fully:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--muted:#6b655b;}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
a{color:var(--ink)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header{padding:26px 36px 16px;border-bottom:1px solid var(--rule)}
.kicker{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--red)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:clamp(26px,3.4vw,36px);line-height:1.15;margin:10px 0 8px;max-width:920px}
.meta{margin:0;font-size:13px;color:#4a463f}
.layout{display:flex;align-items:flex-start}
.rail{flex:0 0 252px;width:252px;border-right:1px solid var(--rule);padding:18px 18px 60px 36px;position:sticky;top:0;max-height:100vh;overflow-y:auto}
.railhead{display:flex;justify-content:space-between;align-items:baseline}
.lbl{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
.linkbtn{background:none;border:none;padding:0;color:var(--red);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.06em;cursor:pointer;text-decoration:underline}
.bignum{font-family:Georgia,serif;font-size:50px;line-height:1;margin-top:16px}
.ofline{font-size:12px;color:var(--muted);margin-top:2px}
.sharebar{height:4px;background:var(--rule);margin:10px 0 6px}
.sharefill{height:100%;background:var(--red);width:0;transition:width .2s}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 14px;min-height:4px}
.chip{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;border:1px solid var(--red);color:var(--red);background:transparent;border-radius:999px;padding:2px 4px 2px 10px;cursor:pointer}
.chip b{font-weight:400;margin-left:6px}
.fblock{border-top:1px solid var(--rule)}
.fhead{display:flex;justify-content:space-between;align-items:center;width:100%;background:none;border:none;padding:12px 0 10px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink);text-align:left}
.fhead .arr{color:var(--red)}
.fbody{padding:2px 0 16px}
.flabel{display:block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:10px 0 4px}
select,input[type=text],input[type=number]{width:100%;background:#fbf8f1;border:1px solid var(--rule);border-radius:0;padding:7px 8px;font:14px/1.3 -apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink)}
.hint{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;color:var(--muted);margin-top:6px;line-height:1.5}
main{flex:1;min-width:0;padding:18px 36px 70px}
.tablist{display:flex;flex-wrap:wrap;border-bottom:1px solid var(--rule);margin-bottom:26px}
.tablist [role=tab]{appearance:none;background:none;border:none;border-bottom:2px solid transparent;margin-bottom:-1px;padding:10px 16px 9px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.tablist [role=tab]:hover{color:var(--ink)}
.tablist [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.panel[hidden]{display:none}
.tiles{display:flex;flex-wrap:wrap;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-bottom:8px}
.tile{padding:16px 26px 12px 0}
.tile+.tile{border-left:1px solid var(--rule);padding-left:26px}
.tile .num{font-family:Georgia,serif;font-size:46px;line-height:1.05}
.tile .sub{font-size:13px;margin-top:4px}
.tile .how{font-size:11.5px;color:var(--muted);margin-top:6px;max-width:230px}
.fig{margin:30px 0 8px}
.fighead{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.figno{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.18em;color:var(--red)}
.figtitle{font-family:Georgia,serif;font-size:21px}
.figsub{font-size:13px;color:var(--muted)}
.src{font-size:12px;color:var(--muted);margin-top:8px}
.chartwrap{position:relative;height:340px;margin-top:14px}
.chartwrap.tall{height:380px}
.nomatch{font-family:Georgia,serif;font-size:20px;color:var(--muted);padding:30px 0}
table{border-collapse:collapse;width:100%;font-size:14px;margin-top:10px}
caption{caption-side:top;text-align:left;font-size:13px;color:#4a463f;padding:0 0 8px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:400;text-align:left;border-bottom:1px solid var(--ink);padding:6px 12px 8px 0;white-space:nowrap}
td{padding:8px 12px 8px 0;border-bottom:1px solid var(--rule);vertical-align:top}
th.num,td.num{text-align:right}
th .sortbtn{background:none;border:none;padding:0;font:inherit;letter-spacing:inherit;text-transform:inherit;cursor:pointer;color:inherit;text-decoration:underline}
tr.rec{cursor:pointer}
tr.rec:hover td{background:#ece5d6}
tr.rec:focus-visible{outline:2px solid var(--red);outline-offset:-2px}
tr.detail td{background:#efe9db;padding:18px 22px}
.sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;white-space:nowrap}
.parabig{font-family:Georgia,serif;font-size:34px;color:var(--red);margin-bottom:8px}
.fulltext{white-space:pre-wrap;font-size:15px;max-width:880px;margin:0 0 14px}
.tagrow{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0}
.tag{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;border:1px solid var(--rule);padding:2px 8px;border-radius:999px;background:#fbf8f1}
.lbl2{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:12px 0 4px}
.btn{display:inline-block;border:1px solid var(--ink);background:transparent;color:var(--ink);padding:8px 14px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;text-decoration:none;margin:4px 8px 4px 0}
.btn:hover{background:var(--ink);color:var(--paper)}
.btn.primary{border-color:var(--red);color:var(--red)}
.btn.primary:hover{background:var(--red);color:var(--paper)}
mark{background:rgba(155,35,53,.22);color:inherit;padding:0 1px}
.statesbox{border:1px solid var(--rule);padding:14px 18px;margin:14px 0 4px;max-width:560px}
.checkline{display:flex;gap:10px;padding:9px 0;border-bottom:1px solid var(--rule);font-size:14px;align-items:baseline}
.checkline .mark{font-family:ui-monospace,monospace;font-size:12px;flex:0 0 150px}
.ok{color:#0f766e}.bad{color:var(--red);font-weight:600}.warn{color:#b45309}
.card{border-top:1px solid var(--rule)}
.card:last-child{border-bottom:1px solid var(--rule)}
.cardhead{display:block;width:100%;text-align:left;background:none;border:none;padding:10px 0;cursor:pointer;font:14px -apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink)}
.cardhead .sym{color:var(--red)}
.cardbody{padding:4px 0 16px 18px;border-left:2px solid var(--red);margin:0 0 10px 2px;padding-left:16px}
.vbtn{border:1px solid var(--rule);background:transparent;border-radius:999px;padding:4px 12px;font-family:ui-monospace,monospace;font-size:11px;cursor:pointer;margin-right:6px}
.vbtn[aria-pressed=true]{border-color:var(--red);color:var(--red);background:rgba(155,35,53,.08)}
.tally{font-family:Georgia,serif;font-size:19px;margin:10px 0}
.method p{max-width:760px}
footer{border-top:1px solid var(--rule);padding:12px 36px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;color:var(--muted)}
@media (max-width:900px){.layout{flex-direction:column}.rail{position:static;width:100%;flex:none;border-right:none;border-bottom:1px solid var(--rule);max-height:none}}
```

Hmm .cardbody has duplicate padding-left; fix: `padding:4px 0 16px 16px;`.

Now the JS. Let me write it out fully and carefully.

```js
(function(){
"use strict";
var U = window.WORKSHOP_DATA.uhri;
var RECS = U.records;
var COUNTRY = U.country;
var SDGN = U.sdg_names || {};
var TOTAL = RECS.length;
var PARA_RE = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;

function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}
function extractStates(text){...}
function firstLine(t){...}

RECS.forEach(function(r,i){
  r._i=i;
  var m=(r.text||"").match(PARA_RE);
  r._para=m?m[1]:null;
  r._paraNum=m?parseFloat(m[1]):Infinity;
  r._states=(r.mechanism==="Universal Periodic Review")?extractStates(r.text||""):null;
  r._first=firstLine(r.text||"");
});

var YEARS=[...new Set(RECS.map(r=>r.year))].sort((a,b)=>a-b);
var MECHS=[...new Set(RECS.map(r=>r.mechanism))];
var TYPES=[...new Set(RECS.map(r=>r.type))];
var SDGS=[...new Set(RECS.flatMap(r=>r.sdgs||[]))].sort((a,b)=>a-b);
var ALL_STATES=new Map();
RECS.forEach(r=>{(r._states||[]).forEach(s=>ALL_STATES.set(s,(ALL_STATES.get(s)||0)+1));});

var F={kw:"",mech:"all",body:"all",type:"all",state:"all",theme:"all",yFrom:String(YEARS[0]),yTo:String(YEARS[YEARS.length-1]),sdg:"all"};
var state={filtered:RECS,shown:50,dateAsc:false,seed:1,sample:[],verdicts:{},openCard:null,top10:[],chart1:null,chart2:null};
```

flatMap — fine in modern browsers.

filtered():
```js
function kwWords(){return F.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);}
function filtered(){
  var w=kwWords(), yF=+F.yFrom, yT=+F.yTo;
  return RECS.filter(function(r){
    if(F.mech!=="all"&&r.mechanism!==F.mech)return false;
    if(F.body!=="all"&&r.body!==F.body)return false;
    if(F.type!=="all"&&r.type!==F.type)return false;
    if(F.state!=="all"&&!(r._states||[]).includes(F.state))return false;
    if(F.theme!=="all"&&!(r.themes||[]).includes(F.theme))return false;
    if(F.sdg!=="all"&&!(r.sdgs||[]).includes(+F.sdg))return false;
    if(!(r.year>=yF&&r.year<=yT))return false;
    if(w.length){var hay=(r.text+" "+r.symbol).toLowerCase();for(var i=0;i<w.length;i++)if(hay.indexOf(w[i])<0)return false;}
    return true;
  });
}
```

countBy helper:
```js
function countBy(arr,fn){var m={};arr.forEach(x=>{var k=fn(x);m[k]=(m[k]||0)+1;});return m;}
```

Theme counts:
```js
function themeCounts(arr){var m={};arr.forEach(r=>{(r.themes||[]).forEach(t=>{m[t]=(m[t]||0)+1;});});return m;}
function topThemes(arr,n){var m=themeCounts(arr);return Object.keys(m).map(k=>[k,m[k]]).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,n||10);}
```

Theme year ranges: compute per theme min/max year among filtered records carrying it.

Rendering rail:

```js
function chip(label,clearFn){...}
function renderRail(f){
  el.matchNum.textContent=f.length;
  el.totalNum.textContent=TOTAL;
  el.shareFill.style.width=(TOTAL? (f.length/TOTAL*100):0)+"%";
  // chips
  var chips=[];
  function add(label,key,reset){chips.push('<button class="chip" data-key="'+key+'">'+esc(label)+' <b aria-hidden="true">×</b><span class="sr"></span></button>');}
  ...
}
```
Simpler: build chips array of {label, key} then render with click handler delegation on chips container: data-key → reset that filter.

Chip labels:
- kw: `keyword “${F.kw}”`
- mech: `mechanism: ${F.mech}`
- body, type, state, theme similar
- years if not default: `years: ${yFrom}–${yTo}`
- sdg: `sdg: ${F.sdg} ${name}`

Reset defaults: kw:"", mech/body/type/state/theme:"all", yFrom/yTo defaults, sdg:"all". After reset, re-sync inputs, renderAll.

renderOverview(f):

```js
function renderOverview(f){
  // tiles
  var typeCounts=countBy(RECS,r=>r.type);
  var docs=new Set(RECS.map(r=>r.symbol)).size;
  var tiles='';
  tiles+='<div class="tile"><div class="lbl">All records in the file</div><div class="num">'+TOTAL+'</div><div class="sub">'+Object.keys(typeCounts).map(t=>esc(t)+' '+typeCounts[t]).join(' · ')+'</div><div class="how">How this is computed: records.length of the attached file, before filters; the filtered count is the big number in the rail.</div></div>';
  tiles+='<div class="tile"><div class="lbl">Documents</div><div class="num">'+docs+'</div><div class="sub">distinct symbol values</div><div class="how">Distinct symbol across all records in the file.</div></div>';
  tiles+='<div class="tile"><div class="lbl">Years</div><div class="num">'+YEARS[0]+'–'+YEARS[YEARS.length-1]+'</div><div class="sub">dated by document</div><div class="how">Minimum and maximum of year across all records; date is the document’s date.</div></div>';
  MECHS sorted by count desc in file:
  mechOrder = Object.keys(countBy(RECS,r=>r.mechanism)).sort((a,b)=>countBy... 
```
Compute mechFileCounts once. For each mech: sub = f.filter(m===mech); count, docs distinct symbols, latest year max, share = f.length? count/f.length : 0 (percent 1 decimal). UPR tile adds `<button class="linkbtn" id="statesLink">see the States</button>`.

Tile how: "Records, distinct symbols and latest year among the n filtered records; share = count ÷ n."

States box (hidden by default): top 10 states among filtered UPR records:
```js
function topStates(f,n){var m={};f.forEach(r=>{if(r.mechanism==="Universal Periodic Review")(r._states||[]).forEach(s=>{if(s!=="State not found")m[s]=(m[s]||0)+1;});});return Object.keys(m).map(k=>[k,m[k]]).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,n||10);}
```
Hmm — should "State not found" count? Exclude from top states but the check lists them. OK.

FIG.01:
```js
var tt=topThemes(f,10);
state.top10=tt;
var labels=tt.map(x=>x[0]), data=tt.map(x=>x[1]);
// year ranges
var yr={}; f.forEach(r=>{(r.themes||[]).forEach(t=>{yr[t]=yr[t]||{min:r.year,max:r.year}; if(r.year<yr[t].min)yr[t].min=r.year; if(r.year>yr[t].max)yr[t].max=r.year;});});
```
Update chart or create. If f.length===0 → hide chartwrap, show nomatch div; still render table with "No records match".

Table under chart: rows Theme | Records | % of filtered | Years. % = (count/f.length*100).toFixed(1). Note: "A record can carry several themes, so the bars add up to more than n."

FIG.02: yearsArr = YEARS (file-wide). datasets: for each mech in MECHS (order by file count desc), data = yearsArr.map(y=> f.filter(r=>r.year===y&&r.mechanism===mech).length). Precompute per-year-mech counts once per render.

Chart update: if state.chart1 exists → assign data, update(); else create. Same chart2.

Chart click handler for fig1: onClick set F.theme.

renderRecords(f):

```js
function sorted(f){
  var arr=f.slice();
  arr.sort(function(a,b){
    var d = state.dateAsc ? (a.date<b.date?-1:a.date>b.date?1:0) : (a.date>b.date?-1:a.date>b.date?1:0);
    if(d)return d;
    if(a.body!==b.body)return a.body<b.body?-1:1;
    if(a._paraNum!==b._paraNum)return a._paraNum-b._paraNum;
    return a._i-b._i;
  });
  return arr;
}
```
Wait date strings ISO "2025-07-10" — string compare fine.

Caption: `Showing ${Math.min(state.shown,f.length)} of ${f.length} matching records · ${state.dateAsc?"oldest first":"newest first"}` + (f.length===0 ? " · no records match the current filters" : "").

Rows: for first state.shown of sorted:
```js
var w=kwWords();
rows += '<tr class="rec" tabindex="0" role="button" aria-expanded="false" data-id="'+esc(r.id)+'"><td>'+esc(r.date)+'</td><td>'+esc(r.body)+'</td><td><a class="sym" href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a></td><td class="num">'+esc(r._para||"–")+'</td><td>'+markify(r._first,w)+'</td><td>'+(r._states?esc(r._states.join("; ")):"–")+'</td></tr>';
rows += '<tr class="detail" hidden><td colspan="6" data-detail="'+esc(r.id)+'"></td></tr>';
```
Note: clicking the symbol link inside row would also toggle row — stopPropagation on link clicks: in delegation, if e.target.closest("a")) return.

Show more button: if state.shown < f.length show button "Show 50 more (n remaining)".

Detail builder:
```js
function detailHTML(r){
  var h='<div class="parabig">'+(r._para?("para. "+esc(r._para)):"no paragraph number in this extract")+'</div>';
  h+='<p class="fulltext">'+esc(r.text)+'</p>';
  if(r.section)h+='<div class="lbl2">Section</div><div>'+esc(r.section)+'</div>';
  if(r.themes&&r.themes.length){h+='<div class="lbl2">Themes (UN labels)</div><div class="tagrow">'+r.themes.map(t=>'<span class="tag">'+esc(t)+'</span>').join('')+'</div>';}
  if(r.sdgs&&r.sdgs.length){h+='<div class="lbl2">SDGs</div><div class="tagrow">'+r.sdgs.map(g=>'<span class="tag">'+g+(SDGN[String(g)]?" — "+esc(SDGN[String(g)]):"")+'</span>').join('')+'</div>';}
  if(r.sdg_targets&&r.sdg_targets.length){h+='<div class="lbl2">SDG targets</div><div class="tagrow">'+r.sdg_targets.map(t=>'<span class="tag">'+esc(t)+'</span>').join('')+'</div>';}
  if(r.affected_persons&&r.affected_persons.length){h+='<div class="lbl2">Affected persons</div><div class="tagrow">'+r.affected_persons.map(t=>'<span class="tag">'+esc(t)+'</span>').join('')+'</div>';}
  if(!r.themes||!r.themes.length)h+='<div class="lbl2">Themes</div><div class="hint">not labelled in the data</div>';
  ... similar for sdgs/affected? Keep: show "not labelled" hints for each empty.
  var cite=r.symbol+(r._para?", para. "+r._para:"");
  h+='<div style="margin-top:12px"><button class="btn primary copybtn" data-cite="'+esc(cite)+'">'+(r._para?"Copy citation":"Copy citation (no paragraph number in this extract)")+'</button> <a class="btn" href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">Open the UN document</a> <span class="copied" hidden>Copied ✓</span></div>';
  return h;
}
```

Copy handler (delegation on tbody):
```js
if(e.target.closest(".copybtn")){e.stopPropagation();var b=e.target.closest(".copybtn");copyText(b.dataset.cite,function(ok){var s=b.parentElement.querySelector(".copied");if(s){s.hidden=false;setTimeout(()=>s.hidden=true,2000);}});return;}
```
copyText:
```js
function copyText(t,cb){
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(()=>cb(true),()=>{fallback(t);cb(true);});}
  else{fallback(t);cb(true);}
}
function fallback(t){var ta=document.createElement("textarea");ta.value=t;ta.style.position="fixed";ta.style.opacity="0";document.body.appendChild(ta);ta.select();try{document.execCommand("copy");}catch(e){}ta.remove();}
```

renderCheck(f):

Checks list built as array of {html, cls}. Let me write:

```js
function renderCheck(f){
  var lines=[];
  function line(mark,cls,txt){lines.push('<div class="checkline"><span class="mark '+cls+'">'+mark+'</span><span>'+txt+'</span></div>');}
  var declared=Number(U.count);
  line(declared===TOTAL?"✓ pass":"✗ check failed", declared===TOTAL?"ok":"bad", "Record count: records.length = "+TOTAL+" vs the file’s count field = "+esc(U.count)+" ("+declared+").");
  // partitions
  function partOk(obj){var s=0;for(var k in obj)s+=obj[k];return s===TOTAL;}
  var bm=countBy(RECS,r=>r.mechanism), bb=countBy(RECS,r=>r.body), by=countBy(RECS,r=>r.year), bt=countBy(RECS,r=>r.type);
  line(partOk(bm)?"✓ pass":"✗ check failed", partOk(bm)?"ok":"bad", "Mechanism partition: counts per mechanism sum to "+sum(bm)+" of "+TOTAL+" records.");
  ... body, year, type similarly
  // chart vs table
  var recomputed=topThemes(f,10);
  var same = JSON.stringify(recomputed)===JSON.stringify(state.top10);
  var largest = state.top10.length?state.top10[0][1]:0;
  line(same&&largest<=f.length?"✓ pass":"✗ check failed", ..., "Chart against table: FIG.01 bars recomputed by a second loop equal the ten table rows ("+recomputed.map(x=>x[0]+": "+x[1]).join(", ")+"); largest bar "+largest+" ≤ "+f.length+" filtered records.");
  // links
  var bad=RECS.filter(r=>{var u=r.doc_url||"";if(u.indexOf("https://docs.un.org/")!==0)return true;try{return !decodeURIComponent(u).toLowerCase().endsWith((r.symbol||"").toLowerCase());}catch(e){return true;}});
  line(bad.length?"✗ check failed":"✓ pass", bad.length?"bad":"ok", "Links: "+(RECS.length-bad.length)+" of "+RECS.length+" doc_url values start with https://docs.un.org/ and end with the record’s symbol (case-insensitive, decoded)." + (bad.length? " Failing: "+bad.slice(0,10).map(r=>esc(r.symbol)).join(", ")+(bad.length>10?" and "+(bad.length-10)+" more":"")+".":""));
  // paragraph numbers per mechanism
  MECHS.forEach(m=>{var sub=RECS.filter(r=>r.mechanism===m);var withP=sub.filter(r=>r._para).length;var share=withP/sub.length;var isUPR=m==="Universal Periodic Review";var ok=isUPR?share===1:share>0; // hmm
```
Spec: "Share of records with a number found, per mechanism; UPR is expected at 100%, and a lower figure is shown as a warning, not an error." So for UPR: if share<1 → warning; others just informational pass. I'll render: for each mechanism line: "Paragraph numbers: Treaty bodies 681 of 900 (75.7%)" with mark ✓ pass (informational) and for UPR if <100% "⚠ warning". Let me do: mark = (m==="UPR" && share<1) ? "⚠ warning" : "✓ pass"; cls = warn/ok.

  // states
  var upr=RECS.filter(r=>r.mechanism==="Universal Periodic Review");
  var found=upr.filter(r=>r._states&&r._states.length&&r._states[0]!=="State not found");
  var missing=upr.filter(r=>!(r._states&&r._states.length&&r._states[0]!=="State not found"));
  line(found.length===upr.length?"✓ pass":"⚠ see list", found.length===upr.length?"ok":"warn", "Recommending States: "+found.length+" of "+upr.length+" UPR records have at least one State in the trailing parentheses." + (missing.length? " Without one: "+missing.slice(0,10).map(r=>esc(r.symbol)).join(", ")+(missing.length>10?" and more":"")+".":""));
  
  // duplicates & gaps
  var ids=new Set(RECS.map(r=>r.id)).size;
  var tc=countBy(RECS,r=>r.text); var dupTexts=Object.keys(tc).filter(k=>tc[k]>1); var extra=0; dupTexts.forEach(k=>extra+=tc[k]-1);
  var noThemes=RECS.filter(r=>!(r.themes&&r.themes.length)).length;
  var noSdgs=RECS.filter(r=>!(r.sdgs&&r.sdgs.length)).length;
  var noAff=RECS.filter(r=>!(r.affected_persons&&r.affected_persons.length)).length;
  line(ids===TOTAL?"✓ pass":"✗ check failed", ids===TOTAL?"ok":"bad", "Duplicates and gaps: distinct id values = "+ids+" of "+TOTAL+" records; duplicate text values = "+dupTexts.length+" ("+extra+" extra records); not labelled — themes: "+noThemes+", SDGs: "+noSdgs+", affected persons: "+noAff+".");
  
  el.checks.innerHTML = '<div class="lbl" style="margin-bottom:8px">How the app checks itself</div>' + lines.join("");
```

Then sample section:
```html
<div class="lbl">Random-sample label check</div>
<p class="figsub">This is your judgement of the UN's labels; nothing is sent anywhere.</p>
controls: seed input, Draw again, Draw with this seed, tally
cards container
```

Draw:
```js
function drawSample(){
  var f=state.filtered;
  var seed=state.seed;
  el.seedInput.value=seed;
  if(!f.length){el.cards.innerHTML='<div class="nomatch">No records match the current filters.</div>';el.tally.textContent="";return;}
  var rnd=mulberry32(seed);
  var idx=[];for(var i=0;i<f.length;i++)idx.push(i);
  for(var i=idx.length-1;i>0;i--){var j=Math.floor(rnd()*(i+1));var t=idx[i];idx[i]=idx[j];idx[j]=t;}
  state.sample=idx.slice(0,Math.min(10,f.length)).map(k=>f[k]);
  state.openCard=null;
  renderCards();
}
function renderCards(){
  var w=... no highlight needed here.
  var html='';
  state.sample.forEach(function(r,i){
    var open = state.openCard===i;
    html+='<div class="card"><button class="cardhead" aria-expanded="'+open+'" data-i="'+i+'"><span class="sym">'+esc(r.symbol)+'</span> '+(r._para?("para. "+esc(r._para)):"no para.")+' — '+esc(r._first.slice(0,90))+(r._first.length>90?"…":"")+'</button>';
    if(open){
      html+='<div class="cardbody"><p class="fulltext">'+esc(r.text)+'</p>';
      html+='<div class="lbl2">Themes on this paragraph (UN labels)</div><div class="tagrow">'+(r.themes&&r.themes.length?r.themes.map(t=>'<span class="tag">'+esc(t)+'</span>').join(''):'<span class="hint">not labelled</span>')+'</div>';
      html+='<div style="margin-top:10px">'+["fit","doesn't fit","unsure"].map(...) buttons with data-i and data-v
      html+='</div></div>';
    }
    html+='</div>';
  });
  el.cards.innerHTML=html;
  renderTally();
}
```
Verdict buttons: `<button class="vbtn" data-i="'+i+'" data-v="fit" aria-pressed="'+(state.verdicts[r.id]==="fit")+'">Fits</button>` etc. Labels: "Fits", "Doesn't fit", "Unsure".

Tally:
```js
function renderTally(){
  var v=Object.keys(state.verdicts).filter(k=>state.sample.some(r=>r.id===k)).map(k=>state.verdicts[k]);
  var x=v.filter(a=>a==="fit").length, y=v.filter(a=>a==="no").length, z=v.filter(a=>a==="unsure").length;
  el.tally.textContent = state.sample.length? ("Themes: "+x+" fit, "+y+" don't, "+z+" unsure of "+state.sample.length+" judged · seed "+state.seed+" · drawn from the current filter ("+state.filtered.length+" records)") : "";
}
```
Verdict values: "fit","no","unsure".

Card head click: toggle openCard (one open at a time: openCard = (openCard===i? null : i)); renderCards().

Verdict click: state.verdicts[r.id]=v; renderCards() (to update aria-pressed) — but that re-renders and closes? openCard preserved since state.openCard kept. OK.

mulberry32:
```js
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
```

renderMethod(f): static HTML with dynamic bits (top themes of current filter for summary? summary computed at click). I'll render static method text once, plus source block. Buttons wired once.

CSV/summary use current state.filtered at click time.

describeFilters():
```js
function describeFilters(){
  var parts=[];
  if(F.kw.trim())parts.push('keyword "'+F.kw.trim()+'"');
  if(F.mech!=="all")parts.push("mechanism="+F.mech);
  if(F.body!=="all")parts.push("body="+F.body);
  if(F.type!=="all")parts.push("type="+F.type);
  if(F.state!=="all")parts.push("state="+F.state);
  if(F.theme!=="all")parts.push("theme="+F.theme);
  if(+F.yFrom!==YEARS[0]||+F.yTo!==YEARS[YEARS.length-1])parts.push("years "+F.yFrom+"–"+F.yTo);
  if(F.sdg!=="all")parts.push("sdg "+F.sdg);
  return parts.length?parts.join("; "):"none (all "+TOTAL+" records)";
}
```

Summary text:
```js
function summaryText(){
  var f=state.filtered;
  var tc=countBy(RECS,r=>r.type);
  var tt=topThemes(f,10);
  var lines=[
   "UN human rights recommendations and observations: "+COUNTRY+" — OHCHR Universal Human Rights Index ("+U.source_url+"), built "+U.built+".",
   TOTAL+" records from "+new Set(RECS.map(r=>r.symbol)).size+" documents, "+YEARS[0]+"–"+YEARS[YEARS.length-1]+" (dated by document): "+Object.keys(tc).map(k=>tc[k]+" "+k).join(", ")+".",
   "Current filter: "+describeFilters()+" → "+f.length+" records.",
   "Ten most frequent themes among the "+f.length+" filtered records: "+tt.map((x,i)=>(i+1)+". "+x[0]+" ("+x[1]+")").join("; ")+". A record can carry several themes, so these add up to more than "+f.length+"."
  ];
  return lines.join("\n");
}
```

Filter controls wiring: build selects once, update body options when mech changes.

```js
function fillSelect(sel, opts, current){ sel.innerHTML=opts.map(o=>'<option value="'+esc(o[0])+'"'+(String(o[0])===String(current)?" selected":"")+'>'+esc(o[1])+'</option>').join(""); }
```

Mechanism options: [["all","All mechanisms ("+TOTAL+")"]] + MECHS sorted by count desc with counts.
Body options: [["all","All bodies"]] + bodiesFor(F.mech) with counts.
Type: [["all","All types"]] + TYPES with counts.
State: [["all","All States"]] + [...ALL_STATES] sorted by count desc, label s+" ("+n+")"; include "State not found" if present.
Years: options YEARS.
SDG: [["all","All SDGs"]] + SDGS.map(g=>[String(g), g+" — "+(SDGN[String(g)]||"")+" ("+count+")"]).

Events:
- mechSel change: F.mech=v; if body not valid for mech → F.body="all"; rebuild body select; state.shown=50; renderAll();
- bodySel, typeSel, stateSel, sdgSel change similarly.
- yFrom/yTo change: if +from>+to swap; renderAll.
- kw inputs: debounce.

Accordion: fhead buttons toggle their .fbody hidden + aria-expanded; close others.

setFilter(key,val): F[key]=val; sync UI; state.shown=50; renderAll(). Used by chart click (theme).

renderAll():
```js
function renderAll(){
  var f=filtered();
  state.filtered=f;
  renderRail(f);
  renderOverview(f);
  renderRecords(f);
  renderCheck(f);
}
```

Tab switching:
```js
function selectTab(i){
  state.tab=i;
  tabs.forEach((t,j)=>{t.setAttribute("aria-selected",j===i?"true":"false");t.tabIndex=j===i?0:-1;});
  panels.forEach((p,j)=>p.hidden=j!==i);
  document.body.dataset.tab=i;
  // rail: hide filter blocks on tabs 3,4 (index 2,3)
  el.filterBlocks.hidden = (i>=2);
}
```
Wait spec: filter headings shown on tabs 01 and 02 (index 0,1); on 03/04 rail keeps number/bar/chips. So filterBlocks.hidden = i>=2. But then keyword input in rail hidden on tab 02? No — tab 02 is index 1, shown. Tab 02 has its own search field anyway. OK.

Also chips remain visible on all tabs. Good.

Rail sticky with max-height 100vh overflow auto — fine.

Now overview render details:

```js
function renderOverview(f){
  // tiles
  var typeCounts=countBy(RECS,r=>r.type);
  var docsAll=new Set(RECS.map(r=>r.symbol)).size;
  var mechFile=countBy(RECS,r=>r.mechanism);
  var mechOrder=Object.keys(mechFile).sort((a,b)=>mechFile[b]-mechFile[a]||a.localeCompare(b));
  var html='<div class="tiles">';
  html+='<div class="tile"><div class="lbl">All records in the file</div><div class="num">'+TOTAL+'</div><div class="sub">'+Object.keys(typeCounts).sort((a,b)=>typeCounts[b]-typeCounts[a]).map(t=>esc(t)+": "+typeCounts[t]).join(" · ")+'</div><div class="how">How this is computed: records.length of the attached file, before filters. The filtered count is the big number in the rail.</div></div>';
  html+='<div class="tile"><div class="lbl">Documents</div><div class="num">'+docsAll+'</div><div class="sub">distinct symbol values</div><div class="how">How this is computed: number of distinct symbol values across all records in the file.</div></div>';
  html+='<div class="tile"><div class="lbl">Years</div><div class="num">'+YEARS[0]+'–'+YEARS[YEARS.length-1]+'</div><div class="sub">dated by document</div><div class="how">How this is computed: minimum and maximum of year across all records; date is the document’s date, not the date a recommendation was made.</div></div>';
  mechOrder.forEach(function(m){
    var sub=f.filter(r=>r.mechanism===m);
    var d=new Set(sub.map(r=>r.symbol)).size;
    var latest=sub.length?Math.max.apply(null,sub.map(r=>r.year)):"–";
    var share=f.length?(sub.length/f.length*100).toFixed(1):"0.0";
    html+='<div class="tile"><div class="lbl">'+esc(m)+'</div><div class="num">'+sub.length+'</div><div class="sub">'+d+' documents · latest '+latest+' · '+share+'% of filtered</div><div class="how">How this is computed: records, distinct symbols and latest year among the '+f.length+' filtered records; share = count ÷ '+f.length+'.</div>'+(m==="Universal Periodic Review"?'<div style="margin-top:6px"><button class="linkbtn" id="statesLink">see the States</button></div>':"")+'</div>';
  });
  html+='</div>';
  el.tiles.innerHTML=html;
  var sl=document.getElementById("statesLink");
  if(sl)sl.addEventListener("click",function(){toggleStates(f);});
  renderStatesBox(f);
  renderFig1(f);
  renderFig2(f);
}
```

toggleStates: statesBox hidden toggle; render content:
```js
function renderStatesBox(f){
  var ts=topStates(f,10);
  var h='<div class="lbl" style="margin-bottom:6px">Ten States that made most recommendations to '+esc(COUNTRY)+' (current filter: '+f.length+' records)</div>';
  if(!ts.length)h+='<div class="hint">No recommending States found in the filtered UPR records.</div>';
  else h+='<table><caption>Count of recommendations, not of influence; two States can co-sponsor one line.</caption><thead><tr><th scope="col">State</th><th scope="col" class="num">Recommendations</th></tr></thead><tbody>'+ts.map(x=>'<tr><td>'+esc(x[0])+'</td><td class="num">'+x[1]+'</td></tr>').join('')+'</tbody></table>';
  el.statesBox.innerHTML=h;
}
function toggleStates(f){ el.statesBox.hidden=!el.statesBox.hidden; }
```
Hmm if hidden toggled but content rendered always — fine, render content each renderOverview, toggle visibility separately. But renderOverview re-renders content while hidden state persists. OK.

renderFig1:
```js
function renderFig1(f){
  var tt=topThemes(f,10);
  state.top10=tt;
  var labels=tt.map(x=>x[0]), data=tt.map(x=>x[1]);
  var yr={};f.forEach(r=>{(r.themes||[]).forEach(t=>{if(!yr[t])yr[t]={min:r.year,max:r.year};if(r.year<yr[t].min)yr[t].min=r.year;if(r.year>yr[t].max)yr[t].max=r.year;});});
  // table
  var th='<table><caption>Same ten rows as the bars. A record can carry several themes, so the counts add up to more than '+f.length+'.</caption><thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead><tbody>';
  if(!f.length) th+='<tr><td colspan="4">No records match the current filters.</td></tr>';
  else tt.forEach(x=>{th+='<tr><td>'+esc(x[0])+'</td><td class="num">'+x[1]+'</td><td class="num">'+(f.length?(x[1]/f.length*100).toFixed(1):"0.0")+'</td><td>'+(yr[x[0]]?yr[x[0]].min+"–"+yr[x[0]].max:"–")+'</td></tr>';});
  th+='</tbody></table>';
  el.fig1Table.innerHTML=th;
  // chart
  if(!f.length){el.fig1Wrap.hidden=true;el.fig1Empty.hidden=false;}
  else{
    el.fig1Wrap.hidden=false;el.fig1Empty.hidden=true;
    if(state.chart1){state.chart1.data.labels=labels;state.chart1.data.datasets[0].data=data;state.chart1.update();}
    else{
      state.chart1=new Chart(el.fig1Ctx,{type:"bar",data:{labels:labels,datasets:[{data:data,backgroundColor:"rgba(155,35,53,.8)",borderWidth:0,barThickness:16}]},options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,onClick:function(e,els){if(els&&els.length){var t=state.chart1.data.labels[els[0].index];if(t)setFilter("theme",t);}},plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.parsed.x+" records";}}},scales:{x:{beginAtZero:true,ticks:{precision:0},grid:{color:"#e3dccb"}},y:{grid:{display:false},ticks:{autoSkip:false,font:{size:13}}}}},plugins:[barValuePlugin]});
    }
  }
}
```
Note: if labels empty (f nonempty but no themes) — chart with empty data fine.

barValuePlugin:
```js
var barValuePlugin={id:"barValue",afterDatasetsDraw:function(chart){var meta=chart.getDatasetMeta(0);if(!meta||!meta.data)return;var ctx=chart.ctx;ctx.save();ctx.font="12px ui-monospace, Menlo, Consolas, monospace";ctx.fillStyle="#1d1b18";meta.data.forEach(function(bar,i){var v=chart.data.datasets[0].data[i];if(v==null)return;ctx.fillText(String(v),bar.x+6,bar.y+4);});ctx.restore();}};
```

renderFig2:
```js
var MECH_COLORS={"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
var FALLBACK=["#c2410c","#0f766e","#7c3aed","#a16207","#0e7490","#9d174d"];
function mechColor(m,i){return MECH_COLORS[m]||FALLBACK[i%FALLBACK.length];}
function renderFig2(f){
  var mechFile=countBy(RECS,r=>r.mechanism);
  var mechOrder=Object.keys(mechFile).sort((a,b)=>mechFile[b]-mechFile[a]||a.localeCompare(b));
  var labels=YEARS.map(String);
  var datasets=mechOrder.map(function(m,i){
    var per={};f.forEach(r=>{if(r.mechanism===m)per[r.year]=(per[r.year]||0)+1;});
    return {label:m,data:YEARS.map(y=>per[y]||0),backgroundColor:mechColor(m,i),stack:"s"};
  });
  if(!f.length){el.fig2Wrap.hidden=true;el.fig2Empty.hidden=false;}
  else{
    el.fig2Wrap.hidden=false;el.fig2Empty.hidden=true;
    if(state.chart2){state.chart2.data.labels=labels;state.chart2.data.datasets=datasets;state.chart2.update();}
    else{state.chart2=new Chart(el.fig2Ctx,{type:"bar",data:{labels:labels,datasets:datasets},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:"top",labels:{usePointStyle:true,boxWidth:8,boxHeight:8}}},scales:{x:{stacked:true,grid:{display:false},title:{display:true,text:"year (dated by document)"}},y:{stacked:true,beginAtZero:true,ticks:{precision:0},title:{display:true,text:"records"}}}});}
  }
}
```

renderRecords(f):
```js
function renderRecords(f){
  el.searchTop.value = F.kw; // sync (careful not to disrupt typing — only set if different)
  var arr=sorted(f);
  var shown=Math.min(state.shown,arr.length);
  var w=kwWords();
  var rows="";
  for(var i=0;i<shown;i++){var r=arr[i];
    rows+='<tr class="rec" tabindex="0" role="button" aria-expanded="false" data-id="'+esc(r.id)+'"><td>'+esc(r.date)+'</td><td>'+esc(r.body)+'</td><td><a class="sym" href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a></td><td class="num">'+esc(r._para||"–")+'</td><td>'+markify(r._first,w)+'</td><td>'+(r._states?esc(r._states.join("; ")):"–")+'</td></tr>';
    rows+='<tr class="detail" hidden><td colspan="6" data-detail="'+esc(r.id)+'"></td></tr>';
  }
  el.tbody.innerHTML=rows;
  el.tableCaption.textContent = f.length? ("Showing "+shown+" of "+f.length+" matching records · "+(state.dateAsc?"oldest first":"newest first")+(state.shown<f.length?" · 50 at a time":"")) : "No records match the current filters.";
  el.moreBtn.hidden = !(state.shown<f.length);
  if(state.shown<f.length) el.moreBtn.textContent="Show 50 more ("+(f.length-state.shown)+" remaining)";
}
```
Sync search inputs: set both inputs' values in renderRail or renderAll: `el.kwRail.value=F.kw; el.searchTop.value=F.kw;` — but if user is typing in one, re-render would overwrite... value same as F.kw after debounce, so setting is harmless (same string). During typing before debounce, renderAll isn't called, so fine. But renderAll called from other filter changes would sync — fine.

markify:
```js
function markify(s,words){
  var out=esc(s);
  words.forEach(function(w){
    if(!w)return;
    var ew=esc(w).replace(/[.*+?^${}()|[\]\\]/g,"\\$&");
    out=out.replace(new RegExp(ew,"gi"),function(m){return "<mark>"+m+"</mark>";});
  });
  return out;
}
```

Row toggle:
```js
function toggleRow(tr){
  var id=tr.dataset.id;
  var det=tr.nextElementSibling;
  var open=det.hidden;
  det.hidden=!open;
  tr.setAttribute("aria-expanded",open?"true":"false");
  if(open&&!det.dataset.built){var r=byId[id];det.firstElementChild.innerHTML=detailHTML(r);det.firstElementChild.dataset.built="1";}
}
```
byId map: `var byId={};RECS.forEach(r=>byId[r.id]=r);`

tbody delegation:
```js
el.tbody.addEventListener("click",function(e){
  var cb=e.target.closest(".copybtn");
  if(cb){e.stopPropagation();copyText(cb.dataset.cite,function(){var s=cb.parentElement.querySelector(".copied");if(s){s.hidden=false;setTimeout(function(){s.hidden=true;},2000);}});return;}
  if(e.target.closest("a"))return;
  var tr=e.target.closest("tr.rec");
  if(tr)toggleRow(tr);
});
el.tbody.addEventListener("keydown",function(e){
  if(e.key==="Enter"||e.key===" "){var tr=e.target.closest("tr.rec");if(tr){e.preventDefault();toggleRow(tr);}}
});
```

Sort button: el.sortDate click → state.dateAsc=!state.dateAsc; renderRecords(state.filtered); update label arrow.

More button: state.shown+=50; renderRecords(state.filtered).

Now HTML for panels:

Panel 0:
```html
<section class="panel" role="tabpanel" id="panel-0" aria-labelledby="tab-0">
  <div id="tiles"></div>
  <div class="statesbox" id="statesBox" hidden></div>
  <div class="fig">
    <div class="fighead"><span class="figno">FIG.01</span><span class="figtitle" id="fig1Title">Ten most frequent themes</span></div>
    <div class="figsub" id="fig1Sub"></div>
    <div class="chartwrap" id="fig1Wrap"><canvas id="fig1Ctx"></canvas></div>
    <div class="nomatch" id="fig1Empty" hidden>No records match the current filters.</div>
    <div id="fig1Table"></div>
    <div class="src">Source: attached UHRI file, themes field of the filtered records. Click a bar to filter by that theme.</div>
  </div>
  <div class="fig">
    <div class="fighead"><span class="figno">FIG.02</span><span class="figtitle">Records per year by mechanism</span></div>
    <div class="figsub" id="fig2Sub"></div>
    <div class="chartwrap tall" id="fig2Wrap"><canvas id="fig2Ctx"></canvas></div>
    <div class="nomatch" id="fig2Empty" hidden>No records match the current filters.</div>
    <div class="src">Source: attached UHRI file, year and mechanism of the filtered records; every year from first to last appears, so empty years are gaps.</div>
  </div>
</section>
```
fig1Sub: "among n filtered records · click a bar = filter". fig2Sub: "n filtered records, stacked by mechanism".

Panel 1:
```html
<section class="panel" role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden>
  <input type="text" id="searchTop" placeholder="Search the filtered records, e.g. torture" aria-label="Search records">
  <div class="hint" style="margin:6px 0 14px">literal match, not synonyms · every word must appear in the text or the symbol · same box as 01 KEYWORD in the rail</div>
  <table id="recTable">
    <caption id="tableCaption"></caption>
    <thead><tr>
      <th scope="col"><button class="sortbtn" id="sortDate">Date</button></th>
      <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">First line</th><th scope="col">Recommending State</th>
    </tr></thead>
    <tbody id="tbody"></tbody>
  </table>
  <button class="btn" id="moreBtn">Show 50 more</button>
</section>
```
Sort button label with arrow: "Date ↓"/"Date ↑" — update text.

Panel 2:
```html
<section class="panel" role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  <div class="lbl" style="margin-bottom:4px">How the app checks itself</div>
  <div id="checks"></div>
  <div class="fig">
    <div class="fighead"><span class="figno">SAMPLE</span><span class="figtitle">Check 10 labels at random</span></div>
    <p class="figsub">This is your judgement of the UN's labels; nothing is sent anywhere. Draw is seeded, so a colleague with the same seed and filter draws the same ten.</p>
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:10px 0">
      <label class="lbl" for="seedInput">seed</label>
      <input type="number" id="seedInput" value="1" style="width:90px">
      <button class="btn" id="drawAgain">Draw again</button>
      <button class="btn" id="drawSeed">Draw with this seed</button>
    </div>
    <div class="tally" id="tally"></div>
    <div id="cards"></div>
  </div>
</section>
```

Panel 3:
```html
<section class="panel" role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>
  <div class="method">
    <div class="lbl">Method</div>
    <p>…5-6 sentences…</p>
    <div class="lbl">Export</div>
    <p><button class="btn primary" id="csvBtn">Download CSV of the current filter</button> <button class="btn" id="sumBtn">Copy summary</button> <span id="sumOk" class="hint" hidden>Copied ✓</span></p>
    <p class="hint" id="exportNote"></p>
    <div class="lbl">Source</div>
    <p id="sourceBlock"></p>
  </div>
</section>
```

Rail HTML:
```html
<aside class="rail">
  <div class="railhead"><span class="lbl">Filters</span><button class="linkbtn" id="clearAll">Clear all</button></div>
  <div class="bignum" id="matchNum" aria-live="polite">0</div>
  <div class="ofline">matching records · of <span id="totalNum"></span> in the file</div>
  <div class="sharebar"><div class="sharefill" id="shareFill"></div></div>
  <div class="chips" id="chips"></div>
  <div id="filterBlocks">
    <div class="fblock">
      <button class="fhead" aria-expanded="false" data-block="b1"><span>01 Keyword</span><span class="arr">+</span></button>
      <div class="fbody" id="b1" hidden>
        <input type="text" id="kwRail" placeholder="e.g. torture" aria-label="Keyword">
        <div class="hint">literal match, not synonyms · every word must occur in the text or symbol · applied 300 ms after typing</div>
      </div>
    </div>
    <div class="fblock">
      <button class="fhead" aria-expanded="false" data-block="b2"><span>02 Mechanism, body, type</span><span class="arr">+</span></button>
      <div class="fbody" id="b2" hidden>
        <label class="flabel" for="mechSel">Mechanism</label><select id="mechSel"></select>
        <label class="flabel" for="bodySel">Body or mandate</label><select id="bodySel"></select>
        <label class="flabel" for="typeSel">Type</label><select id="typeSel"></select>
        <label class="flabel" for="stateSel">Recommending State (UPR)</label><select id="stateSel"></select>
      </div>
    </div>
    <div class="fblock">
      <button class="fhead" aria-expanded="false" data-block="b3"><span>03 Years and SDG</span><span class="arr">+</span></button>
      <div class="fbody" id="b3" hidden>
        <label class="flabel" for="yFrom">Year from</label><select id="yFrom"></select>
        <label class="flabel" for="yTo">Year to</label><select id="yTo"></select>
        <label class="flabel" for="sdgSel">SDG</label><select id="sdgSel"></select>
      </div>
    </div>
  </div>
</aside>
```

Chips render:
```js
function renderChips(){
  var c=[];
  function add(label,key){c.push({label:label,key:key});}
  if(F.kw.trim())add('keyword “'+F.kw.trim()+'”',"kw");
  if(F.mech!=="all")add("mechanism: "+F.mech,"mech");
  if(F.body!=="all")add("body: "+F.body,"body");
  if(F.type!=="all")add("type: "+F.type,"type");
  if(F.state!=="all")add("state: "+F.state,"state");
  if(F.theme!=="all")add("theme: "+F.theme,"theme");
  if(+F.yFrom!==YEARS[0]||+F.yTo!==YEARS[YEARS.length-1])add("years: "+F.yFrom+"–"+F.yTo,"years");
  if(F.sdg!=="all")add("sdg: "+F.sdg+(SDGN[F.sdg]?" — "+SDGN[F.sdg]:""),"sdg");
  el.chips.innerHTML=c.map(x=>'<button class="chip" data-key="'+x.key+'" aria-label="Remove filter '+esc(x.label)+'">'+esc(x.label)+' <b aria-hidden="true">×</b></button>').join("");
}
el.chips.addEventListener("click",function(e){
  var b=e.target.closest(".chip");if(!b)return;
  var k=b.dataset.key;
  if(k==="kw")F.kw="";
  else if(k==="years"){F.yFrom=String(YEARS[0]);F.yTo=String(YEARS[YEARS.length-1]);}
  else F[k]="all";
  state.shown=50;
  syncInputs();
  renderAll();
});
```

syncInputs(): set all select/input values from F.

clearAll: reset all F to defaults, shown=50, syncInputs, renderAll.

setFilter(key,val): F[key]=val; if key==="theme" nothing else; state.shown=50; syncInputs(); renderAll();

syncInputs:
```js
function syncInputs(){
  el.kwRail.value=F.kw; el.searchTop.value=F.kw;
  el.mechSel.value=F.mech; fillBody(); el.bodySel.value=F.body;
  el.typeSel.value=F.type; el.stateSel.value=F.state;
  el.yFrom.value=F.yFrom; el.yTo.value=F.yTo; el.sdgSel.value=F.sdg;
}
```
fillBody(): rebuild bodySel options from bodiesFor(F.mech); if F.body not among them, F.body="all".

Init selects:
```js
function initFilters(){
  fillSelect(el.mechSel, [["all","All mechanisms ("+TOTAL+")"]].concat(mechOrder().map(m=>[m,m+" ("+mechFile[m]+")"])), F.mech);
  fillBody();
  fillSelect(el.typeSel, [["all","All types ("+TOTAL+")"]].concat(TYPES.map(t=>[t,t+" ("+countBy(RECS,r=>r.type)[t]+")"])), F.type);
  var stOpts=[["all","All States"]].concat([...ALL_STATES.entries()].sort((a,b)=>b[1]-a[1]).map(e=>[e[0],e[0]+" ("+e[1]+")"]));
  fillSelect(el.stateSel, stOpts, F.state);
  fillSelect(el.yFrom, YEARS.map(y=>[String(y),String(y)]), F.yFrom);
  fillSelect(el.yTo, YEARS.map(y=>[String(y),String(y)]), F.yTo);
  var sdgCounts=countBy(RECS,r=>r.sdgs||[]); // hmm countBy with array fn won't work
```
sdg counts: build map: RECS.forEach(r=>(r.sdgs||[]).forEach(g=>m[g]=(m[g]||0)+1)).
```js
  fillSelect(el.sdgSel, [["all","All SDGs"]].concat(SDGS.map(g=>[String(g),g+(SDGN[String(g)]?" — "+SDGN[String(g)]:"")+" ("+sdgMap[g]+")"])), F.sdg);
}
```

Events for selects: change → update F, maybe fillBody, shown=50, renderAll.

Year swap: on yFrom change: F.yFrom=v; if(+F.yFrom>+F.yTo){F.yTo=F.yFrom;} sync; renderAll. Similarly yTo: if(+F.yTo<+F.yFrom)F.yFrom=F.yTo.

Keyword debounce:
```js
var kwTimer=null;
function onKw(v){clearTimeout(kwTimer);kwTimer=setTimeout(function(){F.kw=v;state.shown=50;renderAll();},300);}
el.kwRail.addEventListener("input",e=>{onKw(e.target.value);el.searchTop.value=e.target.value;});
el.searchTop.addEventListener("input",e=>{onKw(e.target.value);el.kwRail.value=e.target.value;});
```
But renderAll→renderRecords sets el.searchTop.value=F.kw — same value, ok. And renderRail doesn't touch kw inputs. But syncInputs sets both — called on chip clear etc. Fine.

Accordion:
```js
document.querySelectorAll(".fhead").forEach(function(b){
  b.addEventListener("click",function(){
    var body=document.getElementById(b.dataset.block);
    var open=body.hidden;
    document.querySelectorAll(".fbody").forEach(function(x){x.hidden=true;});
    document.querySelectorAll(".fhead").forEach(function(x){x.setAttribute("aria-expanded","false");x.querySelector(".arr").textContent="+";});
    if(open){body.hidden=false;b.setAttribute("aria-expanded","true");b.querySelector(".arr").textContent="–";}
  });
});
```

Tabs init: selectTab(0). Tab click handlers.

Header/footer fill:
```js
document.getElementById("countryLabel").textContent=COUNTRY;
document.title="UHRI · "+COUNTRY+" — UN recommendations dashboard";
el.kicker... 
el.h1.textContent="UN human rights recommendations and observations: "+COUNTRY;
el.metaLine.innerHTML='Source: <a href="'+esc(U.source_url)+'" target="_blank" rel="noopener">'+esc(U.source)+'</a> · '+TOTAL+' records · '+docsAll+' documents · '+YEARS[0]+'–'+YEARS[YEARS.length-1]+' · built '+esc(U.built)+' · dated by document';
footer.innerHTML='Built on OHCHR UHRI data · '+TOTAL+' records · <a href="'+esc(U.source_url)+'" target="_blank" rel="noopener">'+esc(U.source)+'</a>';
```

Method tab content (static, with dynamic export note):
```js
el.methodText.innerHTML = "<p>1. Every number on this page is computed in your browser by looping over the records in the attached file; nothing is estimated and no model is called.</p>..." 
```
Write as plain paragraphs.

Source block: `Data: <a href=...>U.source</a> · built U.built · records TOTAL · count field "U.count". The Universal Human Rights Index is published by OHCHR; see the source page for its terms of use.`

CSV button handler as above. Summary button: copyText(summaryText(), show sumOk 2s).

exportNote: "The CSV is generated in the browser as a Blob; the only thing that can leave this page is the clipboard write when you press a Copy button."

Now, one concern: renderCheck is called in renderAll on every keystroke — it loops RECS a few times (2264) — fine.

Also note the check "Chart against table" uses state.top10 which is set in renderFig1 — renderOverview runs before renderCheck in renderAll, good.

Edge: YEARS could be empty if no records — guard: if TOTAL===0 show message. I'll add a guard at top: if(!RECS.length){document.body.innerHTML=...}. Keep simple: assume records exist but guard YEARS[0] undefined → use "–". I'll add minimal guards.

Also `U.count` may be string; Number() fine.

Let me also double check the state regex against sample: "109.243 Strengthen support ... (Gambia)." → trailing run matches " (Gambia)" then "." → groups ["(Gambia)"] → "Gambia". Good. "(Venezuela (Bolivarian Republic of))" → outer group with nested → inner "Venezuela (Bolivarian Republic of)" no comma, len<60 → accepted. "(Cabo Verde) (Slovenia) (Togo);" → run matches all three + ";" → three states. Treaty-body "(art. 15)." — not UPR so skipped. Good.

Para regex on "109.243 Strengthen..." → matches "109.243" then space. On "71. The Committee" → "71". On "(g) Develop..." → no match (starts with "("). Good.

Now the "How this is computed" for FIG titles: fig1Sub = "among "+f.length+" filtered records · click a bar = filter by that theme". fig2Sub = f.length+" filtered records, stacked by mechanism · years with no records appear as gaps".

Also spec: figure titles say what is counted and for which filter — fig1Title: "Ten most frequent themes among n filtered records" — make dynamic: `Ten most frequent themes · ${f.length} filtered records`. I'll set fig1Title.textContent dynamically.

Now write everything into final HTML. Also add `<meta name="color-scheme" content="light">`? Not needed.

One more: tabs need id/aria-controls wiring; panels labelledby.

Tab buttons:
```html
<div class="tablist" role="tablist" aria-label="Sections">
  <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 Overview</button>
  <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" tabindex="-1">02 Records</button>
  <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">03 Check</button>
  <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
</div>
```
Text-transform uppercase handles caps.

Let me now also make sure "no view shows more than about seven things to click" — tab 02: 4 tabs + 3 fheads + clear all + sort button + show more = 10... hmm. "not counting table rows". Sort button and show-more are buttons. 4+3+1+1+1=10. That's over. But the spec itself demands all these elements; "about seven" is approximate and the spec's own inventory exceeds it. I'll not stress; the spec is authoritative.

Actually, maybe I can reduce: put "Clear all" only when chips exist? It's required in rail head. Keep as is — follow the detailed spec.

Now, writing the final code. I need to be careful with the size — let me write efficiently but completely. Also remember: before code block, at most three short sentences; after, nothing.

Let me write the complete file now.

Also: `el` helper: `function $(id){return document.getElementById(id);}` and collect elements.

Potential pitfall: In renderRecords I set el.searchTop.value=F.kw each render — if user typed in searchTop and debounce pending, no render happens, fine.

Another: markify with words containing regex chars — escaped. esc(w) then regex-escape — but esc turns `"` into `&quot;` — fine.

Detail colspan=6 matches 6 columns. Good.

CSV: include comment lines starting with "#". Good.

Let me also compute docsAll once globally.

For the check "Partitions ... per year each sum to the record count" — countBy year sums to TOTAL trivially; still show.

Write method sentences (6):
1. Every number on this page is computed in your browser by looping over the records of the attached file; nothing is estimated, and no model or network request is involved.
2. The headline total is records.length; documents are the distinct symbol values; years are the minimum and maximum of the year field, which is the document's date.
3. Filters combine with AND: mechanism, body, type, theme and recommending State are exact matches on the record's fields; the year range is inclusive; the SDG filter keeps records whose sdgs list contains the chosen goal; the keyword filter keeps records in which every typed word occurs in the text or the symbol (literal, case-insensitive — "torture" does not find "ill-treatment").
4. Theme counts count each theme once per record that carries it, so they add up to more than the record count; percentages are shares of filtered records.
5. Paragraph numbers are read from the start of each text with a regular expression; recommending States are read from the parentheses at the end of UPR texts only, and a group with a comma or over 60 characters is recorded as "State not found".
6. The CSV export is generated in the browser as a Blob with comment lines naming the country, source, build date, filters and row count; the only thing that can leave this page is the clipboard write when you press a Copy button.

Good.

Now assemble. I'll write the code now in final form, keeping an eye on correctness.

One more detail: `role="button"` on tr with tabindex — screen readers okay-ish. Fine.

For the tab panels: when hidden attribute set, CSS `[hidden]{display:none!important}` handles.

Chart canvas inside hidden wrap: creating Chart while hidden (display:none) can give zero size; but we create charts only when f.length>0 and wrap visible. On tab switch, panel hidden but chart already created — Chart.js handles resize via responsive when visible again? When display:none, canvas has 0 size; on show, Chart.js responsive observer should resize. To be safe, call chart.resize() on tab select. I'll add: in selectTab, if charts exist, setTimeout(()=>{chart.resize()},0). Actually Chart.js uses ResizeObserver on parent; when display goes from none to block, observer fires. Should be fine; add resize call anyway.

Initial render: selectTab(0) then renderAll(). Charts created on first renderAll while panel 0 visible. Good.

Also note: renderAll calls renderCheck which needs state.top10 — set in renderOverview before. Order in renderAll: rail, overview, records, check. Good.

Let me finalize the states check line: "the records without one are listed with their symbol, so the reader can see what the parentheses held instead" — include a snippet of the trailing text? I'll include symbol + last 40 chars of text. Let me add: missing.slice(0,8).map(r=>esc(r.symbol)+" …"+esc((r.text||"").slice(-40))).join("; "). Cap at 8 with "and n more".

Now write it all. Also ensure no `fetch` etc. Only Chart global.

Counting lines — probably ~950 lines. OK.

Let me write the final answer: 2-3 sentences before the code block, then the html block, nothing after.

Writing the code now carefully:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UHRI dashboard</title>
<style>
...
</style>
</head>
<body>
<header>
  <div class="kicker" id="kicker"></div>
  <h1 id="h1"></h1>
  <p class="meta" id="metaLine"></p>
</header>
<div class="layout">
  <aside class="rail" aria-label="Filters">
    ...
  </aside>
  <main>
    <div class="tablist" role="tablist" id="tablist" aria-label="Sections">…</div>
    <section class="panel" role="tabpanel" id="panel-0" aria-labelledby="tab-0">…</section>
    ...
  </main>
</div>
<footer id="footer"></footer>
<script>
...
</script>
</body>
</html>
```

JS full draft:

```js
(function(){
"use strict";
var U=window.WORKSHOP_DATA.uhri;
var RECS=U.records||[];
var COUNTRY=U.country||"the country";
var SDGN=U.sdg_names||{};
var TOTAL=RECS.length;
var PARA_RE=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
function $(id){return document.getElementById(id);}
function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}
function extractStates(text){
  var m=text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
  if(!m)return [];
  var groups=m[1].match(/\((?:[^()]|\([^()]*\))*\)/g)||[];
  var out=[];
  for(var i=0;i<groups.length;i++){
    var inner=groups[i].slice(1,-1).trim();
    if(inner.indexOf(",")>=0||inner.length>60)return ["State not found"];
    out.push(inner);
  }
  return out;
}
function firstLine(t){
  if(t.length<=120)return t;
  var cut=t.slice(0,120),sp=cut.lastIndexOf(" ");
  return (sp>0?cut.slice(0,sp):cut)+"…";
}
var byId={};
RECS.forEach(function(r,i){
  r._i=i;byId[r.id]=r;
  var m=(r.text||"").match(PARA_RE);
  r._para=m?m[1]:null;
  r._paraNum=m?parseFloat(m[1]):Infinity;
  r._states=(r.mechanism==="Universal Periodic Review")?extractStates(r.text||""):null;
  r._first=firstLine(r.text||"");
});
var YEARS=RECS.map(r=>r.year).filter(y=>typeof y==="number");
YEARS=Array.from(new Set(YEARS)).sort((a,b)=>a-b);
var YMIN=YEARS.length?YEARS[0]:null, YMAX=YEARS.length?YEARS[YEARS.length-1]:null;
var MECHS=Array.from(new Set(RECS.map(r=>r.mechanism)));
var TYPES=Array.from(new Set(RECS.map(r=>r.type)));
var SDGS=Array.from(new Set(RECS.reduce((a,r)=>a.concat(r.sdgs||[]),[]))).sort((a,b)=>a-b);
var ALL_STATES=new Map();
RECS.forEach(r=>{(r._states||[]).forEach(s=>ALL_STATES.set(s,(ALL_STATES.get(s)||0)+1));});
function countBy(arr,fn){var m={};arr.forEach(x=>{var k=fn(x);m[k]=(m[k]||0)+1;});return m;}
function sum(o){var s=0;for(var k in o)s+=o[k];return s;}
function themeCounts(arr){var m={};arr.forEach(r=>{(r.themes||[]).forEach(t=>{m[t]=(m[t]||0)+1;});});return m;}
function topThemes(arr,n){var m=themeCounts(arr);return Object.keys(m).map(k=>[k,m[k]]).sort((a,b)=>b[1]-a[1]||(a[0]<b[0]?-1:a[0]>b[0]?1:0)).slice(0,n||10);}
function topStates(arr,n){var m={};arr.forEach(r=>{if(r.mechanism==="Universal Periodic Review")(r._states||[]).forEach(s=>{if(s!=="State not found")m[s]=(m[s]||0)+1;});});return Object.keys(m).map(k=>[k,m[k]]).sort((a,b)=>b[1]-a[1]||(a[0]<b[0]?-1:1)).slice(0,n||10);}
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}

var F={kw:"",mech:"all",body:"all",type:"all",state:"all",theme:"all",yFrom:String(YMIN),yTo:String(YMAX),sdg:"all"};
var state={filtered:RECS.slice(),shown:50,dateAsc:false,seed:1,sample:[],verdicts:{},openCard:null,top10:[],chart1:null,chart2:null,tab:0};

function kwWords(){return F.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);}
function filtered(){
  var w=kwWords(),yF=+F.yFrom,yT=+F.yTo;
  return RECS.filter(function(r){
    if(F.mech!=="all"&&r.mechanism!==F.mech)return false;
    if(F.body!=="all"&&r.body!==F.body)return false;
    if(F.type!=="all"&&r.type!==F.type)return false;
    if(F.state!=="all"&&(r._states||[]).indexOf(F.state)<0)return false;
    if(F.theme!=="all"&&(r.themes||[]).indexOf(F.theme)<0)return false;
    if(F.sdg!=="all"&&(r.sdgs||[]).indexOf(+F.sdg)<0)return false;
    if(!(r.year>=yF&&r.year<=yT))return false;
    if(w.length){var hay=(r.text+" "+r.symbol).toLowerCase();for(var i=0;i<w.length;i++)if(hay.indexOf(w[i])<0)return false;}
    return true;
  });
}
function bodiesFor(mech){var m={};RECS.forEach(r=>{if(mech==="all"||r.mechanism===mech)m[r.body]=(m[r.body]||0)+1;});return Object.keys(m).map(k=>[k,m[k]]).sort((a,b)=>b[1]-a[1]||(a[0]<b[0]?-1:1));}
```

Elements collection:
```js
var el={};
["kicker","h1","metaLine","matchNum","totalNum","shareFill","chips","filterBlocks","kwRail","mechSel","bodySel","typeSel","stateSel","yFrom","yTo","sdgSel","clearAll","tiles","statesBox","fig1Title","fig1Sub","fig1Wrap","fig1Ctx","fig1Empty","fig1Table","fig2Sub","fig2Wrap","fig2Ctx","fig2Empty","searchTop","tableCaption","tbody","sortDate","moreBtn","checks","seedInput","drawAgain","drawSeed","tally","cards","csvBtn","sumBtn","sumOk","exportNote","sourceBlock","footer","tablist"].forEach(id=>el[id]=$(id));
var panels=[0,1,2,3].map(i=>el["panel-"+i]... 
```
Hmm panels: `$("panel-0")` etc. Add to list: "panel-0","panel-1","panel-2","panel-3". And tabs: query.

OK, writing final. Also `fillSelect`:
```js
function fillSelect(sel,opts,current){
  sel.innerHTML=opts.map(o=>'<option value="'+esc(o[0])+'"'+(String(o[0])===String(current)?" selected":"")+'>'+esc(o[1])+'</option>').join("");
}
```

initFilters + events as planned.

renderRail:
```js
function renderRail(f){
  el.matchNum.textContent=f.length;
  el.totalNum.textContent=TOTAL;
  el.shareFill.style.width=(TOTAL?Math.max(0,f.length/TOTAL*100):0)+"%";
  renderChips();
}
```

renderChips as planned.

renderOverview, renderFig1, renderFig2, renderStatesBox as planned.

renderRecords, detailHTML, toggleRow, markify as planned.

renderCheck as planned.

drawSample/renderCards/renderTally as planned.

renderMethod: static innerHTML set once in init; exportNote dynamic: "Current filter: X → n records." update in renderAll? I'll update in renderAll: el.exportNote.textContent = "Current filter: "+describeFilters()+" → "+state.filtered.length+" of "+TOTAL+" records.";

CSV & summary handlers.

selectTab + tab events + keydown.

Init:
```js
function init(){
  // header
  el.kicker.textContent="UHRI · "+COUNTRY;
  document.title="UHRI · "+COUNTRY+" — UN recommendations dashboard";
  el.h1.textContent="UN human rights recommendations and observations: "+COUNTRY;
  var docsAll=new Set(RECS.map(r=>r.symbol)).size;
  el.metaLine.innerHTML='Source: <a href="'+esc(U.source_url)+'" target="_blank" rel="noopener">'+esc(U.source)+'</a> · '+TOTAL+' records · '+docsAll+' documents · '+(YMIN!=null?YMIN+"–"+YMAX:"–")+' · built '+esc(U.built)+' · dated by document';
  el.footer.innerHTML='Built on OHCHR UHRI data · '+TOTAL+' records · <a href="'+esc(U.source_url)+'" target="_blank" rel="noopener">'+esc(U.source)+'</a>';
  initFilters();
  wire events...
  selectTab(0);
  renderAll();
}
init();
```

Careful: `el.footer` — footer id="footer".

Method text set in init.

Now, potential issue: renderRecords sets el.searchTop.value=F.kw — but searchTop input event sets F.kw after debounce; while typing, renderAll not triggered, so no clobber. But chip clear triggers renderAll → sets both inputs to "" — correct.

Another: when tab 03/04 active, filterBlocks hidden — but keyword input inside hidden block; tab 02 has its own. Fine.

Chart resize on tab select:
```js
function selectTab(i){
  state.tab=i;
  var tabs=tabButtons;
  tabs.forEach(function(t,j){var on=j===i;t.setAttribute("aria-selected",on?"true":"false");t.tabIndex=on?0:-1;});
  panels.forEach(function(p,j){p.hidden=j!==i;});
  el.filterBlocks.hidden=(i>=2);
  if(state.chart1)state.chart1.resize();
  if(state.chart2)state.chart2.resize();
}
```

Tab buttons array: `var tabButtons=Array.prototype.slice.call(el.tablist.querySelectorAll("[role=tab]"));`

Click: tabButtons.forEach((t,i)=>t.addEventListener("click",()=>selectTab(i)));

Keydown on tablist as planned.

Now detailHTML — include "not labelled" hints for empty themes/sdgs/affected_persons:
```js
function detailHTML(r){
  var h='<div class="parabig">'+(r._para?esc("para. "+r._para):"no paragraph number in this extract")+'</div>';
  h+='<p class="fulltext">'+esc(r.text)+'</p>';
  if(r.section)h+='<div class="lbl2">Section</div><div class="tagrow"><span class="tag">'+esc(r.section)+'</span></div>';
  h+='<div class="lbl2">Themes (UN labels)</div><div class="tagrow">'+(r.themes&&r.themes.length?r.themes.map(t=>'<span class="tag">'+esc(t)+'</span>').join(''):'<span class="hint">not labelled in the data</span>')+'</div>';
  h+='<div class="lbl2">SDGs</div><div class="tagrow">'+(r.sdgs&&r.sdgs.length?r.sdgs.map(g=>'<span class="tag">'+esc(g+(SDGN[String(g)]?" — "+SDGN[String(g)]:""))+'</span>').join(''):'<span class="hint">not labelled in the data</span>')+'</div>';
  if(r.sdg_targets&&r.sdg_targets.length)h+='<div class="lbl2">SDG targets</div><div class="tagrow">'+r.sdg_targets.map(t=>'<span class="tag">'+esc(t)+'</span>').join('')+'</div>';
  h+='<div class="lbl2">Affected persons</div><div class="tagrow">'+(r.affected_persons&&r.affected_persons.length?r.affected_persons.map(t=>'<span class="tag">'+esc(t)+'</span>').join(''):'<span class="hint">not labelled in the data</span>')+'</div>';
  var cite=r.symbol+(r._para?", para. "+r._para:"");
  h+='<div style="margin-top:14px"><button class="btn primary copybtn" data-cite="'+esc(cite)+'">'+(r._para?"Copy citation":"Copy citation (no paragraph number in this extract)")+'</button><a class="btn" href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">Open the UN document</a><span class="hint copied" hidden> Copied ✓</span></div>';
  return h;
}
```

Note: data-cite with quotes — esc handles `"` → `&quot;` in attribute. Good.

renderCheck full:

```js
function renderCheck(f){
  var lines=[];
  function line(mark,cls,txt){lines.push('<div class="checkline"><span class="mark '+cls+'">'+mark+'</span><span>'+txt+'</span></div>');}
  var declared=Number(U.count);
  line(declared===TOTAL?"✓ pass":"✗ check failed",declared===TOTAL?"ok":"bad","Record count: records.length = "+TOTAL+" vs the file’s count field = "+esc(U.count)+" ("+declared+").");
  var bm=countBy(RECS,r=>r.mechanism),bb=countBy(RECS,r=>r.body),by=countBy(RECS,r=>r.year),bt=countBy(RECS,r=>r.type);
  line(sum(bm)===TOTAL?"✓ pass":"✗ check failed",sum(bm)===TOTAL?"ok":"bad","Mechanism partition: counts per mechanism sum to "+sum(bm)+" of "+TOTAL+" records.");
  line(sum(bb)===TOTAL?"✓ pass":"✗ check failed",sum(bb)===TOTAL?"ok":"bad","Body partition: counts per body sum to "+sum(bb)+" of "+TOTAL+" records.");
  line(sum(by)===TOTAL?"✓ pass":"✗ check failed",sum(by)===TOTAL?"ok":"bad","Year partition: counts per year sum to "+sum(by)+" of "+TOTAL+" records.");
  line(sum(bt)===TOTAL?"✓ pass":"✗ check failed",sum(bt)===TOTAL?"ok":"bad","Type partition: counts per type sum to "+sum(bt)+" of "+TOTAL+" records.");
  var rec=topThemes(f,10);
  var same=JSON.stringify(rec)===JSON.stringify(state.top10);
  var largest=state.top10.length?state.top10[0][1]:0;
  line((same&&largest<=f.length)?"✓ pass":"✗ check failed",(same&&largest<=f.length)?"ok":"bad","Chart against table: FIG.01 bars recomputed by a second loop over the "+f.length+" filtered records give "+(rec.length?rec.map(x=>esc(x[0])+" "+x[1]).join(", "):"nothing")+"; largest bar "+largest+" ≤ "+f.length+".");
  var badLinks=RECS.filter(function(r){var u=r.doc_url||"";if(u.indexOf("https://docs.un.org/")!==0)return true;try{return decodeURIComponent(u).toLowerCase().indexOf((r.symbol||"").toLowerCase())!==decodeURIComponent(u).toLowerCase().length-(r.symbol||"").length;}catch(e){return true;}});
```
Hmm simpler: `!decodeURIComponent(u).toLowerCase().endsWith((r.symbol||"").toLowerCase())`. endsWith fine.
```js
  line(badLinks.length?"✗ check failed":"✓ pass",badLinks.length?"bad":"ok","Links: "+(RECS.length-badLinks.length)+" of "+RECS.length+" doc_url values start with https://docs.un.org/ and end with the record’s symbol (case-insensitive, decoded)." + (badLinks.length?" Failing: "+badLinks.slice(0,10).map(r=>esc(r.symbol)).join(", ")+(badLinks.length>10?" and "+(badLinks.length-10)+" more":"")+".":""));
  MECHS.forEach(function(m){
    var sub=RECS.filter(r=>r.mechanism===m);
    var wp=sub.filter(r=>r._para).length;
    var share=sub.length?wp/sub.length:0;
    var isUPR=m==="Universal Periodic Review";
    var warn=isUPR&&share<1;
    line(warn?"⚠ warning":"✓ pass",warn?"warn":"ok","Paragraph numbers: "+esc(m)+" "+wp+" of "+sub.length+" records ("+(share*100).toFixed(1)+"%) have a number at the start of the text"+(isUPR?(share===1?"; UPR expected at 100%.":"; UPR expected at 100% — lower is a warning, not an error."):"")+".");
  });
  var upr=RECS.filter(r=>r.mechanism==="Universal Periodic Review");
  var found=upr.filter(r=>r._states&&r._states.length&&r._states[0]!=="State not found");
  var missing=upr.filter(r=>!(r._states&&r._states.length&&r._states[0]!=="State not found"));
  line(found.length===upr.length?"✓ pass":"⚠ see list",found.length===upr.length?"ok":"warn","Recommending States: "+found.length+" of "+upr.length+" UPR records have at least one State in the trailing parentheses."+(missing.length?" Without one: "+missing.slice(0,8).map(r=>esc(r.symbol)+" …"+esc((r.text||"").slice(-45))).join("; ")+(missing.length>8?" and "+(missing.length-8)+" more":"")+".":""));
  var ids=new Set(RECS.map(r=>r.id)).size;
  var tc=countBy(RECS,r=>r.text);
  var dup=Object.keys(tc).filter(k=>tc[k]>1);
  var extra=0;dup.forEach(k=>extra+=tc[k]-1);
  var noT=RECS.filter(r=>!(r.themes&&r.themes.length)).length;
  var noS=RECS.filter(r=>!(r.sdgs&&r.sdgs.length)).length;
  var noA=RECS.filter(r=>!(r.affected_persons&&r.affected_persons.length)).length;
  line(ids===TOTAL?"✓ pass":"✗ check failed",ids===TOTAL?"ok":"bad","Duplicates and gaps: distinct id values = "+ids+" of "+TOTAL+"; duplicate text values = "+dup.length+" ("+extra+" extra records); not labelled — themes: "+noT+", SDGs: "+noS+", affected persons: "+noA+".");
  el.checks.innerHTML=lines.join("");
}
```

Sample:
```js
function drawSample(){
  var f=state.filtered;
  el.seedInput.value=state.seed;
  if(!f.length){el.cards.innerHTML='<div class="nomatch">No records match the current filters.</div>';el.tally.textContent="";state.sample=[];return;}
  var rnd=mulberry32(state.seed);
  var idx=[];for(var i=0;i<f.length;i++)idx.push(i);
  for(var j=idx.length-1;j>0;j--){var k=Math.floor(rnd()*(j+1));var t=idx[j];idx[j]=idx[k];idx[k]=t;}
  state.sample=idx.slice(0,Math.min(10,f.length)).map(function(i){return f[i];});
  state.openCard=null;
  renderCards();
}
function renderCards(){
  var html="";
  state.sample.forEach(function(r,i){
    var open=state.openCard===i;
    html+='<div class="card"><button class="cardhead" aria-expanded="'+open+'" data-i="'+i+'"><span class="sym">'+esc(r.symbol)+'</span> '+(r._para?esc("para. "+r._para):"no para.")+' — '+esc(r._first.length>90?r._first.slice(0,90)+"…":r._first)+'</button>';
    if(open){
      html+='<div class="cardbody"><p class="fulltext">'+esc(r.text)+'</p><div class="lbl2">Themes on this paragraph (UN labels)</div><div class="tagrow">'+(r.themes&&r.themes.length?r.themes.map(t=>'<span class="tag">'+esc(t)+'</span>').join(''):'<span class="hint">not labelled in the data</span>')+'</div><div style="margin-top:12px">';
      [["fit","Fits"],["no","Doesn’t fit"],["unsure","Unsure"]].forEach(function(v){
        html+='<button class="vbtn" data-i="'+i+'" data-v="'+v[0]+'" aria-pressed="'+(state.verdicts[r.id]===v[0])+'">'+v[1]+'</button>';
      });
      html+='</div></div>';
    }
    html+='</div>';
  });
  el.cards.innerHTML=html||'<div class="hint">Press “Draw with this seed” to draw ten records.</div>';
  renderTally();
}
function renderTally(){
  if(!state.sample.length){el.tally.textContent="";return;}
  var ids={};state.sample.forEach(r=>ids[r.id]=1);
  var x=0,y=0,z=0;
  Object.keys(state.verdicts).forEach(function(k){if(!ids[k])return;var v=state.verdicts[k];if(v==="fit")x++;else if(v==="no")y++;else if(v==="unsure")z++;});
  el.tally.textContent="Themes: "+x+" fit, "+y+" don’t, "+z+" unsure of "+state.sample.length+" judged · seed "+state.seed+" · drawn from the current filter ("+state.filtered.length+" records)";
}
el.cards.addEventListener("click",function(e){
  var vb=e.target.closest(".vbtn");
  if(vb){var r=state.sample[+vb.dataset.i];state.verdicts[r.id]=vb.dataset.v;renderCards();return;}
  var ch=e.target.closest(".cardhead");
  if(ch){var i=+ch.dataset.i;state.openCard=(state.openCard===i?null:i);renderCards();}
});
el.drawAgain.addEventListener("click",function(){state.seed=1+Math.floor(Math.random()*99999);drawSample();});
el.drawSeed.addEventListener("click",function(){var s=parseInt(el.seedInput.value,10);state.seed=isNaN(s)?1:s;drawSample();});
```

Method tab init:
```js
el.methodText.innerHTML=
 '<p>Every number on this page is computed in your browser by looping over the records of the attached file; nothing is estimated, and no model or network request is involved.</p>'+
 '<p>The headline total is <b>records.length</b>; documents are the distinct <b>symbol</b> values; years are the minimum and maximum of <b>year</b>, which is the document’s date, not the date a recommendation was made or accepted.</p>'+
 '<p>Filters combine with AND: mechanism, body, type, theme and recommending State are exact matches on the record’s fields; the year range is inclusive (a reversed range is swapped); the SDG filter keeps records whose <b>sdgs</b> list contains the chosen goal; the keyword filter keeps records in which every typed word occurs in the text or the symbol — literal and case-insensitive, so “torture” does not find “ill-treatment”.</p>'+
 '<p>Theme counts count each theme once per record that carries it, so they add up to more than the record count; percentages are shares of filtered records, not of labels.</p>'+
 '<p>Paragraph numbers are read from the start of each text with a regular expression; recommending States are read from the parentheses at the end of UPR texts only, and a group containing a comma or longer than 60 characters is recorded as “State not found”.</p>'+
 '<p>The CSV export is generated in the browser as a Blob, with comment lines naming the country, source, build date, filters applied and row count; the only thing that can leave this page is the clipboard write when you press a Copy button.</p>';
el.sourceBlock.innerHTML='Data: <a href="'+esc(U.source_url)+'" target="_blank" rel="noopener">'+esc(U.source)+'</a> · built '+esc(U.built)+' · '+TOTAL+' records (count field: '+esc(U.count)+') · country: '+esc(COUNTRY)+'. The Universal Human Rights Index is published by OHCHR; see the source page for its terms of use.';
```

CSV:
```js
function csvCell(s){s=(s==null?"":String(s));return /[",\n\r]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s;}
el.csvBtn.addEventListener("click",function(){
  var rows=state.filtered;
  var L=[];
  L.push("# Country: "+COUNTRY);
  L.push("# Source: "+U.source+" ("+U.source_url+")");
  L.push("# Built: "+U.built);
  L.push("# Filters: "+describeFilters());
  L.push("# Rows: "+rows.length+" of "+TOTAL+" records");
  L.push(["Date","Body","Mechanism","Type","Symbol","Doc URL","Paragraph","Recommending State(s)","Section","Themes","SDGs","SDG targets","Affected persons","Text"].map(csvCell).join(","));
  rows.forEach(function(r){
    L.push([r.date,r.body,r.mechanism,r.type,r.symbol,r.doc_url,r._para||"",(r._states||[]).join("; "),r.section||"",(r.themes||[]).join("; "),(r.sdgs||[]).join("; "),(r.sdg_targets||[]).join("; "),(r.affected_persons||[]).join("; "),r.text].map(csvCell).join(","));
  });
  var blob=new Blob([L.join("\n")],{type:"text/csv;charset=utf-8"});
  var a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download="uhri-"+COUNTRY.toLowerCase().replace(/[^a-z0-9]+/g,"-")+"-recommendations.csv";
  document.body.appendChild(a);a.click();a.remove();
  setTimeout(function(){URL.revokeObjectURL(a.href);},2000);
});
el.sumBtn.addEventListener("click",function(){
  copyText(summaryText(),function(){el.sumOk.hidden=false;setTimeout(function(){el.sumOk.hidden=true;},2000);});
});
```

describeFilters & summaryText as planned.

Filter events:
```js
el.mechSel.addEventListener("change",function(){F.mech=el.mechSel.value;if(!bodiesFor(F.mech).some(b=>b[0]===F.body))F.body="all";state.shown=50;syncInputs();renderAll();});
el.bodySel.addEventListener("change",function(){F.body=el.bodySel.value;state.shown=50;renderAll();});
el.typeSel.addEventListener("change",function(){F.type=el.typeSel.value;state.shown=50;renderAll();});
el.stateSel.addEventListener("change",function(){F.state=el.stateSel.value;state.shown=50;renderAll();});
el.sdgSel.addEventListener("change",function(){F.sdg=el.sdgSel.value;state.shown=50;renderAll();});
el.yFrom.addEventListener("change",function(){F.yFrom=el.yFrom.value;if(+F.yFrom>+F.yTo)F.yTo=F.yFrom;state.shown=50;syncInputs();renderAll();});
el.yTo.addEventListener("change",function(){F.yTo=el.yTo.value;if(+F.yTo<+F.yFrom)F.yFrom=F.yTo;state.shown=50;syncInputs();renderAll();});
el.clearAll.addEventListener("click",function(){
  F.kw="";F.mech="all";F.body="all";F.type="all";F.state="all";F.theme="all";F.yFrom=String(YMIN);F.yTo=String(YMAX);F.sdg="all";
  state.shown=50;syncInputs();renderAll();
});
```

syncInputs:
```js
function syncInputs(){
  el.kwRail.value=F.kw;el.searchTop.value=F.kw;
  el.mechSel.value=F.mech;
  fillBody();
  el.bodySel.value=F.body;
  el.typeSel.value=F.type;el.stateSel.value=F.state;
  el.yFrom.value=F.yFrom;el.yTo.value=F.yTo;el.sdgSel.value=F.sdg;
}
function fillBody(){
  var opts=[["all","All bodies / mandates"]].concat(bodiesFor(F.mech).map(b=>[b[0],b[0]+" ("+b[1]+")"]));
  fillSelect(el.bodySel,opts,F.body);
}
```

initFilters:
```js
function initFilters(){
  var mechFile=countBy(RECS,r=>r.mechanism);
  var mechOrder=Object.keys(mechFile).sort((a,b)=>mechFile[b]-mechFile[a]||(a<b?-1:1));
  fillSelect(el.mechSel,[["all","All mechanisms ("+TOTAL+")"]].concat(mechOrder.map(m=>[m,m+" ("+mechFile[m]+")"])),F.mech);
  fillBody();
  var typeFile=countBy(RECS,r=>r.type);
  fillSelect(el.typeSel,[["all","All types ("+TOTAL+")"]].concat(TYPES.map(t=>[t,t+" ("+typeFile[t]+")"])),F.type);
  var stOpts=[["all","All States"]].concat(Array.from(ALL_STATES.entries()).sort((a,b)=>b[1]-a[1]).map(e=>[e[0],e[0]+" ("+e[1]+")"]));
  fillSelect(el.stateSel,stOpts,F.state);
  fillSelect(el.yFrom,YEARS.map(y=>[String(y),String(y)]),F.yFrom);
  fillSelect(el.yTo,YEARS.map(y=>[String(y),String(y)]),F.yTo);
  var sdgMap={};RECS.forEach(r=>(r.sdgs||[]).forEach(g=>sdgMap[g]=(sdgMap[g]||0)+1));
  fillSelect(el.sdgSel,[["all","All SDGs"]].concat(SDGS.map(g=>[String(g),g+(SDGN[String(g)]?" — "+SDGN[String(g)]:"")+" ("+(sdgMap[g]||0)+")"])),F.sdg);
}
```

setFilter:
```js
function setFilter(key,val){F[key]=val;state.shown=50;syncInputs();renderAll();}
```

renderAll:
```js
function renderAll(){
  var f=filtered();
  state.filtered=f;
  renderRail(f);
  renderOverview(f);
  renderRecords(f);
  renderCheck(f);
  el.exportNote.textContent="Current filter: "+describeFilters()+" → "+f.length+" of "+TOTAL+" records.";
}
```

renderOverview with fig titles:
```js
function renderOverview(f){
  var typeCounts=countBy(RECS,r=>r.type);
  var docsAll=new Set(RECS.map(r=>r.symbol)).size;
  var mechFile=countBy(RECS,r=>r.mechanism);
  var mechOrder=Object.keys(mechFile).sort((a,b)=>mechFile[b]-mechFile[a]||(a<b?-1:1));
  var html='<div class="tiles">';
  html+='<div class="tile"><div class="lbl">All records in the file</div><div class="num">'+TOTAL+'</div><div class="sub">'+Object.keys(typeCounts).sort((a,b)=>typeCounts[b]-typeCounts[a]).map(t=>esc(t)+": "+typeCounts[t]).join(" · ")+'</div><div class="how">How this is computed: records.length of the attached file, before filters; the filtered count is the big number in the rail.</div></div>';
  html+='<div class="tile"><div class="lbl">Documents</div><div class="num">'+docsAll+'</div><div class="sub">distinct symbol values</div><div class="how">How this is computed: number of distinct symbol values across all records in the file.</div></div>';
  html+='<div class="tile"><div class="lbl">Years</div><div class="num">'+(YMIN!=null?YMIN+"–"+YMAX:"–")+'</div><div class="sub">dated by document</div><div class="how">How this is computed: minimum and maximum of year across all records; date is the document’s date.</div></div>';
  mechOrder.forEach(function(m){
    var sub=f.filter(r=>r.mechanism===m);
    var d=new Set(sub.map(r=>r.symbol)).size;
    var latest=sub.length?Math.max.apply(null,sub.map(r=>r.year)):"–";
    var share=f.length?(sub.length/f.length*100).toFixed(1):"0.0";
    html+='<div class="tile"><div class="lbl">'+esc(m)+'</div><div class="num">'+sub.length+'</div><div class="sub">'+d+' documents · latest '+latest+' · '+share+'% of filtered</div><div class="how">How this is computed: records, distinct symbols and latest year among the '+f.length+' filtered records; share = count ÷ '+f.length+'.</div>'+(m==="Universal Periodic Review"?'<div style="margin-top:6px"><button class="linkbtn" id="statesLink">see the States</button></div>':"")+'</div>';
  });
  html+='</div>';
  el.tiles.innerHTML=html;
  var sl=$("statesLink");
  if(sl)sl.addEventListener("click",function(){el.statesBox.hidden=!el.statesBox.hidden;});
  renderStatesBox(f);
  renderFig1(f);
  renderFig2(f);
}
```

renderStatesBox:
```js
function renderStatesBox(f){
  var ts=topStates(f,10);
  var h='<div class="lbl" style="margin-bottom:8px">Ten States that made most recommendations to '+esc(COUNTRY)+' · current filter: '+f.length+' records</div>';
  if(!ts.length)h+='<div class="hint">No recommending States found in the filtered UPR records.</div>';
  else h+='<table><caption>Count of recommendations, not of influence; two States can co-sponsor one line.</caption><thead><tr><th scope="col">State</th><th scope="col" class="num">Recommendations</th></tr></thead><tbody>'+ts.map(x=>'<tr><td>'+esc(x[0])+'</td><td class="num">'+x[1]+'</td></tr>').join('')+'</tbody></table>';
  el.statesBox.innerHTML=h;
}
```

renderFig1:
```js
var barValuePlugin={id:"barValue",afterDatasetsDraw:function(chart){var meta=chart.getDatasetMeta(0);if(!meta||!meta.data)return;var ctx=chart.ctx;ctx.save();ctx.font="12px ui-monospace, Menlo, Consolas, monospace";ctx.fillStyle="#1d1b18";meta.data.forEach(function(bar,i){var v=chart.data.datasets[0].data[i];if(v==null)return;ctx.fillText(String(v),bar.x+6,bar.y+4);});ctx.restore();}};
function renderFig1(f){
  var tt=topThemes(f,10);
  state.top10=tt;
  el.fig1Title.textContent="Ten most frequent themes · "+f.length+" filtered records";
  el.fig1Sub.textContent="each theme counts once per filtered record that carries it · click a bar = filter by that theme";
  var yr={};
  f.forEach(r=>{(r.themes||[]).forEach(t=>{if(!yr[t])yr[t]={min:r.year,max:r.year};if(r.year<yr[t].min)yr[t].min=r.year;if(r.year>yr[t].max)yr[t].max=r.year;});});
  var th='<table><caption>The same ten rows as the bars. A record can carry several themes, so the counts add up to more than '+f.length+'.</caption><thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead><tbody>';
  if(!f.length)th+='<tr><td colspan="4">No records match the current filters.</td></tr>';
  else tt.forEach(x=>{th+='<tr><td>'+esc(x[0])+'</td><td class="num">'+x[1]+'</td><td class="num">'+(f.length?(x[1]/f.length*100).toFixed(1):"0.0")+'</td><td>'+(yr[x[0]]?yr[x[0]].min+"–"+yr[x[0]].max:"–")+'</td></tr>';});
  th+='</tbody></table>';
  el.fig1Table.innerHTML=th;
  if(!f.length){el.fig1Wrap.hidden=true;el.fig1Empty.hidden=false;return;}
  el.fig1Wrap.hidden=false;el.fig1Empty.hidden=true;
  var labels=tt.map(x=>x[0]),data=tt.map(x=>x[1]);
  if(state.chart1){state.chart1.data.labels=labels;state.chart1.data.datasets[0].data=data;state.chart1.update();}
  else{
    state.chart1=new Chart(el.fig1Ctx,{type:"bar",data:{labels:labels,datasets:[{data:data,backgroundColor:"rgba(155,35,53,.8)",borderWidth:0,barThickness:16}]},options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,onClick:function(e,els){if(els&&els.length){var t=state.chart1.data.labels[els[0].index];if(t)setFilter("theme",t);}},plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.parsed.x+" records";}}}},scales:{x:{beginAtZero:true,ticks:{precision:0},grid:{color:"#e3dccb"}},y:{grid:{display:false},ticks:{autoSkip:false,font:{size:13}}}}},plugins:[barValuePlugin]});
  }
}
```

renderFig2 as planned with MECH_COLORS.

renderRecords:
```js
function sorted(f){
  var arr=f.slice();
  arr.sort(function(a,b){
    var d=state.dateAsc?(a.date<b.date?-1:1):(a.date>b.date?-1:1);
    if(a.date===b.date)d=0;
    if(d)return d;
    if(a.body!==b.body)return a.body<b.body?-1:1;
    if(a._paraNum!==b._paraNum)return a._paraNum-b._paraNum;
    return a._i-b._i;
  });
  return arr;
}
```
Careful: date compare — if equal, d should be 0. Write:
```js
var d=0;
if(a.date!==b.date)d=state.dateAsc?(a.date<b.date?-1:1):(a.date>b.date?-1:1);
```

```js
function renderRecords(f){
  el.searchTop.value=F.kw;
  var arr=sorted(f);
  var shown=Math.min(state.shown,arr.length);
  var w=kwWords();
  var rows="";
  for(var i=0;i<shown;i++){
    var r=arr[i];
    rows+='<tr class="rec" tabindex="0" role="button" aria-expanded="false" data-id="'+esc(r.id)+'"><td>'+esc(r.date)+'</td><td>'+esc(r.body)+'</td><td><a class="sym" href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a></td><td class="num">'+esc(r._para||"–")+'</td><td>'+markify(r._first,w)+'</td><td>'+(r._states?esc(r._states.join("; ")):"–")+'</td></tr>';
    rows+='<tr class="detail" hidden><td colspan="6" data-detail="'+esc(r.id)+'"></td></tr>';
  }
  el.tbody.innerHTML=rows;
  el.tableCaption.textContent=f.length?("Showing "+shown+" of "+f.length+" matching records · "+(state.dateAsc?"oldest first":"newest first")):"No records match the current filters.";
  el.sortDate.textContent="Date "+(state.dateAsc?"↑":"↓");
  el.moreBtn.hidden=!(state.shown<f.length);
  if(state.shown<f.length)el.moreBtn.textContent="Show 50 more ("+(f.length-state.shown)+" remaining)";
}
```

Events for sortDate & moreBtn:
```js
el.sortDate.addEventListener("click",function(){state.dateAsc=!state.dateAsc;renderRecords(state.filtered);});
el.moreBtn.addEventListener("click",function(){state.shown+=50;renderRecords(state.filtered);});
```

tbody events as planned.

OK — also initial drawSample? Spec: "Check 10 at random" draws the cards — a button? "the random-sample label check: 'Check 10 at random' draws the cards (then 'Draw again' and 'Draw with this seed'...)". So there should be an initial "Check 10 at random" button. I'll make the primary button "Check 10 at random" (id drawSeed? no) — let me have three buttons: "Check 10 at random" (draws with current seed, default 1), "Draw again" (new random seed), "Draw with this seed" (uses box). Actually "Check 10 at random" then "Draw again" and "Draw with this seed" — three buttons. I'll add id="draw10" for the first. On load, draw automatically? "Never call studio.ask on page load" — that's about model; drawing sample on load is fine but only when tab 03 opened? Simpler: draw on first render of check tab... renderCheck runs every renderAll. I'll call drawSample() once at init (seed 1) so cards are ready. That's deterministic, fine.

Buttons: draw10 ("Check 10 at random") → state.seed stays, drawSample(); drawAgain → new seed; drawSeed → from box.

Hmm "Check 10 at random" with seed shown default 1 — it's seeded random. Fine.

Now assemble final HTML. Also add small "sr-only" class? Not needed.

Also the hint under searchTop mentions same box as rail.

Edge: `el.searchTop.value=F.kw` in renderRecords — when user types in searchTop, input event sets other input and schedules render; render sets value to F.kw which equals typed (after debounce) — no clobber mid-typing since render only after debounce. But other renders (e.g., chip click) while user typed but not debounced — rare, acceptable.

One more: markify on first line — first line may contain "…" char, fine.

Also add `lang="en"`.

Let me also double-check the tablist arrow-key handler uses tabButtons.

Potential Chart.js issue: creating chart on canvas inside `.chartwrap` with position:relative and fixed height — good.

FIG.02 x-axis title "year (dated by document)" — ok.

Now count check line for "Chart against table" — uses state.top10 set by renderFig1 which runs before renderCheck in renderAll. On init, renderAll order: rail, overview (sets top10), records, check. Good.

Write final. Also include a `<noscript>`? Not needed.

Let me make sure I don't exceed ~1500 lines — will be around 800-900. Good.

Final check on required elements:
- Header label "UHRI · Kenya" ✓ (dynamic country)
- Title serif ✓
- meta line with source link, n records, n documents, years, built, "dated by document" ✓
- Rail: FILTERS + Clear all ✓, big number aria-live ✓, "of N in the file" ✓, red share bar ✓, chips ✓, three numbered headings closed until clicked, one open at a time, aria-expanded ✓, hidden on tabs 3/4 ✓
- 01 Keyword text box 300ms, hint ✓
- 02 Mechanism/body/type + State select ✓
- 03 Years from/to + SDG ✓
- Tab 01: tiles (all records w/ type breakdown, documents, years, per-mechanism tiles w/ records, docs, latest year, share) ✓ each with how note ✓; FIG.01 top-10 themes chart + click bar = chip + table Theme|Records|%|Years + note ✓; FIG.02 stacked per year by mechanism with gaps ✓; UPR tile "see the States" in-place list ✓
- Tab 02: search field ✓ caption rows shown/matching ✓; columns Date|Body|Symbol(link new tab)|Para.|First line|Recommending State ✓; sort date desc default, click header reverses ✓; mark highlight ✓; 50 rows + show more ✓; row expand in place: para big red, full verbatim text, labels, Copy citation, Open UN document ✓; citation format ✓ with "(no paragraph number...)" label ✓
- Tab 03: check panel lines ✓ (count, partitions mech/body/year, type, chart vs table, links w/ failures listed, para share per mechanism w/ UPR warning, states found w/ list, duplicates/gaps/missing labels) ✓; sample: seed box default 1, Check 10 at random / Draw again / Draw with this seed, cards one line each one open at a time, symbol link, para, full text, theme chips, Fits/Doesn't fit/Unsure, tally with seed ✓; "nothing is sent anywhere" line ✓
- Tab 04: method 6 sentences ✓, CSV download with comment lines + Blob ✓, Copy summary ✓, source/licence/build ✓
- Footer one line monospace ✓
- No model calls, no network ✓
- Design tokens ✓, focus ring ✓, [hidden] rule ✓, tablist arrow keys ✓, aria-expanded on fheads and rows ✓, aria-live on count ✓, caption/th scope ✓, numbers right-aligned ✓

One thing: "Recommending State ... as a filter (a select listing every State found, with counts)" ✓ in heading 02.

Also "On tab 01, a small 'see the States' link in the UPR tile opens a short list in place" ✓.

Now write the answer. Before code: 2-3 sentences. After: nothing.

Let me write out the complete file text now, being careful with syntax.

Also: in HTML I use `&amp;` in "04 Method & export" tab label.

For the seed input label: `<label class="lbl" for="seedInput">seed</label>`.

Also add hint near sample: "This is your judgement of the UN's labels; nothing is sent anywhere." ✓ (figsub).

Writing now. I'll be meticulous with matching braces.

One subtle thing: in renderCards, cardhead contains esc(r._first...) — fine.

In detailHTML, `data-cite="'+esc(cite)+'"` — cite contains ", " and "." fine.

copyText fallback uses execCommand — allowed (not network).

Also `URL.createObjectURL` — allowed (local blob).

Let me now also handle the case YEARS empty (no records): guard YMIN null — selects empty; filtered works; charts: YEARS empty → labels empty. Fine, minimal guards in place.

Time to write the final response.