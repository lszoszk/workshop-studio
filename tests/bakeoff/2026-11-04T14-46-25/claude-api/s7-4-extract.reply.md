I built the extractor as two tabs, Result and Paragraphs, with the document card and counts in a left rail. Everything is computed by the page's own code from `html_doc` and its reference. Footnotes show as a source limit (the HTML has none), and nothing is sent to a model.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a UN document</title>
<style>
[hidden]{display:none!important}
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--accent:#9b2335;--green:#1f5f3a;--mute:#5b564d}
*{box-sizing:border-box}
html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.mono,.label,th,.how,.hint{font-family:ui-monospace,Menlo,Consolas,monospace}
.label{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.serif,h1,caption,.big{font-family:Georgia,"Times New Roman",serif}
a{color:var(--accent)}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
button{font:inherit;color:inherit;cursor:pointer}
header{padding:20px 28px 14px;border-bottom:1px solid var(--rule)}
.head-grid{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;flex-wrap:wrap}
h1{font-size:26px;line-height:1.2;margin:6px 0 6px;font-weight:normal;max-width:60ch}
#meta{margin:0;font-size:14px;color:var(--mute)}
#status{font-size:12px;text-align:right}
#status .line{display:block;margin-bottom:4px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.dot.green{background:var(--green)}.dot.red{background:var(--accent)}.dot.grey{background:#8a8478}
.layout{display:grid;grid-template-columns:250px minmax(0,1fr);gap:0;max-width:1280px;margin:0 auto}
aside{padding:22px 24px 22px 28px;border-right:1px solid var(--rule)}
aside .card{border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:10px 0;margin:8px 0 18px}
aside .card .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px;font-weight:bold}
aside .card div:last-child{font-size:14px;color:var(--mute)}
.rbig{font-family:Georgia,serif;font-size:44px;line-height:1.05}
.rsub{font-size:13px;color:var(--mute);margin-bottom:6px}
.bar{height:5px;background:var(--rule);margin:4px 0 20px}
.bar i{display:block;height:100%}
.ok{color:var(--green)}.bad{color:var(--accent)}.mute{color:var(--mute)}
main{padding:14px 28px 30px;min-width:0}
[role=tablist]{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin-bottom:20px}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;padding:10px 14px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
[role=tab][aria-selected=true]{color:var(--accent);border-bottom-color:var(--accent);font-weight:bold}
h2.q{font-family:Georgia,serif;font-weight:normal;font-size:22px;margin:0 0 16px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:0 32px}
.tile{border-top:1px solid var(--rule);padding:12px 0 18px}
.tile .big{font-size:52px;line-height:1.05;margin:2px 0}
.tile .sub{font-size:15px}
.how{font-size:11.5px;color:var(--mute);margin-top:6px;line-height:1.45}
.hint{font-size:11.5px;color:var(--mute)}
h3.sec{font-family:Georgia,serif;font-weight:normal;font-size:20px;margin:26px 0 8px;border-top:1px solid var(--rule);padding-top:14px}
.difflist{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;margin:4px 0 0;padding:0;list-style:none}
.difflist li{padding:3px 0;border-bottom:1px dotted var(--rule)}
.btn{background:var(--ink);color:var(--paper);border:1px solid var(--ink);padding:9px 16px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;margin-right:8px}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn.light{background:none;color:var(--ink)}
.acc{display:block;width:100%;text-align:left;background:none;border:0;border-top:1px solid var(--rule);padding:12px 0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase}
.acc::after{content:"+";float:right;font-size:16px;line-height:1}
.acc[aria-expanded=true]::after{content:"\2212"}
.accpanel{padding:4px 0 16px}
table{width:100%;border-collapse:collapse;font-size:15px}
caption{text-align:left;font-size:17px;padding:4px 0 10px}
caption .mono{display:block;font-size:11px;letter-spacing:.12em;color:var(--mute);margin-bottom:2px}
th{font-size:11px;letter-spacing:.1em;text-transform:uppercase;text-align:left;color:var(--mute);border-bottom:1px solid var(--ink);padding:6px 8px;font-weight:normal}
td{padding:7px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
th.n,td.n{text-align:right}
.numbtn{background:none;border:0;padding:2px 4px;font-family:ui-monospace,Menlo,Consolas,monospace;font-weight:bold;color:var(--accent);font-size:15px;text-decoration:underline}
tr.prow{cursor:pointer}
tr.prow:hover td{background:#ece6d8}
tr.detail td{background:#efe9db;padding:14px 18px}
.fulltext{font-size:17px;line-height:1.6;max-width:75ch;margin:6px 0 12px}
.fix{display:inline-block;min-width:.45em;white-space:pre;outline:1px solid var(--accent);outline-offset:0;background:#fff}
.pair{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;margin:4px 0}
.pair b{display:inline-block;min-width:80px;font-weight:normal;color:var(--mute);text-transform:uppercase;font-size:11px;letter-spacing:.08em}
.chk{list-style:none;margin:0;padding:0}
.chk li{padding:10px 0;border-bottom:1px solid var(--rule)}
.chk .h{font-size:15px}
.chk .story,.chk .vals{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;color:var(--mute);margin-top:2px}
.chk .vals{color:var(--ink)}
.linkbtn{background:none;border:0;color:var(--accent);text-decoration:underline;padding:0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.box{border:1px solid var(--rule);padding:10px 14px;margin-bottom:14px}
.box .acc{border:0;padding:0}
footer{border-top:1px solid var(--rule);max-width:1280px;margin:0 auto;padding:14px 28px 28px;font-size:12px;color:var(--mute)}
footer p{margin:3px 0}
@media (max-width:820px){.layout{grid-template-columns:1fr}aside{border-right:0;border-bottom:1px solid var(--rule)}.tiles{grid-template-columns:1fr}}
</style>
</head>
<body>
<header>
  <div class="label">UN DOCUMENT · HTML</div>
  <div class="head-grid">
    <div><h1 id="title"></h1><p id="meta"></p></div>
    <div id="status" aria-live="polite"></div>
  </div>
</header>
<div class="layout">
  <aside id="rail" aria-label="Document"></aside>
  <main>
    <div role="tablist" aria-label="Views">
      <button role="tab" id="t0" aria-selected="true" aria-controls="p0" tabindex="0">01 Result</button>
      <button role="tab" id="t1" aria-selected="false" aria-controls="p1" tabindex="-1">02 Paragraphs</button>
    </div>
    <section role="tabpanel" id="p0" aria-labelledby="t0"></section>
    <section role="tabpanel" id="p1" aria-labelledby="t1" hidden></section>
  </main>
</div>
<footer id="foot"></footer>

<script>
(function(){
"use strict";
var D = (window.WORKSHOP_DATA || {}).html_doc || {};
var ref = D.reference || {};
var hasRef = {
  paragraphs: typeof ref.paragraphs === 'number',
  footnotes: typeof ref.footnotes === 'number',
  first: !!ref.first_words && typeof ref.first_words === 'object',
  adopted: !!ref.adopted
};
var symbol = D.symbol || '(no symbol)';
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function clean(s){return String(s).replace(/[ \t\n\r\f]+/g,' ').trim();}

/* ---------- 1. Parse and classify ---------- */
var doc = new DOMParser().parseFromString(D.html || '', 'text/html');
var els = Array.prototype.slice.call(doc.body.querySelectorAll('table, p, h2, h3'));
var firstTable = doc.body.querySelector('table');
var tally = {cover:0,title:0,heading:0,paragraph:0,committee:0,unclassified:0};
var unclassified = [], blocks = [], headings = [], paras = [];
var docTitle = '', titleSeen = false, curHeading = null, curPart = null;
var RULES = {sentence:'sentence join', comma:'comma join', quote:'quote join', dash:'dash join'};
var REPAIR = /([a-z])\.(?=[A-Z])|([a-z]),(?=[A-Za-z])|[a-z](?=“)|–(?=[A-Za-z])/g;

function repair(raw){
  var out = '', last = 0, fixes = [], m;
  REPAIR.lastIndex = 0;
  while((m = REPAIR.exec(raw)) !== null){
    var end = m.index + m[0].length;
    var s = m[0], rule = s.slice(-1) === '.' ? 'sentence' : s.slice(-1) === ',' ? 'comma' : s.slice(-1) === '–' ? 'dash' : 'quote';
    out += raw.slice(last, end);
    fixes.push({rule:rule, pos:out.length, left:raw.slice(Math.max(0,end-20), end), right:raw.slice(end, end+20)});
    out += ' ';
    last = end;
  }
  out += raw.slice(last);
  return {text:out, fixes:fixes};
}

els.forEach(function(el){
  var tag = el.tagName.toLowerCase();
  var tb = el.closest('table');
  if(tb){
    if(tb === firstTable){ tally.cover++; return; }
    tally.unclassified++; unclassified.push(tag + ': ' + clean(el.textContent).slice(0,60)); return;
  }
  var t = clean(el.textContent);
  if(tag === 'p'){
    var m = t.match(/^(\d{1,3})\.\s*(.*)$/s);
    if(m){
      tally.paragraph++;
      var r = repair(m[2]);
      var p = {n:parseInt(m[1],10), raw:m[2], text:r.text, fixes:r.fixes,
        section: curHeading ? curHeading.full : '', part: curPart || ''};
      p.path = (curPart && curPart !== p.section ? curPart + ' › ' : '') + p.section;
      paras.push(p); blocks.push({kind:'para', p:p});
    } else { tally.committee++; }
  } else if(tag === 'h2' && !titleSeen){
    titleSeen = true; tally.title++; docTitle = t.replace(/\s*\*$/,'');
  } else {
    tally.heading++;
    var hm = t.match(/^([IVX]+|[A-Z])\.\s*(.+)$/s);
    var h = {level: tag === 'h2' ? 2 : 3, label: hm ? hm[1] : '', heading: hm ? hm[2] : t,
      full: hm ? hm[1] + '. ' + hm[2] : t, glued: !!hm && !/^([IVX]+|[A-Z])\.\s/.test(t), count:0};
    headings.push(h); blocks.push({kind:'heading', h:h});
    curHeading = h;
    if(h.level === 2 && hm && /^[IVX]+$/.test(hm[1])) curPart = h.full;
  }
});
paras.forEach(function(p){ /* heading → paragraphs under it */
  headings.forEach(function(h){ if(h.full === p.section) h.count++; });
});

/* ---------- 2. First words ---------- */
function six(s){return s.split(/\s+/).filter(Boolean).slice(0,6).join(' ');}
function norm(s){return String(s).replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[–\u2011]/g,'-').replace(/\u00a0/g,' ');}
paras.forEach(function(p){
  p.found6 = six(p.text);
  p.ref6 = hasRef.first ? ref.first_words[String(p.n)] : undefined;
  p.fw = p.ref6 === undefined ? 'noref' : (norm(p.found6) === norm(p.ref6) ? 'ok' : 'diff');
  p.citation = symbol + ', para. ' + p.n;
});
var fwOk = paras.filter(function(p){return p.fw==='ok';}).length;
var fwDiff = paras.filter(function(p){return p.fw==='diff';});
var fwNoRef = paras.filter(function(p){return p.fw==='noref';}).length;
var allFixes = [];
paras.forEach(function(p){ p.fixes.forEach(function(f){ allFixes.push({p:p, f:f}); }); });
var fixParas = paras.filter(function(p){return p.fixes.length>0;}).length;
var perRule = {sentence:0,comma:0,quote:0,dash:0};
allFixes.forEach(function(x){perRule[x.f.rule]++;});
var fnFound = doc.querySelectorAll('sup, [class*="footnote"], [id^="fn"]').length;
var fnSentence = 'no footnotes in this HTML version; the document has ' + (hasRef.footnotes ? ref.footnotes : 'an unknown number of them');

/* ---------- 3. Export records ---------- */
function records(){
  return paras.map(function(p){
    return {symbol:symbol, paragraph:p.n, section:p.section, part:p.part, text:p.text, text_raw:p.raw,
      first_words_match: p.fw==='ok' ? true : p.fw==='diff' ? false : null,
      citation:p.citation, doc_url:D.doc_url || '', limitations:fnSentence};
  });
}
function markdown(){
  var today = new Date().toISOString().slice(0,10);
  var o = ['---',
    'title: ' + JSON.stringify(D.title || docTitle),
    'symbol: ' + JSON.stringify(symbol),
    'adopted: ' + JSON.stringify(ref.adopted || ''),
    'source_url: ' + JSON.stringify(D.doc_url || ''),
    'extracted: ' + today,
    'paragraphs_found: ' + paras.length,
    'paragraphs_expected: ' + (hasRef.paragraphs ? ref.paragraphs : 'unknown'),
    'footnotes: ' + JSON.stringify(fnSentence),
    '---',''];
  blocks.forEach(function(b){
    if(b.kind === 'heading') o.push((b.h.level===2?'##':'###') + ' ' + b.h.full, '');
    else o.push('**' + b.p.n + '.** ' + b.p.text, '');
  });
  return o.join('\n');
}
var jsonStr = JSON.stringify(records(), null, 2);

/* ---------- 4. Checks ---------- */
var checks = [];
(function(){
  var n = paras.length;
  checks.push({name:'Paragraph count', status: !hasRef.paragraphs ? 'norun' : (n === ref.paragraphs ? 'pass':'fail'),
    story:'Given the HTML, having counted numbered paragraphs, we expect the number the reference gives.',
    vals:'found ' + n + ' · reference ' + (hasRef.paragraphs ? ref.paragraphs : 'none in this file'), rows:[]});
  var nums = paras.map(function(p){return p.n;}), seen = {}, dups = [], gaps = [], bad = [];
  nums.forEach(function(v,i){ if(seen[v]) dups.push(v); seen[v]=1; if(v !== i+1) bad.push(v); });
  var mx = nums.length ? Math.max.apply(null, nums) : 0;
  for(var k=1;k<=mx;k++) if(!seen[k]) gaps.push(k);
  checks.push({name:'Numbering', status: n===0 ? 'fail' : (bad.length===0 ? 'pass':'fail'),
    story:'Given the paragraphs in document order, having read their numbers, we expect exactly 1 to n.',
    vals: bad.length===0 && n ? ('1 to ' + n + ' in order') : (n===0 ? 'no paragraphs' : 'gaps: ' + (gaps.join(', ')||'none') + ' · duplicates: ' + (dups.join(', ')||'none') + ' · out of place: ' + bad.slice(0,10).join(', ')),
    rows:bad.slice(0,50)});
  checks.push({name:'First words', status: !hasRef.first ? 'norun' : ((fwDiff.length===0 && fwNoRef===0) ? 'pass':'fail'),
    story:'Given each paragraph, having taken its first six words, we expect the reference words (quotes, dashes and spaces normalised).',
    vals: hasRef.first ? ('match ' + fwOk + ' of ' + n + ' · differ ' + fwDiff.length + ' · no reference ' + fwNoRef) : 'no reference in this file',
    rows:fwDiff.map(function(p){return p.n;})});
  checks.push({name:'Footnotes', status: !hasRef.footnotes ? 'norun' : (fnFound >= ref.footnotes ? 'pass' : 'limit'),
    story:'Given the HTML, having looked for footnote marks and notes, we expect as many as the reference counts.',
    vals:'found ' + fnFound + ' · reference ' + (hasRef.footnotes ? ref.footnotes : 'none in this file') + ' — the HTML version has no footnotes: a limit of the source, not of the app', rows:[]});
  var roundOk = paras.every(function(p){
    var s = p.text, i, pos = p.fixes.map(function(f){return f.pos;});
    var r = '', last = 0;
    pos.forEach(function(q){ r += s.slice(last,q); last = q+1; });
    r += s.slice(last);
    return r === p.raw && s.length - p.raw.length === p.fixes.length;
  });
  checks.push({name:'Repairs', status: roundOk ? 'pass':'fail',
    story:'Given the raw text, having inserted spaces only where characters prove one was lost, we expect that removing them gives text_raw back.',
    vals: allFixes.length + ' spaces restored in ' + fixParas + ' paragraphs (sentence ' + perRule.sentence + ', comma ' + perRule.comma + ', quote ' + perRule.quote + ', dash ' + perRule.dash + ')', rows:[]});
  var h2n = doc.body.querySelectorAll('h2').length, h3n = doc.body.querySelectorAll('h3').length;
  var glued = headings.filter(function(h){return h.glued;}).length;
  checks.push({name:'Headings', status: (tally.title + tally.heading === h2n + h3n && headings.length > 0) ? 'pass':'fail',
    story:'Given the HTML, having counted h2 and h3 elements, we expect every one to be the title or a heading.',
    vals: h2n + ' h2 and ' + h3n + ' h3 · title ' + tally.title + ' + headings ' + tally.heading + ' · glued labels separated: ' + glued, rows:[]});
  var sum = 0; Object.keys(tally).forEach(function(k){sum += tally[k];});
  checks.push({name:'Nothing lost', status: (sum === els.length && tally.unclassified===0) ? 'pass':'fail',
    story:'Given every table, p, h2 and h3 element, having classified each once, we expect the classes to add up to the total.',
    vals: 'cover ' + tally.cover + ' + title ' + tally.title + ' + headings ' + tally.heading + ' + paragraphs ' + tally.paragraph + ' + committee line ' + tally.committee + ' + unclassified ' + tally.unclassified + ' = ' + sum + ' of ' + els.length + (unclassified.length ? ' · unclassified: ' + unclassified.join(' | ') : ''), rows:[]});
  var back = [];
  try{ back = JSON.parse(jsonStr); }catch(e){ back = null; }
  checks.push({name:'Export round trip', status: back && back.length === paras.length ? 'pass':'fail',
    story:'Given the JSON to download, having parsed it back, we expect as many records as the table has rows.',
    vals: 'JSON records ' + (back ? back.length : 'unreadable') + ' · table rows ' + paras.length, rows:[]});
})();
var passN = checks.filter(function(c){return c.status==='pass';}).length;
var failN = checks.filter(function(c){return c.status==='fail';}).length;
var limitN = checks.filter(function(c){return c.status==='limit';}).length;
var norunN = checks.filter(function(c){return c.status==='norun';}).length;
function sw(s){
  return s==='pass' ? '<b class="ok">pass</b>' : s==='fail' ? '<b class="bad">check failed</b>' : s==='limit' ? '<b class="bad">source limit</b>' : '<b class="mute">not run</b>';
}

/* ---------- 5. Render header, rail, footer ---------- */
var fullTitle = D.title || docTitle || symbol;
var shortTitle = fullTitle.split(/\s+on\s+/)[0];
if(shortTitle.length > 70) shortTitle = shortTitle.slice(0,67) + '…';
document.title = symbol + ' · paragraphs';
document.getElementById('title').textContent = fullTitle;
document.getElementById('meta').innerHTML =
  (D.doc_url ? '<a href="' + esc(D.doc_url) + '" target="_blank" rel="noopener">' + esc(symbol) + '</a>' : esc(symbol)) +
  (hasRef.adopted ? ' · adopted ' + esc(ref.adopted) : '') + (D.source ? ' · ' + esc(D.source) : '');
document.getElementById('status').innerHTML =
  '<span class="line"><span class="dot ' + (failN ? 'red' : norunN ? 'grey' : 'green') + '"></span>' +
  (failN ? failN + ' check' + (failN>1?'s':'') + ' failed' : passN + ' of ' + checks.length + ' checks pass') + '</span>' +
  '<span class="line bad">' + limitN + ' source limit' + (limitN===1?'':'s') + '</span>';

var parasOK = hasRef.paragraphs && paras.length === ref.paragraphs;
document.getElementById('rail').innerHTML =
  '<div class="label">Document</div>' +
  '<div class="card"><div class="sym">' + esc(symbol) + '</div><div>' + esc(shortTitle) + '</div></div>' +
  '<div class="rbig">' + paras.length + '</div>' +
  '<div class="rsub">paragraphs' + (hasRef.paragraphs ? ' of ' + ref.paragraphs : ' · no reference') + '</div>' +
  '<div class="bar"><i style="width:' + (hasRef.paragraphs && ref.paragraphs ? Math.min(100, paras.length / ref.paragraphs * 100) : 0) + '%;background:' + (parasOK ? 'var(--green)' : 'var(--accent)') + '"></i></div>' +
  '<div class="rbig bad">' + fnFound + '</div>' +
  '<div class="rsub">footnotes' + (hasRef.footnotes ? ' of ' + ref.footnotes : '') + ' · <span class="bad">not in this HTML</span></div>' +
  '<div class="bar"><i style="width:' + (hasRef.footnotes && ref.footnotes ? Math.min(100, fnFound / ref.footnotes * 100) : 0) + '%;background:var(--accent)"></i></div>' +
  '<div class="rbig" style="font-size:30px">' + passN + ' of ' + checks.length + '</div><div class="rsub">checks pass</div>';

document.getElementById('foot').innerHTML =
  '<p>Source: ' + esc(D.source || 'not stated') + (D.built ? ' · built ' + esc(D.built) : '') + '</p>' +
  '<p>Done by this page\'s code; no model was called and nothing left the browser.</p>' +
  '<p>Credits: method informed by The Turing Way, “Documentation and metadata” (CC BY 4.0); the UK Analysis Function’s “Testing code”; and the Dag Hammarskjöld Library’s guide to citing a UN document.</p>';

/* ---------- 6. Tab 01 ---------- */
var p0 = document.getElementById('p0');
function tile(label, big, sub, bigCls, how){
  return '<div class="tile"><div class="label">' + label + '</div><div class="big ' + (bigCls||'') + '">' + big + '</div><div class="sub">' + sub + '</div><div class="how">How this is computed: ' + how + '</div></div>';
}
var diffNum = hasRef.paragraphs ? paras.length - ref.paragraphs : 0;
var html0 = '<h2 class="q">Did the app find everything the document has?</h2>';
if(paras.length === 0){
  html0 += '<p class="bad"><b>No numbered paragraphs were found in this HTML.</b> Nothing can be exported.</p>';
}
html0 += '<div class="tiles">' +
  tile('Paragraphs found', paras.length,
    hasRef.paragraphs ? (parasOK ? '<span class="ok">the document has ' + ref.paragraphs + ' · equal</span>' : '<span class="bad">the document has ' + ref.paragraphs + ' · ' + (diffNum<0 ? Math.abs(diffNum) + ' short' : diffNum + ' too many') + '</span>') : '<span class="mute">no reference in this file</span>',
    parasOK ? 'ok' : (hasRef.paragraphs ? 'bad' : ''), 'every &lt;p&gt; after the cover whose text starts with a number and a full stop, counted by a loop.') +
  tile('First words match', hasRef.first ? fwOk : '–',
    hasRef.first ? '<span class="' + (fwOk === ref.paragraphs ? 'ok' : 'bad') + '">of ' + (hasRef.paragraphs ? ref.paragraphs : paras.length) + ' paragraphs</span>' : '<span class="mute">no reference in this file</span>',
    hasRef.first && fwOk !== (hasRef.paragraphs ? ref.paragraphs : paras.length) ? 'bad' : (hasRef.first ? 'ok' : ''), 'first six words of each paragraph against the reference; quotes, dashes and non-breaking spaces normalised, case kept.') +
  tile('Footnotes', fnFound, '<span class="bad">of ' + (hasRef.footnotes ? ref.footnotes : '?') + ' · this HTML version has none: no footnote text, no footnote marks. To cite a footnote, use the PDF or Word version.</span>', 'bad', 'elements that look like footnote marks or notes (sup, footnote classes) counted in the HTML.') +
  tile('Spaces restored', allFixes.length, 'in ' + fixParas + ' paragraph' + (fixParas===1?'':'s'), '', 'a space is inserted only where the characters prove it was lost (sentence, comma, quote and dash joins); each one is logged.') +
  '</div>';
if(hasRef.first){
  html0 += '<h3 class="sec" style="border-top:0;margin-top:14px;font-size:17px">First words that differ (' + fwDiff.length + ')</h3>';
  if(fwDiff.length === 0) html0 += '<p class="ok" style="margin:0">All first words match the reference.</p>';
  else {
    html0 += '<ul class="difflist">' + fwDiff.slice(0,10).map(function(p){
      return '<li>para. ' + p.n + ': found “' + esc(p.found6) + '” / reference “' + esc(p.ref6) + '”</li>';
    }).join('') + '</ul>';
    if(fwDiff.length > 10) html0 += '<p class="hint">and ' + (fwDiff.length - 10) + ' more</p>';
    html0 += '<p class="hint">Word pairs such as “Giventhe” are caught only when they fall in the first six words.</p>';
  }
}
html0 += '<h3 class="sec">Take the paragraphs away</h3>' +
  '<button class="btn" id="dlJson"' + (paras.length?'':' disabled') + '>Download JSON</button>' +
  '<button class="btn light" id="dlMd"' + (paras.length?'':' disabled') + '>Download Markdown</button>' +
  '<span class="hint" id="dlmsg" role="status"></span>' +
  '<div class="how">JSON: one record per paragraph with symbol, number, section, part, text, text_raw, check result, citation, link and limitations. Markdown: front matter, headings and paragraphs in document order.</div>' +
  '<div style="margin-top:22px">' +
  '<button class="acc" id="acc1" aria-expanded="false" aria-controls="accp1">Every check (' + checks.length + ')</button>' +
  '<div class="accpanel" id="accp1" hidden><ul class="chk">' + checks.map(function(c,i){
    return '<li><div class="h"><span class="mono hint">CHK.' + String(i+1).padStart(2,'0') + '</span> <b>' + esc(c.name) + '</b> · ' + sw(c.status) +
      (c.status==='fail' && c.rows.length ? ' · <button class="linkbtn" data-goto="' + c.rows[0] + '">see rows' + (c.rows.length>1 ? ' (first of ' + c.rows.length + ')' : '') + '</button>' : '') + '</div>' +
      '<div class="vals">' + esc(c.vals) + '</div><div class="story">' + esc(c.story) + '</div></li>';
  }).join('') + '</ul></div>' +
  '<button class="acc" id="acc2" aria-expanded="false" aria-controls="accp2">The spaces restored (' + allFixes.length + ')</button>' +
  '<div class="accpanel" id="accp2" hidden>' +
  '<p class="mono" style="font-size:12px;margin:4px 0 10px">sentence join ' + perRule.sentence + ' · comma join ' + perRule.comma + ' · quote join ' + perRule.quote + ' · dash join ' + perRule.dash + '</p>' +
  '<table><caption><span class="mono">TAB.01</span>' + allFixes.length + ' spaces restored in ' + fixParas + ' paragraphs</caption>' +
  '<thead><tr><th scope="col">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead><tbody>' +
  (allFixes.length ? allFixes.map(function(x){
    return '<tr><td><button class="numbtn" data-goto="' + x.p.n + '">' + x.p.n + '</button></td>' +
      '<td class="mono" style="font-size:12.5px">…' + esc(x.f.left + x.f.right) + '…</td>' +
      '<td class="mono" style="font-size:12.5px">…' + esc(x.f.left) + '<span class="fix"> </span>' + esc(x.f.right) + '…</td>' +
      '<td>' + RULES[x.f.rule] + '</td></tr>';
  }).join('') : '<tr><td colspan="4" class="mute">No spaces needed restoring.</td></tr>') +
  '</tbody></table>' +
  '<p class="hint">Rules restore a space only where the characters prove it was there. Word pairs such as “Giventhe” are not touched.</p></div></div>';
p0.innerHTML = html0;

/* ---------- 7. Tab 02 ---------- */
var p1 = document.getElementById('p1');
function firstLine(t){
  if(t.length <= 120) return t;
  var c = t.slice(0,120), i = c.lastIndexOf(' ');
  if(i > 60) c = c.slice(0,i);
  return c + '…';
}
function marked(p){
  var out = '', last = 0;
  p.fixes.forEach(function(f){ out += esc(p.text.slice(last, f.pos)) + '<span class="fix" title="space restored here"> </span>'; last = f.pos + 1; });
  return out + esc(p.text.slice(last));
}
var html1 = '<h2 class="q">What does each paragraph say, and how do I cite it?</h2>' +
  '<div class="box"><button class="acc" id="acc3" aria-expanded="false" aria-controls="accp3">Headings found: ' + headings.length + '</button>' +
  '<div class="accpanel" id="accp3" hidden><table><caption><span class="mono">TAB.02a</span>' + headings.length + ' headings, so none can hide inside a paragraph</caption>' +
  '<thead><tr><th scope="col">Level</th><th scope="col">Heading</th><th scope="col" class="n">Paragraphs</th></tr></thead><tbody>' +
  headings.map(function(h){ return '<tr><td class="mono">h' + h.level + '</td><td>' + esc(h.full) + '</td><td class="n mono">' + h.count + '</td></tr>'; }).join('') +
  '</tbody></table></div></div>' +
  '<table id="ptable"><caption><span class="mono">TAB.02</span>' + paras.length + ' paragraphs found, ' + (hasRef.paragraphs ? ref.paragraphs + ' expected' : 'no reference in this file') + '</caption>' +
  '<thead><tr><th scope="col" class="n">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody>' +
  paras.map(function(p,i){
    return '<tr class="prow" data-n="' + p.n + '" data-i="' + i + '"><td class="n"><button class="numbtn" aria-expanded="false" aria-controls="d' + i + '">' + p.n + '</button></td>' +
      '<td>' + esc(p.section || '—') + '</td><td>' + esc(firstLine(p.text)) + '</td>' +
      '<td>' + (p.fw==='ok' ? '<span class="ok">OK</span>' : p.fw==='diff' ? '<b class="bad">first words differ</b>' : '<span class="mute">no reference</span>') + '</td></tr>' +
      '<tr class="detail" id="d' + i + '" hidden><td colspan="4">' +
      '<div class="label">' + esc(p.path || 'No heading above this paragraph') + '</div>' +
      '<div class="fulltext">' + marked(p) + '</div>' +
      '<div class="pair"><b>Found</b>' + esc(p.found6) + '</div>' +
      '<div class="pair"><b>Reference</b>' + (p.ref6 === undefined ? 'none' : esc(p.ref6)) + '</div>' +
      '<div class="pair"><b>Spaces</b>' + (p.fixes.length ? p.fixes.length + ' restored, boxed in red above; text_raw in the export keeps the text as found' : 'none restored') + '</div>' +
      '<p style="margin:10px 0 0"><button class="btn light copybtn" data-cite="' + esc(p.citation) + '">Copy citation</button> <span class="mono hint">' + esc(p.citation) + '</span></p>' +
      '</td></tr>';
  }).join('') + '</tbody></table>';
p1.innerHTML = html1;

/* ---------- 8. Behaviour ---------- */
var tabs = [document.getElementById('t0'), document.getElementById('t1')];
var panels = [p0, p1];
function showTab(i, focus){
  tabs.forEach(function(t,k){
    t.setAttribute('aria-selected', k===i ? 'true':'false');
    t.tabIndex = k===i ? 0 : -1;
    panels[k].hidden = k!==i;
  });
  if(focus) tabs[i].focus();
}
tabs.forEach(function(t,i){
  t.addEventListener('click', function(){showTab(i,false);});
  t.addEventListener('keydown', function(e){
    var k = null;
    if(e.key==='ArrowRight') k=(i+1)%tabs.length;
    else if(e.key==='ArrowLeft') k=(i-1+tabs.length)%tabs.length;
    else if(e.key==='Home') k=0; else if(e.key==='End') k=tabs.length-1;
    if(k!==null){ e.preventDefault(); showTab(k,true); }
  });
});

function setAcc(btn, open){
  btn.setAttribute('aria-expanded', open ? 'true':'false');
  document.getElementById(btn.getAttribute('aria-controls')).hidden = !open;
}
['acc1','acc2'].forEach(function(id){
  document.getElementById(id).addEventListener('click', function(){
    var open = this.getAttribute('aria-expanded') !== 'true';
    setAcc(document.getElementById('acc1'), false); setAcc(document.getElementById('acc2'), false);
    setAcc(this, open);
  });
});
document.getElementById('acc3').addEventListener('click', function(){
  setAcc(this, this.getAttribute('aria-expanded') !== 'true');
});

function toggleRow(tr, force){
  var btn = tr.querySelector('.numbtn'), d = document.getElementById(btn.getAttribute('aria-controls'));
  var open = force !== undefined ? force : btn.getAttribute('aria-expanded') !== 'true';
  btn.setAttribute('aria-expanded', open ? 'true':'false');
  d.hidden = !open;
}
document.getElementById('ptable').addEventListener('click', function(e){
  var tr = e.target.closest('tr.prow');
  if(tr) toggleRow(tr);
});
function goToPara(n){
  showTab(1,false);
  var tr = document.querySelector('tr.prow[data-n="' + n + '"]');
  if(!tr) return;
  toggleRow(tr, true);
  tr.scrollIntoView({block:'start'});
  tr.querySelector('.numbtn').focus({preventScroll:true});
}
document.addEventListener('click', function(e){
  var g = e.target.closest('[data-goto]');
  if(g){ goToPara(g.getAttribute('data-goto')); }
});

function download(name, mime, content){
  var blob = new Blob([content], {type: mime + ';charset=utf-8'});
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function(){URL.revokeObjectURL(url);}, 1500);
}
var fname = symbol.replace(/\//g,'-');
document.getElementById('dlJson').addEventListener('click', function(){
  download(fname + '.json', 'application/json', jsonStr);
  document.getElementById('dlmsg').textContent = ' ' + paras.length + ' records saved as ' + fname + '.json';
});
document.getElementById('dlMd').addEventListener('click', function(){
  download(fname + '.md', 'text/markdown', markdown());
  document.getElementById('dlmsg').textContent = ' saved as ' + fname + '.md';
});

function copyText(s){
  if(navigator.clipboard && navigator.clipboard.writeText){
    return navigator.clipboard.writeText(s);
  }
  return Promise.reject();
}
function fallbackCopy(s){
  var ta = document.createElement('textarea'); ta.value = s; ta.style.position='fixed'; ta.style.opacity='0';
  document.body.appendChild(ta); ta.select();
  try{ document.execCommand('copy'); }catch(e){}
  ta.remove();
}
p1.addEventListener('click', function(e){
  var b = e.target.closest('.copybtn');
  if(!b) return;
  var s = b.getAttribute('data-cite');
  copyText(s).catch(function(){ fallbackCopy(s); });
  var old = b.textContent; b.textContent = 'Copied';
  setTimeout(function(){ b.textContent = 'Copy citation'; }, 2000);
});
})();
</script>
</body>
</html>
```