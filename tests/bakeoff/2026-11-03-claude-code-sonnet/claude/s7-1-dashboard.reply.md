I built the dashboard from your plan: headline tiles, combined filters with removable chips, a ranked theme chart with its table, a stacked timeline by mechanism, and a table of paragraphs linked to the UN documents. Every number is counted by code in the page from the attached file, and a self-check panel with a seeded ten-record sample lets you test the UN's theme labels yourself. You can also download the current selection as CSV or copy a short summary for your notes.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations dashboard</title>
<style>
:root{--accent:#1f6fb2;--ink:#1d2733;--muted:#566474;--line:#d9e0e7;--bg:#f6f8fa;--card:#fff;--bad:#b3261e;--warn:#8a5a00;--ok:#1e6b3a}
*{box-sizing:border-box}
html{font-size:16px}
body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;line-height:1.5}
main{max-width:1200px;margin:0 auto;padding:24px 20px 56px}
h1{font-size:1.9rem;line-height:1.25;margin:0 0 .3rem}
h2{font-size:1.35rem;margin:2.4rem 0 .6rem;padding-top:.5rem;border-top:2px solid var(--accent)}
h3{font-size:1.05rem;margin:0 0 .3rem}
a{color:var(--accent)}
.lead{font-size:1.05rem;margin:.2rem 0 .6rem}
.note{color:var(--muted);font-size:.9rem;margin:.4rem 0}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px 14px}
.tile .big{font-size:1.9rem;font-weight:700;color:var(--accent);line-height:1.15}
.tile .sub{font-size:.92rem;min-height:1.4em}
.tile .how{font-size:.82rem;color:var(--muted);margin:.45rem 0 0}
.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;align-items:end;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:14px}
label{display:flex;flex-direction:column;font-size:.9rem;font-weight:600;gap:4px}
label .hint{font-weight:400;color:var(--muted);font-size:.8rem}
select,input[type=search],input[type=number],textarea{font:inherit;padding:6px 8px;border:1px solid #8f9daa;border-radius:4px;background:#fff;color:var(--ink);width:100%;max-width:100%}
button{font:inherit;cursor:pointer}
.btn{display:inline-block;background:var(--accent);color:#fff;border:1px solid var(--accent);border-radius:4px;padding:7px 14px;text-decoration:none;font-size:.95rem}
.btn.ghost{background:#fff;color:var(--accent)}
.btn[aria-pressed=true]{background:#0f3f6b;border-color:#0f3f6b;color:#fff}
:focus-visible{outline:3px solid #e08a00;outline-offset:2px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:.7rem 0 .2rem;min-height:2px}
.chip{background:#e8f1f9;color:#0f3f6b;border:1px solid #9cc1e0;border-radius:16px;padding:3px 12px;font-size:.9rem}
#showing{font-weight:600;margin:.6rem 0 .2rem}
.panel{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:14px 16px}
.chartbox{position:relative;width:100%}
.msg{padding:18px 0;color:var(--muted)}
.tw{overflow-x:auto}
table{width:100%;border-collapse:collapse;background:#fff;font-size:.95rem}
caption{text-align:left;font-weight:600;padding:8px 0}
th,td{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
thead th{border-bottom:2px solid #8f9daa;background:#f0f4f8}
.num{text-align:right;font-variant-numeric:tabular-nums}
.nw{white-space:nowrap}
.hbtn{background:none;border:0;padding:0;font-weight:700;color:inherit}
.toggle{background:none;border:0;padding:0;text-align:left;color:inherit;width:100%}
.toggle::before{content:"\25B8  ";color:var(--accent)}
.toggle[aria-expanded=true]::before{content:"\25BE  "}
tr.main{cursor:pointer}
tr.main.open td{background:#eef5fb}
tr.detail td{background:#f9fbfd}
.full{white-space:pre-wrap;margin:.2rem 0 .6rem}
dl.labels{display:grid;grid-template-columns:150px 1fr;gap:4px 12px;margin:.4rem 0 .8rem}
dl.labels dt{font-weight:700;font-size:.9rem}
dl.labels dd{margin:0}
.tag{display:inline-block;background:#eef1f4;border:1px solid var(--line);border-radius:4px;padding:1px 8px;margin:2px 4px 2px 0;font-size:.88rem}
.tag.missing{font-style:italic;color:var(--muted);background:#fff}
.linkbtn{background:none;border:0;padding:0;color:var(--accent);text-decoration:underline;text-align:left}
mark{background:#ffe58f;color:inherit;padding:0 1px}
.copied{color:var(--ok);font-weight:600;margin-left:8px}
[hidden]{display:none!important}
ul.checks{list-style:none;margin:0;padding:0}
.chk{display:flex;gap:12px;padding:10px 0;border-bottom:1px solid var(--line)}
.chk .mark{flex:0 0 130px;font-weight:700}
.chk.ok .mark{color:var(--ok)}
.chk.warn .mark{color:var(--warn)}
.chk.fail .mark{color:var(--bad)}
.chk.fail{background:#fdf1f0}
.chk div{min-width:0}
details summary{cursor:pointer;color:var(--accent)}
details ul{margin:.3rem 0 .3rem 1.1rem;padding:0;font-size:.88rem}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:12px;margin-top:10px}
.card{background:#fff;border:1px solid var(--line);border-radius:6px;padding:12px 14px}
.card .full{max-height:260px;overflow:auto;font-size:.93rem}
.vrow{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
.seedrow{display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end;margin:.6rem 0}
.seedrow label{width:140px}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:.6rem 0}
footer{margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--line);color:var(--muted);font-size:.88rem}
.sr{position:absolute;left:-9999px}
@media (max-width:700px){dl.labels{grid-template-columns:1fr}.chk{flex-direction:column;gap:2px}}
</style>
</head>
<body>
<main>
<header>
 <h1 id="title">UN human rights recommendations and observations</h1>
 <p class="lead" id="subtitle"></p>
 <p class="note">Dates are "dated by document": the date of the UN document, not the date a recommendation was made or accepted. Every number on this page is counted by code in your browser from the loaded file. No model is called and nothing leaves the page, except the clipboard when you press a Copy button.</p>
</header>

<section aria-labelledby="h-tiles">
 <h2 id="h-tiles">Headline numbers</h2>
 <div class="tiles" id="tiles"></div>
</section>

<section aria-labelledby="h-filters">
 <h2 id="h-filters">Filters</h2>
 <div class="filters">
  <label>Mechanism<select id="f-mech"></select></label>
  <label>Body or mandate<select id="f-body"></select></label>
  <label>Year from<select id="f-from"></select></label>
  <label>Year to<select id="f-to"></select></label>
  <label>SDG<select id="f-sdg"></select></label>
  <label>Type<select id="f-type"></select></label>
  <label>Recommending State (UPR rows only)<select id="f-state"></select></label>
  <label>Keyword<input id="f-kw" type="search" autocomplete="off"><span class="hint">Literal match, not synonyms: "torture" does not find "ill-treatment".</span></label>
  <div><button type="button" class="btn ghost" id="reset">Reset</button></div>
 </div>
 <div class="chips" id="chips" aria-label="Active filters"></div>
 <p id="showing" aria-live="polite"></p>
 <p class="note">How this is computed: all filters are combined with AND on the loaded records. Keyword means every word must appear in the paragraph text or the document symbol.</p>
</section>

<section aria-labelledby="h-c1">
 <h2 id="h-c1">What the paragraphs are about</h2>
 <div class="panel">
  <h3 id="c1title"></h3>
  <div class="chartbox" id="c1wrap"><canvas id="c1" role="img" aria-label="Horizontal bar chart of the ten most frequent themes"></canvas></div>
  <p class="msg" id="c1msg" hidden></p>
  <p class="note" id="c1note">How this is computed: each record counts once under every theme it carries, so the bars add up to more than the number of records. Percentages are shares of records, not of labels. Click a bar or a theme name to filter by it.</p>
  <div class="tw">
   <table id="themeTable">
    <caption>The same ten themes as a table</caption>
    <thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years (first to last)</th></tr></thead>
    <tbody id="themeBody"></tbody>
   </table>
  </div>
  <p class="note" id="c1src"></p>
  <p class="note">Labels are the UN's, shown as they are. Check the year range: a theme that spans very different years, or that looks odd against the sample check below, may be a legacy label.</p>
 </div>
</section>

<section aria-labelledby="h-c2">
 <h2 id="h-c2">When the UN spoke</h2>
 <div class="panel">
  <h3 id="c2title"></h3>
  <div class="chartbox" id="c2wrap" style="height:340px"><canvas id="c2" role="img" aria-label="Stacked bar chart of records per year by mechanism"></canvas></div>
  <p class="msg" id="c2msg" hidden></p>
  <p class="note">How this is computed: records per document year, split by mechanism, for the current filter. Every year from the first to the last is shown, so an empty year is a gap.</p>
  <p class="note" id="gaps"></p>
  <p class="note" id="c2src"></p>
 </div>
 <div class="panel" style="margin-top:14px">
  <h3>Ten States that made most recommendations to <span id="cname"></span></h3>
  <ol id="statesList"></ol>
  <p class="note">How this is computed: for Universal Periodic Review rows only, the State or States in the parentheses at the end of the text. It counts recommendations, not influence; a line with several States counts once for each.</p>
 </div>
</section>

<section aria-labelledby="h-table">
 <h2 id="h-table">The paragraphs</h2>
 <div class="tw">
  <table id="tbl">
   <caption id="cap"></caption>
   <thead><tr>
    <th scope="col" id="thDate" aria-sort="descending"><button type="button" class="hbtn" id="dateSort"></button></th>
    <th scope="col">Body</th>
    <th scope="col">Symbol</th>
    <th scope="col" class="num">Para.</th>
    <th scope="col">First line (click a row for the full text)</th>
    <th scope="col" id="thState">Recommending State</th>
   </tr></thead>
   <tbody id="tbody"></tbody>
  </table>
 </div>
 <div class="row"><button type="button" class="btn ghost" id="more">Show 50 more</button></div>
 <p class="note" id="tblSource"></p>
 <p class="note">How this is computed: rows are sorted by document date, then body, then paragraph number (numeric). The paragraph number is the number at the start of the text, if there is one; the full text is never shortened or changed.</p>
</section>

<section aria-labelledby="h-check">
 <h2 id="h-check">Check this dashboard</h2>
 <p class="note">How the app checks itself: each line says what was compared and the two values. A failure is shown in red with the values, never hidden.</p>
 <div class="panel"><ul class="checks" id="checks"></ul></div>
 <h3 style="margin-top:1.4rem">Random-sample label check</h3>
 <p class="note">This is your judgement of the UN's labels; nothing is sent anywhere. For each paragraph, judge the themes shown as a set. The sample is drawn from the current filter with a seeded generator (mulberry32), so a colleague with the same filters and seed sees the same ten. Changing a filter draws a new sample and clears your verdicts.</p>
 <div class="seedrow">
  <label>Seed<input type="number" id="seed" value="1" min="0" step="1"></label>
  <button type="button" class="btn" id="drawAgain">Draw again</button>
  <button type="button" class="btn ghost" id="drawSeed">Draw with this seed</button>
 </div>
 <p id="tally" aria-live="polite" style="font-weight:600"></p>
 <div class="cards" id="cards"></div>
</section>

<section aria-labelledby="h-export">
 <h2 id="h-export">Take it with you</h2>
 <div class="row">
  <button type="button" class="btn" id="dl">Download CSV of the current filter</button>
  <button type="button" class="btn ghost" id="cs">Copy summary</button>
  <span class="copied" id="csStatus" role="status"></span>
 </div>
 <p class="note">How this is computed: the CSV holds the visible columns plus the full text and labels, headed by comment lines with the country, source, build date, filters and row count. A cell that starts with = + - or @ gets a leading apostrophe so spreadsheets do not read it as a formula.</p>
 <label>Summary text (also copied to the clipboard)<textarea id="summary" rows="6" readonly></textarea></label>
</section>

<footer id="footer"></footer>
</main>

<script>
(function(){
'use strict';

var D = window.WORKSHOP_DATA || {};
var U = D.uhri || {};
var raw = Array.isArray(U.records) ? U.records : [];
var COUNTRY = U.country ? String(U.country) : 'the selected country';
var SDGN = U.sdg_names || {};
var UPR = 'Universal Periodic Review';
var PARA_RE = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
var RUN_RE = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
var GRP_RE = /\((?:[^()]|\([^()]*\))*\)/g;
var FONT = '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif';
var MECH_COLORS = ['#1f6fb2', '#9ecae1', '#4a4a4a', '#c9892a', '#7a7a7a'];
var PAGE = 50;

function $(id){ return document.getElementById(id); }
function esc(s){ return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }
function fmt(n){ return Number(n).toLocaleString('en-GB'); }
function arr(x){ return Array.isArray(x) ? x : []; }
function map(){ return Object.create(null); }
function safeUrl(u){ u = String(u || ''); return /^https?:\/\//i.test(u) ? u : ''; }
function link(url, html){ var u = safeUrl(url); return u ? '<a href="' + esc(u) + '" target="_blank" rel="noopener">' + html + '</a>' : html; }
function trunc(s, n){ s = String(s); return s.length > n ? s.slice(0, n - 1) + '…' : s; }
function range(a, b){ return a == null ? '–' : (a === b ? String(a) : a + '–' + b); }
function pct(c, n){ return n ? (c / n * 100).toFixed(1) + '%' : '–'; }

/* ---------- prepare records ---------- */
function statesOf(o){
  if (o.mech !== UPR) { return null; }
  var m = RUN_RE.exec(o.text);
  if (!m) { return []; }
  var groups = m[1].match(GRP_RE) || [];
  var out = [];
  for (var k = 0; k < groups.length; k++) {
    var s = groups[k].slice(1, -1).trim();
    if (!s || s.indexOf(',') >= 0 || s.length > 60) { return []; }
    if (out.indexOf(s) < 0) { out.push(s); }
  }
  return out;
}

var recs = raw.map(function(r, i){
  var text = String(r.text == null ? '' : r.text);
  var m = PARA_RE.exec(text);
  var y = typeof r.year === 'number' ? r.year : parseInt(r.year, 10);
  var o = {
    r: r, i: i, text: text,
    symbol: String(r.symbol || ''), body: String(r.body || ''),
    mech: String(r.mechanism || ''), type: String(r.type || ''),
    year: isFinite(y) ? y : null, date: String(r.date || ''),
    themes: arr(r.themes), sdgs: arr(r.sdgs).map(Number), targets: arr(r.sdg_targets),
    aff: arr(r.affected_persons), section: String(r.section || ''),
    para: m ? m[1] : '', paraKey: m ? m[1].split('.').map(Number) : null
  };
  o.hay = (text + '\n' + o.symbol).toLowerCase();
  o.states = statesOf(o);
  return o;
});
var N = recs.length;

function distinctSorted(fn, numeric){
  var seen = map(), out = [];
  recs.forEach(function(o){ var v = fn(o); if (v !== null && v !== '' && !seen[v]) { seen[v] = 1; out.push(v); } });
  return out.sort(numeric ? function(a, b){ return a - b; } : function(a, b){ return String(a).localeCompare(String(b)); });
}
var YEARS = distinctSorted(function(o){ return o.year; }, true);
var MECHS = distinctSorted(function(o){ return o.mech; });
var TYPES = distinctSorted(function(o){ return o.type; });
var SDG_LIST = (function(){
  var seen = map(), out = [];
  recs.forEach(function(o){ o.sdgs.forEach(function(g){ if (isFinite(g) && !seen[g]) { seen[g] = 1; out.push(g); } }); });
  return out.sort(function(a, b){ return a - b; });
})();
var STATE_COUNT = (function(){
  var m = map();
  recs.forEach(function(o){ if (o.states) { o.states.forEach(function(s){ m[s] = (m[s] || 0) + 1; }); } });
  return m;
})();

/* ---------- state ---------- */
var F, W = [], CUR = [], TOP = [], SORTED = [], shown = PAGE, dateDesc = true;
var OPEN = {}, bodyBuiltFor = null, sample = [], verdicts = {}, TILEINFO = {};
var chart1 = null, chart2 = null, kwTimer = null;

function resetF(){
  F = { mech: '', body: '', from: YEARS.length ? YEARS[0] : null, to: YEARS.length ? YEARS[YEARS.length - 1] : null,
        sdg: '', type: '', kw: '', state: '', themes: [] };
}
function yearActive(){ return YEARS.length > 0 && (F.from !== YEARS[0] || F.to !== YEARS[YEARS.length - 1]); }
function words(){ return F.kw.trim().toLowerCase().split(/\s+/).filter(Boolean); }

function match(o){
  if (F.mech && o.mech !== F.mech) { return false; }
  if (F.body && o.body !== F.body) { return false; }
  if (F.type && o.type !== F.type) { return false; }
  if (yearActive() && (o.year == null || o.year < F.from || o.year > F.to)) { return false; }
  if (F.sdg !== '' && o.sdgs.indexOf(Number(F.sdg)) < 0) { return false; }
  if (F.state && !(o.states && o.states.indexOf(F.state) >= 0)) { return false; }
  for (var t = 0; t < F.themes.length; t++) { if (o.themes.indexOf(F.themes[t]) < 0) { return false; } }
  for (var w = 0; w < W.length; w++) { if (o.hay.indexOf(W[w]) < 0) { return false; } }
  return true;
}

function activeFilters(){
  var c = [];
  if (F.mech) { c.push({ k: 'mech', label: 'Mechanism: ' + F.mech }); }
  if (F.body) { c.push({ k: 'body', label: 'Body: ' + F.body }); }
  if (yearActive()) { c.push({ k: 'years', label: 'Years: ' + F.from + '–' + F.to }); }
  if (F.sdg !== '') { c.push({ k: 'sdg', label: 'SDG ' + F.sdg + (SDGN[F.sdg] ? ': ' + SDGN[F.sdg] : '') }); }
  if (F.type) { c.push({ k: 'type', label: 'Type: ' + F.type }); }
  if (F.kw.trim()) { c.push({ k: 'kw', label: 'Keyword: ' + F.kw.trim() }); }
  if (F.state) { c.push({ k: 'state', label: 'Recommending State: ' + F.state }); }
  F.themes.forEach(function(t, k){ c.push({ k: 'theme', t: k, label: 'Theme: ' + t }); });
  return c;
}

/* ---------- sorting ---------- */
function cmpPara(a, b){
  if (!a.paraKey && !b.paraKey) { return 0; }
  if (!a.paraKey) { return 1; }
  if (!b.paraKey) { return -1; }
  if (a.paraKey[0] !== b.paraKey[0]) { return a.paraKey[0] - b.paraKey[0]; }
  var x = a.paraKey.length > 1 ? a.paraKey[1] : -1, y = b.paraKey.length > 1 ? b.paraKey[1] : -1;
  return x - y;
}
function sorted(list){
  var dir = dateDesc ? -1 : 1;
  return list.slice().sort(function(a, b){
    if (a.date !== b.date) { return a.date < b.date ? dir : -dir; }
    if (a.body !== b.body) { return a.body < b.body ? -1 : 1; }
    var p = cmpPara(a, b);
    if (p) { return p; }
    return a.i - b.i;
  });
}

function hl(t){
  if (!W.length) { return esc(t); }
  var re = new RegExp('(' + W.map(function(w){ return w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|') + ')', 'gi');
  return String(t).split(re).map(function(p, k){ return k % 2 ? '<mark>' + esc(p) + '</mark>' : esc(p); }).join('');
}
function firstLine(t){
  t = t.replace(/\s+/g, ' ').trim();
  if (t.length <= 120) { return t; }
  var cut = t.slice(0, 120), sp = cut.lastIndexOf(' ');
  if (sp > 0) { cut = cut.slice(0, sp); }
  return cut + '…';
}
function citation(o){ return o.para ? o.symbol + ', para. ' + o.para : o.symbol; }
function sdgLabel(g){ return 'Goal ' + g + (SDGN[String(g)] ? ': ' + SDGN[String(g)] : ''); }
function sourceText(){ return U.source ? String(U.source) : 'source not stated in the file'; }

/* ---------- controls ---------- */
function fillSelect(id, opts){
  $(id).innerHTML = opts.map(function(o){ return '<option value="' + esc(o.v) + '">' + esc(o.t) + '</option>'; }).join('');
}
function buildSelects(){
  var mc = map();
  recs.forEach(function(o){ mc[o.mech] = (mc[o.mech] || 0) + 1; });
  fillSelect('f-mech', [{ v: '', t: 'All mechanisms (' + fmt(N) + ')' }].concat(MECHS.map(function(m){ return { v: m, t: m + ' (' + fmt(mc[m]) + ')' }; })));
  var yo = YEARS.map(function(y){ return { v: y, t: String(y) }; });
  fillSelect('f-from', yo); fillSelect('f-to', yo);
  fillSelect('f-sdg', [{ v: '', t: 'All goals' }].concat(SDG_LIST.map(function(g){ return { v: g, t: sdgLabel(g) }; })));
  var tc = map();
  recs.forEach(function(o){ tc[o.type] = (tc[o.type] || 0) + 1; });
  fillSelect('f-type', [{ v: '', t: 'All types' }].concat(TYPES.map(function(t){ return { v: t, t: t + ' (' + fmt(tc[t]) + ')' }; })));
  var names = Object.keys(STATE_COUNT).sort(function(a, b){ return a.localeCompare(b); });
  fillSelect('f-state', [{ v: '', t: names.length ? 'All States (' + names.length + ' found)' : 'No States found' }].concat(names.map(function(s){ return { v: s, t: s + ' (' + fmt(STATE_COUNT[s]) + ')' }; })));
}
function buildBody(){
  var bc = map(), names = [];
  recs.forEach(function(o){ if (!F.mech || o.mech === F.mech) { if (!bc[o.body]) { names.push(o.body); } bc[o.body] = (bc[o.body] || 0) + 1; } });
  names = names.filter(function(b){ return b !== ''; }).sort(function(a, b){ return a.localeCompare(b); });
  if (F.body && names.indexOf(F.body) < 0) { F.body = ''; }
  fillSelect('f-body', [{ v: '', t: 'All bodies and mandates' }].concat(names.map(function(b){ return { v: b, t: b + ' (' + fmt(bc[b]) + ')' }; })));
  bodyBuiltFor = F.mech;
}
function setValues(){
  $('f-mech').value = F.mech; $('f-body').value = F.body;
  if (F.from != null) { $('f-from').value = F.from; $('f-to').value = F.to; }
  $('f-sdg').value = F.sdg; $('f-type').value = F.type; $('f-state').value = F.state;
  if ($('f-kw').value !== F.kw) { $('f-kw').value = F.kw; }
}

/* ---------- rendering: tiles, chips ---------- */
function tile(label, big, sub, how){
  return '<div class="tile"><h3>' + esc(label) + '</h3><div class="big">' + big + '</div><div class="sub">' + sub + '</div><p class="how">How this is computed: ' + how + '</p></div>';
}
function renderTiles(list){
  var n = list.length, docs = map(), dn = 0, ymin = null, ymax = null, tc = map(), mc = map();
  list.forEach(function(o){
    if (!docs[o.symbol]) { docs[o.symbol] = 1; dn++; }
    if (o.year != null) { if (ymin == null || o.year < ymin) { ymin = o.year; } if (ymax == null || o.year > ymax) { ymax = o.year; } }
    tc[o.type] = (tc[o.type] || 0) + 1;
    var m = mc[o.mech] || (mc[o.mech] = { n: 0, docs: map(), d: 0, y: null });
    m.n++;
    if (!m.docs[o.symbol]) { m.docs[o.symbol] = 1; m.d++; }
    if (o.year != null && (m.y == null || o.year > m.y)) { m.y = o.year; }
  });
  var tarr = Object.keys(tc).sort(function(a, b){ return tc[b] - tc[a] || a.localeCompare(b); });
  TILEINFO = { n: n, dn: dn, ymin: ymin, ymax: ymax, types: tarr.map(function(t){ return [t, tc[t]]; }), mechs: MECHS.map(function(m){ var x = mc[m]; return [m, x ? x.n : 0, x ? x.d : 0, x ? x.y : null]; }) };
  var h = tile('Records', fmt(n),
    n ? tarr.map(function(t){ return esc(t) + ' ' + fmt(tc[t]); }).join(' · ') : 'no records',
    'counts every record in the current selection, whatever its type; with no filter that is the whole file.');
  h += tile('Documents', fmt(dn), 'distinct document symbols', 'the number of different symbols among these records.');
  h += tile('Years', range(ymin, ymax), 'first to last document year', 'the smallest and largest year among these records.');
  MECHS.forEach(function(m){
    var x = mc[m];
    h += tile(m, fmt(x ? x.n : 0), (x ? fmt(x.d) : '0') + ' documents · latest year ' + (x && x.y != null ? x.y : '–'),
      'records, distinct symbols and the latest year among the selected records of this mechanism.');
  });
  $('tiles').innerHTML = h;
}
function renderChips(){
  $('chips').innerHTML = activeFilters().map(function(c){
    return '<button type="button" class="chip" data-k="' + c.k + '"' + (c.t != null ? ' data-t="' + c.t + '"' : '') + ' aria-label="Remove filter ' + esc(c.label) + '">' + esc(c.label) + ' <span aria-hidden="true">×</span></button>';
  }).join('');
}

/* ---------- rendering: themes ---------- */
function themeTop(list){
  var m = map(), y = map();
  list.forEach(function(o){
    var seen = map();
    o.themes.forEach(function(t){
      if (seen[t]) { return; }
      seen[t] = 1; m[t] = (m[t] || 0) + 1;
      if (o.year != null) {
        if (!y[t]) { y[t] = [o.year, o.year]; }
        else { if (o.year < y[t][0]) { y[t][0] = o.year; } if (o.year > y[t][1]) { y[t][1] = o.year; } }
      }
    });
  });
  return Object.keys(m).map(function(k){ return [k, m[k], y[k] || null]; })
    .sort(function(a, b){ return b[1] - a[1] || a[0].localeCompare(b[0]); }).slice(0, 10);
}
function addTheme(t){
  if (F.themes.indexOf(t) < 0) { F.themes.push(t); update(); }
}
var vlPlugin = {
  id: 'valueLabels',
  afterDatasetsDraw: function(ch){
    var ctx = ch.ctx;
    ctx.save();
    ctx.fillStyle = '#1d2733'; ctx.font = '600 13px ' + FONT; ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
    ch.getDatasetMeta(0).data.forEach(function(bar, i){ ctx.fillText(fmt(ch.data.datasets[0].data[i]), bar.x + 6, bar.y); });
    ctx.restore();
  }
};
function renderThemes(list, top){
  var n = list.length;
  $('c1title').textContent = 'Ten most frequent themes among ' + fmt(n) + ' filtered records' + (top.length && top.length < 10 ? ' (only ' + top.length + ' themes present)' : '');
  $('themeBody').innerHTML = top.length ? top.map(function(t, k){
    return '<tr><td><button type="button" class="linkbtn" data-t="' + k + '">' + esc(t[0]) + '</button></td><td class="num">' + fmt(t[1]) + '</td><td class="num">' + pct(t[1], n) + '</td><td>' + (t[2] ? range(t[2][0], t[2][1]) : '–') + '</td></tr>';
  }).join('') : '<tr><td colspan="4">No themes to show for this selection.</td></tr>';
  $('c1src').textContent = 'Source: ' + sourceText() + '. n = ' + fmt(n) + ' filtered records of ' + fmt(N) + '.';
  if (chart1) { chart1.destroy(); chart1 = null; }
  if (!top.length) {
    $('c1wrap').hidden = true; $('c1msg').hidden = false;
    $('c1msg').textContent = n ? 'No records in this selection carry a theme label.' : 'No records match the current filters.';
    return;
  }
  if (typeof window.Chart === 'undefined') {
    $('c1wrap').hidden = true; $('c1msg').hidden = false;
    $('c1msg').textContent = 'The chart library is not available; the table below shows the same numbers.';
    return;
  }
  $('c1msg').hidden = true; $('c1wrap').hidden = false;
  $('c1wrap').style.height = Math.max(140, top.length * 34 + 60) + 'px';
  chart1 = new window.Chart($('c1'), {
    type: 'bar',
    data: { labels: top.map(function(t){ return trunc(t[0], 46); }), datasets: [{ data: top.map(function(t){ return t[1]; }), backgroundColor: '#1f6fb2', borderWidth: 0, barPercentage: 0.7 }] },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false, animation: false,
      layout: { padding: { right: 48 } },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: {
          title: function(items){ return top[items[0].dataIndex][0]; },
          label: function(c){ return fmt(c.parsed.x) + ' records'; }
        } }
      },
      scales: {
        x: { beginAtZero: true, ticks: { maxTicksLimit: 10, precision: 0 }, grid: { color: '#e3e8ee' }, border: { display: false } },
        y: { grid: { display: false }, ticks: { autoSkip: false, color: '#1d2733' } }
      },
      onClick: function(e, els){ if (els && els.length) { addTheme(top[els[0].index][0]); } },
      onHover: function(e, els){ if (e && e.native && e.native.target) { e.native.target.style.cursor = els.length ? 'pointer' : 'default'; } }
    },
    plugins: [vlPlugin]
  });
}

/* ---------- rendering: timeline, States ---------- */
function renderTimeline(list){
  var n = list.length;
  $('c2title').textContent = 'Records per year by mechanism among ' + fmt(n) + ' filtered records';
  $('c2src').textContent = 'Source: ' + sourceText() + '. n = ' + fmt(n) + ' filtered records of ' + fmt(N) + '.';
  if (chart2) { chart2.destroy(); chart2 = null; }
  var ys = list.filter(function(o){ return o.year != null; }).map(function(o){ return o.year; });
  if (!ys.length) {
    $('c2wrap').hidden = true; $('c2msg').hidden = false; $('gaps').textContent = '';
    $('c2msg').textContent = n ? 'No records in this selection have a year.' : 'No records match the current filters.';
    return;
  }
  var lo = Math.min.apply(null, ys), hi = Math.max.apply(null, ys), years = [];
  for (var y = lo; y <= hi; y++) { years.push(y); }
  var cnt = map();
  list.forEach(function(o){ if (o.year != null) { var k = o.mech + '|' + o.year; cnt[k] = (cnt[k] || 0) + 1; } });
  var tot = map(); ys.forEach(function(v){ tot[v] = (tot[v] || 0) + 1; });
  var empty = years.filter(function(v){ return !tot[v]; });
  $('gaps').textContent = empty.length ? 'Years with no records between ' + lo + ' and ' + hi + ': ' + (empty.length > 25 ? empty.slice(0, 25).join(', ') + ' and ' + (empty.length - 25) + ' more' : empty.join(', ')) + '.' : 'Every year between ' + lo + ' and ' + hi + ' has at least one record.';
  if (typeof window.Chart === 'undefined') {
    $('c2wrap').hidden = true; $('c2msg').hidden = false;
    $('c2msg').textContent = 'The chart library is not available.';
    return;
  }
  $('c2msg').hidden = true; $('c2wrap').hidden = false;
  var ds = MECHS.map(function(m, k){
    return { label: m, backgroundColor: MECH_COLORS[k % MECH_COLORS.length], borderWidth: 0, data: years.map(function(v){ return cnt[m + '|' + v] || 0; }) };
  });
  chart2 = new window.Chart($('c2'), {
    type: 'bar',
    data: { labels: years.map(String), datasets: ds },
    options: {
      responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { position: 'top', labels: { boxWidth: 14, font: { size: 13 } } }, tooltip: { mode: 'index', intersect: false } },
      scales: {
        x: { stacked: true, grid: { display: false }, ticks: { autoSkip: true, maxRotation: 0, minRotation: 0 } },
        y: { stacked: true, beginAtZero: true, ticks: { maxTicksLimit: 10, precision: 0 }, grid: { color: '#e3e8ee' }, border: { display: false } }
      }
    }
  });
}
function renderStates(list){
  $('cname').textContent = COUNTRY;
  var m = map(), upr = 0, found = 0;
  list.forEach(function(o){
    if (o.states === null) { return; }
    upr++;
    if (o.states.length) { found++; o.states.forEach(function(s){ m[s] = (m[s] || 0) + 1; }); }
  });
  var top = Object.keys(m).sort(function(a, b){ return m[b] - m[a] || a.localeCompare(b); }).slice(0, 10);
  if (!upr) { $('statesList').innerHTML = '<li>No Universal Periodic Review records in this selection.</li>'; return; }
  $('statesList').innerHTML = top.map(function(s){ return '<li>' + esc(s) + ': ' + fmt(m[s]) + ' recommendations</li>'; }).join('') +
    '<li style="list-style:none;color:#566474;margin-top:6px">' + fmt(found) + ' of ' + fmt(upr) + ' UPR records in this selection name at least one State.</li>';
}

/* ---------- rendering: table ---------- */
function detailHtml(o){
  function tags(a, f){ return a.length ? a.map(function(x){ return '<span class="tag">' + esc(f ? f(x) : x) + '</span>'; }).join('') : '<span class="tag missing">not labelled</span>'; }
  var h = '<div><p class="full">' + hl(o.text) + '</p><dl class="labels">';
  if (o.section) { h += '<dt>Section</dt><dd>' + esc(o.section) + '</dd>'; }
  h += '<dt>Themes</dt><dd>' + tags(o.themes) + '</dd>';
  h += '<dt>SDGs</dt><dd>' + tags(o.sdgs.filter(isFinite), sdgLabel) + '</dd>';
  h += '<dt>SDG targets</dt><dd>' + tags(o.targets) + '</dd>';
  h += '<dt>Affected persons</dt><dd>' + tags(o.aff) + '</dd>';
  if (o.states !== null) { h += '<dt>Recommending State</dt><dd>' + (o.states.length ? esc(o.states.join(', ')) : 'State not found') + '</dd>'; }
  h += '</dl><div class="row"><button type="button" class="btn copy" data-i="' + o.i + '">Copy citation' + (o.para ? '' : ' (no paragraph number in this extract)') + '</button><span class="copied" role="status"></span>';
  var u = safeUrl(o.r.doc_url);
  if (u) { h += '<a class="btn ghost" href="' + esc(u) + '" target="_blank" rel="noopener">Open the UN document</a>'; }
  return h + '</div></div>';
}
function renderTable(){
  var rows = sorted(CUR);
  SORTED = rows;
  var showState = CUR.some(function(o){ return o.states !== null; });
  $('thState').hidden = !showState;
  var cols = showState ? 6 : 5;
  var upto = Math.min(shown, rows.length), h = '';
  for (var k = 0; k < upto; k++) {
    var o = rows[k], open = !!OPEN[o.i];
    h += '<tr class="main' + (open ? ' open' : '') + '" data-i="' + o.i + '"><td class="nw">' + esc(o.date) + '</td><td>' + esc(o.body) + '</td><td>' +
      link(o.r.doc_url, hl(o.symbol)) + '</td><td class="num">' + (o.para ? esc(o.para) : '–') + '</td><td><button type="button" class="toggle" aria-expanded="' + open + '">' +
      hl(firstLine(o.text)) + '</button></td>';
    if (showState) { h += '<td>' + (o.states === null ? '–' : (o.states.length ? esc(o.states.join(', ')) : 'State not found')) + '</td>'; }
    h += '</tr>';
    if (open) { h += '<tr class="detail"><td colspan="' + cols + '">' + detailHtml(o) + '</td></tr>'; }
  }
  $('tbody').innerHTML = rows.length ? h : '<tr><td colspan="' + cols + '">No records match the current filters.</td></tr>';
  $('cap').textContent = rows.length ? 'Matching records, ' + (dateDesc ? 'newest first' : 'oldest first') + '. Showing ' + fmt(upto) + ' of ' + fmt(rows.length) + ' matching rows.' : 'No records match the current filters.';
  $('dateSort').textContent = 'Date ' + (dateDesc ? '▼' : '▲');
  $('dateSort').setAttribute('aria-label', 'Date, sorted ' + (dateDesc ? 'newest' : 'oldest') + ' first. Activate to reverse.');
  $('thDate').setAttribute('aria-sort', dateDesc ? 'descending' : 'ascending');
  $('more').hidden = upto >= rows.length;
  $('tblSource').textContent = 'Source: ' + sourceText() + '. ' + fmt(rows.length) + ' rows match the filters out of ' + fmt(N) + ' records; each symbol links to the UN document.';
}

/* ---------- checks ---------- */
function item(level, title, detail){
  var lab = level === 'ok' ? '✓ Pass' : (level === 'warn' ? '! Warning' : '✗ Check failed');
  return '<li class="chk ' + level + '"><span class="mark">' + lab + '</span><div><strong>' + title + '</strong><br>' + detail + '</div></li>';
}
function countBy(fn){ var m = map(); recs.forEach(function(o){ var k = fn(o); m[k] = (m[k] || 0) + 1; }); return m; }
function sumOf(m){ var s = 0; Object.keys(m).forEach(function(k){ s += m[k]; }); return s; }
function listItems(arr2, f, cap){
  var shownItems = arr2.slice(0, cap).map(function(x){ return '<li>' + f(x) + '</li>'; }).join('');
  return '<ul>' + shownItems + (arr2.length > cap ? '<li>and ' + fmt(arr2.length - cap) + ' more</li>' : '') + '</ul>';
}
function buildStaticChecks(){
  var out = { a: [], b: [] };
  var cnt = Number(U.count);
  out.a.push(item(N === cnt ? 'ok' : 'fail', 'Record count',
    'records.length = ' + fmt(N) + '; the file\'s count field = ' + esc(U.count) + (typeof U.count === 'string' ? ' (stored as text, read as a number: ' + (isNaN(cnt) ? 'not a number' : fmt(cnt)) + ')' : '') + '.'));
  var parts = [['mechanism', function(o){ return o.mech || '(missing)'; }], ['body', function(o){ return o.body || '(missing)'; }], ['year', function(o){ return o.year == null ? '(missing)' : o.year; }]];
  var bad = false, lines = parts.map(function(p){
    var m = countBy(p[1]), s = sumOf(m), ok = s === N; if (!ok) { bad = true; }
    return 'Per ' + p[0] + ': ' + fmt(Object.keys(m).length) + ' groups sum to ' + fmt(s) + '; records ' + fmt(N) + (ok ? '' : ' (differ)') + '.';
  });
  out.a.push(item(bad ? 'fail' : 'ok', 'Partitions add up', lines.join('<br>')));
  var tm = countBy(function(o){ return o.type || '(missing)'; }), ts = sumOf(tm);
  out.a.push(item(ts === N ? 'ok' : 'fail', 'Type partition',
    Object.keys(tm).map(function(k){ return esc(k) + ' ' + fmt(tm[k]); }).join(' + ') + ' = ' + fmt(ts) + '; headline total ' + fmt(N) + '.'));

  var badLinks = recs.filter(function(o){
    var u = String(o.r.doc_url || '');
    if (u.indexOf('https://docs.un.org/') !== 0 || !o.symbol) { return true; }
    var d = u; try { d = decodeURIComponent(u); } catch (e) { d = u; }
    d = d.toLowerCase(); var s = o.symbol.toLowerCase();
    return d.slice(d.length - s.length) !== s;
  });
  out.b.push(item(badLinks.length ? 'fail' : 'ok', 'Document links',
    fmt(N - badLinks.length) + ' of ' + fmt(N) + ' records have a doc_url that starts with https://docs.un.org/ and ends with their symbol.' +
    (badLinks.length ? '<details open><summary>' + fmt(badLinks.length) + ' records fail</summary>' + listItems(badLinks, function(o){ return esc(o.symbol || '(no symbol)') + ' → ' + esc(o.r.doc_url || '(no link)'); }, 50) + '</details>' : '')));

  var pm = map(), pl = [], uprShare = null;
  recs.forEach(function(o){ var m = pm[o.mech] || (pm[o.mech] = [0, 0]); m[1]++; if (o.para) { m[0]++; } });
  Object.keys(pm).sort().forEach(function(k){
    pl.push(esc(k || '(no mechanism)') + ': ' + fmt(pm[k][0]) + ' of ' + fmt(pm[k][1]) + ' (' + pct(pm[k][0], pm[k][1]) + ')');
    if (k === UPR) { uprShare = pm[k][0] / pm[k][1]; }
  });
  out.b.push(item(uprShare !== null && uprShare < 1 ? 'warn' : 'ok', 'Paragraph numbers found',
    pl.join('<br>') + '<br>' + (uprShare === null ? 'No UPR records in the file.' : 'UPR is expected at 100%; treaty-body and Special Procedures texts often have no number.')));

  var upr = recs.filter(function(o){ return o.states !== null; });
  var noState = upr.filter(function(o){ return !o.states.length; });
  out.b.push(item(noState.length ? 'warn' : 'ok', 'Recommending States found',
    fmt(upr.length - noState.length) + ' of ' + fmt(upr.length) + ' UPR records have at least one State.' +
    (noState.length ? '<details><summary>' + fmt(noState.length) + ' UPR records without a State (what their text ends with)</summary>' + listItems(noState, function(o){
      return link(o.r.doc_url, esc(o.symbol)) + (o.para ? ' para. ' + esc(o.para) : '') + ': …' + esc(o.text.slice(-80));
    }, 100) + '</details>' : '')));

  var ids = map(), idn = 0, txt = map(), dup = 0;
  recs.forEach(function(o){
    var id = String(o.r.id); if (!ids[id]) { ids[id] = 1; idn++; }
    if (txt[o.text]) { dup++; } else { txt[o.text] = 1; }
  });
  out.b.push(item(idn === N ? 'ok' : 'fail', 'Unique ids', 'Distinct id = ' + fmt(idn) + '; records ' + fmt(N) + '.'));
  var nt = recs.filter(function(o){ return !o.themes.length; }).length, ns = recs.filter(function(o){ return !o.sdgs.length; }).length, na = recs.filter(function(o){ return !o.aff.length; }).length;
  out.b.push(item(dup ? 'warn' : 'ok', 'Duplicates and gaps',
    fmt(dup) + ' records repeat the text of an earlier record.<br>Not labelled: no themes ' + fmt(nt) + ', no SDGs ' + fmt(ns) + ', no affected persons ' + fmt(na) + ' (shown as "not labelled", never filled in).'));
  return out;
}
var STATIC = null;
function chartCheck(list, top){
  var lines = [], bad = false;
  var tableVals = Array.prototype.map.call(document.querySelectorAll('#themeBody tr'), function(tr){ return tr.cells.length > 1 ? Number(tr.cells[1].textContent.replace(/[^\d]/g, '')) : NaN; });
  var barVals = chart1 ? chart1.data.datasets[0].data : top.map(function(t){ return t[1]; });
  top.forEach(function(t, k){
    var c2 = 0;
    for (var j = 0; j < list.length; j++) { if (list[j].themes.indexOf(t[0]) >= 0) { c2++; } }
    var okRow = c2 === barVals[k] && c2 === tableVals[k];
    if (!okRow) { bad = true; lines.push(esc(t[0]) + ': bar ' + barVals[k] + ', table ' + tableVals[k] + ', recount ' + c2); }
  });
  var mx = barVals.length ? Math.max.apply(null, barVals) : 0;
  if (mx > list.length) { bad = true; lines.push('largest bar ' + fmt(mx) + ' is larger than the filtered count ' + fmt(list.length)); }
  return item(bad ? 'fail' : 'ok', 'Chart against table (current filter)',
    bad ? lines.join('<br>') : fmt(top.length) + ' bars equal a second recount of the filtered records and the ' + fmt(tableVals.length) + ' table rows; the largest bar (' + fmt(mx) + ') is not larger than the filtered count (' + fmt(list.length) + ').');
}
function renderChecks(){
  if (!STATIC) { STATIC = buildStaticChecks(); }
  $('checks').innerHTML = STATIC.a.join('') + chartCheck(CUR, TOP) + STATIC.b.join('');
}

/* ---------- sample ---------- */
function mulberry32(a){
  return function(){
    var t = a += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
function draw(){
  var seed = parseInt($('seed').value, 10);
  if (isNaN(seed)) { seed = 1; }
  $('seed').value = seed;
  var rnd = mulberry32(seed), pool = CUR.slice();
  for (var k = pool.length - 1; k > 0; k--) {
    var j = Math.floor(rnd() * (k + 1)), t = pool[k]; pool[k] = pool[j]; pool[j] = t;
  }
  sample = pool.slice(0, 10);
  verdicts = {};
  renderSample(seed);
}
function renderSample(seed){
  if (seed == null) { seed = parseInt($('seed').value, 10) || 1; }
  if (!sample.length) {
    $('cards').innerHTML = '<p class="msg">No records match the current filters, so there is nothing to sample.</p>';
  } else {
    $('cards').innerHTML = sample.map(function(o){
      return '<article class="card"><div><strong>' + link(o.r.doc_url, esc(o.symbol)) + '</strong>' + (o.para ? ', para. ' + esc(o.para) : ' (no paragraph number found)') + '</div>' +
        '<p class="full">' + esc(o.text) + '</p><div>' +
        (o.themes.length ? o.themes.map(function(t){ return '<span class="tag">' + esc(t) + '</span>'; }).join('') : '<span class="tag missing">not labelled</span>') +
        '</div><div class="vrow" role="group" aria-label="Do the themes fit this paragraph?">' +
        [['fit', 'Fits'], ['no', 'Doesn\'t fit'], ['unsure', 'Unsure']].map(function(v){
          return '<button type="button" class="btn ghost vbtn" data-i="' + o.i + '" data-v="' + v[0] + '" aria-pressed="false">' + v[1] + '</button>';
        }).join('') + '</div></article>';
    }).join('');
  }
  tally(seed);
}
function tally(seed){
  var c = { fit: 0, no: 0, unsure: 0 }, j = 0;
  sample.forEach(function(o){ var v = verdicts[o.i]; if (v) { c[v]++; j++; } });
  if (seed == null) { seed = parseInt($('seed').value, 10) || 1; }
  $('tally').textContent = 'Themes: ' + c.fit + ' fit, ' + c.no + ' don\'t, ' + c.unsure + ' unsure of ' + j + ' judged (sample of ' + sample.length + ', seed ' + seed + '). This is your judgement, not a UN label.';
  Array.prototype.forEach.call(document.querySelectorAll('.vbtn'), function(b){
    b.setAttribute('aria-pressed', verdicts[b.getAttribute('data-i')] === b.getAttribute('data-v') ? 'true' : 'false');
  });
}

/* ---------- export ---------- */
function filterLabels(){ return activeFilters().map(function(c){ return c.label; }); }
function csvCell(v){
  v = String(v == null ? '' : v);
  if (/^[=+\-@\t\r]/.test(v)) { v = "'" + v; }
  return '"' + v.replace(/"/g, '""') + '"';
}
function buildCsv(){
  var rows = sorted(CUR), fl = filterLabels();
  var lines = [
    '# Country: ' + COUNTRY,
    '# Source: ' + sourceText() + (U.source_url ? ' (' + U.source_url + ')' : ''),
    '# Built: ' + (U.built || 'not stated'),
    '# Filters: ' + (fl.length ? fl.join('; ') : 'none'),
    '# Rows: ' + rows.length + ' of ' + N,
    '# Dates are the date of the UN document. Cells starting with = + - or @ have a leading apostrophe.'
  ];
  lines.push(['Date', 'Body', 'Symbol', 'Para.', 'First line', 'Recommending State', 'Mechanism', 'Type', 'Document URL', 'Section', 'Themes', 'SDGs', 'SDG targets', 'Affected persons', 'Full text'].map(csvCell).join(','));
  rows.forEach(function(o){
    lines.push([o.date, o.body, o.symbol, o.para, firstLine(o.text), o.states === null ? '' : (o.states.length ? o.states.join('; ') : 'State not found'),
      o.mech, o.type, o.r.doc_url || '', o.section, o.themes.join('; '), o.sdgs.filter(isFinite).map(sdgLabel).join('; '), o.targets.join('; '), o.aff.join('; '), o.text].map(csvCell).join(','));
  });
  return lines.join('\r\n');
}
function download(){
  var blob = new Blob(['﻿' + buildCsv()], { type: 'text/csv;charset=utf-8' });
  var url = URL.createObjectURL(blob), a = document.createElement('a');
  a.href = url;
  a.download = 'un-recommendations-' + COUNTRY.replace(/[^A-Za-z0-9]+/g, '-').toLowerCase() + '.csv';
  document.body.appendChild(a); a.click();
  setTimeout(function(){ document.body.removeChild(a); URL.revokeObjectURL(url); }, 1000);
}
function summaryText(){
  var t = TILEINFO, fl = filterLabels(), n = t.n;
  var parts = [
    'UN human rights recommendations and observations: ' + COUNTRY + '.',
    'Selection: ' + (fl.length ? fl.join('; ') : 'no filters, all records') + '.',
    fmt(n) + ' records from ' + fmt(t.dn) + ' documents, years ' + range(t.ymin, t.ymax) + '.',
    'By type: ' + (t.types.length ? t.types.map(function(x){ return x[0] + ' ' + fmt(x[1]); }).join(', ') : 'none') + '.',
    'By mechanism: ' + t.mechs.map(function(x){ return x[0] + ' ' + fmt(x[1]) + ' records in ' + fmt(x[2]) + ' documents'; }).join('; ') + '.',
    'Ten most frequent themes (a record can carry several): ' + (TOP.length ? TOP.map(function(x, k){ return (k + 1) + '. ' + x[0] + ' ' + fmt(x[1]) + ' (' + pct(x[1], n) + ')'; }).join('; ') : 'none') + '.',
    'Source: ' + sourceText() + ', built ' + (U.built || 'date not stated') + '. Counted in the browser; dates are by document.'
  ];
  return parts.join(' ');
}
function copyText(text, done){
  function fallback(){
    var ta = document.createElement('textarea'), ok = false;
    ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta); done(ok);
  }
  if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(function(){ done(true); }, fallback); }
  else { fallback(); }
}
function flash(el, ok){
  if (!el) { return; }
  el.textContent = ok ? 'Copied' : 'Could not copy; select the text and copy it yourself';
  setTimeout(function(){ el.textContent = ''; }, ok ? 2000 : 4000);
}

/* ---------- update ---------- */
function update(){
  W = words();
  if (bodyBuiltFor !== F.mech) { buildBody(); }
  setValues();
  CUR = recs.filter(match);
  shown = PAGE;
  renderChips();
  $('showing').textContent = 'Showing ' + fmt(CUR.length) + ' of ' + fmt(N) + ' records';
  renderTiles(CUR);
  TOP = themeTop(CUR);
  renderThemes(CUR, TOP);
  renderTimeline(CUR);
  renderStates(CUR);
  renderTable();
  renderChecks();
  draw();
}

/* ---------- events ---------- */
function bind(){
  $('f-mech').addEventListener('change', function(){ F.mech = this.value; update(); });
  $('f-body').addEventListener('change', function(){ F.body = this.value; update(); });
  function years(){
    var a = Number($('f-from').value), b = Number($('f-to').value);
    if (a > b) { var t = a; a = b; b = t; }
    F.from = a; F.to = b; update();
  }
  $('f-from').addEventListener('change', years);
  $('f-to').addEventListener('change', years);
  $('f-sdg').addEventListener('change', function(){ F.sdg = this.value; update(); });
  $('f-type').addEventListener('change', function(){ F.type = this.value; update(); });
  $('f-state').addEventListener('change', function(){ F.state = this.value; update(); });
  $('f-kw').addEventListener('input', function(){
    var v = this.value;
    clearTimeout(kwTimer);
    kwTimer = setTimeout(function(){ F.kw = v; update(); }, 300);
  });
  $('reset').addEventListener('click', function(){ clearTimeout(kwTimer); resetF(); $('f-kw').value = ''; update(); });
  $('chips').addEventListener('click', function(e){
    var b = e.target.closest('.chip');
    if (!b) { return; }
    var k = b.getAttribute('data-k');
    if (k === 'mech') { F.mech = ''; }
    else if (k === 'body') { F.body = ''; }
    else if (k === 'years') { F.from = YEARS[0]; F.to = YEARS[YEARS.length - 1]; }
    else if (k === 'sdg') { F.sdg = ''; }
    else if (k === 'type') { F.type = ''; }
    else if (k === 'kw') { F.kw = ''; $('f-kw').value = ''; }
    else if (k === 'state') { F.state = ''; }
    else if (k === 'theme') { F.themes.splice(Number(b.getAttribute('data-t')), 1); }
    update();
  });
  $('themeBody').addEventListener('click', function(e){
    var b = e.target.closest('.linkbtn');
    if (b && TOP[Number(b.getAttribute('data-t'))]) { addTheme(TOP[Number(b.getAttribute('data-t'))][0]); }
  });
  $('dateSort').addEventListener('click', function(){ dateDesc = !dateDesc; renderTable(); });
  $('more').addEventListener('click', function(){ shown += PAGE; renderTable(); });
  $('tbody').addEventListener('click', function(e){
    if (e.target.closest('a')) { return; }
    var cp = e.target.closest('.copy');
    if (cp) {
      var o = recs[Number(cp.getAttribute('data-i'))], st = cp.parentNode.querySelector('.copied');
      copyText(citation(o), function(ok){ flash(st, ok); });
      return;
    }
    var tr = e.target.closest('tr.main');
    if (!tr) { return; }
    var i = Number(tr.getAttribute('data-i'));
    if (OPEN[i]) { delete OPEN[i]; } else { OPEN[i] = true; }
    renderTable();
    var btn = document.querySelector('#tbody tr[data-i="' + i + '"] .toggle');
    if (btn) { btn.focus(); }
  });
  $('drawAgain').addEventListener('click', function(){ $('seed').value = Math.floor(Math.random() * 1000000000); draw(); });
  $('drawSeed').addEventListener('click', draw);
  $('cards').addEventListener('click', function(e){
    var b = e.target.closest('.vbtn');
    if (!b) { return; }
    var i = b.getAttribute('data-i'), v = b.getAttribute('data-v');
    if (verdicts[i] === v) { delete verdicts[i]; } else { verdicts[i] = v; }
    tally();
  });
  $('dl').addEventListener('click', download);
  $('cs').addEventListener('click', function(){
    var s = summaryText();
    $('summary').value = s;
    copyText(s, function(ok){ flash($('csStatus'), ok); });
  });
}

/* ---------- start ---------- */
function init(){
  resetF();
  var docs = map(), dn = 0;
  recs.forEach(function(o){ if (!docs[o.symbol]) { docs[o.symbol] = 1; dn++; } });
  var title = 'UN human rights recommendations and observations: ' + COUNTRY;
  $('title').textContent = title;
  document.title = title;
  var src = U.source ? link(U.source_url, esc(U.source)) : 'source not stated in the file';
  $('subtitle').innerHTML = 'Source: ' + src + ' · ' + fmt(N) + ' records · ' + fmt(dn) + ' documents · ' + (YEARS.length ? range(YEARS[0], YEARS[YEARS.length - 1]) : 'years not stated') + ' · data built ' + esc(U.built || 'date not stated') + '.';
  $('footer').innerHTML = '<p>Data source: ' + src + '. Licence: not stated in the data file; check the UN terms of use before reusing the text. Data built ' + esc(U.built || 'date not stated') + '. Dates are by document.</p>' +
    '<p>Counting, filtering, sorting and charts are done by this page\'s code on the loaded file. Nothing is estimated and no model is called.</p>';
  if (!N) {
    $('showing').textContent = 'No records were loaded, so there is nothing to show.';
  }
  buildSelects();
  bind();
  update();
}
init();
})();
</script>
</body>
</html>
```
