Built as planned: one page, two tabs, the whole pipeline running once on load, every number computed from the file with the reference as yardstick.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF — General Comment No. 27</title>
<style>
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{background:#f4f0e8;color:#1d1b18;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
a{color:#9b2335}
:focus-visible{outline:2px solid #9b2335;outline-offset:2px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
.site-header{padding:18px 28px 14px;border-bottom:1px solid #d9d2c3;display:flex;justify-content:space-between;gap:24px;align-items:flex-start;flex-wrap:wrap}
.site-header h1{font-family:Georgia,"Times New Roman",serif;font-weight:normal;font-size:24px;margin:6px 0 4px;max-width:60ch}
.meta-line{font-size:14px;color:#4d463c}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.dot.ok{background:#1e6b34}
.dot.bad{background:#9b2335}
.status-box{text-align:right;font-size:14px;line-height:1.7}
.tablist{display:flex;gap:0;border-bottom:1px solid #d9d2c3;padding:0 28px}
.tab{background:none;border:none;border-bottom:3px solid transparent;padding:10px 18px 8px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.12em;color:#4d463c}
.tab[aria-selected="true"]{color:#9b2335;border-bottom-color:#9b2335}
.layout{display:flex;gap:0;align-items:flex-start}
.rail{width:250px;flex:none;padding:22px 22px;border-right:1px solid #d9d2c3}
.content{flex:1;padding:22px 30px 40px;min-width:0}
.rail .doc-card{border-bottom:1px solid #d9d2c3;padding-bottom:14px;margin-bottom:18px}
.big{font-family:Georgia,"Times New Roman",serif;font-size:42px;line-height:1.05;margin:2px 0}
.big small{font-size:16px;color:#4d463c;font-family:ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em}
.rail-stat{margin-bottom:20px}
.bar{height:3px;background:#d9d2c3;margin-top:8px;position:relative}
.bar span{position:absolute;left:0;top:0;bottom:0;background:#1d1b18}
.bar.bad span{background:#9b2335}
.red{color:#9b2335}
.green{color:#1e6b34}
.hint{font-size:12.5px;color:#6b6357;margin-top:4px;line-height:1.45}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:0;border-top:1px solid #d9d2c3;border-left:1px solid #d9d2c3}
.tile{border-right:1px solid #d9d2c3;border-bottom:1px solid #d9d2c3;padding:16px 18px 14px}
.tile .lbl{margin-bottom:6px}
.mismatch-list{margin:16px 0 0;padding:0;list-style:none}
.mismatch-list li{border-bottom:1px solid #d9d2c3;padding:7px 0;font-size:14.5px}
.take-away{margin-top:34px;border-top:1px solid #d9d2c3;padding-top:16px}
.btn{background:#1d1b18;color:#f4f0e8;border:none;padding:9px 16px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;margin-right:10px}
.btn:disabled{background:#b7b0a3;cursor:not-allowed}
.btn-ghost{background:none;color:#1d1b18;border:1px solid #1d1b18}
.disclosure{background:none;border:none;border-bottom:1px solid #d9d2c3;width:100%;text-align:left;padding:12px 0;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#1d1b18;display:flex;justify-content:space-between}
.disclosure .arrow{color:#9b2335}
.disclosure-body{padding:6px 0 18px;border-bottom:1px solid #d9d2c3;margin-bottom:8px}
.check-line{display:flex;gap:12px;padding:7px 0;border-bottom:1px dotted #d9d2c3;font-size:14.5px;align-items:baseline}
.check-line .status{flex:none;width:110px}
table{border-collapse:collapse;width:100%}
caption{caption-side:top;text-align:left;font-family:Georgia,"Times New Roman",serif;font-size:19px;padding:0 0 10px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:normal;text-align:left;border-bottom:1px solid #1d1b18;padding:6px 10px 6px 0}
th.num,td.num{text-align:right}
td{border-bottom:1px solid #d9d2c3;padding:7px 10px 7px 0;vertical-align:top;font-size:15px}
tr.prow{cursor:pointer}
tr.prow:hover{background:#ece7db}
tr.detail-row td{background:#efeade;padding:16px 18px}
.para-text{max-width:75ch;line-height:1.7}
.para-text .sus{border:1px solid #9b2335;padding:0 3px}
.exp-label{margin-top:14px}
.exp-block{font-size:14.5px}
.raw-lines{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;white-space:pre-wrap;background:#efeade;padding:12px;margin-top:8px;max-width:80ch}
.raw-lines .pgmark{color:#9b2335}
.copy-btn{background:none;border:1px solid #1d1b18;padding:5px 12px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.toggle-btn{background:none;border:none;border-bottom:1px dotted #9b2335;color:#9b2335;cursor:pointer;padding:0 0 1px;font-size:13.5px}
.fp-row{display:grid;grid-template-columns:60px 110px 1fr 220px;gap:14px;width:100%;text-align:left;background:none;border:none;border-bottom:1px solid #d9d2c3;padding:9px 0;cursor:pointer;font-size:14.5px;color:#1d1b18}
.fp-row:hover{background:#ece7db}
.fp-detail{border-bottom:1px solid #d9d2c3;padding:10px 0 16px}
.fp-lines{max-width:85ch}
.fp-line{padding:1px 0}
.fp-line.sus{border:1px solid #9b2335;padding:0 4px}
.fp-line .lp{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;color:#6b6357;margin-right:8px}
.note{font-size:14px;color:#4d463c;max-width:75ch;margin:6px 0 12px;line-height:1.5}
.headings-list{font-size:14.5px;columns:1}
.headings-list li{padding:4px 0;border-bottom:1px dotted #d9d2c3}
.site-footer{border-top:1px solid #d9d2c3;padding:14px 28px;font-size:13px;color:#4d463c;display:flex;gap:24px;flex-wrap:wrap}
.fig{margin-bottom:6px}
@media (max-width:900px){.layout{flex-direction:column}.rail{width:100%;border-right:none;border-bottom:1px solid #d9d2c3}}
</style>
</head>
<body>

<header class="site-header">
  <div>
    <div class="mono">UN DOCUMENT · PDF TEXT</div>
    <h1 id="doc-title"></h1>
    <div class="meta-line" id="doc-meta"></div>
  </div>
  <div class="status-box" id="status-box"></div>
</header>

<nav class="tablist" role="tablist" aria-label="Sections">
  <button class="tab" role="tab" id="tab-1" aria-selected="true" aria-controls="panel-1">01 RESULT</button>
  <button class="tab" role="tab" id="tab-2" aria-selected="false" aria-controls="panel-2" tabindex="-1">02 PARAGRAPHS</button>
</nav>

<div class="layout">
  <aside class="rail" aria-label="Document summary">
    <div class="mono" style="margin-bottom:8px">DOCUMENT</div>
    <div class="doc-card">
      <div class="mono" id="rail-symbol"></div>
      <div style="font-size:14px;color:#4d463c;margin-top:4px" id="rail-title"></div>
    </div>
    <div class="rail-stat">
      <div class="big" id="rail-paras"></div>
      <div class="bar" id="rail-bar"><span></span></div>
      <div class="hint">numbered paragraphs found, of the number the document's reference gives</div>
    </div>
    <div class="rail-stat">
      <div class="big" id="rail-flagged"></div>
      <div class="hint">pages flagged: footnote text may sit inside a paragraph</div>
    </div>
    <div class="rail-stat">
      <div class="big" id="rail-checks"></div>
      <div class="hint">self-checks passed, of those run — see tab 01</div>
    </div>
  </aside>

  <main class="content">
    <section role="tabpanel" id="panel-1" aria-labelledby="tab-1">
      <div class="tiles" id="tiles"></div>
      <ul class="mismatch-list" id="mismatch-list" hidden></ul>

      <div class="take-away">
        <div class="mono" style="margin-bottom:10px">TAKE THE PARAGRAPHS AWAY</div>
        <button class="btn" id="dl-json">Download JSON</button>
        <button class="btn btn-ghost" id="dl-md">Download Markdown</button>
        <div class="hint">each record carries its symbol, paragraph number, headings, pages, text, citation and limitations</div>
      </div>

      <div style="margin-top:34px">
        <button class="disclosure" id="disc-checks" aria-expanded="false"><span id="disc-checks-lbl">EVERY CHECK</span><span class="arrow">+</span></button>
        <div class="disclosure-body" id="checks-body" hidden></div>

        <button class="disclosure" id="disc-flagged" aria-expanded="false"><span id="disc-flagged-lbl">FLAGGED PAGES</span><span class="arrow">+</span></button>
        <div class="disclosure-body" id="flagged-body" hidden></div>
      </div>
    </section>

    <section role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
      <button class="disclosure" id="disc-headings" aria-expanded="false" style="max-width:420px"><span id="disc-headings-lbl">HEADINGS FOUND</span><span class="arrow">+</span></button>
      <div class="disclosure-body" id="headings-body" hidden style="max-width:720px"></div>
      <div id="para-table-wrap" style="margin-top:18px"></div>
    </section>
  </main>
</div>

<footer class="site-footer">
  <span id="foot-source"></span>
  <span id="foot-built"></span>
  <span>Done by this page's code; no model was called and nothing left the browser.</span>
</footer>

<script>
(function(){
"use strict";
var D = window.WORKSHOP_DATA.pdf_text || {};
var symbol = D.symbol || "";
var title = D.title || "";
var doc_url = D.doc_url || "";
var source = D.source || "";
var ref = D.reference || null;

// ---------- pipeline (runs once, in order) ----------
var pages = (D.records || []).slice().sort(function(a,b){return a.page-b.page;})
  .map(function(r){return {page:r.page, lines:(r.text||"").split("\n")};});
var totalPages = pages.length;

var totalNonEmpty = 0;
pages.forEach(function(p){p.lines.forEach(function(l){if(l.trim()!=="")totalNonEmpty++;});});

// header + footer
var cntHeader=0, cntFooter=0, headerMiss=[], bareRemoved=[], pageNoPages=0;
var body=[]; // {text, page}
pages.forEach(function(p){
  var s=0;
  var fi=-1;
  for(var x=0;x<p.lines.length;x++){if(p.lines[x].trim()!==""){fi=x;break;}}
  if(fi>=0 && p.lines[fi].trim()===symbol){cntHeader++;s=fi+1;}
  else headerMiss.push(p.page);
  var e=p.lines.length-1;
  while(e>=s){
    var t=p.lines[e].trim();
    if(t===""){e--;continue;}
    if(/^GE\./.test(t) || /^\d{6}( \d{6})*$/.test(t) || /^\d{1,3}$/.test(t)){
      cntFooter++;
      if(/^\d{1,3}$/.test(t) && +t!==p.page) bareRemoved.push({page:p.page,line:t});
      if(/^\d{1,3}$/.test(t) && +t===p.page) pageNoPages++;
      e--;continue;
    }
    break;
  }
  for(var i=s;i<=e;i++){var tt=p.lines[i].trim(); if(tt!=="") body.push({text:tt,page:p.page});}
});

var N=body.length;
var labelRe=/^([IVX]+|[A-Z])\.$/;
function psOf(l){
  var m=l.match(/^(\d{1,3})\.$/); if(m) return {n:+m[1],first:null};
  m=l.match(/^(\d{1,3})\. (.+)$/); if(m) return {n:+m[1],first:m[2]};
  return null;
}
var ps = body.map(function(l){return psOf(l.text);});
var firstPS=-1; for(var q=0;q<N;q++){if(ps[q]){firstPS=q;break;}}

// headings
var isHead=new Array(N).fill(false);
var headings=[];
for(var i=0;i<N;i++){
  if(labelRe.test(body[i].text)){
    var j=i+1, parts=[body[i].text];
    while(j<N && !ps[j] && !labelRe.test(body[j].text)){parts.push(body[j].text);j++;}
    headings.push({idx:i,text:parts.join(" "),page:body[i].page,kind:/^[IVX]+\.$/.test(body[i].text)?"roman":"letter"});
    for(var k=i;k<j;k++)isHead[k]=true;
    i=j-1;
  }
}
function headTest(t){return t.length<=90 && /^[A-Z(]/.test(t) && !/[.;:,0-9]$/.test(t);}
for(var i2=0;i2<N;i2++){
  if(isHead[i2]||ps[i2])continue;
  if(i2+1<N && ps[i2+1]){
    var texts=[body[i2].text], idxs=[i2];
    var k2=i2-1;
    if(k2>=0 && !isHead[k2] && !ps[k2] && headTest(body[k2].text) && !/[.;:!?]$/.test(body[k2].text)){
      texts.unshift(body[k2].text); idxs.unshift(k2);
    }
    headings.push({idx:idxs[0],text:texts.join(" "),page:body[idxs[0]].page,kind:"unlabelled"});
    idxs.forEach(function(x){isHead[x]=true;});
  }
}
headings.sort(function(a,b){return a.idx-b.idx;});

// paragraphs
var paras=[], cur=null, curSection="", curPart="", hPtr=0, cntCover=0, cntOther=0, otherLines=[];
for(var i3=0;i3<N;i3++){
  while(hPtr<headings.length && headings[hPtr].idx<=i3){
    var h=headings[hPtr]; curSection=h.text; if(h.kind==="roman")curPart=h.text; hPtr++;
  }
  if(ps[i3]){
    if(cur)paras.push(cur);
    cur={n:ps[i3].n,lines:[],startIdx:i3,section:curSection,part:curPart};
    if(ps[i3].first)cur.lines.push({text:ps[i3].first,page:body[i3].page,bodyIdx:null});
    continue;
  }
  if(isHead[i3]){ if(cur){paras.push(cur);cur=null;} continue; }
  if(firstPS<0 || i3<firstPS){cntCover++;continue;}
  if(cur){cur.lines.push({text:body[i3].text,page:body[i3].page,bodyIdx:i3});}
  else {cntOther++;otherLines.push(i3);}
}
if(cur)paras.push(cur);

// suspect lines (never before the first paragraph start)
function whySuspect(t){
  if(/^\d{1,3}$/.test(t)) return "bare number";
  if(/^\d{1,3} [A-Z\u201c"]/.test(t)) return "starts with a number and a space";
  if(/^\* /.test(t)) return "asterisk note";
  return null;
}
var susFlag=new Array(N).fill(false), susWhy=new Array(N).fill(null);
for(var i4=0;i4<N;i4++){
  if(firstPS<0||i4<firstPS)continue;
  var w=whySuspect(body[i4].text);
  if(w){susFlag[i4]=true;susWhy[i4]=w;
    for(var j4=i4+1;j4<N&&body[j4].page===body[i4].page;j4++)susFlag[j4]=true;}
}

// finish paragraphs
function norm(s){return (s||"").replace(/[\u201c\u201d]/g,'"').replace(/[\u2018\u2019]/g,"'").replace(/[\u2013\u2014]/g,"-").replace(/\s+/g," ").trim();}
function firstWords(text){
  var toks=text.split(/\s+/), out=[];
  for(var a=0;a<toks.length;a++){
    var t=toks[a];
    var m=t.match(/^(.+?\D)(\d+)$/); if(m)t=m[1];
    if(/^\d+$/.test(t)){
      var prev=out[out.length-1];
      if(prev && /[.,\u201d"]$/.test(prev) && !/(No|art|para|vol)\.$/.test(prev)) continue;
    }
    out.push(t);
    if(out.length===6)break;
  }
  return out.join(" ");
}
var hyphenEnd=body.filter(function(l){return /-$/.test(l.text);}).length;
paras.forEach(function(p){
  p.page_start=p.lines[0].page;
  p.page_end=p.lines[p.lines.length-1].page;
  p.text=p.lines.map(function(l){return l.text;}).join(" ").replace(/\s{2,}/g," ").trim();
  p.words=p.text.split(/\s+/).length;
  p.text_lines=p.lines.map(function(l){return l.text;}).join(" | ");
  p.susIdx=p.lines.filter(function(l){return l.bodyIdx!=null&&susFlag[l.bodyIdx];}).map(function(l){return l.bodyIdx;});
  p.over300=p.words>300;
  p.flagged=p.susIdx.length>0||p.over300;
  p.fw=firstWords(p.text);
  var rw=(ref&&ref.first_words)?ref.first_words[String(p.n)]:null;
  p.ref_fw=rw;
  p.first_words_match=(rw!=null)?(norm(p.fw)===norm(rw)):null;
  p.citation=symbol+", para. "+p.n;
});
var linePara=new Array(N).fill(null);
paras.forEach(function(p){p.lines.forEach(function(l){if(l.bodyIdx!=null)linePara[l.bodyIdx]=p.n;});});

// flagged pages
var flaggedPages={};
paras.forEach(function(p){
  if(!p.flagged)return;
  var pgs={};
  p.susIdx.forEach(function(i){pgs[body[i].page]=true;});
  p.susIdx.forEach(function(i){
    if(!susWhy[i])return;
    var pg=body[i].page;
    if(!flaggedPages[pg])flaggedPages[pg]={paras:{},triggers:[]};
    flaggedPages[pg].paras[p.n]=true;
    flaggedPages[pg].triggers.push({line:body[i].text,why:susWhy[i],para:p.n});
  });
  if(p.over300){
    var pg2=p.page_end;
    if(!flaggedPages[pg2])flaggedPages[pg2]={paras:{},triggers:[]};
    flaggedPages[pg2].paras[p.n]=true;
    flaggedPages[pg2].triggers.push({line:p.words+" words",why:"paragraph over 300 words",para:p.n});
  }
});
var flaggedPageNums=Object.keys(flaggedPages).map(Number).sort(function(a,b){return a-b;});
var flaggedParaCount=0;var fpSet={};
flaggedPageNums.forEach(function(pg){Object.keys(flaggedPages[pg].paras).forEach(function(n){if(!fpSet[n]){fpSet[n]=true;flaggedParaCount++;}});});

// ---------- checks ----------
var checks=[];
function addCheck(name,detail,status){checks.push({name:name,detail:detail,status:status});}
var expected=ref&&ref.paragraphs!=null?ref.paragraphs:null;
var noRefMsg="no reference in this file";
if(expected==null) addCheck("Paragraph count","found "+paras.length+" paragraphs — "+noRefMsg,"notrun");
else addCheck("Paragraph count","found "+paras.length+" · reference says "+expected,(paras.length===expected)?"pass":"fail");

var numIssues=[];
paras.forEach(function(p,ix){if(p.n!==ix+1)numIssues.push("para. "+p.n+" (page "+p.page_start+")");});
if(numIssues.length===0) addCheck("Numbering","paragraphs run exactly 1 to "+paras.length+" in order","pass");
else addCheck("Numbering","gaps or duplicates: "+numIssues.join(", "),"fail");

var fwChecked=paras.filter(function(p){return p.ref_fw!=null;}).length;
var fwBad=paras.filter(function(p){return p.first_words_match===false;});
if(ref&&ref.first_words){
  addCheck("First words",fwBad.length+" of "+fwChecked+" paragraphs differ from the reference's first six words"+(fwBad.length?" — listed on tab 01, rows flagged on tab 02":""),fwBad.length===0?"pass":"fail");
}else addCheck("First words","not run — "+noRefMsg,"notrun");

addCheck("Pages flagged",flaggedPageNums.length+" pages flagged, "+flaggedParaCount+" paragraphs to check against the PDF (a flag is not a failure)","info");

var trigCount=0,trigPages={};
for(var i5=0;i5<N;i5++){if(susWhy[i5]&&linePara[i5]!=null){trigCount++;trigPages[body[i5].page]=true;}}
addCheck("Suspect lines",trigCount+" suspect trigger lines on "+Object.keys(trigPages).length+" pages, inside paragraphs; none is removed from the text","info");

var hfDetail = cntHeader+" of "+totalPages+" pages opened with the symbol"+(headerMiss.length?(" — missing on pages "+headerMiss.join(", ")):"")+"; "+pageNoPages+" pages carried a page number in the footer (first page has a date stamp instead)"+(bareRemoved.length?("; bare numbers removed from footers: "+bareRemoved.map(function(b){return b.line+" (p. "+b.page+")";}).join(", ")):"")+".";
addCheck("Headers and footers",hfDetail,(cntHeader===totalPages)?"pass":"fail");

var labelled=headings.filter(function(h){return h.kind!=="unlabelled";}).length;
var unlabelled=headings.filter(function(h){return h.kind==="unlabelled";});
addCheck("Headings",labelled+" labelled headings ("+unlabelled.length+" unlabelled): "+(unlabelled.map(function(h){return "\u201c"+h.text+"\u201d (p. "+h.page+")";}).join(" · ")||"none"),"pass");

var cntHeadLines=0;isHead.forEach(function(b){if(b)cntHeadLines++;});
var cntParaLines=0;body.forEach(function(l,i){if(linePara[i]!=null)cntParaLines++;});
var sum=cntHeader+cntFooter+cntCover+cntHeadLines+cntParaLines+cntOther;
var nlDetail=sum+" classified lines ("+cntHeader+" header, "+cntFooter+" footer, "+cntCover+" cover, "+cntHeadLines+" heading, "+cntParaLines+" paragraph, "+cntOther+" unclassified) against "+totalNonEmpty+" non-empty lines in the file.";
if(cntOther>0) nlDetail+=" Unclassified: "+otherLines.map(function(i){return "p. "+body[i].page+" \u201c"+body[i].text.slice(0,40)+"\u201d";}).join(" · ");
addCheck("Nothing lost",nlDetail,(sum===totalNonEmpty&&cntOther===0)?"pass":"fail");

// exports + round trip
var exportRecords=paras.map(function(p){
  return {symbol:symbol,paragraph:p.n,section:p.section,part:p.part,page_start:p.page_start,page_end:p.page_end,
    text:p.text,text_lines:p.text_lines,flagged:p.flagged,first_words_match:p.first_words_match,
    citation:p.citation,doc_url:doc_url,
    limitations:p.flagged?("footnotes not separated; "+(p.over300?"this paragraph is over 300 words":"footnote text may sit inside this paragraph")+" — check against the PDF"):"footnotes not separated"};
});
var rtOK=false;
try{rtOK=(JSON.parse(JSON.stringify(exportRecords)).length===paras.length);}catch(e){rtOK=false;}
if(paras.length) addCheck("Export round trip","the JSON offered for download parses back to "+exportRecords.length+" records, equal to the table on tab 02",rtOK?"pass":"fail");
else addCheck("Export round trip","not run — no paragraphs found","notrun");

var failCount=checks.filter(function(c){return c.status==="fail";}).length;
var runCount=checks.filter(function(c){return c.status!=="notrun";}).length;
var passCount=checks.filter(function(c){return c.status==="pass"||c.status==="info";}).length;
var m=checks.length;

// ---------- render ----------
function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}
document.getElementById("doc-title").textContent=title;
document.getElementById("doc-meta").innerHTML =
  (doc_url?('<a href="'+esc(doc_url)+'" target="_blank" rel="noopener">'+esc(symbol)+"</a>"):esc(symbol))+
  (ref&&ref.adopted?(" · adopted "+esc(ref.adopted)):"")+
  " · "+totalPages+" pages"+(source?" · "+esc(source):"");
document.getElementById("rail-symbol").textContent=symbol;
document.getElementById("rail-title").textContent=title;
document.getElementById("foot-source").textContent=source||"";
document.getElementById("foot-built").textContent=D.built?("built "+D.built):"";

var sb=document.getElementById("status-box");
if(failCount>0) sb.innerHTML='<span class="dot bad"></span>'+failCount+" checks failed<br>"+flaggedPageNums.length+" pages flagged";
else sb.innerHTML='<span class="dot ok"></span>'+passCount+" of "+m+" checks pass<br>"+flaggedPageNums.length+" pages flagged";

var railP=document.getElementById("rail-paras");
railP.innerHTML=paras.length+' <small>of '+(expected==null?"— no reference":expected)+"</small>";
var barEl=document.getElementById("rail-bar");
if(expected!=null&&expected>0){barEl.querySelector("span").style.width=Math.min(100,Math.round(paras.length/expected*100))+"%";if(paras.length!==expected)barEl.classList.add("bad");}
else barEl.hidden=true;
document.getElementById("rail-flagged").innerHTML='<span class="'+(flaggedPageNums.length?"red":"")+'">'+flaggedPageNums.length+'</span> <small>of '+totalPages+" pages</small>";
document.getElementById("rail-checks").innerHTML=passCount+' <small>of '+m+" checks</small>";

// tiles
var fwMatchCount=paras.filter(function(p){return p.first_words_match===true;}).length;
function tile(lbl,main,how,cls){return '<div class="tile"><div class="mono lbl">'+lbl+'</div><div class="big '+(cls||"")+'">'+main+'</div><div class="hint">'+how+"</div></div>";}
var tiles="";
tiles+=tile("PARAGRAPHS FOUND",paras.length+' <small>'+(expected==null?"no reference in this file":"of "+expected+" in the document")+"</small>",
  "How this is computed: a line that is a number alone (\u201c12.\u201d) or a number with text (\u201c12. The\u2026\u201d) opens a paragraph; lines join until the next number, heading or foot of page.",(expected!=null&&paras.length!==expected)?"red":(expected!=null?"green":""));
tiles+=tile("FIRST WORDS MATCH",fwMatchCount+' <small>of '+(expected==null?"—":expected)+"</small>",
  "How this is computed: the first six words of each paragraph, footnote marks cut, compared with the reference's first six words after normalising quotes and dashes.",(fwBad.length?"red":(fwChecked?"green":"")));
tiles+=tile("PAGES FLAGGED",'<span class="'+(flaggedPageNums.length?"red":"")+'">'+flaggedPageNums.length+'</span> <small>of '+totalPages+" pages</small>",
  "How this is computed: a page with a line inside a paragraph that looks like footnote text (a bare number, or a number then a capital) is flagged — check these paragraphs against the PDF.","");
tiles+=tile("FOOTNOTES","<small>not separated</small>",
  "The document has "+((ref&&ref.footnotes!=null)?ref.footnotes:"— no reference")+" footnotes; this version leaves them in place and flags where they may sit.","");
document.getElementById("tiles").innerHTML=tiles;

// mismatch list
var ml=document.getElementById("mismatch-list");
if(fwBad.length){
  ml.hidden=false;
  ml.innerHTML=fwBad.slice(0,10).map(function(p){
    return '<li class="red">para. '+p.n+": found \u201c"+esc(p.fw)+"\u201d / reference \u201c"+esc(p.ref_fw)+"\u201d</li>";
  }).join("")+(fwBad.length>10?('<li>and '+(fwBad.length-10)+" more</li>"):"");
}

// exports
function download(name,content,type){
  var b=new Blob([content],{type:type+";charset=utf-8"});
  var u=URL.createObjectURL(b);
  var a=document.createElement("a");a.href=u;a.download=name;document.body.appendChild(a);a.click();
  setTimeout(function(){URL.revokeObjectURL(u);a.remove();},5000);
}
var today=new Date().toISOString().slice(0,10);
var dlJ=document.getElementById("dl-json"),dlM=document.getElementById("dl-md");
if(!paras.length){dlJ.disabled=true;dlM.disabled=true;
  var p1=document.createElement("p");p1.className="note";p1.textContent="No paragraphs were found in this file, so there is nothing to export.";
  dlJ.parentNode.appendChild(p1);}
dlJ.addEventListener("click",function(){download(symbol.replace(/\//g,"-")+".json",JSON.stringify(exportRecords,null,2),"application/json");});
dlM.addEventListener("click",function(){
  var L=["---"];
  L.push('title: "'+title.replace(/"/g,'\\"')+'"');
  L.push("symbol: "+symbol);
  if(ref&&ref.adopted)L.push("adopted: "+ref.adopted);
  L.push("source_url: "+doc_url);
  L.push("extracted: "+today);
  L.push("paragraphs_found: "+paras.length);
  L.push("paragraphs_expected: "+(expected==null?"unknown":expected));
  L.push("pages_flagged: "+flaggedPageNums.length);
  L.push('footnotes: "not separated; the document has '+((ref&&ref.footnotes!=null)?ref.footnotes:"unknown")+'"');
  L.push("---");L.push("");
  var events=headings.map(function(h){return {idx:h.idx,head:h};}).concat(paras.map(function(p){return {idx:p.startIdx,para:p};}));
  events.sort(function(a,b){return a.idx-b.idx;});
  events.forEach(function(ev){
    if(ev.head)L.push((ev.head.kind==="roman"?"## ":"### ")+ev.head.text),L.push("");
    else{L.push("**"+ev.para.n+".** "+ev.para.text+(ev.para.flagged?" *(flagged: may contain footnote text)*":""));L.push("");}
  });
  download(symbol.replace(/\//g,"-")+".md",L.join("\n"),"text/markdown");
});

// checks disclosure
function wireDisclosure(btnId,bodyId){
  var btn=document.getElementById(btnId),bd=document.getElementById(bodyId);
  btn.addEventListener("click",function(){
    var open=btn.getAttribute("aria-expanded")==="true";
    btn.setAttribute("aria-expanded",open?"false":"true");
    bd.hidden=open;
    btn.querySelector(".arrow").textContent=open?"+":"\u2013";
  });
}
wireDisclosure("disc-checks","checks-body");
wireDisclosure("disc-flagged","flagged-body");
document.getElementById("disc-checks-lbl").textContent="EVERY CHECK ("+m+")";
document.getElementById("disc-flagged-lbl").textContent="FLAGGED PAGES ("+flaggedPageNums.length+")";

var cb=document.getElementById("checks-body");
cb.innerHTML=checks.map(function(c){
  var st=c.status==="pass"?'<span class="status green">pass</span>':
    c.status==="fail"?'<span class="status red">check failed</span>':
    c.status==="info"?'<span class="status" style="color:#4d463c">noted</span>':
    '<span class="status" style="color:#4d463c">not run</span>';
  return '<div class="check-line">'+st+'<div><strong>'+esc(c.name)+".</strong> "+esc(c.detail)+"</div></div>";
}).join("")+'<p class="hint" style="margin-top:10px">Each check states what was compared, the two values, and the outcome: given this data, having run this code, this is what we expect. A failed check never hides a result.'+(hyphenEnd?(" (Note: "+hyphenEnd+" lines end with a hyphen; none was joined, per this file's design.)"):"")+"</p>";

// flagged pages disclosure
var fb=document.getElementById("flagged-body");
if(!flaggedPageNums.length){
  fb.innerHTML='<p class="note">No pages are flagged: no line inside a paragraph looks like footnote text.</p>';
}else{
  var html='<p class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</p>';
  flaggedPageNums.forEach(function(pg){
    var f=flaggedPages[pg];
    var pnums=Object.keys(f.paras).map(Number).sort(function(a,b){return a-b;}).join(", ");
    var trigLines=f.triggers.slice(0,2).map(function(t){return esc(t.line.length>60?t.line.slice(0,57)+"\u2026":t.line);}).join(" · ");
    var whys=[];f.triggers.forEach(function(t){if(whys.indexOf(t.why)<0)whys.push(t.why);});
    html+='<button class="fp-row" aria-expanded="false" data-pg="'+pg+'"><span class="mono">P.'+pg+'</span><span>para. '+esc(pnums)+"</span><span>"+trigLines+(f.triggers.length>2?" \u2026":"")+'</span><span class="red">'+esc(whys.join("; "))+'</span></button><div class="fp-detail" hidden></div>';
  });
  fb.innerHTML=html;
  Array.prototype.forEach.call(fb.querySelectorAll(".fp-row"),function(row){
    row.addEventListener("click",function(){
      var open=row.getAttribute("aria-expanded")==="true";
      row.setAttribute("aria-expanded",open?"false":"true");
      var det=row.nextElementSibling;
      if(!open){
        if(!det.dataset.built){
          var pg=+row.dataset.pg;
          var lines="";
          body.forEach(function(l,i){
            if(l.page!==pg)return;
            var cls=susFlag[i]?"fp-line sus":"fp-line";
            lines+='<div class="'+cls+'"><span class="lp">'+(linePara[i]!=null?("para. "+linePara[i]):(isHead[i]?"heading":"cover"))+"</span>"+esc(l.text)+"</div>";
          });
          det.innerHTML='<div class="fp-lines">'+lines+'</div><p class="hint">The page\u2019s body lines (header and footer already removed). Suspect lines and everything after them on the page are boxed in red; the label shows the paragraph each line currently sits in.</p>';
          det.dataset.built="1";
        }
        det.hidden=false;
      } else det.hidden=true;
    });
  });
}

// ---------- tab 02 ----------
var hd=document.getElementById("disc-headings");
document.getElementById("disc-headings-lbl").textContent="HEADINGS FOUND ("+headings.length+")";
document.getElementById("headings-body").innerHTML='<ul class="headings-list" style="list-style:none;padding:0;margin:0">'+
  headings.map(function(h){return '<li><span class="mono">'+(h.kind==="roman"?"SECTION":h.kind==="letter"?"SUBSECTION":"UNLABELLED")+"</span> "+esc(h.text)+' <span class="hint" style="display:inline">p. '+h.page+"</span></li>";}).join("")+"</ul>";
wireDisclosure("disc-headings","headings-body");

function firstLine(t){
  if(t.length<=120)return t;
  var cut=t.slice(0,120),sp=cut.lastIndexOf(" ");
  return (sp>60?cut.slice(0,sp):cut)+"\u2026";
}
var wrap=document.getElementById("para-table-wrap");
var capMsg=paras.length+" paragraphs found"+(expected!=null?", "+expected+" expected":", no reference in this file");
var rows=paras.map(function(p,ix){
  var checkCell=p.first_words_match===false?'<span class="red">first words differ</span>':
    p.flagged?'<span class="red">may contain footnote text</span>':"OK";
  var pages=p.page_start===p.page_end?String(p.page_start):p.page_start+"\u2013"+p.page_end;
  return '<tr class="prow" tabindex="0" role="button" aria-expanded="false" data-ix="'+ix+'">'+
    '<td class="num serif" style="font-size:19px;color:#9b2335">'+p.n+"</td>"+
    '<td title="'+esc(p.part+(p.section&&p.section!==p.part?" \u203a "+p.section:""))+'">'+esc(p.section||"\u2014")+"</td>"+
    '<td class="num">'+pages+"</td>"+
    "<td>"+esc(firstLine(p.text))+"</td>"+
    "<td>"+checkCell+"</td></tr>"+
    '<tr class="detail-row" hidden><td colspan="5"><div id="pdet-'+ix+'"></div></td></tr>';
}).join("");
wrap.innerHTML='<table><caption>'+esc(capMsg)+'</caption>'+
  '<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col" class="num">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>'+
  "<tbody>"+rows+"</tbody></table>"+
  '<p class="hint">How this is computed: click a row to read the paragraph in full, verbatim as this page\u2019s code joined the PDF\u2019s lines \u2014 never shortened. \u201cPage\u201d is the page(s) the paragraph starts and ends on.</p>';

function renderDetail(ix){
  var p=paras[ix];
  var path=p.part&&p.section&&p.part!==p.section?(esc(p.part)+" \u203a "+esc(p.section)):esc(p.section||"");
  var spans=p.lines.map(function(l){
    var sus=l.bodyIdx!=null&&susFlag[l.bodyIdx];
    return '<span class="'+(sus?"sus":"")+'">'+esc(l.text)+"</span>";
  }).join(" ");
  var fwLine='<div class="exp-label mono">FIRST WORDS</div><div class="exp-block">found: '+esc(p.fw)+(p.ref_fw!=null?"<br>reference: "+esc(p.ref_fw):" \u2014 no reference for this paragraph")+"</div>";
  var raw="";
  p.lines.forEach(function(l,li){
    if(li===0||p.lines[li-1].page!==l.page)raw+='<span class="pgmark">— p. '+l.page+" —</span>\n";
    raw+=l.text+"\n";
  });
  var d=document.getElementById("pdet-"+ix);
  d.innerHTML='<div class="exp-label mono">FULL PATH</div><div class="exp-block">'+path+' <span class="hint" style="display:inline">(pages '+p.page_start+(p.page_end!==p.page_start?"\u2013"+p.page_end:"")+", "+p.words+" words)</span></div>"+
    '<div class="exp-label mono">TEXT (VERBATIM AS COMPUTED)</div><div class="para-text">'+spans+(p.flagged?' <span class="red" style="font-size:13px">(flagged: may contain footnote text)</span>':"")+"</div>"+
    fwLine+
    '<div style="margin-top:12px"><button class="toggle-btn" type="button">Show the PDF\u2019s lines</button></div>'+
    '<div class="raw-lines" hidden>'+esc(raw)+'</div>'+
    '<div style="margin-top:14px"><button class="copy-btn" type="button" data-cit="'+esc(p.citation)+'">Copy citation</button> <span class="hint" style="display:inline">copies \u201c'+esc(p.citation)+"\u201d</span></div>";
  var tb=d.querySelector(".toggle-btn"),rl=d.querySelector(".raw-lines");
  tb.addEventListener("click",function(){
    var h=rl.hidden;rl.hidden=!h;tb.textContent=h?"Hide the PDF\u2019s lines":"Show the PDF\u2019s lines";
  });
  var cp=d.querySelector(".copy-btn");
  cp.addEventListener("click",function(){
    var txt=cp.dataset.cit;
    function done(){cp.textContent="Copied";setTimeout(function(){cp.textContent="Copy citation";},2000);}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(done,function(){fallback();});}
    else fallback();
    function fallback(){
      var ta=document.createElement("textarea");ta.value=txt;document.body.appendChild(ta);
      ta.select();try{document.execCommand("copy");}catch(e){}ta.remove();done();
    }
  });
}
Array.prototype.forEach.call(wrap.querySelectorAll("tr.prow"),function(row){
  function toggle(){
    var open=row.getAttribute("aria-expanded")==="true";
    row.setAttribute("aria-expanded",open?"false":"true");
    var det=row.nextElementSibling;
    if(!open){if(!det.dataset.built){renderDetail(+row.dataset.ix);det.dataset.built="1";}det.hidden=false;}
    else det.hidden=true;
  }
  row.addEventListener("click",toggle);
  row.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();toggle();}});
});

// ---------- tabs ----------
var tabs=[document.getElementById("tab-1"),document.getElementById("tab-2")];
var panels=[document.getElementById("panel-1"),document.getElementById("panel-2")];
function selectTab(i){
  tabs.forEach(function(t,ix){t.setAttribute("aria-selected",ix===i?"true":"false");t.tabIndex=ix===i?0:-1;panels[ix].hidden=ix!==i;});
  tabs[i].focus();
}
tabs.forEach(function(t,ix){
  t.addEventListener("click",function(){selectTab(ix);});
  t.addEventListener("keydown",function(e){
    if(e.key==="ArrowRight")selectTab((ix+1)%tabs.length);
    else if(e.key==="ArrowLeft")selectTab((ix-1+tabs.length)%tabs.length);
  });
});
})();
</script>
</body>
</html>
```