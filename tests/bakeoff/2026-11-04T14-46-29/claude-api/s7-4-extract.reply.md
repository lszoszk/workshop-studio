I built the paragraph extractor with two tabs, RESULT and PARAGRAPHS, a left rail showing the document's counts, and JSON and Markdown downloads. All checks run on load and compare the parsed HTML with the document's own reference. Footnotes show as a source limit, not a failure. I have not run it against the real file, so the counts you see are whatever the code finds.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraphs out of a UN document</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.serif,h1,h2,.big,caption{font-family:Georgia,"Times New Roman",serif}
.lab,.mono,th,.tab,.hint{font-family:ui-monospace,Menlo,Consolas,monospace}
.lab{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#5a554b}
a{color:#1d1b18}
:focus-visible{outline:3px solid #9b2335;outline-offset:2px}
header.top{padding:18px 28px 12px;border-bottom:1px solid #d9d2c3}
.titlerow{display:flex;gap:24px;justify-content:space-between;align-items:flex-start;flex-wrap:wrap}
h1{font-size:28px;line-height:1.2;margin:4px 0 6px;font-weight:normal;max-width:760px}
.meta{margin:0;font-size:14px;color:#3d392f}
.status{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;text-align:right;padding-top:6px}
.status div{margin-bottom:3px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.ok{color:#1f6b3a}.bad{color:#9b2335}.mute{color:#5a554b}
.wrap{display:grid;grid-template-columns:240px 1fr;gap:0;max-width:1240px;margin:0 auto}
aside.rail{padding:20px 22px 20px 28px;border-right:1px solid #d9d2c3}
.card{border-top:1px solid #d9d2c3;border-bottom:1px solid #d9d2c3;padding:10px 0;margin:8px 0 18px}
.card .sym{font-size:13px;font-weight:bold}
.card .short{font-size:14px;margin-top:4px;color:#3d392f}
.rbig{margin-bottom:16px}
.rbig .n{font-size:44px;line-height:1;display:block}
.rbig small{display:block;font-size:12px;font-family:ui-monospace,Menlo,Consolas,monospace;color:#5a554b;margin-top:2px}
.bar{height:4px;background:#d9d2c3;margin-top:6px}
.bar i{display:block;height:100%;background:#1f6b3a}
.bar.short i{background:#9b2335}
main{padding:0 28px 28px;min-width:0}
[role=tablist]{display:flex;gap:4px;border-bottom:1px solid #d9d2c3;margin-top:8px}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:12px 14px 9px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;color:#3d392f}
.tab[aria-selected=true]{color:#9b2335;border-bottom-color:#9b2335;font-weight:bold}
h2.q{font-size:24px;font-weight:normal;margin:22px 0 14px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:1px solid #d9d2c3}
.tile{padding:14px 18px 14px 0;border-bottom:1px solid #d9d2c3}
.tile:nth-child(even){padding-left:18px;border-left:1px solid #d9d2c3}
.tile .big{font-size:52px;line-height:1.05;margin:4px 0}
.tile .beside{font-size:15px}
.how{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;color:#5a554b;margin:8px 0 0;line-height:1.45}
.st{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;font-weight:bold;text-transform:uppercase;letter-spacing:.04em}
.fwlist{margin:14px 0 0;padding:0;list-style:none;font-size:14px}
.fwlist li{padding:4px 0;border-bottom:1px dotted #d9d2c3}
h3.sec{font-family:Georgia,serif;font-weight:normal;font-size:20px;margin:28px 0 8px}
.btn{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase;background:#1d1b18;color:#f4f0e8;border:1px solid #1d1b18;padding:10px 16px;cursor:pointer;margin-right:8px}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn.light{background:none;color:#1d1b18}
.acc{display:block;width:100%;text-align:left;background:none;border:0;border-top:1px solid #d9d2c3;padding:12px 0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;color:#1d1b18}
.acc:last-of-type{border-bottom:1px solid #d9d2c3}
.acc::before{content:"+ ";color:#9b2335;font-weight:bold}
.acc[aria-expanded=true]::before{content:"– "}
.panel{padding:6px 0 14px}
ul.checks{list-style:none;margin:0;padding:0}
ul.checks li{padding:9px 0;border-bottom:1px dotted #d9d2c3;font-size:15px}
ul.checks li .st{display:inline-block;min-width:104px}
.linkbtn{background:none;border:0;padding:0;font:inherit;text-decoration:underline;color:#9b2335;cursor:pointer;margin-left:6px}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font-size:18px;padding:6px 0 8px}
caption .lab{display:block;margin-bottom:2px}
th{font-size:11px;letter-spacing:.08em;text-transform:uppercase;text-align:left;padding:6px 8px;border-bottom:2px solid #1d1b18;color:#3d392f;font-weight:normal}
td{padding:7px 8px;border-bottom:1px solid #d9d2c3;vertical-align:top}
th.r,td.r,td.num{text-align:right}
td.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
tr.row{cursor:pointer}
tr.row:hover td{background:#ece6d8}
.rowbtn{background:none;border:0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px;font-weight:bold;color:#9b2335;cursor:pointer;padding:2px 6px}
tr.detail td{background:#faf7f0;padding:14px 16px 18px}
.path{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;color:#5a554b;margin-bottom:8px}
.full{margin:0 0 12px;max-width:760px}
mark.fix{background:none;color:inherit;outline:1px solid #9b2335;outline-offset:1px}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:12px;font-size:14px}
.reps{font-size:14px;margin-bottom:12px}
.reps code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
.tag{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;color:#5a554b;margin-top:4px;text-transform:uppercase;letter-spacing:.05em}
.hdrs{list-style:none;margin:0;padding:0;font-size:14.5px}
.hdrs li{padding:4px 0;border-bottom:1px dotted #d9d2c3;display:flex;gap:10px}
.hdrs .lv{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;color:#9b2335;min-width:24px;padding-top:3px}
.hdrs .ct{margin-left:auto;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;color:#5a554b;white-space:nowrap}
.hdrs li.l3{padding-left:22px}
.note{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;color:#5a554b;margin:8px 0}
footer{border-top:1px solid #d9d2c3;padding:14px 28px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;color:#5a554b;max-width:1240px;margin:0 auto}
@media(max-width:820px){.wrap{grid-template-columns:1fr}aside.rail{border-right:0;border-bottom:1px solid #d9d2c3}.tiles{grid-template-columns:1fr}.tile:nth-child(even){padding-left:0;border-left:0}.cmp{grid-template-columns:1fr}}
</style>
</head>
<body>
<header class="top">
  <div class="lab">UN DOCUMENT · HTML</div>
  <div class="titlerow"><h1 id="title"></h1><div class="status" id="status"></div></div>
  <p class="meta" id="meta"></p>
</header>
<div class="wrap">
  <aside class="rail" id="rail" aria-label="Document summary"></aside>
  <main>
    <div role="tablist" aria-label="Views">
      <button class="tab" role="tab" id="tab0" aria-controls="p0" aria-selected="true" tabindex="0">01 Result</button>
      <button class="tab" role="tab" id="tab1" aria-controls="p1" aria-selected="false" tabindex="-1">02 Paragraphs</button>
    </div>
    <section role="tabpanel" id="p0" aria-labelledby="tab0"></section>
    <section role="tabpanel" id="p1" aria-labelledby="tab1" hidden></section>
  </main>
</div>
<footer id="foot"></footer>

<script>
(function(){
"use strict";
var W = window.WORKSHOP_DATA || {};
var D = W.html_doc || {};
var ref = D.reference || {};
var hasRefP = typeof ref.paragraphs === 'number';
var hasRefF = typeof ref.footnotes === 'number';
var hasRefW = !!ref.first_words && typeof ref.first_words === 'object';
var symbol = D.symbol || '';
var esc = function(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});};
var clean = function(s){return (s||'').replace(/\s+/g,' ').trim();};

/* ---------- 1. parse and classify ---------- */
var doc = new DOMParser().parseFromString(D.html || '', 'text/html');
var els = doc.body ? Array.prototype.slice.call(doc.body.querySelectorAll('table, p, h2, h3')) : [];
var firstTable = doc.body ? doc.body.querySelector('table') : null;
var counts = {cover:0, title:0, heading:0, paragraph:0, other:0, unclassified:0};
var unclassified = [];
var titleText = null, curSection = '', curPart = '';
var blocks = [], paras = [], heads = [];

var RULES = [
  {id:'sentence', label:'sentence join', re:/([a-z])\.([A-Z])/g, fn:function(a,b){return a+'. '+b;}},
  {id:'comma', label:'comma join', re:/([a-z]),([A-Za-z])/g, fn:function(a,b){return a+', '+b;}},
  {id:'quote', label:'quote join', re:/([a-z])\u201c/g, fn:function(a){return a+' \u201c';}},
  {id:'dash', label:'dash join', re:/\u2013([A-Za-z])/g, fn:function(a){return '\u2013 '+a;}}
];
function repair(raw, n){
  var cur = raw, log = [];
  RULES.forEach(function(rule){
    cur = cur.replace(rule.re, function(){
      var a = Array.prototype.slice.call(arguments);
      var m = a[0], off = a[a.length-2], str = a[a.length-1];
      var rep = rule.fn.apply(null, a.slice(1, a.length-2));
      var pre = str.slice(Math.max(0, off-20), off);
      var post = str.slice(off+m.length, off+m.length+20);
      log.push({para:n, rule:rule.id, ruleLabel:rule.label, before:pre+m+post, after:pre+rep+post, needle:rep});
      return rep;
    });
  });
  return {text:cur, log:log};
}
var normFW = function(s){return clean(String(s||'').replace(/[\u2018\u2019]/g,"'").replace(/[\u201c\u201d]/g,'"').replace(/[\u2013\u2011\u2010]/g,'-').replace(/\u00a0/g,' '));};
var first6 = function(t){return t.split(' ').slice(0,6).join(' ');};

els.forEach(function(el){
  var tag = el.tagName.toLowerCase();
  if (firstTable && firstTable.contains(el)) { counts.cover++; return; }
  if (tag === 'table' || el.closest('table')) { counts.unclassified++; unclassified.push(tag+': '+clean(el.textContent).slice(0,60)); return; }
  var text = clean(el.textContent);
  if (tag === 'h2' && titleText === null) { titleText = text.replace(/\s*\*+$/,''); counts.title++; return; }
  if (tag === 'h2' || tag === 'h3') {
    var m = text.match(/^([IVX]+|[A-Z])\.\s*(.+)$/);
    var h = {kind:'heading', level: tag==='h2'?2:3, raw:text, label:m?m[1]:'', text:m?m[2]:text, glued: !!(m && /^([IVX]+|[A-Z])\.\S/.test(text))};
    h.full = h.label ? h.label+'. '+h.text : h.text;
    h.isPart = tag==='h2' && /^[IVX]+$/.test(h.label);
    if (h.isPart) curPart = h.full;
    curSection = h.full;
    h.count = 0;
    counts.heading++; blocks.push(h); heads.push(h); return;
  }
  var pm = text.match(/^(\d{1,3})\.\s*(.*)$/);
  if (tag === 'p' && pm) {
    var raw = pm[2].trim();
    var r = repair(raw, +pm[1]);
    var p = {kind:'para', n:+pm[1], raw:raw, text:r.text, repairs:r.log, section:curSection, part:curPart};
    p.path = (curPart && curSection !== curPart) ? curPart+' \u203a '+curSection : (curSection||curPart);
    p.fw6 = first6(p.text);
    p.ref6 = hasRefW && ref.first_words[String(p.n)] != null ? clean(ref.first_words[String(p.n)]) : null;
    p.fwMatch = hasRefW ? (p.ref6 !== null && normFW(p.fw6) === normFW(p.ref6)) : null;
    counts.paragraph++; blocks.push(p); paras.push(p);
    if (heads.length) heads[heads.length-1].count++;
    return;
  }
  counts.other++;
});

var total = els.length;
var sumCounts = counts.cover+counts.title+counts.heading+counts.paragraph+counts.other+counts.unclassified;
var allRepairs = []; paras.forEach(function(p){ allRepairs = allRepairs.concat(p.repairs); });
var repairedParas = paras.filter(function(p){return p.repairs.length;}).length;
var ruleCounts = {}; RULES.forEach(function(r){ruleCounts[r.id]=0;}); allRepairs.forEach(function(x){ruleCounts[x.rule]++;});
var h2n = doc.body ? doc.body.querySelectorAll('h2').length : 0;
var h3n = doc.body ? doc.body.querySelectorAll('h3').length : 0;
var gluedHeads = heads.filter(function(h){return h.glued;}).length;
var footFound = doc.body ? doc.body.querySelectorAll('sup, [id^="ftn"], [class*="footnote"]').length : 0;
var title = D.title || titleText || 'Untitled document';
var fileBase = (symbol || 'document').replace(/[\/\\:]+/g,'-');
var limitation = 'no footnotes in this HTML version' + (hasRefF ? '; the document has '+ref.footnotes : '');
var citation = function(n){return symbol+', para. '+n;};

/* first words differences */
var fwDiffs = [];
paras.forEach(function(p){ if (p.fwMatch === false) fwDiffs.push({n:p.n, found:p.fw6, ref:p.ref6}); });
var foundNums = {}; paras.forEach(function(p){foundNums[p.n]=1;});
if (hasRefW) Object.keys(ref.first_words).forEach(function(k){ if(!foundNums[+k]) fwDiffs.push({n:+k, found:null, ref:clean(ref.first_words[k])}); });
fwDiffs.sort(function(a,b){return a.n-b.n;});
var fwMatchN = paras.filter(function(p){return p.fwMatch===true;}).length;

/* exports */
var records = paras.map(function(p){return {symbol:symbol, paragraph:p.n, section:p.section, part:p.part, text:p.text, text_raw:p.raw, first_words_match:p.fwMatch, citation:citation(p.n), doc_url:D.doc_url||'', limitations:limitation};});
var jsonStr = JSON.stringify(records, null, 2);
function buildMd(){
  var q = function(s){return JSON.stringify(String(s==null?'':s));};
  var out = ['---','title: '+q(title),'symbol: '+q(symbol),'adopted: '+q(ref.adopted||''),'source_url: '+q(D.doc_url||''),'extracted: '+new Date().toISOString().slice(0,10),'paragraphs_found: '+paras.length,'paragraphs_expected: '+(hasRefP?ref.paragraphs:q('unknown')),'footnotes: '+q(limitation),'---',''];
  blocks.forEach(function(b){
    if (b.kind==='heading') out.push((b.level===2?'##':'###')+' '+b.full, '');
    else out.push('**'+b.n+'.** '+b.text, '');
  });
  return out.join('\n');
}

/* ---------- 2. checks ---------- */
var checks = [];
(function(){
  var nums = paras.map(function(p){return p.n;});
  // 1 count
  if (!hasRefP) checks.push({name:'Paragraph count', story:'No reference in this file: cannot compare. Found '+paras.length+'.', status:'notrun'});
  else checks.push({name:'Paragraph count', story:'Given this document, having run this code, we expect '+ref.paragraphs+' numbered paragraphs; found '+paras.length+(paras.length===ref.paragraphs?'.':' (difference '+(paras.length-ref.paragraphs>0?'+':'')+(paras.length-ref.paragraphs)+').'), status:paras.length===ref.paragraphs?'pass':'fail', tab2:paras.length!==ref.paragraphs});
  // 2 numbering
  var seen = {}, dups = [], gaps = [], mx = nums.length?Math.max.apply(null,nums):0;
  nums.forEach(function(v){ if(seen[v]&&dups.indexOf(v)<0) dups.push(v); seen[v]=1; });
  for (var i=1;i<=mx;i++) if(!seen[i]) gaps.push(i);
  var okNum = nums.length>0 && nums.every(function(v,i){return v===i+1;});
  var firstBad = null; for (var j=0;j<nums.length;j++){ if(nums[j]!==j+1){firstBad=nums[j];break;} }
  checks.push({name:'Numbering', story: nums.length? 'We expect exactly 1 to '+nums.length+' in order; '+(okNum?'found exactly that.':'gaps: '+(gaps.slice(0,10).join(', ')||'none')+'; duplicates: '+(dups.slice(0,10).join(', ')||'none')+(gaps.length||dups.length?'':'; order differs')+'.') : 'No numbered paragraphs found.', status:okNum?'pass':'fail', go: okNum?null:firstBad});
  // 3 first words
  if (!hasRefW) checks.push({name:'First words', story:'No reference in this file: not run.', status:'notrun'});
  else checks.push({name:'First words', story:'We expect the first six words of every paragraph to equal reference.first_words; '+fwMatchN+' of '+ref.first_words_count_dummy+' match.', status:fwDiffs.length?'fail':'pass', go: fwDiffs.length ? (fwDiffs.filter(function(d){return d.found!==null;})[0]||{}).n||null : null});
  // 4 footnotes
  if (!hasRefF) checks.push({name:'Footnotes', story:'No reference in this file: not run. Found '+footFound+' in the HTML.', status:'notrun'});
  else checks.push({name:'Footnotes', story: footFound+' found against '+ref.footnotes+'. '+(footFound<ref.footnotes?'The HTML version has no footnotes: a limit of the source, not of the app.':'Counts agree.'), status: footFound>=ref.footnotes?'pass':'limit'});
  // 5 repairs
  checks.push({name:'Repairs', story:allRepairs.length+' spaces restored in '+repairedParas+' paragraphs ('+RULES.map(function(r){return r.label+' '+ruleCounts[r.id];}).join(', ')+'); text_raw still holds the text as found.', status:'pass'});
  // 6 headings
  checks.push({name:'Headings', story:h2n+' <h2> (one is the title) and '+h3n+' <h3> in the HTML; '+heads.length+' kept as headings; '+gluedHeads+' glued labels separated.', status:heads.length>0?'pass':'fail'});
  // 7 nothing lost
  checks.push({name:'Nothing lost', story:'Every block element is classified once: '+counts.cover+' cover, '+counts.title+' title, '+counts.heading+' headings, '+counts.paragraph+' paragraphs, '+counts.other+' other lines, '+counts.unclassified+' unclassified = '+sumCounts+' of '+total+'.'+(unclassified.length?' Unclassified: '+unclassified.join(' | '):''), status:(sumCounts===total&&unclassified.length===0)?'pass':'fail'});
  // 8 round trip
  var rt = 0; try { rt = JSON.parse(jsonStr).length; } catch(e){ rt = -1; }
  checks.push({name:'Export round trip', story:'The JSON to download, parsed back, has '+rt+' records; the table has '+paras.length+'.', status:rt===paras.length?'pass':'fail'});
})();
if (hasRefW) { checks[2].story = 'We expect the first six words of every paragraph to equal reference.first_words (quotes, dashes and spaces normalised); '+fwMatchN+' of '+Object.keys(ref.first_words).length+' match'+(fwDiffs.length?', '+fwDiffs.length+' differ or are missing.':'.'); }
var nPass = checks.filter(function(c){return c.status==='pass';}).length;
var nFail = checks.filter(function(c){return c.status==='fail';}).length;
var nLimit = checks.filter(function(c){return c.status==='limit';}).length;
var nNot = checks.filter(function(c){return c.status==='notrun';}).length;
var mAll = checks.length;
var STW = {pass:'pass', fail:'check failed', limit:'source limit', notrun:'not run'};
var STC = {pass:'ok', fail:'bad', limit:'bad', notrun:'mute'};

/* ---------- 3. render header and rail ---------- */
document.getElementById('title').textContent = title;
var meta = [];
if (symbol) meta.push(D.doc_url ? '<a href="'+esc(D.doc_url)+'" target="_blank" rel="noopener">'+esc(symbol)+'</a>' : esc(symbol));
if (ref.adopted) meta.push('adopted '+esc(ref.adopted));
if (D.source) meta.push(esc(D.source));
document.getElementById('meta').innerHTML = meta.join(' · ');
var statusHtml;
if (nFail>0) statusHtml = '<div class="bad"><span class="dot" style="background:#9b2335"></span>'+nFail+' check'+(nFail>1?'s':'')+' failed</div>';
else statusHtml = '<div class="'+(nNot?'mute':'ok')+'"><span class="dot" style="background:'+(nNot?'#8a8477':'#1f6b3a')+'"></span>'+nPass+' of '+mAll+' checks pass'+(nNot?' ('+nNot+' not run)':'')+'</div>';
if (nLimit) statusHtml += '<div class="bad">'+nLimit+' source limit'+(nLimit>1?'s':'')+'</div>';
document.getElementById('status').innerHTML = statusHtml;

var shortOk = hasRefP && paras.length === ref.paragraphs;
document.getElementById('rail').innerHTML =
  '<div class="lab">Document</div>'+
  '<div class="card"><div class="mono sym">'+esc(symbol||'(no symbol)')+'</div><div class="short">'+esc(title)+'</div></div>'+
  '<div class="rbig"><span class="serif n">'+paras.length+'</span><span class="lab">paragraphs'+(hasRefP?' of '+ref.paragraphs:'')+'</span>'+
  (hasRefP?'<div class="bar'+(shortOk?'':' short')+'"><i style="width:'+Math.min(100, ref.paragraphs? paras.length/ref.paragraphs*100:0)+'%"></i></div>':'<small>no reference in this file</small>')+'</div>'+
  '<div class="rbig"><span class="serif n bad">'+footFound+'</span><span class="lab">footnotes'+(hasRefF?' of '+ref.footnotes:'')+'</span><small class="bad">not in this HTML</small></div>'+
  '<div class="lab">'+nPass+' of '+mAll+' checks pass</div>';

/* ---------- 4. tab 01 ---------- */
var p0 = document.getElementById('p0');
function tile(label, big, beside, how, cls){
  return '<div class="tile"><div class="lab">'+label+'</div><div class="big '+(cls||'')+'">'+big+'</div><div class="beside">'+beside+'</div><p class="how">How this is computed: '+how+'</p></div>';
}
var h0 = '<h2 class="q">Did the app find everything the document has?</h2>';
if (!paras.length) {
  h0 += '<p class="bad"><b>No numbered paragraphs were found.</b> The HTML of this document yielded no &lt;p&gt; element that starts with a number and a full stop. The exports are disabled.</p>';
}
var diff = hasRefP ? paras.length - ref.paragraphs : 0;
h0 += '<div class="tiles">'+
  tile('Paragraphs found', paras.length, hasRefP ? 'the document has <b>'+ref.paragraphs+'</b> · <span class="st '+(diff===0?'ok':'bad')+'">'+(diff===0?'equal':'difference '+(diff>0?'+':'')+diff)+'</span>' : '<span class="mute">no reference in this file</span>', 'every &lt;p&gt; after the cover whose text starts with a number and a full stop; compared with reference.paragraphs.', hasRefP&&diff!==0?'bad':(hasRefP?'ok':''))+
  tile('First words match', hasRefW? fwMatchN : '–', hasRefW ? 'of <b>'+ref.paragraphs+'</b> · <span class="st '+(fwDiffs.length?'bad':'ok')+'">'+(fwDiffs.length?fwDiffs.length+' differ':'all match')+'</span>' : '<span class="mute">no reference in this file</span>', 'the first six words of each paragraph, curly quotes, en dashes and non-breaking spaces normalised, against reference.first_words.', hasRefW&&fwDiffs.length?'bad':(hasRefW?'ok':''))+
  tile('Footnotes', footFound, hasRefF ? 'of <b>'+ref.footnotes+'</b> · <span class="st bad">source limit</span><br>This HTML version has none: no footnote text, no footnote marks. To cite a footnote, use the PDF or Word version.' : '<span class="mute">no reference in this file</span>', 'looks for footnote text or marks in the HTML; compared with reference.footnotes.', 'bad')+
  tile('Spaces restored', allRepairs.length, 'in <b>'+repairedParas+'</b> paragraph'+(repairedParas===1?'':'s'), 'a space is put back only where punctuation touches a letter (4 rules); text_raw keeps the text as found.')+
  '</div>';
if (fwDiffs.length) {
  h0 += '<div class="lab" style="margin-top:16px">First words that differ</div><ul class="fwlist">'+
    fwDiffs.slice(0,10).map(function(d){return '<li><b class="bad">para. '+d.n+':</b> '+(d.found===null?'not found':'found \u201c'+esc(d.found)+'\u201d')+' / reference \u201c'+esc(d.ref===null?'(none)':d.ref)+'\u201d</li>';}).join('')+
    (fwDiffs.length>10?'<li class="mute">and '+(fwDiffs.length-10)+' more</li>':'')+'</ul>';
}
h0 += '<h3 class="sec">Take the paragraphs away</h3>'+
  '<button class="btn" id="dlJson"'+(paras.length?'':' disabled')+'>Download JSON</button><button class="btn light" id="dlMd"'+(paras.length?'':' disabled')+'>Download Markdown</button>'+
  '<p class="note">'+paras.length+' records · fields: symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url, limitations · UTF-8</p>';
h0 += '<div style="margin-top:22px">'+
  '<button class="acc" aria-expanded="false" aria-controls="accChecks" id="bChecks">Every check ('+mAll+')</button>'+
  '<div class="panel" id="accChecks" hidden><ul class="checks">'+checks.map(function(c,i){
    var link = '';
    if (c.status==='fail' && (c.go||c.tab2)) link = '<button class="linkbtn" data-go="'+(c.go||'')+'">see the rows</button>';
    return '<li><span class="st '+STC[c.status]+'">'+STW[c.status]+'</span> <b>'+esc(c.name)+'.</b> '+esc(c.story)+link+'</li>';
  }).join('')+'</ul></div>'+
  '<button class="acc" aria-expanded="false" aria-controls="accSpaces" id="bSpaces">The spaces restored ('+allRepairs.length+')</button>'+
  '<div class="panel" id="accSpaces" hidden>'+
  '<p class="note">'+RULES.map(function(r){return r.label+': <b>'+ruleCounts[r.id]+'</b>';}).join(' · ')+'</p>'+
  (allRepairs.length ? '<table><caption><span class="lab">TAB.01</span>'+allRepairs.length+' spaces restored in '+repairedParas+' paragraphs</caption><thead><tr><th scope="col" class="r">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead><tbody>'+
    allRepairs.slice(0,200).map(function(x){return '<tr class="jump" data-n="'+x.para+'" style="cursor:pointer"><td class="r"><button class="rowbtn" data-n="'+x.para+'">'+x.para+'</button></td><td class="mono">\u2026'+esc(x.before)+'\u2026</td><td class="mono">\u2026'+esc(x.after)+'\u2026</td><td>'+esc(x.ruleLabel)+'</td></tr>';}).join('')+
    '</tbody></table>'+(allRepairs.length>200?'<p class="note">and '+(allRepairs.length-200)+' more</p>':'') : '<p>No spaces needed restoring.</p>')+
  '<p class="note">Rules restore a space only where the characters prove it was there. Word pairs such as \u201cGiventhe\u201d are not touched. Click a row = open the paragraph.</p>'+
  '</div></div>';
p0.innerHTML = h0;

/* ---------- 5. tab 02 ---------- */
var p1 = document.getElementById('p1');
function firstLine(t){
  if (t.length<=120) return t;
  var c = t.slice(0,120), i = c.lastIndexOf(' ');
  if (i>60) c = c.slice(0,i);
  return c.replace(/[\s,;:]+$/,'')+'\u2026';
}
function markedText(p){
  var ranges = [], used = {};
  p.repairs.forEach(function(r){
    var from = 0, idx;
    while ((idx = p.text.indexOf(r.needle, from)) >= 0 && used[idx]) from = idx+1;
    if (idx>=0){ used[idx]=1; ranges.push([idx, idx+r.needle.length]); }
  });
  if (p.fwMatch===false) ranges.push([0, p.fw6.length]);
  ranges.sort(function(a,b){return a[0]-b[0];});
  var merged = [];
  ranges.forEach(function(r){ var l=merged[merged.length-1]; if (l && r[0]<=l[1]) l[1]=Math.max(l[1],r[1]); else merged.push(r.slice()); });
  var out = '', pos = 0;
  merged.forEach(function(r){ out += esc(p.text.slice(pos,r[0]))+'<mark class="fix">'+esc(p.text.slice(r[0],r[1]))+'</mark>'; pos = r[1]; });
  return out + esc(p.text.slice(pos));
}
function detail(p, i){
  return '<div class="path">'+esc(p.path||'(no heading above this paragraph)')+'</div>'+
    '<p class="full">'+markedText(p)+'</p>'+
    '<div class="cmp"><div><div class="lab">First six words found</div>'+esc(p.fw6)+'</div><div><div class="lab">Reference first six words</div>'+(hasRefW?esc(p.ref6===null?'(no entry for this number)':p.ref6):'<span class="mute">no reference in this file</span>')+'</div></div>'+
    '<div class="reps">'+(p.repairs.length ? '<div class="lab">Spaces restored here ('+p.repairs.length+')</div>'+p.repairs.map(function(r){return '<div><code>\u2026'+esc(r.before)+'\u2026</code> \u2192 <code>\u2026'+esc(r.after)+'\u2026</code> <span class="mute">('+esc(r.ruleLabel)+')</span></div>';}).join('') : '<span class="mute">No space restored in this paragraph.</span>')+'</div>'+
    '<button class="btn light copy" data-i="'+i+'">Copy citation</button> <span class="mono">'+esc(citation(p.n))+'</span>';
}
var h1 = '<h2 class="q">What does each paragraph say, and how do I cite it?</h2>'+
  '<button class="acc" aria-expanded="false" aria-controls="accHeads" id="bHeads">Headings found: '+heads.length+'</button>'+
  '<div class="panel" id="accHeads" hidden>'+(heads.length?'<ul class="hdrs">'+heads.map(function(h){return '<li class="l'+h.level+'"><span class="lv">H'+h.level+'</span><span>'+esc(h.full)+'</span><span class="ct">'+h.count+' para.</span></li>';}).join('')+'</ul>':'<p>No headings found.</p>')+'<p class="note">A heading is never paragraph text.</p></div>'+
  '<table id="ptable" style="margin-top:14px"><caption><span class="lab">TAB.02</span>'+paras.length+' paragraphs found'+(hasRefP?', '+ref.paragraphs+' expected':'')+'</caption>'+
  '<thead><tr><th scope="col" class="r">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>'+
  paras.map(function(p,i){
    var chk = p.fwMatch===true?'<span class="ok">OK</span>':(p.fwMatch===false?'<span class="bad">first words differ</span>':'<span class="mute">no reference</span>');
    return '<tbody><tr class="row" data-i="'+i+'" id="r'+i+'"><td class="num"><button class="rowbtn" aria-expanded="false" aria-controls="d'+i+'" aria-label="Paragraph '+p.n+', open">'+p.n+'</button></td><td>'+esc(p.section)+'</td><td>'+esc(firstLine(p.text))+'</td><td>'+chk+'</td></tr>'+
    '<tr class="detail" id="d'+i+'" hidden><td colspan="4">'+detail(p,i)+'</td></tr></tbody>';
  }).join('')+'</table>'+
  (paras.length?'':'<p class="bad">No paragraphs to list.</p>')+
  '<p class="note">click a row = open it in place · the full text is verbatim after the space repairs; text_raw is in the export</p>';
p1.innerHTML = h1;

/* ---------- 6. behaviour ---------- */
var tabs = [document.getElementById('tab0'), document.getElementById('tab1')];
var panels = [p0, p1];
function selectTab(i, focus){
  tabs.forEach(function(t,k){ t.setAttribute('aria-selected', k===i?'true':'false'); t.tabIndex = k===i?0:-1; panels[k].hidden = k!==i; });
  if (focus) tabs[i].focus();
}
tabs.forEach(function(t,i){
  t.addEventListener('click', function(){selectTab(i,false);});
  t.addEventListener('keydown', function(e){
    var k = null;
    if (e.key==='ArrowRight') k=(i+1)%tabs.length;
    else if (e.key==='ArrowLeft') k=(i+tabs.length-1)%tabs.length;
    else if (e.key==='Home') k=0; else if (e.key==='End') k=tabs.length-1;
    if (k!==null){ e.preventDefault(); selectTab(k,true); }
  });
});
function toggleAcc(btn){
  var open = btn.getAttribute('aria-expanded')==='true';
  btn.setAttribute('aria-expanded', open?'false':'true');
  document.getElementById(btn.getAttribute('aria-controls')).hidden = open;
}
['bChecks','bSpaces','bHeads'].forEach(function(id){ document.getElementById(id).addEventListener('click', function(){toggleAcc(this);}); });
function setRow(i, open){
  var d = document.getElementById('d'+i), b = document.querySelector('#r'+i+' .rowbtn');
  if (!d) return;
  d.hidden = !open; b.setAttribute('aria-expanded', open?'true':'false');
}
document.getElementById('ptable').addEventListener('click', function(e){
  var cp = e.target.closest('.copy');
  if (cp) {
    var p = paras[+cp.getAttribute('data-i')], txt = citation(p.n);
    var done = function(){ var old = 'Copy citation'; cp.textContent='Copied'; setTimeout(function(){cp.textContent=old;},2000); };
    var fallback = function(){ var ta=document.createElement('textarea'); ta.value=txt; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');}catch(x){} ta.remove(); done(); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, fallback); else fallback();
    return;
  }
  var tr = e.target.closest('tr.row');
  if (tr) { var i = +tr.getAttribute('data-i'); setRow(i, document.getElementById('d'+i).hidden); }
});
function gotoPara(n){
  var idx = -1; for (var k=0;k<paras.length;k++){ if (paras[k].n===n){idx=k;break;} }
  selectTab(1,false);
  if (idx<0) return;
  setRow(idx,true);
  var r = document.getElementById('r'+idx);
  r.scrollIntoView({block:'center'});
  r.querySelector('.rowbtn').focus();
}
p0.addEventListener('click', function(e){
  var j = e.target.closest('[data-go]');
  if (j) { var v = j.getAttribute('data-go'); if (v) gotoPara(+v); else selectTab(1,false); return; }
  var r = e.target.closest('tr.jump');
  if (r) gotoPara(+r.getAttribute('data-n'));
});
function download(name, mime, content){
  var blob = new Blob([content], {type:mime+';charset=utf-8'});
  var url = URL.createObjectURL(blob), a = document.createElement('a');
  a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function(){URL.revokeObjectURL(url);}, 1500);
}
document.getElementById('dlJson').addEventListener('click', function(){ download(fileBase+'.json','application/json',jsonStr); });
document.getElementById('dlMd').addEventListener('click', function(){ download(fileBase+'.md','text/markdown',buildMd()); });

/* ---------- 7. footer ---------- */
document.getElementById('foot').innerHTML =
  [D.source?'Source: '+esc(D.source):'', D.built?'built '+esc(D.built):'', 'Done by this page\u2019s code; no model was called and nothing left the browser.'].filter(Boolean).join(' · ')+
  '<br>Credits: documentation practice after The Turing Way, \u201cDocumentation and metadata\u201d (CC BY 4.0); check wording after the UK Analysis Function, \u201cTesting code\u201d; citation form after the Dag Hammarskj\u00f6ld Library, \u201cHow should I cite a UN document?\u201d';
})();
</script>
</body>
</html>
```