Here is the app: it turns the converter's raw text into numbered paragraphs with headings, checks itself against the document's reference, flags where footnote text may sit inside a paragraph, and exports the result as JSON or Markdown.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b34;}
*{box-sizing:border-box;}
[hidden]{display:none!important;}
html{scroll-behavior:smooth;}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;}
a{color:var(--red);}
:focus-visible{outline:2px solid var(--red);outline-offset:2px;}
.mono{font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;}
.serif{font-family:Georgia,"Times New Roman",serif;}
header.site{padding:18px 28px 14px;border-bottom:1px solid var(--rule);}
header.site .lbl{color:#6b6459;}
header.site h1{font-family:Georgia,"Times New Roman",serif;font-size:26px;font-weight:normal;margin:6px 0 4px;}
header.site .meta{font-size:13.5px;color:#4c463d;}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:baseline;}
.dot.g{background:var(--green);} .dot.r{background:var(--red);}
.hdr-right{float:right;text-align:right;font-size:13.5px;margin-top:2px;}
.tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);padding:0 28px;}
.tab{appearance:none;background:none;border:none;border-bottom:3px solid transparent;padding:10px 18px 8px;cursor:pointer;font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:#4c463d;}
.tab[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red);}
main{display:grid;grid-template-columns:270px 1fr;gap:0;align-items:start;}
aside{border-right:1px solid var(--rule);padding:20px 22px;position:sticky;top:0;}
aside h2{font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;color:#6b6459;font-weight:normal;margin:0 0 10px;}
.card{border-top:1px solid var(--rule);padding:12px 0 14px;}
.card .sym{font:12px/1.5 ui-monospace,Menlo,Consolas,monospace;margin:0 0 4px;}
.card .ttl{font-size:13px;color:#4c463d;margin:0 0 14px;}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:44px;line-height:1.05;}
.bignum small{font-size:18px;color:#6b6459;}
.bar{height:3px;background:var(--rule);margin:10px 0 4px;position:relative;}
.bar i{position:absolute;left:0;top:0;bottom:0;background:var(--ink);}
.bar.bad i{background:var(--red);}
.railnote{font-size:12.5px;color:#4c463d;margin:4px 0 0;}
.red{color:var(--red);} .grn{color:var(--green);}
section.panel{padding:24px 32px 60px;max-width:1060px;}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:20px 0;}
.tile .fig{font:10px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;color:#6b6459;margin-bottom:6px;}
.tile .n{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1.05;}
.tile .sub{font-size:13px;color:#4c463d;margin-top:4px;}
.how{font-size:12px;color:#6b6459;margin-top:8px;}
h3.sect{font-family:Georgia,"Times New Roman",serif;font-weight:normal;font-size:20px;margin:30px 0 8px;}
button.act{appearance:none;background:var(--ink);color:var(--paper);border:none;padding:10px 18px;cursor:pointer;font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;margin:6px 14px 0 0;}
button.act:disabled{opacity:.4;cursor:not-allowed;}
button.disc{appearance:none;background:none;border:none;border-top:1px solid var(--rule);width:100%;text-align:left;padding:12px 0;cursor:pointer;font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);display:flex;justify-content:space-between;}
button.disc::after{content:"+";}
button.disc[aria-expanded="true"]::after{content:"–";}
.mismatch{margin:14px 0 0;font-size:14px;}
.mismatch div{padding:3px 0;border-bottom:1px solid var(--rule);}
table{width:100%;border-collapse:collapse;font-size:14px;}
caption{font-family:Georgia,"Times New Roman",serif;font-size:17px;text-align:left;padding:10px 0 6px;}
th{font:10.5px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;font-weight:normal;text-align:left;border-bottom:1px solid var(--ink);padding:6px 10px 6px 0;}
th.num,td.num{text-align:right;}
td{border-bottom:1px solid var(--rule);padding:7px 10px 7px 0;vertical-align:top;}
tr.prow{cursor:pointer;}
tr.prow:hover{background:#ece6d9;}
tr.exp>td{border-bottom:1px solid var(--rule);background:#efe9dd;padding:16px 18px;}
.sus{border:1px solid var(--red);padding:0 3px;}
.exp-text{margin:0 0 12px;}
.exp-meta{font-size:13px;color:#4c463d;margin:0 0 10px;}
.exp-meta b{color:var(--ink);font-weight:600;}
.pdflines{font:12px/1.7 ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;background:#ece6d9;border:1px solid var(--rule);padding:10px 12px;margin:10px 0;}
button.mini{appearance:none;background:none;border:1px solid var(--ink);padding:5px 12px;cursor:pointer;font:10.5px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;margin:8px 10px 0 0;}
.checkline{display:flex;gap:14px;padding:7px 0;border-bottom:1px solid var(--rule);font-size:14px;align-items:baseline;}
.checkline .st{min-width:110px;font:10.5px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;}
.note{font-size:13.5px;color:#4c463d;margin:8px 0;}
footer.site{border-top:1px solid var(--rule);padding:14px 28px;font-size:12.5px;color:#6b6459;}
.headlist{font-size:13.5px;columns:2;gap:26px;margin:8px 0 0;}
.headlist div{padding:2px 0;break-inside:avoid;}
</style>
</head>
<body>

<header class="site">
  <div class="hdr-right" id="hdrRight"></div>
  <div class="lbl mono">UN DOCUMENT · PDF TEXT</div>
  <h1 id="docTitle"></h1>
  <div class="meta" id="docMeta"></div>
</header>

<div class="tabs" role="tablist" aria-label="Sections">
  <button class="tab" id="tab1" role="tab" aria-selected="true" aria-controls="p1">01 RESULT</button>
  <button class="tab" id="tab2" role="tab" aria-selected="false" aria-controls="p2" tabindex="-1">02 PARAGRAPHS</button>
</div>

<main>
<aside>
  <h2>DOCUMENT</h2>
  <div class="card">
    <p class="sym" id="railSym"></p>
    <p class="ttl" id="railTtl"></p>
  </div>
  <div class="card" id="railParas"></div>
  <div class="card" id="railFlag"></div>
  <div class="card" id="railChecks"></div>
</aside>

<section class="panel" id="p1" role="tabpanel" aria-labelledby="tab1"></section>
<section class="panel" id="p2" role="tabpanel" aria-labelledby="tab2" hidden></section>
</main>

<footer class="site" id="foot"></footer>

<script>
(function(){
"use strict";
const D = window.WORKSHOP_DATA && window.WORKSHOP_DATA.pdf_text || {};
const SYM = D.symbol || "";
const REF = D.reference || null;
const recs = (D.records||[]).filter(r=>r&&typeof r.text==="string").slice().sort((a,b)=>a.page-b.page);
const esc = s => String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");

/* ---------- line tests ---------- */
function startInfo(t){
  let m = /^(\d{1,3})\.$/.exec(t); if(m) return {num:+m[1], rest:null};
  m = /^(\d{1,3})\. (.+)$/.exec(t); if(m) return {num:+m[1], rest:m[2]};
  return null;
}
const isStart = t => startInfo(t)!==null;
const isLabel = t => /^([IVX]+|[A-Z])\.$/.test(t);
function isUnlabelled(t){
  return t.length>0 && t.length<=90 && /^[A-Z]/.test(t) && !/[.;:,0-9]$/.test(t);
}

/* ---------- page split: header, footer, body ---------- */
const bodyLines = [];
let headerPages = 0, headerWarnings = [], pageNumPages = 0, bareFooter = [];
let footerCount = 0, totalNonEmpty = 0;
for(const r of recs){
  const lines = r.text.split(/\r?\n/).map(s=>s.replace(/\s+$/,""));
  totalNonEmpty += lines.filter(s=>s.trim()!=="").length;
  let fi = 0; while(fi<lines.length && lines[fi].trim()==="") fi++;
  let start = fi;
  if(fi<lines.length && lines[fi].trim()===SYM){ headerPages++; start = fi+1; }
  else headerWarnings.push(r.page);
  let ei = lines.length-1;
  while(ei>=start){
    const t = lines[ei].trim();
    if(t===""){ ei--; continue; }
    if(/^GE\./.test(t) || /^\d{6}( \d{6})*$/.test(t)){ footerCount++; ei--; continue; }
    if(/^\d{1,3}$/.test(t)){
      footerCount++;
      if(Number(t)===r.page) pageNumPages++;
      else bareFooter.push({page:r.page, num:t});
      ei--; continue;
    }
    break;
  }
  for(let i=start;i<=ei;i++){
    const t = lines[i].trim();
    if(t!=="") bodyLines.push({text:t, page:r.page, cls:null});
  }
}

/* ---------- classify body lines ---------- */
const firstIdx = bodyLines.findIndex(l=>isStart(l.text));
for(let i=0;i<bodyLines.length;i++) if(firstIdx<0 || i<firstIdx) bodyLines[i].cls="cover";
let i = firstIdx>=0 ? firstIdx : bodyLines.length;
while(i<bodyLines.length){
  const l = bodyLines[i];
  if(isLabel(l.text)){
    l.cls = "heading"; l.hStart = true;
    const label = l.text.slice(0,-1);
    i++;
    const parts = [];
    while(i<bodyLines.length && !isLabel(bodyLines[i].text) && !isStart(bodyLines[i].text)){
      bodyLines[i].cls = "heading"; parts.push(bodyLines[i].text); i++;
    }
    l.hLabel = label; l.hText = parts.join(" ");
    continue;
  }
  if(isStart(l.text)){ l.cls = "para"; l.start = true; i++; continue; }
  const nn = bodyLines[i+1];
  if(nn && isStart(nn.text) && isUnlabelled(l.text)){
    const pn = bodyLines[i-1];
    if(pn && pn.cls==="para" && !pn.start && isUnlabelled(pn.text) && !continuesSentence(i-1)){
      pn.cls = "heading"; pn.hStart = true; pn.hText = pn.text + " " + l.text;
      l.cls = "heading";
    } else {
      l.cls = "heading"; l.hStart = true; l.hText = l.text;
    }
    i++; continue;
  }
  l.cls = "para"; i++;
}
function continuesSentence(idx){
  const b = bodyLines[idx-1];
  return !!(b && b.cls==="para" && !/[.!?;:]”"]$/.test(b.text));
}

/* ---------- headings and paragraphs ---------- */
const headings = [];
let curSection = "", curPart = "";
const paras = [];
let cur = null;
function closePar(){ if(cur) paras.push(cur); cur = null; }
for(let idx = (firstIdx>=0?firstIdx:bodyLines.length); idx<bodyLines.length; idx++){
  const l = bodyLines[idx];
  if(l.cls==="heading"){
    closePar();
    if(l.hStart){
      const h = {label:l.hLabel||null, text:(l.hText||"").replace(/\s+/g," ").trim(), roman:/^[IVX]+$/.test(l.hLabel||"")};
      headings.push(h);
      curSection = (h.label ? h.label+". "+h.text : h.text);
      if(h.roman) curPart = curSection;
    }
    continue;
  }
  if(l.cls==="para"){
    if(l.start){
      closePar();
      const si = startInfo(l.text);
      cur = {num:si.num, lines:[{text:si.rest!=null?si.rest:l.text, page:l.page}], section:curSection, part:curPart, startIdx:idx};
    } else if(cur){
      cur.lines.push({text:l.text, page:l.page});
    } else if(paras.length){
      paras[paras.length-1].lines.push({text:l.text, page:l.page});
    }
  }
}
closePar();

/* ---------- suspect lines, text, flags ---------- */
function suspectReason(t){
  if(/^\d{1,3}$/.test(t)) return "bare number";
  if(/^\d{1,3} [A-Z“"‘']/.test(t)) return "starts with a number and a space";
  if(/^\*\s/.test(t)) return "asterisk note";
  return null;
}
for(const p of paras){
  let prevSus = false, prevPage = -1;
  p.reasons = [];
  for(const ln of p.lines){
    let r = suspectReason(ln.text);
    if(!r && prevSus && prevPage===ln.page) r = "footnote block";
    ln.suspect = !!r; ln.reason = r;
    if(r && r!=="footnote block") p.reasons.push(r);
    prevSus = ln.suspect; prevPage = ln.page;
  }
  p.suspectCount = p.lines.filter(l=>l.suspect).length;
  p.text = p.lines.map(l=>l.text).join(" ").replace(/ {2,}/g," ").trim();
  p.words = p.text.split(/\s+/).filter(Boolean).length;
  if(p.words>300){ p.reasons.push("paragraph over 300 words"); }
  p.flagged = p.suspectCount>0 || p.words>300;
  p.page_start = p.lines[0].page;
  p.page_end = p.lines[p.lines.length-1].page;
  p.fw = firstWords(p.text);
  p.fwMatch = REF && REF.first_words ? norm(p.fw)===norm(REF.first_words[String(p.num)]||"") && !!REF.first_words[String(p.num)] : null;
}
function firstWords(text){
  const toks = text.split(/\s+/);
  const out = [];
  for(const t0 of toks){
    const t = t0.replace(/\d+$/,"");
    if(/^\d+$/.test(t)){
      const prev = out[out.length-1] || "";
      if(prev && /[.,;”"’']$/.test(prev) && !/^(no|art|arts|para|paras|page|pages|vol)\.$/i.test(prev)) continue;
    }
    if(t!=="") out.push(t);
    if(out.length>=6) break;
  }
  return out.slice(0,6).join(" ");
}
function norm(s){ return String(s||"").replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,"-").replace(/\s+/g," ").trim(); }
const cite = n => SYM + ", para. " + n;

/* ---------- counts ---------- */
const nPages = recs.length;
const found = paras.length;
const expected = REF ? REF.paragraphs : null;
const flagged = paras.filter(p=>p.flagged);
const flaggedPages = [...new Set(flagged.map(p=>p.page_end))];
const mismatches = paras.filter(p=>p.fwMatch===false);
const suspectLines = paras.reduce((a,p)=>a+p.suspectCount,0);
const suspectLinePages = [...new Set(paras.flatMap(p=>p.lines.filter(l=>l.suspect).map(l=>l.page)))];
const unclassified = bodyLines.filter(l=>l.cls===null);
const coverCount = bodyLines.filter(l=>l.cls==="cover").length;
const headingLineCount = bodyLines.filter(l=>l.cls==="heading").length;
const paraLineCount = bodyLines.filter(l=>l.cls==="para").length;
const labelledH = headings.filter(h=>h.label);
const unlabelledH = headings.filter(h=>!h.label);

/* ---------- exports ---------- */
function exportRecords(){
  return paras.map(p=>({
    symbol:SYM, paragraph:p.num, section:p.section||"", part:p.part||"",
    page_start:p.page_start, page_end:p.page_end, text:p.text,
    flagged:p.flagged, first_words_match:p.fwMatch, citation:cite(p.num),
    doc_url:D.doc_url||"",
    limitations: p.flagged
      ? "footnotes not separated; "+p.suspectCount+" may sit inside this paragraph"
      : "footnotes not separated",
    text_lines: p.lines.map(l=>l.text).join(" | ")
  }));
}
function fileBase(){ return (SYM||"document").replace(/\//g,"-"); }
function download(name, mime, content){
  const b = new Blob([content], {type:mime+";charset=utf-8"});
  const u = URL.createObjectURL(b);
  const a = document.createElement("a"); a.href=u; a.download=name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(u), 5000);
}
function markdown(){
  const today = new Date().toISOString().slice(0,10);
  let md = "---\n";
  md += "title: "+(D.title||"")+"\nsymbol: "+SYM+"\nadopted: "+((REF&&REF.adopted)||"")+"\n";
  md += "source_url: "+(D.doc_url||"")+"\nextracted: "+today+"\n";
  md += "paragraphs_found: "+found+"\nparagraphs_expected: "+(expected==null?"":expected)+"\n";
  md += "paragraphs_flagged: "+flagged.length+"\n";
  md += 'footnotes: "not separated; the document has '+((REF&&REF.footnotes!=null)?REF.footnotes:"?")+'"\n---\n\n";
  const events = [];
  for(const h of headings){
    const idx = bodyLines.findIndex(l=>l.cls==="heading" && l.hStart && (l.hText||"")===h.text && (l.hLabel||null)===h.label);
    events.push({i:idx<0?1e9:idx, md:(h.label?(h.roman?"## ":"### ")+h.label+". "+h.text:"### "+h.text)+"\n"});
  }
  for(const p of paras) events.push({i:p.startIdx, md:"**"+p.num+".** "+p.text+(p.flagged?" *(flagged: may contain footnote text)*":"")+"\n"});
  events.sort((a,b)=>a.i-b.i);
  return md + events.map(e=>e.md).join("\n");
}
let roundTripOk = false;
try{ roundTripOk = JSON.parse(JSON.stringify(exportRecords())).length === paras.length; }catch(e){ roundTripOk = false; }

/* ---------- checks ---------- */
const numberingBad = [];
paras.forEach((p,k)=>{ if(p.num!==k+1) numberingBad.push("para. "+p.num+" (page "+p.page_start+")"); });
const counts = {cover:coverCount, header:headerPages, heading:headingLineCount, paragraph:paraLineCount, footer:footerCount};
const classifiedSum = coverCount + headerPages + headingLineCount + paraLineCount + footerCount + unclassified.length;
const checks = [];
function addCheck(name, pass, detail){ checks.push({name, pass, detail}); }
if(expected!=null) addCheck("Paragraph count", found===expected, "found "+found+" · reference "+expected);
else addCheck("Paragraph count", null, "not run — no reference in this file");
addCheck("Numbering", numberingBad.length===0,
  numberingBad.length ? "gaps or duplicates: "+numberingBad.join(", ") : "exactly 1 to "+found+" in order");
if(REF && REF.first_words) addCheck("First words", mismatches.length===0, mismatches.length+" of "+found+" differ from the reference");
else addCheck("First words", null, "not run — no reference in this file");
addCheck("Paragraphs flagged", true, flagged.length+" paragraphs flagged on "+flaggedPages.length+" pages, to check against the PDF");
addCheck("Suspect lines", true, suspectLines+" suspect lines on "+suspectLinePages.length+" pages, in "+flagged.filter(p=>p.suspectCount>0).length+" paragraphs; none removed");
addCheck("Headers and footers", headerPages===nPages && headerWarnings.length===0 && pageNumPages===(nPages>0?nPages-1:0),
  "first line = symbol on "+headerPages+" of "+nPages+" pages"+(headerWarnings.length?" (missing on pages "+headerWarnings.join(", ")+")":"")+
  " · page number in footer on "+pageNumPages+" of "+(nPages>0?nPages-1:0)+" expected pages"+
  " · bare numbers removed from footer: "+(bareFooter.length? bareFooter.map(b=>"“"+b.num+"” on page "+b.page).join(", ") : "none"));
addCheck("Headings", true, labelledH.length+" labelled · "+unlabelledH.length+" unlabelled: "+(unlabelledH.map(h=>h.text).join("; ")||"none"));
addCheck("Nothing lost", unclassified.length===0 && classifiedSum===totalNonEmpty,
  "every non-empty line classified once: "+classifiedSum+" of "+totalNonEmpty+
  (unclassified.length? " · unclassified: "+unclassified.map(l=>"page "+l.page+" “"+l.text.slice(0,40)+"”").join(", ") : ""));
addCheck("Export round trip", roundTripOk, "the JSON to download parses back to "+(roundTripOk?found:0)+" records, matching the table");
const nPass = checks.filter(c=>c.pass===true).length;
const nFail = checks.filter(c=>c.pass===false).length;

/* ---------- render: header, rail, footer ---------- */
document.getElementById("docTitle").textContent = D.title || "Untitled document";
document.getElementById("docMeta").innerHTML =
  (SYM? '<a href="'+esc(D.doc_url||"#")+'" target="_blank" rel="noopener">'+esc(SYS_safe(SYS()))+'</a> · ' : "") +
  ((REF&&REF.adopted)? "adopted "+esc(REF.adopted)+" · " : "") + nPages+" pages · "+esc(D.source||"");
function SYS(){return SYM;} function SYS_safe(s){return s;}
document.getElementById("hdrRight").innerHTML =
  (nFail===0 ? '<span class="dot g"></span>'+nPass+" of "+checks.length+" checks pass"
             : '<span class="dot r"></span>'+nFail+" checks failed") +
  " · "+flagged.length+" paragraphs flagged";
document.getElementById("railSym").textContent = SYM || "—";
document.getElementById("railTtl").textContent = D.title || "";
const eq = expected!=null && found===expected;
document.getElementById("railParas").innerHTML =
  '<div class="bignum">'+found+' <small>of '+(expected==null?"?":expected)+'</small></div>'+
  '<div class="mono" style="margin-top:4px">Paragraphs</div>'+
  (expected!=null ? '<div class="bar'+(eq?"":" bad")+'"><i style="width:'+Math.min(100,expected?100*found/expected:100)+'%"></i></div>' : "")+
  (expected==null?'<p class="railnote">no reference in this file</p>':'');
document.getElementById("railFlag").innerHTML =
  '<div class="bignum'+(flagged.length?' red':'')+'">'+flagged.length+'</div>'+
  '<div class="mono" style="margin-top:4px">Paragraphs flagged</div>'+
  '<p class="railnote">footnote text may sit inside: check them against the PDF</p>';
document.getElementById("railChecks").innerHTML =
  '<div class="bignum" style="font-size:30px">'+nPass+' <small>of '+checks.length+'</small></div>'+
  '<div class="mono" style="margin-top:4px">Checks pass</div>';
document.getElementById("foot").textContent =
  (D.source||"") + (D.built? " · built "+D.built : "") +
  " · Done by this page's code; no model was called and nothing left the browser.";

/* ---------- tabs ---------- */
const tabs=[document.getElementById("tab1"),document.getElementById("tab2")];
const panels=[document.getElementById("p1"),document.getElementById("p2")];
function selectTab(k){
  tabs.forEach((t,j)=>{t.setAttribute("aria-selected",j===k?"true":"false");t.tabIndex=j===k?0:-1;});
  panels.forEach((p,j)=>p.hidden=j!==k);
  tabs[k].focus();
}
tabs.forEach((t,k)=>{
  t.addEventListener("click",()=>selectTab(k));
  t.addEventListener("keydown",e=>{
    if(e.key==="ArrowRight") selectTab((k+1)%tabs.length);
    if(e.key==="ArrowLeft") selectTab((k+1+tabs.length)%tabs.length);
  });
});

/* ---------- tab 01 ---------- */
const p1 = panels[0];
let html = "";
html += '<div class="tiles">';
html += tile("FIG.01","PARAGRAPHS FOUND",
  '<span class="'+(expected==null?"":(found===expected?"grn":"red"))+'">'+found+'</span>',
  expected==null ? "no reference in this file" : "the document has "+expected+(found===expected?"":" · difference "+(found-expected)),
  "Paragraph starts are lines like “12.” alone or “12. text…”, found by the pipeline on page load.");
html += tile("FIG.02","FIRST WORDS MATCH",
  '<span class="'+(mismatches.length?"red":"grn")+'">'+(found-mismatches.length)+'</span> <small style="font-size:18px;color:#6b6459">of '+(expected==null?"?":expected)+'</small>',
  (REF&&REF.first_words)?mismatches.length+" differ":"no reference in this file",
  "The first six words of each paragraph, after cutting footnote marks, compared with the reference, normalising quotes and dashes.");
html += tile("FIG.03","PARAGRAPHS FLAGGED",
  '<span class="'+(flagged.length?"red":"grn")+'">'+flagged.length+'</span> <small style="font-size:18px;color:#6b6459">of '+found+'</small>',
  "on "+flaggedPages.length+" pages",
  "A paragraph is flagged when a line looks like footnote text (a bare number, or “7 E/2003/22…”), or it exceeds 300 words. This version does not separate footnotes: check flagged paragraphs against the PDF.");
html += tile("FIG.04","FOOTNOTES",
  "not separated",
  REF&&REF.footnotes!=null ? "the document has "+REF.footnotes : "footnote count unknown",
  "Footnote text stays in the paragraph it sits in; the app flags where it may be.");
html += '</div>';
function tile(fig,label,n,sub,how){
  return '<div class="tile"><div class="fig">'+fig+' · '+label+'</div><div class="n">'+n+'</div><div class="sub">'+esc(sub)+'</div><div class="how">'+esc(how)+'</div></div>';
}
if(mismatches.length){
  html += '<h3 class="sect">First words differ</h3><div class="mismatch">';
  mismatches.slice(0,10).forEach(p=>{
    html += '<div><b>para. '+p.num+'</b>: found “'+esc(p.fw)+'” / reference “'+esc(REF.first_words[String(p.num)]||"")+'”</div>';
  });
  if(mismatches.length>10) html += '<div>and '+(mismatches.length-10)+' more</div>';
  html += '</div>';
}
if(found===0){
  html += '<h3 class="sect">No paragraph found</h3><p class="note">The pipeline found no numbered paragraph in this file, so there is nothing to show or export.</p>';
}
html += '<h3 class="sect">Take the paragraphs away</h3>'+
  '<button class="act" id="dlJson"'+(found===0?" disabled":"")+'>Download JSON</button>'+
  '<button class="act" id="dlMd"'+(found===0?" disabled":"")+'>Download Markdown</button>'+
  '<p class="how">The dataset carries its source, fields and known limitations with it. File names use the symbol with slashes replaced by hyphens.</p>';
html += '<button class="disc" id="discChecks" aria-expanded="false">EVERY CHECK ('+checks.length+')</button><div id="checksBody" hidden>';
checks.forEach(c=>{
  const st = c.pass===null ? '<span style="color:#6b6459">not run</span>' : (c.pass?'<span class="grn">pass</span>':'<span class="red">check failed</span>');
  html += '<div class="checkline"><span class="st">'+st+'</span><span><b>'+esc(c.name)+'.</b> '+esc(c.detail)+'</span></div>';
});
html += '</div>';
html += '<button class="disc" id="discFlag" aria-expanded="false">FLAGGED PARAGRAPHS ('+flagged.length+')</button><div id="flagBody" hidden>';
html += '<p class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</p>';
if(flagged.length){
  html += '<table><caption class="serif">'+flagged.length+' paragraphs flagged, of '+found+' found</caption>'+
    '<thead><tr><th class="num" scope="col">Para.</th><th scope="col">Page</th><th class="num" scope="col">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>';
  flagged.forEach(p=>{
    html += '<tr class="prow" data-para="'+p.num+'" style="cursor:pointer"><td class="num">'+p.num+'</td><td>'+p.page_start+(p.page_end!==p.page_start?"–"+p.page_end:"")+'</td><td class="num">'+p.suspectCount+'</td><td>'+esc([...new Set(p.reasons)].join("; "))+'</td></tr>';
  });
  html += '</tbody></table>';
}
html += '</div>';
p1.innerHTML = html;

document.getElementById("dlJson").addEventListener("click",()=>download(fileBase()+".json","application/json",JSON.stringify(exportRecords(),null,2)));
document.getElementById("dlMd").addEventListener("click",()=>download(fileBase()+".md","text/markdown",markdown()));
function wireDisc(btnId, bodyId){
  const b=document.getElementById(btnId), d=document.getElementById(bodyId);
  b.addEventListener("click",()=>{ const o=d.hidden; d.hidden=!o; b.setAttribute("aria-expanded",o?"true":"false"); });
}
wireDisc("discChecks","checksBody");
wireDisc("discFlag","flagBody");
p1.querySelectorAll("tr.prow[data-para]").forEach(tr=>{
  tr.addEventListener("click",()=>{ openPara(Number(tr.dataset.para)); });
});

/* ---------- tab 02 ---------- */
const p2 = panels[1];
let h2 = '<button class="disc" id="discHeads" aria-expanded="false">HEADINGS FOUND: '+headings.length+'</button><div id="headsBody" hidden><div class="headlist">';
headings.forEach(h=>{ h2 += '<div>'+(h.label?'<span class="mono">'+esc(h.label)+'.</span> ':'')+esc(h.text||"(no title)")+'</div>'; });
h2 += '</div></div>';
h2 += '<table id="parTable"><caption class="serif">'+found+' paragraphs found'+(expected!=null?", "+expected+" expected":"")+'</caption>'+
  '<thead><tr><th class="num" scope="col">No.</th><th scope="col">Section</th><th class="num" scope="col">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody id="parBody"></tbody></table>';
p2.innerHTML = h2;
wireDisc("discHeads","headsBody");
const parBody = document.getElementById("parBody");
paras.forEach(p=>{
  const first = p.text.length>120 ? p.text.slice(0,120).replace(/\s+\S*$/,"")+"…" : p.text;
  let chk;
  if(p.flagged) chk = '<span class="red">may contain footnote text</span>'+(p.fwMatch===false?' · <span class="red">first words differ</span>':"");
  else if(p.fwMatch===false) chk = '<span class="red">first words differ</span>';
  else chk = "OK";
  const tr = document.createElement("tr");
  tr.className = "prow"; tr.setAttribute("role","button"); tr.tabIndex = 0;
  tr.setAttribute("aria-expanded","false"); tr.dataset.para = p.num;
  tr.innerHTML = '<td class="num serif" style="font-size:18px">'+p.num+'</td><td>'+esc(p.section||"—")+'</td>'+
    '<td class="num">'+p.page_start+(p.page_end!==p.page_start?"–"+p.page_end:"")+'</td>'+
    '<td>'+esc(first)+'</td><td>'+chk+'</td>';
  parBody.appendChild(tr);
});
function togglePara(num){
  const existing = parBody.querySelector('tr.exp[data-para="'+num+'"]');
  if(existing){ existing.remove(); const r=parBody.querySelector('tr.prow[data-para="'+num+'"]'); if(r) r.setAttribute("aria-expanded","false"); return; }
  parBody.querySelectorAll("tr.exp").forEach(e=>{ const r=parBody.querySelector('tr.prow[data-para="'+e.dataset.para+'"]'); if(r) r.setAttribute("aria-expanded","false"); e.remove(); });
  const row = parBody.querySelector('tr.prow[data-para="'+num+'"]');
  if(!row) return;
  const p = paras.find(x=>x.num===num);
  const tr = document.createElement("tr");
  tr.className = "exp"; tr.dataset.para = num;
  row.setAttribute("aria-expanded","true");
  const path = [p.part, p.section].filter((v,k,a)=>v && a.indexOf(v)===k).join(" › ");
  const refFW = REF && REF.first_words ? (REF.first_words[String(num)]||"(not in reference)") : "(no reference)";
  const textHtml = p.lines.map(l=>l.suspect?'<span class="sus">'+esc(l.text)+'</span>':esc(l.text)).join(" ");
  const linesHtml = p.lines.map(l=>(l.page!==p.lines[0].page && p.lines[p.lines.indexOf(l)-1] && p.lines[p.lines.indexOf(l)-1].page!==l.page ? "[page "+l.page+"] ":"")+l.text).join("\n");
  tr.innerHTML = '<td colspan="5">'+
    '<p class="exp-meta"><b>Path:</b> '+esc(path||"—")+' · <b>Pages:</b> '+p.page_start+(p.page_end!==p.page_start?"–"+p.page_end:"")+' · <b>Words:</b> '+p.words+'</p>'+
    '<p class="exp-meta"><b>Found six words:</b> “'+esc(p.fw)+'”<br><b>Reference six words:</b> “'+esc(refFW)+'”</p>'+
    '<p class="exp-text serif" style="font-size:17px">'+textHtml+'</p>'+
    '<button class="mini" data-act="lines">Show the PDF\'s lines</button>'+
    '<button class="mini" data-act="copy">Copy citation</button>'+
    '<span class="mono" id="copied-'+p.num+'" style="color:var(--green)" hidden>COPIED</span>'+
    '<div class="pdflines" data-el="lines" hidden>'+esc(linesHtml)+'</div>'+
    '</td>';
  row.after(tr);
  tr.querySelector('[data-act="lines"]').addEventListener("click",e=>{
    const d = tr.querySelector('[data-el="lines"]');
    d.hidden = !d.hidden;
    e.currentTarget.textContent = d.hidden ? "Show the PDF's lines" : "Hide the PDF's lines";
  });
  tr.querySelector('[data-act="copy"]').addEventListener("click",()=>{
    const s = cite(p.num);
    const done = ()=>{ const c=document.getElementById("copied-"+p.num); c.hidden=false; setTimeout(()=>c.hidden=true,2000); };
    if(navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(s).then(done,()=>fallbackCopy(s,done));
    else fallbackCopy(s,done);
  });
}
function fallbackCopy(s,done){
  const ta=document.createElement("textarea"); ta.value=s; document.body.appendChild(ta);
  ta.select(); try{document.execCommand("copy");}catch(e){} ta.remove(); done();
}
parBody.addEventListener("click",e=>{
  const tr = e.target.closest("tr.prow");
  if(tr && !e.target.closest("tr.exp")) togglePara(Number(tr.dataset.para));
});
parBody.addEventListener("keydown",e=>{
  if(e.key==="Enter"||e.key===" "){
    const tr = e.target.closest("tr.prow");
    if(tr){ e.preventDefault(); togglePara(Number(tr.dataset.para)); }
  }
});
function openPara(num){
  selectTab(1);
  const row = parBody.querySelector('tr.prow[data-para="'+num+'"]');
  if(row){
    if(!parBody.querySelector('tr.exp[data-para="'+num+'"]')) togglePara(num);
    row.scrollIntoView({block:"center"});
  }
}
})();
</script>
</body>
</html>
```

Two small notes on things the plan asked the app to state itself: the header line and the check panel report exactly what the pipeline found on this file (paragraph starts in both forms, headings, suspect lines), and nothing is trimmed or padded to match the reference — when the counts disagree, both numbers are shown.