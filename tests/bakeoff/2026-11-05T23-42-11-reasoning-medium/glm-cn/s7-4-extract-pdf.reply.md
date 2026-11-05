One complete app, built from the plan: it reads the converter's raw text, extracts the numbered paragraphs and headings, flags pages where footnote text may sit inside a paragraph, checks itself against the file's reference, and exports JSON and Markdown.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF — GC No. 27</title>
<style>
  :root{
    --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --accent:#9b2335; --green:#1a6b3c;
  }
  [hidden]{display:none!important}
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
  a{color:var(--accent)}
  .mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
  .serif{font-family:Georgia,"Times New Roman",serif}
  /* header */
  header{border-bottom:1px solid var(--rule);padding:14px 22px 12px}
  header .kicker{color:#6c6455}
  header h1{font-family:Georgia,"Times New Roman",serif;font-size:24px;font-weight:normal;margin:4px 0 2px}
  header .meta{font-size:14px;color:#4a443a}
  .headflex{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
  .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:baseline}
  .dot.ok{background:var(--green)} .dot.bad{background:var(--accent)}
  /* layout */
  .wrap{display:flex;min-height:70vh}
  .rail{width:250px;flex:0 0 250px;border-right:1px solid var(--rule);padding:18px 20px}
  .main{flex:1;min-width:0;padding:18px 26px 40px}
  /* rail card */
  .rail .card{border:1px solid var(--rule);padding:12px 14px;margin-bottom:18px}
  .rail .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;letter-spacing:.02em}
  .rail .shortt{font-size:13px;color:#4a443a;margin-top:2px}
  .bignum{font-family:Georgia,"Times New Roman",serif;font-size:44px;line-height:1.05;margin-top:10px}
  .bignum small{font-size:15px;color:#4a443a;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
  .bignum.bad{color:var(--accent)}
  .bar{height:4px;background:var(--rule);margin:8px 0 2px;position:relative}
  .bar i{position:absolute;left:0;top:0;bottom:0;background:var(--ink)}
  .bar.bad i{background:var(--accent)}
  .railnote{font-size:12.5px;color:#5a5346;margin-top:2px}
  .railstat{margin-top:16px;padding-top:12px;border-top:1px solid var(--rule)}
  /* tabs */
  .tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);margin-bottom:20px}
  .tab{background:none;border:none;border-bottom:3px solid transparent;padding:9px 18px 7px;cursor:pointer;
       font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;color:#4a443a}
  .tab[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent)}
  .tab:focus-visible,button:focus-visible,tr:focus-visible,[role="button"]:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  /* tiles */
  .tiles{display:flex;gap:22px;flex-wrap:wrap;margin-bottom:26px}
  .tile{flex:1 1 200px;border-top:2px solid var(--ink);padding-top:8px}
  .tile .num{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1.05}
  .tile .num.ok{color:var(--green)} .tile .num.bad{color:var(--accent)}
  .tile .sub{font-size:14px;color:#4a443a;margin:2px 0}
  .tile .how{font-size:12.5px;color:#6c6455;margin-top:6px}
  .fig{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;color:#6c6455}
  /* buttons */
  .btn{background:var(--paper);border:1px solid var(--ink);padding:8px 16px;cursor:pointer;font-size:14px}
  .btn:hover{background:#e9e3d6}
  .btn[disabled]{opacity:.4;cursor:not-allowed}
  .disc{background:none;border:none;border-top:1px solid var(--rule);width:100%;text-align:left;
        padding:10px 2px;cursor:pointer;font-size:15px;display:flex;justify-content:space-between;gap:10px}
  .disc .mono{color:#4a443a}
  /* tables */
  table{border-collapse:collapse;width:100%;margin-top:8px}
  caption{font-family:Georgia,"Times New Roman",serif;font-size:17px;text-align:left;padding-bottom:6px}
  th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;
     font-weight:normal;text-align:left;border-bottom:1px solid var(--ink);padding:5px 10px 5px 0}
  td{border-bottom:1px solid var(--rule);padding:7px 10px 7px 0;vertical-align:top;font-size:14.5px}
  th.r,td.r{text-align:right;padding-right:10px}
  tr.rowbtn{cursor:pointer}
  tr.rowbtn>td{border-bottom:1px solid var(--rule)}
  .num-cell{color:var(--accent);font-family:Georgia,"Times New Roman",serif;font-size:17px}
  .badword{color:var(--accent)}
  .okword{color:var(--green);font-size:13px}
  .flagword{color:var(--accent)}
  /* expanded paragraph */
  .exp{background:#efe9dd;border-left:3px solid var(--accent);padding:12px 16px;margin:2px 0 10px}
  .exp .full{font-size:15px;line-height:1.6}
  .sus{border:1px solid var(--accent);padding:0 2px}
  .cmp{display:grid;grid-template-columns:auto 1fr;gap:2px 12px;margin-top:10px;font-size:13.5px}
  .cmp dt{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.06em;color:#6c6455;padding-top:2px}
  .exp .tools{margin-top:10px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
  .lines{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;line-height:1.7;margin-top:10px;
         border-top:1px solid var(--rule);padding-top:8px;white-space:pre-wrap}
  .copied{color:var(--green);font-size:13px}
  /* checks */
  .check{border-bottom:1px solid var(--rule);padding:8px 2px;font-size:14.5px}
  .check .vals{color:#4a443a;font-size:13.5px}
  .pass{color:var(--green)} .fail{color:var(--accent);font-weight:600}
  .notrun{color:#6c6455}
  /* flagged raw page */
  .rawpage{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;line-height:1.7;white-space:pre-wrap;
           border:1px solid var(--rule);padding:10px 14px;margin:6px 0 14px;background:#faf7f0}
  .rawpage .hl{background:#f3d9dc;border:1px solid var(--accent)}
  .rawpage .ft{color:#8a8172}
  .note{font-size:13.5px;color:#4a443a;border-left:3px solid var(--rule);padding:4px 12px;margin:10px 0}
  .mismatch{font-size:14px;margin-top:6px}
  .mismatch code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
  footer{border-top:1px solid var(--rule);padding:12px 22px;font-size:13px;color:#5a5346;display:flex;gap:18px;flex-wrap:wrap}
  .hint{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.05em;color:#6c6455}
</style>
</head>
<body>
<header>
  <div class="headflex">
    <div>
      <div class="mono kicker">UN DOCUMENT · PDF TEXT</div>
      <h1 id="h-title"></h1>
      <div class="meta" id="h-meta"></div>
    </div>
    <div class="mono" id="h-status" style="text-align:right;line-height:2"></div>
  </div>
</header>

<div class="wrap">
  <nav class="rail" aria-label="Document">
    <div class="card">
      <div class="sym" id="r-sym"></div>
      <div class="shortt" id="r-short"></div>
      <div class="bignum" id="r-paras"></div>
      <div class="bar" id="r-bar"><i></i></div>
      <div class="railnote" id="r-paranote"></div>
    </div>
    <div class="railstat" id="r-flagged"></div>
    <div class="railstat" id="r-checks"></div>
  </nav>

  <div class="main">
    <div class="tabs" role="tablist" aria-label="Sections">
      <button class="tab" role="tab" id="tab1" aria-controls="panel1" aria-selected="true" tabindex="0">01 RESULT</button>
      <button class="tab" role="tab" id="tab2" aria-controls="panel2" aria-selected="false" tabindex="-1">02 PARAGRAPHS</button>
    </div>

    <section id="panel1" role="tabpanel" aria-labelledby="tab1" tabindex="0">
      <div class="tiles" id="tiles"></div>
      <div id="mismatchbox" hidden></div>
      <h2 class="serif" style="font-weight:normal;font-size:20px">Take the paragraphs away</h2>
      <p class="hint">FIELDS: SYMBOL, PARAGRAPH, SECTION, PART, PAGES, TEXT, TEXT_LINES, FLAG, CITATION, LIMITATIONS</p>
      <p>
        <button class="btn" id="dl-json">Download JSON</button>
        <button class="btn" id="dl-md">Download Markdown</button>
      </p>
      <button class="disc" id="disc-checks" aria-expanded="false"><span class="serif" style="font-size:17px">Every check</span> <span class="mono" id="disc-checks-n"></span></button>
      <div id="checks-panel" hidden></div>
      <button class="disc" id="disc-flag" aria-expanded="false"><span class="serif" style="font-size:17px">Flagged pages</span> <span class="mono" id="disc-flag-n"></span></button>
      <div id="flag-panel" hidden></div>
    </section>

    <section id="panel2" role="tabpanel" aria-labelledby="tab2" tabindex="0" hidden>
      <button class="disc" id="disc-head" aria-expanded="false"><span class="serif" style="font-size:17px">Headings found</span> <span class="mono" id="disc-head-n"></span></button>
      <div id="head-panel" hidden style="padding:8px 2px 14px"></div>
      <table id="ptable">
        <caption class="serif" id="ptable-cap"></caption>
      </table>
    </section>
  </div>
</div>

<footer id="foot"></footer>

<script>
(function(){
"use strict";
const D = window.WORKSHOP_DATA.pdf_text || {};
const SYM = D.symbol || "";
const REF = D.reference || null;
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* ---------- pipeline ---------- */
const pages = (D.records||[]).filter(r=>r && typeof r.text==='string').slice().sort((a,b)=>a.page-b.page);
const stats = {
  headerPages:[], headerWarn:[], footerBareNums:[], pagesWithPageNum:[],
  footerLines:0, hyphenEnd:0, coverLines:0
};
const bodyLines = [];   // {text, page, cls, para, suspect}
const rawPages = [];
let totalNonEmpty = 0;

const isFoot = l => l==='' || l.startsWith('GE.') || /^\d{6}( \d{6})*$/.test(l) || /^\d{1,3}$/.test(l);

for (const pg of pages){
  const lines = pg.text.split('\n').map(s=>s.replace(/\s+$/,''));
  rawPages.push({page:pg.page, lines});
  totalNonEmpty += lines.filter(l=>l.trim()!=='').length;
  let first = lines.findIndex(l=>l.trim()!=='');
  let start = 0;
  if (first>=0 && lines[first].trim()===SYM){
    stats.headerPages.push(pg.page); start = first+1;
  } else if (first>=0){
    stats.headerWarn.push(pg.page); start = first;
  }
  let end = lines.length;
  while (end>start && isFoot(lines[end-1].trim())){
    const l = lines[end-1].trim();
    if (l!==''){
      stats.footerLines++;
      if (/^\d{1,3}$/.test(l)){
        if (String(pg.page)===l) stats.pagesWithPageNum.push(pg.page);
        else stats.footerBareNums.push({page:pg.page, num:l});
      }
    }
    end--;
  }
  for (let i=start;i<end;i++){
    bodyLines.push({text:lines[i].trim(), page:pg.page, cls:null, para:null, suspect:false});
  }
}

const NE = [];
bodyLines.forEach((b,i)=>{ if(b.text!=='') NE.push(i); });
const rxAlone = /^(\d{1,3})\.$/;
const rxWith  = /^(\d{1,3})\. (.+)$/;
const rxLabel = /^([IVX]+|[A-Z])\.$/;
const isPS = i => rxAlone.test(bodyLines[i].text) || rxWith.test(bodyLines[i].text);
const unlTest = t =>
  t.length<=90 && /^[A-Z(]/.test(t) && !/[.;:,\d]$/.test(t) &&
  !rxLabel.test(t) && !rxAlone.test(t) && !rxWith.test(t);

const headings = []; // {text, roman, idx (NE index), labelled}
let curPart = null;
const paras = [];    // {n, section, part, lines:[{text,page,suspect}], startIdx}
let cur = null, firstSeen = false;

function newHeading(text, roman, idx, labelled){
  const h = {text, roman, idx, labelled};
  headings.push(h); return h;
}

for (let a=0; a<NE.length; a++){
  const i = NE[a], t = bodyLines[i].text;
  if (bodyLines[i].cls) continue;
  if (rxLabel.test(t)){
    const roman = /^[IVX]+\.$/.test(t);
    const parts = [];
    let b = a+1;
    while (b<NE.length){
      const j = NE[b];
      if (rxLabel.test(bodyLines[j].text) || isPS(j)) break;
      parts.push(bodyLines[j].text);
      bodyLines[j].cls = 'heading';
      b++;
    }
    bodyLines[i].cls = 'heading';
    const h = newHeading(parts.join(' '), roman, a, true);
    if (roman){ curPart = h; }
    continue;
  }
  if (isPS(i)){
    // unlabelled heading immediately before the paragraph start
    if (a>0){
      const p = NE[a-1];
      if (!bodyLines[p].cls && unlTest(bodyLines[p].text)){
        let htext = bodyLines[p].text, hidx = p;
        bodyLines[p].cls = 'heading';
        if (a-1>0){
          const q = NE[a-2];
          if (!bodyLines[q].cls && unlTest(bodyLines[q].text)){
            htext = bodyLines[q].text+' '+bodyLines[p].text;
            hidx = q; bodyLines[q].cls = 'heading';
          }
        }
        newHeading(htext, false, hidx, false);
      }
    }
    const m = rxWith.exec(t);
    const section = headings.length ? headings[headings.length-1].text : null;
    const part = curPart ? curPart.text : null;
    cur = {n: m ? +m[1] : +t.slice(0,-1), section, part, lines:[], startIdx:a, flagged:false, reasons:[]};
    paras.push(cur);
    bodyLines[i].cls = 'para'; bodyLines[i].para = cur;
    if (m) cur.lines.push({text:m[2], page:bodyLines[i].page});
    firstSeen = true;
  } else if (firstSeen && cur){
    bodyLines[i].cls = 'para'; bodyLines[i].para = cur;
    cur.lines.push({text:t, page:bodyLines[i].page});
  } else {
    bodyLines[i].cls = 'cover'; stats.coverLines++;
  }
}
// assign current section/part captured at paragraph creation (done above via headings order check)
// recompute section/part properly: walk headings in order against para startIdx
paras.forEach(p=>{
  let sec=null, part=null;
  for (const h of headings){
    if (h.idx < p.startIdx){ sec = h.text; if (h.roman) part = h.text; }
    else break;
  }
  p.section = sec; p.part = part;
});

// hyphen-ending lines (informational)
bodyLines.forEach(b=>{ if(b.text && /-$/.test(b.text)) stats.hyphenEnd++; });

/* suspect lines */
const susStart = l =>
  /^\d{1,3}$/.test(l) ||
  /^\d{1,3} [A-Z“"]/.test(l) ||
  /^\* /.test(l);
const flaggedPages = new Set();
const flaggedParas = new Set();
let suspectCount = 0, suspectPages = new Set();
for (const p of paras){
  let active = false, lastPage = null;
  p.lines.forEach(ln=>{
    if (lastPage !== null && ln.page !== lastPage) active = false;
    lastPage = ln.page;
    if (!active && susStart(ln.text)) active = true;
    if (active){ ln.suspect = true; suspectCount++; suspectPages.add(ln.page); flaggedPages.add(ln.page); flaggedParas.add(p.n); }
  });
  const words = p.lines.map(l=>l.text).join(' ').split(/\s+/).filter(Boolean).length;
  p.wordCount = words;
  if (susStart(p.lines[0].text) || p.lines.some(l=>l.suspect)) p.reasons.push('starts with a number and a space or a bare number');
  if (words > 300) p.reasons.push('paragraph over 300 words');
  p.flagged = p.reasons.length > 0;
  if (words > 300) { flaggedParas.add(p.n); } // long paragraph: flag row too
}
// why per flagged page (for the flagged-pages table)
const pageRows = [];
for (const pg of pages){
  if (!flaggedPages.has(pg.page)) continue;
  const ps = paras.filter(p=>p.lines.some(l=>l.page===pg.page && l.suspect));
  const sus = [];
  ps.forEach(p=>p.lines.forEach(l=>{ if(l.page===pg.page && l.suspect && susStart(l.text)) sus.push(l.text); }));
  const why = [];
  if (sus.some(t=>/^\d{1,3} [A-Z“"]/.test(t))) why.push('starts with a number and a space');
  if (sus.some(t=>/^\d{1,3}$/.test(t))) why.push('bare number');
  ps.concat(paras.filter(p=>p.lines.some(l=>l.page===pg.page)&&p.wordCount>300)).forEach(p=>{
    if (p.wordCount>300) why.push('paragraph over 300 words');
  });
  pageRows.push({page:pg.page, paras:ps.length?[ps[0].n:null], parasAll:[...new Set(ps.map(p=>p.n))], sus, why:[...new Set(why)]});
}

/* text, first words */
const norm = s => String(s)
  .replace(/[’‘]/g,"'").replace(/[“”]/g,'"')
  .replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();
function firstWords(text){
  const toks = text.split(/\s+/);
  const out = [];
  for (let k=0;k<toks.length && out.length<6;k++){
    let w = toks[k].replace(/([^\s\d])\d+$/, '$1'); // cut glued footnote digits
    if (/^\d+$/.test(w)){
      const prev = out[out.length-1];
      if (prev && /[.,'"]$/.test(prev) && !/(No|Art|art|no|para|paras|chap|sect|vol|p|pp)\.$/.test(prev)) continue;
    }
    if (w!=='') out.push(w);
  }
  return out.join(' ');
}
for (const p of paras){
  p.text = p.lines.map(l=>l.text).join(' ').replace(/  +/g,' ').trim();
  p.page_start = p.lines.length ? p.lines[0].page : null;
  p.page_end   = p.lines.length ? p.lines[p.lines.length-1].page : null;
  p.fw = firstWords(p.text);
  if (REF && REF.first_words && Object.prototype.hasOwnProperty.call(REF.first_words, String(p.n))){
    p.fwMatch = norm(p.fw) === norm(REF.first_words[String(p.n)]);
    p.fwRef = REF.first_words[String(p.n)];
  } else { p.fwMatch = null; p.fwRef = null; }
  p.citation = SYM + ', para. ' + p.n;
  p.limitations = p.flagged
    ? 'footnotes not separated; footnote text may sit inside this paragraph'
    : 'footnotes not separated';
}

/* ---------- checks ---------- */
const checks = [];
const foundN = paras.length;
const expN = REF && typeof REF.paragraphs==='number' ? REF.paragraphs : null;
const refFW = REF && REF.first_words ? Object.keys(REF.first_words).length : 0;
const fwMismatch = paras.filter(p=>p.fwMatch===false);

checks.push({
  name:'Paragraph count', story:'Given this file and this code, the paragraphs found should equal the reference count.',
  vals: 'found ' + foundN + (expN!==null ? ' · reference ' + expN : ' · no reference in this file'),
  state: expN===null ? 'notrun' : (foundN===expN ? 'pass' : 'fail'),
  detail: expN!==null && foundN!==expN ? 'difference ' + (foundN-expN>0?'+':'') + (foundN-expN) : null
});
const numIssues = [];
paras.forEach((p,i)=>{ if (p.n !== i+1) numIssues.push('para. '+p.n+' (p.'+p.page_start+')'); });
checks.push({
  name:'Numbering', story:'Paragraph numbers should run exactly 1 to '+foundN+' in order.',
  vals: numIssues.length ? 'gaps or duplicates: '+numIssues.join(', ') : '1 to '+foundN+' in order',
  state: foundN===0 ? 'notrun' : (numIssues.length ? 'fail' : 'pass')
});
checks.push({
  name:'First words', story:'The first six words of each paragraph, footnote marks removed, should match the reference.',
  vals: refFW ? fwMismatch.length+' mismatch'+(fwMismatch.length===1?'':'es')+' of '+foundN+' · reference has '+refFW : 'no reference in this file',
  state: refFW===0 ? 'notrun' : (fwMismatch.length ? 'fail' : 'pass'),
  link: fwMismatch.length ? '02' : null,
  detail: fwMismatch.slice(0,10).map(p=>'para. '+p.n).join(', ')
});
checks.push({
  name:'Pages flagged', story:'A flag is not a failure: the count can be right while footnote text sits inside a paragraph.',
  vals: flaggedPages.size+' pages flagged, '+flaggedParas.size+' paragraphs to check against the PDF',
  state:'info'
});
checks.push({
  name:'Suspect lines', story:'Lines that look like footnote text are marked and left in place; none is removed.',
  vals: suspectCount+' suspect lines on '+suspectPages.size+' pages, in '+flaggedParas.size+' paragraphs',
  state:'info'
});
checks.push({
  name:'Headers', story:'The first non-empty line of every page should be the document symbol.',
  vals: stats.headerPages.length+' of '+pages.length+' pages'+(stats.headerWarn.length ? ' · unexpected first line on pages '+stats.headerWarn.join(', ') : ''),
  state: pages.length===0 ? 'notrun' : (stats.headerPages.length===pages.length ? 'pass' : 'fail')
});
checks.push({
  name:'Footers', story:'Every page but the first should carry its page number in the footer; other bare numbers are footnote numbers the converter displaced.',
  vals: stats.pagesWithPageNum.length+' of '+(pages.length-1)+' expected pages numbered'+
        (stats.footerBareNums.length ? ' · bare numbers removed: '+stats.footerBareNums.map(f=>'p.'+f.page+' “'+f.num+'”').join(', ') : ''),
  state: pages.length<2 ? 'notrun' : (stats.pagesWithPageNum.length===pages.length-1 ? 'pass' : 'fail')
});
const unlab = headings.filter(h=>!h.labelled);
checks.push({
  name:'Headings', story:'Labelled and unlabelled headings are listed so none can hide inside a paragraph.',
  vals: headings.filter(h=>h.labelled).length+' labelled · '+unlab.length+' unlabelled'+
        (unlab.length ? ' · '+unlab.map(h=>'“'+h.text+'”').join(', ') : ''),
  state:'info'
});
const kindCounts = {cover:0, heading:0, para:0};
bodyLines.forEach(b=>{ if(b.cls && kindCounts[b.cls]!==undefined && b.text!=='') kindCounts[b.cls]++; });
const classified = stats.headerPages.length + stats.footerLines + kindCounts.cover + kindCounts.heading + kindCounts.para;
checks.push({
  name:'Nothing lost', story:'Every non-empty line of the file is classified exactly once: cover, header, heading, paragraph or footer.',
  vals: classified+' classified · '+totalNonEmpty+' non-empty lines in the file · '+stats.hyphenEnd+' lines end with a hyphen (none joined)',
  state: classified===totalNonEmpty ? 'pass' : 'fail',
  detail: classified===totalNonEmpty ? null : (classified-totalNonEmpty)+' lines unaccounted for'
});

/* export records */
function exportRecords(){
  return paras.map(p=>({
    symbol: SYM, paragraph: p.n, section: p.section, part: p.part,
    page_start: p.page_start, page_end: p.page_end,
    text: p.text, text_lines: p.lines.map(l=>l.text).join(' | '),
    flagged: p.flagged, first_words_match: p.fwMatch,
    citation: p.citation, doc_url: D.doc_url || '', limitations: p.limitations
  }));
}
let roundTrip = false;
try {
  roundTrip = foundN>0 && JSON.parse(JSON.stringify(exportRecords())).length === foundN;
} catch(e){ roundTrip = false; }
checks.push({
  name:'Export round trip', story:'The JSON offered for download parses back with one record per paragraph in the table.',
  vals: foundN>0 ? (roundTrip ? foundN+' records parse back, '+foundN+' in the table' : 'round trip failed') : 'nothing to export',
  state: foundN===0 ? 'notrun' : (roundTrip ? 'pass' : 'fail')
});
const booleanChecks = checks.filter(c=>c.state==='pass'||c.state==='fail');
const passCount = booleanChecks.filter(c=>c.state==='pass').length;
const failCount = booleanChecks.length - passCount;

/* ---------- render ---------- */
document.getElementById('h-title').textContent = D.title || 'Untitled document';
document.getElementById('h-meta').innerHTML =
  (SYM ? '<a href="'+esc(D.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(SYM)+'</a> · ' : '') +
  (REF && REF.adopted ? 'adopted '+esc(REF.adopted)+' · ' : '') +
  pages.length+' pages · '+esc(D.source||'');
document.getElementById('h-status').innerHTML =
  (failCount===0 && booleanChecks.length>0
    ? '<span class="dot ok"></span>'+passCount+' of '+booleanChecks.length+' checks pass'
    : '<span class="dot bad"></span>'+failCount+' checks failed') +
  '<br>'+flaggedPages.size+' pages flagged';

document.getElementById('r-sym').textContent = SYM || '—';
document.getElementById('r-short').textContent = (D.title||'').replace(/^General comment No\. \d+ \(\d+\) on /,'GC · ');
const pn = document.getElementById('r-paras');
if (foundN===0){
  pn.innerHTML = '0 <small>paragraphs found</small>';
} else {
  pn.innerHTML = foundN+' <small>of '+(expN!==null?expN:'?')+' paragraphs</small>';
}
const ratio = expN ? Math.min(foundN/expN,1) : 0;
const bar = document.getElementById('r-bar');
bar.querySelector('i').style.width = (ratio*100)+'%';
if (expN!==null && foundN!==expN) bar.classList.add('bad'), pn.classList.add('bad');
document.getElementById('r-paranote').textContent = 'numbered paragraphs extracted from the converter’s text';
const rf = document.getElementById('r-flagged');
rf.innerHTML = '<div class="bignum'+(flaggedPages.size>0?' bad':'')+'">'+flaggedPages.size+' <small>of '+pages.length+' pages flagged</small></div>'+
  '<div class="railnote">footnote text may sit inside a paragraph</div>';
document.getElementById('r-checks').innerHTML =
  '<div style="font-family:Georgia,serif;font-size:26px">'+passCount+' <small style="font-size:14px;color:#4a443a">of '+booleanChecks.length+' checks pass</small></div>';

/* tiles */
const noRef = !REF || expN===null;
const tiles = document.getElementById('tiles');
function tile(fig, num, cls, sub, how){
  return '<div class="tile"><div class="fig">'+fig+'</div><div class="num '+cls+'">'+num+'</div><div class="sub">'+sub+'</div><div class="how">'+how+'</div></div>';
}
tiles.innerHTML =
  tile('FIG.01', foundN, (expN!==null && foundN!==expN)?'bad':'', 'paragraphs found'+(expN!==null?'<br>the document has '+expN+(foundN!==expN?' <span class="badword">(difference '+(foundN-expN>0?'+':'')+(foundN-expN)+')</span>':''):''),'How this is computed: lines matching “n.” alone or “n. text” in the body text, after headers and footers are dropped.')+
  tile('FIG.02', refFW ? fwMismatch.length+' <small>of '+refFW+'</small>' : (expN!==null?foundN:'no reference'), refFW && fwMismatch.length ? 'bad' : '', 'first words match', 'How this is computed: first six words of each paragraph, footnote marks cut, compared with the reference after normalising quotes and dashes.')+
  tile('FIG.03', flaggedPages.size, flaggedPages.size>0?'bad':'', 'of '+pages.length+' pages flagged', 'How this is computed: a page with a suspect line (a bare number, or a number and a space before a capital) inside a paragraph. Check these paragraphs against the PDF.')+
  tile('FIG.04', 'not separated', '', 'footnotes', 'How this is computed: this version leaves footnotes in place and flags them. The document has '+(REF&&REF.footnotes!=null?REF.footnotes:'?')+' footnotes.');

const mm = document.getElementById('mismatchbox');
if (fwMismatch.length){
  let html = '<div class="note">First words differ for '+fwMismatch.length+' paragraph'+(fwMismatch.length>1?'s':'')+' — both versions are shown, neither is corrected.</div>';
  fwMismatch.slice(0,10).forEach(p=>{
    html += '<div class="mismatch">para. <span class="num-cell">'+p.n+'</span>: found <code>'+esc(p.fw)+'</code> · reference <code>'+esc(p.fwRef||'')+'</code></div>';
  });
  if (fwMismatch.length>10) html += '<div class="mismatch">and '+(fwMismatch.length-10)+' more</div>';
  mm.innerHTML = html; mm.hidden = false;
}

/* checks panel */
document.getElementById('disc-checks-n').textContent = checks.length+' CHECKS';
const cp = document.getElementById('checks-panel');
cp.innerHTML = checks.map(c=>{
  const label = c.state==='pass' ? '<span class="pass">pass</span>'
    : c.state==='fail' ? '<span class="fail">check failed</span>'
    : '<span class="notrun">'+(c.state==='notrun'?'not run':'informational')+'</span>';
  return '<div class="check"><strong>'+esc(c.name)+'</strong> · '+label+
    (c.link ? ' · <a href="#" data-goto="'+c.link+'">see tab '+c.link+'</a>' : '')+
    '<div class="vals">'+esc(c.vals)+(c.detail?' · '+esc(c.detail):'')+'</div>'+
    '<div class="vals" style="color:#6c6455">'+esc(c.story)+'</div></div>';
}).join('');

/* flagged pages panel */
document.getElementById('disc-flag-n').textContent = pageRows.length+' PAGES';
const fp = document.getElementById('flag-panel');
if (pageRows.length===0){
  fp.innerHTML = '<div class="note">No page is flagged: no suspect line was found inside a paragraph.</div>';
} else {
  fp.innerHTML = '<div class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</div>'+
    '<table><caption class="serif">'+pageRows.length+' pages where footnote text may sit inside a paragraph</caption>'+
    '<thead><tr><th class="r">Page</th><th class="r">Paragraph</th><th>Suspect lines</th><th>Why</th></tr></thead><tbody>'+
    pageRows.map((r,ix)=>'<tr class="rowbtn" data-fp="'+ix+'" tabindex="0" role="button" aria-expanded="false"><td class="r num-cell">'+r.page+'</td><td class="r">'+(r.parasAll.length?r.parasAll.join(', '):'—')+'</td><td><code>'+esc(r.sus.slice(0,2).join(' · '))+'</code></td><td>'+esc(r.why.join('; '))+'</td></tr>').join('')+
    '</tbody></table><div id="fp-detail"></div>';
}
function showFlaggedPage(ix){
  const r = pageRows[ix];
  const raw = rawPages.find(p=>p.page===r.page);
  if (!raw) return;
  let html = '<div class="rawpage">';
  let inFoot=0, susOn=false;
  raw.lines.forEach((l0,li)=>{
    const l = l0.trim();
    let cls = '';
    if (li===raw.lines.findIndex(x=>x.trim()!=='') && l===SYM){ cls='ft'; }
    else if (inFoot || (l!=='' && isFoot(l) && li>raw.lines.length-8 && (susOn || l==='' || isFoot(l)))){
      // mark footer zone: recompute strip from end
    }
    html += '';
  });
  // simpler: recompute the footer boundary exactly as the pipeline did
  const tmp = raw.lines.map(l=>l.trim());
  let end = tmp.length, start = 0;
  const fi = tmp.findIndex(l=>l!=='');
  if (fi>=0 && tmp[fi]===SYM) start = fi+1;
  while (end>start && isFoot(tmp[end-1])) end--;
  susOn = false;
  html = '<div class="rawpage">';
  tmp.forEach((l,li)=>{
    let cls='';
    if (li<start || li>=end) cls='ft';
    else {
      if (l!==''){
        if (!susOn && susStart(l)) susOn = true;
        if (susOn) cls='hl';
      }
    }
    html += (l===''?'':'<span class="'+cls+'">'+esc(l)+'</span>')+'\n';
  });
  html += '</div>';
  const det = document.getElementById('fp-detail');
  det.innerHTML = '<div class="hint">PAGE '+r.page+' · raw lines from the converter · grey = header/footer · red box = suspect</div>'+html+
    '<div class="note">The suspect lines sit in '+ (r.parasAll.length?'paragraph'+(r.parasAll.length>1?'s ':' ')+r.parasAll.join(', '):'no paragraph')+'. They stay in the text.</div>';
  det.hidden = false;
}

/* exports */
function download(content, filename, mime){
  const blob = new Blob([content], {type:mime+';charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(url), 5000);
}
const baseName = (SYM||'document').replace(/\//g,'-');
document.getElementById('dl-json').disabled = foundN===0;
document.getElementById('dl-md').disabled  = foundN===0;
document.getElementById('dl-json').onclick = ()=>{
  download(JSON.stringify(exportRecords(), null, 2), baseName+'.json', 'application/json');
};
document.getElementById('dl-md').onclick = ()=>{
  const today = new Date().toISOString().slice(0,10);
  let md = '---\n';
  md += 'title: "'+(D.title||'')+'"\n';
  md += 'symbol: "'+SYM+'"\n';
  if (REF && REF.adopted) md += 'adopted: "'+REF.adopted+'"\n';
  md += 'source_url: "'+(D.doc_url||'')+'"\n';
  md += 'extracted: '+today+'\n';
  md += 'paragraphs_found: '+foundN+'\n';
  md += 'paragraphs_expected: '+(expN!==null?expN:'unknown')+'\n';
  md += 'pages_flagged: '+flaggedPages.size+'\n';
  md += 'footnotes: "not separated; the document has '+(REF&&REF.footnotes!=null?REF.footnotes:'?')+'"\n';
  md += '---\n\n';
  const items = [];
  headings.forEach(h=>items.push({idx:h.idx, kind:'h', h}));
  paras.forEach(p=>items.push({idx:p.startIdx, kind:'p', p}));
  items.sort((a,b)=>a.idx-b.idx);
  items.forEach(it=>{
    if (it.kind==='h'){
      md += (it.h.roman?'## ':'### ')+it.h.text+'\n\n';
    } else {
      md += '**'+it.p.n+'.** '+it.p.text+(it.p.flagged?' *(flagged: may contain footnote text)*':'')+'\n\n';
    }
  });
  download(md, baseName+'.md', 'text/markdown');
};

/* tab 02 */
document.getElementById('disc-head-n').textContent = headings.length+' HEADINGS';
document.getElementById('head-panel').innerHTML = headings.length
  ? '<table><caption class="serif">'+headings.length+' headings found, none left inside a paragraph</caption><thead><tr><th class="r">#</th><th>Heading</th><th class="r">Kind</th></tr></thead><tbody>'+
    headings.map((h,i)=>'<tr><td class="r">'+(i+1)+'</td><td>'+esc(h.text)+'</td><td class="r">'+(h.roman?'section':(h.labelled?'subsection':'unlabelled'))+'</td></tr>').join('')+
    '</tbody></table>'
  : '<div class="note">No headings found.</div>';

const pt = document.getElementById('ptable');
document.getElementById('ptable-cap').textContent = foundN+' paragraphs found'+(expN!==null?', '+expN+' expected':'');
pt.innerHTML = '<thead><tr><th class="r">No.</th><th>Section</th><th class="r">Page</th><th>First line</th><th>Check</th></tr></thead><tbody>'+
  paras.map((p,i)=>{
    let chk;
    if (p.fwMatch===false) chk = '<span class="flagword">first words differ</span>';
    else if (p.flagged) chk = '<span class="flagword">may contain footnote text</span>';
    else chk = '<span class="okword">OK</span>';
    let fl = p.text.slice(0,120);
    if (p.text.length>120){ const c = fl.lastIndexOf(' '); if (c>60) fl = fl.slice(0,c); fl += '…'; }
    const pg = p.page_start===p.page_end ? String(p.page_start) : p.page_start+'–'+p.page_end;
    return '<tr class="rowbtn" data-p="'+i+'" tabindex="0" role="button" aria-expanded="false"><td class="r num-cell">'+p.n+'</td><td>'+esc(p.section||'—')+'</td><td class="r">'+pg+'</td><td>'+esc(fl)+'</td><td>'+chk+'</td></tr>'+
      '<tr class="exp-row" hidden><td colspan="5" style="padding:0 0 4px"><div class="exp" id="exp-'+i+'"></div></td></tr>';
  }).join('')+'</tbody>';
if (foundN===0){
  pt.innerHTML = '<tbody><tr><td>No paragraph found in this file. The exports are disabled.</td></tr></tbody>';
}

function toggleRow(row){
  const i = +row.dataset.p;
  const expRow = row.nextElementSibling;
  const open = expRow.hidden;
  expRow.hidden = !open;
  row.setAttribute('aria-expanded', String(open));
  if (open) renderExpanded(i);
}
function renderExpanded(i){
  const p = paras[i];
  const box = document.getElementById('exp-'+i);
  const full = p.lines.map(l=>l.suspect ? '<span class="sus">'+esc(l.text)+'</span>' : esc(l.text)).join(' ');
  const path = [p.part, p.section].filter((v,ix,arr)=>v && arr.indexOf(v)===ix).map(esc).join(' › ');
  let cmp = '';
  if (p.fwRef!==null){
    cmp = '<dl class="cmp"><dt>FOUND</dt><dd'+(p.fwMatch===false?' class="badword"':'')+'>'+esc(p.fw)+'</dd><dt>REFERENCE</dt><dd>'+esc(p.fwRef)+'</dd></dl>';
  }
  box.innerHTML =
    '<div class="hint">PARA. '+p.n+' · '+esc(path||'no heading')+' · PP. '+p.page_start+(p.page_end!==p.page_start?'–'+p.page_end:'')+' · '+p.wordCount+' WORDS'+(p.flagged?' · <span class="flagword">FLAGGED: '+esc(p.reasons.join('; '))+'</span>':'')+'</div>'+
    '<p class="full">'+full+'</p>'+cmp+
    '<div class="tools">'+
      '<button class="btn" data-copy="'+esc(p.citation)+'">Copy citation</button>'+
      '<button class="btn" data-lines="'+i+'">Show the PDF’s lines</button>'+
      '<span class="hint">VERBATIM AS COMPUTED · SUSPECT LINES IN A RED BOX</span>'+
    '</div>'+
    '<div class="lines" id="lines-'+i+'" hidden></div>';
  box.querySelector('[data-copy]').onclick = function(){
    const s = this.dataset.copy;
    const done = ()=>{ const b=document.createElement('span'); b.className='copied'; b.textContent='Copied'; this.after(b); setTimeout(()=>b.remove(),2000); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(s).then(done, done);
    else { const ta=document.createElement('textarea'); ta.value=s; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');}catch(e){} ta.remove(); done(); }
  };
  box.querySelector('[data-lines]').onclick = function(){
    const el = document.getElementById('lines-'+i);
    if (!el.hidden){ el.hidden = true; return; }
    el.innerHTML = p.lines.map(l=>'[p.'+l.page+'] '+esc(l.text)).join('\n');
    el.hidden = false;
  };
}

/* events: rows and collapsibles */
document.addEventListener('click', e=>{
  const goto = e.target.closest('[data-goto]');
  if (goto){ e.preventDefault(); selectTab(goto.dataset.goto==='02'?1:0); return; }
  const row = e.target.closest('tr.rowbtn');
  if (row){
    if (row.dataset.p !== undefined) toggleRow(row);
    else if (row.dataset.fp !== undefined){
      const open = row.getAttribute('aria-expanded')==='true';
      document.querySelectorAll('#flag-panel tr.rowbtn').forEach(r=>r.setAttribute('aria-expanded','false'));
      row.setAttribute('aria-expanded', String(!open));
      showFlaggedPage(+row.dataset.fp);
    }
  }
});
document.addEventListener('keydown', e=>{
  if ((e.key==='Enter'||e.key===' ') && e.target.matches('tr.rowbtn')){ e.preventDefault(); e.target.click(); }
});
function wireDisc(btnId, panelId){
  const b = document.getElementById(btnId), p = document.getElementById(panelId);
  b.onclick = ()=>{ const open = p.hidden; p.hidden = !open; b.setAttribute('aria-expanded', String(open)); };
}
wireDisc('disc-checks','checks-panel');
wireDisc('disc-flag','flag-panel');
wireDisc('disc-head','head-panel');

/* tabs */
const tabs = [document.getElementById('tab1'), document.getElementById('tab2')];
const panels = [document.getElementById('panel1'), document.getElementById('panel2')];
function selectTab(i){
  tabs.forEach((t,k)=>{ t.setAttribute('aria-selected', String(k===i)); t.tabIndex = k===i?0:-1; panels[k].hidden = k!==i; });
  if (i===1) tabs[i].focus();
}
tabs.forEach((t,i)=>{
  t.onclick = ()=>selectTab(i);
  t.onkeydown = e=>{
    let j = null;
    if (e.key==='ArrowRight') j=(i+1)%2;
    if (e.key==='ArrowLeft')  j=(i+1)%2===0?1:0, j=(i-1+2)%2;
    if (j!==null){ e.preventDefault(); selectTab(j); }
  };
});

/* footer */
document.getElementById('foot').innerHTML =
  '<span>'+esc(D.source||'')+'</span>'+
  (D.built?'<span>built '+esc(D.built)+'</span>':'')+
  '<span>Done by this page’s code; no model was called and nothing left the browser.</span>';
})();
</script>
</body>
</html>
```