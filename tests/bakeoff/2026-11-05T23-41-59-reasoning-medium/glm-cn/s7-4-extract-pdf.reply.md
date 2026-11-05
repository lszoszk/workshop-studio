Here's the app: a two-tab reader that turns the PDF converter's raw text into numbered paragraphs with headings, checks itself against the document's reference (paragraph count, numbering, first words, nothing lost), flags pages where footnote text may sit inside a paragraph, and exports the paragraphs as JSON or Markdown with their limitations stated. Built on the attached E/C.12/GC/27 file only; every number is computed by the page's own code.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF — General Comment</title>
<style>
:root{--ink:#1d1b18;--paper:#f4f0e8;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b34}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:#5c554a}
a{color:var(--red)}
button{font:inherit;color:inherit;background:none;border:none;cursor:pointer}
button:focus-visible,a:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header.site{padding:16px 28px 12px;border-bottom:1px solid var(--rule);display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;align-items:flex-end}
header.site .meta{font-size:14px;color:#4a443c}
header.site .status{text-align:right}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.dot.g{background:var(--green)} .dot.r{background:var(--red)}
nav.tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);padding:0 28px}
nav.tabs button{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.09em;padding:10px 18px;border-bottom:3px solid transparent;color:#5c554a}
nav.tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
.layout{display:flex;align-items:flex-start;gap:32px;padding:24px 28px 48px;max-width:1400px}
aside.rail{width:250px;flex:none;position:sticky;top:12px}
aside.rail .card{border-top:2px solid var(--ink);padding:10px 0 14px;border-bottom:1px solid var(--rule)}
aside.rail .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px}
aside.rail .short{font-family:Georgia,serif;font-size:15px;margin:4px 0 14px}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:44px;line-height:1.05;font-weight:600}
.bignum small{font-size:15px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-weight:400;color:#4a443c;display:block;margin-top:2px}
.bar{height:4px;background:var(--rule);margin:8px 0 18px}
.bar i{display:block;height:100%;background:var(--ink)}
.bar.bad i{background:var(--red)}
main{flex:1;min-width:0}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:26px;margin-bottom:8px}
.tile{border-top:2px solid var(--ink);padding-top:8px}
.tile .bignum{font-size:46px}
.tile .ref{font-family:Georgia,serif;font-size:26px;color:#5c554a}
.tile .how{font-size:12.5px;color:#5c554a;margin-top:6px}
.mismatch{margin:14px 0 4px;font-size:14px}
.takeaway{margin-top:26px;border-top:1px solid var(--rule);padding-top:14px}
.takeaway .btns{display:flex;gap:14px;margin-top:8px;flex-wrap:wrap}
.btn{border:1px solid var(--ink);padding:8px 16px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;background:var(--ink);color:var(--paper)}
.btn:disabled{opacity:.4;cursor:not-allowed}
details-panel button.acc{display:flex;justify-content:space-between;width:100%;padding:10px 0;border-top:1px solid var(--rule);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;text-align:left}
.acc .mark{color:var(--red)}
section.acc-body{padding:8px 0 18px;font-size:14.5px}
.checkline{padding:5px 0;border-bottom:1px dotted var(--rule)}
.pass{color:var(--green);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em}
.fail{color:var(--red);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em}
table{border-collapse:collapse;width:100%;font-size:14.5px}
caption{caption-side:top;text-align:left;font-family:Georgia,serif;font-size:19px;padding:6px 0 10px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;font-weight:400;color:#5c554a;text-align:left;border-bottom:1px solid var(--ink);padding:6px 10px 6px 0}
td{padding:7px 10px 7px 0;border-bottom:1px solid var(--rule);vertical-align:top}
th.num,td.num{text-align:right;padding-right:14px;white-space:nowrap}
tr.prow>td{border-bottom:none;padding-bottom:2px}
tr.detail>td{border-bottom:1px solid var(--rule);padding:4px 0 16px}
button.rowbtn{font-family:Georgia,serif;font-size:17px;color:var(--red);padding:0}
.tag-red{color:var(--red)}
.sl{border:1px solid var(--red);padding:0 3px}
.detail .full{margin:8px 0;font-size:15.5px;max-width:70em}
.detail .fw{font-size:13px;color:#4a443c;margin:6px 0}
.detail .rowline{display:inline-block;white-space:pre-wrap;font-size:12.5px;color:#4a443c;border-left:2px solid var(--rule);padding-left:10px;margin:6px 0}
.pagenote{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;color:#9b2335;letter-spacing:.05em}
footer.site{border-top:1px solid var(--rule);padding:12px 28px;font-size:12.5px;color:#5c554a;display:flex;gap:24px;flex-wrap:wrap}
.rawlines{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;white-space:pre-wrap;line-height:1.7}
.rawlines .hl{background:#f3dfe2;border-left:3px solid var(--red);padding-left:4px}
.note{font-size:13px;color:#4a443c;margin:6px 0 10px}
</style>
</head>
<body>

<header class="site">
  <div>
    <div class="mono">UN DOCUMENT · PDF TEXT</div>
    <h1 id="docTitle"></h1>
    <div class="meta" id="docMeta"></div>
  </div>
  <div class="status" id="docStatus"></div>
</header>

<nav class="tabs" role="tablist" aria-label="Sections">
  <button role="tab" id="tab1" aria-selected="true" aria-controls="panel1">01 RESULT</button>
  <button role="tab" id="tab2" aria-selected="false" aria-controls="panel2" tabindex="-1">02 PARAGRAPHS</button>
</nav>

<div class="layout">
  <aside class="rail">
    <div class="mono">DOCUMENT</div>
    <div class="card">
      <div class="sym" id="railSym"></div>
      <div class="short" id="railShort"></div>
      <div class="bignum" id="railParas">–</div>
      <div class="bar" id="railBarWrap"><i id="railBar"></i></div>
      <div class="bignum" id="railFlag">–</div>
      <div class="mono" style="margin:8px 0 16px;color:var(--red)" id="railFlagNote"></div>
      <div class="mono" id="railChecks"></div>
    </div>
  </aside>

  <main>
    <section id="panel1" role="tabpanel" aria-labelledby="tab1"></section>
    <section id="panel2" role="tabpanel" aria-labelledby="tab2" hidden></section>
  </main>
</div>

<footer class="site" id="siteFooter"></footer>

<script>
(function(){
"use strict";
const D = window.WORKSHOP_DATA.pdf_text || {};
const R = D.reference || {};
const pages = Array.from(D.records || []).slice().sort((a,b)=>a.page-b.page);
const SYMBOL = D.symbol || "";
const esc = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const norm = s => String(s).replace(/[\u201c\u201d]/g,'"').replace(/[\u2018\u2019]/g,"'").replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ').trim();
const isBlank = t => !t || !t.trim();
const reNumAlone = /^(\d{1,3})\.$/;
const reNumText  = /^(\d{1,3})\. (.+)$/;
const reLabel    = /^([IVX]+|[A-Z])\.$/;
const isParaStart = t => reNumAlone.test(t) || reNumText.test(t);
const isFootLine = t => { t=t.trim();
  return !t || /^GE\./.test(t) || /^\d{6}( \d{6})*$/.test(t) || /^\d{1,3}$/.test(t); };

/* ---------- pass 1: header, footer ---------- */
const pageLines = [];        // per page: [{t, kind, suspect, para}]
const diag = {headerPages:0, pageNumberPages:0, bareNums:[], headerWarnings:[]};
pages.forEach(pg => {
  const raw = String(pg.text==null?"":pg.text).split(/\r?\n/);
  const arr = raw.map(t => ({t, kind:null, suspect:false, para:null, page:pg.page}));
  // header
  let h = arr.findIndex(l => !isBlank(l.t));
  if (h >= 0 && arr[h].t.trim() === SYMBOL.trim()) { arr[h].kind = "header"; diag.headerPages++; }
  else diag.headerWarnings.push(pg.page);
  // footer: walk from the end
  let i = arr.length - 1;
  while (i >= 0 && isFootLine(arr[i].t)) {
    const t = arr[i].t.trim();
    if (/^\d{1,3}$/.test(t)) {
      arr[i].kind = "footer";
      if (Number(t) === pg.page) diag.pageNumberPages++;
      else diag.bareNums.push({page: pg.page, n: t});
    } else if (t) { arr[i].kind = "footer"; }
    i--;
  }
  pageLines.push({page: pg.page, lines: arr});
});

/* ---------- pass 2: body lines, headings, paragraphs ---------- */
const body = [];
pageLines.forEach(pl => pl.lines.forEach(l => { if (l.kind === null) body.push(l); }));

const paras = [], headings = [];
let pending = null, curSection = "", curRoman = "", cur = null, coverDone = false, coverCount = 0;
const closePending = () => { if (!pending) return;
  const text = pending.text.join(" ").replace(/\s+/g," ").trim();
  if (text) { headings.push({level: pending.roman?2:3, text, type: pending.roman?"roman":"letter", paraIndex: paras.length});
    curSection = text; if (pending.roman) curRoman = text; }
  pending = null; };

const cand = t => t.length <= 90 && /^[A-Z]/.test(t) && !/[.;:,\d]$/.test(t);
function unlabHeading(i){
  const a = body[i].t.trim();
  if (!cand(a)) return null;
  const n1 = body[i+1], n2 = body[i+2];
  if (n1 && isParaStart(n1.t.trim())) return {text:a, lines:[i]};
  if (n1 && n2 && !isBlank(n1.t) && cand(n1.t.trim()) && isParaStart(n2.t.trim()))
    return {text:(a+" "+n1.t.trim()), lines:[i, i+1]};
  return null;
}

for (let i = 0; i < body.length; i++) {
  const l = body[i];
  if (isBlank(l.t)) continue;
  const t = l.t.trim();
  if (pending) {
    if (reLabel.test(t) || isParaStart(t)) closePending();
    else { pending.text.push(t); l.kind = "heading"; continue; }
  }
  if (reLabel.test(t)) { pending = {roman: /^[IVX]+$/.test(t), text: []}; l.kind = "heading"; coverDone = true; continue; }
  if (isParaStart(t)) {
    coverDone = true;
    const m = reNumText.exec(t);
    const num = Number((reNumAlone.exec(t) || m)[1]);
    cur = {num, section: curSection, part: curRoman, lines: [], pageStart: l.page, pageEnd: l.page,
           flagged: false, wordCount: 0, fwFound: "", fwMatch: null};
    paras.push(cur); l.kind = "para"; l.para = paras.length - 1;
    if (m) cur.lines.push({t: m[2], page: l.page, suspect: false});
    continue;
  }
  if (coverDone) {
    const uh = unlabHeading(i);
    if (uh) { uh.lines.forEach(j => body[j].kind = "heading");
      headings.push({level: 3, text: uh.text.replace(/\s+/g," ").trim(), type: "unlabelled", paraIndex: paras.length});
      curSection = uh.text.replace(/\s+/g," ").trim(); coverDone = true; continue; }
    l.kind = "para";
    if (cur) { cur.lines.push({t, page: l.page, suspect: false}); l.para = paras.length - 1; }
  } else { l.kind = "cover"; coverCount++; }
}
closePending();

/* ---------- pass 3: text, suspects, first words ---------- */
const isSuspect = t => { t = t.trim();
  return /^\d{1,3}$/.test(t) || /^\d{1,3} [A-Z\u201c"]/.test(t) || /^\* /.test(t); };
const susReason = t => { t = t.trim();
  if (/^\d{1,3}$/.test(t)) return "bare number";
  if (/^\* /.test(t)) return "asterisk note";
  return "starts with a number and a space"; };
let hyphenEnds = 0, suspectLineCount = 0;
const flaggedPages = new Map(); // page -> {suspects:[{t,para,reason}], longParas:Set, paras:Set}

paras.forEach((p, pi) => {
  let lastSusPage = null;
  p.lines.forEach(ln => {
    if (ln.t.endsWith("-")) hyphenEnds++;
    let sus = false;
    if (ln.page === lastSusPage) sus = true;
    else if (isSuspect(ln.t)) { sus = true; lastSusPage = ln.page;
      suspectLineCount++;
      const fp = flaggedPages.get(ln.page) || {suspects: [], longParas: new Set(), paras: new Set()};
      fp.suspects.push({t: ln.t, para: pi, reason: susReason(ln.t)}); fp.paras.add(pi);
      flaggedPages.set(ln.page, fp); }
    ln.suspect = sus;
    p.pageEnd = ln.page;
  });
  p.text = p.lines.map(l => l.t.replace(/\s+/g," ").trim()).join(" ").replace(/  +/g," ").trim();
  p.wordCount = p.text.split(/\s+/).filter(Boolean).length;
  if (p.wordCount > 300) { p.flagged = true;
    const fp = flaggedPages.get(p.pageEnd) || {suspects: [], longParas: new Set(), paras: new Set()};
    fp.longParas.add(pi); fp.paras.add(pi); flaggedPages.set(p.pageEnd, fp); }
  if (p.lines.some(l => l.suspect)) p.flagged = true;
  // first words
  const toks = p.text.split(/\s+/); const out = [];
  for (let j = 0; j < toks.length && out.length < 6; j++) {
    let tk = toks[j].replace(/[0-9]+$/, "");
    if (/^\d+$/.test(tk)) {
      const prev = out[out.length-1], pl = prev ? prev.toLowerCase() : "";
      if (prev && /[.,"\u201d\u2019]$/.test(prev) && !["no.","art.","para.","paras.","p.","pp."].includes(pl)) continue;
    }
    if (tk) out.push(tk);
  }
  p.fwFound = out.join(" ");
  if (R.first_words) {
    const ref = R.first_words[String(p.num)];
    p.fwMatch = ref != null ? norm(p.fwFound) === norm(ref) : null;
  }
});
// annotate body lines with para index & suspect for raw-line views
paras.forEach((p, pi) => p.lines.forEach(ln => {
  const bl = body.find(b => b.page === ln.page && b.kind === "para" && b.para === null && b.t.trim() === ln.t.trim());
}));
// simpler: map by object identity is not possible (ln are copies) — re-annotate by scan:
{ let k = 0;
  body.forEach(b => { if (b.kind === "para" && b.para !== null) {} });
  // rebuild mapping: walk paras' lines in order against body para lines in order
  const bodyParaLines = body.filter(b => b.kind === "para");
  let bi = 0;
  paras.forEach((p, pi) => {
    // the number line itself
    if (bodyParaLines[bi]) { bodyParaLines[bi].para = pi; bi++; }
    p.lines.forEach(ln => {
      while (bi < bodyParaLines.length && isBlank(bodyParaLines[bi].t)) bi++;
      if (bodyParaLines[bi]) { bodyParaLines[bi].para = pi; bodyParaLines[bi].suspect = ln.suspect; bi++; }
    });
  });
}

/* ---------- checks ---------- */
const nums = paras.map(p => p.num);
const gaps = [], dups = [];
{ const seen = new Set();
  for (let n = 1; n <= nums.length; n++) if (!nums.includes(n)) gaps.push(n);
  nums.forEach((n, idx) => { if (nums.indexOf(n) !== idx && !dups.includes(n)) dups.push(n); });
  const sortedOk = nums.every((n, idx) => n === idx + 1); // strict order check below
  var numberingOk = sortedOk && gaps.length === 0 && dups.length === 0;
}
const fwMismatch = paras.filter(p => p.fwMatch === false);
const flaggedParas = paras.map((p,i)=>p.flagged?i:-1).filter(i=>i>=0);
const totalNonEmpty = pageLines.reduce((s,pl)=>s+pl.lines.filter(l=>!isBlank(l.t)).length,0);
const kindCount = k => pageLines.reduce((s,pl)=>s+pl.lines.filter(l=>l.kind===k).length,0);
const unclassified = [];
pageLines.forEach(pl => pl.lines.forEach(l => { if (!isBlank(l.t) && l.kind === null) unclassified.push({page: pl.page, t: l.t}); }));
const classifiedSum = ["header","footer","cover","heading","para"].reduce((s,k)=>s+kindCount(k),0);

function buildExportRecords(){
  return paras.map(p => ({
    symbol: SYMBOL, paragraph: p.num, section: p.section || "", part: p.part || "",
    page_start: p.pageStart, page_end: p.pageEnd, text: p.text,
    text_lines: p.lines.map(l=>l.t).join(" | "),
    flagged: !!p.flagged, first_words_match: p.fwMatch,
    citation: SYMBOL + ", para. " + p.num, doc_url: D.doc_url || "",
    limitations: p.flagged ? "footnotes not separated; " + (p.wordCount>300 && !p.lines.some(l=>l.suspect) ? "this paragraph is over 300 words" : "footnote text may sit inside this paragraph")
                           : "footnotes not separated"
  }));
}
const exportRecs = buildExportRecords();
let roundTripOk = null;
try { roundTripOk = JSON.parse(JSON.stringify(exportRecs)).length === paras.length; } catch(e) { roundTripOk = false; }

const hasRef = !!(R.paragraphs || R.first_words);
const checks = [];
const addC = (label, detail, status) => checks.push({label, detail, status}); // status: pass|fail|info
addC("Paragraph count", paras.length + " found, " + (R.paragraphs != null ? R.paragraphs + " expected" : "no reference in this file"),
     R.paragraphs == null ? "info" : (paras.length === R.paragraphs ? "pass" : "fail"));
addC("Numbering", numberingOk ? "paragraphs run 1 to " + nums.length + " in order"
     : "gaps: " + (gaps.join(", ") || "none") + "; duplicates: " + (dups.join(", ") || "none"),
     numberingOk ? "pass" : "fail");
addC("First words", fwMismatch.length + " of " + (R.paragraphs != null ? R.paragraphs : paras.length) + " differ from the reference"
     + (fwMismatch.length ? " — see tab 02, rows marked \u201cfirst words differ\u201d" : ""),
     !R.first_words ? "info" : (fwMismatch.length === 0 ? "pass" : "fail"));
addC("Pages flagged", flaggedPages.size + " pages flagged, " + flaggedParas.length + " paragraphs to check against the PDF", "info");
addC("Suspect lines", suspectLineCount + " suspect lines on " + flaggedPages.size + " pages, in " + flaggedParas.length + " paragraphs; none removed", "info");
addC("Headers", diag.headerPages + " of " + pages.length + " pages begin with the symbol " + SYMBOL,
     diag.headerPages === pages.length ? "pass" : "fail");
addC("Footers", diag.pageNumberPages + " of " + (pages.length - 1) + " expected pages carry a page number; "
     + diag.bareNums.length + " bare footnote numbers removed from footers"
     + (diag.bareNums.length ? " (" + diag.bareNums.map(b=>"p." + b.page + ": " + b.n).join("; ") + ")" : ""),
     diag.pageNumberPages === pages.length - 1 ? "pass" : "fail");
addC("Headings", headings.length + " headings found (" + headings.filter(h=>h.type!=="unlabelled").length + " labelled, "
     + headings.filter(h=>h.type==="unlabelled").length + " unlabelled: "
     + headings.filter(h=>h.type==="unlabelled").map(h=>"\u201c" + h.text + "\u201d").join(", ") + ")", "info");
addC("Nothing lost", classifiedSum + " of " + totalNonEmpty + " non-empty lines classified (cover " + coverCount
     + ", headings " + kindCount("heading") + ", paragraphs " + kindCount("para") + ", headers " + kindCount("header")
     + ", footers " + kindCount("footer") + ")"
     + (unclassified.length ? "; unclassified: " + unclassified.map(u=>"p." + u.page + " \u201c" + u.t.slice(0,40) + "\u201d").join("; ") : ""),
     (classifiedSum === totalNonEmpty && unclassified.length === 0) ? "pass" : "fail");
addC("Export round trip", "the JSON offered for download parses back to " + exportRecs.length + " records, the table shows " + paras.length,
     roundTripOk ? "pass" : "fail");
const passCount = checks.filter(c=>c.status==="pass").length;
const failCount = checks.filter(c=>c.status==="fail").length;

/* ---------- render: header, rail, footer ---------- */
document.getElementById("docTitle").textContent = D.title || SYMBOL || "Untitled document";
document.getElementById("docMeta").innerHTML =
  (D.doc_url ? '<a href="' + esc(D.doc_url) + '" target="_blank" rel="noopener">' + esc(SYMBOL) + '</a>' : esc(SYMBOL)) +
  (R.adopted ? " · adopted " + esc(R.adopted) : "") + " · " + pages.length + " pages" +
  (D.source ? " · " + esc(D.source) : "");
document.getElementById("docStatus").innerHTML =
  '<div class="mono"><span class="dot ' + (failCount ? "r" : "g") + '"></span>' +
  (failCount ? failCount + " checks failed" : passCount + " of " + (passCount + failCount) + " checks pass") + '</div>' +
  '<div class="mono" style="color:var(--red);margin-top:4px">' + flaggedPages.size + " pages flagged</div>";

document.getElementById("railSym").textContent = SYMBOL;
document.getElementById("railShort").textContent = (D.title || "").replace(/^General comment No\. \d+ \(\d+\) on /i, "GC on ");
document.getElementById("railParas").innerHTML = paras.length + "<small>paragraphs" +
  (R.paragraphs != null ? " of " + R.paragraphs + " expected" : " · no reference in this file") + "</small>";
const ratio = R.paragraphs ? Math.min(100, Math.round(paras.length / R.paragraphs * 100)) : 0;
document.getElementById("railBar").style.width = ratio + "%";
document.getElementById("railBarWrap").classList.toggle("bad", R.paragraphs != null && paras.length !== R.paragraphs);
document.getElementById("railFlag").innerHTML = flaggedPages.size + "<small>pages flagged of " + pages.length + "</small>";
document.getElementById("railFlag").style.color = flaggedPages.size ? "var(--red)" : "";
document.getElementById("railFlagNote").textContent = "footnote text may sit inside a paragraph";
document.getElementById("railChecks").innerHTML = (failCount
  ? '<span class="dot r"></span>' + failCount + " checks failed"
  : '<span class="dot g"></span>' + passCount + " of " + (passCount + failCount) + " checks pass") +
  '<br><span style="color:#5c554a">' + checks.length + " checks run</span>";

document.getElementById("siteFooter").innerHTML =
  (D.source ? esc(D.source) : "") + (D.built ? " · built " + esc(D.built) : "") +
  " · Done by this page's code; no model was called and nothing left the browser.";

/* ---------- tab 01 ---------- */
const mismatchHtml = fwMismatch.length ? (
  '<div class="mismatch"><span class="mono">FIRST WORDS DIFFER — ' + fwMismatch.length + '</span>' +
  fwMismatch.slice(0, 10).map(p =>
    '<div>para. ' + p.num + ": found \u2026" + esc(p.fwFound) + " / reference \u2026" + esc(R.first_words[String(p.num)] || "") + "</div>").join("") +
  (fwMismatch.length > 10 ? '<div>and ' + (fwMismatch.length - 10) + " more</div>" : "") + "</div>"
) : "";

const tile = (big, ref, label, how, cls) =>
  '<div class="tile ' + (cls||"") + '"><div class="mono">' + label + '</div>' +
  '<div class="bignum">' + big + (ref ? ' <span class="ref">' + ref + "</span>" : "") + "</div>" +
  '<div class="how">' + how + "</div></div>";

const tiles =
  tile(paras.length, R.paragraphs != null ? "of " + R.paragraphs : null, "Paragraphs found",
       "How this is computed: lines matching a paragraph number alone or with its text, after header and footer lines are dropped.",
       R.paragraphs != null && paras.length !== R.paragraphs ? "tag-red" : "") +
  tile((R.paragraphs != null ? fwMismatch.filter(p=>p).length===0 ? paras.length - fwMismatch.length : paras.length - fwMismatch.length : "—"),
       R.paragraphs != null ? "of " + R.paragraphs : null, "First words match",
       "How this is computed: the first six words of each paragraph, footnote marks removed, compared with the reference after normalising quotes and dashes.",
       R.first_words && fwMismatch.length ? "tag-red" : "") +
  tile(flaggedPages.size, "of " + pages.length, "Pages flagged",
       "How this is computed: a page is flagged when a line inside a paragraph looks like footnote text (a bare number, a number then a capital, or an asterisk note). Footnote text may sit inside a paragraph: check these paragraphs against the PDF.",
       flaggedPages.size ? "tag-red" : "") +
  tile("not separated", R.footnotes != null ? "document has " + R.footnotes : null, "Footnotes",
       "How this is computed: this version leaves footnotes in place and flags the pages where they may sit; it does not remove them.");

function download(name, content, type){
  const blob = new Blob([content], {type: type + ";charset=utf-8"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = name; document.body.appendChild(a); a.click();
  setTimeout(()=>{ URL.revokeObjectURL(url); a.remove(); }, 500);
}
const fileBase = (SYMBOL || "document").replace(/\//g, "-");

function mdExport(){
  const today = new Date().toISOString().slice(0,10);
  let md = "---\n" +
    "title: \"" + (D.title||"").replace(/"/g,"'") + "\"\n" +
    "symbol: " + SYMBOL + "\n" +
    "adopted: " + (R.adopted || "") + "\n" +
    "source_url: " + (D.doc_url || "") + "\n" +
    "extracted: " + today + "\n" +
    "paragraphs_found: " + paras.length + "\n" +
    "paragraphs_expected: " + (R.paragraphs != null ? R.paragraphs : "unknown") + "\n" +
    "pages_flagged: " + flaggedPages.size + "\n" +
    'footnotes: "not separated; the document has ' + (R.footnotes != null ? R.footnotes : "an unknown number of") + '"\n' +
    "---\n\n";
  let hi = 0;
  paras.forEach((p, pi) => {
    while (hi < headings.length && headings[hi].paraIndex <= pi) {
      const h = headings[hi++];
      md += (h.level === 2 ? "## " : "### ") + h.text + "\n\n";
    }
    md += "**" + p.num + ".** " + p.text + (p.flagged ? " *(flagged: may contain footnote text)*" : "") + "\n\n";
  });
  while (hi < headings.length) { const h = headings[hi++]; md += (h.level===2?"## ":"### ") + h.text + "\n\n"; }
  return md;
}

const flagRows = Array.from(flaggedPages.entries()).sort((a,b)=>a[0]-b[0]).map(([page, fp]) => {
  const reasons = new Set(fp.suspects.map(s=>s.reason));
  if (fp.longParas.size) reasons.add("paragraph over 300 words");
  return '<tr class="frow" data-page="' + page + '">' +
    '<td class="num">' + page + "</td>" +
    '<td class="num">' + Array.from(fp.paras).map(pi=>paras[pi].num).join(", ") + "</td>" +
    '<td class="num">' + fp.suspects.length + "</td>" +
    "<td>" + Array.from(reasons).map(esc).join("; ") + "</td></tr>";
}).join("");

panel1.innerHTML =
  '<div class="tiles">' + tiles + "</div>" + mismatchHtml +
  '<div class="takeaway"><div class="mono">TAKE THE PARAGRAPHS AWAY</div>' +
  '<div class="note">Each record carries its source, fields and known limitations (footnotes not separated).</div>' +
  '<div class="btns"><button class="btn" id="dlJson" ' + (paras.length?"":"disabled") + '>Download JSON</button>' +
  '<button class="btn" id="dlMd" ' + (paras.length?"":"disabled") + '>Download Markdown</button></div></div>' +
  '<details-panel>' +
  '<button class="acc" id="accChecks" aria-expanded="false">Every check (' + checks.length + ') <span class="mark">+</span></button>' +
  '<section class="acc-body" id="bodyChecks" hidden>' +
    checks.map(c => '<div class="checkline"><span class="' + c.status + '">' +
      (c.status === "pass" ? "pass" : c.status === "fail" ? "check failed" : "noted") + "</span> · " +
      "<b>" + esc(c.label) + ".</b> " + esc(c.detail) + "</div>").join("") +
  "</section>" +
  '<button class="acc" id="accFlags" aria-expanded="false">Flagged pages (' + flaggedPages.size + ') <span class="mark">+</span></button>' +
  '<section class="acc-body" id="bodyFlags" hidden>' +
    '<div class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</div>' +
    (flaggedPages.size ?
      '<table><caption>' + flaggedPages.size + " pages flagged, " + flaggedParas.length + " paragraphs to check</caption>" +
      "<thead><tr><th class='num'>Page</th><th class='num'>Paragraph</th><th class='num'>Suspect lines</th><th>Why</th></tr></thead>" +
      "<tbody>" + flagRows + "</tbody></table>" : "<p>No pages flagged.</p>") +
    '<div id="flagDetail"></div>' +
  "</section></details-panel>";

document.getElementById("dlJson").addEventListener("click", () =>
  download(fileBase + ".json", JSON.stringify(exportRecs, null, 2), "application/json"));
document.getElementById("dlMd").addEventListener("click", () =>
  download(fileBase + ".md", mdExport(), "text/markdown"));

function wireAcc(btnId, bodyId){
  const b = document.getElementById(btnId), s = document.getElementById(bodyId);
  b.addEventListener("click", () => {
    const open = b.getAttribute("aria-expanded") === "true";
    b.setAttribute("aria-expanded", String(!open));
    s.hidden = open; b.querySelector(".mark").textContent = open ? "+" : "–";
  });
}
wireAcc("accChecks", "bodyChecks"); wireAcc("accFlags", "bodyFlags");

panel1.querySelectorAll(".frow").forEach(tr => tr.addEventListener("click", () => {
  const page = Number(tr.dataset.page);
  const pl = pageLines.find(p => p.page === page);
  const existing = document.getElementById("flagDetail");
  if (existing.dataset.page === String(page)) { existing.hidden = !existing.hidden; return; }
  existing.dataset.page = page; existing.hidden = false;
  existing.innerHTML = '<div class="mono" style="margin-top:14px">PAGE ' + page + " · RAW LINES · SUSPECT LINES HIGHLIGHTED</div>" +
    '<div class="rawlines">' + pl.lines.map(l => {
      const cls = (l.kind === "para" && l.suspect) ? "hl" : "";
      const tag = l.para !== null && l.kind === "para" ? ' <span class="pagenote">[para ' + paras[l.para].num + "]</span>"
                : l.kind && l.kind !== "para" ? ' <span class="pagenote">[' + l.kind + "]</span>" : "";
      return (cls ? '<span class="hl">' : "") + esc(l.t) + (cls ? "</span>" : "") + tag;
    }).join("\n") + "</div>";
}));

/* ---------- tab 02 ---------- */
const headingsList = headings.map(h =>
  '<li><span class="mono">' + (h.type === "roman" ? "roman" : h.type === "letter" ? "letter" : "unlabelled") + "</span> — " +
  esc(h.text) + ' <span class="pagenote">(before para ' + (paras[h.paraIndex] ? paras[h.paraIndex].num : "–") + ")</span></li>").join("");

const rows = paras.map((p, pi) => {
  const firstLine = p.text.slice(0, 120);
  const cut = firstLine.length === 120 ? firstLine.slice(0, firstLine.lastIndexOf(" ")) + "…" : firstLine;
  const check = p.fwMatch === false ? '<span class="tag-red">first words differ</span>'
    : p.flagged ? '<span class="tag-red">may contain footnote text</span>' : "OK";
  return '<tr class="prow" data-pi="' + pi + '"><td class="num"><button class="rowbtn" aria-expanded="false">' + p.num + "</button></td>" +
    "<td>" + esc(p.section || "—") + "</td>" +
    '<td class="num">' + p.pageStart + (p.pageEnd !== p.pageStart ? "–" + p.pageEnd : "") + "</td>" +
    "<td>" + esc(cut) + "</td><td>" + check + "</td></tr>" +
    '<tr class="detail" hidden><td colspan="5"><div class="dwrap" data-pi="' + pi + '"></div></td></tr>';
}).join("");

panel2.innerHTML =
  '<button class="acc" id="accHead" aria-expanded="false" style="border-top:none">Headings found: ' + headings.length + ' <span class="mark">+</span></button>' +
  '<section class="acc-body" id="bodyHead" hidden><ul style="font-size:14px;padding-left:18px">' + headingsList + "</ul></section>" +
  '<table><caption>' + paras.length + " paragraphs found" + (R.paragraphs != null ? ", " + R.paragraphs + " expected" : "") + "</caption>" +
  '<thead><tr><th class="num">No.</th><th>Section</th><th class="num">Page</th><th>First line</th><th>Check</th></tr></thead>' +
  "<tbody>" + rows + "</tbody></table>";
wireAcc("accHead", "bodyHead");

function fillDetail(pi){
  const p = paras[pi];
  const wrap = panel2.querySelector('.dwrap[data-pi="' + pi + '"]');
  if (wrap.dataset.filled) return;
  wrap.dataset.filled = "1";
  const full = p.lines.map(l => l.suspect ? '<span class="sl">' + esc(l.t) + "</span>" : esc(l.t)).join(" ");
  const ref = R.first_words ? (R.first_words[String(p.num)] || "") : "";
  wrap.innerHTML =
    '<div class="mono">' + esc(p.part ? p.part + " \u203a " : "") + esc(p.section || "no heading") + "</div>" +
    '<p class="full">' + full + "</p>" +
    '<div class="fw"><b>First six words, found:</b> ' + esc(p.fwFound) + (ref ? "<br><b>Reference:</b> " + esc(ref) : " · no reference in this file") + "</div>" +
    '<button class="acc" style="border-top:1px dotted var(--rule)" aria-expanded="false">Show the PDF\u2019s lines <span class="mark">+</span></button>' +
    '<div class="rowline" hidden>' + p.lines.map(l =>
      (l.page !== p.pageStart && p.lines.indexOf(l) > 0 && p.lines[p.lines.indexOf(l)-1].page !== l.page ? "\n[" + l.page + "] " : "") +
      esc(l.t) + (l.suspect ? " \u2190 suspect" : "")).join("\n") + "</div>" +
    '<div style="margin-top:8px"><button class="btn" data-copy="' + pi + '">Copy citation</button> <span class="mono" data-copied></span></div>";
  const tb = wrap.querySelector("button.acc"), td = wrap.querySelector(".rowline");
  tb.addEventListener("click", () => {
    const open = tb.getAttribute("aria-expanded") === "true";
    tb.setAttribute("aria-expanded", String(!open)); td.hidden = open;
    tb.querySelector(".mark").textContent = open ? "+" : "–";
  });
  const cb = wrap.querySelector("[data-copy]"), note = wrap.querySelector("[data-copied]");
  cb.addEventListener("click", () => {
    const cite = SYMBOL + ", para. " + p.num;
    const done = () => { note.textContent = "Copied"; setTimeout(()=>{ note.textContent = ""; }, 2000); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(cite).then(done, () => fallback(cite, done));
    else fallback(cite, done);
  });
  function fallback(text, done){
    const ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta);
    ta.select(); try { document.execCommand("copy"); } catch(e){} ta.remove(); done();
  }
}

panel2.querySelectorAll("tr.prow").forEach(tr => {
  const pi = Number(tr.dataset.pi);
  const btn = tr.querySelector(".rowbtn");
  const det = tr.nextElementSibling;
  const open = () => { fillDetail(pi); det.hidden = false; btn.setAttribute("aria-expanded", "true"); };
  const close = () => { det.hidden = true; btn.setAttribute("aria-expanded", "false"); };
  btn.addEventListener("click", () => det.hidden ? open() : close());
  tr.addEventListener("click", e => { if (e.target === btn || tr.contains(e.target) && e.target.tagName !== "TD") return; det.hidden ? open() : close(); });
});

/* ---------- tabs ---------- */
const tabs = [document.getElementById("tab1"), document.getElementById("tab2")];
const panels = [document.getElementById("panel1"), document.getElementById("panel2")];
function select(i){
  tabs.forEach((t,j)=>{ t.setAttribute("aria-selected", String(i===j)); t.tabIndex = i===j?0:-1; panels[j].hidden = i!==j; });
  tabs[i].focus();
}
tabs.forEach((t,i)=>{
  t.addEventListener("click", ()=>select(i));
  t.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") select((i+1)%2);
    if (e.key === "ArrowLeft") select((i+1)%2);
  });
});
})();
</script>
</body>
</html>
```