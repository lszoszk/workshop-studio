```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UHRI · Kenya</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--muted:#5d564b;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--ink)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.label,.fig-no{font:600 11px/1.2 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
h1{font:400 30px/1.2 var(--serif);margin:.25em 0 .1em}
h2{font:400 22px/1.25 var(--serif);margin:.2em 0 .4em}
.hd{padding:18px 24px 12px;border-bottom:1px solid var(--rule)}
.meta{margin:.4em 0 0;font-size:14px;color:var(--muted)}
.layout{display:grid;grid-template-columns:260px 1fr;min-height:72vh}
.rail{border-right:1px solid var(--rule);padding:16px 18px}
.rail-head{display:flex;justify-content:space-between;align-items:center}
button{font:inherit;color:inherit;cursor:pointer}
.link-btn{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;font-size:14px}
.bignum{font:400 48px/1 var(--serif);margin:14px 0 4px;color:var(--ink)}
.sub{font-size:13px;color:var(--muted)}
.bar{height:6px;background:var(--rule);margin:10px 0 12px}
.bar>div{height:100%;background:var(--red);width:0}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.chip{background:none;border:1px solid var(--red);color:var(--red);border-radius:12px;padding:2px 9px;font-size:13px}
.acc{border-top:1px solid var(--rule);margin-top:8px}
.acc-h{display:flex;justify-content:space-between;width:100%;background:none;border:0;border-bottom:1px solid var(--rule);padding:10px 0;font:600 11px/1.2 var(--mono);letter-spacing:.08em;text-transform:uppercase;text-align:left}
.acc-h[aria-expanded=true]{color:var(--red)}
.acc-b{padding:10px 0 14px}
.acc-b label{display:block;font-size:13px;color:var(--muted);margin:8px 0 3px}
.acc-b input,.acc-b select,.search input,.ctl select{width:100%;padding:6px;font:inherit;background:#fffdf8;border:1px solid var(--rule);color:var(--ink)}
.hint{font:11px/1.3 var(--mono);color:var(--muted);margin-top:4px}
main{padding:0 24px 24px;min-width:0}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin:0 -24px;padding:0 24px}
.tab{font:500 12px var(--mono);text-transform:uppercase;letter-spacing:.06em;background:none;border:0;padding:12px 10px;color:var(--muted);border-bottom:3px solid transparent}
.tab[aria-selected=true]{color:var(--red);border-color:var(--red)}
.panel{padding-top:18px}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px;margin-bottom:20px}
.tile{border-top:1px solid var(--ink);padding-top:8px}
.tl{font-size:14px;margin-bottom:4px;display:flex;align-items:center;gap:6px}
.tn{font:400 46px/1.05 var(--serif)}
.tm{font-size:13px;color:var(--muted)}
.note{font-size:12px;color:var(--muted);margin-top:6px}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block}
.fig{margin:26px 0 10px;border-top:1px solid var(--rule);padding-top:10px}
.src{font-size:12px;color:var(--muted);margin-top:6px}
.chart-wrap{position:relative;height:340px}
.msg{padding:30px 0;color:var(--muted);font-style:italic}
table{width:100%;border-collapse:collapse;font-size:14px}
caption{caption-side:top;text-align:left;font-size:13px;color:var(--muted);padding:6px 0;font-family:var(--mono)}
th,td{padding:7px 8px;border-bottom:1px solid var(--rule);text-align:left;vertical-align:top}
th{font-weight:600;font-size:12px;letter-spacing:.04em;color:var(--muted)}
th button{background:none;border:0;padding:0;font:inherit;letter-spacing:inherit;color:inherit;text-decoration:underline}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
tr.row{cursor:pointer}
tr.row:hover td{background:#ece6d8}
mark{background:#efe2c4;color:inherit;padding:0 1px}
.det td{background:#fffdf8}
.det-in{padding:8px 4px 10px;max-width:880px}
.pn{font:400 34px/1 var(--serif);color:var(--red);margin-bottom:8px}
.full{white-space:pre-wrap;font-size:16px;margin:0 0 12px}
dl.lab{display:grid;grid-template-columns:130px 1fr;gap:4px 10px;font-size:14px;margin:0 0 12px}
dl.lab dt{color:var(--muted)}
dl.lab dd{margin:0}
.btn{background:none;border:1px solid var(--ink);padding:6px 12px;margin:4px 6px 4px 0;font-size:14px}
.btn:hover{background:var(--ink);color:var(--paper)}
.chk{border-bottom:1px solid var(--rule);padding:9px 0;font-size:14px}
.ck-n{font-weight:600}
.ck-s{font:600 12px var(--mono);text-transform:uppercase;letter-spacing:.05em}
.s-pass{color:#166534}.s-fail{color:var(--red)}.s-warn{color:#b45309}.s-info{color:var(--muted)}
.det-list{font:12px/1.5 var(--mono);color:var(--muted);margin-top:4px;word-break:break-word}
.ft{border-top:1px solid var(--rule);padding:10px 24px;font:12px var(--mono);color:var(--muted)}
.ft a{color:var(--muted)}
.prose p{max-width:760px}
@media (max-width:820px){.layout{grid-template-columns:1fr}.rail{border-right:0;border-bottom:1px solid var(--rule)}}
</style>
</head>
<body>
<header class="hd">
  <div class="label" id="lbl"></div>
  <h1 id="ttl"></h1>
  <p class="meta" id="meta"></p>
</header>

<div class="layout">
  <aside class="rail" aria-label="Filters">
    <div class="rail-head"><span class="label">Filters</span><button class="link-btn" id="clearAll">Clear all</button></div>
    <div class="bignum" aria-live="polite"><span id="matchN">0</span></div>
    <div class="sub"><span id="matchTxt">matching records</span> · of <span id="fileN"></span> in the file</div>
    <div class="bar"><div id="barFill"></div></div>
    <div class="chips" id="chips"></div>
    <div class="acc" id="acc">
      <button class="acc-h" id="acc0" aria-expanded="false" aria-controls="pan0"><span>01 Keyword</span><span>+</span></button>
      <div class="acc-b" id="pan0" hidden>
        <label for="kw">Words in the text or symbol</label>
        <input id="kw" type="search" autocomplete="off" placeholder="e.g. torture">
        <div class="hint">literal match, not synonyms</div>
      </div>
      <button class="acc-h" id="acc1" aria-expanded="false" aria-controls="pan1"><span>02 Mechanism, body, type</span><span>+</span></button>
      <div class="acc-b" id="pan1" hidden>
        <label for="s-mech">Mechanism</label><select id="s-mech"></select>
        <label for="s-body">Body or mandate</label><select id="s-body"></select>
        <label for="s-type">Type</label><select id="s-type"></select>
        <div id="stateWrap"><label for="s-state">Recommending State (UPR)</label><select id="s-state"></select></div>
      </div>
      <button class="acc-h" id="acc2" aria-expanded="false" aria-controls="pan2"><span>03 Years and SDG</span><span>+</span></button>
      <div class="acc-b" id="pan2" hidden>
        <label for="s-yf">Year from</label><select id="s-yf"></select>
        <label for="s-yt">Year to</label><select id="s-yt"></select>
        <label for="s-sdg">Sustainable Development Goal</label><select id="s-sdg"></select>
      </div>
    </div>
  </aside>

  <main>
    <div class="tabs" role="tablist" aria-label="Sections">
      <button class="tab" role="tab" id="t0" aria-controls="p0" aria-selected="true">01 Overview</button>
      <button class="tab" role="tab" id="t1" aria-controls="p1" aria-selected="false" tabindex="-1">02 Records</button>
      <button class="tab" role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">03 Method &amp; export</button>
    </div>

    <section class="panel" role="tabpanel" id="p0" aria-labelledby="t0">
      <h2>What has the UN said, how much, and when?</h2>
      <div id="overview"></div>
      <div class="fig"><div class="fig-no">FIG.01</div>
        <h2 id="fig1Title" style="font-size:18px"></h2>
        <div id="themeMsg" class="msg" hidden>No records match</div>
        <div class="chart-wrap" id="fig1wrap"><canvas id="fig1" role="img" aria-label="Ten most frequent themes"></canvas></div>
        <div class="src">A record can carry several themes, so the bars add up to more than n. Percentages are of records, not of labels. Click a bar to filter by it. Source: UHRI, <span id="src1"></span>.</div>
        <table id="themeTable" style="margin-top:10px"></table>
      </div>
      <div class="fig"><div class="fig-no">FIG.02</div>
        <h2 id="fig2Title" style="font-size:18px"></h2>
        <div id="timeMsg" class="msg" hidden>No records match</div>
        <div class="chart-wrap" id="fig2wrap"><canvas id="fig2" role="img" aria-label="Records per year by mechanism"></canvas></div>
        <div class="src">Every year from first to last appears; empty years are gaps. Source: UHRI, <span id="src2"></span>.</div>
      </div>
      <div style="margin-top:22px">
        <button class="acc-h" id="chkBtn" aria-expanded="false" aria-controls="chkPanel" style="border:1px solid var(--rule);padding:10px 12px;font-size:12px"><span id="chkLbl">Every check</span><span>+</span></button>
        <div id="chkPanel" hidden>
          <p class="hint" style="margin:10px 0">How the app checks itself: each line compares two values computed by separate loops.</p>
          <div id="checks"></div>
        </div>
      </div>
    </section>

    <section class="panel" role="tabpanel" id="p1" aria-labelledby="t1" hidden>
      <h2>Which paragraph says it, and in which UN document?</h2>
      <div class="search" style="margin-bottom:10px"><input id="q" type="search" autocomplete="off" aria-label="Search records" placeholder="Search records, e.g. torture"></div>
      <div class="hint" style="margin:-6px 0 10px">literal match, not synonyms · click a row to read the full paragraph</div>
      <div style="overflow-x:auto">
      <table id="recTable">
        <caption id="recCap"></caption>
        <thead><tr>
          <th scope="col"><button id="dateSort" type="button">Date ↓</button></th>
          <th scope="col">Body</th>
          <th scope="col">Symbol</th>
          <th scope="col" class="num">Para.</th>
          <th scope="col">First line</th>
          <th scope="col">Recommending State</th>
        </tr></thead>
        <tbody id="recBody"></tbody>
      </table>
      </div>
      <p style="margin-top:10px"><button class="btn" id="more" type="button">Show 50 more</button></p>
      <div class="src">Source: UHRI, <span id="src3"></span>. Dates are the document's date, not the date a recommendation was made or accepted.</div>
    </section>

    <section class="panel" role="tabpanel" id="p2" aria-labelledby="t2" hidden>
      <h2>How was this made, and how do I take it with me?</h2>
      <div class="prose">
        <p>The matching count is the number of records in the file that pass every active filter, combined with AND. The file's own total is <code>records.length</code>, checked against the file's stated count.</p>
        <p>Themes: each record counts once for each theme it carries; the top ten are ranked by count, ties alphabetical. Percentages are of matching records. A year range shows when each theme's records were dated.</p>
        <p>Paragraph numbers are the number at the start of each text. For UPR records, the recommending States are the names in parentheses at the end of the text; a record counts once for each State it names.</p>
        <p>Nothing is estimated and no model is called. Every count is a loop over the records in the browser. Dates are the document's date.</p>
        <p>Keyword search is literal: "torture" does not find "ill-treatment".</p>
      </div>
      <p style="margin-top:14px">
        <button class="btn" id="csvBtn" type="button">Download CSV of the current filter</button>
        <button class="btn" id="sumBtn" type="button">Copy summary</button>
        <span id="expStatus" class="hint" role="status"></span>
      </p>
      <div class="label" style="margin-top:18px">Data source</div>
      <p id="srcLine" style="font-size:14px"></p>
    </section>
  </main>
</div>

<footer class="ft" id="ft"></footer>

<script>
(function(){
const D = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.uhri) || {records:[]};
const COUNTRY = D.country || 'the country';
const MECH_ORDER = ['Universal Periodic Review','Treaty bodies','Special Procedures'];
const MCOL = {'Universal Periodic Review':'#c2410c','Treaty bodies':'#0f766e','Special Procedures':'#7c3aed'};
const TRAIL = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const GROUP = /\((?:[^()]|\([^()]*\))*\)/g;
const PARA = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const escRe = s => s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const fmt = n => Number(n).toLocaleString('en');
const $ = id => document.getElementById(id);

// ---- prepare records (original order kept in _i) ----
const R = (D.records || []).map((r, i) => {
  const text = r.text || '';
  const m = text.match(PARA);
  let states = null;
  if (r.mechanism === 'Universal Periodic Review') {
    states = [];
    const t = text.match(TRAIL);
    if (t) {
      for (const g of (t[1].match(GROUP) || [])) {
        const s = g.slice(1, -1).trim();
        if (s && !s.includes(',') && s.length <= 60 && !states.includes(s)) states.push(s);
      }
    }
  }
  return Object.assign({}, r, {
    _i: i, _para: m ? m[1] : null, _states: states,
    _hay: ((r.symbol || '') + ' ' + text).toLowerCase(),
    _sdgs: (r.sdgs || []).map(Number), _themes: r.themes || []
  });
});
const YEARS = R.map(r => r.year).filter(Number.isFinite);
const YMIN = YEARS.length ? Math.min(...YEARS) : '—';
const YMAX = YEARS.length ? Math.max(...YEARS) : '—';
const DYEARS = [...new Set(YEARS)].sort((a, b) => a - b);
const MECHS = [...new Set(R.map(r => r.mechanism))].sort((a, b) =>
  ((MECH_ORDER.indexOf(a) + 1) || 99) - ((MECH_ORDER.indexOf(b) + 1) || 99));
const TYPES = [...new Set(R.map(r => r.type))].sort();
const SDG_NAMES = D.sdg_names || {};
const SDGS = [...new Set(R.flatMap(r => r._sdgs))].sort((a, b) => a - b);
const STATE_COUNT = {};
R.forEach(r => (r._states || []).forEach(s => STATE_COUNT[s] = (STATE_COUNT[s] || 0) + 1));
const STATES = Object.keys(STATE_COUNT).sort((a, b) => STATE_COUNT[b] - STATE_COUNT[a] || a.localeCompare(b));
const DOCS_FILE = new Set(R.map(r => r.symbol)).size;

// ---- state ----
const F = {kw:'', mech:'', body:'', type:'', state:'', yf:'', yt:'', sdg:'', themes:[]};
let M = [], themeTop = [], shown = 50, asc = false, expanded = new Set(), chipCache = [], openAcc = -1, stOpen = false;

function passes(r){
  if (F.kw) { for (const w of F.kw.split(/\s+/)) if (w && !r._hay.includes(w)) return false; }
  if (F.mech && r.mechanism !== F.mech) return false;
  if (F.body && r.body !== F.body) return false;
  if (F.type && r.type !== F.type) return false;
  if (F.state && !(r._states && r._states.includes(F.state))) return false;
  if (F.yf && r.year < Number(F.yf)) return false;
  if (F.yt && r.year > Number(F.yt)) return false;
  if (F.sdg && !r._sdgs.includes(Number(F.sdg))) return false;
  for (const t of F.themes) if (!r._themes.includes(t)) return false;
  return true;
}
function recompute(){ M = R.filter(passes); themeTop = themeStats(M); }

function themeStats(list){
  const map = new Map();
  for (const r of list) for (const t of r._themes) {
    let s = map.get(t);
    if (!s) { s = {t, n:0, y0:Infinity, y1:-Infinity}; map.set(t, s); }
    s.n++; s.y0 = Math.min(s.y0, r.year); s.y1 = Math.max(s.y1, r.year);
  }
  return [...map.values()].sort((a, b) => b.n - a.n || a.t.localeCompare(b.t)).slice(0, 10);
}
function describe(){ return chipList().map(c => c.label).join(', '); }

function chipList(){
  const out = [];
  if (F.kw) out.push({label:'“' + F.kw + '”', remove:() => F.kw = ''});
  if (F.mech) out.push({label:F.mech, remove:() => { F.mech = ''; }});
  if (F.body) out.push({label:'Body: ' + F.body, remove:() => F.body = ''});
  if (F.type) out.push({label:'Type: ' + F.type, remove:() => F.type = ''});
  if (F.state) out.push({label:'State: ' + F.state, remove:() => F.state = ''});
  if (F.yf || F.yt) out.push({label:'Years ' + (F.yf || YMIN) + '–' + (F.yt || YMAX), remove:() => { F.yf = ''; F.yt = ''; }});
  if (F.sdg) out.push({label:'SDG ' + F.sdg + ' ' + (SDG_NAMES[F.sdg] || ''), remove:() => F.sdg = ''});
  F.themes.forEach(t => out.push({label:'Theme: ' + t, remove:() => { F.themes = F.themes.filter(x => x !== t); }}));
  return out;
}

// ---- controls ----
function opt(v, label){ const o = document.createElement('option'); o.value = v; o.textContent = label; return o; }
function fillStatic(){
  const mech = $('s-mech'); mech.append(opt('', 'All mechanisms'));
  MECHS.forEach(m => mech.append(opt(m, m)));
  const type = $('s-type'); type.append(opt('', 'All types'));
  TYPES.forEach(t => type.append(opt(t, t)));
  const yf = $('s-yf'), yt = $('s-yt');
  yf.append(opt('', 'any')); yt.append(opt('', 'any'));
  DYEARS.forEach(y => { yf.append(opt(y, y)); yt.append(opt(y, y)); });
  const sdg = $('s-sdg'); sdg.append(opt('', 'All goals'));
  SDGS.forEach(g => sdg.append(opt(g, g + '. ' + (SDG_NAMES[g] || 'Goal ' + g))));
  const st = $('s-state'); st.append(opt('', 'All States (' + STATES.length + ' found)'));
  STATES.forEach(s => st.append(opt(s, s + ' (' + STATE_COUNT[s] + ')')));
  if (!STATES.length) $('stateWrap').hidden = true;
}
function fillBody(){
  const sel = $('s-body'); sel.innerHTML = '';
  sel.append(opt('', 'All bodies'));
  const cnt = {};
  R.forEach(r => { if (!F.mech || r.mechanism === F.mech) cnt[r.body] = (cnt[r.body] || 0) + 1; });
  Object.keys(cnt).sort().forEach(b => sel.append(opt(b, b + ' (' + cnt[b] + ')')));
  if (F.body && !cnt[F.body]) F.body = '';
  sel.value = F.body;
}
function syncControls(){
  $('kw').value = F.kw; $('q').value = F.kw;
  $('s-mech').value = F.mech; fillBody();
  $('s-type').value = F.type; $('s-state').value = F.state;
  $('s-yf').value = F.yf; $('s-yt').value = F.yt; $('s-sdg').value = F.sdg;
}
function changed(){ shown = 50; expanded.clear(); renderAll(); }

let kwT = null;
function onKw(el){
  const other = el.id === 'kw' ? 'q' : 'kw';
  const raw = el.value;
  clearTimeout(kwT);
  kwT = setTimeout(() => {
    F.kw = raw.trim().toLowerCase();
    $(other).value = raw;
    changed();
  }, 300);
}

// ---- rail ----
function renderRail(){
  $('matchN').textContent = fmt(M.length);
  $('matchTxt').textContent = M.length === 1 ? 'matching record' : 'matching records';
  $('fileN').textContent = fmt(R.length);
  $('barFill').style.width = (R.length ? M.length / R.length * 100 : 0) + '%';
  chipCache = chipList();
  $('chips').innerHTML = chipCache.map((c, i) =>
    '<button class="chip" type="button" data-chip="' + i + '" aria-label="Remove filter ' + esc(c.label) + '">' + esc(c.label) + ' ×</button>').join('');
}

// ---- tabs and accordion ----
const tabs = [...document.querySelectorAll('[role=tab]')];
const panels = ['p0','p1','p2'].map(id => $(id));
function showTab(i){
  tabs.forEach((t, k) => { t.setAttribute('aria-selected', k === i); t.tabIndex = k === i ? 0 : -1; });
  panels.forEach((p, k) => p.hidden = k !== i);
  $('acc').hidden = i === 2;
  if (i === 2) setOpen(-1);
}
function setOpen(k){
  openAcc = k;
  [0,1,2].forEach(j => {
    $('acc' + j).setAttribute('aria-expanded', j === k);
    $('pan' + j).hidden = j !== k;
  });
}

// ---- records table ----
function sorted(list){
  const s = list.slice().sort((a, b) => {
    const d = (b.date || '').localeCompare(a.date || ''); if (d) return d;
    const bo = (a.body || '').localeCompare(b.body || ''); if (bo) return bo;
    const pa = a._para == null ? Infinity : parseFloat(a._para);
    const pb = b._para == null ? Infinity : parseFloat(b._para);
    if (pa !== pb) return pa < pb ? -1 : 1;
    return a._i - b._i;
  });
  return asc ? s.reverse() : s;
}
function firstLine(t){
  if (t.length <= 120) return t;
  const cut = t.slice(0, 120); const sp = cut.lastIndexOf(' ');
  return (sp > 60 ? cut.slice(0, sp) : cut) + '…';
}
function hl(s){
  const words = F.kw.split(/\s+/).filter(Boolean);
  if (!words.length) return esc(s);
  const re = new RegExp('(' + words.map(escRe).join('|') + ')', 'gi');
  return s.split(re).map((p, i) => i % 2 ? '<mark>' + esc(p) + '</mark>' : esc(p)).join('');
}
function stateCell(r){
  if (r.mechanism !== 'Universal Periodic Review') return '—';
  return r._states && r._states.length ? esc(r._states.join('; ')) : 'State not found';
}
function renderTable(){
  const list = sorted(M);
  const rows = list.slice(0, shown);
  $('dateSort').textContent = asc ? 'Date ↑' : 'Date ↓';
  $('recCap').textContent = M.length
    ? fmt(M.length) + ' of ' + fmt(R.length) + ' records match · showing ' + fmt(rows.length) + ' · ' + (asc ? 'oldest first' : 'newest first')
    : 'No records match';
  let h = '';
  for (const r of rows) {
    const open = expanded.has(r._i);
    h += '<tr class="row" tabindex="0" data-id="' + r._i + '" aria-expanded="' + open + '">' +
      '<td>' + esc(r.date) + '</td><td>' + esc(r.body) + '</td><td>' +
      (r.doc_url ? '<a href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol) + '</a>' : esc(r.symbol)) +
      '</td><td class="num">' + (r._para ? esc(r._para) : '—') + '</td><td>' + hl(firstLine(r.text || '')) +
      '</td><td>' + stateCell(r) + '</td></tr>';
    if (open) h += detail(r);
  }
  $('recBody').innerHTML = h;
  $('more').hidden = list.length <= shown;
}
function detail(r){
  const p = r._para;
  const names = SDG_NAMES;
  const sdgTxt = r._sdgs.length ? r._sdgs.map(g => g + ' ' + esc(names[g] || '')).join('; ') : 'not labelled';
  const cite = r.symbol + (p ? ', para. ' + p : '');
  const label = p ? 'Copy citation' : 'Copy symbol (no paragraph number in this extract)';
  const row = (k, v) => '<dt>' + k + '</dt><dd>' + v + '</dd>';
  return '<tr class="det"><td colspan="6"><div class="det-in">' +
    '<div class="pn">' + (p ? 'para. ' + esc(p) : 'no paragraph number in this extract') + '</div>' +
    '<p class="full">' + esc(r.text || '') + '</p>' +
    '<dl class="lab">' +
    row('Themes', r._themes.length ? r._themes.map(esc).join(' · ') : 'not labelled') +
    row('SDGs', sdgTxt) +
    row('SDG targets', (r.sdg_targets || []).length ? r.sdg_targets.map(esc).join(' · ') : 'not labelled') +
    row('Affected persons', (r.affected_persons || []).length ? r.affected_persons.map(esc).join(' · ') : 'not labelled') +
    (r.section ? row('Section', esc(r.section)) : '') +
    '</dl>' +
    '<button class="btn copy" type="button" data-id="' + r._i + '" data-label="' + esc(label) + '">' + esc(label) + '</button>' +
    (r.doc_url ? '<a class="btn" style="text-decoration:none;display:inline-block" href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">Open the UN document</a>' : '') +
    '</div></td></tr>';
}
function copyText(t, btn){
  const done = () => { const l = btn.dataset.label; btn.textContent = 'Copied'; setTimeout(() => btn.textContent = l, 2000); };
  const fallback = () => {
    const ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); done(); } catch (e) { btn.textContent = t; }
    ta.remove();
  };
  if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, fallback);
  else fallback();
}

// ---- overview ----
function renderOverview(){
  const types = {};
  R.forEach(r => types[r.type] = (types[r.type] || 0) + 1);
  const typeLine = Object.keys(types).sort().map(k => esc(k) + ' ' + fmt(types[k])).join(' · ');
  const mDocs = new Set(M.map(r => r.symbol)).size;
  const yrs = new Set(YEARS).size;
  let h = '<div class="tiles">' +
    '<div class="tile"><div class="tl">All records in the file</div><div class="tn">' + fmt(R.length) + '</div>' +
    '<div class="tm">' + typeLine + '</div><div class="tm">Matching the filters: <b>' + fmt(M.length) + '</b></div>' +
    '<div class="note">How this is computed: every record in the file, counted by its type as spelled in the data. The matching line applies the filters on the left.</div></div>' +
    '<div class="tile"><div class="tl">Documents</div><div class="tn">' + fmt(DOCS_FILE) + '</div>' +
    '<div class="tm">Matching the filters: ' + fmt(mDocs) + '</div>' +
    '<div class="note">Distinct UN document symbols in the file, and in the matching set.</div></div>' +
    '<div class="tile"><div class="tl">Years</div><div class="tn">' + YMIN + '–' + YMAX + '</div>' +
    '<div class="tm">' + yrs + ' distinct years with records</div>' +
    '<div class="note">Smallest and largest <code>year</code>. Years with no records are gaps in FIG.02.</div></div>' +
    '</div>';
  h += '<div class="tiles">';
  for (const mech of MECHS) {
    const mm = M.filter(r => r.mechanism === mech);
    const docs = new Set(mm.map(r => r.symbol)).size;
    const latest = mm.length ? Math.max(...mm.map(r => r.year)) : '—';
    const share = M.length ? (mm.length / M.length * 100).toFixed(1) + '%' : '—';
    const upr = mech === 'Universal Periodic Review';
    h += '<div class="tile"><div class="tl"><span class="dot" style="background:' + (MCOL[mech] || '#555') + '"></span>' + esc(mech) + '</div>' +
      '<div class="tn">' + fmt(mm.length) + '</div>' +
      '<div class="tm">' + fmt(docs) + ' documents · latest ' + latest + ' · ' + share + ' of matching</div>' +
      '<div class="note">How this is computed: matching records with this mechanism; share = that count ÷ matching records.</div>' +
      (upr ? '<p style="margin:8px 0 0"><button class="link-btn" id="stBtn" type="button" aria-expanded="' + stOpen + '">see the States</button></p><div id="stList" ' + (stOpen ? '' : 'hidden') + '></div>' : '') +
      '</div>';
  }
  h += '</div>';
  $('overview').innerHTML = h;
  if (stOpen) renderStates();
  $('fig1Title').textContent = 'Ten most frequent themes among ' + fmt(M.length) + ' filtered records';
  $('fig2Title').textContent = 'Records per year by mechanism, ' + fmt(M.length) + ' filtered records';
  $('src1').textContent = fmt(R.length) + ' records';
  $('src2').textContent = fmt(R.length) + ' records';
  renderThemeTable();
  renderChecks();
}
function renderStates(){
  const cnt = {};
  M.filter(r => r.mechanism === 'Universal Periodic Review').forEach(r => (r._states || []).forEach(s => cnt[s] = (cnt[s] || 0) + 1));
  const top = Object.keys(cnt).sort((a, b) => cnt[b] - cnt[a] || a.localeCompare(b)).slice(0, 10);
  const el = $('stList'); if (!el) return;
  el.innerHTML = '<p class="hint" style="margin:8px 0 4px">Ten States that made most recommendations to ' + esc(COUNTRY) + '. Counts of recommendations in the matching set; a line naming two States counts for each.</p>' +
    (top.length ? '<table><thead><tr><th scope="col">State</th><th scope="col" class="num">Records</th></tr></thead><tbody>' +
      top.map(s => '<tr><td>' + esc(s) + '</td><td class="num">' + fmt(cnt[s]) + '</td></tr>').join('') + '</tbody></table>'
      : '<p class="msg">No States found in the matching set.</p>');
  const b = $('stBtn'); if (b) b.setAttribute('aria-expanded', stOpen);
}
function renderThemeTable(){
  const empty = !M.length;
  $('themeMsg').hidden = !empty; $('fig1wrap').hidden = empty;
  let h = '<caption>Ten most frequent themes among ' + fmt(M.length) + ' filtered records</caption><thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead><tbody>';
  if (!empty) themeTop.forEach(t => {
    h += '<tr><td>' + esc(t.t) + '</td><td class="num">' + fmt(t.n) + '</td><td class="num">' + (t.n / M.length * 100).toFixed(1) + '%</td><td>' + t.y0 + '–' + t.y1 + '</td></tr>';
  });
  else h += '<tr><td colspan="4" class="msg">No records match</td></tr>';
  $('themeTable').innerHTML = h + '</tbody>';
}

// ---- charts ----
const endLabels = {id:'endl', afterDatasetsDraw(c){
  const ctx = c.ctx; const meta = c.getDatasetMeta(0);
  ctx.save(); ctx.fillStyle = '#1d1b18'; ctx.font = '12px system-ui'; ctx.textBaseline = 'middle';
  meta.data.forEach((bar, i) => ctx.fillText(fmt(c.data.datasets[0].data[i]), bar.x + 6, bar.y));
  ctx.restore();
}};
const themeChart = new Chart($('fig1'), {
  type:'bar',
  data:{labels:[], datasets:[{data:[], backgroundColor:'rgba(155,35,53,0.8)', borderWidth:0}]},
  options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:false,
    layout:{padding:{right:44}},
    plugins:{legend:{display:false}, tooltip:{callbacks:{label:c => fmt(c.raw) + ' records'}}},
    scales:{x:{beginAtZero:true, ticks:{precision:0}, grid:{color:'#e6dfd0'}}, y:{ticks:{autoSkip:false, font:{size:12}}, grid:{display:false}}},
    onClick:(evt, els) => {
      if (!els.length) return;
      const t = themeTop[els[0].index]; if (!t) return;
      if (!F.themes.includes(t.t)) F.themes.push(t.t);
      changed();
    }},
  plugins:[endLabels]
});
const timeChart = new Chart($('fig2'), {
  type:'bar',
  data:{labels:[], datasets:[]},
  options:{responsive:true, maintainAspectRatio:false, animation:false,
    plugins:{legend:{position:'top', labels:{boxWidth:12}}},
    scales:{x:{stacked:true, ticks:{autoSkip:false, maxRotation:90}}, y:{stacked:true, beginAtZero:true, ticks:{precision:0}, grid:{color:'#e6dfd0'}}}}
});
function renderCharts(){
  const empty = !M.length;
  $('timeMsg').hidden = !empty; $('fig2wrap').hidden = empty;
  themeChart.data.labels = themeTop.map(t => t.t);
  themeChart.data.datasets[0].data = themeTop.map(t => t.n);
  themeChart.update();
  const years = [];
  if (YEARS.length) for (let y = YMIN; y <= YMAX; y++) years.push(y);
  const grid = {};
  M.forEach(r => { const k = r.mechanism + '|' + r.year; grid[k] = (grid[k] || 0) + 1; });
  timeChart.data.labels = years;
  timeChart.data.datasets = MECHS.map(m => ({
    label: m, backgroundColor: MCOL[m] || '#555',
    data: years.map(y => grid[m + '|' + y] || 0)
  }));
  timeChart.update();
}

// ---- checks ----
function renderChecks(){
  const checks = [];
  const add = (name, compared, a, b, status, detail) => checks.push({name, compared, a, b, status, detail});
  // 1 record count
  add('Record count', 'records.length vs stated count', R.length, Number(D.count), R.length === Number(D.count) ? 'pass' : 'fail');
  // 2-4 partitions
  const part = (key, label) => {
    const o = {}; R.forEach(r => o[r[key]] = (o[r[key]] || 0) + 1);
    let s = 0; Object.values(o).forEach(v => s += v);
    add('Partition by ' + label, 'sum of counts per ' + label + ' vs records', s, R.length, s === R.length ? 'pass' : 'fail',
      Object.keys(o).sort().map(k => k + ': ' + fmt(o[k])).join(' · '));
  };
  part('mechanism', 'mechanism'); part('body', 'body'); part('year', 'year');
  // 5 type partition
  const tyo = {}; R.forEach(r => tyo[r.type] = (tyo[r.type] || 0) + 1);
  let ts = 0; Object.values(tyo).forEach(v => ts += v);
  add('Type partition', 'sum of counts per type vs headline total', ts, R.length, ts === R.length ? 'pass' : 'fail',
    Object.keys(tyo).sort().map(k => k + ': ' + fmt(tyo[k])).join(' · '));
  // 6 chart against table
  let okBars = 0;
  themeTop.forEach(t => { const again = M.filter(r => r._themes.includes(t.t)).length; if (again === t.n) okBars++; });
  const maxBar = themeTop.length ? themeTop[0].n : 0;
  const barsOk = okBars === themeTop.length && maxBar <= M.length;
  add('Chart against table', 'bars recomputed by a second loop', okBars, themeTop.length, barsOk ? 'pass' : 'fail',
    'largest bar ' + fmt(maxBar) + ' ≤ filtered records ' + fmt(M.length));
  // 7 links
  const bad = R.filter(r => {
    let d = r.doc_url || '';
    try { d = decodeURIComponent(d); } catch (e) {}
    return !(d.toLowerCase().startsWith('https://docs.un.org/') && d.toLowerCase().endsWith(String(r.symbol || '').toLowerCase()));
  });
  add('Links', 'doc_url starts with docs.un.org and ends with symbol', R.length - bad.length, R.length, bad.length ? 'fail' : 'pass',
    bad.length ? 'Failing: ' + bad.slice(0, 30).map(r => r.symbol + ' (' + (r.doc_url || 'no URL') + ')').join('; ') : '');
  // 8 paragraph numbers
  const pn = MECHS.map(m => {
    const a = R.filter(r => r.mechanism === m); const f = a.filter(r => r._para).length;
    return {m, pct: a.length ? f / a.length * 100 : 0, f, n: a.length};
  });
  const upr8 = pn.find(x => x.m === 'Universal Periodic Review');
  const pnWarn = upr8 && upr8.pct < 100;
  add('Paragraph numbers', 'share of records with a number, per mechanism (UPR expected 100%)', upr8 ? upr8.f : 0, upr8 ? upr8.n : 0,
    pnWarn ? 'warn' : 'pass', pn.map(x => x.m + ': ' + x.pct.toFixed(1) + '% (' + fmt(x.f) + ' of ' + fmt(x.n) + ')').join(' · '));
  // 9 states
  const upr = R.filter(r => r.mechanism === 'Universal Periodic Review');
  const withS = upr.filter(r => r._states && r._states.length);
  const noS = upr.filter(r => !(r._states && r._states.length));
  add('States found', 'UPR records with at least one State vs UPR records', withS.length, upr.length, noS.length ? 'warn' : 'pass',
    noS.length ? 'Without a State: ' + noS.slice(0, 40).map(r => r.symbol + ' … ' + (r.text || '').slice(-60)).join(' | ') : '');
  // 10 ids
  const ids = new Set(R.map(r => r.id)).size;
  add('Distinct ids', 'distinct id vs record count', ids, R.length, ids === R.length ? 'pass' : 'fail');
  // 11 duplicate texts
  const tc = {}; R.forEach(r => tc[r.text] = (tc[r.text] || 0) + 1);
  const dupVals = Object.keys(tc).filter(k => tc[k] > 1);
  add('Duplicate texts', 'text values occurring more than once', dupVals.length, 0, dupVals.length ? 'warn' : 'pass',
    dupVals.length ? 'Records involved: ' + fmt(dupVals.reduce((s, k) => s + tc[k], 0)) : '');
  // 12-14 not labelled
  const nl = (label, pred) => { const n = R.filter(pred).length; add('Records with no ' + label, 'count', n, R.length, 'info', n ? 'not labelled' : ''); };
  nl('themes', r => !(r.themes && r.themes.length));
  nl('SDGs', r => !(r.sdgs && r.sdgs.length));
  nl('affected persons', r => !(r.affected_persons && r.affected_persons.length));

  const cls = {pass:'s-pass', fail:'s-fail', warn:'s-warn', info:'s-info'};
  const lab = {pass:'pass', fail:'check failed', warn:'warning', info:'not labelled'};
  $('checks').innerHTML = checks.map(c =>
    '<div class="chk"><div class="ck-n">' + esc(c.name) + '</div>' +
    '<div>' + esc(c.compared) + ': <b>' + esc(c.a) + '</b> vs <b>' + esc(c.b) + '</b></div>' +
    '<div class="ck-s ' + cls[c.status] + '">' + (c.status === 'fail' ? 'check failed' : lab[c.status]) + '</div>' +
    (c.detail ? '<div class="det-list">' + esc(c.detail) + '</div>' : '') + '</div>').join('');
  $('chkLbl').textContent = 'Every check (' + checks.length + ')';
}

// ---- render all ----
function renderAll(){
  recompute();
  renderRail();
  renderOverview();
  renderCharts();
  renderTable();
}

// ---- export ----
function csv(v){ return '"' + String(v ?? '').replace(/"/g, '""') + '"'; }
function exportCsv(){
  const list = sorted(M);
  const lines = [
    '# Country: ' + COUNTRY, '# Source: ' + (D.source || '') + ' ' + (D.source_url || ''), '# Built: ' + (D.built || ''),
    '# Filters: ' + (describe() || 'none'), '# Rows: ' + list.length, '# Dated by document.'
  ];
  lines.push(['date','year','body','mechanism','type','symbol','paragraph','doc_url','recommending_state','themes','sdgs','sdg_targets','affected_persons','section','text'].map(csv).join(','));
  list.forEach(r => lines.push([
    r.date, r.year, r.body, r.mechanism, r.type, r.symbol, r._para || '', r.doc_url || '',
    r.mechanism === 'Universal Periodic Review' ? (r._states && r._states.length ? r._states.join('; ') : 'State not found') : '',
    (r.themes || []).join('; '), (r.sdgs || []).join('; '), (r.sdg_targets || []).join('; '),
    (r.affected_persons || []).join('; '), r.section || '', r.text || ''
  ].map(csv).join(',')));
  const blob = new Blob([lines.join('\n')], {type:'text/csv'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'uhri-' + COUNTRY.toLowerCase().replace(/\W+/g, '-') + '-filtered.csv';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  $('expStatus').textContent = 'CSV prepared: ' + fmt(list.length) + ' rows.';
}
function summary(){
  const docs = new Set(M.map(r => r.symbol)).size;
  return COUNTRY + ': ' + fmt(M.length) + ' of ' + fmt(R.length) + ' records in the file match the current filters (' + (describe() || 'no filters') + '). ' +
    fmt(docs) + ' documents, dated ' + YMIN + '–' + YMAX + '. Top themes: ' +
    (themeTop.length ? themeTop.map(t => t.t + ' (' + fmt(t.n) + ')').join('; ') : 'none') +
    '. Source: ' + (D.source || '') + ', built ' + (D.built || '') + '. Dated by document; no model was called.';
}

// ---- wiring ----
function init(){
  $('lbl').textContent = 'UHRI · ' + COUNTRY;
  $('ttl').textContent = 'UN human rights recommendations and observations: ' + COUNTRY;
  $('meta').innerHTML = 'Source: <a href="' + esc(D.source_url || '#') + '" target="_blank" rel="noopener">' + esc(D.source || 'UHRI') + '</a> · ' +
    fmt(R.length) + ' records · ' + fmt(DOCS_FILE) + ' documents · ' + YMIN + '–' + YMAX + ' · built ' + esc(D.built || '—') + ' · dated by document';
  $('ft').innerHTML = 'Built on OHCHR UHRI data · ' + fmt(R.length) + ' records · <a href="' + esc(D.source_url || '#') + '" target="_blank" rel="noopener">source</a>';
  $('srcLine').innerHTML = esc(D.source || 'UHRI') + ', <a href="' + esc(D.source_url || '#') + '" target="_blank" rel="noopener">' + esc(D.source_url || '') + '</a>, built ' + esc(D.built || '—') + '. Licence and terms as stated by the source.';
  $('src3').textContent = fmt(R.length) + ' records';
  fillStatic(); fillBody();

  tabs.forEach((t, k) => t.addEventListener('click', () => { showTab(k); tabs[k].focus(); }));
  $('t0').parentElement.addEventListener('keydown', e => {
    const k = tabs.indexOf(document.activeElement); if (k < 0) return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
      const n = (k + (e.key === 'ArrowRight' ? 1 : 2)) % 3; showTab(n); tabs[n].focus(); e.preventDefault();
    }
  });
  [0,1,2].forEach(j => $('acc' + j).addEventListener('click', () => setOpen(openAcc === j ? -1 : j)));
  $('kw').addEventListener('input', e => onKw(e.target));
  $('q').addEventListener('input', e => onKw(e.target));
  $('s-mech').addEventListener('change', e => { F.mech = e.target.value; fillBody(); changed(); });
  $('s-body').addEventListener('change', e => { F.body = e.target.value; changed(); });
  $('s-type').addEventListener('change', e => { F.type = e.target.value; changed(); });
  $('s-state').addEventListener('change', e => { F.state = e.target.value; changed(); });
  $('s-sdg').addEventListener('change', e => { F.sdg = e.target.value; changed(); });
  const yf = $('s-yf'), yt = $('s-yt');
  const yrs = () => {
    let a = yf.value, b = yt.value;
    if (a && b && Number(a) > Number(b)) { [a, b] = [b, a]; }
    F.yf = a; F.yt = b; yf.value = a; yt.value = b; changed();
  };
  yf.addEventListener('change', yrs); yt.addEventListener('change', yrs);
  $('clearAll').addEventListener('click', () => {
    Object.assign(F, {kw:'', mech:'', body:'', type:'', state:'', yf:'', yt:'', sdg:'', themes:[]});
    syncControls(); changed();
  });
  $('chips').addEventListener('click', e => {
    const b = e.target.closest('button[data-chip]'); if (!b) return;
    const c = chipCache[Number(b.dataset.chip)]; if (!c) return;
    c.remove(); syncControls(); changed();
  });
  $('dateSort').addEventListener('click', () => { asc = !asc; renderTable(); });
  $('more').addEventListener('click', () => { shown += 50; renderTable(); });
  const rb = $('recBody');
  rb.addEventListener('click', e => {
    if (e.target.closest('a')) return;
    const b = e.target.closest('button.copy');
    if (b) {
      const r = R[Number(b.dataset.id)];
      copyText(r.symbol + (r._para ? ', para. ' + r._para : ''), b); return;
    }
    const tr = e.target.closest('tr.row'); if (!tr) return;
    toggle(Number(tr.dataset.id));
  });
  rb.addEventListener('keydown', e => {
    if (e.key !== 'Enter') return;
    const tr = e.target.closest('tr.row'); if (!tr) return;
    e.preventDefault(); toggle(Number(tr.dataset.id));
  });
  function toggle(id){
    if (expanded.has(id)) expanded.delete(id); else expanded.add(id);
    renderTable();
    const tr = rb.querySelector('tr.row[data-id="' + id + '"]'); if (tr) tr.focus();
  }
  $('overview').addEventListener('click', e => {
    if (e.target.closest('#stBtn')) { stOpen = !stOpen; $('stList').hidden = !stOpen; if (stOpen) renderStates(); e.target.closest('#stBtn').setAttribute('aria-expanded', stOpen); }
  });
  $('chkBtn').addEventListener('click', () => {
    const open = $('chkPanel').hidden;
    $('chkPanel').hidden = !open; $('chkBtn').setAttribute('aria-expanded', open);
  });
  $('csvBtn').addEventListener('click', exportCsv);
  $('sumBtn').addEventListener('click', () => copyText(summary(), $('sumBtn')));
  showTab(0); setOpen(-1);
  renderAll(); syncControls();
}
init();
})();
</script>
</body>
</html>
```