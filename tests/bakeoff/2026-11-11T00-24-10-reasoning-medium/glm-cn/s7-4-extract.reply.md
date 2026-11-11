Built as planned: one document in, the pipeline runs once on load, and everything on screen — tiles, checks, flags, exports — is computed by the page's own code from `WORKSHOP_DATA.pdf_text`.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b3a;}
*{box-sizing:border-box;}
[hidden]{display:none!important;}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;}
a{color:var(--red);}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;}
header.site{padding:18px 28px 14px;border-bottom:1px solid var(--rule);display:flex;justify-content:space-between;gap:24px;align-items:flex-end;flex-wrap:wrap;}
header.site h1{font-family:Georgia,"Times New Roman",serif;font-size:26px;font-weight:normal;margin:4px 0 6px;}
.meta{font-size:14px;color:#4c463d;}
.meta a{text-decoration:none;border-bottom:1px solid var(--rule);}
.hdr-right{text-align:right;font-size:14px;}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline;}
.dot.ok{background:var(--green);} .dot.bad{background:var(--red);}
nav.tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);padding:0 28px;}
nav.tabs button{background:none;border:none;border-bottom:3px solid transparent;padding:10px 18px 8px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.1em;color:#4c463d;}
nav.tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red);}
nav.tabs button:focus-visible,button:focus-visible,tr:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--red);outline-offset:2px;}
.layout{display:flex;min-height:60vh;}
aside.rail{width:250px;flex:none;border-right:1px solid var(--rule);padding:22px 20px;}
main{flex:1;padding:26px 32px;max-width:980px;}
.doccard{border:1px solid var(--rule);padding:12px 14px;margin-bottom:22px;}
.doccard .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;}
.doccard .t{font-size:13px;color:#4c463d;margin-top:4px;}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:44px;line-height:1.05;margin:18px 0 2px;}
.bignum small{font-size:16px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#4c463d;}
.bignum.red{color:var(--red);}
.bar{height:3px;background:var(--rule);margin:6px 0 2px;}
.bar i{display:block;height:3px;background:var(--ink);}
.bar.bad i{background:var(--red);}
.railnote{font-size:12.5px;color:#4c463d;margin-bottom:8px;}
.railnote.red{color:var(--red);}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:22px;margin-bottom:8px;}
.tile{border-top:1px solid var(--rule);padding-top:10px;}
.tile .n{font-family:Georgia,"Times New Roman",serif;font-size:48px;line-height:1;}
.tile .n.red{color:var(--red);} .tile .n .exp{font-size:20px;color:#4c463d;}
.tile .lbl{margin-top:6px;font-weight:600;}
.how{font-size:12.5px;color:#4c463d;margin-top:4px;}
.mismatch{margin:18px 0;font-size:14px;}
.mismatch div{padding:3px 0;border-bottom:1px dotted var(--rule);}
.mismatch b{color:var(--red);}
.takeaway{margin:26px 0 8px;border-top:1px solid var(--rule);padding-top:14px;}
.btnrow{display:flex;gap:12px;margin:10px 0 26px;flex-wrap:wrap;}
button.download{background:var(--ink);color:var(--paper);border:none;padding:9px 18px;cursor:pointer;font-size:14px;font-family:inherit;}
button.download:disabled{background:#a39c8d;cursor:not-allowed;}
button.plain{background:none;border:none;border-bottom:1px solid var(--rule);padding:2px 0;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);}
details-like{display:block;}
.checkpanel,.flagpanel{border-top:1px solid var(--rule);margin-top:18px;padding-top:10px;}
.checkline{font-size:14px;padding:5px 0;border-bottom:1px dotted var(--rule);display:flex;gap:10px;flex-wrap:wrap;}
.pass{color:var(--green);font-weight:600;} .fail{color:var(--red);font-weight:600;} .notrun{color:#7a7263;}
table{border-collapse:collapse;width:100%;margin:10px 0 20px;font-size:14.5px;}
caption{font-family:Georgia,"Times New Roman",serif;font-size:18px;text-align:left;padding-bottom:8px;}
caption .mono{display:block;margin-bottom:2px;color:#7a7263;}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:1px solid var(--rule);padding:6px 10px 6px 0;font-weight:normal;color:#4c463d;}
td{border-bottom:1px solid var(--rule);padding:7px 10px 7px 0;vertical-align:top;}
th.num,td.num{text-align:right;}
td.pno{font-family:Georgia,serif;color:var(--red);text-align:right;}
tr.main{cursor:pointer;}
tr.main:hover{background:#ece6d9;}
tr.detail td{background:#fbf8f1;border-bottom:1px solid var(--rule);}
.ptext{margin:4px 0 10px;}
.sl{border:1px solid var(--red);padding:0 2px;}
.cite{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;}
button.copy{background:none;border:1px solid var(--rule);padding:4px 10px;cursor:pointer;font-size:13px;font-family:inherit;}
.fw{font-size:13px;color:#4c463d;margin:8px 0;}
.fw b{color:var(--ink);font-weight:600;}
.pdf-lines{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;white-space:pre-wrap;background:#f0ebdf;border:1px solid var(--rule);padding:10px 12px;margin:10px 0;}
.pagemark{color:var(--red);}
.flag-table tr.main{cursor:pointer;}
.suspect-list{font-size:13px;}
.suspect-list .sl{margin-right:6px;}
.why{font-size:13px;}
.note{font-size:13.5px;color:#4c463d;margin:8px 0;}
.headings-list{font-size:14px;margin:10px 0 0;}
.headings-list div{padding:2px 0;}
.headings-list .k{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;color:#7a7263;margin-right:8px;}
footer.site{border-top:1px solid var(--rule);padding:14px 28px;font-size:13px;color:#4c463d;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;}
.section-path{font-size:13px;color:#4c463d;}
@media(max-width:800px){.layout{flex-direction:column;}aside.rail{width:auto;border-right:none;border-bottom:1px solid var(--rule);}}
</style>
</head>
<body>

<header class="site">
  <div>
    <div class="mono" style="color:#7a7263">UN DOCUMENT · PDF TEXT</div>
    <h1 id="doc-title"></h1>
    <div class="meta" id="doc-meta"></div>
  </div>
  <div class="hdr-right" id="hdr-checks"></div>
</header>

<nav class="tabs" role="tablist" aria-label="Sections">
  <button role="tab" id="tab1" aria-controls="panel-result" aria-selected="true">01 RESULT</button>
  <button role="tab" id="tab2" aria-controls="panel-paras" aria-selected="false" tabindex="-1">02 PARAGRAPHS</button>
</nav>

<div class="layout">
  <aside class="rail" id="rail"></aside>
  <main>
    <section id="panel-result" role="tabpanel" aria-labelledby="tab1"></section>
    <section id="panel-paras" role="tabpanel" aria-labelledby="tab2" hidden></section>
  </main>
</div>

<footer class="site" id="foot"></footer>

<script>
(function(){
"use strict";
const D = window.WORKSHOP_DATA && window.WORKSHOP_DATA.pdf_text;
if(!D || !D.records || !D.records.length){
  document.getElementById('doc-title').textContent='No document loaded';
  return;
}
const SYM = D.symbol || '';
const REF = D.reference || null;
const pages = D.records.slice().sort((a,b)=>a.page-b.page);
const esc = s => String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const norm = s => String(s||'').replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ').trim();

/* ---------- pipeline ---------- */
const labelRe = /^([IVX]+|[A-Z])\.$/;
const pAlone  = /^(\d{1,3})\.$/;
const pInline = /^(\d{1,3})\. (.+)$/;
const isPS = t => pAlone.test(t) || pInline.test(t);

let headerOkPages = 0, headerWarnPages = [];
let pagesWithPageNum = 0, footerBares = [];           // {page, n}
const body = [];                                       // {text, page}
let hyphenEndings = 0;

for(const pg of pages){
  const L = pg.text.split('\n').map(s=>s.trim());
  let hi = -1;
  for(let i=0;i<L.length;i++){ if(L[i]){hi=i;break;} }
  if(hi>=0 && L[hi]===SYM){ headerOkPages++; } else { headerWarnPages.push(pg.page); }
  // footer scan from the end
  let pageNum = false;
  let i = L.length-1;
  while(i>hi){
    const s = L[i];
    if(!s){ i--; continue; }
    if(s.indexOf('GE.')===0){ i--; continue; }
    if(/^\d{6}(\s+\d{6})*$/.test(s)){ i--; continue; }         // date stamp
    if(/^\d{1,3}$/.test(s)){
      if(Number(s)===pg.page){ pageNum = true; } else { footerBares.push({page:pg.page, n:Number(s)}); }
      i--; continue;
    }
    break;
  }
  if(pageNum) pagesWithPageNum++;
  for(let k=hi+1;k<=i;k++){
    if(!L[k]) continue;
    if(/-$/.test(L[k])) hyphenEndings++;
    body.push({text:L[k], page:pg.page});
  }
}

const N = body.length;
const psIdx=new Array(N).fill(false), labIdx=new Array(N).fill(false), unlabIdx=new Array(N).fill(false);
for(let i=0;i<N;i++){
  const t=body[i].text;
  if(isPS(t)) psIdx[i]=true;
  else if(labelRe.test(t)) labIdx[i]=true;
}
const looksHeading = t => !!t && t.length<=90 && /^[A-Z]/.test(t) && !/[.;:,\u2026]$/.test(t) && !/\d$/.test(t);
for(let i=0;i<N;i++){
  const t=body[i].text;
  if(!t || psIdx[i] || labIdx[i]) continue;
  const nx = body[i+1] && body[i+1].text;
  if(nx && isPS(nx) && looksHeading(t)) unlabIdx[i]=true;
}
// heading spans
const spans=[];
for(let i=0;i<N;i++){
  const t=body[i].text;
  if(labIdx[i]){
    const kind = /^[IVX]+\.$/.test(t) ? 'roman' : 'letter';
    let j=i+1, txt=[];
    while(j<N){
      const s=body[j].text;
      if(!s){ j++; continue; }
      if(psIdx[j]||labIdx[j]||unlabIdx[j]) break;
      txt.push(s); j++;
    }
    spans.push({start:i, end:j-1, kind, text:(txt.join(' ')||t)});
  } else if(unlabIdx[i]){
    let start=i;
    let j=i-1; while(j>=0 && !body[j].text) j--;
    if(j>=0 && !psIdx[j] && !labIdx[j] && !unlabIdx[j] && looksHeading(body[j].text) && !/[.!?]$/.test(body[j].text)) start=j;
    spans.push({start, end:i, kind:'unlabelled', text: body.slice(start,i+1).map(x=>x.text).filter(Boolean).join(' ')});
  }
}
const inSpan={};
spans.forEach(s=>{ for(let k=s.start;k<=s.end;k++) inSpan[k]=s; });

let firstSpecial = N;
for(let i=0;i<N;i++){ if(body[i].text && (psIdx[i]||labIdx[i]||unlabIdx[i])){ firstSpecial=i; break; } }

// main walk
let cur=null, curHead=null, curPart=null, coverCount=0;
const paragraphs=[];
for(let i=0;i<N;i++){
  const t=body[i].text;
  if(!t) continue;
  if(inSpan[i]){
    const s=inSpan[i];
    if(i===s.start){
      if(s.kind==='roman') curPart=s;
      curHead=s;
      if(s.kind==='unlabelled' && s.start<s.end && cur && cur.lines.length){
        const pl=cur.lines[cur.lines.length-1];
        if(pl && pl.text===body[s.start].text && pl.page===body[s.start].page) cur.lines.pop();
      }
    }
    continue;
  }
  if(psIdx[i]){
    if(cur) paragraphs.push(cur);
    const m=t.match(pInline);
    cur={num:Number(t.match(/^(\d{1,3})\./)[1]), startIdx:i, lines:[], section:curHead?curHead.text:null, part:curPart?curPart.text:null};
    if(m) cur.lines.push({text:m[2], page:body[i].page});
    continue;
  }
  if(i<firstSpecial || !cur){ coverCount++; continue; }
  cur.lines.push({text:t, page:body[i].page});
}
if(cur) paragraphs.push(cur);

// suspect lines
const suspectLine = t =>
  /^\d{1,3}$/.test(t) ? 'bare number' :
  /^\d{1,3}\s+[A-Z\u201C"']/.test(t) ? 'starts with a number and a space' :
  /^[A-Z]{1,4}\/[A-Z0-9]/.test(t) ? 'starts with a document symbol or quotation mark' :
  (/^\*\s/.test(t) ? 'asterisk note' : null);

for(const p of paragraphs){
  let contPage=null;
  for(const ln of p.lines){
    if(contPage!==null){
      if(ln.page===contPage){ ln.suspect=true; ln.why='footnote block (after a suspect line)'; }
      else contPage=null;
    }
    if(!ln.suspect){
      const w=suspectLine(ln.text);
      if(w){ ln.suspect=true; ln.why=w; contPage=ln.page; }
    }
  }
  p.text = p.lines.map(l=>l.text).join(' ').replace(/  +/g,' ').trim();
  p.text_lines = p.lines.map(l=>l.text).join(' | ');
  p.page_start = p.lines.length? p.lines[0].page : null;
  p.page_end   = p.lines.length? p.lines[p.lines.length-1].page : null;
  p.wordCount = p.text.split(/\s+/).filter(Boolean).length;
  p.flagged = p.lines.some(l=>l.suspect) || p.wordCount>300;
  p.reasons = [...new Set(p.lines.filter(l=>l.suspect).map(l=>l.why))];
  if(p.wordCount>300) p.reasons.push('paragraph over 300 words');
}

// first words
function firstWords(text){
  const toks=text.split(/\s+/).filter(Boolean);
  const out=[];
  for(let k=0;k<toks.length && out.length<6;k++){
    let w=toks[k].replace(/\d+([.,;:]?)$/,'$1');
    if(/^\d+$/.test(w)){
      const prevRaw = out.length ? out[out.length-1] : (k>0?toks[k-1]:null);
      if(prevRaw && /[.,\u2019\u201D"]$/.test(prevRaw) && !/\b(No|art|para|Vol|p)\.$/.test(prevRaw)) continue;
    }
    if(w) out.push(w);
  }
  return out.join(' ');
}
for(const p of paragraphs){
  p.fw = firstWords(p.text);
  const refw = REF && REF.first_words ? REF.first_words[String(p.num)] : null;
  p.first_words_match = refw==null ? null : norm(p.fw)===norm(refw);
  p.ref_fw = refw;
}
const fwMismatch = paragraphs.filter(p=>p.first_words_match===false);

// numbering check
const nums = paragraphs.map(p=>p.num);
const gaps=[], dups=[];
{
  const seen={};
  nums.forEach(n=>{ seen[n]=(seen[n]||0)+1; });
  Object.keys(seen).forEach(k=>{ if(seen[k]>1) dups.push(k); });
  const max = nums.length? Math.max(...nums):0;
  for(let n=1;n<=max;n++) if(!seen[n]) gaps.push(n);
  const sortedOk = nums.every((n,i)=>n===nums[0]+i);
  if(!sortedOk && !gaps.length && !dups.length) gaps.push('out of order');
}
const numberingOk = gaps.length===0 && dups.length===0 && nums.length===(nums.length?Math.max(...nums)-Math.min(...nums)+1:0) && nums.every((n,i)=>i===0||n>nums[i-1]);

// nothing lost
const headerLines = headerOkPages + headerWarnPages.length;
const footerLineCount = (()=>{ // recompute count of removed footer lines
  let c=0;
  for(const pg of pages){
    const L=pg.text.split('\n').map(s=>s.trim());
    let hi=-1; for(let i=0;i<L.length;i++){ if(L[i]){hi=i;break;} }
    let i=L.length-1;
    while(i>hi){
      const s=L[i];
      if(!s){i--;continue;}
      if(s.indexOf('GE.')===0){c++;i--;continue;}
      if(/^\d{6}(\s+\d{6})*$/.test(s)){c++;i--;continue;}
      if(/^\d{1,3}$/.test(s)){c++;i--;continue;}
      break;
    }
  }
  return c;
})();
const spanLineCount = spans.reduce((a,s)=>a+(s.end-s.start+1),0);
const paraLineCount = paragraphs.reduce((a,p)=>a+p.lines.length,0);
const totalNonEmpty = pages.reduce((a,pg)=>a+pg.text.split('\n').filter(s=>s.trim()).length,0);
const classified = headerLines + footerLineCount + spanLineCount + paraLineCount + coverCount;
const unclassified = totalNonEmpty - classified;

// export records
const today = new Date().toISOString().slice(0,10);
const records = paragraphs.map(p=>({
  symbol:SYM, paragraph:p.num, section:p.section, part:p.part,
  page_start:p.page_start, page_end:p.page_end, text:p.text, text_lines:p.text_lines,
  flagged:p.flagged, first_words_match:p.first_words_match,
  citation: SYM + ', para. ' + p.num, doc_url:D.doc_url||'',
  limitations: p.flagged ? ('footnotes not separated; ' + (p.lines.some(l=>l.suspect)? p.lines.filter(l=>l.suspect).length + ' suspect line(s) may sit inside this paragraph' : 'over 300 words')) : 'footnotes not separated'
}));
const jsonString = JSON.stringify(records, null, 2);
let roundTripOk = false;
try{ roundTripOk = JSON.parse(jsonString).length === paragraphs.length; }catch(e){ roundTripOk=false; }

const flagged = paragraphs.filter(p=>p.flagged);
const flaggedPages = [...new Set(flagged.map(p=>p.page_start))];
const suspectLinesAll = paragraphs.flatMap(p=>p.lines.filter(l=>l.suspect).map(l=>({p:p.num, line:l})));
const suspectPages = [...new Set(suspectLinesAll.map(s=>s.line.page))];
const labelledH = spans.filter(s=>s.kind!=='unlabelled');
const unlabH = spans.filter(s=>s.kind==='unlabelled');
const hasRef = !!REF && REF.paragraphs!=null;

/* ---------- checks ---------- */
const checks=[];
const addC=(name, detail, pass)=>checks.push({name, detail, pass});
if(hasRef){
  addC('Paragraph count', paragraphs.length+' found · '+REF.paragraphs+' in the reference', paragraphs.length===REF.paragraphs);
} else addC('Paragraph count', paragraphs.length+' found · no reference in this file', null);
addC('Numbering', numberingOk ? 'exactly 1 to '+nums.length+' in order' : ('gaps: '+(gaps.join(', ')||'none')+' · duplicates: '+(dups.join(', ')||'none')), numberingOk);
if(hasRef && REF.first_words){
  addC('First words', fwMismatch.length+' of '+REF.paragraphs+' differ from the reference', fwMismatch.length===0);
} else addC('First words','not run · no reference first words',null);
addC('Paragraphs flagged', flagged.length+' paragraphs flagged on '+flaggedPages.length+' pages, to check against the PDF (a flag is not a failure)', true);
addC('Suspect lines', suspectLinesAll.length+' suspect lines on '+suspectPages.length+' pages, in '+new Set(suspectLinesAll.map(s=>s.p)).size+' paragraphs; none removed', true);
addC('Page headers', headerOkPages+' of '+pages.length+' pages open with the symbol '+SYM, headerOkPages===pages.length);
addC('Page footers', pagesWithPageNum+' of '+(pages.length-1)+' pages after the first carry their page number'+(footerBares.length?' · bare numbers removed from the footer: '+footerBares.map(b=>'p.'+b.page+' ('+b.n+')').join(', '):''), pagesWithPageNum===(pages.length-1));
addC('Headings', labelledH.length+' labelled ('+spans.filter(s=>s.kind==='roman').length+' roman, '+spans.filter(s=>s.kind==='letter').length+' letter) and '+unlabH.length+' unlabelled found; unlabelled: '+(unlabH.map(h=>esc(h.text)).join(' · ')||'none'), true);
addC('Nothing lost', 'every non-empty line classified: '+headerLines+' header, '+footerLineCount+' footer, '+spanLineCount+' heading, '+paraLineCount+' paragraph, '+coverCount+' cover = '+classified+' of '+totalNonEmpty+(hyphenEndings?' · '+hyphenEndings+' lines end with a hyphen (none joined)':''), unclassified===0);
addC('Export round trip', 'the JSON to download parses back to '+records.length+' records, the table shows '+paragraphs.length, roundTripOk && records.length===paragraphs.length);

const runChecks = checks.filter(c=>c.pass!==null);
const passCount = runChecks.filter(c=>c.pass).length;
const failCount = runChecks.length - passCount;

/* ---------- header / rail / footer ---------- */
document.getElementById('doc-title').textContent = D.title || SYM;
document.getElementById('doc-meta').innerHTML =
  (D.doc_url ? '<a href="'+esc(D.doc_url)+'" target="_blank" rel="noopener">'+esc(SYM)+'</a>' : esc(SYM)) +
  (REF && REF.adopted ? ' · adopted '+esc(REF.adopted) : '') +
  ' · '+pages.length+' pages · '+esc(D.source||'');
document.getElementById('hdr-checks').innerHTML =
  (failCount ? '<span class="dot bad"></span>'+failCount+' checks failed' : '<span class="dot ok"></span>'+passCount+' of '+runChecks.length+' checks pass') +
  ' · <span style="color:var(--red)">'+flagged.length+' paragraphs flagged</span>';

const expP = hasRef ? REF.paragraphs : null;
const barW = expP ? Math.min(100, Math.round(paragraphs.length/expP*100)) : 0;
document.getElementById('rail').innerHTML =
 '<div class="mono" style="color:#7a7263">DOCUMENT</div>'+
 '<div class="doccard"><div class="sym">'+esc(SYM)+'</div><div class="t">'+esc(D.title||'')+'</div></div>'+
 '<div class="bignum'+(expP!=null&&paragraphs.length!==expP?' red':'')+'">'+paragraphs.length+' <small>paragraphs'+(expP!=null?' of '+expP:'')+'</small></div>'+
 (expP!=null?'<div class="bar'+(paragraphs.length!==expP?' bad':'')+'"><i style="width:'+barW+'%"></i></div>':'')+
 '<div class="railnote">'+(expP==null?'no reference in this file':(paragraphs.length===expP?'all numbered paragraphs found':'short or over: both counts shown, nothing trimmed or padded'))+'</div>'+
 '<div class="bignum red">'+flagged.length+'</div>'+
 '<div class="railnote'+(flagged.length?' red':'')+'">paragraphs flagged'+(flagged.length?' — footnote text may sit inside: check them against the PDF':'')+'</div>'+
 '<div class="railnote" style="margin-top:18px;border-top:1px solid var(--rule);padding-top:10px">'+(failCount?'<span class="fail">'+failCount+' checks failed</span>':'<span class="pass">'+passCount+' of '+runChecks.length+' checks pass</span>')+'</div>';

document.getElementById('foot').innerHTML =
 '<span>'+esc(D.source||'')+(D.built?' · built '+esc(D.built):'')+'</span>'+
 '<span>Done by this page\u2019s code; no model was called and nothing left the browser.</span>';

/* ---------- tabs ---------- */
const tab1=document.getElementById('tab1'), tab2=document.getElementById('tab2');
const panel1=document.getElementById('panel-result'), panel2=document.getElementById('panel-paras');
function selectTab(which){
  const on = which===1;
  tab1.setAttribute('aria-selected', on); tab2.setAttribute('aria-selected', !on);
  tab1.tabIndex = on?0:-1; tab2.tabIndex = on?-1:0;
  panel1.hidden=!on; panel2.hidden=on;
  if(on) tab1.focus(); else tab2.focus();
}
tab1.addEventListener('click',()=>selectTab(1));
tab2.addEventListener('click',()=>selectTab(2));
document.querySelector('nav.tabs').addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'){e.preventDefault();selectTab(2);}
  if(e.key==='ArrowLeft'){e.preventDefault();selectTab(1);}
});

/* ---------- tab 01 ---------- */
const mismList = fwMismatch.length ?
  '<div class="mismatch">'+fwMismatch.slice(0,10).map(p=>
    '<div>para. '+p.num+': <b>found</b> '+esc(p.fw)+' / <b>reference</b> '+esc(p.ref_fw||'')+'</div>').join('')+
    (fwMismatch.length>10?'<div>and '+(fwMismatch.length-10)+' more</div>':'')+'</div>' : '';

const noPara = paragraphs.length===0;

panel1.innerHTML =
 '<div class="tiles">'+
  '<div class="tile"><div class="n'+(expP!=null&&paragraphs.length!==expP?' red':'')+'">'+paragraphs.length+(expP!=null?' <span class="exp">/ '+expP+'</span>':'')+'</div>'+
   '<div class="lbl">Paragraphs found</div><div class="how">How this is computed: lines starting a numbered paragraph, both forms (number alone, number with text).'+(expP==null?' No reference in this file.':(paragraphs.length===expP?' Equal to the document\u2019s count.':' Difference: '+(paragraphs.length-expP)+'.'))+'</div></div>'+
  '<div class="tile"><div class="n'+(fwMismatch.length?' red':'')+'">'+(hasRef&&REF.first_words?(REF.paragraphs-fwMismatch.length):(hasRef?0:'—'))+(hasRef?' <span class="exp">of '+REF.paragraphs+'</span>':'')+'</div>'+
   '<div class="lbl">First words match</div><div class="how">How this is computed: the first six words of each paragraph, footnote marks removed, against the reference, after normalising quotes and dashes.'+(hasRef?'':' No reference in this file.')+'</div></div>'+
  '<div class="tile"><div class="n'+(flagged.length?' red':'')+'">'+flagged.length+'</div>'+
   '<div class="lbl">Paragraphs flagged</div><div class="how">of the '+paragraphs.length+' found, on '+flaggedPages.length+' pages — footnote text may sit inside these paragraphs: check them against the PDF.</div></div>'+
  '<div class="tile"><div class="n" style="font-size:26px;padding-top:14px">not separated</div>'+
   '<div class="lbl">Footnotes</div><div class="how">How this is computed: the document has '+(REF&&REF.footnotes!=null?REF.footnotes:'(no count in the reference)')+'; this version leaves them in place and flags them.</div></div>'+
 '</div>'+
 (noPara?'<p class="note" style="color:var(--red)">No paragraph was found in this file; the exports are disabled.</p>':'')+
 mismList+
 '<div class="takeaway"><div class="mono" style="color:#7a7263">TAKE THE PARAGRAPHS AWAY</div>'+
  '<div class="btnrow">'+
   '<button class="download" id="dl-json"'+(noPara?' disabled':'')+'>Download JSON</button>'+
   '<button class="download" id="dl-md"'+(noPara?' disabled':'')+'>Download Markdown</button>'+
  '</div>'+
  '<div class="how">Each record carries its source, fields and known limitations; the symbol is the key and the paragraph the pinpoint.</div></div>'+
 '<div class="checkpanel"><button class="plain" aria-expanded="false" id="chk-btn">EVERY CHECK ('+checks.length+')</button><div id="chk-body" hidden>'+
  checks.map(c=>'<div class="checkline"><span class="'+(c.pass===null?'notrun':(c.pass?'pass':'fail'))+'">'+(c.pass===null?'not run':(c.pass?'pass':'check failed'))+'</span><span><b>'+esc(c.name)+'.</b> '+c.detail+'</span></div>').join('')+
 '</div></div>'+
 '<div class="flagpanel"><button class="plain" aria-expanded="false" id="flg-btn">FLAGGED PARAGRAPHS ('+flagged.length+')</button><div id="flg-body" hidden>'+
  '<p class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</p>'+
  (flagged.length?
   '<table class="flag-table"><caption>'+flagged.length+' paragraphs flagged, on '+flaggedPages.length+' pages<span class="mono">TAB.01</span></caption>'+
   '<thead><tr><th scope="col" class="num">Paragraph</th><th scope="col" class="num">Page</th><th scope="col">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>'+
   flagged.map(p=>{
     const sl=p.lines.filter(l=>l.suspect);
     return '<tr class="main" data-num="'+p.num+'" tabindex="0"><td class="pno">'+p.num+'</td><td class="num">'+p.page_start+'</td>'+
      '<td class="suspect-list">'+sl.slice(0,2).map(l=>'<span class="sl">'+esc(l.text.slice(0,60))+(l.text.length>60?'…':'')+'</span>').join(' ')+(sl.length>2?' +'+(sl.length-2)+' more':'')+'</td>'+
      '<td class="why">'+p.reasons.map(esc).join('; ')+'</td></tr>';
   }).join('')+'</tbody></table>':'<p class="note">None.</p>')+
 '</div></div>';

function wireToggle(btnId, bodyId){
  const b=document.getElementById(btnId), d=document.getElementById(bodyId);
  b.addEventListener('click',()=>{ const open=b.getAttribute('aria-expanded')==='true'; b.setAttribute('aria-expanded',!open); d.hidden=open; });
}
wireToggle('chk-btn','chk-body');
wireToggle('flg-btn','flg-body');
document.querySelectorAll('#flg-body tr.main').forEach(tr=>{
  const open=()=>{ selectTab(2); openPara(Number(tr.dataset.num)); };
  tr.addEventListener('click',open);
  tr.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){e.preventDefault();open();} });
});

/* ---------- tab 02 ---------- */
const items=[];
spans.forEach(s=>items.push({idx:s.start, type:'h', s}));
paragraphs.forEach(p=>items.push({idx:p.startIdx, type:'p', p}));
items.sort((a,b)=>a.idx-b.idx);

function paraRow(p){
  const sl=p.lines.filter(l=>l.suspect);
  const running=p.lines.map(l=>l.suspect?'<span class="sl">'+esc(l.text)+'</span>':esc(l.text)).join(' ');
  const pdfLines=p.lines.map((l,i)=>{
    const mark=(i===0||p.lines[i-1].page!==l.page)?'<span class="pagemark">[p. '+l.page+']</span> ':'';
    return mark+(l.suspect?'<span class="sl">'+esc(l.text)+'</span>':esc(l.text));
  }).join('\n');
  const check = p.flagged ? '<span style="color:var(--red)">may contain footnote text</span>'
             : (p.first_words_match===false ? '<span style="color:var(--red)">first words differ</span>' : 'OK');
  const first = p.text.slice(0,120);
  const cut = p.text.length>120 ? first.slice(0, first.lastIndexOf(' '))+'…' : first;
  const cite = SYM+', para. '+p.num;
  return '<tr class="main" data-num="'+p.num+'" tabindex="0" aria-expanded="false">'+
   '<td class="pno">'+p.num+'</td><td>'+esc(p.section||'—')+'</td>'+
   '<td class="num">'+(p.page_start===p.page_end?p.page_start:p.page_start+'–'+p.page_end)+'</td>'+
   '<td>'+esc(cut)+'</td><td>'+check+'</td></tr>'+
   '<tr class="detail" hidden><td colspan="5">'+
    '<div class="section-path">'+esc((p.part?p.part+' \u203A ':'')+(p.section||''))+'</div>'+
    '<p class="ptext">'+running+'</p>'+
    '<div class="fw">First words, found: <b>'+esc(p.fw)+'</b>'+(p.ref_fw!=null?' · reference: <b>'+esc(p.ref_fw)+'</b>':'')+(p.first_words_match===false?' · <span style="color:var(--red)">they differ</span>':'')+'</div>'+
    '<button class="plain flg-toggle" aria-expanded="false" style="margin:6px 0">SHOW THE PDF\u2019S LINES</button>'+
    '<div class="pdf-lines" hidden>'+pdfLines+'</div>'+
    '<button class="copy" data-cite="'+esc(cite)+'">Copy citation</button> <span class="cite">'+esc(cite)+'</span>'+
   '</td></tr>';
}

panel2.innerHTML =
 '<div class="checkpanel" style="margin-top:0;border-top:none;padding-top:0">'+
  '<button class="plain" aria-expanded="false" id="hdg-btn">HEADINGS FOUND: '+spans.length+'</button>'+
  '<div id="hdg-body" hidden><div class="headings-list">'+
   (spans.length?spans.map(s=>'<div><span class="k">'+(s.kind==='roman'?'ROMAN':s.kind==='letter'?'LETTER':'UNLABELLED')+'</span>'+esc(s.text)+'</div>').join(''):'<div>None found.</div>')+
  '</div><p class="how">Listed so none can hide inside a paragraph. Unlabelled headings are lines just before a paragraph number that look like titles.</p></div>'+
 '</div>'+
 '<table id="para-table"><caption>'+paragraphs.length+' paragraphs found'+(hasRef?', '+REF.paragraphs+' expected':'')+'<span class="mono">TAB.02</span></caption>'+
 '<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col" class="num">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>'+
 '<tbody>'+ (paragraphs.length?paragraphs.map(paraRow).join(''):'') +'</tbody></table>'+
 (paragraphs.length?'':'<p class="note">No paragraphs found in this file.</p>');

wireToggle('hdg-btn','hdg-body');

function toggleRow(tr){
  const det=tr.nextElementSibling;
  const open=tr.getAttribute('aria-expanded')==='true';
  tr.setAttribute('aria-expanded',!open);
  det.hidden=open;
}
document.querySelectorAll('#para-table tr.main').forEach(tr=>{
  tr.addEventListener('click',e=>{ if(e.target.closest('button'))return; toggleRow(tr); });
  tr.addEventListener('keydown',e=>{ if((e.key==='Enter'||e.key===' ')&&e.target===tr){e.preventDefault();toggleRow(tr);} });
});
document.querySelectorAll('#para-table .flg-toggle').forEach(b=>{
  b.addEventListener('click',()=>{ const d=b.nextElementSibling; const open=b.getAttribute('aria-expanded')==='true'; b.setAttribute('aria-expanded',!open); d.hidden=open; });
});
document.querySelectorAll('#para-table .copy').forEach(b=>{
  b.addEventListener('click',async()=>{
    const t=b.dataset.cite;
    let ok=false;
    try{ await navigator.clipboard.writeText(t); ok=true; }catch(e){
      try{ const ta=document.createElement('textarea'); ta.value=t; document.body.appendChild(ta); ta.select(); ok=document.execCommand('copy'); ta.remove(); }catch(e2){ ok=false; }
    }
    const old=b.textContent; b.textContent= ok?'Copied':'Copy failed';
    setTimeout(()=>{b.textContent=old;},2000);
  });
});
function openPara(num){
  const tr=document.querySelector('#para-table tr.main[data-num="'+num+'"]');
  if(!tr) return;
  if(tr.getAttribute('aria-expanded')!=='true') toggleRow(tr);
  tr.scrollIntoView({block:'center'});
  tr.style.outline='2px solid var(--red)';
  setTimeout(()=>{tr.style.outline='';},2500);
}

/* ---------- exports ---------- */
function download(name, mime, content){
  const blob=new Blob([content],{type:mime+';charset=utf-8'});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');
  a.href=url; a.download=name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),4000);
}
const fname=(SYM||'document').replace(/\//g,'-');
const dj=document.getElementById('dl-json'), dm=document.getElementById('dl-md');
if(dj) dj.addEventListener('click',()=>download(fname+'.json','application/json',jsonString));
if(dm) dm.addEventListener('click',()=>{
  let md='---\n';
  md+='title: '+(D.title||'')+'\nsymbol: '+SYM+'\n';
  if(REF&&REF.adopted) md+='adopted: '+REF.adopted+'\n';
  md+='source_url: '+(D.doc_url||'')+'\nextracted: '+today+'\n';
  md+='paragraphs_found: '+paragraphs.length+'\n';
  if(hasRef) md+='paragraphs_expected: '+REF.paragraphs+'\n';
  md+='paragraphs_flagged: '+flagged.length+'\n';
  md+='footnotes: "not separated; the document has '+(REF&&REF.footnotes!=null?REF.footnotes:'no count in the reference')+'"\n---\n\n';
  for(const it of items){
    if(it.type==='h'){
      md+=(it.s.kind==='roman'?'## ':'### ')+it.s.text+'\n\n';
    } else {
      md+='**'+it.p.num+'.** '+it.p.text+(it.p.flagged?' *(flagged: may contain footnote text)*':'')+'\n\n';
    }
  }
  download(fname+'.md','text/markdown',md);
});
})();
</script>
</body>
</html>
```

What it does: the pipeline strips each page's header and footer, joins the body lines across pages, finds numbered paragraphs (both forms), labelled and unlabelled headings, marks suspect footnote lines without removing them, and compares first words with the reference — then shows the result, the checks, the flagged paragraphs and the two exports.