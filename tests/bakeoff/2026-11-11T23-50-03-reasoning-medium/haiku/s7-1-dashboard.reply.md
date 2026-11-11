The dashboard reads only `WORKSHOP_DATA.uhri`, makes no network calls, and runs fourteen self-checks on its own numbers. Filters sit in the left rail, and the three tabs answer what the UN has said, which paragraph says it, and how the figures were made.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UHRI · Kenya</title>
<style>
[hidden]{display:none!important}
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--accent:#9b2335;--muted:#5f5a50;--row:#ebe5d8;
--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;--sans:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 var(--sans)}
button,input,select{font:inherit;color:inherit}
button{cursor:pointer}
a{color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.wrap{max-width:1200px;margin:0 auto;padding:20px 24px 12px}
.mono{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.muted{color:var(--muted)}
.small{font-size:14px;color:var(--muted)}
h1{font:normal 30px/1.2 var(--serif);margin:6px 0 8px}
h2{font:normal 22px/1.3 var(--serif);margin:0 0 6px}
h3{font-size:12px;margin:26px 0 8px}
.meta{margin:0 0 16px;font-size:14px;color:var(--muted)}
.layout{display:grid;grid-template-columns:250px 1fr;gap:32px;align-items:start}
.rail{position:sticky;top:12px;border-top:2px solid var(--ink);padding-top:10px}
.railTop{display:flex;justify-content:space-between;align-items:center}
.linkbtn{background:none;border:0;padding:0;color:var(--accent);text-decoration:underline;font-size:14px}
.bigN{font:normal 52px/1 var(--serif);margin:14px 0 2px}
.track{height:4px;background:var(--rule);margin:8px 0 12px}
.track i{display:block;height:100%;background:var(--accent)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
.chip{background:none;border:1px solid var(--accent);color:var(--accent);border-radius:2px;padding:2px 8px;font-size:13px}
.sec{border-top:1px solid var(--rule)}
.acc{display:flex;width:100%;justify-content:space-between;align-items:center;background:none;border:0;padding:10px 0;text-align:left;font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.acc[aria-expanded="true"]{color:var(--accent)}
.acc::after{content:"+"}
.acc[aria-expanded="true"]::after{content:"−"}
.secBody{padding:0 0 12px}
.secBody label{display:block;font-size:14px;margin:8px 0 2px}
.secBody select,.secBody input{width:100%;padding:6px;background:#fffdf8;border:1px solid var(--rule);border-radius:2px}
.hint{font-family:var(--mono);font-size:11px;color:var(--muted);display:block;margin-top:4px}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin-bottom:20px;flex-wrap:wrap}
.tabs button{background:none;border:0;border-bottom:3px solid transparent;padding:8px 12px;font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:-1px}
.tabs button[aria-selected="true"]{border-bottom-color:var(--accent);color:var(--accent)}
.hero{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:24px}
.tile{border-top:1px solid var(--rule);padding:12px 0 14px}
.num{font:normal 52px/1.05 var(--serif);margin:6px 0}
.num.sm{font-size:34px}
.how{font-size:13px;color:var(--muted);margin-top:6px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:middle}
.mechs{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
figure{margin:28px 0 0;border-top:1px solid var(--rule);padding-top:10px}
figcaption{margin-bottom:8px}
.fig{font-family:var(--mono);color:var(--accent);margin-right:8px}
.chartBox{position:relative;height:360px}
.chartBox.tl{height:320px}
.source{font-size:12px;color:var(--muted);font-family:var(--mono);margin:8px 0 0}
table{width:100%;border-collapse:collapse;font-size:15px}
caption{text-align:left;font-size:14px;color:var(--muted);padding:6px 0;caption-side:top}
th,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font:normal 12px var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.rec{cursor:pointer}
tr.rec:hover{background:var(--row)}
tr.rec td:first-child{white-space:nowrap}
td.sym a{word-break:break-word}
mark{background:#f0dc95;color:var(--ink);padding:0 1px}
.searchRow{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:10px}
.searchRow input{flex:1;min-width:240px;padding:8px 10px;font-size:16px;background:#fffdf8;border:1px solid var(--rule);border-radius:2px}
.btn{background:none;border:1px solid var(--ink);padding:7px 14px;margin:6px 8px 6px 0;border-radius:2px;text-decoration:none;display:inline-block;color:var(--ink)}
.btn:hover{border-color:var(--accent);color:var(--accent)}
td.detailCell{background:#fbf9f4;padding:18px 16px}
.bignum{font:normal 44px/1 var(--serif);color:var(--accent);margin-top:6px}
.fulltext{font-size:16px;margin:12px 0 14px;max-width:80ch;white-space:pre-wrap}
dl.labels{display:grid;grid-template-columns:max-content 1fr;gap:4px 14px;font-size:14px;margin:0 0 12px}
dl.labels dt{font-family:var(--mono);font-size:11px;text-transform:uppercase;color:var(--muted);padding-top:2px}
dl.labels dd{margin:0}
.checks{list-style:none;padding:0;margin:0}
.check{border-top:1px solid var(--rule);padding:10px 0}
.badge{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.06em;padding:1px 6px;border:1px solid currentColor;margin-left:8px;border-radius:2px}
.badge.ok{color:var(--ink)}
.badge.warn{color:#8a5a00}
.badge.fail{color:var(--accent);font-weight:bold}
.badge.note{color:var(--muted)}
.clist{font-size:13px;margin:6px 0 0;padding-left:18px;color:var(--muted)}
.statesBox{border-top:1px solid var(--rule);margin-top:20px;padding-top:10px}
footer{border-top:1px solid var(--rule);margin-top:28px;padding:12px 0;font-family:var(--mono);font-size:12px;color:var(--muted)}
ol.method li{margin-bottom:8px}
@media (max-width:860px){.layout{grid-template-columns:1fr}.rail{position:static}.hero,.mechs{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="mono muted" id="labelLine"></div>
  <h1 id="title"></h1>
  <p class="meta" id="srcLine"></p>
</header>

<div class="layout">
<aside class="rail" aria-label="Filters">
  <div class="railTop"><span class="mono">Filters</span><button class="linkbtn" id="clearAll">Clear all</button></div>
  <div class="bigN" aria-live="polite" id="matchN">0</div>
  <div class="small" id="ofN"></div>
  <div class="track" aria-hidden="true"><i id="shareBar" style="width:0"></i></div>
  <div class="chips" id="chips"></div>
  <div id="railHeads">
    <div class="sec">
      <button class="acc" id="accKw" aria-expanded="false" aria-controls="secKw">01 Keyword</button>
      <div class="secBody" id="secKw" hidden>
        <label for="kwRail">Words in the text or the symbol</label>
        <input id="kwRail" type="search" autocomplete="off">
        <span class="hint">literal match, not synonyms</span>
      </div>
    </div>
    <div class="sec">
      <button class="acc" id="accMech" aria-expanded="false" aria-controls="secMech">02 Mechanism, body, type</button>
      <div class="secBody" id="secMech" hidden>
        <label for="fMech">Mechanism</label><select id="fMech"></select>
        <label for="fBody">Body or mandate</label><select id="fBody"></select>
        <label for="fType">Type</label><select id="fType"></select>
        <div id="stateWrap"><label for="fState">Recommending State (UPR)</label><select id="fState"></select></div>
      </div>
    </div>
    <div class="sec">
      <button class="acc" id="accYears" aria-expanded="false" aria-controls="secYears">03 Years and SDG</button>
      <div class="secBody" id="secYears" hidden>
        <label for="fY0">Year from</label><select id="fY0"></select>
        <label for="fY1">Year to</label><select id="fY1"></select>
        <label for="fSdg">Sustainable Development Goal</label><select id="fSdg"></select>
      </div>
    </div>
  </div>
</aside>

<main>
  <div class="tabs" role="tablist" aria-label="Questions">
    <button role="tab" id="t0" aria-controls="p0" aria-selected="true">01 Overview</button>
    <button role="tab" id="t1" aria-controls="p1" aria-selected="false" tabindex="-1">02 Records</button>
    <button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">03 Method &amp; export</button>
  </div>

  <section role="tabpanel" id="p0" aria-labelledby="t0">
    <div class="hero">
      <div class="tile">
        <div class="mono muted">All records in the file</div>
        <div class="num" id="totalN"></div>
        <div class="small" id="typeBreak"></div>
        <div class="how">How this is computed: every record in the file, counted once; the breakdown uses the type values as the data spells them. The rail shows the filtered count.</div>
      </div>
      <div class="tile">
        <div class="mono muted">Documents</div>
        <div class="num sm" id="docsN"></div>
        <div class="how">How this is computed: distinct symbol values in the file.</div>
      </div>
      <div class="tile">
        <div class="mono muted">Years</div>
        <div class="num sm" id="yearsN"></div>
        <div class="how">How this is computed: lowest and highest year field in the file. Dated by document.</div>
      </div>
    </div>

    <h3 class="mono">By mechanism · the filtered set</h3>
    <div class="mechs" id="mechTiles"></div>
    <div class="statesBox" id="statesPanel" hidden></div>

    <figure>
      <figcaption><span class="fig">FIG.01</span><span id="fig1Title"></span></figcaption>
      <div class="chartBox" id="themeBox"><canvas id="themeChart" role="img" aria-label="Horizontal bars: the ten most frequent themes in the filtered records"></canvas></div>
      <p class="muted" id="themeEmpty" hidden>No records match the filters.</p>
      <table>
        <caption>The same ten themes as a table</caption>
        <thead><tr><th scope="col">Theme</th><th scope="col" class="n">Records</th><th scope="col" class="n">% of filtered</th><th scope="col" class="n">Years</th></tr></thead>
        <tbody id="themeBody"></tbody>
      </table>
      <p class="source">How this is computed: each theme counts once per record that carries it; a record can carry several, so the bars add up to more than the number of records. Click a bar to filter by that theme. Source: UHRI, theme labels as OHCHR gives them.</p>
    </figure>

    <figure>
      <figcaption><span class="fig">FIG.02</span><span id="fig2Title"></span></figcaption>
      <div class="chartBox tl" id="tlBox"><canvas id="tlChart" role="img" aria-label="Stacked bars: records per year, by mechanism"></canvas></div>
      <p class="muted" id="tlEmpty" hidden>No records match the filters.</p>
      <p class="source">How this is computed: records per year field, per mechanism, in the filtered set; every year from the first to the last appears, zero where there are none. Source: UHRI.</p>
    </figure>

    <h3 class="mono">Check</h3>
    <button class="acc" id="accChecks" aria-expanded="false" aria-controls="checkPanel" style="border-top:1px solid var(--rule)">Every check (0)</button>
    <div id="checkPanel" hidden>
      <p class="small">Check this dashboard: how the app checks itself. Each line gives what was compared, the values, and the result.</p>
      <ol class="checks" id="checkList"></ol>
    </div>
  </section>

  <section role="tabpanel" id="p1" aria-labelledby="t1" hidden>
    <div class="searchRow">
      <label for="kwTab" class="sr-only">Search the records</label>
      <input id="kwTab" type="search" autocomplete="off">
      <span class="hint">literal match, not synonyms</span>
    </div>
    <table>
      <caption id="recCap"></caption>
      <thead><tr>
        <th scope="col"><button class="linkbtn mono" id="dateSort" style="text-decoration:none">Date ↓</button></th>
        <th scope="col">Body</th>
        <th scope="col">Symbol</th>
        <th scope="col" class="n">Para.</th>
        <th scope="col">First line</th>
        <th scope="col">Recommending State</th>
      </tr></thead>
      <tbody id="recBody"></tbody>
    </table>
    <button class="btn" id="more" hidden>Show 50 more</button>
    <p class="source" id="recSrc"></p>
  </section>

  <section role="tabpanel" id="p2" aria-labelledby="t2" hidden>
    <h2>How each number is computed</h2>
    <ol class="method" id="method"></ol>
    <h3 class="mono">Take it with you</h3>
    <button class="btn" id="csvBtn">Download CSV of the current filter</button>
    <button class="btn" id="sumBtn">Copy summary</button>
    <span class="small" id="sumOk" role="status"></span>
    <h3 class="mono">Data and licence</h3>
    <p class="small" id="dataLine"></p>
  </section>
</main>
</div>

<footer id="footer"></footer>
</div>

<script>
(() => {
'use strict';

/* ---------- helpers ---------- */
const $ = s => document.querySelector(s);
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt = n => Number(n).toLocaleString('en-GB');
const pct = (a, b) => b ? (a / b * 100).toFixed(1) + '%' : '0.0%';
const slug = s => String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

/* ---------- data ---------- */
const D = window.WORKSHOP_DATA.uhri || {};
const COUNTRY = D.country || 'the country';
const SRC = D.source || 'UHRI';
const RAW = D.records || [];
const TOTAL = RAW.length;
const SDGN = D.sdg_names || {};
const UPR = 'Universal Periodic Review';
const MECH_COL = {[UPR]: '#c2410c', 'Treaty bodies': '#0f766e', 'Special Procedures': '#7c3aed'};
const RUN_RE = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const GROUP_RE = /\((?:[^()]|\([^()]*\))*\)/g;
const PARA_RE = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;

const ITEMS = RAW.map((r, i) => {
  const text = String(r.text || '');
  const pm = text.match(PARA_RE);
  const upr = r.mechanism === UPR;
  let states = [], stateRun = null;
  if (upr) {
    const m = text.match(RUN_RE);
    if (m) {
      stateRun = m[1].trim();
      const set = new Set();
      (m[1].match(GROUP_RE) || []).forEach(g => {
        const n = g.slice(1, -1).trim();
        if (n && !n.includes(',') && n.length <= 60) set.add(n);
      });
      states = [...set];
    }
  }
  return {
    r, i, text, upr, states, stateRun,
    para: pm ? pm[1] : null,
    year: Number(r.year),
    themes: r.themes || [],
    sdgs: (r.sdgs || []).map(Number),
    hay: (text + ' ' + (r.symbol || '')).toLowerCase()
  };
});

const YEARS = [...new Set(ITEMS.map(x => x.year).filter(Number.isFinite))].sort((a, b) => a - b);
const MINY = YEARS[0], MAXY = YEARS[YEARS.length - 1];
const MECHS = [...new Set(RAW.map(r => r.mechanism))].filter(Boolean).sort();
const TYPES = [...new Set(RAW.map(r => r.type))].filter(Boolean).sort();
const DOCS = new Set(RAW.map(r => r.symbol)).size;
const SDG_PRESENT = [...new Set(ITEMS.flatMap(x => x.sdgs))].filter(Number.isFinite).sort((a, b) => a - b);
const STATE_COUNT = new Map();
ITEMS.forEach(x => x.states.forEach(s => STATE_COUNT.set(s, (STATE_COUNT.get(s) || 0) + 1)));
const sdgName = g => SDGN[String(g)] || ('Goal ' + g);

/* ---------- state ---------- */
const F = {kw: '', mech: '', body: '', type: '', state: '', y0: MINY, y1: MAXY, sdg: '', themes: []};
let statesOpen = false, LAST = [], SHOWN = 50, DATE_DESC = true, EXPANDED = new Set();
let kwTimer = null, openSec = null, topNow = [];
let chTheme = null, chTl = null;

const words = () => F.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);

function filtered() {
  const w = words();
  return ITEMS.filter(x => {
    const r = x.r;
    if (F.mech && r.mechanism !== F.mech) return false;
    if (F.body && r.body !== F.body) return false;
    if (F.type && r.type !== F.type) return false;
    if (F.state && !x.states.includes(F.state)) return false;
    if (!(x.year >= F.y0 && x.year <= F.y1)) return false;
    if (F.sdg && !x.sdgs.includes(Number(F.sdg))) return false;
    for (const t of F.themes) if (!x.themes.includes(t)) return false;
    for (const k of w) if (!x.hay.includes(k)) return false;
    return true;
  });
}

function themeCounts(set) {
  const m = new Map();
  for (const x of set) {
    for (const t of new Set(x.themes)) {
      const e = m.get(t) || {n: 0, y0: Infinity, y1: -Infinity};
      e.n++; e.y0 = Math.min(e.y0, x.year); e.y1 = Math.max(e.y1, x.year);
      m.set(t, e);
    }
  }
  return [...m.entries()].map(([t, e]) => ({t, ...e}))
    .sort((a, b) => b.n - a.n || a.t.localeCompare(b.t)).slice(0, 10);
}

function firstLine(t) {
  if (t.length <= 120) return t;
  let c = t.slice(0, 120);
  const sp = c.lastIndexOf(' ');
  if (sp > 0) c = c.slice(0, sp);
  return c.trimEnd() + '…';
}

function hl(el, text, ws) {
  el.textContent = '';
  if (!ws.length) { el.textContent = text; return; }
  const re = new RegExp('(' + ws.slice().sort((a, b) => b.length - a.length)
    .map(w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')', 'gi');
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) el.appendChild(document.createTextNode(text.slice(last, m.index)));
    const mk = document.createElement('mark');
    mk.textContent = m[0];
    el.appendChild(mk);
    last = m.index + m[0].length;
  }
  if (last < text.length) el.appendChild(document.createTextNode(text.slice(last)));
}

function citation(x) {
  return x.para ? `${x.r.symbol}, para. ${x.para}` : String(x.r.symbol || '');
}

/* ---------- header, footer, static ---------- */
function renderHeader() {
  document.title = `UHRI · ${COUNTRY}`;
  $('#labelLine').textContent = `UHRI · ${COUNTRY}`;
  $('#title').textContent = `UN human rights recommendations and observations: ${COUNTRY}`;
  $('#srcLine').innerHTML = `<a href="${esc(D.source_url || '#')}" target="_blank" rel="noopener">${esc(SRC)}</a> · ${fmt(TOTAL)} records · ${fmt(DOCS)} documents · ${MINY}–${MAXY} · built ${esc(D.built || '')} · dated by document`;
  $('#footer').innerHTML = `Built on OHCHR UHRI data · ${fmt(TOTAL)} records · <a href="${esc(D.source_url || '#')}" target="_blank" rel="noopener">source</a>`;
  $('#dataLine').innerHTML = `Source: <a href="${esc(D.source_url || '#')}" target="_blank" rel="noopener">${esc(SRC)}</a>. Built ${esc(D.built || '')}. The file carries no licence field; see the source page for its terms. Dates are dated by document.`;
  $('#recSrc').textContent = `Source: ${SRC}, built ${D.built || ''}. Dated by document. Click a row for the full text and the citation.`;
  const steps = [
    'All records in the file are counted once; the headline breakdown uses the type values as the data spells them.',
    'Documents are the distinct symbols, and years run from the lowest to the highest year field; dates are dated by document, not by the day a recommendation was made.',
    'Filters combine with AND: mechanism, body and type match exactly; years are inclusive; the SDG filter matches a goal in a record’s SDG list; keyword is literal, and every word must occur in the text or the symbol.',
    'Theme counts count each theme once per record, so the bars add up to more than the number of records; percentages are of records, not of theme labels.',
    'A paragraph number is the number at the start of the text (for example 71 or 144.43); a recommending State is a name in the last parentheses of a UPR text; the text itself is never changed.',
    'Nothing is estimated and no model is called; the only things that leave the page are the clipboard write and the CSV you download.'
  ];
  $('#method').innerHTML = steps.map(s => `<li>${esc(s)}</li>`).join('');
}

/* ---------- filter controls ---------- */
function fillSelects() {
  const cnt = key => { const m = new Map(); RAW.forEach(r => m.set(r[key], (m.get(r[key]) || 0) + 1)); return m; };
  const mc = cnt('mechanism'), tc = cnt('type');
  $('#fMech').innerHTML = '<option value="">All mechanisms</option>' +
    MECHS.map(m => `<option value="${esc(m)}">${esc(m)} (${fmt(mc.get(m))})</option>`).join('');
  $('#fType').innerHTML = '<option value="">All types</option>' +
    TYPES.map(t => `<option value="${esc(t)}">${esc(t)} (${fmt(tc.get(t))})</option>`).join('');
  const yo = YEARS.map(y => `<option value="${y}">${y}</option>`).join('');
  $('#fY0').innerHTML = yo;
  $('#fY1').innerHTML = yo;
  $('#fSdg').innerHTML = '<option value="">All goals</option>' +
    SDG_PRESENT.map(g => `<option value="${g}">${g} · ${esc(sdgName(g))}</option>`).join('');
  const st = [...STATE_COUNT.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  $('#fState').innerHTML = '<option value="">All States</option>' +
    st.map(([s, n]) => `<option value="${esc(s)}">${esc(s)} (${fmt(n)})</option>`).join('');
  $('#stateWrap').hidden = !st.length;
}

function populateBody() {
  const m = new Map();
  RAW.forEach(r => { if (!F.mech || r.mechanism === F.mech) m.set(r.body, (m.get(r.body) || 0) + 1); });
  const list = [...m.entries()].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0])));
  if (F.body && !m.has(F.body)) F.body = '';
  $('#fBody').innerHTML = '<option value="">All bodies</option>' +
    list.map(([b, n]) => `<option value="${esc(b)}">${esc(b)} (${fmt(n)})</option>`).join('');
  $('#fBody').value = F.body;
}

function syncControls() {
  populateBody();
  $('#fMech').value = F.mech;
  $('#fType').value = F.type;
  $('#fState').value = F.state;
  $('#fY0').value = F.y0;
  $('#fY1').value = F.y1;
  $('#fSdg').value = F.sdg;
}

function syncKw() {
  ['#kwRail', '#kwTab'].forEach(s => { const el = $(s); if (el.value !== F.kw) el.value = F.kw; });
}

function setKwDeferred(v) {
  clearTimeout(kwTimer);
  kwTimer = setTimeout(() => { F.kw = v; syncKw(); render(); }, 300);
}

function chipList() {
  const c = [];
  if (F.kw.trim()) c.push({t: `Keyword: “${F.kw.trim()}”`, off: () => { F.kw = ''; clearTimeout(kwTimer); }});
  if (F.mech) c.push({t: `Mechanism: ${F.mech}`, off: () => { F.mech = ''; F.body = ''; }});
  if (F.body) c.push({t: `Body: ${F.body}`, off: () => { F.body = ''; }});
  if (F.type) c.push({t: `Type: ${F.type}`, off: () => { F.type = ''; }});
  if (F.state) c.push({t: `State: ${F.state}`, off: () => { F.state = ''; }});
  if (F.y0 !== MINY || F.y1 !== MAXY) c.push({t: `Years ${F.y0}–${F.y1}`, off: () => { F.y0 = MINY; F.y1 = MAXY; }});
  if (F.sdg) c.push({t: `SDG ${F.sdg}: ${sdgName(F.sdg)}`, off: () => { F.sdg = ''; }});
  F.themes.forEach(t => c.push({t: `Theme: ${t}`, off: () => { F.themes = F.themes.filter(z => z !== t); }}));
  return c;
}

function renderChips() {
  const box = $('#chips');
  box.innerHTML = '';
  const list = chipList();
  if (!list.length) { box.innerHTML = '<span class="small">No filters applied</span>'; return; }
  list.forEach(c => {
    const b = document.createElement('button');
    b.className = 'chip';
    b.textContent = c.t + '  ×';
    b.setAttribute('aria-label', 'Remove filter: ' + c.t);
    b.onclick = () => { c.off(); render(); };
    box.appendChild(b);
  });
}

function renderRail(set) {
  $('#matchN').textContent = fmt(set.length);
  $('#ofN').textContent = `of ${fmt(TOTAL)} in the file`;
  $('#shareBar').style.width = (TOTAL ? set.length / TOTAL * 100 : 0).toFixed(2) + '%';
}

/* ---------- overview ---------- */
function toggleStates() {
  statesOpen = !statesOpen;
  const b = document.querySelector('#statesBtn');
  if (b) b.setAttribute('aria-expanded', String(statesOpen));
  renderStates(LAST);
}

function renderStates(set) {
  const p = $('#statesPanel');
  p.hidden = !statesOpen;
  if (!statesOpen) return;
  const upr = set.filter(x => x.upr);
  const m = new Map();
  upr.forEach(x => x.states.forEach(s => m.set(s, (m.get(s) || 0) + 1)));
  const rows = [...m.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 10);
  p.innerHTML = `<h3 class="mono">Ten States that made most recommendations to ${esc(COUNTRY)}</h3>
    <p class="small">How this is computed: a record that names two States counts once for each; the count is recommendations, not influence. ${fmt(upr.length)} UPR records in the filtered set.</p>
    <table><thead><tr><th scope="col">Recommending State</th><th scope="col" class="n">Records</th></tr></thead>
    <tbody>${rows.map(([s, n]) => `<tr><td>${esc(s)}</td><td class="n">${fmt(n)}</td></tr>`).join('') || '<tr><td colspan="2" class="muted">No States in the filtered set.</td></tr>'}</tbody></table>`;
}

function renderOverview(set) {
  $('#totalN').textContent = fmt(TOTAL);
  const tc = new Map();
  RAW.forEach(r => tc.set(r.type, (tc.get(r.type) || 0) + 1));
  $('#typeBreak').textContent = [...tc.entries()].sort((a, b) => b[1] - a[1])
    .map(([k, v]) => `${fmt(v)} ${k}`).join(' · ');
  $('#docsN').textContent = fmt(DOCS);
  $('#yearsN').textContent = `${MINY}–${MAXY}`;

  const box = $('#mechTiles');
  box.innerHTML = '';
  MECHS.forEach(m => {
    const s = set.filter(x => x.r.mechanism === m);
    const docs = new Set(s.map(x => x.r.symbol)).size;
    const latest = s.length ? Math.max(...s.map(x => x.year)) : '–';
    const div = document.createElement('div');
    div.className = 'tile';
    div.innerHTML = `<div class="mono"><span class="dot" style="background:${MECH_COL[m] || '#6b645a'}"></span>${esc(m)}</div>
      <div class="num sm">${fmt(s.length)}</div>
      <div class="small">${fmt(docs)} documents · latest year ${latest} · ${pct(s.length, set.length)} of the filtered set</div>
      <div class="how">How this is computed: records of this mechanism in the filtered set; documents are distinct symbols.</div>`;
    if (m === UPR) {
      const b = document.createElement('button');
      b.className = 'linkbtn';
      b.id = 'statesBtn';
      b.textContent = 'see the States';
      b.setAttribute('aria-expanded', String(statesOpen));
      b.setAttribute('aria-controls', 'statesPanel');
      b.onclick = toggleStates;
      div.appendChild(b);
    }
    box.appendChild(div);
  });

  renderStates(set);
  renderThemes(set);
  renderTimeline(set);
  renderChecks(set);
}

const endLabels = {
  id: 'endLabels',
  afterDatasetsDraw(c) {
    const meta = c.getDatasetMeta(0), v = c.data.datasets[0].data, ctx = c.ctx;
    ctx.save();
    ctx.fillStyle = '#1d1b18';
    ctx.font = '13px system-ui, sans-serif';
    ctx.textBaseline = 'middle';
    meta.data.forEach((b, i) => ctx.fillText(fmt(v[i]), b.x + 6, b.y));
    ctx.restore();
  }
};

function addTheme(t) {
  if (!F.themes.includes(t)) F.themes.push(t);
  render();
}

function renderThemes(set) {
  const top = themeCounts(set);
  topNow = top;
  const has = set.length > 0;
  $('#fig1Title').textContent = `Ten most frequent themes among ${fmt(set.length)} filtered records`;
  $('#themeEmpty').hidden = has;
  $('#themeBox').hidden = !has;
  if (chTheme) { chTheme.destroy(); chTheme = null; }
  const tb = $('#themeBody');
  tb.innerHTML = '';
  if (!has) return;
  top.forEach(t => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${esc(t.t)}</td><td class="n">${fmt(t.n)}</td><td class="n">${pct(t.n, set.length)}</td><td class="n">${t.y0 === t.y1 ? t.y0 : t.y0 + '–' + t.y1}</td>`;
    tb.appendChild(tr);
  });
  const max = top[0].n;
  chTheme = new Chart($('#themeChart'), {
    type: 'bar',
    plugins: [endLabels],
    data: {
      labels: top.map(t => t.t),
      datasets: [{data: top.map(t => t.n), backgroundColor: 'rgba(155,35,53,0.8)', borderWidth: 0, barThickness: 18}]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      layout: {padding: {right: 44}},
      plugins: {legend: {display: false}, tooltip: {callbacks: {label: c => `${fmt(c.parsed.x)} records`}}},
      scales: {
        x: {beginAtZero: true, suggestedMax: max * 1.1, grid: {display: false}, ticks: {precision: 0}},
        y: {grid: {display: false}, ticks: {font: {size: 13}, color: '#1d1b18', autoSkip: false}}
      },
      onClick: (e, els) => { if (els.length) addTheme(topNow[els[0].index].t); }
    }
  });
}

function renderTimeline(set) {
  if (chTl) { chTl.destroy(); chTl = null; }
  const has = set.length > 0;
  $('#fig2Title').textContent = `Records per year by mechanism, ${fmt(set.length)} filtered records`;
  $('#tlEmpty').hidden = has;
  $('#tlBox').hidden = !has;
  if (!has) return;
  const y0 = Math.min(...set.map(x => x.year)), y1 = Math.max(...set.map(x => x.year));
  const years = [];
  for (let y = y0; y <= y1; y++) years.push(y);
  const datas