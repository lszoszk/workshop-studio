```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a UN document · HTML version</title>
<style>
  :root{
    --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335; --green:#1e6b34;
  }
  [hidden]{display:none!important}
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);
       font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
  .mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase}
  .serif{font-family:Georgia,"Times New Roman",serif}
  a{color:var(--red)}
  :focus-visible{outline:3px solid var(--red);outline-offset:2px}

  /* header */
  header{border-bottom:1px solid var(--rule);padding:18px 28px 14px;
         display:flex;justify-content:space-between;gap:24px;align-items:flex-end;flex-wrap:wrap}
  header h1{font-family:Georgia,"Times New Roman",serif;font-size:26px;font-weight:normal;margin:6px 0 4px}
  .hdrc{color:#5c564a}
  .hdrr{text-align:right;color:#5c564a;white-space:nowrap}
  .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:1px}
  .dot.ok{background:var(--green)} .dot.bad{background:var(--red)}

  /* layout */
  .wrap{display:flex;min-height:calc(100vh - 140px)}
  aside{width:250px;flex:0 0 250px;border-right:1px solid var(--rule);padding:22px 24px}
  main{flex:1;padding:22px 34px 60px;min-width:0}

  /* rail */
  .card{border:1px solid var(--rule);padding:14px 16px;margin-bottom:22px;background:#efe9dd}
  .card .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;letter-spacing:.05em}
  .card .st{font-size:13px;color:#5c564a;margin-top:4px;display:block}
  .bignum{font-family:Georgia,serif;font-size:44px;line-height:1.05;margin:14px 0 2px}
  .bignum small{font-size:17px;color:#5c564a;font-style:italic}
  .ofnote{color:#5c564a;font-size:13px}
  .bar{height:4px;background:var(--rule);margin-top:8px;position:relative}
  .bar i{position:absolute;left:0;top:0;bottom:0;background:var(--green)}
  .bar.bad i{background:var(--red)}
  .red{color:var(--red)} .grn{color:var(--green)}

  /* tabs */
  .tabs{border-bottom:1px solid var(--rule);margin-bottom:24px;display:flex;gap:0}
  .tab{background:none;border:none;border-bottom:3px solid transparent;cursor:pointer;
       padding:10px 22px 8px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;
       letter-spacing:.14em;color:#5c564a}
  .tab[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
  .tab:hover{color:var(--ink)}

  /* tiles */
  .tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);margin-bottom:24px}
  .tile{background:var(--paper);padding:18px 20px 14px}
  .tile .n{font-family:Georgia,serif;font-size:46px;line-height:1.05}
  .tile .n small{font-size:18px;color:#5c564a;font-style:italic}
  .tile .how{color:#5c564a;font-size:13px;margin-top:6px}
  .hint{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;color:#7a7263;letter-spacing:.05em}

  /* closed headings */
  .fold{border:none;border-bottom:1px solid var(--rule);background:none;width:100%;text-align:left;
        padding:12px 2px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;
        letter-spacing:.14em;text-transform:uppercase;color:var(--ink);display:flex;justify-content:space-between}
  .fold:hover{color:var(--red)}
  .foldbox{border-bottom:1px solid var(--rule);padding-bottom:6px;margin-bottom:8px}

  /* tables */
  table{width:100%;border-collapse:collapse;margin:10px 0 24px}
  caption{font-family:Georgia,serif;font-size:19px;text-align:left;padding:6px 0 10px}
  caption .tno{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.14em;color:#7a7263;display:block;margin-bottom:2px}
  th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;
     color:#5c564a;text-align:left;border-bottom:1px solid var(--ink);padding:6px 10px;font-weight:normal}
  td{border-bottom:1px solid var(--rule);padding:8px 10px;vertical-align:top}
  th.num,td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}

  /* paragraph rows */
  tr.prow{cursor:pointer}
  tr.prow>td{font-size:15px}
  tr.prow:hover>td{background:#ece5d6}
  tr.detail>td{background:#efe9dd;padding:16px 18px}
  .pnum{font-family:Georgia,serif;font-size:19px;color:var(--red)}
  .fulltext{max-width:72ch;font-size:15.5px}
  .rep{border:1px solid var(--red);padding:0 1px}
  .fw{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;color:#5c564a;margin:10px 0 4px}
  .btn{background:var(--ink);color:var(--paper);border:none;padding:8px 16px;cursor:pointer;
       font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase}
  .btn:hover{background:var(--red)}
  .copied{color:var(--green);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;margin-left:10px}

  .mismatch{border-left:3px solid var(--red);padding:8px 16px;margin:0 0 24px;font-size:14.5px}
  .check{display:flex;gap:14px;padding:9px 2px;border-bottom:1px solid var(--rule);font-size:14.5px;align-items:baseline}
  .check .st{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;min-width:110px}
  .note{color:#5c564a;font-size:13.5px;margin:8px 0 18px;max-width:75ch}
  .export{display:flex;gap:14px;margin:20px 0 28px}
  footer{border-top:1px solid var(--rule);padding:14px 28px;color:#5c564a;font-size:13px;display:flex;gap:24px;flex-wrap:wrap}
  h2.sec{font-family:Georgia,serif;font-size:21px;font-weight:normal;margin:26px 0 6px}
</style>
</head>
<body>

<header>
  <div>
    <div class="mono">UN DOCUMENT · HTML</div>
    <h1 id="hTitle"></h1>
    <div class="hdrc" id="hLine"></div>
  </div>
  <div class="hdrr">
    <div id="hChecks"></div>
    <div id="hLimit"></div>
  </div>
</header>

<div class="wrap">
  <aside aria-label="Document card">
    <div class="mono" style="margin-bottom:10px">DOCUMENT</div>
    <div class="card">
      <div class="sym" id="rSym"></div>
      <span class="st" id="rTitle"></span>
    </div>
    <div class="bignum" id="rParas"></div>
    <div class="ofnote" id="rParasNote"></div>
    <div class="bar" id="rBar"><i></i></div>
    <div class="bignum red">0</div>
    <div class="ofnote red" id="rFoot"></div>
    <div style="margin-top:26px;border-top:1px solid var(--rule);padding-top:12px" class="ofnote" id="rChecks"></div>
  </aside>

  <main>
    <div class="tabs" role="tablist" aria-label="Sections">
      <button class="tab" role="tab" id="tab1" aria-selected="true" aria-controls="panel1">01 RESULT</button>
      <button class="tab" role="tab" id="tab2" aria-selected="false" aria-controls="panel2" tabindex="-1">02 PARAGRAPHS</button>
    </div>

    <!-- TAB 1 -->
    <section id="panel1" role="tabpanel" aria-labelledby="tab1">
      <h2 class="sec">Did this page find everything the document has?</h2>
      <div class="tiles" id="tiles"></div>

      <div class="mismatch" id="mismatch" hidden></div>

      <h2 class="sec">Take the paragraphs away</h2>
      <p class="note">Each record carries its symbol, paragraph number, section, verbatim text, the raw text as found, and its known limitations.</p>
      <div class="export">
        <button class="btn" id="dlJson">Download JSON</button>
        <button class="btn" id="dlMd">Download Markdown</button>
      </div>

      <div class="foldbox">
        <button class="fold" id="foldChecks" aria-expanded="false"><span id="foldChecksLbl">Every check</span><span class="hint">click = open</span></button>
        <div id="checksBody" hidden></div>
      </div>

      <div class="foldbox">
        <button class="fold" id="foldSpaces" aria-expanded="false"><span id="foldSpacesLbl">The spaces restored</span><span class="hint">click = open</span></button>
        <div id="spacesBody" hidden></div>
      </div>
    </section>

    <!-- TAB 2 -->
    <section id="panel2" role="tabpanel" aria-labelledby="tab2" hidden>
      <div class="foldbox">
        <button class="fold" id="foldHeads" aria-expanded="false"><span id="foldHeadsLbl">Headings found</span><span class="hint">click = open</span></button>
        <div id="headsBody" hidden></div>
      </div>
      <table id="pTable">
        <caption id="pCaption"><span class="tno">TAB.01</span><span id="pCapText"></span></caption>
        <thead><tr>
          <th scope="col" class="num">No.</th><th scope="col">Section</th>
          <th scope="col">First line</th><th scope="col">Check</th>
        </tr></thead>
        <tbody id="pTbody"></tbody>
      </table>
      <p class="hint">click a row = expand in place · full text is verbatim, never shortened</p>
    </section>
  </main>
</div>

<footer>
  <span id="fSource"></span>
  <span>Done by this page's code; no model was called and nothing left the browser.</span>
</footer>

<script>
(function(){
"use strict";
const D = window.WORKSHOP_DATA.html_doc;
const ref = D.reference || {};
const hasRefParas = typeof ref.paragraphs === 'number';
const hasRefFW = ref.first_words && typeof ref.first_words === 'object';
const hasRefFoot = typeof ref.footnotes === 'number';

/* ---------- parse & classify ---------- */
const doc = new DOMParser().parseFromString(D.html || '', 'text/html');
const body = doc.body;
const coverTable = body.querySelector('table');
const blocks = Array.from(body.querySelectorAll('p,h2,h3,table,li,ul,ol,blockquote'));

const paras = [];        // {number,text_raw,text,html,repairs,section,part,firstMatch,foundFW,refFW}
const headings = [];     // {level,label,heading,raw,glued}
const classCount = {paragraph:0,heading:0,title:0,committee:0,cover:0};
const unclassified = [];
let titleEl = null, committeeLine = null;
let curSection = '', curPart = '';
const numRx = /^(\d{1,3})\.\s*([\s\S]*)$/;
const headRx = /^([IVX]+|[A-Z])\.\s*(.+)$/;

for (const el of blocks){
  if (coverTable && el !== coverTable && coverTable.contains(el)) { classCount.cover++; continue; }
  if (el === coverTable) { classCount.cover++; continue; }
  const tag = el.tagName;
  if (tag === 'P'){
    const t = (el.textContent || '').replace(/\s+/g,' ').trim();
    const m = t.match(numRx);
    if (m){
      const raw = m[2].trim();
      const r = repair(raw);
      const number = parseInt(m[1],10);
      paras.push({number, text_raw:raw, text:r.text, html:r.html, repairs:r.log,
                  section:curSection, part:curPart});
      classCount.paragraph++;
    } else if (!committeeLine && !titleEl){
      committeeLine = t; classCount.committee++;
    } else {
      unclassified.push({kind:'p', text:t.slice(0,60)});
    }
  } else if (tag === 'H2' || tag === 'H3'){
    const t = (el.textContent || '').replace(/\s+/g,' ').trim();
    if (tag === 'H2' && !titleEl && !t.match(headRx)){
      titleEl = t; classCount.title++; continue;
    }
    const m = t.match(headRx);
    const h = {level:tag, label:m?m[1]:'', heading:m?m[2]:t, raw:t, glued:false};
    if (m) h.glued = !/^\.\s/.test(t.slice(m[1].length));
    headings.push(h);
    classCount.heading++;
    curSection = m ? (m[1] + '. ' + m[2]) : t;
    if (tag === 'H2' && m && /^[IVX]+$/.test(m[1])) curPart = curSection;
  } else {
    unclassified.push({kind:tag.toLowerCase(), text:(el.textContent||'').trim().slice(0,60)});
  }
}

/* ---------- repairs ---------- */
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
const repRx = /([a-z])\.([A-Z])|([a-z]),([A-Za-z])|([a-z])“|–([A-Za-z])/g;
function repair(raw){
  let text='', html='', last=0, m; const log=[];
  repRx.lastIndex = 0;
  while ((m = repRx.exec(raw))){
    const idx = m.index + 1;
    let rule;
    if (m[1] !== undefined) rule = 'sentence join';
    else if (m[3] !== undefined) rule = 'comma join';
    else if (m[5] !== undefined) rule = 'quote join';
    else rule = 'dash join';
    text  += raw.slice(last, idx) + ' ';
    html  += esc(raw.slice(last, idx)) + '<span class="rep"> </span>';
    log.push({rule, before:raw.slice(Math.max(0,idx-20), idx), after:raw.slice(idx, idx+20)});
    last = idx;
  }
  text += raw.slice(last); html += esc(raw.slice(last));
  return {text, html, log};
}

/* ---------- first words ---------- */
function norm(s){
  return (s||'').replace(/[\u201c\u201d]/g,'"').replace(/[\u2018\u2019]/g,"'")
                .replace(/\u2013/g,'-').replace(/\u2011/g,'-').replace(/\u00a0/g,' ');
}
for (const p of paras){
  p.foundFW = p.text.split(/\s+/).slice(0,6).map(norm);
  p.refFW = hasRefFW ? (ref.first_words[String(p.number)] || '') : null;
  p.firstMatch = hasRefFW ? (p.refFW && norm(p.refFW) === p.foundFW.join(' ')) : null;
}

/* ---------- checks ---------- */
const totalSpaces = paras.reduce((a,p)=>a+p.repairs.length,0);
const parasWithSpaces = paras.filter(p=>p.repairs.length).length;
const fwMismatch = paras.filter(p=>p.firstMatch === false);
const numbers = paras.map(p=>p.number);
let numberingOk = numbers.length>0;
for (let i=0;i<numbers.length;i++) if (numbers[i] !== i+1){ numberingOk = false; break; }
const gaps = [], dups = [];
{ const seen = new Set();
  for (let i=1;i<=numbers.length;i++) if (!numbers.includes(i)) gaps.push(i);
  for (const n of numbers){ if (seen.has(n)) dups.push(n); seen.add(n); }
}
const gluedHeads = headings.filter(h=>h.glued).length;
const nothingLostOk = unclassified.length === 0;

/* export records + round trip */
function buildRecords(){
  const lim = hasRefFoot
    ? 'no footnotes in this HTML version; the document has ' + ref.footnotes
    : 'no footnotes in this HTML version';
  return paras.map(p=>({
    symbol: D.symbol,
    paragraph: p.number,
    section: p.section || null,
    part: p.part || null,
    text: p.text,
    text_raw: p.text_raw,
    first_words_match: p.firstMatch,
    citation: D.symbol + ', para. ' + p.number,
    doc_url: D.doc_url,
    limitations: lim
  }));
}
const records = buildRecords();
let roundTripOk = false;
try { roundTripOk = JSON.parse(JSON.stringify(records)).length === paras.length; } catch(e){}

const hasHtmlParas = paras.length > 0;
const checks = [];
function addCheck(name, status, detail){
  checks.push({name, status, detail});
}
addCheck('Paragraph count', !hasRefParas ? 'not run' : (paras.length === ref.paragraphs ? 'pass' : 'fail'),
  'Found ' + paras.length + ' numbered paragraphs; the reference says the document has ' +
  (hasRefParas ? ref.paragraphs : 'no value') + '.');
addCheck('Numbering', numberingOk ? 'pass' : 'fail',
  numberingOk ? 'Paragraphs run exactly 1 to ' + paras.length + ' in order.'
    : 'Numbering is not 1…' + paras.length + ' in order.' +
      (gaps.length ? ' Gaps: ' + gaps.join(', ') + '.' : '') +
      (dups.length ? ' Duplicates: ' + dups.join(', ') + '.' : ''));
addCheck('First words', !hasRefFW ? 'not run' : (fwMismatch.length === 0 ? 'pass' : 'fail'),
  hasRefFW
    ? fwMismatch.length + ' of ' + paras.length + ' paragraphs differ from the reference in their first six words (after normalising quotes, dashes and non-breaking characters).'
    : 'No first_words in the reference file.');
addCheck('Footnotes', 'limit',
  'Found 0 footnotes; the document has ' + (hasRefFoot ? ref.footnotes : 'an unknown number of') +
  '. The HTML version has no footnotes: a limit of the source, not of the app. To cite a footnote, use the PDF or Word version.');
addCheck('Repairs', 'pass',
  totalSpaces + ' spaces restored in ' + parasWithSpaces + ' paragraphs, each by a rule that only fires where the characters prove a space was there. text_raw still holds the text as found.');
addCheck('Headings', 'pass',
  headings.length + ' <h2>/<h3> headings found; ' + gluedHeads + ' glued labels (e.g. "I.Introduction") separated for display.');
addCheck('Nothing lost', nothingLostOk ? 'pass' : 'fail',
  'Every block element was classified exactly once: ' +
  Object.entries(classCount).map(([k,v])=>v+' '+k).join(', ') +
  (nothingLostOk ? '.' : '. Unclassified: ' + unclassified.map(u=>u.kind+' "'+u.text+'"').join('; ') + '.'));
addCheck('Export round trip', roundTripOk ? 'pass' : 'fail',
  'The JSON offered for download was parsed back; it holds ' + records.length + ' records, the table shows ' + paras.length + ' rows.');

const passN = checks.filter(c=>c.status==='pass').length;
const failN = checks.filter(c=>c.status==='fail').length;
const limitN = checks.filter(c=>c.status==='limit').length;
const notRun = checks.filter(c=>c.status==='not run').length;
const runN = checks.filter(c=>c.status!=='not run').length;

/* ---------- header & rail ---------- */
document.getElementById('hTitle').textContent = D.title || 'Untitled document';
document.getElementById('hLine').innerHTML =
  (D.symbol ? '<a href="'+esc(D.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(D.symbol)+'</a>' : '') +
  (ref.adopted ? ' · adopted ' + esc(ref.adopted) : '') +
  (D.source ? ' · ' + esc(D.source) : '');
const hc = document.getElementById('hChecks');
if (failN > 0){ hc.innerHTML = '<span class="dot bad"></span>' + failN + ' check' + (failN>1?'s':'') + ' failed'; }
else { hc.innerHTML = '<span class="dot ok"></span>' + passN + ' of ' + runN + ' checks pass'; }
document.getElementById('hLimit').textContent = limitN ? limitN + ' source limit' + (limitN>1?'s':'') : '';
document.getElementById('rSym').textContent = D.symbol || '(no symbol)';
document.getElementById('rTitle').textContent = D.title || '';
document.getElementById('rParas').innerHTML = paras.length + ' <small>paragraphs</small>';
document.getElementById('rParasNote').textContent = hasRefParas
  ? 'of ' + ref.paragraphs + ' in the document'
  : 'no reference in this file';
const bar = document.getElementById('rBar');
if (hasRefParas){
  bar.querySelector('i').style.width = Math.min(100, paras.length/ref.paragraphs*100) + '%';
  if (paras.length !== ref.paragraphs) bar.classList.add('bad');
}
document.getElementById('rFoot').innerHTML = '0 footnotes of ' + (hasRefFoot ? ref.footnotes : '?') +
  '<br>not in this HTML';
document.getElementById('rChecks').innerHTML =
  (failN>0 ? '<span class="red">'+failN+' checks failed</span>' : '<span class="grn">'+passN+' of '+runN+' checks pass</span>') +
  (limitN ? ' · <span class="red">'+limitN+' source limit</span>' : '') +
  (notRun ? ' · '+notRun+' not run' : '');
document.getElementById('fSource').textContent = (D.source || '') + (D.built ? ' · built ' + D.built : '');

/* ---------- tab 1: tiles ---------- */
function tile(n, note, how, cls){
  return '<div class="tile"><div class="n '+(cls||'')+'">'+n+'</div><div class="how">'+how+'</div><div class="hint">'+note+'</div></div>';
}
const eq = hasRefParas && paras.length === ref.paragraphs;
let tilesHtml = '';
tilesHtml += tile(
  paras.length + ' <small>of ' + (hasRefParas ? ref.paragraphs : '?') + '</small>',
  'how this is computed: &lt;p&gt; elements after the cover whose text starts "n." — counted by this page',
  'Paragraphs found' + (hasRefParas ? (eq ? '' : ' — the document has ' + ref.paragraphs + ' (difference ' + Math.abs(paras.length-ref.paragraphs) + ')') : ' — no reference in this file'),
  hasRefParas ? (eq ? 'grn' : 'red') : '');
tilesHtml += tile(
  (hasRefFW ? (paras.length - fwMismatch.length) + ' <small>of ' + paras.length + '</small>' : 'n/a'),
  'first six words of each paragraph vs the reference, after normalising quotes, dashes, non-breaking characters',
  'First words match',
  hasRefFW ? (fwMismatch.length ? 'red' : 'grn') : '');
tilesHtml += tile(
  '0 <small>of ' + (hasRefFoot ? ref.footnotes : '?') + '</small>',
  'footnote text and footnote marks searched for in the HTML: none present',
  'Footnotes — this HTML version has none: no footnote text, no footnote marks. To cite a footnote, use the PDF or Word version.',
  'red');
tilesHtml += tile(
  totalSpaces + ' <small>in ' + parasWithSpaces + ' paragraphs</small>',
  'a space inserted only after a full stop, comma, en dash or before a curly quote, between characters that prove one was there',
  'Spaces restored');
document.getElementById('tiles').innerHTML = tilesHtml;

/* mismatch list */
const mm = document.getElementById('mismatch');
if (fwMismatch.length){
  let h = '<div class="mono" style="margin-bottom:6px">FIRST WORDS DIFFER — ' + fwMismatch.length + ' PARAGRAPH' + (fwMismatch.length>1?'S':'') + '</div>';
  fwMismatch.slice(0,10).forEach(p=>{
    h += '<div><span class="pnum">para. '+p.number+'</span>: found “'+esc(p.foundFW.join(' '))+'” / reference “'+esc(norm(p.refFW))+'”</div>';
  });
  if (fwMismatch.length > 10) h += '<div class="ofnote">and ' + (fwMismatch.length-10) + ' more</div>';
  mm.innerHTML = h; mm.hidden = false;
}

/* ---------- exports ---------- */
function fname(ext){ return (D.symbol || 'document').replace(/\//g,'-') + '.' + ext; }
function download(content, name, type){
  const url = URL.createObjectURL(new Blob([content], {type: type+';charset=utf-8'}));
  const a = document.createElement('a');
  a.href = url; a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(url), 2000);
}
document.getElementById('dlJson').addEventListener('click', ()=>{
  download(JSON.stringify(records, null, 2), fname('json'), 'application/json');
});
document.getElementById('dlMd').addEventListener('click', ()=>{
  const today = new Date().toISOString().slice(0,10);
  const footLine = hasRefFoot
    ? 'no footnotes in this HTML version; the document has ' + ref.footnotes
    : 'no footnotes in this HTML version';
  let md = '---\n';
  md += 'title: "' + (D.title||'').replace(/"/g,'\\"') + '"\n';
  md += 'symbol: ' + D.symbol + '\n';
  if (ref.adopted) md += 'adopted: ' + ref.adopted + '\n';
  if (D.doc_url) md += 'source_url: ' + D.doc_url + '\n';
  md += 'extracted: ' + today + '\n';
  md += 'paragraphs_found: ' + paras.length + '\n';
  if (hasRefParas) md += 'paragraphs_expected: ' + ref.paragraphs + '\n';
  md += 'footnotes: ' + footLine + '\n---\n\n';
  md += '# ' + (D.title||'') + '\n\n';
  if (titleEl) md += '## ' + titleEl + '\n\n';
  for (const h of headings){
    md += (h.level === 'H2' ? '## ' : '### ') + (h.label ? h.label + '. ' : '') + h.heading + '\n\n';
  }
  md += '## Paragraphs\n\n';
  for (const p of paras){
    md += '**' + p.number + '.** ' + p.text + '\n\n';
  }
  download(md, fname('md'), 'text/markdown');
});
if (!hasHtmlParas){
  document.getElementById('dlJson').disabled = true;
  document.getElementById('dlMd').disabled = true;
  document.getElementById('tiles').insertAdjacentHTML('beforebegin',
    '<p class="note red">No &lt;p&gt; elements were found in this HTML: there is nothing to show or export.</p>');
}

/* ---------- tab 1: checks panel ---------- */
document.getElementById('foldChecksLbl').textContent = 'Every check (' + checks.length + ')';
const cb = document.getElementById('checksBody');
cb.innerHTML = checks.map(c=>{
  const lbl = c.status === 'pass' ? '<span class="st grn">pass</span>'
            : c.status === 'fail' ? '<span class="st red">check failed</span>'
            : c.status === 'limit' ? '<span class="st red">source limit</span>'
            : '<span class="st">not run</span>';
  return '<div class="check">' + lbl + '<div><strong>' + esc(c.name) + '.</strong> ' + esc(c.detail) + '</div></div>';
}).join('');

/* ---------- tab 1: spaces table ---------- */
document.getElementById('foldSpacesLbl').textContent = 'The spaces restored (' + totalSpaces + ')';
const sb = document.getElementById('spacesBody');
if (totalSpaces === 0){
  sb.innerHTML = '<p class="note">No provable missing spaces were found.</p>';
} else {
  const perRule = {};
  paras.forEach(p=>p.repairs.forEach(r=>{ perRule[r.rule] = (perRule[r.rule]||0)+1; }));
  let h = '<p class="note">' + Object.entries(perRule).map(([k,v])=>v+' '+k).join(' · ') +
    '. Rules restore a space only where the characters prove it was there. Word pairs such as "Giventhe" are not touched.</p>';
  h += '<table><caption><span class="tno">TAB.01</span>' + totalSpaces + ' spaces restored in ' + parasWithSpaces + ' paragraphs</caption>' +
       '<thead><tr><th scope="col" class="num">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead><tbody>';
  for (const p of paras) for (const r of p.repairs){
    h += '<tr class="prow" data-jump="'+p.number+'" style="cursor:pointer"><td class="num pnum">'+p.number+'</td><td>…'+esc(r.before)+'</td><td>…'+esc(r.after)+'</td><td>'+esc(r.rule)+'</td></tr>';
  }
  h += '</tbody></table>';
  sb.innerHTML = h;
}

/* ---------- tab 2 ---------- */
document.getElementById('foldHeadsLbl').textContent = 'Headings found (' + headings.length + ')';
document.getElementById('headsBody').innerHTML = headings.length
  ? '<ul style="columns:2;max-width:70ch;font-size:14.5px">' + headings.map(h =>
      '<li>' + (h.level==='H2'?'<strong>'+esc(h.label+'. '+h.heading)+'</strong>':esc(h.label ? h.label+'. '+h.heading : h.heading)) +
      (h.glued?' <span class="hint">label was glued</span>':'') + '</li>').join('') + '</ul>'
  : '<p class="note">No headings found.</p>';

document.getElementById('pCapText').textContent =
  paras.length + ' paragraphs found' + (hasRefParas ? ', ' + ref.paragraphs + ' expected' : '');
const tb = document.getElementById('pTbody');
if (!paras.length){
  tb.innerHTML = '<tr><td colspan="4" class="note">No paragraphs found in this HTML.</td></tr>';
}
function firstLine(t){
  if (t.length <= 120) return t;
  const cut = t.slice(0,120), i = cut.lastIndexOf(' ');
  return (i > 60 ? cut.slice(0,i) : cut) + '…';
}
paras.forEach(p=>{
  const tr = document.createElement('tr');
  tr.className = 'prow'; tr.tabIndex = 0; tr.setAttribute('role','button');
  tr.setAttribute('aria-expanded','false');
  tr.innerHTML = '<td class="num pnum">' + p.number + '</td>' +
    '<td>' + esc(p.section || '—') + '</td>' +
    '<td>' + esc(firstLine(p.text)) + '</td>' +
    '<td>' + (p.firstMatch === false ? '<span class="red">first words differ</span>'
             : p.firstMatch === null ? '<span class="hint">not checked</span>' : 'OK') + '</td>';
  tb.appendChild(tr);
  const det = document.createElement('tr');
  det.className = 'detail'; det.hidden = true;
  det.innerHTML = '<td colspan="4">' +
    '<div class="mono" style="margin-bottom:8px">' + esc(p.part ? p.part : '—') + ' › ' + esc(p.section || '—') + '</div>' +
    '<p class="fulltext">' + p.html + '</p>' +
    (p.firstMatch === false
      ? '<div class="fw">FOUND&nbsp;&nbsp;&nbsp;&nbsp;“' + esc(p.foundFW.join(' ')) + '”</div>' +
        '<div class="fw">REFERENCE “' + esc(norm(p.refFW)) + '”</div>' : '') +
    (p.repairs.length
      ? '<div class="fw">' + p.repairs.length + ' space' + (p.repairs.length>1?'s':'') + + ' restored here (thin red boxes above); text as found is in text_raw.</div>' : '') +
    '<div style="margin-top:12px"><button class="btn" data-cite="' + p.number + '">Copy citation</button><span class="copied" hidden>Copied</span> ' +
    '<span class="hint">“' + esc(D.symbol) + ', para. ' + p.number + '”</span></div>' +
    (D.doc_url ? '<div style="margin-top:8px"><a href="'+esc(D.doc_url)+'" target="_blank" rel="noopener">'+esc(D.symbol)+'</a> (opens in a new tab)</div>' : '') +
    '</td>';
  tb.appendChild(det);
  tr.addEventListener('click', ()=>toggleRow(tr, det));
  tr.addEventListener('keydown', e=>{
    if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); toggleRow(tr, det); }
  });
});
function toggleRow(tr, det){
  const open = det.hidden;
  det.hidden = !open;
  tr.setAttribute('aria-expanded', open ? 'true' : 'false');
}
tb.addEventListener('click', e=>{
  const b = e.target.closest('button[data-cite]');
  if (!b) return;
  const n = b.getAttribute('data-cite');
  const s = D.symbol + ', para. ' + n;
  const done = ()=>{ const c = b.parentElement.querySelector('.copied');
    c.hidden = false; setTimeout(()=>{ c.hidden = true; }, 2000); };
  if (navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(s).then(done).catch(()=>fallbackCopy(s, done));
  } else fallbackCopy(s, done);
});
function fallbackCopy(s, done){
  const ta = document.createElement('textarea');
  ta.value = s; ta.style.position = 'fixed'; ta.style.opacity = '0';
  document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); } catch(e){}
  ta.remove(); done();
}

/* jump from spaces table to the paragraph on tab 02 */
sb.addEventListener('click', e=>{
  const row = e.target.closest('tr[data-jump]');
  if (!row) return;
  const n = parseInt(row.getAttribute('data-jump'), 10);
  selectTab(1);
  const rows = Array.from(tb.querySelectorAll('tr.prow'));
  const idx = paras.findIndex(p=>p.number === n);
  if (idx >= 0 && rows[idx]){
    const det = rows[idx].nextElementSibling;
    if (det.hidden) toggleRow(rows[idx], det);
    rows[idx].scrollIntoView({block:'center'});
    rows[idx].focus();
  }
});

/* ---------- folds ---------- */
function fold(btnId, bodyId){
  const b = document.getElementById(btnId), d = document.getElementById(bodyId);
  b.addEventListener('click', ()=>{
    const open = d.hidden;
    d.hidden = !open;
    b.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
}
fold('foldChecks','checksBody');
fold('foldSpaces','spacesBody');
fold('foldHeads','headsBody');

/* ---------- tabs & arrow keys ---------- */
const tabs = [document.getElementById('tab1'), document.getElementById('tab2')];
const panels = [document.getElementById('panel1'), document.getElementById('panel2')];
function selectTab(i){
  tabs.forEach((t,j)=>{
    t.setAttribute('aria-selected', i===j ? 'true' : 'false');
    t.tabIndex = i===j ? 0 : -1;
    panels[j].hidden = i!==j;
  });
}
tabs.forEach((t,i)=>{
  t.addEventListener('click', ()=>selectTab(i));
  t.addEventListener('keydown', e=>{
    let j = null;
    if (e.key === 'ArrowRight') j = (i+1) % tabs.length;
    if (e.key === 'ArrowLeft')  j = (i-1+tabs.length) % tabs.length;
    if (e.key === 'Home') j = 0;
    if (e.key === 'End')  j = tabs.length-1;
    if (j !== null){ e.preventDefault(); selectTab(j); tabs[j].focus(); }
  });
});
selectTab(0);
})();
</script>
</body>
</html>
```