This app splits the converter's text into numbered paragraphs under their headings, compares the result with the document's reference, and flags the paragraphs where footnote text may sit inside. It can also download the paragraphs as JSON or Markdown.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
[hidden]{display:none!important}
*{box-sizing:border-box}
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#2b6a3b;--muted:#625c50;--wash:#fbf9f4}
html,body{margin:0;background:var(--paper);color:var(--ink)}
body{font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.mono{font:600 11.5px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.serif{font-family:Georgia,"Times New Roman",serif}
.big{font-family:Georgia,"Times New Roman",serif;font-size:48px;line-height:1.05}
.small{font-size:14px;color:var(--muted)}
.how{font:11.5px/1.4 ui-monospace,Menlo,Consolas,monospace;color:var(--muted);margin-top:8px}
a{color:var(--ink)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
button{font:inherit;background:none;border:1px solid var(--rule);color:var(--ink);padding:6px 12px;cursor:pointer;margin:2px 6px 2px 0}
button:hover{border-color:var(--ink)}
button:disabled{opacity:.45;cursor:default}
.red{color:var(--red)}
.okt{color:var(--green);font-weight:600}
.bad-t{color:var(--red);font-weight:600}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle;background:var(--green)}
.dot.bad{background:var(--red)}
header.top{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;padding:20px 28px;border-bottom:1px solid var(--rule)}
header.top h1{font:400 30px/1.2 Georgia,"Times New Roman",serif;margin:6px 0}
.shell{display:grid;grid-template-columns:250px 1fr;gap:28px;padding:22px 28px}
@media(max-width:820px){.shell{grid-template-columns:1fr}.rail{border-right:0!important;border-bottom:1px solid var(--rule);padding:0 0 16px!important}}
.rail{border-right:1px solid var(--rule);padding-right:18px}
.card{border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:10px 0;margin:8px 0 16px}
.bar{height:6px;background:var(--rule);margin:8px 0}
.bar i{display:block;height:100%;background:var(--ink)}
.bar i.red{background:var(--red)}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin-bottom:18px}
.tabs button{border:0;border-bottom:3px solid transparent;padding:8px 14px;font:600 11.5px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;margin:0}
.tabs button[aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
@media(max-width:900px){.tiles{grid-template-columns:1fr 1fr}}
.tile{border-top:1px solid var(--rule);padding-top:10px}
.acc{width:100%;text-align:left;border:0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:10px 0;margin:14px 0 0;font:600 11.5px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase}
.acc::before{content:"+ "}
.acc[aria-expanded=true]::before{content:"− "}
table{width:100%;border-collapse:collapse;font-size:15px;margin-top:8px}
caption{text-align:left;font:400 18px Georgia,"Times New Roman",serif;padding:6px 0 10px;caption-side:top}
th,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font:600 11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
td.num,th.num{text-align:right}
tr.prow{cursor:pointer}
tr.prow:hover td,tr[data-flag]:hover td{background:#ebe5d6}
.pno{font-family:Georgia,serif;color:var(--red);font-size:17px;border:0;padding:0;margin:0;background:none}
.detail td{background:#ebe5d6;padding:14px 16px}
.detail p{margin:6px 0}
.run{font-size:17px;line-height:1.7}
mark.sus{background:none;outline:1px solid var(--red);padding:0 2px;color:var(--ink)}
pre.lines{white-space:pre-wrap;font:13px/1.5 ui-monospace,Menlo,Consolas,monospace;background:var(--wash);padding:10px;border:1px solid var(--rule);max-height:360px;overflow:auto}
.pagebeg{color:var(--muted);font-size:11px;display:block;margin-top:6px}
.note{background:var(--wash);border-left:3px solid var(--red);padding:8px 12px;margin:10px 0}
ol.list{padding-left:20px;margin:6px 0}
ol.list li{margin:3px 0}
footer{padding:16px 28px;border-top:1px solid var(--rule);font-size:13px;color:var(--muted)}
</style>
</head>
<body>
<header class="top">
  <div>
    <div class="mono" id="kick"></div>
    <h1 id="ttl"></h1>
    <div class="small" id="meta"></div>
  </div>
  <div style="text-align:right">
    <div><span class="dot" id="dot"></span><span id="dotText"></span></div>
    <div class="mono" id="flagTop" style="margin-top:6px"></div>
  </div>
</header>
<div class="shell">
  <aside class="rail">
    <div class="mono">DOCUMENT</div>
    <div class="card"><div class="mono" id="railSym"></div><div class="small" id="railShort"></div></div>
    <div class="big" id="railParas"></div>
    <div class="bar"><i id="railBar"></i></div>
    <div class="small" id="railParasNote"></div>
    <div class="big" id="railFlag" style="margin-top:22px"></div>
    <div class="small" id="railFlagNote"></div>
    <div class="small" id="railChecks" style="margin-top:22px"></div>
  </aside>
  <main>
    <div class="tabs" role="tablist">
      <button role="tab" id="tab1" aria-controls="p1" aria-selected="true" tabindex="0">01 RESULT</button>
      <button role="tab" id="tab2" aria-controls="p2" aria-selected="false" tabindex="-1">02 PARAGRAPHS</button>
    </div>
    <section role="tabpanel" id="p1" aria-labelledby="tab1">
      <div class="tiles" id="tiles"></div>
      <div id="fwBox"></div>
      <div style="margin-top:26px">
        <div class="mono">Take the paragraphs away</div>
        <p class="small">A dataset travels with its source, its fields and its known limitations.</p>
        <button id="dlJson">Download JSON</button>
        <button id="dlMd">Download Markdown</button>
        <div class="small" id="exportNote"></div>
      </div>
      <button class="acc" id="accChecks" aria-expanded="false" aria-controls="checksBox"></button>
      <div id="checksBox" hidden></div>
      <button class="acc" id="accFlag" aria-expanded="false" aria-controls="flagBox"></button>
      <div id="flagBox" hidden></div>
    </section>
    <section role="tabpanel" id="p2" aria-labelledby="tab2" hidden>
      <button class="acc" id="accHead" aria-expanded="false" aria-controls="headBox"></button>
      <div id="headBox" hidden></div>
      <table id="ptable">
        <caption id="ptCap"></caption>
        <thead><tr>
          <th scope="col">No.</th><th scope="col">Section</th><th scope="col">Page</th>
          <th scope="col">First line</th><th scope="col">Check</th>
        </tr></thead>
        <tbody id="ptBody"></tbody>
      </table>
    </section>
  </main>
</div>
<footer id="foot"></footer>

<script>
(function(){
'use strict';
const D = window.WORKSHOP_DATA.pdf_text || {};
const REF = D.reference || null;
const SYMBOL = D.symbol || '';
const DOC_URL = D.doc_url || '#';
const RECS = (D.records || []).slice().sort((a, b) => a.page - b.page);
const PAGES = RECS.length;
const EXP = REF && typeof REF.paragraphs === 'number' ? REF.paragraphs : null;
const FN = REF && typeof REF.footnotes === 'number' ? REF.footnotes : null;
const FW = REF && REF.first_words ? REF.first_words : null;
const $ = id => document.getElementById(id);
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function normalise(s){
  return String(s).replace(/[\u2018\u2019\u201A\u201B]/g, "'").replace(/[\u201C\u201D\u201E\u201F]/g, '"')
    .replace(/[\u2013\u2014]/g, '-').replace(/\s+/g, ' ').trim();
}
function citeOf(n){ return SYMBOL + ', para. ' + n; }

// first six words, footnote marks removed
function firstWords(text){
  const toks = text.split(/\s+/).filter(Boolean);
  const out = [];
  for (const t of toks) {
    if (/^\d+$/.test(t)) {
      const prev = out[out.length - 1];
      const dropIt = prev !== undefined && /[.,"”’]$/.test(prev) &&
        !/^\(?(?:No|art|arts|para|paras|sect|vol|chap|p|pp|ch)\.$/i.test(prev);
      if (!dropIt) out.push(t);
      continue;
    }
    const u = t.replace(/([A-Za-z.,;:”"’)\]])\d{1,3}$/, '$1');
    if (u.length) out.push(u);
  }
  return out.slice(0, 6).join(' ');
}

function analyse(){
  const pageNum = {}, hdrPages = [], footerBare = [], all = [], B = [], warnings = [];
  for (const rec of RECS) {
    const arr = String(rec.text || '').split(/\r?\n/).map(t => ({ t: t.trim(), page: rec.page, kind: null }));
    arr.forEach(l => { if (l.t === '') l.kind = 'empty'; else all.push(l); });
    // header: first non-empty line equal to the symbol
    const first = arr.find(l => l.t !== '');
    if (first && first.t === SYMBOL) { first.kind = 'header'; hdrPages.push(rec.page); }
    else warnings.push('page ' + rec.page + ': first line is not the symbol');
    // footer: from the end, job codes, date stamps and bare numbers
    let num = null;
    for (let i = arr.length - 1; i >= 0; i--) {
      const l = arr[i];
      if (l.kind === 'empty') continue;
      if (l.kind === 'header') break;
      if (l.t.startsWith('GE.') || /^\d{6}(\s+\d{6})*$/.test(l.t)) { l.kind = 'footer'; continue; }
      if (/^\d{1,3}$/.test(l.t)) {
        l.kind = 'footer';
        if (Number(l.t) === rec.page && num === null) num = rec.page;
        else footerBare.push({ page: rec.page, value: l.t });
        continue;
      }
      break;
    }
    pageNum[rec.page] = num;
    arr.forEach(l => { if (l.kind === null) B.push(l); });
  }

  const isLabel = t => /^([IVX]+|[A-Z])\.$/.test(t);
  const pm = t => /^(\d{1,3})\.$/.exec(t) || /^(\d{1,3})\. (.+)$/.exec(t);
  B.forEach(l => { if (pm(l.t)) { l.kind = 'para'; l.start = true; } });
  const firstStart = B.findIndex(l => l.start);

  // labelled headings: label line, then title lines up to the next label or paragraph
  B.forEach((l, i) => {
    if (l.kind !== null || !isLabel(l.t)) return;
    l.kind = 'heading'; l.label = l.t.slice(0, -1);
    for (let k = i + 1; k < B.length && !B[k].start && !isLabel(B[k].t); k++) {
      if (B[k].kind === null) B[k].kind = 'heading';
    }
  });

  // unlabelled headings: short capitalised lines right above a paragraph start
  const cap = s => /^[A-Z]/.test(s), cont = s => /^[a-z(]/.test(s);
  const okLen = s => s.length <= 90 && !/[.;:,\d]$/.test(s);
  B.forEach((l, p) => {
    if (!l.start) return;
    const near = B[p - 1], prev = B[p - 2];
    if (!near || near.kind !== null || !okLen(near.t) || !(cap(near.t) || cont(near.t))) return;
    if (prev && prev.kind === null && !prev.start && cap(prev.t) && okLen(prev.t)) {
      prev.kind = 'heading'; near.kind = 'heading'; prev.label = null; near.label = null;
    } else if (cap(near.t)) {
      near.kind = 'heading'; near.label = null;
    }
  });

  // everything else before the first paragraph is cover; after it, paragraph text
  B.forEach((l, i) => { if (l.kind === null) l.kind = (firstStart < 0 || i < firstStart) ? 'cover' : 'para'; });

  // ordered events: headings and paragraphs
  const headings = [], events = [], paras = [];
  let block = null, section = '', part = '', cur = null;
  const flush = () => {
    if (!block) return;
    const title = block.parts.join(' ').replace(/\s+/g, ' ').trim();
    const h = { label: block.label, title, page: block.page, text: block.label != null ? block.label + '. ' + title : title };
    headings.push(h); events.push({ type: 'h', h });
    if (block.label != null && /^[IVX]+$/.test(block.label)) part = h.text;
    section = h.text; block = null;
  };
  for (const l of B) {
    if (l.kind === 'heading') {
      if (l.label != null || !block) {
        flush();
        block = { label: l.label != null ? l.label : null, parts: l.label != null ? [] : [l.t], page: l.page };
      } else block.parts.push(l.t);
      continue;
    }
    flush();
    if (l.start) {
      const m = pm(l.t);
      l.content = m[2] || '';
      cur = { num: Number(m[1]), section, part, lines: [l], startPage: l.page };
      paras.push(cur); events.push({ type: 'p', p: cur });
    } else if (l.kind === 'para' && cur) {
      l.content = l.t; cur.lines.push(l);
    }
  }
  flush();

  // suspect lines, paragraph text, first words
  const susWhy = t => /^\d{1,3}$/.test(t) ? 'bare number'
    : /^\d{1,3} (?=["“”‘'A-Z])/.test(t) ? 'starts with a number and a space'
    : /^\* /.test(t) ? 'starts with an asterisk and a space' : null;
  for (const p of paras) {
    let on = null;
    p.reasons = [];
    p.lines.forEach((l, i) => {
      if (l.page !== on) on = null;
      if (i === 0) { l.sus = false; return; }
      const why = susWhy(l.t);
      if (why) { on = l.page; l.sus = true; l.why = why; p.reasons.push(why); }
      else if (on !== null) { l.sus = true; l.why = null; }
      else { l.sus = false; l.why = null; }
    });
    p.suspect = p.lines.filter(l => l.sus);
    p.text = p.lines.map(l => l.content).join(' ').replace(/\s+/g, ' ').trim();
    p.wordCount = p.text ? p.text.split(' ').length : 0;
    if (p.wordCount > 300) p.reasons.push('paragraph over 300 words');
    p.reasons = [...new Set(p.reasons)];
    p.flagged = p.suspect.length > 0 || p.wordCount > 300;
    p.pagesEnd = p.lines[p.lines.length - 1].page;
    p.fwFound = firstWords(p.text);
    const ref = FW ? FW[String(p.num)] : undefined;
    p.fwRef = ref === undefined ? null : ref;
    p.fwMatch = FW ? (ref !== undefined && normalise(p.fwFound) === normalise(ref)) : null;
  }

  const kinds = { header: 0, footer: 0, cover: 0, heading: 0, para: 0 };
  const unclassified = [];
  all.forEach(l => { if (Object.prototype.hasOwnProperty.call(kinds, l.kind)) kinds[l.kind]++; else unclassified.push(l); });

  return {
    paras, events, headings, kinds, unclassified, footerBare, pageNum, hdrPages, warnings,
    total: all.length,
    hyphen: B.filter(l => /-$/.test(l.t)).length,
    n: paras.length,
    flagged: paras.filter(p => p.flagged),
    susParas: paras.filter(p => p.suspect.length),
    susLines: paras.reduce((a, p) => a + p.suspect.length, 0),
    labelled: headings.filter(h => h.label != null),
    unlabelled: headings.filter(h => h.label == null)
  };
}

const S = analyse();
let CHECKS = [];

function buildRecords(){
  return S.paras.map(p => {
    const k = p.suspect.length;
    return {
      symbol: SYMBOL, paragraph: p.num, section: p.section || '', part: p.part || '',
      page_start: p.lines[0].page, page_end: p.pagesEnd, text: p.text, flagged: p.flagged,
      first_words_match: p.fwMatch, citation: citeOf(p.num), doc_url: DOC_URL,
      limitations: p.flagged
        ? (k ? 'footnotes not separated; ' + k + ' may sit inside this paragraph' : 'footnotes not separated; paragraph over 300 words')
        : 'footnotes not separated',
      text_lines: p.lines.map(l => l.t).join(' | ')
    };
  });
}
function buildMd(){
  const today = new Date().toISOString().slice(0, 10);
  const out = ['---',
    'title: "' + String(D.title || '').replace(/"/g, '\\"') + '"',
    'symbol: "' + SYMBOL + '"',
    'adopted: "' + (REF && REF.adopted ? REF.adopted : 'no reference in this file') + '"',
    'source_url: "' + DOC_URL + '"',
    'extracted: "' + today + '"',
    'paragraphs_found: ' + S.n,
    'paragraphs_expected: ' + (EXP == null ? '"no reference in this file"' : EXP),
    'paragraphs_flagged: ' + S.flagged.length,
    'footnotes: "not separated; the document has ' + (FN == null ? 'no reference' : FN) + '"',
    '---', ''];
  for (const ev of S.events) {
    if (ev.type === 'h') {
      const lvl = ev.h.label != null && /^[IVX]+$/.test(ev.h.label) ? '##' : '###';
      out.push(lvl + ' ' + ev.h.text, '');
    } else {
      const p = ev.p;
      out.push('**' + p.num + '.** ' + p.text + (p.flagged ? ' (flagged: may contain footnote text)' : ''), '');
    }
  }
  return out.join('\n');
}
function download(name, text, type){
  const url = URL.createObjectURL(new Blob([text], { type: type + ';charset=utf-8' }));
  const a = document.createElement('a');
  a.href = url; a.download = name; document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 1000);
}
const fileBase = () => SYMBOL.replace(/\//g, '-');

function buildChecks(){
  const C = [];
  const add = (name, compared, status, rows, detail) => C.push({ name, compared, status, rows: rows || [], detail: detail || '' });
  const n = S.n;

  add('Paragraph count', 'found ' + n + '; reference.paragraphs ' + (EXP == null ? 'missing' : EXP),
    EXP == null ? 'na' : (n === EXP ? 'pass' : 'fail'));

  const nums = S.paras.map(p => p.num);
  const numProblems = [];
  nums.forEach((x, i) => { if (x !== i + 1) numProblems.push({ num: x, page: S.paras[i].startPage, expected: i + 1 }); });
  const missing = [];
  const mx = nums.length ? Math.max(...nums) : 0;
  for (let k = 1; k <= mx; k++) if (!nums.includes(k)) missing.push(k);
  add('Numbering', 'numbers 1 to ' + n + ' in order', numProblems.length || missing.length ? 'fail' : 'pass',
    numProblems.map(x => x.num).concat(missing).slice(0, 1).concat([]),
    numProblems.slice(0, 20).map(x => 'para. ' + x.num + ' on page ' + x.page + ' (expected ' + x.expected + ')').concat(
      missing.length ? ['missing: ' + missing.join(', ')] : []).join('; '));

  if (!FW) add('First words', 'not in this file', 'na');
  else {
    const mm = S.paras.filter(p => p.fwMatch === false);
    add('First words', 'mismatches: ' + mm.length + ' of ' + n + ' compared', mm.length ? 'fail' : 'pass',
      mm.map(p => p.num), mm.slice(0, 20).map(p => 'para. ' + p.num).join(', '));
  }

  const pagesFlagged = new Set(S.flagged.map(p => (p.suspect[0] || p.lines[0]).page)).size;
  add('Paragraphs flagged', S.flagged.length + ' paragraphs flagged on ' + pagesFlagged + ' pages, to check against the PDF', 'info', [], '');
  const pagesSus = new Set(S.paras.flatMap(p => p.suspect.map(l => l.page))).size;
  add('Suspect lines', S.susLines + ' suspect lines on ' + pagesSus + ' pages, in ' + S.susParas.length + ' paragraphs; none is removed', 'info');

  add('Headers', 'pages whose first line was the symbol: ' + S.hdrPages.length + ' of ' + PAGES + ' (expected all)',
    S.hdrPages.length === PAGES ? 'pass' : 'fail', [], S.warnings.join('; '));

  const expNum = RECS.filter(r => r.page > 1).length;
  const gotNum = RECS.filter(r => r.page > 1 && S.pageNum[r.page] !== null).length;
  add('Page numbers in footers', 'pages with a page number: ' + gotNum + ' (expected ' + expNum + ', all but the first)',
    gotNum === expNum ? 'pass' : 'fail');

  add('Bare numbers removed from footers', S.footerBare.length + ' removed (footnote numbers the converter displaced)', 'info', [],
    S.footerBare.map(b => 'page ' + b.page + ': ' + b.value).join('; '));

  add('Headings', S.labelled.length + ' labelled, ' + S.unlabelled.length + ' unlabelled', 'info', [],
    S.unlabelled.map(h => 'page ' + h.page + ': ' + h.text).join('; '));

  const sum = S.kinds.header + S.kinds.footer + S.kinds.cover + S.kinds.heading + S.kinds.para;
  add('Nothing lost', 'classified ' + sum + ' of ' + S.total + ' non-empty lines; ' + S.unclassified.length + ' unclassified',
    sum === S.total && S.unclassified.length === 0 ? 'pass' : 'fail', [],
    S.unclassified.map(l => 'page ' + l.page + ': ' + l.t).join('; '));

  let rt = false, rtCount = 0;
  try { rtCount = JSON.parse(JSON.stringify(buildRecords())).length; rt = rtCount === S.n; } catch (e) { rt = false; }
  add('Export round trip', 'JSON records ' + rtCount + '; table rows ' + S.n, rt ? 'pass' : 'fail');

  add('Lines ending in a hyphen', S.hyphen + ' lines (none joined; counted only)', 'info');
  return C;
}

// ---------- rendering ----------
function renderHeader(){
  $('kick').textContent = 'UN DOCUMENT · PDF TEXT';
  $('ttl').textContent = D.title || '';
  $('meta').innerHTML = '<a href="' + esc(DOC_URL) + '" target="_blank" rel="noopener">' + esc(SYMBOL) + '</a> · adopted ' +
    esc(REF && REF.adopted ? REF.adopted : 'no reference in this file') + ' · ' + PAGES + ' pages · ' + esc(D.source || '');
  const pass = CHECKS.filter(c => c.status === 'pass').length;
  const fail = CHECKS.filter(c => c.status === 'fail').length;
  const m = pass + fail;
  $('dot').className = 'dot' + (fail ? ' bad' : '');
  $('dotText').textContent = fail ? fail + ' checks failed' : pass + ' of ' + m + ' checks pass';
  $('flagTop').textContent = S.flagged.length + ' paragraphs flagged';
  $('foot').textContent = 'Source: ' + (D.source || '') + ' · Done by this page\'s code; no model was called and nothing left the browser.';
}
function renderRail(){
  const n = S.n, pass = CHECKS.filter(c => c.status === 'pass').length, fail = CHECKS.filter(c => c.status === 'fail').length;
  $('railSym').textContent = SYMBOL;
  $('railShort').textContent = D.title || '';
  $('railParas').innerHTML = '<span class="' + (EXP != null && n !== EXP ? 'red' : '') + '">' + n + '</span>';
  $('railParasNote').textContent = 'paragraphs' + (EXP == null ? ' · no reference in this file' : ' of ' + EXP + ' in reference.paragraphs');
  const bar = $('railBar');
  bar.style.width = '100%';
  bar.innerHTML = '';
  bar.className = '';
  const pct = EXP ? Math.min(100, n / EXP * 100) : 0;
  const bi = document.createElement('i');
  bi.style.width = pct + '%';
  if (EXP != null && n !== EXP) bi.className = 'red';
  $('railBar').parentNode.innerHTML = '';
  $('railBar').parentNode.appendChild(Object.assign(document.createElement('div'), { className: 'bar' })).appendChild(bi);
  $('railFlag').innerHTML = '<span class="' + (S.flagged.length ? 'red' : '') + '">' + S.flagged.length + '</span>';
  $('railFlagNote').textContent = 'paragraphs flagged: footnote text may sit inside; check them against the PDF';
  $('railChecks').innerHTML = fail ? '<span class="bad-t">' + fail + ' checks failed</span>' : '<span class="okt">' + pass + ' of ' + (pass + fail) + ' checks pass</span>';
}
function renderTiles(){
  const n = S.n;
  const tile = (label, big, sub, how) => '<div class="tile"><div class="mono">' + label + '</div><div class="big">' + big +
    '</div><div class="small">' + sub + '</div><div class="how">' + how + '</div></div>';
  const diff = EXP == null ? '' : n - EXP;
  const t1 = tile('Paragraphs found', n,
    EXP == null ? 'no reference in this file' : '<span class="' + (diff === 0 ? 'okt' : 'bad-t') + '">the document has ' + EXP +
      (diff === 0 ? '' : ' (difference ' + (diff > 0 ? '+' : '') + diff + ')') + '</span>',
    'How this is computed: numbered lines found in the converter text after headers and footers are removed.');
  const matched = S.paras.filter(p => p.fwMatch === true).length;
  const t2 = tile('First words match', FW ? matched : '—',
    FW ? 'of ' + (EXP != null ? EXP : n) + ' paragraphs' : 'no reference in this file',
    'How this is computed: first six words of each paragraph, footnote marks removed, compared with reference.first_words.');
  const nf = S.flagged.length;
  const t3 = tile('Paragraphs flagged', '<span class="' + (nf ? 'red' : '') + '">' + nf + '</span>',
    'of ' + n + ' paragraphs found, on ' + new Set(S.flagged.map(p => (p.suspect[0] || p.lines[0]).page)).size + ' pages' +
    (nf ? '<br><span class="red">footnote text may sit inside these paragraphs: check them against the PDF</span>' : ''),
    'How this is computed: a suspect line (bare number, number and space, asterisk) or over 300 words.');
  const t4 = tile('Footnotes', '<span style="font-size:26px">not separated</span>',
    FN == null ? 'no reference in this file' : 'the document has ' + FN + '; this version leaves them in place and flags them',
    'How this is computed: the reference footnote count; footnotes are not split from paragraphs.');
  $('tiles').innerHTML = t1 + t2 + t3 + t4;

  const mm = S.paras.filter(p => p.fwMatch === false);
  let fw = '';
  if (mm.length) {
    fw = '<div class="note"><div class="mono red">First words differ: ' + mm.length + '</div><ul class="list">' +
      mm.slice(0, 10).map(p => '<li>para. ' + p.num + ': found “' + esc(p.fwFound) + '” / reference “' + esc(p.fwRef) + '”</li>').join('') +
      (mm.length > 10 ? '<li>and ' + (mm.length - 10) + ' more</li>' : '') + '</ul></div>';
  }
  if (!n) fw = '<div class="note red">No paragraph was found in this file. The exports are disabled.</div>';
  $('fwBox').innerHTML = fw;
  const ok = n > 0;
  $('dlJson').disabled = !ok; $('dlMd').disabled = !ok;
  $('exportNote').textContent = ok ? n + ' records' : 'no paragraphs: nothing to export';
}
function renderChecksBox(){
  const rowTxt = c => c.status === 'pass' ? '<span class="okt">pass</span>'
    : c.status === 'fail' ? '<span class="bad-t">check failed</span>' +
      (c.rows.length ? ' <button data-go="' + c.rows[0] + '">show para. ' + c.rows[0] + '</button>' : '')
    : c.status === 'info' ? '<span class="small">to check</span>' : '<span class="small">not run</span>';
  $('checksBox').innerHTML = '<table><caption>' + CHECKS.length + ' checks, each with its values</caption><thead><tr>' +
    '<th scope="col">Check</th><th scope="col">Compared</th><th scope="col">Result</th></tr></thead><tbody>' +
    CHECKS.map(c => '<tr><td>' + esc(c.name) + '</td><td>' + esc(c.compared) +
      (c.detail ? '<div class="small' + (c.status === 'fail' && c.name === 'Nothing lost' ? ' red' : '') + '">' + esc(c.detail) + '</div>' : '') +
      '</td><td>' + rowTxt(c) + '</td></tr>').join('') + '</tbody></table>';
  $('accChecks').textContent = 'Every check (' + CHECKS.length + ')';
}
function renderFlagBox(){
  $('accFlag').textContent = 'Flagged paragraphs (' + S.flagged.length + ')';
  let html = '<div class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</div>';
  html += '<table><caption>' + S.flagged.length + ' paragraphs flagged</caption><thead><tr>' +
    '<th scope="col" class="num">Paragraph</th><th scope="col" class="num">Page</th><th scope="col">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>' +
    S.flagged.map(p => {
      const first = (p.suspect[0] || {}).t || '';
      const sus = p.suspect.length ? p.suspect.length + ': “' + esc(first.slice(0, 60)) + '”' : 'none';
      return '<tr tabindex="0" data-flag="' + p.num + '"><td class="num red">' + p.num + '</td><td class="num">' + (p.suspect[0] || p.lines[0]).page +
        '</td><td>' + sus + '</td><td>' + esc(p.reasons.join('; ')) + '</td></tr>';
    }).join('') + '</tbody></table>';
  $('flagBox').innerHTML = html;
}
function renderHeadBox(){
  $('accHead').textContent = 'Headings found (' + S.headings.length + ')';
  $('headBox').innerHTML = '<ol class="list">' + S.headings.map(h =>
    '<li><span class="mono">' + (h.label != null ? 'labelled' : 'unlabelled') + '</span> page ' + h.page + ' · ' + esc(h.text) + '</li>').join('') + '</ol>';
}
function detailHTML(p){
  const path = (p.part && p.part !== p.section ? p.part + ' › ' : '') + (p.section || '(no heading above this paragraph)');
  const run = p.lines.filter(l => l.content !== '').map(l => l.sus ? '<mark class="sus">' + esc(l.content) + '</mark>' : esc(l.content)).join(' ');
  let lines = '', last = null;
  p.lines.forEach(l => {
    if (l.page !== last) { lines += '<span class="pagebeg">— PDF page ' + l.page + ' begins —</span>'; last = l.page; }
    lines += (l.sus ? '<mark class="sus">' + esc(l.t) + '</mark>' : esc(l.t)) + '\n';
  });
  return '<p class="mono">Paragraph ' + p.num + ' · ' + esc(path) + '</p>' +
    '<p class="run">' + run + '</p>' +
    '<p class="small">' + p.wordCount + ' words' + (p.suspect.length ? ' · ' + p.suspect.length + ' suspect line(s) outlined in red' : '') + '</p>' +
    '<p class="small">first six words: found “' + esc(p.fwFound) + '”' + (FW ? ' · reference “' + esc(p.fwRef == null ? '—' : p.fwRef) + '”' : ' · no reference in this file') + '</p>' +
    '<p><button data-tog="' + p.num + '" aria-expanded="false">Show the PDF\'s lines</button></p>' +
    '<div id="pdf' + p.num + '" hidden><pre class="lines">' + lines + '</pre></div>' +
    '<p><button data-cite="' + p.num + '">Copy citation</button> <span class="small">' + esc(citeOf(p.num)) + '</span></p>';
}
function renderParas(){
  const n = S.n;
  $('ptCap').textContent = n + ' paragraphs found, ' + (EXP == null ? 'no reference expected' : EXP + ' expected');
  $('ptBody').innerHTML = S.paras.map(p => {
    const checks = [];
    if (p.fwMatch === false) checks.push('<span class="bad-t">first words differ</span>');
    if (p.flagged) checks.push('<span class="bad-t">may contain footnote text</span>');
    if (!checks.length) checks.push('<span class="okt">OK</span>');
    let first = p.lines.map(l => l.content).join(' ').replace(/\s+/g, ' ').trim();
    if (first.length > 120) { first = first.slice(0, 120); first = first.replace(/\s+\S*$/, '') + '…'; }
    const pg = p.lines[0].page === p.pagesEnd ? String(p.lines[0].page) : p.lines[0].page + '–' + p.pagesEnd;
    return '<tr class="prow" tabindex="0" data-n="' + p.num + '"><td><button class="pno" aria-expanded="false" aria-controls="d' + p.num + '">' + p.num + '.</button></td>' +
      '<td>' + esc(p.section || '—') + '</td><td>' + pg + '</td><td>' + esc(first) + '</td><td>' + checks.join(' · ') + '</td></tr>' +
      '<tr class="detail" id="d' + p.num + '" hidden><td colspan="5">' + detailHTML(p) + '</td></tr>';
  }).join('');
}

// ---------- behaviour ----------
const tabs = [$('tab1'), $('tab2')], panels = [$('p1'), $('p2')];
function selectTab(i, focus){
  tabs.forEach((t, k) => { t.setAttribute('aria-selected', String(k === i)); t.tabIndex = k === i ? 0 : -1; });
  panels.forEach((p, k) => { p.hidden = k !== i; });
  if (focus) tabs[i].focus();
}
tabs.forEach((t, i) => {
  t.addEventListener('click', () => selectTab(i));
  t.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); selectTab((i + 1) % 2, true); }
  });
});
function acc(btn, box){
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') !== 'true';
    btn.setAttribute('aria-expanded', String(open)); box.hidden = !open;
  });
}
function togglePara(n, force){
  const row = document.querySelector('tr.prow[data-n="' + n + '"]');
  const det = $('d' + n);
  if (!row || !det) return;
  const open = force === undefined ? det.hidden : force;
  det.hidden = !open;
  row.querySelector('button').setAttribute('aria-expanded', String(open));
}
function openPara(n){
  selectTab(1, false);
  togglePara(n, true);
  const row = document.querySelector('tr.prow[data-n="' + n + '"]');
  if (row) { row.scrollIntoView({ block: 'center' }); row.querySelector('button').focus(); }
}
function copyCite(n, btn){
  const text = citeOf(n);
  const restore = () => setTimeout(() => { btn.textContent = 'Copy citation'; }, 2000);
  const fallback = () => { btn.textContent = text; restore(); };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => { btn.textContent = 'Copied'; restore(); }, fallback);
  } else fallback();
}
document.addEvent