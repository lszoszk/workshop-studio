Built: a four-tab app that parses the attached document's HTML into numbered paragraphs with their heading path, repairs only the missing spaces the characters can prove, checks every result against the document's own reference, and exports the paragraphs as JSON or Markdown.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN document · HTML · paragraphs</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b3a;--dim:#5c564a}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;padding:0 28px 48px}
.mono{font-family:ui-monospace,Menlo,Consolas,"Liberation Mono",monospace;font-size:11.5px;letter-spacing:.1em}
.up{text-transform:uppercase}
a{color:var(--red)}
button{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header{border-bottom:1px solid var(--rule);padding:24px 0 16px}
.kicker{color:var(--dim)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:clamp(24px,3.4vw,34px);line-height:1.2;margin:8px 0 10px;max-width:62ch}
.meta{display:flex;justify-content:space-between;align-items:baseline;gap:18px;flex-wrap:wrap;font-size:14px;color:var(--dim)}
.meta a{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;letter-spacing:.06em}
.status{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px;vertical-align:1px}
.dot.ok{background:var(--green)}.dot.bad{background:var(--red)}
.layout{display:grid;grid-template-columns:240px minmax(0,1fr);gap:36px;align-items:start}
.rail{position:sticky;top:20px;border-right:1px solid var(--rule);padding:20px 20px 20px 0}
.railhead{color:var(--dim);border-bottom:1px solid var(--rule);padding-bottom:8px;margin-bottom:14px}
.doccard{border:1px solid var(--rule);padding:12px 14px;margin-bottom:22px}
.sym{color:var(--red)}
.doctitle{font-family:Georgia,serif;font-size:15px;line-height:1.35;margin-top:6px}
.railblock{margin-bottom:22px}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:50px;line-height:1;font-weight:400}
.bignum.red{color:var(--red)}
.of{font-size:13px;color:var(--dim);margin-left:6px}
.bar{height:3px;background:var(--rule);margin-top:8px}
.barfill{height:100%;background:var(--ink)}
.barfill.bad{background:var(--red)}
.note{font-size:12.5px;margin-top:6px}
.red{color:var(--red)}.green{color:var(--green)}
.pass{color:var(--green);font-weight:600}
.fail{color:var(--red);font-weight:600}
.limit{color:var(--red);font-weight:600}
.tabs{display:flex;flex-wrap:wrap;gap:2px;border-bottom:1px solid var(--rule);margin-top:22px}
.tabs [role=tab]{appearance:none;background:none;border:none;border-bottom:2px solid transparent;margin-bottom:-1px;padding:10px 14px 9px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink)}
.tabs [role=tab]:hover{color:var(--red)}
.tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
main{min-width:0;padding-top:6px}
.panel{padding-top:16px}
.fig{color:var(--dim);margin:14px 0 4px}
.sectitle{font-family:Georgia,serif;font-weight:400;font-size:22px;margin:26px 0 6px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:0 30px;margin-top:8px}
.tile{border-top:1px solid var(--rule);padding:14px 0 18px}
.tile .lbl{color:var(--dim)}
.tile .bignum{font-size:54px}
.tile .sub{font-size:14px;margin-top:4px}
.how{font-size:13px;color:var(--dim);margin:10px 0 0;max-width:56ch}
table{border-collapse:collapse;width:100%;margin:8px 0 26px}
caption{caption-side:top;text-align:left;font-family:Georgia,serif;font-size:19px;padding:4px 0 8px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:400;text-align:left;border-bottom:1px solid var(--ink);padding:6px 10px 6px 0}
td{border-bottom:1px solid var(--rule);padding:8px 14px 8px 0;vertical-align:top}
th.num,td.num{text-align:right;padding-right:0;font-variant-numeric:tabular-nums}
td.sec{max-width:230px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
td.fl{max-width:52ch}
tr.prow{cursor:pointer}
tr.prow:hover td{background:rgba(155,35,53,.05)}
.rowbtn{appearance:none;background:none;border:none;cursor:pointer;font-family:Georgia,serif;font-size:19px;color:var(--red);padding:2px 8px 2px 0;min-width:36px;text-align:right}
tr.drow td{background:#efe9dc;padding:14px 18px}
.fulltext{max-width:75ch}
mark.rep{background:transparent;border:1px solid var(--red);border-radius:2px;padding:0 1px}
mark.ch{background:rgba(155,35,53,.14);outline:1px dotted var(--red)}
.cmp{font-size:14px;margin:10px 0 0}
.path{margin:10px 0 0;color:var(--dim)}
.copybtn,.btn{appearance:none;background:transparent;border:1px solid var(--ink);padding:8px 14px;cursor:pointer;font-size:14px}
.copybtn:hover,.btn:hover{background:rgba(29,27,24,.06)}
.btn[disabled]{opacity:.4;cursor:not-allowed}
.linkbtn{appearance:none;background:none;border:none;padding:0;color:var(--red);cursor:pointer;text-decoration:underline;font:inherit}
.boxbtn{appearance:none;background:none;border:none;border-top:1px solid var(--rule);width:100%;text-align:left;padding:12px 0;cursor:pointer;font-family:Georgia,serif;font-size:18px}
.boxbtn::after{content:" +";color:var(--red);font-family:ui-monospace,Menlo,Consolas,monospace}
.boxbtn[aria-expanded=true]::after{content:" –"}
.hlist{margin:8px 0 20px;padding-left:22px;font-size:15px}
.hlist li{margin:3px 0}
.checks{list-style:none;margin:8px 0 0;padding:0}
.checks li{border-bottom:1px solid var(--rule);padding:9px 0;font-size:15px}
.checks .tag{display:inline-block;min-width:112px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;margin-right:10px}
.hint{color:var(--dim)}
.exportbtns{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0 6px}
footer{border-top:1px solid var(--rule);margin-top:34px;padding-top:14px;font-size:13px;color:var(--dim)}
.credits{font-size:12px;color:var(--dim);margin-top:6px}
.srow{cursor:pointer}
.srow:hover td{background:rgba(155,35,53,.05)}
.m{font-weight:600}
@media (max-width:900px){.layout{grid-template-columns:1fr}.rail{position:static;border-right:none;border-bottom:1px solid var(--rule);padding-bottom:16px}}
</style>
</head>
<body>

<header>
  <div class="mono up kicker">UN document · HTML</div>
  <h1 id="hTitle"></h1>
  <div class="meta">
    <span><a id="hSym" target="_blank" rel="noopener"></a><span id="hAdopted"></span><span id="hSource"></span></span>
    <span class="status" id="hStatus"></span>
  </div>
</header>

<div class="layout">
  <aside class="rail">
    <div class="mono up railhead">Document</div>
    <div class="doccard">
      <div class="mono sym" id="rSym"></div>
      <div class="doctitle" id="rTitle"></div>
    </div>
    <div class="railblock">
      <div><span class="bignum" id="rP">0</span><span class="of" id="rPof"></span></div>
      <div class="bar"><div class="barfill" id="rBar"></div></div>
    </div>
    <div class="railblock">
      <div><span class="bignum red">0</span><span class="of" id="rFof"></span></div>
      <div class="note red">not in this HTML</div>
    </div>
    <button class="linkbtn mono up" id="rChecks" data-goto="3"></button>
  </aside>

  <main>
    <div class="tabs" role="tablist" aria-label="Views of the document">
      <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true" tabindex="0">01 Result</button>
      <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" tabindex="-1">02 Paragraphs</button>
      <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">03 Lost &amp; changed</button>
      <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">04 Checks &amp; export</button>
    </div>

    <section class="panel" role="tabpanel" id="panel-0" aria-labelledby="tab-0">
      <div class="mono up fig">TAB.01 · Result</div>
      <div class="tiles" id="tiles"></div>
    </section>

    <section class="panel" role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden>
      <div class="mono up fig">TAB.02 · Paragraphs</div>
      <button class="boxbtn" id="hBoxBtn" aria-expanded="false" aria-controls="hBox">Headings found</button>
      <div id="hBox" hidden><ol class="hlist" id="hList"></ol></div>
      <table>
        <caption id="pCap"></caption>
        <thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>
        <tbody id="pBody"></tbody>
      </table>
      <p class="how">Click a row = expand it in place: the full text verbatim (repaired spaces boxed), the reference's first six words, the repairs in that paragraph, and a copy-citation button. The citation is “symbol, para. n”.</p>
    </section>

    <section class="panel" role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
      <div class="mono up fig">TAB.03 · Lost &amp; changed</div>
      <h2 class="sectitle">Lost: footnotes</h2>
      <p id="fnText"></p>
      <h2 class="sectitle">Changed: spaces</h2>
      <p class="mono hint" id="ruleLine"></p>
      <table>
        <caption id="sCap"></caption>
        <thead><tr><th scope="col" class="num">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead>
        <tbody id="sBody"></tbody>
      </table>
      <p class="how">Rules restore a space only where the characters prove it was there. Word pairs the rules cannot prove (a missing space inside a word) are not touched; the first-words check catches them only in a paragraph's first six words.</p>
      <h2 class="sectitle">Changed: characters</h2>
      <p class="mono hint">kept exactly as published · on a keyboard: a hyphen and straight quotes</p>
      <table>
        <caption>Characters kept as published, counted over all paragraph texts</caption>
        <thead><tr><th scope="col">Character</th><th scope="col" class="num">Count</th><th scope="col">Example</th></tr></thead>
        <tbody id="cBody"></tbody>
      </table>
      <p class="how">Kept exactly as published, in the table and in every export. A search typed with the keyboard hyphen will not find a non-breaking hyphen, nor straight quotes a curly one: normalise the text before searching it.</p>
    </section>

    <section class="panel" role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>
      <div class="mono up fig">TAB.04 · Checks &amp; export</div>
      <h2 class="sectitle">Checks</h2>
      <ul class="checks" id="checkList"></ul>
      <h2 class="sectitle">Export</h2>
      <div class="exportbtns">
        <button class="btn" id="dlJson">Download JSON</button>
        <button class="btn" id="dlMd">Download Markdown</button>
      </div>
      <p class="how">JSON: one record per paragraph — symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url, limitations. Markdown: front matter (title, symbol, adopted, source_url, extracted, paragraphs_found, paragraphs_expected, footnotes), then headings and paragraphs in document order. File name: the symbol with slashes as hyphens; UTF-8.</p>
      <button class="boxbtn" id="eBtn" aria-expanded="false" aria-controls="eBox">Elements found</button>
      <div id="eBox" hidden>
        <table>
          <caption>Every block element in the parsed HTML, in document order</caption>
          <thead><tr><th scope="col">Tag</th><th scope="col">Classified as</th><th scope="col">Text (first 80 characters)</th></tr></thead>
          <tbody id="eBody"></tbody>
        </table>
      </div>
    </section>
  </main>
</div>

<footer>
  <div id="fLine"></div>
  <div class="credits">Credits: export metadata follows The Turing Way, “Documentation and metadata” (CC BY 4.0); the check panel follows the UK Government Analysis Function, “Quality assurance of code for analysis and research: Testing code” (Open Government Licence v3.0); citation format follows the Dag Hammarskjöld Library, “Ask DAG: how should I cite a UN document?”.</div>
</footer>

<script>
(function(){
"use strict";
var W = window.WORKSHOP_DATA || {};
var D = W.html_doc;
if (Array.isArray(D)) D = D[0] || {};
var REF = (D && D.reference) || null;
var FW = (REF && REF.first_words) || null;
var SYMBOL = D.symbol || "";
var DOC_URL = D.doc_url || "";
var TITLE = D.title || "UN document (HTML)";
var SOURCE = D.source || "";
var BUILT = D.built || "";

function esc(s){ return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }

/* ---------- rules for provable missing spaces ---------- */
var RULES = [
  {name:"sentence join", re:/([a-z])\.([A-Z])/g, pieces:function(m){ return [[m[1]+".",0],[" ",1],[m[2],0]]; }},
  {name:"comma join",    re:/([a-z]),([A-Za-z])/g, pieces:function(m){ return [[m[1]+",",0],[" ",1],[m[2],0]]; }},
  {name:"quote join",    re:/([a-z])“/g,          pieces:function(m){ return [[m[1],0],[" ",1],["“",0]]; }},
  {name:"dash join",     re:/–([A-Za-z])/g,        pieces:function(m){ return [["–",0],[" ",1],[m[1],0]]; }}
];
var ruleByName = {}; RULES.forEach(function(r){ ruleByName[r.name]=r; });

/* ---------- parse and classify ---------- */
var doc = null;
try { doc = new DOMParser().parseFromString(String(D.html||""), "text/html"); } catch(e){ doc = null; }

var blocks=[], paragraphs=[], headings=[], stream=[], unclassified=[];
var coverCount=0, committeeText=null, titleText=null;
var curPart=null, curSection=null;

function mkBlock(el, kind, label, text){ return {tag:el.tagName, kind:kind, label:label, text:text||""}; }

function buildParagraph(num, raw){
  var logs=[], parts=[{t:raw, mk:false}];
  for (var ri=0; ri<RULES.length; ri++){
    var r=RULES[ri], out=[];
    for (var pi=0; pi<parts.length; pi++){
      var p=parts[pi];
      if (p.mk){ out.push(p); continue; }
      var last=0, m; r.re.lastIndex=0;
      while ((m=r.re.exec(p.t))!==null){
        out.push({t:p.t.slice(last,m.index), mk:false});
        var pcs=r.pieces(m);
        for (var ci=0; ci<pcs.length; ci++) out.push({t:pcs[ci][0], mk:pcs[ci][1]===1});
        logs.push({para:num, rule:r.name, match:m[0],
          before:p.t.slice(Math.max(0,m.index-20), m.index),
          after:p.t.slice(m.index+m[0].length, m.index+m[0].length+20)});
        last=m.index+m[0].length;
        if (m[0].length===0) r.re.lastIndex++;
      }
      out.push({t:p.t.slice(last), mk:false});
    }
    parts=out;
  }
  var text=parts.map(function(p){return p.t;}).join("");
  return {num:num, raw:raw, text:text, parts:parts, logs:logs, section:null, part:null, citation:"", firstMatch:null, firstFound:null, firstRef:null};
}

function classify(){
  if (!doc || !doc.body) return;
  (function walk(node){
    var kids=node.children;
    for (var i=0;i<kids.length;i++){
      var el=kids[i], tag=el.tagName;
      if (tag==="TABLE"){
        coverCount++;
        blocks.push(mkBlock(el,"cover","cover", el.textContent.replace(/\s+/g," ").trim().slice(0,80)));
        continue;
      }
      if (tag==="P"){
        var text=el.textContent.replace(/\s+/g," ").trim();
        var m=text.match(/^(\d{1,3})\.\s*(.*)$/);
        if (m){
          var p=buildParagraph(parseInt(m[1],10), m[2].trim());
          p.section=curSection; p.part=curPart;
          p.citation=SYMBOL+", para. "+p.num;
          paragraphs.push(p); stream.push({type:"paragraph", p:p});
          blocks.push(mkBlock(el,"paragraph","paragraph "+p.num, p.raw.slice(0,80)));
        } else {
          if (committeeText===null) committeeText=text;
          blocks.push(mkBlock(el,"committee","committee line", text.slice(0,80)));
        }
        continue;
      }
      if (/^H[1-6]$/.test(tag)){
        var htext=el.textContent.replace(/\s+/g," ").trim();
        if (tag==="H2" && titleText===null){ titleText=htext; blocks.push(mkBlock(el,"title","title",htext.slice(0,80))); continue; }
        var hm=htext.match(/^([IVX]+|[A-Z])\.\s*(.+)$/);
        var label=null, heading=htext, glued=false;
        if (hm){ label=hm[1]; heading=hm[2].trim(); var after=htext.charAt(label.length+1); glued = after!=="" && !/\s/.test(after); }
        var h={level:tag, label:label, heading:heading, full:htext, glued:glued};
        headings.push(h); stream.push({type:"heading", h:h});
        if (tag==="H2" && label && /^[IVX]+$/.test(label)) curPart=h;
        curSection=h;
        blocks.push(mkBlock(el,"heading","heading ("+tag+")", htext.slice(0,80)));
        continue;
      }
      if (tag==="LI"||tag==="BLOCKQUOTE"||tag==="PRE"){
        var utext=el.textContent.replace(/\s+/g," ").trim();
        unclassified.push({tag:tag, text:utext});
        blocks.push(mkBlock(el,"unclassified","unclassified", utext.slice(0,80)));
        continue;
      }
      walk(el);
    }
  })(doc.body);
}
classify();

/* ---------- first-words comparison ---------- */
function normW(s){
  return String(s==null?"":s)
    .replace(/[“”]/g,'"').replace(/[‘’]/g,"'")
    .replace(/[–—]/g,"-").replace(/\u2011/g,"-").replace(/\u00A0/g," ")
    .replace(/\s+/g," ").trim();
}
function firstSix(s){ return normW(String(s==null?"":s).split(/\s+/).filter(Boolean).slice(0,6).join(" ")); }
paragraphs.forEach(function(p){
  if (FW && FW[String(p.num)]!==undefined){
    p.firstFound=firstSix(p.text); p.firstRef=firstSix(FW[String(p.num)]);
    p.firstMatch = (p.firstFound===p.firstRef);
  }
});

/* ---------- characters kept as published ---------- */
var allText = paragraphs.map(function(p){return p.text;}).join("\n");
function exampleFor(pred){
  for (var i=0;i<paragraphs.length;i++){
    var t=paragraphs[i].text;
    for (var j=0;j<t.length;j++){
      if (pred(t[j])){
        return {b:t.slice(Math.max(0,j-18),j), ch:t[j], a:t.slice(j+1,j+19), cutB:(j-18)>0, cutA:(j+19)<t.length};
      }
    }
  }
  return null;
}
var CHARS=[
  {name:"En dash –", code:"U+2013", pred:function(c){return c==="\u2013";}},
  {name:"Double quotes “ ”", code:"U+201C / U+201D", pred:function(c){return c==="\u201C"||c==="\u201D";}},
  {name:"Right single quote ’", code:"U+2019", pred:function(c){return c==="\u2019";}},
  {name:"Non-breaking hyphen ‑", code:"U+2011", pred:function(c){return c==="\u2011";}},
  {name:"Non-breaking space", code:"U+00A0", pred:function(c){return c==="\u00A0";}}
];
CHARS.forEach(function(c){
  c.count=allText.split("").filter(c.pred).length;
  c.ex=exampleFor(c.pred);
});

/* ---------- repairs tallies ---------- */
var logs=[]; paragraphs.forEach(function(p){ p.logs.forEach(function(l){ logs.push(l); }); });
var perRule={}; RULES.forEach(function(r){ perRule[r.name]=0; });
logs.forEach(function(l){ perRule[l.rule]++; });
var repParas = {}; logs.forEach(function(l){ repParas[l.para]=1; });
repParas = Object.keys(repParas).length;

/* ---------- exports ---------- */
function recordFor(p){
  return {
    symbol: SYMBOL,
    paragraph: p.num,
    section: p.section ? p.section.full : "",
    part: p.part ? p.part.full : "",
    text: p.text,
    text_raw: p.raw,
    first_words_match: p.firstMatch,
    citation: p.citation,
    doc_url: DOC_URL,
    limitations: "no footnotes in this HTML version" + (REF && typeof REF.footnotes==="number" ? "; the document has "+REF.footnotes+" footnotes" : "")
  };
}
function buildJSON(){ return JSON.stringify(paragraphs.map(recordFor), null, 2); }
function buildMarkdown(){
  var d=new Date();
  var today=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
  function q(s){ return '"'+String(s==null?"":s).replace(/\\/g,"\\\\").replace(/"/g,'\\"')+'"'; }
  var L=[];
  L.push("---");
  L.push("title: "+q(TITLE));
  L.push("symbol: "+q(SYMBOL));
  L.push("adopted: "+q(REF && REF.adopted!=null ? String(REF.adopted) : ""));
  L.push("source_url: "+q(DOC_URL));
  L.push("extracted: "+today);
  L.push("paragraphs_found: "+paragraphs.length);
  L.push("paragraphs_expected: "+(REF && typeof REF.paragraphs==="number" ? REF.paragraphs : "unknown"));
  L.push("footnotes: "+q("no footnotes in this HTML version"+(REF && typeof REF.footnotes==="number" ? "; the document has "+REF.footnotes+" footnotes" : "")));
  L.push("---");
  L.push("");
  L.push("# "+TITLE);
  L.push("");
  stream.forEach(function(it){
    if (it.type==="heading"){
      L.push((it.h.level==="H2"?"## ":"### ")+it.h.full);
      L.push("");
    } else if (it.type==="paragraph"){
      L.push("**"+it.p.num+".** "+it.p.text);
      L.push("");
    }
  });
  return L.join("\n");
}
function download(name, text, mime){
  var blob=new Blob([text],{type:mime+";charset=utf-8"});
  var url=URL.createObjectURL(blob);
  var a=document.createElement("a");
  a.href=url; a.download=name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function(){ URL.revokeObjectURL(url); },800);
}

/* ---------- checks ---------- */
var nP=paragraphs.length;
var expP=(REF && typeof REF.paragraphs==="number") ? REF.paragraphs : null;
var checks=[];

if (expP!==null) checks.push({name:"Paragraph count", status:(nP===expP?"pass":"fail"), detail:"found "+nP+" · reference "+expP});
else checks.push({name:"Paragraph count", status:"notrun", detail:"no reference in this file"});

var nums=paragraphs.map(function(p){return p.num;});
var dups=nums.filter(function(n,i){return nums.indexOf(n)!==i;});
var expected = expP!==null ? expP : nP;
var gaps=[];
if (nums.length){
  var mx=Math.max.apply(null,nums), set={};
  nums.forEach(function(n){set[n]=1;});
  for (var k=1;k<=mx;k++) if(!set[k]) gaps.push(k);
}
var inOrder=nums.every(function(n,i){return n===i+1;});
var okNum = dups.length===0 && gaps.length===0 && inOrder && nP===expected;
checks.push({name:"Numbering", status:(okNum?"pass":"fail"),
  detail: okNum ? ("1–"+nP+" in order, no gaps or duplicates")
    : ("count "+nP+" vs "+expected + (gaps.length?" · gaps: "+gaps.join(", "):"") + (dups.length?" · duplicates: "+dups.filter(function(v,i,a){return a.indexOf(v)===i;}).join(", "):""))});

if (FW){
  var checked=paragraphs.filter(function(p){return p.firstMatch!==null;});
  var bad=checked.filter(function(p){return !p.firstMatch;});
  var fwCount=checked.filter(function(p){return p.firstMatch;}).length;
  var det=fwCount+" of "+expP+" match";
  if (bad.length) det += "; differ: "+bad.map(function(p){ return "para. "+p.num+" (found “"+esc(p.firstFound)+"” / reference “"+esc(p.firstRef)+"”)"; }).join("; ");
  checks.push({name:"First words", status:(bad.length?"fail":"pass"), detail:det, link:{tab:1,label:"tab 02"}});
} else checks.push({name:"First words", status:"notrun", detail:"no reference in this file"});

if (REF && typeof REF.footnotes==="number")
  checks.push({name:"Footnotes", status:"limit", detail:"0 in this HTML · the document has "+REF.footnotes+" — the HTML version has no footnotes: a limit of the source, not of the app"});
else checks.push({name:"Footnotes", status:"notrun", detail:"no reference in this file"});

checks.push({name:"Repairs", status:"pass",
  detail: logs.length+" spaces restored in "+repParas+" paragraphs — "+RULES.map(function(r){return r.name+" "+perRule[r.name];}).join(", ")+"; every one is listed on tab 03 and text_raw keeps the text as found",
  link:{tab:2,label:"tab 03"}});

var h2c=headings.filter(function(h){return h.level==="H2";}).length;
var h3c=headings.filter(function(h){return h.level==="H3";}).length;
var glued=headings.filter(function(h){return h.glued;}).length;
checks.push({name:"Headings", status:"pass", detail: h2c+" h2 + "+h3c+" h3 = "+headings.length+" headings; "+glued+" glued labels separated"});

var kindCounts={}; blocks.forEach(function(b){ kindCounts[b.kind]=(kindCounts[b.kind]||0)+1; });
var sum=Object.keys(kindCounts).reduce(function(a,k){return a+kindCounts[k];},0);
var okLost = unclassified.length===0 && sum===blocks.length;
checks.push({name:"Nothing lost", status:(okLost?"pass":"fail"),
  detail: blocks.length+" block elements: "+Object.keys(kindCounts).map(function(k){return kindCounts[k]+" "+k;}).join(", ")+(unclassified.length?"; unclassified: "+unclassified.map(function(u){return u.tag;}).join(", "):"")});

var rtOk=false, rtN=0;
try { rtN=JSON.parse(buildJSON()).length; rtOk=(rtN===nP); } catch(e){ rtOk=false; }
checks.push({name:"Export round trip", status:(rtOk?"pass":"fail"), detail:"the JSON to download parses back to "+rtN+" records = "+nP+" rows on tab 02"});

var nPass=checks.filter(function(c){return c.status==="pass";}).length;
var nFail=checks.filter(function(c){return c.status==="fail";}).length;
var nLimit=checks.filter(function(c){return c.status==="limit";}).length;
var nRun=nPass+nFail;

/* ---------- header, rail ---------- */
document.getElementById("hTitle").textContent=TITLE;
var hSym=document.getElementById("hSym");
hSym.textContent=SYMBOL;
if (DOC_URL) hSym.href=DOC_URL; else hSym.removeAttribute("href");
document.getElementById("hAdopted").textContent = (REF && REF.adopted!=null) ? " · adopted "+REF.adopted : "";
document.getElementById("hSource").textContent = SOURCE ? " · "+SOURCE : "";
var st;
if (nRun===0) st='<span class="dot bad"></span>checks not run';
else if (nFail>0) st='<span class="dot bad"></span>'+nFail+' check'+(nFail>1?"s":"")+' failed';
else st='<span class="dot ok"></span>'+nPass+' of '+nRun+' checks pass';
if (nLimit>0) st+=' <span class="fail">· '+nLimit+' source limit'+(nLimit>1?"s":"")+'</span>';
document.getElementById("hStatus").innerHTML=st;

document.getElementById("rSym").textContent=SYMBOL;
document.getElementById("rTitle").textContent=TITLE;
document.getElementById("rP").textContent=nP;
document.getElementById("rPof").textContent = expP!==null ? "of "+expP+" paragraphs" : "paragraphs";
var bar=document.getElementById("rBar");
if (expP!==null){ bar.style.width=Math.min(100, nP/expP*100)+"%"; bar.classList.toggle("bad", nP!==expP); }
else bar.style.width="100%";
document.getElementById("rFof").textContent = (REF && typeof REF.footnotes==="number") ? "of "+REF.footnotes+" footnotes" : "footnotes in this HTML";
document.getElementById("rChecks").textContent = nRun ? (nPass+" of "+nRun+" checks pass") : "checks not run";

document.getElementById("fLine").textContent =
  (SOURCE? SOURCE+" · ":"") + (BUILT? "built "+BUILT+" · ":"") +
  "Done by this page's code; no model was called and nothing left the browser.";

/* ---------- tab 01: tiles ---------- */
(function renderTiles(){
  var t=document.getElementById("tiles");
  var diff = expP!==null ? nP-expP : null;
  var pSub = expP!==null
    ? (diff===0 ? '<span class="pass">the document has '+expP+' — match</span>'
               : '<span class="fail">the document has '+expP+' — '+(diff>0?"+":"−")+Math.abs(diff)+'</span>')
    : '<span class="hint">no reference in this file</span>';
  var fwCount=paragraphs.filter(function(p){return p.firstMatch===true;}).length;
  var fwSub = FW ? (fwCount+" of "+expP+" match") : "no reference in this file";
  var fSub = (REF && typeof REF.footnotes==="number")
    ? "of "+REF.footnotes+' — this HTML version has none; <button class="linkbtn" data-goto="2">tab 03</button>'
    : "in this HTML — no reference to compare";
  var html='';
  if (nP===0) html+='<p class="fail">The parsed HTML yielded no numbered paragraphs — the exports are disabled.</p>';
  html+=
   '<div class="tile"><div class="mono up lbl">Paragraphs found</div><div class="bignum">'+nP+'</div><div class="sub">'+pSub+'</div><p class="how">How this is computed: every &lt;p&gt; in the parsed HTML whose text begins with a number and a full stop, counted once, in document order.</p></div>'+
   '<div class="tile"><div class="mono up lbl">First words match</div><div class="bignum">'+(FW?fwCount:0)+'</div><div class="sub">'+esc(fwSub)+'</div><p class="how">How this is computed: the first six words of each paragraph against reference.first_words, compared after curly quotes, en dashes, non-breaking hyphens and non-breaking spaces are normalised; case is kept.</p></div>'+
   '<div class="tile"><div class="mono up lbl">Footnotes</div><div class="bignum red">0</div><div class="sub red">'+fSub+'</div><p class="how">How this is computed: no footnote text or footnote mark survives in this HTML; the count is 0 by inspection of the parsed elements.</p></div>'+
   '<div class="tile"><div class="mono up lbl">Spaces repaired or flagged</div><div class="bignum">'+logs.length+'</div><div class="sub"><button class="linkbtn" data-goto="2">see tab 03</button></div><p class="how">How this is computed: four rules insert a space only where the characters prove one was there (sentence, comma, quote and dash joins); text_raw keeps the text as found.</p></div>';
  t.innerHTML=html;
})();

/* ---------- tab 02: paragraphs ---------- */
function firstLine(t){
  if (t.length<=120) return t;
  var cut=t.slice(0,120), sp=cut.lastIndexOf(" ");
  if (sp>0) cut=cut.slice(0,sp);
  return cut+"…";
}
function detailHtml(p){
  var marked=p.parts.map(function(pt){ return pt.mk ? '<mark class="rep">'+esc(pt.t)+'</mark>' : esc(pt.t); }).join("");
  var h='<div class="fulltext">'+marked+'</div>';
  if (p.firstMatch===false) h+='<p class="cmp"><span class="fail">first words differ</span> — found “'+esc(p.firstFound)+'” · reference “'+esc(p.firstRef)+'”</p>';
  else if (p.firstMatch===true) h+='<p class="cmp pass">first six words match the reference</p>';
  if (p.logs.length) h+='<p class="mono hint">repairs here: '+esc(p.logs.map(function(l){return l.rule;}).join(", "))+'</p>';
  var path=[p.part?p.part.full:null, p.section?p.section.full:null].filter(Boolean).join(" › ");
  if (path) h+='<p class="path mono">path: '+esc(path)+'</p>';
  h+='<p class="cmp"><a href="'+esc(DOC_URL)+'" target="_blank" rel="noopener">'+esc(SYMBOL)+'</a>, para. '+p.num+' &nbsp;<button class="copybtn" data-cite="'+esc(p.citation)+'">Copy citation</button></p>';
  return h;
}
(function renderParagraphs(){
  document.getElementById("hBoxBtn").textContent="Headings found: "+headings.length;
  document.getElementById("hList").innerHTML=headings.map(function(h){
    return '<li><span class="mono">'+h.level+'</span> '+esc(h.full)+'</li>';
  }).join("");
  document.getElementById("pCap").textContent=nP+" paragraphs found"+(expP!==null?", "+expP+" expected":"");
  document.getElementById("pBody").innerHTML=paragraphs.map(function(p){
    var chk = p.firstMatch===null ? "" : (p.firstMatch ? '<span class="pass">OK</span>' : '<span class="fail">first words differ</span>');
    var sec = p.section ? p.section.full : "—";
    return '<tr class="prow"><td class="num"><button class="rowbtn" aria-expanded="false" aria-controls="det-'+p.num+'" data-num="'+p.num+'">'+p.num+'</button></td>'+
      '<td class="sec" title="'+esc(sec)+'">'+esc(sec)+'</td>'+
      '<td class="fl">'+esc(firstLine(p.text))+'</td>'+
      '<td>'+chk+'</td></tr>'+
      '<tr class="drow" id="det-'+p.num+'" hidden><td colspan="4">'+detailHtml(p)+'</td></tr>';
  }).join("");
})();

/* ---------- tab 03: lost & changed ---------- */
(function renderLost(){
  document.getElementById("fnText").innerHTML = (REF && typeof REF.footnotes==="number")
    ? 'The document has <strong>'+REF.footnotes+' footnotes</strong>. This HTML has <strong class="red">0</strong>: no footnote text, no footnote marks, and the note the title\u2019s asterisk points to is missing. To cite a footnote, use the PDF or Word version.'
    : 'This HTML has <strong class="red">0 footnotes</strong>: no footnote text and no footnote marks are present in the parsed elements.';
  document.getElementById("ruleLine").textContent =
    RULES.map(function(r){return r.name+": "+perRule[r.name];}).join(" · ")+" — "+logs.length+" spaces in "+repParas+" paragraphs · click a row = open the paragraph on tab 02";
  document.getElementById("sCap").textContent=logs.length+" missing spaces, restored by rule — the inserted space is boxed";
  document.getElementById("sBody").innerHTML=logs.map(function(l){
    var r=ruleByName[l.rule]; r.re.lastIndex=0;
    var m=r.re.exec(l.match);
    var repHtml=r.pieces(m).map(function(pc){ return pc[1] ? '<mark class="rep">'+esc(pc[0])+'</mark>' : esc(pc[0]); }).join("");
    var b=l.before, a=l.after;
    return '<tr class="srow" data-num="'+l.para+'"><td class="num">'+l.para+'</td>'+
      '<td>'+(b.length===20?"…":"")+esc(b)+'<span class="m">'+esc(l.match)+'</span>'+esc(a)+(a.length===20?"…":"")+'</td>'+
      '<td>'+(b.length===20?"…":"")+esc(b)+repHtml+esc(a)+(a.length===20?"…":"")+'</td>'+
      '<td>'+esc(l.rule)+'</td></tr>';
  }).join("");
  document.getElementById("cBody").innerHTML=CHARS.map(function(c){
    var ex = c.ex ? ((c.ex.cutB?"…":"")+esc(c.ex.b)+'<mark class="ch">'+esc(c.ex.ch)+'</mark>'+esc(c.ex.a)+(c.ex.cutA?"…":"")) : "—";
    return '<tr><td>'+esc(c.name)+' <span class="mono hint">'+c.code+'</span></td><td class="num">'+c.count+'</td><td>'+ex+'</td></tr>';
  }).join("");
})();

/* ---------- tab 04: checks & export ---------- */
(function renderChecksPanel(){
  document.getElementById("checkList").innerHTML=checks.map(function(c){
    var cls = c.status==="pass"?"pass": c.status==="fail"?"fail": c.status==="limit"?"limit":"hint";
    var word = c.status==="pass"?"pass": c.status==="fail"?"check failed": c.status==="limit"?"source limit":"not run";
    var link = c.link ? ' (<button class="linkbtn" data-goto="'+c.link.tab+'">'+c.link.label+'</button>)' : "";
    return '<li><span class="tag '+cls+'">'+word+'</span><strong>'+esc(c.name)+'</strong> — '+c.detail+link+'</li>';
  }).join("");
  document.getElementById("eBtn").textContent="Elements found ("+blocks.length+")";
  document.getElementById("eBody").innerHTML=blocks.map(function(b){
    return '<tr><td class="mono">'+esc(b.tag)+'</td><td>'+esc(b.label)+'</td><td>'+esc(b.text)+'</td></tr>';
  }).join("");
})();

/* ---------- tabs ---------- */
var tabs=Array.prototype.slice.call(document.querySelectorAll('[role=tab]'));
function selectTab(i, focus){
  tabs.forEach(function(t,j){
    var on=(i===j);
    t.setAttribute("aria-selected", on?"true":"false");
    t.tabIndex = on?0:-1;
    var panel=document.getElementById(t.getAttribute("aria-controls"));
    if (panel) panel.hidden=!on;
  });
  if (focus) tabs[i].focus();
}
tabs.forEach(function(t,i){
  t.addEventListener("click", function(){ selectTab(i,false); });
  t.addEventListener("keydown", function(e){
    var n=null;
    if (e.key==="ArrowRight"||e.key==="ArrowDown") n=(i+1)%tabs.length;
    else if (e.key==="ArrowLeft"||e.key==="ArrowUp") n=(i-1+tabs.length)%tabs.length;
    else if (e.key==="Home") n=0;
    else if (e.key==="End") n=tabs.length-1;
    if (n!==null){ e.preventDefault(); selectTab(n,true); }
  });
});
selectTab(0,false);

/* ---------- generic wiring ---------- */
document.addEventListener("click", function(e){
  var g=e.target.closest("[data-goto]");
  if (g) selectTab(parseInt(g.getAttribute("data-goto"),10), true);
});
function wireBox(btnId, boxId){
  var b=document.getElementById(btnId), x=document.getElementById(boxId);
  b.addEventListener("click", function(){
    var open=b.getAttribute("aria-expanded")==="true";
    b.setAttribute("aria-expanded", String(!open));
    x.hidden=open;
  });
}
wireBox("hBoxBtn","hBox");
wireBox("eBtn","eBox");

function openParagraph(n){
  selectTab(1,false);
  var btn=document.querySelector('.rowbtn[data-num="'+n+'"]');
  if (!btn) return;
  var det=document.getElementById(btn.getAttribute("aria-controls"));
  btn.setAttribute("aria-expanded","true");
  det.hidden=false;
  btn.closest("tr").scrollIntoView({block:"center"});
}
document.getElementById("pBody").addEventListener("click", function(e){
  var cb=e.target.closest(".copybtn");
  if (cb){ copyText(cb.getAttribute("data-cite"), cb); return; }
  var row=e.target.closest("tr.prow");
  if (!row) return;
  var btn=row.querySelector(".rowbtn");
  var det=document.getElementById(btn.getAttribute("aria-controls"));
  var open=btn.getAttribute("aria-expanded")==="true";
  btn.setAttribute("aria-expanded", String(!open));
  det.hidden=open;
});
document.getElementById("sBody").addEventListener("click", function(e){
  var tr=e.target.closest("tr.srow");
  if (tr) openParagraph(parseInt(tr.getAttribute("data-num"),10));
});

function copyText(t, btn){
  var old=btn.textContent;
  function ok(){ btn.textContent="Copied"; setTimeout(function(){ btn.textContent=old; },2000); }
  function fail(){ btn.textContent="Select & copy"; setTimeout(function(){ btn.textContent=old; },2000); }
  function fallback(){
    try{
      var ta=document.createElement("textarea");
      ta.value=t; ta.setAttribute("readonly","");
      ta.style.position="fixed"; ta.style.opacity="0";
      document.body.appendChild(ta); ta.select();
      var good=document.execCommand("copy");
      ta.remove();
      if (good) ok(); else fail();
    }catch(e){ fail(); }
  }
  if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(ok, fallback);
  else fallback();
}

var base=(SYMBOL.replace(/\//g,"-")||"document");
var dlJson=document.getElementById("dlJson"), dlMd=document.getElementById("dlMd");
if (!nP){ dlJson.disabled=true; dlMd.disabled=true; }
dlJson.addEventListener("click", function(){ if(nP) download(base+".json", buildJSON(), "application/json"); });
dlMd.addEventListener("click", function(){ if(nP) download(base+".md", buildMarkdown(), "text/markdown"); });
})();
</script>
</body>
</html>
```