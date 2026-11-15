I built a drafting-history tool that opens on the first article in your file, shows every draft in date order with added and removed words marked, lists the votes taken between drafts, and ranks the drafts by how much of the text they changed.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Drafting history of a Covenant article</title>
<style>
:root{--bg:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--acc:#9b2335;--mute:#5a554c;
--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;
--sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 var(--sans)}
.wrap{max-width:1040px;margin:0 auto;padding:22px 24px 60px}
.mono{font:11.5px/1.4 var(--mono);text-transform:uppercase;letter-spacing:.09em;color:var(--mute)}
h1{font:400 34px/1.15 var(--serif);margin:6px 0 6px}
.src{margin:0 0 14px;color:var(--mute);font-size:15px}
.pick{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:10px 0 0}
select{font:16px var(--sans);color:var(--ink);background:var(--bg);border:1px solid var(--ink);padding:7px 10px;max-width:100%}
header{border-bottom:1px solid var(--rule);padding-bottom:14px}
[role=tablist]{display:flex;gap:6px;flex-wrap:wrap;border-bottom:1px solid var(--rule);margin:0 0 22px}
[role=tab]{font:12px var(--mono);text-transform:uppercase;letter-spacing:.09em;background:none;border:0;border-bottom:3px solid transparent;color:var(--ink);padding:12px 14px 9px;cursor:pointer}
[role=tab][aria-selected=true]{color:var(--acc);border-bottom-color:var(--acc);font-weight:700}
button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
a{color:var(--acc)}
.big{font:400 52px/1 var(--serif)}
.nums{display:flex;gap:40px;flex-wrap:wrap;margin:6px 0 20px}
.nums div{min-width:150px}
.lead{font:400 21px/1.4 var(--serif);max-width:760px;margin:0 0 22px}
h2{font:400 24px/1.2 var(--serif);margin:26px 0 4px}
.how{font:12px/1.5 var(--mono);color:var(--mute);margin:8px 0 0}
.bars{margin:12px 0 0;padding:0;list-style:none}
.bars li{border-top:1px solid var(--rule)}
.bar{display:grid;grid-template-columns:minmax(150px,300px) 1fr 150px;gap:14px;align-items:center;width:100%;text-align:left;background:none;border:0;color:var(--ink);font:15px var(--sans);padding:9px 2px;cursor:pointer}
.bar:hover .lab{text-decoration:underline}
.track{height:16px}
.fill{height:100%;background:var(--acc);min-width:2px}
.val{font:13px var(--mono);text-align:right;font-variant-numeric:tabular-nums}
.stage{border-top:1px solid var(--rule);padding:14px 0 8px}
.stage h3{margin:0;font:400 21px/1.3 var(--serif)}
.sth{display:block;width:100%;text-align:left;background:none;border:0;color:var(--ink);font:inherit;cursor:pointer;padding:2px 0}
.sth .mono::before{content:"+ ";color:var(--acc)}
.sth[aria-expanded=true] .mono::before{content:"\2212  "}
.meta{display:flex;gap:18px;flex-wrap:wrap;margin:4px 0 0;font:12px var(--mono);color:var(--mute)}
.body{margin:10px 0 6px;max-width:820px}
.draft{font:400 18px/1.7 var(--serif);margin:0 0 16px}
ins{background:#dbe8d0;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:3px}
del{background:#f0d6d2;text-decoration:line-through;text-decoration-thickness:2px}
.legend{font:12px var(--mono);color:var(--mute);margin:0 0 14px}
table{border-collapse:collapse;width:100%;font-size:15px;margin:6px 0 10px}
caption{text-align:left;font:11.5px var(--mono);text-transform:uppercase;letter-spacing:.09em;color:var(--mute);padding:4px 0}
th{font:11px var(--mono);text-transform:uppercase;letter-spacing:.08em;color:var(--mute);text-align:left;border-bottom:1px solid var(--ink);padding:6px 8px 6px 0;vertical-align:bottom}
td{border-top:1px solid var(--rule);padding:7px 8px 7px 0;vertical-align:top}
.n{text-align:right;font-variant-numeric:tabular-nums}
.none{color:var(--mute);font-style:italic;margin:4px 0 12px}
.chk{display:grid;grid-template-columns:70px 220px 1fr;gap:6px 16px;border-top:1px solid var(--rule);padding:9px 0}
.st{font:12px var(--mono);letter-spacing:.08em}
.st.warn{color:var(--acc);font-weight:700}
.meth{max-width:780px;padding-left:20px}
.meth li{margin:0 0 8px}
@media(max-width:720px){.bar{grid-template-columns:1fr}.val{text-align:left}.chk{grid-template-columns:1fr}.big{font-size:40px}h1{font-size:28px}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="mono">WORKSHOP_DATA.drafts &middot; drafting history</div>
  <h1>How an article changed while it was drafted</h1>
  <p class="src" id="src"></p>
  <div class="pick"><label class="mono" for="art">Article</label><select id="art"></select><span class="mono">pick an article, every tab follows</span></div>
</header>
<div id="tabs" role="tablist" aria-label="Views" style="margin-top:14px">
  <button role="tab" id="t0" aria-controls="p0" aria-selected="true">01 Overview</button>
  <button role="tab" id="t1" aria-controls="p1" aria-selected="false" tabindex="-1">02 Stages</button>
  <button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">03 Can I trust this?</button>
</div>
<section id="p0" role="tabpanel" aria-labelledby="t0"></section>
<section id="p1" role="tabpanel" aria-labelledby="t1" hidden></section>
<section id="p2" role="tabpanel" aria-labelledby="t2" hidden></section>
</div>
<script>
(function(){
var D = window.WORKSHOP_DATA && window.WORKSHOP_DATA.drafts;
var $ = function(s){ return document.querySelector(s); };
function esc(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
var MON = {january:1,february:2,march:3,april:4,may:5,june:6,july:7,august:8,september:9,october:10,november:11,december:12};
var P = function(n){ return (n < 10 ? '0' : '') + n; };

if (!D || !D.records || !D.records.length) {
  $('#p0').innerHTML = '<p class="lead">The drafting file is not attached, so there is nothing to show. Drag "Drafts of three ICCPR articles" from "Your files" into the chat.</p>';
  $('#tabs').hidden = true; $('#art').parentNode.hidden = true;
  return;
}

/* ---------- dates ---------- */
function parseDate(s){
  s = String(s || '').trim(); var m;
  if ((m = s.match(/^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$/)) && MON[m[2].toLowerCase()])
    return {end: m[3] + '-' + P(MON[m[2].toLowerCase()]) + '-' + P(+m[1]), exact: true};
  if ((m = s.match(/^([A-Za-z]+)\s+(\d{4})$/)) && MON[m[1].toLowerCase()]) {
    var mo = MON[m[1].toLowerCase()], last = new Date(Date.UTC(+m[2], mo, 0)).getUTCDate();
    return {end: m[2] + '-' + P(mo) + '-' + P(last), exact: false};
  }
  return null;
}

/* ---------- words and diff ---------- */
function toks(text){
  var t = String(text || '').replace(/(\p{L})-\s+(\p{L})/gu, '$1$2').replace(/[—–]/g, ' ');
  return t.split(/\s+/).map(function(w){
    return {w: w, k: w.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '')};
  }).filter(function(x){ return x.k; });
}
function diff(a, b){
  var n = a.length, m = b.length, ops = [], i, j;
  if (n * m > 16e6) {
    a.forEach(function(x){ ops.push({t:'del', w:x.w}); });
    b.forEach(function(x){ ops.push({t:'ins', w:x.w}); });
    return ops;
  }
  var W = m + 1, dp = new Int32Array((n + 1) * W);
  for (i = n - 1; i >= 0; i--) for (j = m - 1; j >= 0; j--)
    dp[i*W + j] = a[i].k === b[j].k ? dp[(i+1)*W + j + 1] + 1 : Math.max(dp[(i+1)*W + j], dp[i*W + j + 1]);
  i = 0; j = 0;
  while (i < n && j < m) {
    if (a[i].k === b[j].k) { ops.push({t:'eq', w:b[j].w}); i++; j++; }
    else if (dp[(i+1)*W + j] >= dp[i*W + j + 1]) { ops.push({t:'del', w:a[i].w}); i++; }
    else { ops.push({t:'ins', w:b[j].w}); j++; }
  }
  while (i < n) ops.push({t:'del', w:a[i++].w});
  while (j < m) ops.push({t:'ins', w:b[j++].w});
  return ops;
}
function opsHtml(ops){
  var out = '', cur = null, buf = [];
  function flush(){
    if (!buf.length) return;
    var t = esc(buf.join(' '));
    out += cur === 'ins' ? '<ins>' + t + '</ins> ' : cur === 'del' ? '<del>' + t + '</del> ' : t + ' ';
    buf = [];
  }
  ops.forEach(function(o){ if (o.t !== cur) { flush(); cur = o.t; } buf.push(o.w); });
  flush();
  return out;
}
function count(ops, t){ var c = 0; ops.forEach(function(o){ if (o.t === t) c++; }); return c; }

/* ---------- model per article ---------- */
var cache = {};
function model(ix){
  if (cache[ix]) return cache[ix];
  var rec = D.records[ix];
  var st = (rec.stages || []).map(function(s, i){
    return Object.assign({}, s, {i0: i, d: parseDate(s.date), toks: toks(s.text)});
  });
  var allDated = st.length > 0 && st.every(function(s){ return s.d; });
  var asDelivered = allDated && st.every(function(s, i){ return i === 0 || st[i-1].d.end <= s.d.end; });
  if (allDated) st.sort(function(a, b){ return a.d.end < b.d.end ? -1 : a.d.end > b.d.end ? 1 : a.i0 - b.i0; });
  st.forEach(function(s, i){
    s.votes = [];
    if (i === 0) { s.ops = null; s.add = 0; s.rem = 0; s.share = null; return; }
    s.ops = diff(st[i-1].toks, s.toks);
    s.add = count(s.ops, 'ins'); s.rem = count(s.ops, 'del');
    var tot = st[i-1].toks.length + s.toks.length;
    s.share = tot ? (s.add + s.rem) / tot : 0;
  });
  var orphan = [];
  (rec.votes || []).slice().sort(function(a, b){ return String(a.date).localeCompare(String(b.date)); }).forEach(function(v){
    var k = -1, why = 'no usable date';
    if (allDated && /^\d{4}-\d{2}-\d{2}$/.test(v.date || '')) {
      for (var i = 1; i < st.length; i++) if (v.date > st[i-1].d.end && v.date <= st[i].d.end) { k = i; break; }
      if (k < 0) why = v.date <= st[0].d.end ? 'on or before the end of the first draft’s month'
                     : v.date > st[st.length-1].d.end ? 'after the last stage' : 'falls in a month shared by two drafts';
    }
    if (k < 0) orphan.push({v: v, why: why}); else st[k].votes.push(v);
  });
  var carry = null;
  if (st.length > 1 && st[st.length-1].toks.length) {
    var o = diff(st[0].toks, st[st.length-1].toks);
    carry = count(o, 'eq') / st[st.length-1].toks.length;
  }
  return cache[ix] = {rec: rec, st: st, allDated: allDated, asDelivered: asDelivered, orphan: orphan, carry: carry};
}

/* ---------- helpers ---------- */
function docLink(sym){
  if (!sym) return '<span class="mono">no symbol</span>';
  return '<a href="https://docs.un.org/en/' + encodeURI(sym) + '" target="_blank" rel="noopener">' + esc(sym) + '</a>';
}
function pct(x){ return x == null ? 'n/a' : Math.round(x * 100) + '%'; }
function label(s){ return esc(s.date) + ' · ' + esc(s.symbol); }

/* ---------- tab 01 ---------- */
function overview(m){
  var st = m.st, r = m.rec;
  if (!st.length) return '<p class="lead">This article has no drafts in the file.</p>';
  var first = st[0], last = st[st.length-1];
  var ranked = st.slice(1).sort(function(a, b){ return b.share - a.share; });
  var nv = (r.votes || []).length;
  var h = '<p class="lead">Article ' + esc(r.article) + ' (' + esc(r.title) + '), ' + esc(r.instrument) + ', went through ' + st.length +
    ' drafts between ' + esc(first.date) + ' and ' + esc(last.date) + '.' +
    (ranked.length ? ' The biggest rewrite was the draft of ' + esc(ranked[0].date) + ' (' + pct(ranked[0].share) + ' of the words changed).' : '') + '</p>';
  h += '<div class="nums"><div><div class="big">' + st.length + '</div><div class="mono">drafts, first to adopted</div></div>' +
       '<div><div class="big">' + nv + '</div><div class="mono">recorded votes on this article</div></div>' +
       '<div><div class="big">' + pct(m.carry) + '</div><div class="mono">of the adopted words are in the first draft</div></div></div>';
  h += '<h2><span class="mono">FIG.01</span><br>Which drafts changed the text most</h2>';
  if (!ranked.length) return h + '<p class="none">Only one draft: nothing to compare.</p>';
  h += '<ol class="bars" aria-label="Drafts ranked by share of words changed">';
  var max = ranked[0].share || 1;
  ranked.forEach(function(s){
    var idx = st.indexOf(s);
    h += '<li><button class="bar" data-go="' + idx + '" title="Open this draft"><span class="lab">' + label(s) + '</span>' +
      '<span class="track"><span class="fill" style="display:block;width:' + Math.max(1, s.share / max * 100) + '%"></span></span>' +
      '<span class="val">' + pct(s.share) + ' &middot; +' + s.add + ' −' + s.rem + '</span></button></li>';
  });
  h += '</ol><p class="how">click = open that draft &middot; How this is computed: share = (words added + words removed) / (words in the earlier draft + words in this draft), after ignoring punctuation, capitals and line-end hyphens. The first draft has no earlier one, so it is not ranked.</p>';
  return h;
}

/* ---------- tab 02 ---------- */
function votesTable(s, prev){
  if (!s.votes.length) return '<p class="none">No recorded vote on this article is dated between ' + esc(prev.date) + ' and ' + esc(s.date) + '.</p>';
  var h = '<table><caption>Votes since the previous stage (' + esc(prev.date) + ' to ' + esc(s.date) + ')</caption><thead><tr>' +
    '<th scope="col">Date</th><th scope="col">Voted on</th><th scope="col">Result</th>' +
    '<th scope="col" class="n">Yes</th><th scope="col" class="n">No</th><th scope="col" class="n">Abst.</th>' +
    '<th scope="col">Proposed by</th><th scope="col">Meeting</th></tr></thead><tbody>';
  s.votes.forEach(function(v){
    var num = function(x){ return x == null ? '<span title="not recorded">–</span>' : esc(x); };
    h += '<tr><td>' + esc(v.date) + '</td><td>' + esc(v.subject || 'not recorded') + '</td><td>' + esc(v.outcome || 'not recorded') + '</td>' +
      '<td class="n">' + num(v.yes) + '</td><td class="n">' + num(v.no) + '</td><td class="n">' + num(v.abstentions) + '</td>' +
      '<td>' + ((v.proposers || []).length ? esc(v.proposers.join(', ')) : 'not recorded') + '</td><td>' + docLink(v.meeting) + '</td></tr>';
  });
  return h + '</tbody></table>';
}
function stages(m){
  var st = m.st;
  if (!st.length) return '<p class="none">No drafts.</p>';
  var h = '<p class="legend"><ins>added words</ins> &nbsp; <del>removed words</del> &nbsp; plain = unchanged &middot; click a stage = fold / unfold</p>';
  st.forEach(function(s, i){
    var id = 'st' + i;
    h += '<article class="stage" id="' + id + '"><h3><button class="sth" aria-expanded="true" aria-controls="' + id + 'b">' +
      '<span class="mono">Stage ' + P(i + 1) + ' &middot; ' + esc(s.date) + '</span>' + esc(s.stage || 'Draft') + '</button></h3>' +
      '<div class="meta"><span>' + docLink(s.symbol) + '</span><span>draft article no. ' + esc(s.draft_article == null ? '?' : s.draft_article) + '</span>' +
      (s.page != null ? '<span>page ' + esc(s.page) + '</span>' : '') +
      (i ? '<span>+' + s.add + ' added · −' + s.rem + ' removed · ' + pct(s.share) + ' changed</span>' : '<span>first draft: nothing to compare</span>') +
      '</div><div class="body" id="' + id + 'b">';
    if (!s.toks.length) h += '<p class="none">This stage has no text in the file.</p>';
    else h += '<p class="draft">' + (i ? opsHtml(s.ops) : esc(s.toks.map(function(t){ return t.w; }).join(' '))) + '</p>';
    h += i ? votesTable(s, st[i-1]) : '<p class="none">Earliest draft in the file: no earlier stage, so no votes are assigned here.</p>';
    h += '</div></article>';
  });
  return h;
}

/* ---------- tab 03 ---------- */
function checks(m){
  var st = m.st, rows = [];
  function add(ok, name, text){ rows.push([ok, name, text]); }
  if (!st.length) return '<p class="none">No drafts, no checks.</p>';
  var last = st[st.length-1];
  add(true, 'Stages in the file', st.length + ' drafts, ' + esc(st[0].date) + ' to ' + esc(last.date) + '.');
  add(/^A\/RES\/2200/.test(last.symbol || ''), 'Ends with the adopted text',
      'The last stage is ' + esc(last.symbol || 'without a symbol') + (/^A\/RES\/2200/.test(last.symbol || '') ? ', the General Assembly resolution of 1966.' : ', not the General Assembly resolution 2200 A (XXI).'));
  add(m.allDated && m.asDelivered, 'Dates and order',
      m.allDated ? (m.asDelivered ? 'All dates read; the file was already in date order.' : 'All dates read, but the file was not in date order; the stages were sorted by date.')
                 : 'At least one date could not be read, so the stages stay in file order and votes cannot be assigned.');
  var empty = st.filter(function(s){ return !s.toks.length; });
  add(!empty.length, 'Empty texts', empty.length ? empty.length + ' stage(s) have no text.' : 'Every stage has text.');
  var same = st.filter(function(s, i){ return i && s.add + s.rem === 0; });
  add(!same.length, 'Drafts identical to the one before',
      same.length ? same.map(function(s){ return esc(s.date); }).join('; ') + ': the words are the same after normalising.' : 'None: every stage differs from the one before.');
  var shared = 0; st.forEach(function(s, i){ if (i && m.allDated && s.d.end === st[i-1].d.end) shared++; });
  add(!shared, 'Two drafts in one month', shared ? shared + ' stage(s) share a month with the one before; votes of that month go to the first only.' : 'None.');
  var assigned = 0; st.forEach(function(s){ assigned += s.votes.length; });
  var nv = (m.rec.votes || []).length;
  add(!m.orphan.length, 'Votes placed on a stage', assigned + ' of ' + nv + ' recorded votes fall between two stages.' +
      (m.orphan.length ? ' Not placed: ' + m.orphan.map(function(o){ return esc(o.v.date) + ' (' + esc(o.v.meeting || 'no meeting') + '): ' + o.why; }).join('; ') + '.' : ''));
  var nofig = (m.rec.votes || []).filter(function(v){ return v.yes == null || v.no == null || v.abstentions == null; }).length;
  add(!nofig, 'Vote figures', nofig ? nofig + ' vote(s) have no recorded figures; they show as a dash.' : 'All votes carry yes, no and abstention figures.');
  var noise = 0, where = [];
  st.forEach(function(s){ var c = s.toks.filter(function(t){ return /\p{Ll}\p{Lu}/u.test(t.w); }).length; noise += c; if (c) where.push(esc(s.date) + ' (' + c + ')'); });
  add(!noise, 'Likely OCR errors', noise ? noise + ' word(s) have a capital inside them (e.g. "AawPul"): ' + where.join(', ') + '. They survive normalising and show as changes, so the shares are upper bounds.' : 'No word with a capital letter inside it.');
  var h = '<h2><span class="mono">FIG.02</span><br>The app’s own checks for this article</h2>';
  rows.forEach(function(r){
    h += '<div class="chk"><span class="st' + (r[0] ? '' : ' warn') + '">' + (r[0] ? 'OK' : 'CHECK') + '</span><strong>' + esc(r[1]) + '</strong><span>' + r[2] + '</span></div>';
  });
  h += '<h2>Method</h2><ol class="meth">' +
    '<li>Words are compared after lower-casing, dropping punctuation and joining words broken at a line end ("restric- tions" becomes "restrictions"). Words shown keep the spelling of the draft they come from.</li>' +
    '<li>The comparison is a longest-common-sequence of words, the same every time. Text that moved appears once as removed and once as added.</li>' +
    '<li>Share changed = (added + removed) / (words before + words after). "Carried over" = adopted words that also appear, in order, in the first draft.</li>' +
    '<li>A vote belongs to the first stage whose end date is on or after the vote and later than the previous stage’s end. A draft dated only by month ends on the last day of that month.</li>' +
    '<li>Document links are built from the symbol on docs.un.org; scans of 1940s and 1950s documents may not open there.</li></ol>';
  return h;
}

/* ---------- app ---------- */
var state = {art: 0, tab: 0};
function render(){
  var m = model(state.art);
  $('#p0').innerHTML = overview(m);
  $('#p1').innerHTML = stages(m);
  $('#p2').innerHTML = checks(m);
  showTab(state.tab);
}
function showTab(n){
  state.tab = n;
  [0,1,2].forEach(function(i){
    var t = $('#t' + i), on = i === n;
    t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1;
    $('#p' + i).hidden = !on;
  });
}
(function init(){
  var total = 0, years = [];
  D.records.forEach(function(r, i){
    total += (r.stages || []).length;
    (r.stages || []).forEach(function(s){ var y = String(s.date || '').match(/\d{4}/); if (y) years.push(+y[0]); });
    var o = document.createElement('option');
    o.value = i; o.textContent = (r.instrument || '') + ' Art. ' + r.article + ' · ' + (r.title || '');
    $('#art').appendChild(o);
  });
  $('#src').textContent = 'Source: ' + (D.source || 'UN drafting records') + ' · n = ' + total + ' drafts of ' + D.records.length + ' articles · ' +
    (years.length ? Math.min.apply(null, years) + '–' + Math.max.apply(null, years) : 'years not available');
})();
$('#art').addEventListener('change', function(e){ state.art = +e.target.value; render(); });
$('#tabs').addEventListener('click', function(e){
  var b = e.target.closest('[role=tab]'); if (b) showTab(+b.id.slice(1));
});
$('#tabs').addEventListener('keydown', function(e){
  var k = {ArrowRight:1, ArrowLeft:-1}[e.key], n = state.tab;
  if (k) n = (state.tab + k + 3) % 3; else if (e.key === 'Home') n = 0; else if (e.key === 'End') n = 2; else return;
  e.preventDefault(); showTab(n); $('#t' + n).focus();
});
document.addEventListener('click', function(e){
  var g = e.target.closest('[data-go]');
  if (g) {
    showTab(1);
    var box = document.getElementById('st' + g.getAttribute('data-go'));
    var btn = box.querySelector('.sth');
    btn.setAttribute('aria-expanded', 'true'); document.getElementById(btn.getAttribute('aria-controls')).hidden = false;
    box.scrollIntoView(); btn.focus();
    return;
  }
  var s = e.target.closest('.sth');
  if (s) {
    var open = s.getAttribute('aria-expanded') === 'true';
    s.setAttribute('aria-expanded', !open);
    document.getElementById(s.getAttribute('aria-controls')).hidden = open;
  }
});
render();
})();
</script>
</body>
</html>
```
