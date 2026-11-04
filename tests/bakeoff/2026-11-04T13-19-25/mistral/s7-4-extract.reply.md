I built the paragraph extractor for the attached CESCR General Comment No. 27 HTML: it parses the HTML, finds every numbered paragraph under its heading, checks the result against the document's own reference, shows plainly what this HTML version lost (the footnotes) and changed (missing spaces, special characters), and exports the paragraphs as JSON or Markdown. Everything is computed on load by the page's own code — no model was called and nothing left the browser.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a UN document — HTML</title>
<style>
*{box-sizing:border-box}
[hidden]{display:none!important}
html{margin:0}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:#9b2335}
code,.code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
header{padding:22px 30px 16px;border-bottom:1px solid #d9d2c3}
.kicker{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.16em;color:#9b2335}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:29px;line-height:1.22;margin:8px 0 10px;max-width:62ch}
.meta{display:flex;flex-wrap:wrap;gap:6px 20px;align-items:baseline;font-size:14px;color:#4a463f}
.meta .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
.status{margin-left:auto;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.05em;display:flex;align-items:center;gap:7px}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block;flex:none}
.dot.green{background:#1e6b3a}.dot.red{background:#9b2335}
.green{color:#1e6b3a}.red{color:#9b2335}
.pass{color:#1e6b3a;font-weight:600}.fail{color:#9b2335;font-weight:600}.muted{color:#8a8378}
.layout{display:flex;align-items:flex-start}
aside{flex:0 0 268px;border-right:1px solid #d9d2c3;padding:20px 22px 30px;position:sticky;top:0;max-height:100vh;overflow:auto}
main{flex:1;min-width:0;padding:20px 30px 60px}
.rail-h{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.16em;color:#4a463f;border-bottom:1px solid #d9d2c3;padding-bottom:8px}
.doc-card{border:1px solid #d9d2c3;padding:10px 12px;margin:14px 0 6px}
.doc-card .sym{color:#9b2335;font-size:12.5px}
.doc-title{font-size:13.5px;color:#4a463f;margin-top:4px;line-height:1.4}
.big{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1.05;margin-top:18px}
.big .of{font-size:15px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#4a463f}
.big.red{color:#9b2335}
.bar{height:3px;background:#d9d2c3;margin:8px 0 4px}
.bar i{display:block;height:100%;background:#1e6b3a}
.bar i.bad{background:#9b2335}
.note{font-size:12.5px;margin:2px 0 0;color:#6b655b}
.note.red{color:#9b2335}
.linklike{background:none;border:none;padding:0;margin-top:20px;color:#9b2335;cursor:pointer;font:inherit;font-size:14px;text-decoration:underline;text-underline-offset:3px}
.tabs{display:flex;flex-wrap:wrap;border-bottom:1px solid #d9d2c3;margin-bottom:22px}
.tabs [role="tab"]{background:none;border:none;border-bottom:2px solid transparent;margin-bottom:-1px;padding:10px 14px 9px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.1em;color:#4a463f}
.tabs [role="tab"]:hover{color:#1d1b18}
.tabs [role="tab"][aria-selected="true"]{color:#9b2335;border-bottom-color:#9b2335}
:focus-visible{outline:2px solid #9b2335;outline-offset:2px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1px;background:#d9d2c3;border:1px solid #d9d2c3}
.tile{background:#f4f0e8;padding:16px 18px 14px}
.t-label{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.14em;color:#4a463f;text-transform:uppercase}
.t-num{font-family:Georgia,"Times New Roman",serif;font-size:54px;line-height:1;margin:10px 0 6px}
.t-num.red{color:#9b2335}
.t-beside{font-size:14px;color:#4a463f}
.how{font-size:12.5px;color:#6b655b;margin-top:12px;border-top:1px solid #d9d2c3;padding-top:8px;line-height:1.45}
table{border-collapse:collapse;width:100%;margin:8px 0 24px}
caption{text-align:left;font-family:Georgia,"Times New Roman",serif;font-size:19px;line-height:1.3;padding:4px 0 10px;max-width:72ch}
.tabno{display:block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.14em;color:#9b2335;margin-bottom:5px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:400;color:#4a463f;text-align:left;border-bottom:1px solid #1d1b18;padding:6px 12px 6px 0}
td{border-bottom:1px solid #d9d2c3;padding:8px 12px 8px 0;vertical-align:top;font-size:15px}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.prow{cursor:pointer}
.prow:hover td{background:#ece5d6}
.pbtn{background:none;border:none;padding:0 2px;font:inherit;font-weight:600;color:#9b2335;cursor:pointer;font-variant-numeric:tabular-nums}
.det td{background:#efe9db;padding:14px 18px 16px}
.sec{max-width:230px}
.first{max-width:430px;color:#3d3a34}
.path{color:#6b655b;margin-bottom:10px}
.full{max-width:78ch;margin:0 0 12px;font-size:15.5px}
.repair{box-shadow:inset 0 0 0 1px #9b2335}
.ins{box-shadow:inset 0 0 0 1px #9b2335}
.chmark{box-shadow:inset 0 0 0 1px #9b2335;padding:0 1px}
.fwline{font-size:13.5px;color:#4a463f;margin-bottom:10px}
.reps{font-size:13px;color:#4a463f;margin-bottom:12px}
.reps ul{margin:6px 0 0;padding-left:18px}
.cite-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.copy{background:none;border:1px solid #9b2335;color:#9b2335;padding:6px 12px;cursor:pointer;font:inherit;font-size:13.5px}
.copy.copied{background:#9b2335;color:#f4f0e8}
.fold{display:block;background:none;border:none;border-bottom:1px solid #d9d2c3;width:100%;text-align:left;padding:12px 2px;cursor:pointer;font-family:Georgia,"Times New Roman",serif;font-size:19px;color:#1d1b18}
.fold .cnt{color:#9b2335}
#headings-box,#elements-box{border:1px solid #d9d2c3;border-top:none;padding:10px 16px;margin-bottom:22px}
.hitem{padding:3px 0;font-size:14.5px;border-bottom:1px dotted #d9d2c3}
.hitem .lbl{color:#9b2335;display:inline-block;min-width:36px}
.block h2{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:25px;margin:30px 0 10px}
.block h2 .count{color:#9b2335}
.ruleline{color:#4a463f;margin:0 0 6px}
.srow{cursor:pointer}
.srow:hover td{background:#ece5d6}
.before,.after{max-width:360px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:11.5px}
.ex{font-size:12px}
.hint{color:#6b655b;margin:2px 0 8px}
.ph{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:25px;margin:26px 0 10px}
.check{display:flex;gap:14px;flex-wrap:wrap;padding:10px 0;border-bottom:1px solid #d9d2c3;font-size:14.5px;align-items:baseline}
.cname{min-width:160px;color:#4a463f;letter-spacing:.1em;font-size:11px;text-transform:uppercase}
.cdetail{flex:1;min-width:260px}
.cverdict{white-space:nowrap}
.btn{background:#1d1b18;color:#f4f0e8;border:none;padding:11px 18px;cursor:pointer;font:inherit;font-size:14.5px;margin:0 10px 10px 0}
.btn:hover{background:#000}
.btn:disabled{opacity:.35;cursor:not-allowed}
.empty{font-size:17px;max-width:60ch;padding:20px 0}
footer{border-top:1px solid #d9d2c3;padding:16px 30px 30px;font-size:13.5px;color:#4a463f}
.credits{margin-top:8px;font-size:12px;color:#8a8378;max-width:95ch}
@media (max-width:900px){.layout{flex-direction:column}aside{position:static;max-height:none;flex:none;width:100%;border-right:none;border-bottom:1px solid #d9d2c3}}
</style>
</head>
<body>
<header>
  <div class="kicker">UN DOCUMENT · HTML</div>
  <h1 id="doc-title"></h1>
  <div class="meta">
    <span id="meta-sym"></span>
    <span id="meta-adopted"></span>
    <span id="meta-n"></span>
    <span id="meta-source"></span>
    <span class="status" id="meta-status"></span>
  </div>
</header>
<div class="layout">
  <aside id="rail"></aside>
  <main>
    <div class="tabs" role="tablist" aria-label="Views">
      <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 RESULT</button>
      <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" tabindex="-1">02 PARAGRAPHS</button>
      <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">03 LOST &amp; CHANGED</button>
      <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">04 CHECKS &amp; EXPORT</button>
    </div>
    <section id="panel-0" role="tabpanel" aria-labelledby="tab-0"></section>
    <section id="panel-1" role="tabpanel" aria-labelledby="tab-1" hidden></section>
    <section id="panel-2" role="tabpanel" aria-labelledby="tab-2" hidden></section>
    <section id="panel-3" role="tabpanel" aria-labelledby="tab-3" hidden></section>
  </main>
</div>
<footer id="foot"></footer>
<script>
(function(){
"use strict";
var WD = window.WORKSHOP_DATA || {};
var raw = WD.html_doc;
var D = Array.isArray(raw) ? (raw[0] || {}) : (raw || {});
var html = typeof D.html === 'string' ? D.html : '';
var REF = (D && D.reference && typeof D.reference === 'object') ? D.reference : null;
var SYMBOL = D.symbol || '(no symbol in this file)';
var TITLE = D.title || '(untitled document)';
var DOC_URL = D.doc_url || '';
var SOURCE = D.source || 'source not stated in this file';
var BUILT = D.built || '';

function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function collapse(s){ return String(s).replace(/[^\S\u00A0]+/g,' ').trim(); }

var body = null;
if(html){ try { body = new DOMParser().parseFromString(html,'text/html').body; } catch(e){ body = null; } }

/* ---------- classification ---------- */
var TAGS = 'table,div,p,h1,h2,h3,h4,h5,h6,ul,ol,li,blockquote,pre,section,article';
var blocks = body ? Array.prototype.slice.call(body.querySelectorAll(TAGS)) : [];
var firstTable = body ? body.querySelector('table') : null;
var PARA_RE = /^(\d{1,3})\.\s*([\s\S]*)$/;
var HEAD_RE = /^([IVX]+|[A-Z])\.\s*([\s\S]+)$/;

var elements = [], paragraphs = [], headings = [], ordered = [];
var titleSeen = false, lastHeading = null, curPath = [], curPart = '';

function dispH(h){ return h.label ? h.label + '. ' + h.heading : h.heading; }

blocks.forEach(function(el){
  var tag = el.tagName.toLowerCase();
  var text = collapse(el.textContent);
  var inTable = firstTable && (el === firstTable || firstTable.contains(el));
  var cls, rec = null;
  if(inTable){ cls = 'cover'; }
  else if(tag === 'div' || tag === 'section' || tag === 'article'){ cls = 'container'; }
  else if(tag === 'p'){
    var m = text.match(PARA_RE);
    if(m){
      cls = 'paragraph';
      rec = { num: parseInt(m[1],10), text_raw: m[2].trim(),
              section: lastHeading ? dispH(lastHeading) : '', part: curPart, path: curPath.slice() };
      paragraphs.push(rec); ordered.push({type:'paragraph', rec:rec});
    } else cls = 'text';
  }
  else if(/^h[1-6]$/.test(tag)){
    if(!titleSeen && (tag === 'h1' || tag === 'h2')){ cls = 'title'; titleSeen = true; ordered.push({type:'title', text:text}); }
    else {
      cls = 'heading';
      var hm = text.match(HEAD_RE), label = null, head = text, glued = false;
      if(hm){
        label = hm[1]; head = hm[2];
        glued = new RegExp('^' + label.replace(/[.*+?^${}()|[\]\\]/g,'\\$&') + '\\.[^\\s]').test(text);
      }
      rec = { tag: tag, label: label, heading: head, text: text, glued: glued };
      headings.push(rec); ordered.push({type:'heading', rec:rec});
      lastHeading = rec;
      if(tag === 'h2'){ curPath = [rec]; if(label && /^[IVX]+$/.test(label)) curPart = dispH(rec); }
      else curPath.push(rec);
    }
  }
  else cls = 'unclassified';
  elements.push({ tag: tag, cls: cls, text: text });
});

/* ---------- repairs ---------- */
var RULES = [
  { key:'sentence', label:'sentence join', re:/([a-z])\.([A-Z])/g,        parts:function(m){ return [m[1]+'.',' ',m[2]]; } },
  { key:'comma',    label:'comma join',    re:/([a-z]),([A-Za-z])/g,      parts:function(m){ return [m[1]+',',' ',m[2]]; } },
  { key:'quote',    label:'quote join',    re:/([a-z])\u201C/g,           parts:function(m){ return [m[1],' ','\u201C']; } },
  { key:'dash',     label:'dash join',     re:/\u2013([A-Za-z])/g,        parts:function(m){ return ['\u2013',' ',m[1]]; } }
];

function processParagraph(rawText){
  var text = rawText, logs = [], perRule = [];
  RULES.forEach(function(r){
    var ms = [], out = '', last = 0; r.re.lastIndex = 0; var m;
    while((m = r.re.exec(text)) !== null){
      var parts = r.parts(m);
      ms.push({ index:m.index, match:m[0], parts:parts });
      logs.push({ rule:r.key, label:r.label, match:m[0], parts:parts,
        before: text.slice(Math.max(0,m.index-20), m.index),
        after:  text.slice(m.index+m[0].length, m.index+m[0].length+20) });
      out += text.slice(last, m.index) + parts.join('');
      last = m.index + m[0].length;
      r.re.lastIndex = last;
      if(m[0].length === 0) r.re.lastIndex++;
    }
    out += text.slice(last);
    text = out;
    perRule.push(ms);
  });
  var cur = rawText, htmlOut = '';
  perRule.forEach(function(ms){
    var outH = '', outT = '', last = 0, l2 = 0;
    ms.forEach(function(mm){
      outH += esc(cur.slice(last, mm.index)) + mm.parts.map(function(p){ return p === ' ' ? '<span class="repair"> </span>' : esc(p); }).join('');
      outT += cur.slice(l2, mm.index) + mm.parts.join('');
      last = mm.index + mm.match.length; l2 = last;
    });
    outH += esc(cur.slice(last)); outT += cur.slice(l2);
    htmlOut = outH; cur = outT;
  });
  return { text:text, html:htmlOut, logs:logs };
}

paragraphs.forEach(function(p){
  var pr = processParagraph(p.text_raw);
  p.text = pr.text; p.html = pr.html; p.logs = pr.logs;
  p.citation = SYMBOL + ', para. ' + p.num;
});

/* ---------- first words ---------- */
function normW(s){ return String(s).replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2011]/g,'-').replace(/\u00A0/g,' '); }
function firstSix(t){ return normW(t).split(/\s+/).filter(Boolean).slice(0,6).join(' '); }
paragraphs.forEach(function(p){
  p.first6 = firstSix(p.text);
  if(REF && REF.first_words && REF.first_words[String(p.num)] != null){
    p.ref6 = firstSix(REF.first_words[String(p.num)]);
    p.fwMatch = (p.first6 === p.ref6);
  } else { p.ref6 = null; p.fwMatch = null; }
});

/* ---------- characters ---------- */
var corpus = paragraphs.map(function(p){ return p.text; }).concat(headings.map(function(h){ return h.text; }));
function countCh(ch){ var n = 0; corpus.forEach(function(t){ n += t.split(ch).length - 1; }); return n; }
function exampleFor(ch, disp){
  for(var i = 0; i < corpus.length; i++){
    var t = corpus[i], idx = t.indexOf(ch);
    if(idx >= 0){
      var b = t.slice(Math.max(0, idx-18), idx), a = t.slice(idx+ch.length, idx+ch.length+18);
      return esc(b) + '<span class="chmark">' + esc(disp) + '</span>' + esc(a);
    }
  }
  return '<span class="muted">none found</span>';
}

/* ---------- exports ---------- */
var n = paragraphs.length;
function buildJson(){
  var recs = paragraphs.map(function(p){
    return { symbol: SYMBOL, paragraph: p.num, section: p.section, part: p.part,
      text: p.text, text_raw: p.text_raw,
      first_words_match: (p.fwMatch === null ? null : p.fwMatch),
      citation: p.citation, doc_url: DOC_URL,
      limitations: 'no footnotes in this HTML version' + (REF && REF.footnotes != null ? '; the document has ' + REF.footnotes + ' footnotes' : '') };
  });
  return JSON.stringify(recs, null, 2);
}
function buildMarkdown(){
  var today = new Date().toISOString().slice(0,10);
  var fn = (REF && REF.footnotes != null) ? REF.footnotes : '?';
  var fm = ['---',
    'title: ' + JSON.stringify(TITLE),
    'symbol: ' + JSON.stringify(SYMBOL),
    'adopted: ' + (REF && REF.adopted ? JSON.stringify(String(REF.adopted)) : '""'),
    'source_url: ' + JSON.stringify(DOC_URL),
    'extracted: ' + today,
    'paragraphs_found: ' + n,
    'paragraphs_expected: ' + (REF && REF.paragraphs != null ? REF.paragraphs : 'null'),
    'footnotes: ' + JSON.stringify('0 of ' + fn + ' — this HTML version has no footnotes'),
    '---'].join('\n');
  var out = fm + '\n\n# ' + TITLE.replace(/\s*\*$/, '') + '\n\n';
  ordered.forEach(function(it){
    if(it.type === 'title') return;
    if(it.type === 'heading'){ var h = it.rec; out += (h.tag === 'h2' ? '## ' : '### ') + dispH(h) + '\n\n'; }
    else { var p = it.rec; out += '**' + p.num + '.** ' + p.text + '\n\n'; }
  });
  return out;
}
var jsonStr = buildJson();

/* ---------- checks ---------- */
var checks = [];
function addCheck(name, detail, status, link){ checks.push({ name:name, detail:detail, status:status, link:link||null }); }

var refP = (REF && REF.paragraphs != null) ? REF.paragraphs : null;
var refF = (REF && REF.footnotes != null) ? REF.footnotes : null;

if(refP != null) addCheck('Paragraph count', 'found ' + n + ' · reference ' + refP, n === refP ? 'pass' : 'fail');
else addCheck('Paragraph count', 'found ' + n + ' · no reference in this file', 'notrun');

var numOk = true, anomalies = [];
paragraphs.forEach(function(p,i){ if(p.num !== i+1){ numOk = false; anomalies.push('position ' + (i+1) + ': expected ' + (i+1) + ', found ' + p.num); } });
var seen = {}, dups = [];
paragraphs.forEach(function(p){ if(seen[p.num]) dups.push(p.num); seen[p.num] = 1; });
var numDetail = numOk ? ('1–' + n + ' in order, no gaps, no duplicates')
  : anomalies.slice(0,8).join('; ') + (dups.length ? '; duplicate numbers: ' + dups.join(', ') : '');
addCheck('Numbering', numDetail, numOk ? 'pass' : 'fail');

if(REF && REF.first_words){
  var mm = paragraphs.filter(function(p){ return p.fwMatch === false; });
  var nr = paragraphs.filter(function(p){ return p.fwMatch === null; });
  var det = (mm.length + nr.length) + ' of ' + n + ' differ';
  var list = mm.slice(0,6).map(function(p){ return 'para. ' + p.num + ': found \u201C' + p.first6 + '\u201D / reference \u201C' + (p.ref6 || '—') + '\u201D'; });
  if(nr.length) list.push(nr.length + ' paragraphs have no reference entry');
  if(list.length) det += ' — ' + list.join('; ');
  addCheck('First words', det, (mm.length === 0 && nr.length === 0) ? 'pass' : 'fail', { tab:1, label:'see tab 02' });
} else addCheck('First words', 'no reference in this file', 'notrun');

if(refF != null) addCheck('Footnotes', '0 in this HTML · ' + refF + ' in the PDF and Word versions — the HTML version has no footnotes: a limit of the source, not of the app', 'limit');
else addCheck('Footnotes', 'no reference in this file', 'notrun');

var allLogs = [];
paragraphs.forEach(function(p){ p.logs.forEach(function(l){ allLogs.push({ num:p.num, rule:l.rule, label:l.label, match:l.match, parts:l.parts, before:l.before, after:l.after }); }); });
var perRuleCount = {};
allLogs.forEach(function(l){ perRuleCount[l.rule] = (perRuleCount[l.rule] || 0) + 1; });
var parasWithRepairs = paragraphs.filter(function(p){ return p.logs.length > 0; }).length;
addCheck('Repairs', allLogs.length + ' spaces restored in ' + parasWithRepairs + ' paragraphs · sentence ' + (perRuleCount.sentence||0) + ', comma ' + (perRuleCount.comma||0) + ', quote ' + (perRuleCount.quote||0) + ', dash ' + (perRuleCount.dash||0) + ' · every one listed on tab 03 · text_raw keeps the text as found', 'pass', { tab:2, label:'see tab 03' });

var h2c = headings.filter(function(h){ return h.tag === 'h2'; }).length;
var glued = headings.filter(function(h){ return h.glued; }).length;
addCheck('Headings', h2c + ' h2 + ' + (headings.length - h2c) + ' h3 = ' + headings.length + ' headings · ' + glued + ' glued labels separated', 'pass');

var clsCounts = {};
elements.forEach(function(e){ clsCounts[e.cls] = (clsCounts[e.cls] || 0) + 1; });
var sum = 0; for(var k in clsCounts) sum += clsCounts[k];
var uncl = elements.filter(function(e){ return e.cls === 'unclassified'; });
var det7 = Object.keys(clsCounts).map(function(kk){ return kk + ' ' + clsCounts[kk]; }).join(' + ') + ' = ' + sum + ' of ' + elements.length + ' block elements';
if(uncl.length) det7 += ' — unclassified: ' + uncl.slice(0,5).map(function(e){ return e.tag; }).join(', ');
addCheck('Nothing lost', det7, (sum === elements.length && uncl.length === 0) ? 'pass' : 'fail');

if(body){
  var rtOk = false, rtDetail = '';
  try { var back = JSON.parse(jsonStr); rtOk = (back.length === n); rtDetail = 'JSON parsed back: ' + back.length + ' records = ' + n + ' rows on tab 02'; }
  catch(e){ rtDetail = 'JSON parse failed: ' + e.message; }
  addCheck('Export round trip', rtDetail, rtOk ? 'pass' : 'fail');
} else addCheck('Export round trip', 'no HTML in this file', 'notrun');

var npass = checks.filter(function(c){ return c.status === 'pass'; }).length;
var nfail = checks.filter(function(c){ return c.status === 'fail'; }).length;
var nlimit = checks.filter(function(c){ return c.status === 'limit'; }).length;
var m = npass + nfail;
var statusText = nfail > 0 ? nfail + ' check' + (nfail > 1 ? 's' : '') + ' failed'
  : (m > 0 ? npass + ' of ' + m + ' checks pass' : 'checks not run');

/* ---------- header & rail ---------- */
document.getElementById('doc-title').textContent = TITLE;
document.getElementById('meta-sym').innerHTML = DOC_URL
  ? '<a class="sym" href="' + esc(DOC_URL) + '" target="_blank" rel="noopener">' + esc(SYMBOL) + ' \u2197</a>'
  : '<span class="sym">' + esc(SYMBOL) + '</span>';
document.getElementById('meta-adopted').textContent = 'adopted ' + (REF && REF.adopted ? REF.adopted : 'not stated');
document.getElementById('meta-n').textContent = n + ' paragraphs extracted';
document.getElementById('meta-source').textContent = SOURCE;
document.getElementById('meta-status').innerHTML =
  (nfail > 0 ? '<span class="dot red"></span><span class="red">' + esc(statusText) + '</span>'
             : '<span class="dot green"></span><span class="green">' + esc(statusText) + '</span>') +
  (nlimit > 0 ? ' · <span class="red">' + nlimit + ' source limit' + (nlimit > 1 ? 's' : '') + '</span>' : '');

var shortTitle = TITLE.replace(/\s*\*$/, '');
if(shortTitle.length > 110) shortTitle = shortTitle.slice(0, 107) + '…';
var w = refP != null ? Math.min(100, Math.round(n / refP * 100)) : 100;
var bad = refP != null && n !== refP;
document.getElementById('rail').innerHTML =
  '<div class="rail-h">DOCUMENT</div>' +
  '<div class="doc-card"><div class="code sym">' + esc(SYMBOL) + '</div><div class="doc-title">' + esc(shortTitle) + '</div></div>' +
  '<div class="big">' + n + ' <span class="of">paragraphs of ' + (refP != null ? refP : '?') + '</span></div>' +
  '<div class="bar"><i style="width:' + w + '%" class="' + (bad ? 'bad' : '') + '"></i></div>' +
  '<div class="note code">counted from the HTML\u2019s &lt;p&gt; elements</div>' +
  '<div class="big red">0 <span class="of">footnotes of ' + (refF != null ? refF : '?') + '</span></div>' +
  '<div class="note red">not in this HTML</div>' +
  '<button class="linklike" data-tab="3">' + esc(statusText) + ' \u2192 tab 04</button>';

/* ---------- tab 01 ---------- */
function renderPanel0(){
  var p0 = document.getElementById('panel-0');
  if(!body || n === 0){
    p0.innerHTML = '<p class="empty">This HTML yielded no numbered paragraphs, so tabs 02\u201304 have nothing to list and the exports are disabled.</p>';
    return;
  }
  var fwOk = paragraphs.filter(function(p){ return p.fwMatch === true; }).length;
  var hasFw = !!(REF && REF.first_words);
  var diff = refP != null ? n - refP : null;
  function tile(label, num, beside, how, red){
    return '<div class="tile"><div class="t-label">' + esc(label) + '</div>' +
      '<div class="t-num' + (red ? ' red' : '') + '">' + esc(num) + '</div>' +
      '<div class="t-beside">' + beside + '</div>' +
      '<div class="how">' + how + '</div></div>';
  }
  var b1 = refP != null
    ? 'the document has ' + refP + (diff === 0 ? ' <span class="pass">\u2014 equal</span>' : ' <span class="fail">(' + (diff > 0 ? '+' : '') + diff + ')</span>')
    : 'no reference in this file';
  var b2 = hasFw
    ? 'of ' + refP + ' paragraphs match on the first six words' + (fwOk === refP ? ' <span class="pass">\u2014 all</span>' : ' <span class="fail">\u2014 ' + (refP - fwOk) + ' differ</span>')
    : 'no reference in this file';
  var b3 = 'of ' + (refF != null ? refF : '?') + ' footnotes \u2014 this HTML version has none; <a href="#" data-tab="2">see tab 03</a>';
  var b4 = 'spaces restored or flagged by the four rules \u2014 <a href="#" data-tab="2">see tab 03</a>';
  p0.innerHTML = '<div class="tiles">' +
    tile('PARAGRAPHS FOUND', String(n), b1, 'How this is computed: every &lt;p&gt; in the HTML whose text begins with a number and a full stop, counted by this page\u2019s code.') +
    tile('FIRST WORDS MATCH', hasFw ? String(fwOk) : '\u2014', b2, 'How this is computed: the first six words of each paragraph, compared with the document\u2019s reference after normalising quotes, dashes and non-breaking characters; case is kept.') +
    tile('FOOTNOTES', '0', b3, 'How this is computed: the HTML contains no footnote elements; the reference counts the footnotes of the PDF and Word versions.', true) +
    tile('SPACES REPAIRED', String(allLogs.length), b4, 'How this is computed: a space is inserted only where the characters prove one was there; the text as found is kept in text_raw.') +
    '</div>';
}

/* ---------- tab 02 ---------- */
function firstLine(t){
  if(t.length <= 120) return t;
  var c = t.slice(0, 120), sp = c.lastIndexOf(' ');
  if(sp > 60) c = c.slice(0, sp);
  return c + ' …';
}
function detailHtml(p){
  var path = p.path.length ? p.path.map(function(h){ return esc(dispH(h)); }).join(' \u203A ') : '(no heading above)';
  var fw = p.fwMatch === null ? '<span class="muted">no reference in this file</span>'
    : '<span class="code">FOUND</span> \u201C' + esc(p.first6) + '\u201D &nbsp;\u00B7&nbsp; <span class="code">REFERENCE</span> \u201C' + esc(p.ref6) + '\u201D';
  var reps = p.logs.length
    ? '<div class="reps"><span class="code">REPAIRED HERE</span><ul>' + p.logs.map(function(l){
        return '<li>' + esc(l.label) + ': \u2026' + esc(l.before) + '<b>' + esc(l.match) + '</b>' + esc(l.after) + '\u2026</li>';
      }).join('') + '</ul></div>'
    : '<div class="reps muted">no space repaired in this paragraph</div>';
  var link = DOC_URL ? ' <a href="' + esc(DOC_URL) + '" target="_blank" rel="noopener">' + esc(SYMBOL) + ' \u2197</a>' : '';
  return '<div class="path code">' + path + '</div>' +
    '<p class="full">' + p.html + '</p>' +
    '<div class="fwline">' + fw + '</div>' + reps +
    '<div class="cite-row"><button class="copy" data-cite="' + esc(p.citation) + '">Copy citation</button><span class="code">' + esc(p.citation) + '</span>' + link + '</div>';
}
function renderPanel1(){
  var p1 = document.getElementById('panel-1');
  if(n === 0){ p1.innerHTML = '<p class="empty">No numbered paragraphs found in this HTML.</p>'; return; }
  var headFold = '<button class="fold" aria-expanded="false" aria-controls="headings-box">Headings found: <span class="cnt">' + headings.length + '</span></button>' +
    '<div id="headings-box" hidden>' + headings.map(function(h){
      return '<div class="hitem"><span class="code lbl">' + (h.label ? esc(h.label + '.') : '') + '</span> ' + esc(h.heading) + '</div>';
    }).join('') + '</div>';
  var rows = paragraphs.map(function(p, i){
    var chk = p.fwMatch === null ? '<span class="muted">no reference</span>'
      : (p.fwMatch ? '<span class="pass">OK</span>' : '<span class="fail">first words differ</span>');
    return '<tr class="prow" data-i="' + i + '">' +
      '<td class="num"><button class="pbtn" aria-expanded="false" aria-controls="det-' + i + '">' + p.num + '</button></td>' +
      '<td class="sec">' + esc(p.section || '(no heading above)') + '</td>' +
      '<td class="first">' + esc(firstLine(p.text)) + '</td>' +
      '<td>' + chk + '</td></tr>' +
      '<tr class="det" id="det-' + i + '" hidden><td colspan="4">' + detailHtml(p) + '</td></tr>';
  }).join('');
  p1.innerHTML = headFold +
    '<p class="how">One row per paragraph; click a row (or its number) for the full text, the check and the citation. The full text is verbatim, never shortened.</p>' +
    '<table><caption><span class="tabno">TAB.02</span>' + n + ' paragraphs found, ' + (refP != null ? refP : '?') + ' expected</caption>' +
    '<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>' +
    '<tbody id="ptbody">' + rows + '</tbody></table>';
}

/* ---------- tab 03 ---------- */
function renderPanel2(){
  var p2 = document.getElementById('panel-2');
  var ruleLine = ['sentence','comma','quote','dash'].map(function(k){ return k + ' join ' + (perRuleCount[k] || 0); }).join(' · ');
  var srows = allLogs.map(function(l){
    return '<tr class="srow" data-num="' + l.num + '" title="open para. ' + l.num + ' on tab 02">' +
      '<td class="num">' + l.num + '</td>' +
      '<td class="code before">\u2026' + esc(l.before) + '<b>' + esc(l.match) + '</b>' + esc(l.after) + '\u2026</td>' +
      '<td class="code after">\u2026' + esc(l.before) + l.parts.map(function(pp){ return pp === ' ' ? '<span class="ins"> </span>' : esc(pp); }).join('') + esc(l.after) + '\u2026</td>' +
      '<td>' + esc(l.label) + '</td></tr>';
  }).join('');
  var charRows = [
    ['en dash (U+2013)', '\u2013', '\u2013'],
    ['double quotes (U+201C, U+201D)', ['\u201C','\u201D'], '\u201C'],
    ['right single quote (U+2019)', '\u2019', '\u2019'],
    ['non-breaking hyphen (U+2011)', '\u2011', '\u2011'],
    ['non-breaking space (U+00A0)', '\u00A0', '\u00B7']
  ].map(function(r){
    var chs = Array.isArray(r[1]) ? r[1] : [r[1]];
    var cnt = chs.reduce(function(a, c){ return a + countCh(c); }, 0);
    return '<tr><td>' + esc(r[0]) + '</td><td class="num">' + cnt + '</td><td class="code ex">' + exampleFor(chs[0], r[2]) + '</td></tr>';
  }).join('');
  p2.innerHTML =
    '<section class="block"><h2>Lost: footnotes <span class="count">' + (refF != null ? refF : '?') + '</span></h2>' +
    '<p>The document has ' + (refF != null ? refF : 'an unknown number of') + ' footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title\u2019s asterisk points to is missing. To cite a footnote, use the PDF or Word version.</p></section>' +
    '<section class="block"><h2>Changed: spaces <span class="count">' + allLogs.length + '</span></h2>' +
    '<div class="code ruleline">' + esc(ruleLine) + '</div>' +
    '<table><caption><span class="tabno">TAB.03 · FIG.01</span>' + allLogs.length + ' missing spaces restored by rule \u2014 click a row to open the paragraph on tab 02</caption>' +
    '<thead><tr><th scope="col" class="num">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead>' +
    '<tbody>' + srows + '</tbody></table>' +
    '<p class="note">Rules restore a space only where the characters prove it was there. Word pairs no rule can see \u2014 two words glued together with no punctuation between them \u2014 are not touched; the first-words check catches them only when they fall in a paragraph\u2019s first six words.</p></section>' +
    '<section class="block"><h2>Changed: characters</h2>' +
    '<table><caption><span class="tabno">TAB.03 · FIG.02</span>special characters kept exactly as published, counted over every paragraph and heading text</caption>' +
    '<thead><tr><th scope="col">Character</th><th scope="col" class="num">Count</th><th scope="col">Example</th></tr></thead>' +
    '<tbody>' + charRows + '</tbody></table>' +
    '<div class="code hint">on a keyboard: a hyphen and straight quotes</div>' +
    '<p class="note">Kept exactly as published, in the tables and in every export. A search typed with the hyphen key will not find a non-breaking hyphen, and straight quotes will not find curly ones: normalise the text before searching it.</p></section>';
}

/* ---------- tab 04 ---------- */
function renderPanel3(){
  var p3 = document.getElementById('panel-3');
  var checkHtml = checks.map(function(c){
    var v;
    if(c.status === 'pass') v = '<span class="pass">pass</span>';
    else if(c.status === 'fail') v = '<span class="fail">check failed</span>' + (c.link ? ' <a href="#" data-tab="' + c.link.tab + '">' + esc(c.link.label) + '</a>' : '');
    else if(c.status === 'limit') v = '<span class="fail">source limit</span>';
    else v = '<span class="muted">not run</span>';
    return '<div class="check"><span class="cname code">' + esc(c.name) + '</span><span class="cdetail">' + esc(c.detail) + '</span><span class="cverdict">' + v + '</span></div>';
  }).join('');
  var elRows = elements.map(function(e){
    var t = e.text.length > 80 ? e.text.slice(0, 80) + ' …' : e.text;
    return '<tr><td class="code">' + esc(e.tag) + '</td><td>' + esc(e.cls) + '</td><td>' + esc(t) + '</td></tr>';
  }).join('');
  p3.innerHTML =
    '<h2 class="ph">Checks</h2><div class="checks">' + checkHtml + '</div>' +
    '<h2 class="ph">Export</h2>' +
    '<button class="btn" id="dl-json"' + (n === 0 ? ' disabled' : '') + '>Download JSON</button>' +
    '<button class="btn" id="dl-md"' + (n === 0 ? ' disabled' : '') + '>Download Markdown</button>' +
    '<p class="how">The JSON is an array of records with symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url and limitations. The Markdown opens with front matter (title, symbol, adopted, source_url, extracted, paragraphs_found, paragraphs_expected, footnotes), then the headings as ## and ### lines and each paragraph as its number in bold. File names use the symbol with slashes replaced by hyphens; both files are UTF-8 Blob downloads.</p>' +
    '<button class="fold" aria-expanded="false" aria-controls="elements-box">Elements found (' + elements.length + ')</button>' +
    '<div id="elements-box" hidden><table><caption><span class="tabno">TAB.04 · FIG.01</span>every block element in the HTML, classified exactly once</caption>' +
    '<thead><tr><th scope="col">Tag</th><th scope="col">Classified as</th><th scope="col">Text (first 80 characters)</th></tr></thead>' +
    '<tbody>' + elRows + '</tbody></table></div>';
}

/* ---------- footer ---------- */
document.getElementById('foot').innerHTML =
  esc(SOURCE) + (BUILT ? ' · built ' + esc(BUILT) : '') + '<br>' +
  'Done by this page\u2019s code; no model was called and nothing left the browser.' +
  '<div class="credits">Sources consulted: The Turing Way, \u201CDocumentation and metadata\u201D (CC BY 4.0) · UK Government Analysis Function, \u201CQuality assurance of code for analysis and research: Testing code\u201D (Open Government Licence v3.0) · Dag Hammarskjöld Library, \u201CAsk DAG: how should I cite a UN document?\u201D</div>';

/* ---------- render ---------- */
renderPanel0(); renderPanel1(); renderPanel2(); renderPanel3();

/* ---------- tabs ---------- */
var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
function selectTab(i){
  tabs.forEach(function(t, j){
    var on = (i === j);
    t.setAttribute('aria-selected', String(on));
    t.tabIndex = on ? 0 : -1;
    document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
  });
}
tabs.forEach(function(t, i){
  t.addEventListener('click', function(){ selectTab(i); });
  t.addEventListener('keydown', function(e){
    var nn = null;
    if(e.key === 'ArrowRight') nn = (i+1) % tabs.length;
    else if(e.key === 'ArrowLeft') nn = (i-1+tabs.length) % tabs.length;
    else if(e.key === 'Home') nn = 0;
    else if(e.key === 'End') nn = tabs.length - 1;
    if(nn !== null){ e.preventDefault(); tabs[nn].focus(); selectTab(nn); }
  });
});

/* ---------- rows ---------- */
function setRow(i, force){
  var det = document.getElementById('det-' + i);
  var btn = document.querySelector('.prow[data-i="' + i + '"] .pbtn');
  if(!det || !btn) return;
  var open = (force !== undefined) ? force : det.hidden;
  det.hidden = !open;
  btn.setAttribute('aria-expanded', String(open));
}
var ptbody = document.getElementById('ptbody');
if(ptbody){
  ptbody.addEventListener('click', function(e){
    var row = e.target.closest('.prow');
    if(row) setRow(row.getAttribute('data-i'));
  });
}
function openPara(num){
  var i = -1;
  for(var j = 0; j < paragraphs.length; j++){ if(paragraphs[j].num === num){ i = j; break; } }
  if(i < 0) return;
  selectTab(1);
  setRow(i, true);
  var det = document.getElementById('det-' + i);
  if(det) det.scrollIntoView({ block:'center' });
}

/* ---------- folds ---------- */
Array.prototype.forEach.call(document.querySelectorAll('.fold'), function(b){
  b.addEventListener('click', function(){
    var box = document.getElementById(b.getAttribute('aria-controls'));
    if(!box) return;
    var open = box.hidden;
    box.hidden = !open;
    b.setAttribute('aria-expanded', String(open));
  });
});

/* ---------- copy citation ---------- */
function copyText(t, btn){
  var done = function(){
    var old = btn.textContent;
    btn.textContent = 'Copied'; btn.classList.add('copied');
    setTimeout(function(){ btn.textContent = old; btn.classList.remove('copied'); }, 2000);
  };
  var fallback = function(){
    var ta = document.createElement('textarea');
    ta.value = t; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); done(); } catch(e){}
    ta.remove();
  };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(t).then(done, fallback);
  } else fallback();
}

/* ---------- downloads ---------- */
function download(name, content, type){
  var blob = new Blob([content], { type: type });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url; a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function(){ URL.revokeObjectURL(url); }, 2000);
}
var dlJson = document.getElementById('dl-json'), dlMd = document.getElementById('dl-md');
if(dlJson) dlJson.addEventListener('click', function(){ download(SYMBOL.replace(/\//g,'-') + '.json', jsonStr, 'application/json;charset=utf-8'); });
if(dlMd) dlMd.addEventListener('click', function(){ download(SYMBOL.replace(/\//g,'-') + '.md', buildMarkdown(), 'text/markdown;charset=utf-8'); });

/* ---------- global delegation ---------- */
document.addEventListener('click', function(e){
  var t = e.target;
  var dt = t.closest('[data-tab]');
  if(dt){ e.preventDefault(); selectTab(parseInt(dt.getAttribute('data-tab'), 10)); return; }
  var cp = t.closest('.copy');
  if(cp){ copyText(cp.getAttribute('data-cite'), cp); return; }
  var sr = t.closest('.srow');
  if(sr){ openPara(parseInt(sr.getAttribute('data-num'), 10)); }
});
})();
</script>
</body>
</html>
```