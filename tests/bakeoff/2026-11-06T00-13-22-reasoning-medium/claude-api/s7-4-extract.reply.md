I built the two-tab app: Result and Paragraphs. It reads `WORKSHOP_DATA.pdf_text` and rebuilds the numbered paragraphs with their headings. It compares them with the document's own reference and flags the paragraphs that may contain footnote text. I have not run it against the real file, so check the counts on first load.

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
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.mono{font:11.5px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
a{color:#9b2335}
button{font:inherit;color:inherit;cursor:pointer}
:focus-visible{outline:3px solid #9b2335;outline-offset:2px}
header.top{padding:18px 28px 12px;border-bottom:1px solid #d9d2c3;display:flex;gap:24px;justify-content:space-between;flex-wrap:wrap}
header.top h1{font:normal 28px/1.2 Georgia,serif;margin:4px 0 6px}
.meta{font-size:14px;color:#4a463f}
.status{text-align:right;font-size:14px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;background:#2f6b3a}
.dot.bad{background:#9b2335}
.layout{display:grid;grid-template-columns:250px 1fr;gap:0}
.rail{border-right:1px solid #d9d2c3;padding:18px 20px;min-height:60vh}
.rail .card{border-top:1px solid #d9d2c3;border-bottom:1px solid #d9d2c3;padding:8px 0;margin:8px 0 18px;font-size:14px}
.rail .card b{font:12px ui-monospace,Menlo,Consolas,monospace;display:block}
.big{font:normal 48px/1.05 Georgia,serif}
.big.red{color:#9b2335}
.big.green{color:#2f6b3a}
.sub{font-size:14px;color:#4a463f}
.bar{height:5px;background:#d9d2c3;margin:6px 0 18px}
.bar i{display:block;height:5px;background:#2f6b3a}
.bar.bad i{background:#9b2335}
main{padding:0 28px 28px;min-width:0}
[role=tablist]{display:flex;gap:4px;border-bottom:1px solid #d9d2c3;margin-bottom:18px}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;padding:12px 14px 9px;font:12px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase}
[role=tab][aria-selected=true]{color:#9b2335;border-bottom-color:#9b2335;font-weight:bold}
h2.q{font:normal 22px/1.3 Georgia,serif;margin:0 0 14px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:1px solid #d9d2c3}
.tile{padding:14px 18px 14px 0;border-bottom:1px solid #d9d2c3}
.tile:nth-child(even){padding-left:18px;border-left:1px solid #d9d2c3}
.how{font:11.5px ui-monospace,Menlo,Consolas,monospace;color:#5a554b;margin-top:6px}
.red{color:#9b2335}.green{color:#2f6b3a}
.list{margin:12px 0;font-size:14px;font-family:ui-monospace,Menlo,Consolas,monospace}
h3.sec{font:normal 20px Georgia,serif;margin:26px 0 8px}
.btn{border:1px solid #1d1b18;background:#fff8;padding:8px 14px;margin-right:8px;font-size:15px}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn:hover:not(:disabled){background:#1d1b18;color:#f4f0e8}
.disc{display:block;width:100%;text-align:left;background:none;border:0;border-top:1px solid #d9d2c3;padding:12px 0;font:12px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase}
.disc::before{content:"+ ";color:#9b2335}
.disc[aria-expanded=true]::before{content:"– "}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font:normal 18px Georgia,serif;padding:6px 0}
caption .mono{display:block;color:#5a554b;font-size:11px}
th{font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:2px solid #1d1b18;padding:6px 8px}
td{border-bottom:1px solid #d9d2c3;padding:7px 8px;vertical-align:top}
th.num,td.num{text-align:right}
tr.row{cursor:pointer}
tr.row:hover{background:#ebe5d8}
.rowbtn{background:none;border:0;color:#9b2335;font:bold 15px ui-monospace,Menlo,Consolas,monospace;padding:2px 4px}
td.detail{background:#fbf8f2;padding:14px 18px}
.ptext{font:17px/1.6 Georgia,serif;max-width:75ch}
.sus{border:1px solid #9b2335;padding:0 2px;margin:0 1px}
pre.lines{white-space:pre-wrap;font:13px/1.5 ui-monospace,Menlo,Consolas,monospace;background:#f4f0e8;border:1px solid #d9d2c3;padding:10px;max-width:90ch}
.pg{color:#9b2335}
.chk{border-top:1px solid #d9d2c3;padding:9px 0;font-size:14px}
.chk b{font-family:Georgia,serif;font-size:16px}
.pass{color:#2f6b3a;font-weight:bold}.fail{color:#9b2335;font-weight:bold}
.note{font-size:14px;color:#4a463f;margin:0 0 10px}
footer.bot{border-top:1px solid #d9d2c3;padding:14px 28px;color:#4a463f}
.lk{background:none;border:0;color:#9b2335;text-decoration:underline;padding:0;font-size:inherit}
@media(max-width:820px){.layout{grid-template-columns:1fr}.rail{border-right:0;border-bottom:1px solid #d9d2c3;min-height:0}.tiles{grid-template-columns:1fr}.tile:nth-child(even){padding-left:0;border-left:0}}
</style>
</head>
<body>
<header class="top">
  <div>
    <div class="mono">UN document · PDF text</div>
    <h1 id="title">…</h1>
    <div class="meta" id="meta"></div>
  </div>
  <div class="status" id="status"></div>
</header>
<div class="layout">
  <aside class="rail" id="rail" aria-label="Document summary"></aside>
  <main>
    <div role="tablist" aria-label="Views">
      <button role="tab" id="tab1" aria-selected="true" aria-controls="p1" tabindex="0">01 Result</button>
      <button role="tab" id="tab2" aria-selected="false" aria-controls="p2" tabindex="-1">02 Paragraphs</button>
    </div>
    <section role="tabpanel" id="p1" aria-labelledby="tab1"></section>
    <section role="tabpanel" id="p2" aria-labelledby="tab2" hidden></section>
  </main>
</div>
<footer class="bot mono" id="foot"></footer>

<script>
(function(){
"use strict";
function h(tag,attrs){var e=document.createElement(tag);attrs=attrs||{};for(var k in attrs){var v=attrs[k];if(v==null||v===false)continue;if(k==='class')e.className=v;else if(k.indexOf('on')===0)e.addEventListener(k.slice(2),v);else e.setAttribute(k,v===true?'':v);}
  for(var i=2;i<arguments.length;i++){var c=arguments[i];if(Array.isArray(c)){c.forEach(function(x){if(x!=null&&x!==false)e.append(x.nodeType?x:document.createTextNode(String(x)))});}else if(c!=null&&c!==false)e.append(c.nodeType?c:document.createTextNode(String(c)));}
  return e;}
function plural(n,a,b){return n+' '+(n===1?a:b);}

/* ---------- data ---------- */
var D=window.WORKSHOP_DATA&&window.WORKSHOP_DATA.pdf_text;
if(Array.isArray(D))D={records:D};
D=D||{};
var SYMBOL=D.symbol||'';
var REF=D.reference||null;
var recs=(D.records||[]).slice().sort(function(a,b){return (a.page||0)-(b.page||0)});
var hasRefCount=REF&&typeof REF.paragraphs==='number';
var hasRefFW=REF&&REF.first_words&&typeof REF.first_words==='object';

/* ---------- pipeline ---------- */
var LABEL=/^([IVX]+|[A-Z])\.$/, PS1=/^(\d{1,3})\.$/, PS2=/^(\d{1,3})\. (.+)$/;
var all=[]; // every non-empty line, with kind
var body=[];
var warnings=[], pagesHeader=0, pagesPageNo=0, displaced=[], footerLines=0;
recs.forEach(function(r){
  var lines=String(r.text||'').replace(/\r/g,'').split('\n').map(function(s){return s.trim()});
  var firstIdx=-1;
  for(var i=0;i<lines.length;i++){if(lines[i]!==''){firstIdx=i;break;}}
  var objs=lines.map(function(t){var o={page:r.page,t:t,empty:t==='',kind:null};return o;});
  if(firstIdx>=0){
    if(objs[firstIdx].t===SYMBOL){objs[firstIdx].kind='header';pagesHeader++;}
    else warnings.push('page '+r.page+': first line is not the symbol');
  }
  var end=objs.length-1, hasNo=false;
  while(end>=0){
    var o=objs[end],t=o.t;
    if(o.kind==='header')break;
    if(t===''){end--;continue;}
    if(/^GE\./.test(t)||/^\d{6}(\s+\d{6})*$/.test(t)){o.kind='footer';end--;continue;}
    if(/^\d{1,3}$/.test(t)){o.kind='footer';if(Number(t)===r.page)hasNo=true;else displaced.push({page:r.page,n:t});end--;continue;}
    break;
  }
  if(hasNo)pagesPageNo++;
  objs.forEach(function(o){if(!o.empty){all.push(o);if(o.kind==='footer')footerLines++;}if(o.kind!=='header'&&o.kind!=='footer')body.push(o);});
});
body.forEach(function(o,i){o.i=i;});

function headLike(t){return t.length<=90&&/^[A-Z]/.test(t)&&!/[.;:,\d]$/.test(t);}
function isStart(t){return PS1.test(t)||PS2.test(t);}
function nextIsPara(i){var n=body[i+1];return n&&!n.empty&&isStart(n.t)&&n.page===body[i].page;}
var paras=[],heads=[],seq=[];
var cur=null,curSection=null,curPart=null,lastLetter=null;
function addHead(label,text,page){var hd={label:label,text:text,page:page,roman:!!label&&/^[IVX]+$/.test(label)&&label!==lastLetterFlag};return hd;}
var lastLetterFlag=null;
function isRoman(label){if(!/^[IVX]+$/.test(label))return false;if(label.length===1&&lastLetter&&label.charCodeAt(0)===lastLetter.charCodeAt(0)+1)return false;return true;}
for(var i=0;i<body.length;i++){
  var L=body[i];if(L.empty)continue;
  var m;
  if(LABEL.test(L.t)){
    var label=L.t.slice(0,-1);L.kind='heading';
    var j=i+1,parts=[];
    while(j<body.length){
      var X=body[j];
      if(X.empty){j++;continue;}
      if(LABEL.test(X.t)||isStart(X.t))break;
      X.kind='heading';
      if(/^[a-z(]/.test(X.t)&&parts.length)parts[parts.length-1]+=' '+X.t;else parts.push(X.t);
      j++;
    }
    var roman=isRoman(label);
    var hd={label:label,text:parts[0]||'',page:L.page,roman:roman,kind:'labelled'};
    if(roman){curPart=hd;lastLetter=null;}else lastLetter=label;
    heads.push(hd);seq.push({type:'heading',h:hd});curSection=hd;
    for(var q=1;q<parts.length;q++){var h2={label:'',text:parts[q],page:L.page,roman:false,kind:'unlabelled'};heads.push(h2);seq.push({type:'heading',h:h2});curSection=h2;}
    i=j-1;continue;
  }
  if((m=PS1.exec(L.t))||(m=PS2.exec(L.t))){
    L.kind='paragraph';
    cur={n:Number(m[1]),page_start:L.page,lines:[],section:curSection,part:curPart,startPage:L.page};
    if(m[2]!==undefined)cur.lines.push({t:m[2],page:L.page,i:L.i,ref:L});
    paras.push(cur);seq.push({type:'para',p:cur});continue;
  }
  if(!cur){L.kind='cover';continue;}
  if(nextIsPara(i)&&headLike(L.t)){
    var txt=L.t;L.kind='heading';
    var prev=cur.lines[cur.lines.length-1];
    if(prev&&cur.lines.length>1&&prev.i===i-1&&prev.page===L.page&&headLike(prev.t)){cur.lines.pop();prev.ref.kind='heading';txt=prev.t+' '+L.t;}
    var h3={label:'',text:txt,page:L.page,roman:false,kind:'unlabelled'};
    heads.push(h3);seq.push({type:'heading',h:h3});curSection=h3;continue;
  }
  L.kind='paragraph';
  cur.lines.push({t:L.t,page:L.page,i:L.i,ref:L});
}
function hText(hd){return hd?(hd.label?hd.label+'. ':'')+hd.text:'';}

function startType(t){
  if(/^\d{1,3}$/.test(t))return 'bare number';
  if(/^\* /.test(t))return 'starts with an asterisk';
  if(/^\d{1,3} [A-Z“"‘']/.test(t))return 'starts with a number and a space';
  return null;
}
function cleanWords(text){
  var tk=text.split(/\s+/).slice(0,24),out=[];
  for(var a=0;a<tk.length;a++){
    var t=tk[a];if(t==='')continue;
    if(/^\d{1,3}$/.test(t)&&out.length){var pv=out[out.length-1];if(/[.,”"’']$/.test(pv)&&!/^(No|Nos|art|arts|para|paras|p|pp|vol|Rev|Add|Corr)\.$/i.test(pv))continue;}
    t=t.replace(/(?<=[A-Za-z.,;:”"’')\]])\d{1,3}$/,'');
    if(t==='')continue;
    out.push(t);if(out.length===6)break;
  }
  return out.join(' ');
}
function norm(s){return String(s).replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();}
var hyphenEnds=0;
paras.forEach(function(p){
  var susPage=null,reasons=[],cnt=0,pages={};
  p.lines.forEach(function(e){
    if(susPage!==null&&e.page!==susPage)susPage=null;
    if(susPage===null){var st=startType(e.t);if(st){susPage=e.page;if(reasons.indexOf(st)<0)reasons.push(st);}}
    e.sus=susPage!==null;
    if(e.sus){cnt++;pages[e.page]=1;}
    if(/-$/.test(e.t))hyphenEnds++;
  });
  p.textLines=p.lines.map(function(e){return e.t;});
  p.text=p.textLines.join(' ').replace(/\s+/g,' ').trim();
  p.words=p.text?p.text.split(/\s+/).length:0;
  if(p.words>300)reasons.push('paragraph over 300 words');
  p.susCount=cnt;p.susPages=Object.keys(pages);
  p.reasons=reasons;p.flagged=cnt>0||p.words>300;
  p.page_end=p.lines.length?p.lines[p.lines.length-1].page:p.startPage;
  if(p.page_end<p.page_start)p.page_end=p.page_start;
  p.found=cleanWords(p.text);
  p.refFW=hasRefFW&&REF.first_words[String(p.n)]!=null?String(REF.first_words[String(p.n)]):null;
  p.fwMatch=p.refFW==null?null:norm(p.found)===norm(p.refFW);
  p.citation=SYMBOL+', para. '+p.n;
  p.sectionText=hText(p.section);p.partText=hText(p.part);
  p.limitations=p.flagged?'footnotes not separated; '+(cnt>0?plural(cnt,'suspect line','suspect lines')+' may sit inside this paragraph':'footnote text may sit inside this paragraph (over 300 words)'):'footnotes not separated';
});
var flagged=paras.filter(function(p){return p.flagged});
var flaggedPages={};flagged.forEach(function(p){p.susPages.forEach(function(x){flaggedPages[x]=1});if(!p.susPages.length)flaggedPages['p'+p.page_start]=1;});
var nFlaggedPages=Object.keys(flaggedPages).length;
var totalSusLines=0,susPagesAll={},susParas=0;
paras.forEach(function(p){totalSusLines+=p.susCount;p.susPages.forEach(function(x){susPagesAll[x]=1});if(p.susCount)susParas++;});

/* ---------- export ---------- */
function pageRange(p){return p.page_start===p.page_end?String(p.page_start):p.page_start+'–'+p.page_end;}
function buildJSON(){
  return JSON.stringify(paras.map(function(p){return {symbol:SYMBOL,paragraph:p.n,section:p.sectionText,part:p.partText,page_start:p.page_start,page_end:p.page_end,text:p.text,text_lines:p.textLines.join(' | '),flagged:p.flagged,first_words_match:p.fwMatch,citation:p.citation,doc_url:D.doc_url||'',limitations:p.limitations};}),null,2);
}
function buildMD(){
  var q=function(s){return JSON.stringify(String(s==null?'':s));};
  var o=['---','title: '+q(D.title),'symbol: '+q(SYMBOL),'adopted: '+q(REF&&REF.adopted||''),'source_url: '+q(D.doc_url||''),'extracted: '+q(new Date().toISOString().slice(0,10)),'paragraphs_found: '+paras.length,'paragraphs_expected: '+(hasRefCount?REF.paragraphs:q('unknown')),'paragraphs_flagged: '+flagged.length,'footnotes: '+q('not separated; the document has '+(REF&&REF.footnotes!=null?REF.footnotes:'an unknown number'))+'','---',''];
  seq.forEach(function(s){
    if(s.type==='heading'){var hd=s.h;o.push((hd.roman?'## ':'### ')+hText(hd),'');}
    else{var p=s.p;o.push('**'+p.n+'.** '+p.text+(p.flagged?' (flagged: may contain footnote text)':''),'');}
  });
  return o.join('\n');
}
var jsonStr=buildJSON(),mdStr=buildMD();
function download(name,mime,str){var b=new Blob([str],{type:mime+';charset=utf-8'});var u=URL.createObjectURL(b);var a=h('a',{href:u,download:name});document.body.append(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u)},2000);}
var fileBase=(SYMBOL||'document').replace(/\//g,'-');

/* ---------- checks ---------- */
var fwMismatch=[];
paras.forEach(function(p){if(p.fwMatch!==true)fwMismatch.push(p);});
var refMissing=[];
if(hasRefFW){var have={};paras.forEach(function(p){have[p.n]=1});Object.keys(REF.first_words).forEach(function(k){if(!have[k])refMissing.push(k);});}
var fwMatchCount=paras.filter(function(p){return p.fwMatch===true}).length;
var checks=[],notes=[];
function addCheck(c){checks.push(c);}
addCheck(hasRefCount?{title:'Paragraph count',story:'Given this PDF text, having run the paragraph finder, we expect as many paragraphs as the reference lists.',detail:'found '+paras.length+' / reference '+REF.paragraphs,status:paras.length===REF.paragraphs?'pass':'fail'}:{title:'Paragraph count',story:'Needs reference.paragraphs.',detail:'no reference in this file',status:'notrun'});
(function(){
  var exp=1,issues=[];
  paras.forEach(function(p){
    if(p.n===exp)exp++;
    else if(p.n<exp)issues.push('para '+p.n+' repeated or out of order (page '+p.page_start+')');
    else{issues.push('missing '+(p.n-1>exp?exp+'–'+(p.n-1):exp)+' before para '+p.n+' (page '+p.page_start+')');exp=p.n+1;}
  });
  addCheck({title:'Numbering',story:'We expect paragraph numbers 1 to n, once each, in order.',detail:paras.length?(issues.length?issues.join('; '):'1 to '+paras.length+', no gaps, no duplicates'):'no paragraphs found',status:paras.length&&!issues.length?'pass':'fail',jump:issues.length&&paras.length?{label:'open first paragraph',fn:function(){openPara(paras[0].n)}}:null});
})();
addCheck(hasRefFW?{title:'First words',story:'We expect the first six words of every paragraph to equal the reference (quotes and dashes normalised).',detail:fwMatchCount+' match, '+(fwMismatch.length+refMissing.length)+' differ',status:fwMismatch.length+refMissing.length===0?'pass':'fail',jump:fwMismatch.length?{label:'open para '+fwMismatch[0].n,fn:function(){openPara(fwMismatch[0].n)}}:null}:{title:'First words',story:'Needs reference.first_words.',detail:'no reference in this file',status:'notrun'});
var hfOK=recs.length>0&&pagesHeader===recs.length&&pagesPageNo>=recs.length-1;
addCheck({title:'Headers and footers',story:'We expect the symbol as first line of every page and a page number in the footer of every page but the first.',detail:pagesHeader+' of '+recs.length+' pages start with the symbol; '+pagesPageNo+' pages have a page number; '+displaced.length+' bare numbers removed from the footer'+(displaced.length?' (page '+displaced.map(function(d){return d.page+': '+d.n}).join(', ')+')':'')+'; '+warnings.length+' warnings',status:hfOK?'pass':'fail'});
var kinds={cover:0,header:0,heading:0,paragraph:0,footer:0},unclass=[];
all.forEach(function(o){if(o.kind&&kinds[o.kind]!==undefined)kinds[o.kind]++;else unclass.push(o);});
var sumKinds=0;for(var k in kinds)sumKinds+=kinds[k];
addCheck({title:'Nothing lost',story:'We expect every non-empty line to be classified exactly once, and the classes to sum to the total.',detail:'cover '+kinds.cover+' + header '+kinds.header+' + heading '+kinds.heading+' + paragraph '+kinds.paragraph+' + footer '+kinds.footer+' = '+sumKinds+' of '+all.length+' lines; '+hyphenEnds+' lines end with a hyphen (not joined)'+(unclass.length?'; unclassified: '+unclass.map(function(o){return 'p.'+o.page+' "'+o.t.slice(0,40)+'"'}).join(', '):''),status:sumKinds===all.length&&!unclass.length?'pass':'fail'});
var rt=false;try{rt=JSON.parse(jsonStr).length===paras.length;}catch(e){}
addCheck({title:'Export round trip',story:'We expect the JSON to download to parse back with as many records as the table.',detail:'table '+paras.length+' rows; JSON parsed back '+(rt?paras.length:'with a different count'),status:rt?'pass':'fail'});
notes.push({title:'Paragraphs flagged',story:'A flag is not a failure: the count can be right while footnote text sits inside a paragraph.',detail:plural(flagged.length,'paragraph','paragraphs')+' flagged on '+plural(nFlaggedPages,'page','pages')+', to check against the PDF'});
notes.push({title:'Suspect lines',story:'Lines that look like footnotes stay in the text; none is removed.',detail:plural(totalSusLines,'suspect line','suspect lines')+' on '+Object.keys(susPagesAll).length+' pages, in '+plural(susParas,'paragraph','paragraphs')});
var unl=heads.filter(function(x){return x.kind==='unlabelled'});
notes.push({title:'Headings',story:'Unlabelled headings are listed so you can spot a paragraph\'s last line mistaken for one.',detail:(heads.length-unl.length)+' labelled, '+unl.length+' unlabelled'+(unl.length?': '+unl.map(function(x){return '“'+x.text+'” (p. '+x.page+')'}).join('; '):'')});
var nPass=checks.filter(function(c){return c.status==='pass'}).length,nFail=checks.filter(function(c){return c.status==='fail'}).length,nChecks=checks.length;

/* ---------- header, rail, footer ---------- */
document.getElementById('title').textContent=D.title||'(no title in this file)';
var meta=document.getElementById('meta');
if(SYMBOL){meta.append(D.doc_url?h('a',{href:D.doc_url,target:'_blank',rel:'noopener'},SYMBOL):SYMBOL);}
meta.append(' · adopted '+(REF&&REF.adopted?REF.adopted:'unknown')+' · '+plural(recs.length,'page','pages')+(D.source?' · '+D.source:''));
document.getElementById('status').append(
  h('div',null,h('span',{class:'dot'+(nFail?' bad':'')}),nFail?plural(nFail,'check','checks')+' failed':nPass+' of '+nChecks+' checks pass'),
  h('div',{class:flagged.length?'red':''},plural(flagged.length,'paragraph','paragraphs')+' flagged'));
var shortOK=hasRefCount&&paras.length===REF.paragraphs;
var rail=document.getElementById('rail');
rail.append(
  h('div',{class:'mono'},'Document'),
  h('div',{class:'card'},h('b',null,SYMBOL||'—'),D.title||''),
  h('div',{class:'big serif'+(hasRefCount&&!shortOK?' red':'')},String(paras.length)),
  h('div',{class:'sub'},hasRefCount?'paragraphs of '+REF.paragraphs:'paragraphs found (no reference)'),
  h('div',{class:'bar'+(hasRefCount&&!shortOK?' bad':'')},h('i',{style:'width:'+(hasRefCount&&REF.paragraphs?Math.min(100,paras.length/REF.paragraphs*100):100)+'%'})),
  h('div',{class:'big serif'+(flagged.length?' red':'')},String(flagged.length)),
  h('div',{class:'sub'},'paragraphs flagged of '+paras.length+' found'+(flagged.length?': footnote text may sit inside: check them against the PDF':'')),
  h('div',{class:'bar'}),
  h('div',{class:'big serif '+(nFail?'red':'green')},nPass+' of '+nChecks),
  h('div',{class:'sub'},'checks pass'));
document.getElementById('foot').textContent=(D.source||'')+(D.built?' · built '+D.built:'')+' · Done by this page\'s code; no model was called and nothing left the browser.';

/* ---------- widgets ---------- */
function disc(label,content,onOpen){
  var b=h('button',{class:'disc','aria-expanded':'false'},label);
  content.hidden=true;
  b.addEventListener('click',function(){var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!o));content.hidden=o;if(!o&&onOpen)onOpen();});
  return [b,content];
}
function tile(label,big,cls,sub,how){return h('div',{class:'tile'},h('div',{class:'mono'},label),h('div',{class:'big serif '+(cls||'')},big),h('div',{class:'sub'},sub),h('div',{class:'how'},'How this is computed: '+how));}

/* ---------- tab 1 ---------- */
var p1=document.getElementById('p1'),p2=document.getElementById('p2');
var flaggedDisc;
(function(){
  p1.append(h('h2',{class:'q'},'Did the app find everything the document has?'));
  if(!paras.length){p1.append(h('p',{class:'fail'},'No paragraphs were found in this file. The exports are disabled.'));}
  var diff=hasRefCount?paras.length-REF.paragraphs:0;
  var t=h('div',{class:'tiles'},
    tile('Paragraphs found',String(paras.length),hasRefCount?(shortOK?'green':'red'):'',hasRefCount?'the document has '+REF.paragraphs+(shortOK?' · equal':' · difference '+(diff>0?'+':'')+diff):'no reference in this file','lines matching “n.” or “n. text”, counted in a loop over the pages in order.'),
    tile('First words match',hasRefFW?String(fwMatchCount):'—',hasRefFW?(fwMatchCount===(REF.paragraphs||paras.length)?'green':'red'):'','of '+(hasRefCount?REF.paragraphs:'?')+(hasRefFW?'':' · no reference in this file'),'first six words of each paragraph, footnote marks removed, compared with reference.first_words after straightening quotes and dashes.'),
    tile('Paragraphs flagged',String(flagged.length),flagged.length?'red':'','of '+paras.length+' found, on '+plural(nFlaggedPages,'page','pages')+(flagged.length?': footnote text may sit inside these paragraphs: check them against the PDF':''),'a paragraph is flagged when a line looks like a footnote (a bare number, “7 E/2003/22…”, “* …”), or it has over 300 words.'),
    tile('Footnotes','not separated','', 'the document has '+(REF&&REF.footnotes!=null?REF.footnotes:'an unknown number')+'; this version leaves them in place and flags them','read from reference.footnotes; nothing is counted from the text.'));
  p1.append(t);
  var total=fwMismatch.length+refMissing.length;
  if(hasRefFW&&total){
    var lst=h('div',{class:'list red'});
    var items=[];
    fwMismatch.forEach(function(p){items.push('para. '+p.n+': found “'+p.found+'” / reference '+(p.refFW==null?'none':'“'+p.refFW+'”'));});
    refMissing.forEach(function(k){items.push('para. '+k+': not found / reference “'+REF.first_words[k]+'”');});
    items.slice(0,10).forEach(function(s){lst.append(h('div',null,s));});
    if(items.length>10)lst.append(h('div',null,'and '+(items.length-10)+' more'));
    p1.append(lst);
  }
  p1.append(h('h3',{class:'sec'},'Take the paragraphs away'),
    h('div',null,
      h('button',{class:'btn',disabled:!paras.length,onclick:function(){download(fileBase+'.json','application/json',jsonStr)}},'Download JSON'),
      h('button',{class:'btn',disabled:!paras.length,onclick:function(){download(fileBase+'.md','text/markdown',mdStr)}},'Download Markdown')),
    h('div',{class:'how'},'Each record carries symbol, paragraph, section, part, pages, text, flags, citation, doc_url and its known limitation.'));
  /* checks */
  var cbox=h('div');
  function chkRow(c,counted){
    var st=c.status==='pass'?h('span',{class:'pass'},'pass'):c.status==='fail'?h('span',{class:'fail'},'check failed'):c.status==='notrun'?h('span',null,'not run'):h('span',{class:'mono'},'for your attention');
    return h('div',{class:'chk'},h('b',null,c.title+' '),st,h('div',{class:'sub'},c.story),h('div',null,c.detail),c.jump?h('button',{class:'lk',onclick:c.jump.fn},c.jump.label):null);
  }
  checks.forEach(function(c){cbox.append(chkRow(c));});
  cbox.append(h('div',{class:'mono',style:'margin-top:12px'},'Notes (not counted as checks)'));
  notes.forEach(function(c){c.status='info';cbox.append(chkRow(c));});
  disc('Every check ('+nChecks+')',cbox).forEach(function(x){p1.append(x)});
  /* flagged */
  var fbox=h('div');
  fbox.append(h('p',{class:'note'},'This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.'));
  var tb=h('tbody');
  flagged.forEach(function(p){
    var firstSus=p.lines.filter(function(e){return e.sus})[0];
    var bt=h('button',{class:'rowbtn',onclick:function(){openPara(p.n)}},String(p.n));
    tb.append(h('tr',{class:'row',onclick:function(e){if(e.target!==bt)openPara(p.n)}},h('td',{class:'num'},bt),h('td',{class:'num'},pageRange(p)),h('td',null,p.susCount?p.susCount+(firstSus?' · “'+firstSus.t.slice(0,40)+(firstSus.t.length>40?'…':'')+'”':''):'0'),h('td',null,p.reasons.join('; '))));
  });
  fbox.append(h('table',null,h('caption',null,h('span',{class:'mono'},'TAB.01'),plural(flagged.length,'paragraph','paragraphs')+' flagged, '+paras.length+' found'),
    h('thead',null,h('tr',null,h('th',{scope:'col',class:'num'},'Paragraph'),h('th',{scope:'col',class:'num'},'Page'),h('th',{scope:'col'},'Suspect lines'),h('th',{scope:'col'},'Why'))),tb));
  disc('Flagged paragraphs ('+flagged.length+')',fbox).forEach(function(x,i){p1.append(x);if(i===0)flaggedDisc=x;});
})();

/* ---------- tab 2 ---------- */
var rowState={};
function copyText(t){
  if(navigator.clipboard&&navigator.clipboard.writeText){return navigator.clipboard.writeText(t).then(function(){return true},function(){return fallback(t)});}
  return Promise.resolve(fallback(t));
  function fallback(s){var ta=h('textarea',{style:'position:fixed;opacity:0'});ta.value=s;document.body.append(ta);ta.select();var ok=false;try{ok=document.execCommand('copy')}catch(e){}ta.remove();return ok;}
}
function buildDetail(p){
  var box=h('div');
  box.append(h('div',{class:'mono',style:'margin-bottom:6px'},'Path: '+(p.partText&&p.sectionText&&p.partText!==p.sectionText?p.partText+' › '+p.sectionText:(p.sectionText||'no heading'))+' · page '+pageRange(p)));
  var pt=h('div',{class:'ptext'});
  p.lines.forEach(function(e,i){
    var sp=e.sus?h('span',{class:'sus'},e.t):document.createTextNode(e.t);
    pt.append(sp);if(i<p.lines.length-1)pt.append(' ');
  });
  box.append(pt);
  box.append(h('p',{class:'how'},'First six words — reference: '+(p.refFW==null?'none':'“'+p.refFW+'”')+' · found: “'+p.found+'” · '+(p.fwMatch===true?'match':p.fwMatch===false?'differ':'not compared')));
  if(p.flagged)box.append(h('p',{class:'red'},'May contain footnote text ('+p.reasons.join('; ')+'). Suspect lines are boxed in red; they stay in the text.'));
  var pre=h('pre',{class:'lines'});pre.hidden=true;
  var lastPage=null;
  var firstLine=h('span',null,p.n+'.\n');
  pre.append(h('span',{class:'pg'},'[page '+p.startPage+' begins]\n'),firstLine);lastPage=p.startPage;
  p.lines.forEach(function(e){
    if(e.page!==lastPage){pre.append(h('span',{class:'pg'},'[page '+e.page+' begins]\n'));lastPage=e.page;}
    pre.append(e.sus?h('span',{class:'sus'},e.t):document.createTextNode(e.t),'\n');
  });
  var tg=h('button',{class:'btn','aria-expanded':'false'},'Show the PDF\'s lines');
  tg.addEventListener('click',function(){var o=tg.getAttribute('aria-expanded')==='true';tg.setAttribute('aria-expanded',String(!o));pre.hidden=o;tg.textContent=o?'Show the PDF\'s lines':'Hide the PDF\'s lines';});
  var cp=h('button',{class:'btn'},'Copy citation');
  cp.addEventListener('click',function(){copyText(p.citation).then(function(ok){cp.textContent=ok?'Copied':'Copy failed';setTimeout(function(){cp.textContent='Copy citation'},2000)});});
  box.append(h('div',null,tg,cp,h('span',{class:'mono'},p.citation)),pre);
  return box;
}
function toggleRow(p,force){
  var st=rowState[p.n];var open=force!==undefined?force:!(st.btn.getAttribute('aria-expanded')==='true');
  st.btn.setAttribute('aria-expanded',String(open));
  if(open&&!st.built){st.cell.append(buildDetail(p));st.built=true;}
  st.detail.hidden=!open;
}
function checkCell(p){
  if(p.fwMatch===false)return h('span',{class:'red'},'first words differ'+(p.flagged?'; ':''),p.flagged?'may contain footnote text':'');
  if(p.flagged)return h('span',{class:'red'},'may contain footnote text');
  if(p.fwMatch===null)return 'not compared';
  return 'OK';
}
function firstLineOf(p){var t=p.text;if(t.length<=120)return t;var c=t.slice(0,120),k=c.lastIndexOf(' ');return (k>40?c.slice(0,k):c)+'…';}
(function(){
  p2.append(h('h2',{class:'q'},'What does each paragraph say, and how do I cite it?'));
  var hb=h('div');
  var hl=h('div',{class:'list'});
  heads.forEach(function(x){hl.append(h('div',null,(x.kind==='unlabelled'?'unlabelled':'labelled')+' · p. '+x.page+' · '+hText(x)));});
  if(!heads.length)hl.append('No headings found.');
  hb.append(hl);
  disc('Headings found: '+heads.length,hb).forEach(function(x){p2.append(x)});
  var tb=h('tbody');
  paras.forEach(function(p){
    var btn=h('button',{class:'rowbtn','aria-expanded':'false','aria-controls':'d'+p.n},String(p.n));
    var tr=h('tr',{class:'row',id:'r'+p.n},h('td',{class:'num'},btn),h('td',null,p.sectionText||'—'),h('td',{class:'num'},pageRange(p)),h('td',null,firstLineOf(p)),h('td',null,checkCell(p)));
    var cell=h('td',{class:'detail',colspan:'5'});
    var dt=h('tr',{id:'d'+p.n},cell);dt.hidden=true;
    rowState[p.n]={btn:btn,detail:dt,cell:cell,tr:tr,built:false};
    btn.addEventListener('click',function(e){e.stopPropagation();toggleRow(p);});
    tr.addEventListener('click',function(e){if(e.target.closest('button'))return;toggleRow(p);});
    tb.append(tr,dt);
  });
  p2.append(h('table',null,h('caption',null,h('span',{class:'mono'},'TAB.02'),plural(paras.length,'paragraph','paragraphs')+' found'+(hasRefCount?', '+REF.paragraphs+' expected':'')),
    h('thead',null,h('tr',null,h('th',{scope:'col',class:'num'},'No.'),h('th',{scope:'col'},'Section'),h('th',{scope:'col',class:'num'},'Page'),h('th',{scope:'col'},'First line'),h('th',{scope:'col'},'Check'))),tb));
  p2.append(h('p',{class:'how'},'Click a row to open the full text. Section is the nearest heading above the paragraph.'));
})();

/* ---------- tabs ---------- */
var tabs=[document.getElementById('tab1'),document.getElementById('tab2')],panels=[p1,p2];
function selectTab(i,focus){tabs.forEach(function(t,k){t.setAttribute('aria-selected',String(k===i));t.tabIndex=k===i?0:-1;panels[k].hidden=k!==i;});if(focus)tabs[i].focus();}
tabs.forEach(function(t,i){
  t.addEventListener('click',function(){selectTab(i)});
  t.addEventListener('keydown',function(e){
    var n=null;if(e.key==='ArrowRight')n=(i+1)%tabs.length;else if(e.key==='ArrowLeft')n=(i+tabs.length-1)%tabs.length;else if(e.key==='Home')n=0;else if(e.key==='End')n=tabs.length-1;
    if(n!==null){e.preventDefault();selectTab(n,true);}
  });
});
function openPara(n){
  var p=paras.filter(function(x){return x.n===n})[0];if(!p)return;
  selectTab(1);toggleRow(p,true);
  var st=rowState[n];st.tr.scrollIntoView({block:'start'});st.btn.focus();
}
})();
</script>
</body>
</html>
```