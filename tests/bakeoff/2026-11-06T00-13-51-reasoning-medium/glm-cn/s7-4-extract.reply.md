I built the app exactly to the plan: a two-tab reader that turns the raw PDF text of E/C.12/GC/27 into numbered paragraphs with headings, flags paragraphs that may contain footnote text, checks itself against the document's reference, and exports the result as JSON or Markdown. Everything is computed on load by the page's own code — no model, no network.```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
:root{
  --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335; --green:#1e6b34;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
a{color:var(--red)}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase}
header.app{border-bottom:1px solid var(--rule);padding:16px 0 12px}
header.app .label{color:#6b6355}
header.app h1{font-family:Georgia,"Times New Roman",serif;font-size:26px;font-weight:normal;margin:6px 0 4px}
header.app .meta{font-size:14px;color:#4a443a}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;vertical-align:-1px;margin-right:6px}
.dot.ok{background:var(--green)} .dot.bad{background:var(--red)}
.statusbox{float:right;text-align:right;font-size:13px;line-height:1.7}
nav.tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);margin-top:8px}
nav.tabs button{background:none;border:none;border-bottom:3px solid transparent;padding:10px 18px 8px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.12em;color:#4a443a}
nav.tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
nav.tabs button:focus-visible{outline:2px solid var(--red);outline-offset:2px}
.layout{display:grid;grid-template-columns:250px 1fr;gap:32px;padding:22px 0}
aside .card{border:1px solid var(--rule);padding:14px;margin-bottom:18px}
aside .card .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;color:var(--red)}
aside .card .st{font-family:Georgia,serif;font-size:14px;margin-top:4px}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1.05;margin:10px 0 2px}
.bignum.bad{color:var(--red)}
.bar{height:4px;background:var(--rule);margin:6px 0}
.bar i{display:block;height:100%;background:var(--ink)}
.bar.bad i{background:var(--red)}
.railnote{font-size:12.5px;color:#4a443a}
.railflag{font-size:12.5px;color:var(--red)}
h2.fig{font-family:Georgia,"Times New Roman",serif;font-size:19px;font-weight:normal;margin:26px 0 4px}
.how{font-size:12.5px;color:#6b6355;margin:0 0 14px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);margin-top:18px}
.tile{background:var(--paper);padding:16px}
.tile .t{font-family:Georgia,"Times New Roman",serif;font-size:42px;line-height:1.05}
.tile .t.ok{color:var(--green)} .tile .t.bad{color:var(--red)}
.tile .sub{font-size:13px;color:#4a443a;margin-top:4px}
.tile .h{font-size:12.5px;color:#6b6355;margin-top:6px}
button.btn{background:var(--ink);color:var(--paper);border:none;padding:10px 16px;cursor:pointer;font:inherit;font-size:14px;margin-right:10px}
button.btn:focus-visible{outline:2px solid var(--red);outline-offset:2px}
button.btn:disabled{background:#a49b8b;cursor:not-allowed}
button.collapser{background:none;border:none;border-bottom:1px solid var(--rule);width:100%;text-align:left;padding:12px 0;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);display:flex;justify-content:space-between}
button.collapser:focus-visible{outline:2px solid var(--red);outline-offset:2px}
table{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0 4px}
caption{font-family:Georgia,"Times New Roman",serif;font-size:16px;text-align:left;padding:6px 0;caption-side:top}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:normal;text-align:left;border-bottom:1px solid var(--rule);padding:6px 8px}
td{border-bottom:1px solid var(--rule);padding:7px 8px;vertical-align:top}
th.num,td.num{text-align:right}
td pno{font-family:Georgia,serif}
.okword{color:var(--green)} .badword{color:var(--red)}
.checkline{display:flex;gap:10px;padding:6px 0;border-bottom:1px dotted var(--rule);font-size:14px}
.checkline .val{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
.misline{font-size:14px;padding:4px 0;border-bottom:1px dotted var(--rule)}
.expander{background:none;border:none;cursor:pointer;padding:0;font:inherit;color:var(--red);text-align:left}
.expander:focus-visible{outline:2px solid var(--red);outline-offset:2px}
tr.detail td{background:#efe9dd}
.parafull{font-size:15px;line-height:1.65}
.suspect{border:1px solid var(--red);padding:0 2px}
.linelist{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;white-space:pre-wrap;background:#efe9dd;padding:10px;margin:8px 0}
.pagemark{color:var(--red)}
.refcmp{font-size:13.5px;margin:10px 0 4px;color:#4a443a}
.copybtn{background:none;border:1px solid var(--ink);padding:5px 10px;cursor:pointer;font:inherit;font-size:13px}
.copybtn:focus-visible{outline:2px solid var(--red)}
.note{font-size:13.5px;color:#4a443a;margin:6px 0}
footer.app{border-top:1px solid var(--rule);padding:14px 0 30px;font-size:13px;color:#4a443a}
@media (max-width:760px){.layout{grid-template-columns:1fr}.statusbox{float:none;margin-top:8px}}
</style>
</head>
<body>
<header class="app"><div class="wrap">
  <div class="statusbox" id="statusbox"></div>
  <div class="label mono">UN DOCUMENT · PDF TEXT</div>
  <h1 id="doctitle"></h1>
  <div class="meta" id="docmeta"></div>
  <nav class="tabs" role="tablist" aria-label="Sections">
    <button role="tab" id="tab1" aria-selected="true" aria-controls="panel1">01 RESULT</button>
    <button role="tab" id="tab2" aria-selected="false" aria-controls="panel2" tabindex="-1">02 PARAGRAPHS</button>
  </nav>
</div></header>

<div class="wrap layout">
  <aside>
    <div class="card">
      <div class="sym" id="railSymbol"></div>
      <div class="st" id="railTitle"></div>
    </div>
    <div>
      <div class="mono" style="color:#6b6355">Paragraphs</div>
      <div class="bignum" id="railParaN">–</div>
      <div class="bar" id="railParaBar"><i></i></div>
      <div class="railnote" id="railParaNote"></div>
    </div>
    <div>
      <div class="mono" style="color:#6b6355;margin-top:18px">Flagged</div>
      <div class="bignum" id="railFlagN">–</div>
      <div class="railflag" id="railFlagNote"></div>
    </div>
    <div style="margin-top:18px;border-top:1px solid var(--rule);padding-top:10px">
      <div class="railnote" id="railChecks"></div>
    </div>
  </aside>

  <main>
    <!-- TAB 1 -->
    <section id="panel1" role="tabpanel" aria-labelledby="tab1">
      <h2 class="fig" style="margin-top:0">Did the app find everything the document has?</h2>
      <p class="how">How this is computed: the page's code splits the converter's text on every page, drops the header and footer lines, and reads numbered paragraphs and headings from what remains. Nothing is estimated and no model is called.</p>
      <div class="tiles" id="tiles"></div>
      <div id="mismatchList"></div>

      <h2 class="fig">Take the paragraphs away</h2>
      <p class="how">How this is computed: the paragraph records built on this page are written to a file in your browser; the dataset travels with its source, fields and known limitations.</p>
      <button class="btn" id="dlJson">Download JSON</button>
      <button class="btn" id="dlMd">Download Markdown</button>
      <span class="note" id="dlNote"></span>

      <button class="collapser" id="checksToggle" aria-expanded="false"><span>Every check</span><span id="checksCount"></span></button>
      <div id="checksPanel" hidden></div>

      <button class="collapser" id="flagToggle" aria-expanded="false" style="margin-top:14px"><span>Flagged paragraphs</span><span id="flagCount"></span></button>
      <div id="flagPanel" hidden></div>
    </section>

    <!-- TAB 2 -->
    <section id="panel2" role="tabpanel" aria-labelledby="tab2" hidden>
      <h2 class="fig" style="margin-top:0">What does each paragraph say, and how do I cite it?</h2>
      <p class="how">How this is computed: each row is a numbered paragraph read from the converter's text, verbatim; the check column compares its first six words with the document's reference. Click a row to read it in full.</p>
      <button class="collapser" id="headToggle" aria-expanded="false"><span>Headings found</span><span id="headCount"></span></button>
      <div id="headPanel" hidden></div>
      <table>
        <caption id="tab2caption"></caption>
        <thead><tr>
          <th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">Page</th><th scope="col">First line</th><th scope="col">Check</th>
        </tr></thead>
        <tbody id="paraRows"></tbody>
      </table>
      <p class="note" id="tab2note"></p>
    </section>
  </main>
</div>

<footer class="app"><div class="wrap" id="footline"></div></footer>

<script>
(function(){
"use strict";
var D = window.WORKSHOP_DATA.pdf_text || {};
var recs = (D.records||[]).slice().sort(function(a,b){return a.page-b.page;});
var sym = D.symbol || "";
var ref = D.reference || null;
var hasRef = !!(ref && ref.paragraphs && ref.first_words);

/* ---------- classification helpers ---------- */
var isLabel = function(t){ return /^([IVX]+|[A-Z])\.$/.test(t); };
var isRomanLabel = function(t){ return /^[IVX]+\.$/.test(t); };
var isParaStart = function(t){ return /^(\d{1,3})\.( |$)/.test(t); };
var headingTest = function(t){
  return t.length>0 && t.length<=90 && /^[A-Z]/.test(t) && !/[.;:,\d]$/.test(t);
};

/* ---------- pass 1: header / footer ---------- */
var headerPages=0, headerWarn=[], pageNumPages=[], bareFoot=[], footerLineCount=0;
var body=[]; // {text,page,cls}
var totalNonEmpty=0;
var hyphenEnd=0;

recs.forEach(function(rec){
  var lines = (rec.text||"").split("\n").map(function(l){return l.replace(/\r$/,"");});
  totalNonEmpty += lines.filter(function(l){return l.trim()!=="";}).length;
  lines.forEach(function(l){ if(/-$/.test(l.trim())) hyphenEnd++; });
  // header
  var i0=-1; for(var i=0;i<lines.length;i++){ if(lines[i].trim()!==""){i0=i;break;} }
  if(i0>=0 && lines[i0].trim()===sym){ headerPages++; lines.splice(i0,1); }
  else headerWarn.push(rec.page);
  // footer
  var end=lines.length;
  while(end>0){
    var l=lines[end-1].trim();
    if(l===""){ end--; continue; }
    if(/^GE\./.test(l)){ footerLineCount++; end--; continue; }
    if(/^(\d{6})( \d{6})*$/.test(l)){ footerLineCount++; end--; continue; }
    if(/^\d{1,3}$/.test(l)){
      footerLineCount++;
      if(Number(l)===rec.page) pageNumPages.push(rec.page);
      else bareFoot.push({page:rec.page,num:l});
      end--; continue;
    }
    break;
  }
  for(var k=0;k<end;k++){
    if(lines[k].trim()!=="") body.push({text:lines[k].trim(),page:rec.page,cls:null});
  }
});

/* ---------- pass 2: paragraphs and headings ---------- */
var paras=[], headings=[], order=[];
var curPara=null, seenParaStart=false, romanText=null, curHead=null;

var paraStartMatch = function(t){ return t.match(/^(\d{1,3})\.(?:$| (.*)$)/); };

for(var i=0;i<body.length;i++){
  var line=body[i], t=line.text;

  if(isLabel(t)){
    var level = isRomanLabel(t)?2:3;
    var parts=[], j=i+1;
    while(j<body.length && !isLabel(body[j].text) && !paraStartMatch(body[j].text)){
      parts.push(body[j].text); body[j].cls="heading"; j++;
    }
    var h = {level:level, num:t.replace(/\.$/,""), text:parts.join(" "), roman:level===2};
    headings.push(h); order.push({type:"heading",h:h});
    if(level===2) romanText = (h.num+". "+h.text);
    curHead = h;
    i=j-1; continue;
  }
  var m = paraStartMatch(t);
  if(m){
    curPara = {num:Number(m[1]), lines:[], flags:[], suspectIdx:{}};
    if(m[2]!==undefined && m[2]!=="") curPara.lines.push({text:m[2],page:line.page});
    body[i].cls="para";
    paras.push(curPara); order.push({type:"para",p:curPara});
    seenParaStart=true; continue;
  }
  // unlabelled heading: next line is a paragraph start
  if(seenParaStart && i+1<body.length && paraStartMatch(body[i+1].text) && headingTest(t)){
    var startTxt = t, startIdx = i;
    if(i>0 && body[i-1].cls==="para" && headingTest(body[i-1].text)){
      // two-line heading: pull last line out of previous paragraph
      var prev = body[i-1];
      startTxt = prev.text+" "+t;
      if(curPara && curPara.lines.length && curPara.lines[curPara.lines.length-1].text===prev.text){
        curPara.lines.pop();
      }
      prev.cls="heading"; startIdx=i-1;
    }
    var uh={level:3,num:null,text:startTxt,roman:false,unlabelled:true};
    headings.push(uh); order.push({type:"heading",h:uh});
    curHead=uh; body[i].cls="heading"; continue;
  }
  if(!seenParaStart){ body[i].cls="cover"; continue; }
  if(curPara){ body[i].cls="para"; curPara.lines.push({text:t,page:line.page}); }
  else body[i].cls="cover";
}

/* ---------- paragraph text, pages, suspect lines ---------- */
var suspectLineTotal=0, suspectPagesSet={}, suspectParaCount=0;

paras.forEach(function(p){
  p.page_start = p.lines.length? p.lines[0].page : null;
  p.page_end   = p.lines.length? p.lines[p.lines.length-1].page : null;
  p.text = p.lines.map(function(l){return l.text;}).join(" ").replace(/ {2,}/g," ").trim();
  p.text_lines = p.lines.map(function(l){return l.text;}).join(" | ");
  p.section = curHeadFor(p);
  p.flagged=false; p.reasons=[];
  // suspect lines
  var susActivePage=null;
  p.lines.forEach(function(l,idx){
    var isSus=false;
    if(/^\d{1,3}$/.test(l.text)){ isSus=true; if(p.reasons.indexOf("bare number")<0)p.reasons.push("bare number"); }
    else if(/^\d{1,3} [A-Z\u201C"]/.test(l.text) || /^\* /.test(l.text)){
      isSus=true;
      var why = /^\* /.test(l.text) ? "starts with an asterisk" : "starts with a number and a space";
      if(p.reasons.indexOf(why)<0)p.reasons.push(why);
    }
    if(susActivePage===l.page) isSus=true;
    if(isSus){ l.suspect=true; p.suspectIdx[idx]=true; susActivePage=l.page; suspectLineTotal++; suspectPagesSet[l.page]=true; }
  });
  if(p.lines.some(function(l){return l.suspect;})){ p.flagged=true; suspectParaCount++; }
  var words = p.text.split(/\s+/).filter(Boolean).length;
  p.word_count=words;
  if(words>300){ p.flagged=true; if(p.reasons.indexOf("paragraph over 300 words")<0)p.reasons.push("paragraph over 300 words"); }
});

function curHeadFor(p){
  // nearest heading recorded before this paragraph in `order`
  var sec=null, part=null;
  for(var k=0;k<order.length;k++){
    var o=order[k];
    if(o.type==="heading"){ if(o.h.roman) part=o.h.num+". "+o.h.text; sec=o.h; }
    else if(o.p===p) break;
  }
  p.part = part;
  return sec ? (sec.num ? sec.num+". "+sec.text : sec.text) : "";
}

/* ---------- first words ---------- */
var ABBR = /^(no|art|para|paras|vol|p|pp|sec)\.$/i;
function stripGlued(tok){
  return tok.replace(/\d+$/, function(d){
    // only cut when digits are glued to a word or punctuation (i.e. token is not all digits)
    return tok.length>d.length ? "" : d;
  });
}
function firstWords(text){
  var raw = text.split(/\s+/).filter(Boolean);
  var kept=[], prev="";
  for(var i=0;i<raw.length && kept.length<6;i++){
    var tok = raw[i];
    var t = stripGlued(tok);
    if(/^\d+$/.test(t)){
      var prevEnds = /[.,\u201D"]$/.test(prev) && !ABBR.test(prev);
      if(kept.length>0 && prevEnds){ continue; }
    }
    kept.push(t); prev=t;
  }
  return kept.join(" ");
}
function norm(s){
  return (s||"").replace(/\u2018|\u2019/g,"'").replace(/\u201C|\u201D/g,'"")
    .replace(/\u2013|\u2014/g,"-").replace(/\s+/g," ").trim();
}
paras.forEach(function(p){
  p.fw = firstWords(p.text);
  if(hasRef){
    var r = ref.first_words[String(p.num)];
    p.fw_match = (r!==undefined) ? norm(p.fw)===norm(r) : null;
    p.fw_ref = (r!==undefined)? r : "(no reference entry)";
  } else { p.fw_match=null; p.fw_ref=null; }
});

/* ---------- checks ---------- */
var mismatches = hasRef ? paras.filter(function(p){return p.fw_match===false;}) : [];
var seq_ok = true; var seq_probs=[];
(function(){
  var seen={};
  paras.forEach(function(p){
    if(seen[p.num]) seq_probs.push("duplicate "+p.num);
    seen[p.num]=true;
  });
  for(var n=1;n<=paras.length;n++){ if(!seen[n]) seq_probs.push("missing "+n); }
  var ordered = paras.every(function(p,idx){return p.num===idx+1;});
  if(!ordered && seq_probs.length===0) seq_probs.push("not in order");
  seq_ok = seq_probs.length===0;
})();
var unclassified = body.filter(function(l){return l.cls===null;});
var exportRecs = paras.map(function(p){
  return {
    symbol: sym, paragraph: p.num, section: p.section, part: p.part||"",
    page_start: p.page_start, page_end: p.page_end,
    text: p.text, text_lines: p.text_lines,
    flagged: p.flagged, first_words_match: p.fw_match,
    citation: sym+", para. "+p.num, doc_url: D.doc_url||"",
    limitations: p.flagged
      ? "footnotes not separated; "+(p.reasons.length? p.reasons[0] : "footnote text")+" may sit inside this paragraph"
      : "footnotes not separated"
  };
});
var roundtrip_ok = false;
try{ roundtrip_ok = JSON.parse(JSON.stringify(exportRecs)).length === paras.length; }catch(e){}

var checks=[];
function addCheck(ran,name,detail,pass,linkTo){
  checks.push({ran:ran,name:name,detail:detail,pass:pass,linkTo:linkTo||null});
}
addCheck(hasRef,"Paragraph count",
  hasRef ? paras.length+" found, "+ref.paragraphs+" expected" : "no reference in this file",
  hasRef ? paras.length===ref.paragraphs : null);
addCheck(true,"Numbering", seq_ok? "exactly 1 to "+paras.length+" in order" : seq_probs.join("; "),
  seq_ok);
addCheck(hasRef,"First words",
  hasRef ? (mismatches.length===0 ? "all "+ref.paragraphs+" match the reference" : mismatches.length+" of "+paras.length+" differ") : "no reference in this file",
  hasRef ? mismatches.length===0 : null, mismatches.length? "mismatch" : null);
addCheck(true,"Paragraphs flagged",
  paras.length? flagCountText() : "no paragraphs found", true, flagAny()? "flagged":null);
addCheck(true,"Suspect lines",
  suspectLineTotal+" suspect lines on "+Object.keys(suspectPagesSet).length+" pages, in "+suspectParaCount+" paragraphs; none removed", true);
addCheck(true,"Headers and footers",
  headerPages+" of "+recs.length+" pages open with the symbol; "+pageNumPages.length+" pages carry their page number in the footer; "+bareFoot.length+" bare numbers removed from the footer"+(bareFoot.length? " ("+bareFoot.map(function(b){return "p."+b.page+" no."+b.num;}).join(", ")+")" : ""),
  headerPages===recs.length && pageNumPages.length===Math.max(0,recs.length-1));
addCheck(true,"Headings",
  headings.filter(function(h){return !h.unlabelled;}).length+" labelled and "+headings.filter(function(h){return h.unlabelled;}).length+" unlabelled headings found", true, "headings");
addCheck(true,"Nothing lost",
  unclassified.length===0
    ? (headerPages+footerLineCount+body.length)+" of "+totalNonEmpty+" non-empty lines classified (header, footer, cover, heading, paragraph)"
    : unclassified.length+" unclassified lines: "+unclassified.slice(0,5).map(function(l){return "p."+l.page+" “"+l.text.slice(0,40)+"”";}).join("; "),
  unclassified.length===0);
addCheck(true,"Export round trip",
  exportRecs.length+" records parse back, matching the "+paras.length+" rows of the table", roundtrip_ok);

function flagCountText(){
  var pages = {}; paras.forEach(function(p){ if(p.flagged){ (p.lines||[]).forEach(function(l){pages[l.page]=true;}); } });
  return flagCount()+" paragraphs flagged on "+Object.keys(pages).length+" pages, to check against the PDF";
}
function flagCount(){ return paras.filter(function(p){return p.flagged;}).length; }
function flagAny(){ return flagCount()>0; }

var ranChecks = checks.filter(function(c){return c.ran;});
var passed = ranChecks.filter(function(c){return c.pass;}).length;
var failed = ranChecks.length - passed;

/* ---------- render ---------- */
var $ = function(id){return document.getElementById(id);};
$("doctitle").textContent = D.title || "(untitled document)";
$("docmeta").innerHTML = "";
(function(){
  var bits=[];
  if(D.doc_url) bits.push('<a href="'+esc(D.doc_url)+'" target="_blank" rel="noopener">'+esc(sym)+'</a>');
  else bits.push(esc(sym));
  if(ref && ref.adopted) bits.push("adopted "+esc(ref.adopted));
  bits.push(recs.length+" pages");
  if(D.source) bits.push(esc(D.source));
  $("docmeta").innerHTML = bits.join(" · ");
})();
function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}

$("statusbox").innerHTML = failed>0
  ? '<span class="dot bad"></span>'+failed+' check'+(failed>1?"s":"")+' failed<br>'
  : '<span class="dot ok"></span>'+passed+' of '+ranChecks.length+' checks pass<br>';
$("statusbox").innerHTML += '<span style="color:var(--red)">'+flagCount()+' paragraphs flagged</span>';

$("railSymbol").textContent = sym;
$("railTitle").textContent = D.title || "";
$("railParaN").textContent = paras.length;
$("railParaN").className = "bignum" + ((hasRef && paras.length!==ref.paragraphs) || paras.length===0 ? " bad":"");
(function(){
  var pct = hasRef ? Math.min(100, Math.round(paras.length/ref.paragraphs*100)) : 0;
  var bar=$("railParaBar"); bar.innerHTML='<i style="width:'+pct+'%"></i>';
  bar.className = "bar" + ((hasRef && paras.length!==ref.paragraphs)?" bad":"");
  $("railParaNote").textContent = hasRef
    ? "of "+ref.paragraphs+" in the reference"
    : "no reference in this file";
})();
$("railFlagN").textContent = flagCount();
$("railFlagN").className = "bignum" + (flagCount()>0?" bad":"");
$("railFlagNote").textContent = flagCount()>0
  ? "of "+paras.length+" paragraphs found — footnote text may sit inside: check them against the PDF"
  : "no paragraphs flagged";
$("railChecks").innerHTML = failed>0
  ? '<span class="badword">✗ '+failed+' of '+ranChecks.length+' checks failed</span>'
  : '<span class="'+(ranChecks.length? "okword":"")+'">✓ '+passed+' of '+ranChecks.length+' checks pass</span>';

/* tiles */
var tilesData=[
  {n:paras.length, cls: hasRef ? (paras.length===ref.paragraphs?"ok":"bad") : "",
   title:"Paragraphs found",
   sub: hasRef ? "the document has "+ref.paragraphs+(paras.length!==ref.paragraphs? " (difference "+(paras.length-ref.paragraphs)+")":"") : "no reference in this file",
   how:"Numbered lines matching “n.” alone or with text, counted across all pages."},
  {n: hasRef ? (paras.length-mismatches.length) : "–", cls: hasRef ? (mismatches.length?"bad":"ok") : "",
   title:"First words match",
   sub: hasRef? "of "+ref.paragraphs+" expected" : "no reference in this file",
   how:"The first six words of each paragraph, footnote marks removed, compared with the reference."},
  {n:flagCount(), cls: flagCount()>0?"bad":"",
   title:"Paragraphs flagged",
   sub: flagCount()>0 ? "of "+paras.length+" found, on "+Object.keys((function(){var pp={};paras.forEach(function(p){if(p.flagged)p.lines.forEach(function(l){pp[l.page]=true;});});return pp;})()).length+" pages" : "none",
   how:"A paragraph is flagged when a line looks like footnote text (a bare number, or a number and a space before a capital) or it runs over 300 words."},
  {n:"–", cls:"", title:"Footnotes", sub:"not separated",
   how:"The document has "+(hasRef?ref.footnotes:"?")+" footnotes; this version leaves them in place and flags the paragraphs where they may sit."}
];
$("tiles").innerHTML = tilesData.map(function(t){
  return '<div class="tile"><div class="t '+t.cls+'">'+esc(t.n)+'</div><div><strong>'+esc(t.title)+'</strong></div><div class="sub">'+esc(t.sub)+'</div><div class="h">'+esc(t.how)+'</div></div>';
}).join("");

/* mismatch list */
if(mismatches.length){
  var mm = mismatches.slice(0,10).map(function(p){
    return '<div class="misline">para. '+p.num+': found “'+esc(p.fw)+'” / reference “'+esc(p.fw_ref)+'”</div>';
  }).join("");
  if(mismatches.length>10) mm += '<div class="misline">and '+(mismatches.length-10)+' more</div>';
  $("mismatchList").innerHTML = '<h2 class="fig">Paragraphs whose first words differ</h2>'+mm;
}

/* downloads */
function today(){ var d=new Date(); return d.toISOString().slice(0,10); }
function fileBase(){ return (sym||"document").replace(/\//g,"-"); }
function download(content,mime,name){
  var blob=new Blob([content],{type:mime+";charset=utf-8"});
  var url=URL.createObjectURL(blob);
  var a=document.createElement("a"); a.href=url; a.download=name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function(){URL.revokeObjectURL(url);},2000);
}
$("dlJson").disabled = paras.length===0;
$("dlMd").disabled = paras.length===0;
$("dlJson").addEventListener("click",function(){
  download(JSON.stringify(exportRecs,null,2),"application/json",fileBase()+".json");
});
$("dlMd").addEventListener("click",function(){
  var L=[];
  L.push("---");
  L.push("title: "+(D.title||""));
  L.push("symbol: "+sym);
  if(ref&&ref.adopted) L.push("adopted: "+ref.adopted);
  L.push("source_url: "+(D.doc_url||""));
  L.push("extracted: "+today());
  L.push("paragraphs_found: "+paras.length);
  L.push("paragraphs_expected: "+(hasRef?ref.paragraphs:"unknown"));
  L.push("paragraphs_flagged: "+flagCount());
  L.push('footnotes: "not separated; the document has '+(hasRef?ref.footnotes:"?")+'"');
  L.push("---");
  L.push("");
  order.forEach(function(o){
    if(o.type==="heading"){
      L.push("");
      L.push((o.h.level===2?"## ":"### ")+esc(o.h.num? o.h.num+". "+o.h.text : o.h.text));
      L.push("");
    } else {
      L.push("**"+o.p.num+".** "+o.p.text+(o.p.flagged?" *(flagged: may contain footnote text)*":""));
      L.push("");
    }
  });
  download(L.join("\n"),"text/markdown",fileBase()+".md");
});
if(paras.length===0) $("dlNote").textContent = "exports disabled: no paragraphs were found in this file.";

/* checks panel */
$("checksCount").textContent = "("+ranChecks.length+")";
$("checksPanel").innerHTML = '<p class="note">Each check states what was compared, on this data, with this code, and what was expected. A failed check never hides a result.</p>'+
 checks.map(function(c){
   if(!c.ran) return '<div class="checkline"><span class="mono">NOT RUN</span><span><strong>'+esc(c.name)+'</strong> — '+esc(c.detail)+'</span></div>';
   var mark = c.pass? '<span class="okword">pass</span>' : '<span class="badword">check failed</span>';
   return '<div class="checkline"><span class="val" style="min-width:96px">'+mark+'</span><span><strong>'+esc(c.name)+'</strong> — '+esc(c.detail)+'</span></div>';
 }).join("");

/* flagged panel */
$("flagCount").textContent = "("+flagCount()+")";
(function(){
  var flagged = paras.filter(function(p){return p.flagged;});
  if(!flagged.length){ $("flagPanel").innerHTML='<p class="note">No paragraphs flagged.</p>'; return; }
  var rows = flagged.map(function(p){
    var sus = p.lines.filter(function(l){return l.suspect;}).map(function(l){return l.text;});
    var susTxt = sus.slice(0,2).map(function(s){return esc(s.length>60?s.slice(0,60)+"…":s);}).join(" · ") + (sus.length>2?" · +"+(sus.length-2):"");
    return '<tr data-para="'+p.num+'" class="flagrow"><td class="num"><button class="expander" data-open="'+p.num+'">'+p.num+'</button></td><td class="num">'+p.page_start+(p.page_end!==p.page_start?"–"+p.page_end:"")+'</td><td>'+susTxt+'</td><td>'+esc(p.reasons.join("; "))+'</td></tr>';
  }).join("");
  $("flagPanel").innerHTML =
    '<p class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</p>'+
    '<table><caption class="mono">TAB.01a</caption><thead><tr><th scope="col" class="num">Paragraph</th><th scope="col" class="num">Page</th><th scope="col">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>'+rows+'</tbody></table>';
})();

/* headings panel (tab 2) */
$("headCount").textContent = "("+headings.length+")";
$("headPanel").innerHTML = headings.length
  ? '<table><caption class="mono">TAB.02a</caption><thead><tr><th scope="col">Level</th><th scope="col">Heading</th></tr></thead><tbody>'+
    headings.map(function(h){
      return '<tr><td>'+(h.level===2?"section (roman)":"subsection")+(h.unlabelled?" · unlabelled":"")+'</td><td>'+esc((h.num?h.num+". ":"")+h.text)+'</td></tr>';
    }).join("")+'</tbody></table>'
  : '<p class="note">No headings found.</p>';

/* tab 2 table */
$("tab2caption").innerHTML = (paras.length+" paragraphs found"+(hasRef?", "+ref.paragraphs+" expected":"")+" · <span class='mono'>TAB.02</span>");
$("paraRows").innerHTML = paras.map(function(p){
  var first = p.text.length>120 ? p.text.slice(0,120).replace(/\s+\S*$/,"")+"…" : p.text;
  var check = p.flagged ? '<span class="badword">may contain footnote text</span>'
    : (p.fw_match===false ? '<span class="badword">first words differ</span>' : "OK");
  var page = p.page_start + (p.page_end!==p.page_start ? "–"+p.page_end : "");
  return '<tr class="prow" data-para="'+p.num+'">'+
    '<td class="num"><button class="expander" data-open="'+p.num+'" aria-expanded="false">'+p.num+'</button></td>'+
    '<td>'+esc(p.section)+'</td><td class="num">'+page+'</td>'+
    '<td>'+esc(first)+'</td><td>'+check+'</td></tr>'+
    '<tr class="detail" hidden><td colspan="5" id="detail-'+p.num+'"></td></tr>';
}).join("");
$("tab2note").textContent = paras.length
  ? "Full text is verbatim as computed from the converter's lines; suspect lines are boxed in red and left in place."
  : "No paragraphs were found in this file.";

function detailHTML(p){
  var path = [];
  var sec=null, part=null;
  for(var k=0;k<order.length;k++){
    var o=order[k];
    if(o.type==="heading"){ if(o.h.roman) part=o.h.num+". "+o.h.text; sec=o.h; }
    else if(o.p===p) break;
  }
  var fullText = p.lines.map(function(l,idx){
    return l.suspect ? '<span class="suspect">'+esc(l.text)+'</span>' : esc(l.text);
  }).join(" ");
  var h = '<div class="parafull">'+fullText+'</div>';
  h += '<div class="refcmp">Path: '+esc((part?part+" › ":"")+(p.section||""))+' · Page '+(p.page_start+(p.page_end!==p.page_start?"–"+p.page_end:""))+' · '+p.word_count+' words</div>';
  if(hasRef){
    h += '<div class="refcmp">First six words — found: “'+esc(p.fw)+'”'+(p.fw_match===false?' <span class="badword">(differs)</span>':' <span class="okword">(matches)</span>')+' · reference: “'+esc(p.fw_ref)+'”</div>';
  }
  h += '<div style="margin:8px 0"><button class="copybtn" data-copy="'+p.num+'">Copy citation</button> ';
  h += '<span class="mono" style="margin-left:8px">'+esc(sym)+', para. '+p.num+'</span></div>';
  h += '<button class="expander" data-lines="'+p.num+'" aria-expanded="false" style="font-size:13px">Show the PDF’s lines</button>';
  h += '<div class="linelist" id="lines-'+p.num+'" hidden>';
  var lastPage=null;
  p.lines.forEach(function(l){
    if(l.page!==lastPage){ h += '<span class="pagemark">— page '+l.page+' —\n</span>'; lastPage=l.page; }
    h += (l.suspect?"[S] ":"")+esc(l.text)+"\n";
  });
  h += '</div>';
  return h;
}

/* expansion */
document.addEventListener("click",function(e){
  var t=e.target;
  var openBtn = t.closest ? t.closest("[data-open]") : null;
  if(openBtn && openBtn.tagName==="BUTTON" && openBtn.dataset.open!==undefined && openBtn.closest("#paraRows")){
    var num=Number(openBtn.dataset.open);
    togglePara(num);
    return;
  }
  var lineBtn = t.closest ? t.closest("[data-lines]") : null;
  if(lineBtn){
    var n2=Number(lineBtn.dataset.lines);
    var box=$("lines-"+n2);
    box.hidden=!box.hidden;
    lineBtn.setAttribute("aria-expanded",String(!box.hidden));
    lineBtn.textContent = box.hidden? "Show the PDF’s lines" : "Hide the PDF’s lines";
    return;
  }
  var copyBtn = t.closest ? t.closest("[data-copy]") : null;
  if(copyBtn){
    var n3=Number(copyBtn.dataset.copy);
    var cit=sym+", para. "+n3;
    function done(){ copyBtn.textContent="Copied"; setTimeout(function(){copyBtn.textContent="Copy citation";},2000); }
    if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(cit).then(done,done); }
    else{ var ta=document.createElement("textarea"); ta.value=cit; document.body.appendChild(ta); ta.select(); try{document.execCommand("copy");}catch(x){} ta.remove(); done(); }
    return;
  }
  var row = t.closest ? t.closest("tr.prow") : null;
  if(row){ togglePara(Number(row.dataset.para)); return; }
  var frow = t.closest ? t.closest("tr.flagrow") : null;
  if(frow){ selectTab(1); togglePara(Number(frow.dataset.para), true);
    var r=$("row-"+frow.dataset.para); return; }
});

function togglePara(num, forceOpen){
  var btn=document.querySelector('#paraRows button[data-open="'+num+'"]');
  if(!btn) return;
  var row=btn.closest("tr");
  var detail=row.nextElementSibling;
  var open = forceOpen===true ? true : detail.hidden;
  if(open && !detail.dataset.filled){ detail.firstElementChild.innerHTML=detailHTML(paras.find(function(p){return p.num===num;})); detail.dataset.filled="1"; }
  detail.hidden=!open;
  btn.setAttribute("aria-expanded",String(open));
  if(open) detail.scrollIntoView({block:"nearest"});
}

/* collapsers */
[["checksToggle","checksPanel"],["flagToggle","flagPanel"],["headToggle","headPanel"]].forEach(function(pair){
  $(pair[0]).addEventListener("click",function(){
    var p=$(pair[1]); p.hidden=!p.hidden;
    this.setAttribute("aria-expanded",String(!p.hidden));
  });
});

/* tabs */
var tabs=[$("tab1"),$("tab2")], panels=[$("panel1"),$("panel2")];
function selectTab(idx){
  tabs.forEach(function(tb,i){
    tb.setAttribute("aria-selected",String(i===idx));
    tb.tabIndex = i===idx?0:-1;
    panels[i].hidden = i!==idx;
  });
  tabs[idx].focus();
}
tabs.forEach(function(tb,i){ tb.addEventListener("click",function(){selectTab(i);}); });
$("tab1").parentNode.addEventListener("keydown",function(e){
  var idx = tabs.indexOf(document.activeElement);
  if(idx<0) return;
  if(e.key==="ArrowRight"){ e.preventDefault(); selectTab((idx+1)%2); }
  if(e.key==="ArrowLeft"){ e.preventDefault(); selectTab((idx+1)%2); }
  if(e.key==="Home"){ e.preventDefault(); selectTab(0); }
  if(e.key==="End"){ e.preventDefault(); selectTab(1); }
});

/* footer */
(function(){
  var bits=[];
  if(D.source) bits.push(esc(D.source));
  if(D.built) bits.push("built "+esc(D.built));
  bits.push("Done by this page's code; no model was called and nothing left the browser.");
  $("footline").textContent = bits.join(" · ");
})();
})();
</script>
</body>
</html>
```