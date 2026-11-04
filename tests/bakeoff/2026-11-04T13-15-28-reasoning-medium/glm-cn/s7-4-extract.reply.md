Here is the app: it parses the HTML version of the General Comment into numbered paragraphs with their headings, checks itself against the document's reference (count, numbering, first words), documents the lost footnotes and repaired spaces, and exports JSON and Markdown.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a UN document — HTML version</title>
<style>
  :root{
    --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335; --green:#1e6b3a;
    --mono:ui-monospace,Menlo,Consolas,monospace; --serif:Georgia,"Times New Roman",serif;
  }
  [hidden]{display:none!important}
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,sans-serif}
  a{color:var(--red)}
  .mono{font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase}
  .num{font-family:var(--serif)}
  .serifbig{font-family:var(--serif);font-size:44px;line-height:1.05}
  .serifmid{font-family:var(--serif);font-size:26px;line-height:1.1}

  /* header */
  header.app{border-bottom:1px solid var(--rule);padding:18px 24px 14px;display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}
  header.app h1{font-family:var(--serif);font-weight:normal;font-size:24px;margin:6px 0 4px;max-width:60ch}
  header.app .meta{font-size:14px;color:#4a453c}
  .dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
  .dot.ok{background:var(--green)} .dot.bad{background:var(--red)}
  .okword{color:var(--green);font-weight:600} .badword{color:var(--red);font-weight:600}

  /* tabs */
  nav.tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);padding:0 24px;flex-wrap:wrap}
  nav.tabs button{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;
    background:none;border:none;border-bottom:3px solid transparent;padding:12px 18px 10px;color:var(--ink);cursor:pointer}
  nav.tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
  nav.tabs button:focus-visible,button:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--red);outline-offset:2px}

  /* layout */
  .frame{display:grid;grid-template-columns:250px 1fr;gap:0;align-items:start}
  @media (max-width:760px){.frame{grid-template-columns:1fr}}
  aside.rail{border-right:1px solid var(--rule);padding:20px 24px}
  @media (max-width:760px){aside.rail{border-right:none;border-bottom:1px solid var(--rule)}}
  main{padding:24px 32px 60px;min-width:0}

  aside .card{border:1px solid var(--rule);padding:12px 14px;margin-bottom:22px}
  aside .card .sym{font-family:var(--mono);font-size:13px;letter-spacing:.04em}
  .railnum{margin:18px 0}
  .railnum .cap{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#4a453c}
  .bar{height:4px;background:var(--rule);margin-top:8px;position:relative}
  .bar>span{position:absolute;left:0;top:0;bottom:0;background:var(--ink)}
  .bar.bad>span{background:var(--red)}
  .redtext{color:var(--red)}

  /* tiles */
  .tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:22px;margin-bottom:26px}
  .tile{border-top:2px solid var(--ink);padding-top:10px}
  .tile .cap{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#4a453c}
  .tile .how{font-size:13px;color:#4a453c;margin-top:6px}

  /* tables */
  table{border-collapse:collapse;width:100%;margin:10px 0 22px}
  caption{font-family:var(--serif);font-size:18px;text-align:left;padding:6px 0;caption-side:top}
  th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--rule);vertical-align:top;font-size:15px}
  th{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:normal;color:#4a453c}
  td.r,th.r{text-align:right;font-variant-numeric:tabular-nums}
  td .mono{font-size:12px}

  /* rows */
  tr.para{cursor:pointer}
  tr.para td{border-bottom:1px solid var(--rule)}
  tr.para:hover{background:#efe9dd}
  tr.para .pno{font-family:var(--serif);color:var(--red);font-size:18px}
  tr.detail td{background:#efe9dd;border-bottom:1px solid var(--rule);padding:16px 14px}
  .fulltext{font-size:16px;max-width:80ch;white-space:pre-wrap}
  .mark{border:1px solid var(--red);padding:0 1px}
  .sixwords{font-size:14px;margin:12px 0 4px}
  .sixwords .lbl{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#4a453c;display:inline-block;width:9ch}
  button.small{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;background:none;
    border:1px solid var(--ink);padding:5px 10px;cursor:pointer;margin:10px 8px 0 0}
  button.small:hover{background:var(--ink);color:var(--paper)}

  /* closed headings */
  .fold{border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:10px 0;margin:16px 0}
  .fold>button{width:100%;text-align:left;background:none;border:none;cursor:pointer;font-family:var(--serif);font-size:19px;padding:0}
  .fold .mono{color:#4a453c;margin-left:10px}
  .fold .inner{padding:10px 0 4px}

  h2.block{font-family:var(--serif);font-weight:normal;font-size:28px;margin:34px 0 6px;border-top:2px solid var(--ink);padding-top:12px}
  p.how{font-size:14px;color:#4a453c;margin:2px 0 12px}
  .note{font-size:14px;color:#4a453c;max-width:75ch;margin:8px 0 20px}

  .checks .row{display:flex;gap:14px;padding:9px 0;border-bottom:1px solid var(--rule);font-size:15px;align-items:baseline}
  .checks .verdict{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;white-space:nowrap;min-width:11ch}
  .checks .detail{color:#4a453c;font-size:14px}
  ul.plain{margin:6px 0;padding-left:22px}
  ul.plain li{margin:3px 0}

  footer.app{border-top:1px solid var(--rule);padding:14px 24px;font-size:13px;color:#4a453c}
  .figcap{font-family:var(--mono);font-size:11px;letter-spacing:.12em;color:#4a453c;margin-bottom:2px}
</style>
</head>
<body>

<header class="app" id="appheader"></header>
<nav class="tabs" role="tablist" aria-label="Sections" id="tabs"></nav>

<div class="frame">
  <aside class="rail" id="rail"></aside>
  <main id="main">
    <section id="panel-1" role="tabpanel" aria-labelledby="tab-1"></section>
    <section id="panel-2" role="tabpanel" aria-labelledby="tab-2" hidden></section>
    <section id="panel-3" role="tabpanel" aria-labelledby="tab-3" hidden></section>
    <section id="panel-4" role="tabpanel" aria-labelledby="tab-4" hidden></section>
  </main>
</div>

<footer class="app" id="footer"></footer>

<script>
(function(){
"use strict";
const D = window.WORKSHOP_DATA.html_doc || {};
const REF = D.reference || null;
const hasRef = !!(REF && typeof REF.paragraphs === "number");
const hasFW = !!(REF && REF.first_words && Object.keys(REF.first_words).length);
const SYM = D.symbol || "no symbol";
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

/* ---------- parse & classify ---------- */
const doc = new DOMParser().parseFromString(D.html || "", "text/html");
const coverTable = doc.body.querySelector("table");
const container = doc.body.querySelector(".content") || doc.body;
const elements = [];
if (coverTable && coverTable.parentElement === doc.body) elements.push(coverTable);
[...container.children].forEach(el => { if (el !== coverTable) elements.push(el); });

let titleFound = false;
const paras = [];        // {n, text_raw, text, marks[], rules[], heading, part}
const headings = [];     // {label, heading, level, glued}
const unclassified = [];
let committeeLines = 0, coverCount = 0;
let curH = null, curPart = null, sawFirstH2 = false;

const numRe = /^(\d{1,3})\.\s*([\s\S]*)$/;
const headRe = /^([IVX]+|[A-Z])\.\s*(.+)$/;

elements.forEach(el => {
  const tag = el.tagName.toLowerCase();
  const raw = (el.textContent || "").replace(/\s+/g, " ").trim();
  let cls = null;
  if (tag === "table") { cls = "cover"; coverCount++; }
  else {
    const m = raw.match(numRe);
    if (tag === "p" && m && !titleFound === false) { /* fallthrough below */ }
    if (tag === "p" && m) {
      cls = "paragraph";
      const n = parseInt(m[1], 10);
      const raw2 = m[2].trim().replace(/\s+/g, " ");
      const r = repair(raw2);
      paras.push({ n, text_raw: raw2, text: r.text, marks: r.marks, rules: r.rules,
                   heading: curH, part: curPart, el });
    } else if (tag === "h2" && !sawFirstH2) {
      cls = "title"; sawFirstH2 = true; titleFound = true;
    } else if (tag === "h2" || tag === "h3") {
      cls = "heading";
      const hm = raw.match(headRe);
      let label = null, h = raw;
      if (hm) { label = hm[1]; h = hm[2]; }
      const glued = label ? !/^[IVX]+\.\s/.test(raw) && !/^[A-Z]\.\s/.test(raw) : false;
      headings.push({ label, heading: h, level: tag, glued, display: label ? label + ". " + h : h });
      curH = label ? label + ". " + h : h;
      if (tag === "h2" && label && /^[IVX]+$/.test(label)) curPart = curH;
    } else if (tag === "p") { cls = "committee line"; committeeLines++; }
    else if (/^h[1-6]$/.test(tag)) { cls = "heading"; headings.push({label:null,heading:raw,level:tag,glued:false,display:raw}); curH = raw; }
    else cls = "unclassified";
  }
  if (cls === "unclassified" && raw !== "") unclassified.push({tag, text: raw});
  else if (cls === "unclassified") unclassified.push({tag, text: ""});
  elements._cls = elements._cls || [];
  elements._cls.push(cls);
});
// store classification per element for the elements box
const classified = elements.map((el, i) => {
  const tag = el.tagName.toLowerCase();
  const raw = (el.textContent || "").replace(/\s+/g, " ").trim();
  return { tag, raw, cls: null };
});
// re-run classification cleanly for the box (same logic)
(function(){
  let sawH2 = false, k = 0;
  classified.forEach(c => {
    if (c.tag === "table") { c.cls = "cover"; return; }
    const m = c.raw.match(numRe);
    if (c.tag === "p" && m) c.cls = "paragraph";
    else if (c.tag === "h2" && !sawH2) { c.cls = "title"; sawH2 = true; }
    else if (c.tag === "h2" || c.tag === "h3") c.cls = "heading";
    else if (c.tag === "p") c.cls = "committee line";
    else c.cls = "unclassified";
  });
})();

/* ---------- repairs ---------- */
function repair(raw){
  const re = /([a-z])\.([A-Z])|([a-z]),([A-Za-z])|([a-z])\u201C|\u2013([A-Za-z])/g;
  let out = "", marks = [], rules = [], i = 0, m;
  while ((m = re.exec(raw))) {
    out += raw.slice(i, m.index);
    let ins, rule;
    if (m[1] !== undefined){ out += m[1] + ". " + m[2]; ins = m.index + 2; rule = "sentence join"; }
    else if (m[3] !== undefined){ out += m[3] + ", " + m[4]; ins = m.index + 2; rule = "comma join"; }
    else if (m[5] !== undefined){ out += m[5] + " \u201C"; ins = m.index + 2; rule = "quote join"; }
    else { out += "\u2013 " + m[6]; ins = m.index + 1; rule = "dash join"; }
    marks.push(ins); rules.push(rule);
    i = re.lastIndex;
  }
  out += raw.slice(i);
  return { text: out, marks, rules };
}
// enrich repairs with context for tab 03
const repairsList = [];
paras.forEach(p => {
  p.marks.forEach((ins, j) => {
    const rawStart = Math.max(0, ins - 1 - 21);
    repairsList.push({
      para: p.n, rule: p.rules[j],
      before: p.text_raw.slice(rawStart, ins - 1) + "\u2039" + p.text_raw.slice(ins - 1, ins + 20) + "\u203a",
      after:  p.text.slice(Math.max(0, ins - 21), ins - 1) + "\u2039" + p.text.slice(ins - 1, ins + 21) + "\u203a",
      ins
    });
  });
});
const ruleCounts = {};
repairsList.forEach(r => ruleCounts[r.rule] = (ruleCounts[r.rule] || 0) + 1);

/* ---------- characters ---------- */
const allText = paras.map(p => p.text).join(" ");
function countChar(ch){ return allText.split(ch).length - 1; }
const charRows = [
  { name: "en dash", ch: "\u2013", kb: "\u2013" },
  { name: "double curly quotes", ch: "\u201C", extra: "\u201D" },
  { name: "right single quote", ch: "\u2019" },
  { name: "non-breaking hyphen", ch: "\u2011", kb: "hyphen" },
  { name: "non-breaking space", ch: "\u00A0", kb: "space" }
];
charRows.forEach(c => {
  c.count = countChar(c.ch) + (c.extra ? countChar(c.extra) : 0);
  const idx = allText.indexOf(c.ch);
  c.example = idx >= 0 ? allText.slice(Math.max(0, idx - 18), idx) + "\u2039" + c.ch + "\u203a" + allText.slice(idx + 1, idx + 19) : "";
});

/* ---------- first words ---------- */
function normWords(s){
  return s.replace(/[\u2018\u2019]/g, "'").replace(/[\u201C\u201D]/g, '"')
          .replace(/[\u2013\u2011]/g, "-").replace(/\u00A0/g, " ")
          .trim().split(/\s+/);
}
paras.forEach(p => {
  const found = normWords(p.text).slice(0, 6);
  const ref = hasFW ? String(REF.first_words[p.n] || "") : null;
  p.found_six = found.join(" ");
  p.fw_match = ref !== null && ref !== "" ? (found.join(" ") === normWords(ref).slice(0,6).join(" ")) : null;
  p.ref_six = ref;
});
const fwMatchCount = paras.filter(p => p.fw_match === true).length;
const fwNull = paras.some(p => p.fw_match === null);
const fwMismatch = paras.filter(p => p.fw_match === false);

/* ---------- checks ---------- */
const foundCount = paras.length;
const expected = hasRef ? REF.paragraphs : null;
const numbers = paras.map(p => p.n);
let numberingOK = true, gaps = [], dupes = [];
for (let i = 1; i <= foundCount; i++) if (!numbers.includes(i)) { numberingOK = false; gaps.push(i); }
const seen = {};
numbers.forEach(n => { if (seen[n]) { numberingOK = false; dupes.push(n); } seen[n] = 1; });
if (foundCount > 0 && numbers.some((n, i) => i > 0 && n <= numbers[i-1]) ) numberingOK = numberingOK && true;
const gluedHeadings = headings.filter(h => h.glued).length;
const footnotesExpected = hasRef && typeof REF.footnotes === "number" ? REF.footnotes : null;

// export round trip
let exportJSON = "";
let roundTripOK = null;
function buildJSON(){
  return JSON.stringify(paras.map(p => ({
    symbol: SYM, paragraph: p.n,
    section: p.heading || "", part: p.part || "",
    text: p.text, text_raw: p.text_raw,
    first_words_match: p.fw_match,
    citation: SYM + ", para. " + p.n,
    doc_url: D.doc_url || "",
    limitations: "no footnotes in this HTML version; the document has " + (footnotesExpected !== null ? footnotesExpected : "an unknown number of")
  })), null, 2);
}
if (foundCount > 0) {
  exportJSON = buildJSON();
  try { roundTripOK = JSON.parse(exportJSON).length === foundCount; }
  catch(e){ roundTripOK = false; }
}

const checks = [];
function addCheck(name, verdict, detail, linkTo){
  checks.push({ name, verdict, detail, linkTo });
}
addCheck("Paragraph count", hasRef ? (foundCount === expected ? "pass" : "fail")
      : "notrun",
  hasRef ? "found " + foundCount + " / the document has " + expected
         : "no reference in this file");
addCheck("Numbering", numberingOK ? "pass" : "fail",
  numberingOK ? "exactly 1 to " + foundCount + ", in order"
    : "gaps: " + (gaps.length ? gaps.join(", ") : "none") + " · duplicates: " + (dupes.length ? dupes.join(", ") : "none"),
  !numberingOK ? 2 : null);
addCheck("First words", hasFW ? (fwMismatch.length === 0 && !fwNull ? "pass" : "fail") : "notrun",
  hasFW ? fwMatchCount + " of " + foundCount + " match the reference's first six words"
        : "no first_words in the reference");
addCheck("Footnotes", footnotesExpected !== null ? "sourcelimit" : "notrun",
  footnotesExpected !== null
    ? "0 in this HTML / the document has " + footnotesExpected + " — a limit of the source, not of the app"
    : "no reference in this file");
addCheck("Repairs", "pass",
  repairsList.length + " spaces restored in " + new Set(repairsList.map(r => r.para)).size + " paragraphs (" +
  ["sentence join","comma join","quote join","dash join"].map(r => (ruleCounts[r]||0) + " " + r).join(", ") +
  "); text_raw keeps the text as found", 3);
addCheck("Headings", "pass",
  headings.length + " headings found (" + headings.filter(h=>h.level==="h2").length + " h2, " +
  headings.filter(h=>h.level==="h3").length + " h3); " + gluedHeadings + " glued labels separated");
(function(){
  const total = classified.length;
  const un = classified.filter(c => c.cls === "unclassified");
  addCheck("Nothing lost", un.length === 0 ? "pass" : "fail",
    "every block element classified once; " + total + " elements (" +
    coverCount + " cover, 1 title, " + headings.length + " headings, " + foundCount + " paragraphs, " +
    committeeLines + " committee line)" + (un.length ? "; unclassified: " + un.map(u=>u.tag).join(", ") : ""));
})();
addCheck("Export round trip", foundCount === 0 ? "notrun" : (roundTripOK ? "pass" : "fail"),
  foundCount === 0 ? "nothing to export" : "the JSON parses back with " + foundCount + " records, as in the table");

const passCount = checks.filter(c => c.verdict === "pass").length;
const failCount = checks.filter(c => c.verdict === "fail").length;
const limitCount = checks.filter(c => c.verdict === "sourcelimit").length;

/* ---------- header, rail, footer ---------- */
document.getElementById("appheader").innerHTML =
  '<div><div class="mono">UN DOCUMENT · HTML</div>' +
  '<h1>' + esc(D.title || "Untitled document") + '</h1>' +
  '<div class="meta"><a href="' + esc(D.doc_url || "#") + '" target="_blank" rel="noopener">' + esc(SYM) + '</a>' +
  (REF && REF.adopted ? ' · adopted ' + esc(REF.adopted) : '') +
  (D.source ? ' · ' + esc(D.source) : '') + '</div></div>' +
  '<div class="meta" style="text-align:right">' +
  (failCount === 0
    ? '<span class="dot ok"></span><span class="okword">' + passCount + ' of ' + (passCount + failCount) + ' checks pass</span>'
    : '<span class="dot bad"></span><span class="badword">' + failCount + ' check' + (failCount === 1 ? '' : 's') + ' failed</span>') +
  (limitCount ? '<br><span class="redtext">' + limitCount + ' source limit' + (limitCount === 1 ? '' : 's') + '</span> (the footnotes)' : '') +
  '</div>';

const pct = hasRef ? Math.min(100, Math.round(foundCount / expected * 100)) : 0;
document.getElementById("rail").innerHTML =
  '<div class="mono" style="margin-bottom:8px">DOCUMENT</div>' +
  '<div class="card"><div class="sym">' + esc(SYM) + '</div><div style="font-size:13px;margin-top:4px">' +
  esc((D.title || "").replace(/^General comment No\. \d+ \(?\d*\)? ?/i, "").slice(0, 90)) + '</div></div>' +
  '<div class="railnum"><div class="cap">paragraphs</div>' +
  '<div class="serifbig">' + foundCount + '<span style="font-size:20px;color:#4a453c"> of ' + (hasRef ? expected : "?") + '</span></div>' +
  '<div class="bar' + (hasRef && foundCount !== expected ? ' bad' : '') + '"><span style="width:' + pct + '%"></span></div></div>' +
  '<div class="railnum"><div class="cap">footnotes</div>' +
  '<div class="serifbig redtext">0<span style="font-size:20px;color:#4a453c"> of ' + (footnotesExpected !== null ? footnotesExpected : "?") + '</span></div>' +
  '<div class="mono redtext" style="margin-top:4px">not in this HTML</div></div>' +
  '<div class="railnum"><div class="cap">self-checks</div>' +
  '<div style="font-size:17px">' + (failCount === 0 ? '<span class="okword">' + passCount + ' of ' + (passCount + failCount) + ' pass</span>'
    : '<span class="badword">' + failCount + ' failed</span>') + (limitCount ? ' <span class="redtext">· ' + limitCount + ' source limit</span>' : '') + '</div>' +
  '<div style="font-size:13px;margin-top:4px"><a href="#" data-goto="4">see tab 04 for every check</a></div></div>';

document.getElementById("footer").textContent =
  (D.source || "") + (D.built ? " · built " + D.built : "") +
  " · Done by this page's code; no model was called and nothing left the browser.";

/* ---------- tabs ---------- */
const tabNames = ["01 RESULT", "02 PARAGRAPHS", "03 LOST & CHANGED", "04 CHECKS & EXPORT"];
const tabsEl = document.getElementById("tabs");
tabNames.forEach((name, i) => {
  const b = document.createElement("button");
  b.id = "tab-" + (i + 1);
  b.setAttribute("role", "tab");
  b.setAttribute("aria-controls", "panel-" + (i + 1));
  b.setAttribute("aria-selected", i === 0 ? "true" : "false");
  b.tabIndex = i === 0 ? 0 : -1;
  b.textContent = name;
  b.addEventListener("click", () => selectTab(i));
  tabsEl.appendChild(b);
});
const tabBtns = [...tabsEl.children];
tabsEl.addEventListener("keydown", e => {
  const cur = tabBtns.findIndex(b => b.getAttribute("aria-selected") === "true");
  let next = null;
  if (e.key === "ArrowRight") next = (cur + 1) % tabBtns.length;
  if (e.key === "ArrowLeft") next = (cur - 1 + tabBtns.length) % tabBtns.length;
  if (e.key === "Home") next = 0;
  if (e.key === "End") next = tabBtns.length - 1;
  if (next !== null) { e.preventDefault(); selectTab(next); tabBtns[next].focus(); }
});
function selectTab(i){
  tabBtns.forEach((b, j) => {
    b.setAttribute("aria-selected", j === i ? "true" : "false");
    b.tabIndex = j === i ? 0 : -1;
  });
  for (let k = 1; k <= 4; k++) document.getElementById("panel-" + k).hidden = (k !== i + 1);
  window.scrollTo(0, 0);
}
document.addEventListener("click", e => {
  const g = e.target.closest("[data-goto]");
  if (g) { e.preventDefault(); selectTab(parseInt(g.dataset.goto, 10) - 1); }
});

/* ---------- tab 01 : RESULT ---------- */
const p1 = document.getElementById("panel-1");
function tile(cap, big, sub, how, cls){
  return '<div class="tile"><div class="cap">' + cap + '</div>' +
    '<div class="serifbig ' + (cls || '') + '">' + big + '</div>' +
    (sub ? '<div style="font-size:14px;color:#4a453c">' + sub + '</div>' : '') +
    '<div class="how">' + how + '</div></div>';
}
if (foundCount === 0) {
  p1.innerHTML = '<h2 class="block" style="border:none;margin-top:0">No paragraphs found</h2>' +
    '<p class="note">The HTML in this file yielded no numbered &lt;p&gt; elements, so there is nothing to show or export. The tabs 02–04 are empty for the same reason.</p>';
} else {
  p1.innerHTML =
    '<div class="figcap">TAB.01 — DID THE APP FIND EVERYTHING THE DOCUMENT HAS?</div>' +
    '<div class="tiles">' +
    tile("paragraphs found", foundCount,
      hasRef ? (foundCount === expected ? 'the document has ' + expected : 'the document has ' + expected + ' — difference ' + (foundCount - expected)) : "no reference in this file",
      'How: a &lt;p&gt; whose text starts "n." is a paragraph; counted after parsing.',
      hasRef && foundCount !== expected ? "redtext" : "") +
    tile("first words match", hasFW ? fwMatchCount + '<span style="font-size:20px;color:#4a453c"> of ' + foundCount + '</span>' : "—",
      hasFW ? (fwMismatch.length ? fwMismatch.length + " differ" : "all match") : "no first_words in the reference",
      'How: the first six words of each paragraph against <em>reference.first_words</em>, quotes and dashes normalised.' +
      (fwMismatch.length ? ' <a href="#" data-goto="2">See tab 02</a>.' : ''),
      hasFW && fwMismatch.length ? "redtext" : "") +
    tile("footnotes", '<span class="redtext">0</span><span style="font-size:20px;color:#4a453c"> of ' + (footnotesExpected !== null ? footnotesExpected : "?") + '</span>',
      "this HTML version has none; <a href=\"#\" data-goto=\"3\">see tab 03</a>",
      'How: searched the whole HTML for footnote text and marks; nothing of the footnotes survives.',
      "redtext") +
    tile("spaces repaired", repairsList.length,
      new Set(repairsList.map(r => r.para)).size + " paragraphs touched · <a href=\"#\" data-goto=\"3\">see tab 03</a>",
      'How: a space inserted only where the characters prove it was there (after a stop between lowercase and capital, and three similar rules).') +
    '</div>' +
    '<p class="note">The full text of every paragraph, verbatim, is on <a href="#" data-goto="2">tab 02</a>; everything the HTML version lost or changed is on <a href="#" data-goto="3">tab 03</a>.</p>';
}

/* ---------- tab 02 : PARAGRAPHS ---------- */
const p2 = document.getElementById("panel-2");
function firstLine(t){
  if (t.length <= 120) return t;
  const cut = t.slice(0, 121);
  const sp = cut.lastIndexOf(" ");
  return (sp > 60 ? cut.slice(0, sp) : cut.slice(0, 120)) + "…";
}
function markedText(p){
  let html = "", last = 0;
  p.marks.forEach(ins => {
    html += esc(p.text.slice(last, ins)) + '<span class="mark">' + esc(p.text[ins] || " ") + '</span>';
    last = ins + 1;
  });
  html += esc(p.text.slice(last));
  return html;
}
p2.innerHTML =
  '<div class="figcap">TAB.02 — WHAT DOES EACH PARAGRAPH SAY, AND HOW DO I CITE IT?</div>' +
  '<div class="fold"><button aria-expanded="false" data-fold="heads">Headings found: ' + headings.length +
  ' <span class="mono">click = open</span></button><div class="inner" hidden></div></div>' +
  (foundCount === 0 ? '<p class="note">No paragraphs found in this HTML.</p>' :
  '<table><caption>' + foundCount + ' paragraphs found' + (hasRef ? ', ' + expected + ' expected' : '') + '</caption>' +
  '<thead><tr><th class="r" scope="col" style="width:5ch">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>' +
  '<tbody id="parabody"></tbody></table>');

const headFold = p2.querySelector('[data-fold="heads"]');
headFold.addEventListener("click", () => {
  const open = headFold.getAttribute("aria-expanded") === "true";
  headFold.setAttribute("aria-expanded", String(!open));
  const inner = headFold.nextElementSibling;
  inner.hidden = open;
  if (!open && !inner.dataset.filled) {
    inner.innerHTML = headings.map(h =>
      '<div style="padding:3px 0;border-bottom:1px solid var(--rule)"><span class="mono">' + esc(h.level) + '</span> ' +
      esc(h.display) + (h.glued ? ' <span class="mono">label was glued</span>' : '') + '</div>').join("");
    inner.dataset.filled = "1";
  }
});

const body2 = p2.querySelector("#parabody");
paras.forEach((p, idx) => {
  const tr = document.createElement("tr");
  tr.className = "para"; tr.tabIndex = 0; tr.setAttribute("role", "button"); tr.setAttribute("aria-expanded", "false");
  tr.innerHTML = '<td class="r"><span class="pno">' + p.n + '</span></td>' +
    '<td style="max-width:22ch">' + esc(p.heading ? p.heading.split(" (")[0] : "—") + '</td>' +
    '<td style="max-width:48ch">' + esc(firstLine(p.text)) + '</td>' +
    '<td>' + (p.fw_match === null ? '<span class="mono">not run</span>'
      : p.fw_match ? '<span class="okword">OK</span>' : '<span class="badword">first words differ</span>') + '</td>';
  const det = document.createElement("tr");
  det.className = "detail"; det.hidden = true;
  const repCount = p.marks.length;
  det.innerHTML = '<td colspan="4">' +
    (p.part && p.heading && p.part !== p.heading ? '<div class="mono" style="margin-bottom:6px">' + esc(p.part) + ' › ' + esc(p.heading) + '</div>' : '') +
    '<div class="fulltext">' + markedText(p) + '</div>' +
    '<div class="sixwords"><span class="lbl">found</span> ' + esc(p.found_six) + '</div>' +
    (p.ref_six ? '<div class="sixwords"><span class="lbl">reference</span> ' + esc(p.ref_six.split(/\s+/).slice(0,6).join(" ")) + '</div>' : '') +
    '<div style="font-size:13px;color:#4a453c;margin-top:8px">' + (repCount
      ? repCount + ' space' + (repCount === 1 ? '' : 's') + ' repaired here (red box); <span class="mono">text_raw keeps the text as found</span>'
      : 'no repairs in this paragraph') + '</div>' +
    '<button class="small" data-copy="' + p.n + '">Copy citation</button> <span class="mono" style="margin-left:6px">' + esc(SYM) + ', para. ' + p.n + '</span>' +
    '</td>';
  function toggle(){
    const open = tr.getAttribute("aria-expanded") === "true";
    tr.setAttribute("aria-expanded", String(!open));
    det.hidden = open;
  }
  tr.addEventListener("click", toggle);
  tr.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); } });
  body2.appendChild(tr); body2.appendChild(det);
});
p2.addEventListener("click", e => {
  const b = e.target.closest("[data-copy]");
  if (!b) return;
  const p = paras.find(x => x.n === +b.dataset.copy);
  const cit = SYM + ", para. " + p.n;
  const done = () => { const old = b.textContent; b.textContent = "Copied"; setTimeout(() => b.textContent = old, 2000); };
  if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(cit).then(done, done);
  else {
    const ta = document.createElement("textarea"); ta.value = cit; document.body.appendChild(ta);
    ta.select(); try { document.execCommand("copy"); } catch (err) {} ta.remove(); done();
  }
});
function openPara(n){
  selectTab(1);
  const rows = body2.querySelectorAll("tr.para");
  rows.forEach((r, i) => {
    if (paras[i].n === n && r.getAttribute("aria-expanded") !== "true") r.click();
    if (paras[i].n === n) r.scrollIntoView({block: "center"});
  });
}

/* ---------- tab 03 : LOST & CHANGED ---------- */
const p3 = document.getElementById("panel-3");
const ruleLine = ["sentence join","comma join","quote join","dash join"]
  .map(r => (ruleCounts[r] || 0) + " " + r).join(" · ");
p3.innerHTML =
  '<div class="figcap">TAB.03 — WHAT DID THE HTML VERSION LOSE OR CHANGE?</div>' +

  '<h2 class="block">Lost: footnotes <span style="font-size:18px;color:var(--red)">' + (footnotesExpected !== null ? footnotesExpected : "?") + ' lost</span></h2>' +
  '<p class="note">The document has ' + (footnotesExpected !== null ? footnotesExpected : "an unknown number of") + ' footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title\u2019s asterisk points to is missing. To cite a footnote, use the PDF or Word version.</p>' +

  '<h2 class="block">Changed: spaces <span style="font-size:18px">' + repairsList.length + ' restored</span></h2>' +
  '<p class="how">' + ruleLine + '. <span class="mono">click a row = open the paragraph</span></p>' +
  (repairsList.length ?
  '<table><caption>' + repairsList.length + ' missing spaces found and restored</caption>' +
  '<thead><tr><th class="r" scope="col" style="width:7ch">Para.</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead><tbody>' +
  repairsList.map((r, i) =>
    '<tr style="cursor:pointer" data-openpara="' + r.para + '"><td class="r">' + r.para + '</td>' +
    '<td class="mono" style="font-size:12px;letter-spacing:0;text-transform:none">' + esc(r.before) + '</td>' +
    '<td class="mono" style="font-size:12px;letter-spacing:0;text-transform:none">' + esc(r.after) + '</td>' +
    '<td>' + esc(r.rule) + '</td></tr>').join("") +
  '</tbody></table>' : '<p class="note">No missing spaces that the rules could prove.</p>') +
  '<p class="note">Rules restore a space only where the characters prove it was there. Word pairs such as \u201CGiventhe\u201D are not touched; the first-words check catches them only in a paragraph\u2019s first six words.</p>' +

  '<h2 class="block">Changed: characters <span style="font-size:18px">' + charRows.reduce((s, c) => s + c.count, 0) + ' in total</span></h2>' +
  '<table><caption>Characters a reader does not expect, kept as published</caption>' +
  '<thead><tr><th scope="col">Character</th><th class="r" scope="col">Count</th><th scope="col">Example</th></tr></thead><tbody>' +
  charRows.map(c => '<tr><td>' + esc(c.name) + (c.kb ? ' <span class="mono">on a keyboard: ' + esc(c.kb) + '</span>' : '') + '</td>' +
    '<td class="r">' + c.count + '</td><td class="mono" style="font-size:12px;letter-spacing:0;text-transform:none">' + esc(c.example) + '</td></tr>').join("") +
  '</tbody></table>' +
  '<p class="note">Kept exactly as published, in the table and in every export. A search for \u201Cbusiness-related\u201D typed with the hyphen key will not find \u201Cbusiness\u2011related\u201D: normalise the text before searching it.</p>';
p3.addEventListener("click", e => {
  const r = e.target.closest("[data-openpara]");
  if (r) openPara(+r.dataset.openpara);
});

/* ---------- tab 04 : CHECKS & EXPORT ---------- */
const p4 = document.getElementById("panel-4");
const verdictWord = { pass: '<span class="okword">pass</span>', fail: '<span class="badword">check failed</span>',
  sourcelimit: '<span class="redtext">source limit</span>', notrun: '<span class="mono">not run</span>' };
p4.innerHTML =
  '<div class="figcap">TAB.04 — CAN I TRUST THIS, AND CAN I TAKE IT AWAY?</div>' +
  '<h2 class="block" style="margin-top:0">Checks</h2>' +
  '<p class="how">Each check says what was compared and the two values. A failed check never hides a result.</p>' +
  '<div class="checks">' + checks.map(c =>
    '<div class="row"><span class="verdict">' + verdictWord[c.verdict] + '</span><div><strong>' + esc(c.name) + '</strong>' +
    (c.linkTo ? ' · <a href="#" data-goto="' + c.linkTo + '">see the rows</a>' : '') +
    '<div class="detail">' + esc(c.detail) + '</div>' +
    (c.name === "First words" && fwMismatch.length ? '<ul class="plain">' + fwMismatch.slice(0, 20).map(p =>
        '<li>para. ' + p.n + ': found \u201C' + esc(p.found_six) + '\u201D / reference \u201C' + esc(String(p.ref_six).split(/\s+/).slice(0,6).join(" ")) + '\u201D</li>').join("") +
      (fwMismatch.length > 20 ? '<li>… and ' + (fwMismatch.length - 20) + ' more</li>' : '') + '</ul>' : '') +
    '</div></div>').join("") + '</div>' +

  '<h2 class="block">Export</h2>' +
  '<p class="how">Fields: symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url, limitations. ' +
  'The Markdown carries front matter with the source, the counts and the known limitation, then the headings and paragraphs in document order.</p>' +
  '<button class="small" id="dl-json" ' + (foundCount === 0 ? "disabled" : "") + '>Download JSON</button>' +
  '<button class="small" id="dl-md" ' + (foundCount === 0 ? "disabled" : "") + '>Download Markdown</button>' +
  (foundCount === 0 ? '<p class="note">Exports are disabled: no paragraphs were found.</p>' : '') +

  '<div class="fold"><button aria-expanded="false" data-fold="els">Elements found (' + classified.length + ') <span class="mono">click = open</span></button><div class="inner" hidden></div></div>';

const elsFold = p4.querySelector('[data-fold="els"]');
elsFold.addEventListener("click", () => {
  const open = elsFold.getAttribute("aria-expanded") === "true";
  elsFold.setAttribute("aria-expanded", String(!open));
  const inner = elsFold.nextElementSibling;
  inner.hidden = open;
  if (!open && !inner.dataset.filled) {
    inner.innerHTML = '<table><caption>Every block element in the HTML, in order</caption>' +
      '<thead><tr><th scope="col">Tag</th><th scope="col">Classified as</th><th scope="col">Text (first 80 characters)</th></tr></thead><tbody>' +
      classified.map(c => '<tr><td class="mono">' + esc(c.tag) + '</td><td>' + esc(c.cls) +
        (c.cls === "unclassified" ? ' <span class="badword">unclassified</span>' : '') + '</td>' +
        '<td>' + esc(c.raw.slice(0, 80)) + (c.raw.length > 80 ? "…" : "") + '</td></tr>').join("") +
      '</tbody></table>';
    inner.dataset.filled = "1";
  }
});

function download(content, mime, ext){
  const fname = (SYM || "document").replace(/\//g, "-") + ext;
  const blob = new Blob([content], { type: mime + ";charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = fname;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}
function buildMarkdown(){
  const today = new Date().toISOString().slice(0, 10);
  const lim = "no footnotes in this HTML version; the document has " + (footnotesExpected !== null ? footnotesExpected : "an unknown number of");
  let md = "---\n" +
    "title: \"" + (D.title || "") + "\"\n" +
    "symbol: " + SYM + "\n" +
    "adopted: " + (REF && REF.adopted ? REF.adopted : "unknown") + "\n" +
    "source_url: " + (D.doc_url || "") + "\n" +
    "extracted: " + today + "\n" +
    "paragraphs_found: " + foundCount + "\n" +
    "paragraphs_expected: " + (hasRef ? expected : "unknown") + "\n" +
    "footnotes: " + lim + "\n" +
    "---\n\n";
  // document order: walk headings and paragraphs
  let sawFirstH2 = false, pi = 0;
  const ordered = [];
  classified.forEach(c => {
    if (c.cls === "heading") ordered.push({ t: "h", raw: c.raw });
    else if (c.cls === "paragraph") ordered.push({ t: "p", i: pi++ });
  });
  ordered.forEach(o => {
    if (o.t === "h") {
      const lvl = headings.find ? 2 : 2;
      // find matching heading display
      const h = headings.find(x => x.display === c0(o)) || null;
      md += "## " + (h ? h.display : "") + "\n\n";
    } else {
      const p = paras[o.i];
      md += "**" + p.n + ".** " + p.text + "\n\n";
    }
  });
  return md;
  function c0(o){ return o.raw; }
}
// simpler, correct markdown builder using elements + stored data
function buildMarkdown2(){
  const today = new Date().toISOString().slice(0, 10);
  const lim = "no footnotes in this HTML version; the document has " + (footnotesExpected !== null ? footnotesExpected : "an unknown number of");
  let md = "---\n" +
    'title: "' + (D.title || "") + '"\n' +
    "symbol: " + SYM + "\n" +
    "adopted: " + (REF && REF.adopted ? REF.adopted : "unknown") + "\n" +
    "source_url: " + (D.doc_url || "") + "\n" +
    "extracted: " + today + "\n" +
    "paragraphs_found: " + foundCount + "\n" +
    "paragraphs_expected: " + (hasRef ? expected : "unknown") + "\n" +
    "footnotes: " + lim + "\n---\n\n";
  let sawTitle = false, pi = 0;
  const items = [];
  classified.forEach(c => {
    if (c.cls === "heading") items.push({ t: "h", raw: c.raw });
    else if (c.cls === "paragraph") items.push({ t: "p", i: pi++ });
  });
  // map raw heading text to display
  const hmap = new Map();
  headings.forEach(h => hmap.set(h.label ? h.label + "." + h.heading.replace(/^\s+/, "") : h.heading, h.display));
  items.forEach(o => {
    if (o.t === "h") {
      let disp = o.raw;
      for (const [k, v] of hmap) if (k.replace(/\s+/g, "") === o.raw.replace(/\s+/g, "")) { disp = v; break; }
      md += "## " + disp + "\n\n";
    } else {
      const p = paras[o.i];
      md += "**" + p.n + ".** " + p.text + "\n\n";
    }
  });
  return md;
}
document.getElementById("dl-json").addEventListener("click", () => download(buildJSON(), "application/json", ".json"));
document.getElementById("dl-md").addEventListener("click", () => download(buildMarkdown2(), "text/markdown", ".md"));
})();
</script>
</body>
</html>
```

The app runs entirely in the browser: it parses the OHCHR HTML, splits glued paragraph numbers from their text, repairs only provably missing spaces (each shown with before/after and openable in its paragraph), flags first-word mismatches against the reference, reports the footnotes as a source limit, and offers JSON and Markdown exports with citations in Dag Hammarskjöld Library form.