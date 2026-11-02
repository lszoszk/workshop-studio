I built a two-State vote-comparison tool for the Human Rights Council dataset: pick any two Council members, see how many recorded votes they both took part in and how often they agreed, a stacked year-by-year timeline, a filter for resolutions/amendments/both, and a full list of their differing votes with links and roll-call-vs-official-totals warnings.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Compare two States' votes at the Human Rights Council</title>
<style>
:root{
  --accent:#1f6fb2; --accent-dark:#175a92; --ink:#1c2733; --muted:#5b6b7b;
  --bg:#f4f6f9; --card:#ffffff; --border:#dfe5ec;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:24px 20px 48px}
header.page{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px 24px;margin-bottom:18px}
h1{font-size:24px;margin:0 0 6px;color:var(--accent-dark)}
.desc{margin:0;color:var(--muted);font-size:15px}
.card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:18px 22px;margin-bottom:18px}
.card h2{font-size:18px;margin:0 0 12px;color:var(--accent-dark)}
.controls{display:flex;flex-wrap:wrap;gap:14px 18px;align-items:flex-end}
.field{display:flex;flex-direction:column;gap:6px}
.field label{font-size:14px;font-weight:600;color:var(--muted)}
select{padding:9px 10px;border:1px solid #c6d2de;border-radius:7px;font-size:16px;background:#fff;color:var(--ink);min-width:250px;max-width:100%}
button{cursor:pointer;font-size:15px}
.swap{padding:9px 12px;border:1px solid #c6d2de;border-radius:7px;background:#fff;color:var(--accent-dark);font-weight:600}
.swap:hover{background:#eef4fa}
.seg{display:inline-flex;border:1px solid #c6d2de;border-radius:8px;overflow:hidden}
.seg button{padding:9px 14px;border:none;background:#fff;color:#33414f;border-right:1px solid #e3e9ef}
.seg button:last-child{border-right:none}
.seg button.active{background:var(--accent);color:#fff;font-weight:600}
.hint{font-size:13.5px;color:var(--muted);margin:10px 0 0}
.notice{display:none;margin-top:12px;padding:8px 12px;border-radius:7px;background:#e8f1f9;color:var(--accent-dark);font-size:14.5px}
.notice.show{display:block}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:14px}
.stat{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 18px}
.stat .num{font-size:30px;font-weight:700;color:var(--accent)}
.stat .lbl{font-weight:600;margin-top:2px}
.stat .sub{color:var(--muted);font-size:14px;margin-top:2px}
.note{font-size:13px;color:var(--muted);margin-top:9px}
code{background:#eef1f5;padding:1px 5px;border-radius:4px;font-size:12.5px}
.chart-box{position:relative;height:320px}
.empty{padding:14px 0;color:var(--muted)}
.vote-row{padding:14px 0;border-top:1px solid var(--border)}
.vote-row:first-child{border-top:none;padding-top:4px}
.vote-meta{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;font-size:14px;color:var(--muted)}
.badge{font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;background:#e8f1f9;color:var(--accent-dark);padding:2px 8px;border-radius:4px;font-weight:700}
.symbol{font-weight:600;color:var(--accent)}
.vote-title{font-weight:600;margin:6px 0 8px;font-size:16.5px}
.vote-cmp{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:15px}
.who{font-weight:600}
.vs{color:var(--muted);font-size:12.5px;text-transform:uppercase;letter-spacing:.05em}
.chip{display:inline-block;padding:2px 12px;border-radius:999px;font-weight:700;font-size:14px}
.chip.Y{background:#e3f2e8;color:#1c7a3d}
.chip.N{background:#fbe7e4;color:#b3372a}
.chip.A,.chip.other{background:#eceff3;color:#4a5a6a}
.warn{margin-top:9px;font-size:13.5px;background:#fff6e0;border:1px solid #eed488;color:#7a5b00;padding:6px 10px;border-radius:6px}
table.fallback{border-collapse:collapse;margin-top:8px}
table.fallback th,table.fallback td{border:1px solid var(--border);padding:5px 12px;text-align:left;font-size:14.5px}
table.fallback th{background:#eef4fa}
footer{color:var(--muted);font-size:13.5px;padding:0 4px}
</style>
</head>
<body>
<div class="wrap">

<header class="page">
  <h1>Compare two States' votes at the Human Rights Council</h1>
  <p class="desc" id="dataDesc"></p>
</header>

<section class="card">
  <h2>1 · Choose the two States and the kind of vote</h2>
  <div class="controls">
    <div class="field"><label for="selA">State A</label><select id="selA"></select></div>
    <button class="swap" id="swapBtn" title="Swap State A and State B">⇄ Swap</button>
    <div class="field"><label for="selB">State B</label><select id="selB"></select></div>
    <div class="field"><label id="kindLabel">Kind of vote</label>
      <div class="seg" id="kindSeg" role="group" aria-labelledby="kindLabel">
        <button data-kind="all" class="active">Both</button>
        <button data-kind="resolution">Resolutions</button>
        <button data-kind="amendment">Amendments</button>
      </div>
    </div>
  </div>
  <div class="notice" id="sameNotice"></div>
  <p class="hint" id="memberHint"></p>
</section>

<section class="card">
  <h2>2 · Headline numbers <span id="filterLine" style="font-weight:400;color:var(--muted);font-size:14px"></span></h2>
  <div class="stats">
    <div class="stat">
      <div class="num" id="statBoth">–</div>
      <div class="lbl">Recorded votes both took part in</div>
      <div class="sub" id="statBothSub"></div>
      <div class="note">How this is computed: filtered records where both selected States have an entry in the roll call (<code>votes</code>).</div>
    </div>
    <div class="stat">
      <div class="num" id="statSame">–</div>
      <div class="lbl">Voted the same way</div>
      <div class="sub" id="statSameSub"></div>
      <div class="note">How this is computed: of those common votes, the ones where both cast the identical code (Y / N / A).</div>
    </div>
    <div class="stat">
      <div class="num" id="statDiff">–</div>
      <div class="lbl">Voted differently</div>
      <div class="sub" id="statDiffSub"></div>
      <div class="note">How this is computed: common votes where the two codes differ — each one is listed in section 4 below.</div>
    </div>
    <div class="stat">
      <div class="num" id="statPart" style="font-size:21px;line-height:1.35">–</div>
      <div class="lbl">Votes each State took part in</div>
      <div class="sub" id="statPartSub"></div>
      <div class="note">How this is computed: filtered records where that State appears in the roll call, regardless of the other State.</div>
    </div>
  </div>
</section>

<section class="card">
  <h2>3 · Timeline by year</h2>
  <div class="chart-box"><canvas id="chart"></canvas></div>
  <div class="empty" id="chartEmpty" style="display:none"></div>
  <p class="note">How this is computed: for each year, the filtered votes in which both States took part, split into “voted the same” and “voted differently”. Counts come from counting each record's roll call (<code>votes</code>), not from the official totals. Years with no common vote are omitted.</p>
</section>

<section class="card">
  <h2>4 · Votes where they differed</h2>
  <p class="hint" id="listInfo"></p>
  <div id="diffList"></div>
  <p class="note">How this is computed: every filtered vote where the two States' codes differ, newest first. The symbol links to the UN document (<code>doc_url</code>) in a new tab; where that is missing, the OHCHR record page (<code>record_url</code>) is used instead. Rows marked ⚠ are votes where counting the roll call gives different Y/N/A numbers than the official yes/no/abstain totals — both figures are shown, neither is corrected.</p>
</section>

<footer id="foot"></footer>
</div>

<script>
(function(){
"use strict";
var HRC = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.hrc) ? window.WORKSHOP_DATA.hrc : {};
var records = Array.isArray(HRC.records) ? HRC.records : [];
var countryNames = HRC.countries || {};
var voteCodes = HRC.vote_codes || {};

function $(s){ return document.querySelector(s); }
function esc(s){
  return String(s==null?'':s).replace(/[&<>"']/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
  });
}
function nameOf(code){ return countryNames[code] || code; }
function voteLabel(c){
  var u = String(c==null?'':c).toUpperCase();
  if (voteCodes && typeof voteCodes[u]==='string' && voteCodes[u]) return voteCodes[u];
  return {Y:'Yes', N:'No', A:'Abstain'}[u] || (u || '—');
}
function kindOf(r){ return String((r && r.kind) || '').toLowerCase(); }
function kindLabel(r){
  var k = kindOf(r);
  if (k==='resolution') return 'Resolution';
  if (k==='amendment') return 'Amendment';
  return (r && r.kind) ? String(r.kind) : 'Vote';
}
function yearOf(r){
  if (r && typeof r.year==='number') return r.year;
  var m = (r && r.date) ? String(r.date).match(/^(\d{4})/) : null;
  return m ? +m[1] : null;
}
function rollCall(r){
  var c = {Y:0, N:0, A:0, other:0};
  if (r && r.votes){
    Object.keys(r.votes).forEach(function(k){
      var u = String(r.votes[k]).toUpperCase();
      if (u==='Y'||u==='N'||u==='A') c[u]++; else c.other++;
    });
  }
  return c;
}
function totalsMismatch(r){
  if (!r) return false;
  var y=r.yes, n=r.no, a=r.abstain;
  if (typeof y!=='number' || typeof n!=='number' || typeof a!=='number') return false;
  var rc = rollCall(r);
  return rc.Y!==y || rc.N!==n || rc.A!==a || rc.other>0;
}

/* Only States that appear as Council members in at least one recorded vote */
var memberSet = {};
records.forEach(function(r){
  if (r && r.votes) Object.keys(r.votes).forEach(function(k){ memberSet[k]=true; });
});
var members = Object.keys(memberSet).map(function(code){
  return {code:code, name: countryNames[code] || code};
}).sort(function(a,b){ return a.name.localeCompare(b.name, undefined, {sensitivity:'base'}); });

var state = {
  a: members.length ? members[0].code : null,
  b: members.length > 1 ? members[1].code : (members.length ? members[0].code : null),
  kind: 'all'
};
var chart = null;

function pct(part, whole){ return whole>0 ? Math.round(part/whole*1000)/10 : null; }

function fillSelect(sel){
  sel.innerHTML = '';
  members.forEach(function(m){
    var o = document.createElement('option');
    o.value = m.code;
    o.textContent = (m.name===m.code) ? m.code : m.name + ' (' + m.code + ')';
    sel.appendChild(o);
  });
}

function renderChart(byYear){
  var years = Object.keys(byYear).map(Number).sort(function(a,b){ return a-b; });
  var canvas = $('#chart'), box = $('#chartEmpty');
  if (chart){ chart.destroy(); chart = null; }
  if (!years.length){
    canvas.style.display='none'; box.style.display='block';
    box.textContent = 'No recorded votes under this filter in which both States took part.';
    return;
  }
  var sameData = years.map(function(y){ return byYear[y].same; });
  var diffData = years.map(function(y){ return byYear[y].diff; });
  if (window.Chart){
    canvas.style.display='block'; box.style.display='none';
    chart = new Chart(canvas.getContext('2d'), {
      type:'bar',
      data:{ labels: years.map(String), datasets:[
        {label:'Voted the same',    data:sameData, backgroundColor:'#1f6fb2', stack:'s'},
        {label:'Voted differently', data:diffData, backgroundColor:'#e08a3c', stack:'s'}
      ]},
      options:{
        responsive:true, maintainAspectRatio:false,
        scales:{
          x:{stacked:true, title:{display:true, text:'Year'}},
          y:{stacked:true, beginAtZero:true, ticks:{precision:0}, title:{display:true, text:'Votes both took part in'}}
        },
        plugins:{
          legend:{position:'bottom'},
          tooltip:{callbacks:{label:function(c){ return ' ' + c.dataset.label + ': ' + c.parsed.y; }}}
        }
      }
    });
  } else {
    canvas.style.display='none'; box.style.display='block';
    box.innerHTML = '<table class="fallback"><thead><tr><th>Year</th><th>Voted the same</th><th>Voted differently</th></tr></thead><tbody>'
      + years.map(function(y,i){
          return '<tr><td>'+y+'</td><td>'+sameData[i]+'</td><td>'+diffData[i]+'</td></tr>';
        }).join('') + '</tbody></table>';
  }
}

function renderList(diffs, filteredN, mismatchCount, A, B){
  var info = $('#listInfo');
  info.textContent = diffs.length + ' vote' + (diffs.length===1?'':'s') + ' where ' + nameOf(A) + ' and ' + nameOf(B)
    + ' voted differently (of ' + filteredN + ' filtered votes).'
    + (mismatchCount>0 ? ' ⚠ In ' + mismatchCount + ' of the ' + filteredN + ' filtered votes the roll call differs from the official totals; those rows are marked below.' : '');
  var el = $('#diffList');
  if (!diffs.length){
    el.innerHTML = '<p class="empty">No differing votes under the current filter — the two States voted the same way in every vote they both took part in.</p>';
    return;
  }
  el.innerHTML = diffs.map(function(r){
    var v = r.votes || {};
    var ca = String(v[A]).toUpperCase(), cb = String(v[B]).toUpperCase();
    var clsA = /^[YNA]$/.test(ca) ? ca : 'other';
    var clsB = /^[YNA]$/.test(cb) ? cb : 'other';
    var href = r.doc_url || r.record_url || '';
    var sym = href
      ? '<a class="symbol" target="_blank" rel="noopener" href="' + esc(href) + '">' + esc(r.symbol || '(no symbol)') + '</a>'
      : '<span class="symbol">' + esc(r.symbol || '(no symbol)') + '</span>';
    var meta = [];
    if (r.session) meta.push(r.session);
    if (r.agenda_item) meta.push(r.agenda_item);
    var metaHtml = meta.length ? '<span>· ' + esc(meta.join(' · ')) + '</span>' : '';
    var warn = '';
    if (totalsMismatch(r)){
      var rc = rollCall(r);
      warn = '<div class="warn">⚠ Roll call counted from the votes (Y ' + rc.Y + ' · N ' + rc.N + ' · A ' + rc.A
        + (rc.other ? ' · other ' + rc.other : '')
        + ') differs from the official totals (yes ' + r.yes + ' · no ' + r.no + ' · abstain ' + r.abstain
        + '). Both are shown; neither is corrected.</div>';
    }
    return '<article class="vote-row">'
      + '<div class="vote-meta"><span class="badge">' + esc(kindLabel(r)) + '</span>'
      + '<span>' + esc(r.date || 'date unknown') + (r.year ? ' · ' + esc(r.year) : '') + '</span>'
      + sym + metaHtml + '</div>'
      + '<div class="vote-title">' + esc(r.title || '(untitled vote)') + '</div>'
      + '<div class="vote-cmp"><span class="who">' + esc(nameOf(A)) + '</span> <span class="chip ' + clsA + '">' + esc(voteLabel(ca)) + '</span>'
      + '<span class="vs">vs</span>'
      + '<span class="who">' + esc(nameOf(B)) + '</span> <span class="chip ' + clsB + '">' + esc(voteLabel(cb)) + '</span></div>'
      + warn
      + '</article>';
  }).join('');
}

function render(){
  var A = state.a, B = state.b;
  $('#selA').value = A; $('#selB').value = B;

  var sn = $('#sameNotice');
  if (A && A===B){
    sn.textContent = 'Both selectors are set to ' + nameOf(A) + ' — every vote it took part in counts as “the same”.';
    sn.classList.add('show');
  } else {
    sn.classList.remove('show');
  }

  if (!A || !B || !records.length){
    $('#filterLine').textContent = '';
    $('#statBoth').textContent = '–'; $('#statBothSub').textContent = 'no data';
    $('#statSame').textContent = '–'; $('#statSameSub').textContent = 'no data';
    $('#statDiff').textContent = '–'; $('#statDiffSub').textContent = 'no data';
    $('#statPart').textContent = '–'; $('#statPartSub').textContent = 'no data';
    renderChart({});
    $('#listInfo').textContent = 'No recorded votes available in this dataset.';
    $('#diffList').innerHTML = '';
    return;
  }

  var filtered = records.filter(function(r){
    return state.kind==='all' || kindOf(r)===state.kind;
  });

  var both=0, sameN=0, diffN=0, aPart=0, bPart=0, mismatchCount=0;
  var byYear = {}, diffs = [];
  filtered.forEach(function(r){
    if (totalsMismatch(r)) mismatchCount++;
    var v = r.votes || {};
    var ca = (v[A]!=null) ? String(v[A]).toUpperCase() : null;
    var cb = (v[B]!=null) ? String(v[B]).toUpperCase() : null;
    if (ca) aPart++;
    if (cb) bPart++;
    if (ca && cb){
      both++;
      var y = yearOf(r);
      if (y!=null && !byYear[y]) byYear[y] = {same:0, diff:0};
      if (ca===cb){ sameN++; if (y!=null) byYear[y].same++; }
      else { diffN++; if (y!=null) byYear[y].diff++; diffs.push(r); }
    }
  });
  diffs.sort(function(a,b){
    var da = String(a.date||''), db = String(b.date||'');
    if (da!==db) return da<db ? 1 : -1;
    return String(a.title||'').localeCompare(String(b.title||''));
  });

  var kindTxt = state.kind==='all' ? 'resolutions and amendments' : (state.kind==='resolution' ? 'resolutions only' : 'amendments only');
  $('#filterLine').textContent = ' — showing ' + filtered.length + ' of ' + records.length + ' recorded votes (' + kindTxt + ')';

  $('#statBoth').textContent = both;
  $('#statBothSub').textContent = 'of ' + filtered.length + ' filtered votes';
  $('#statSame').textContent = sameN;
  var ps = pct(sameN, both);
  $('#statSameSub').textContent = both>0 ? (ps + '% of the ' + both + ' votes both took part in') : 'no common votes under this filter';
  $('#statDiff').textContent = diffN;
  var pd = pct(diffN, both);
  $('#statDiffSub').textContent = both>0 ? (pd + '% of the ' + both + ' votes both took part in') : 'no common votes under this filter';
  $('#statPart').textContent = nameOf(A) + ': ' + aPart + ' · ' + nameOf(B) + ': ' + bPart;
  $('#statPartSub').textContent = 'roll-call entries per State (filtered)';

  renderChart(byYear);
  renderList(diffs, filtered.length, mismatchCount, A, B);
}

function init(){
  var yrs = records.map(yearOf).filter(function(y){ return y!=null; });
  var min = yrs.length ? Math.min.apply(null, yrs) : null;
  var max = yrs.length ? Math.max.apply(null, yrs) : null;
  $('#dataDesc').textContent = (HRC.title || 'Human Rights Council recorded votes')
    + ' · ' + records.length + ' recorded votes'
    + (min!=null ? ' · years ' + min + '–' + max : '')
    + ' · ' + members.length + ' States appear as Council members in at least one vote'
    + ' · source: OHCHR recorded-vote records preloaded in this workshop (WORKSHOP_DATA.hrc).';
  $('#memberHint').textContent = 'Only States that were Council members in at least one recorded vote are listed (' + members.length
    + ' States). Every vote is read from each record’s roll call (votes: ISO3 → Y/N/A).';
  $('#foot').textContent = 'All counting, filtering and sorting is done locally in your browser from WORKSHOP_DATA.hrc; nothing is sent anywhere. Chart drawn with Chart.js.';

  var selA = $('#selA'), selB = $('#selB');
  fillSelect(selA); fillSelect(selB);
  selA.value = state.a; selB.value = state.b;
  selA.addEventListener('change', function(){ state.a = selA.value; render(); });
  selB.addEventListener('change', function(){ state.b = selB.value; render(); });
  $('#swapBtn').addEventListener('click', function(){
    var t = state.a; state.a = state.b; state.b = t; render();
  });
  Array.prototype.forEach.call(document.querySelectorAll('#kindSeg button'), function(btn){
    btn.addEventListener('click', function(){
      state.kind = btn.getAttribute('data-kind');
      Array.prototype.forEach.call(document.querySelectorAll('#kindSeg button'), function(b){
        b.classList.toggle('active', b===btn);
      });
      render();
    });
  });

  render();
}
init();
})();
</script>
</body>
</html>
```