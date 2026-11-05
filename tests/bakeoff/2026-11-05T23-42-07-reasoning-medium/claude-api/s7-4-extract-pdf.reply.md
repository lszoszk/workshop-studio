I built a two-tab app on the General Comment text. It rebuilds the numbered paragraphs, checks them against the document's own reference, flags pages where footnote text may sit inside a paragraph, and exports JSON and Markdown. Everything is computed by the page's own code; no model is called.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraphs out of a PDF</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
[hidden]{display:none!important}
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#2b6a35;--mute:#5d574d}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.serif{font-family:Georgia,"Times New Roman",serif}
.red{color:var(--red)}.green{color:var(--green)}
button{font:inherit;color:inherit;cursor:pointer}
a{color:var(--red)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header{padding:18px 28px 12px;border-bottom:1px solid var(--rule)}
.top{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;align-items:flex-start}
h1{font:normal 28px/1.2 Georgia,"Times New Roman",serif;margin:4px 0 6px;max-width:900px}
#meta{margin:0;font-size:14px;color:var(--mute)}
.status{text-align:right;font-size:14px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.layout{display:grid;grid-template-columns:250px 1fr;gap:0}
aside{border-right:1px solid var(--rule);padding:20px 22px}
main{padding:14px 28px 30px;min-width:0}
.card{border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:8px 0;margin:8px 0 18px}
.card .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px}
.card div.t{font-size:14px;color:var(--mute)}
.big{font:normal 46px/1.05 Georgia,"Times New Roman",serif}
.bignote{font-size:13px;color:var(--mute);margin-bottom:6px}
.bar{height:4px;background:var(--rule);margin:4px 0 20px}.bar i{display:block;height:4px}
[role=tablist]{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin-bottom:18px}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;padding:10px 14px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
[role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.q{font:italic 18px Georgia,serif;margin:0 0 14px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:1px solid var(--rule)}
.tile{padding:14px 18px 14px 0;border-bottom:1px solid var(--rule)}
.tile:nth-child(even){padding-left:18px;border-left:1px solid var(--rule)}
.tile .big{margin:4px 0}
.tile .sub{font-size:14px}
.how{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;color:var(--mute);margin-top:6px}
h2.fig{font:normal 20px Georgia,serif;margin:26px 0 8px}
.btn{border:1px solid var(--ink);background:none;padding:8px 14px;margin-right:8px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.btn:hover:not(:disabled){background:var(--ink);color:var(--paper)}
.btn:disabled{opacity:.4;cursor:not-allowed}
.sec{display:flex;width:100%;justify-content:space-between;background:none;border:0;border-top:1px solid var(--rule);padding:12px 0;text-align:left;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.sec[aria-expanded=true]{color:var(--red)}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font:normal 18px Georgia,serif;padding:6px 0 8px}
caption .mono{margin-right:8px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);text-align:left;border-bottom:1px solid var(--ink);padding:6px 8px}
td{border-bottom:1px solid var(--rule);padding:7px 8px;vertical-align:top}
.num{text-align:right}
td.n button{background:none;border:0;color:var(--red);font:bold 15px ui-monospace,Menlo,Consolas,monospace;padding:0}
tr.row{cursor:pointer}tr.row:hover{background:#ece6d9}
tr.detail td{background:#faf7f0;padding:14px 16px}
.para{font:17px/1.65 Georgia,serif;max-width:78ch}
.sus{outline:1px solid var(--red);padding:0 2px;margin:0 1px}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0;font-size:14px}
.cmp div{border-top:1px solid var(--rule);padding-top:4px}
pre{white-space:pre-wrap;font:13px/1.5 ui-monospace,Menlo,Consolas,monospace;background:var(--paper);border:1px solid var(--rule);padding:10px;margin:8px 0}
.pg{color:var(--red)}
.note{font-size:14px;color:var(--mute);margin:6px 0 10px}
ul.checks{list-style:none;margin:0;padding:0}
ul.checks li{border-top:1px solid var(--rule);padding:9px 0;font-size:14.5px}
ul.checks .nm{font-weight:600}
.chip{display:inline-flex;gap:8px;align-items:center;border:1px solid var(--red);color:var(--red);padding:2px 8px;font-size:13px;margin-bottom:10px}
.chip button{background:none;border:0;color:var(--red);font-weight:bold}
.linkbtn{background:none;border:0;color:var(--red);text-decoration:underline;padding:0;font-size:inherit}
.hl{border-top:1px solid var(--rule);padding:6px 0 10px}
.ln{font:13px ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap}
.ln b{color:var(--mute);font-weight:normal;margin-right:8px}
footer{border-top:1px solid var(--rule);padding:14px 28px;font-size:13px;color:var(--mute)}
@media(max-width:820px){.layout{grid-template-columns:1fr}aside{border-right:0;border-bottom:1px solid var(--rule)}.tiles{grid-template-columns:1fr}.tile:nth-child(even){padding-left:0;border-left:0}.cmp{grid-template-columns:1fr}main{padding:14px}}
</style>
</head>
<body>
<header>
 <div class="top">
  <div>
   <div class="mono">UN DOCUMENT · PDF TEXT</div>
   <h1 id="title"></h1>
   <p id="meta"></p>
  </div>
  <div class="status" id="status"></div>
 </div>
</header>
<div class="layout">
 <aside id="rail" aria-label="Document summary"></aside>
 <main>
  <div role="tablist" aria-label="Views" id="tabs">
   <button role="tab" id="t0" aria-controls="p0" aria-selected="true" data-i="0">01 RESULT</button>
   <button role="tab" id="t1" aria-controls="p1" aria-selected="false" tabindex="-1" data-i="1">02 PARAGRAPHS</button>
  </div>
  <section role="tabpanel" id="p0" aria-labelledby="t0"></section>
  <section role="tabpanel" id="p1" aria-labelledby="t1" hidden></section>
 </main>
</div>
<footer id="foot"></footer>

<script>
(function(){
var D=window.WORKSHOP_DATA||{};
var DOC=D.pdf_text; if(Array.isArray(DOC)) DOC={records:DOC}; DOC=DOC||{};
var recs=(DOC.records||[]).slice().sort(function(a,b){return a.page-b.page});
var symbol=DOC.symbol||'';
var REF=DOC.reference||null;
var hasN=REF&&typeof REF.paragraphs==='number';
var hasFW=REF&&REF.first_words&&typeof REF.first_words==='object';
var P=recs.length;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function norm(s){return String(s).replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\s+/g,' ').trim()}

/* ---------- pipeline ---------- */
var pagesMap={},warnings=[],displaced=[],headerPages=[],numPages=[],allLines=[],body=[];
recs.forEach(function(r){
 var lines=String(r.text||'').split(/\r?\n/).map(function(t){return{t:t.replace(/\s+$/,''),page:r.page,kind:null,suspect:false,para:null}});
 pagesMap[r.page]=lines; allLines=allLines.concat(lines);
 var first=null;for(var a=0;a<lines.length;a++){if(lines[a].t.trim()){first=lines[a];break}}
 if(first&&first.t.trim()===symbol){first.kind='header';headerPages.push(r.page)}else warnings.push('page '+r.page+': first line is not the symbol');
 var k=lines.length-1;
 while(k>=0){
  var s=lines[k].t.trim();
  if(!s){k--;continue}
  if(lines[k].kind) break;
  if(/^GE\./.test(s)||/^\d{6}(\s+\d{6})*$/.test(s)){lines[k].kind='footer'}
  else if(/^\d{1,3}$/.test(s)){lines[k].kind='footer';if(+s===r.page)numPages.push(r.page);else displaced.push({page:r.page,value:s})}
  else break;
  k--;
 }
 lines.forEach(function(l){if(l.kind===null)body.push(l)});
});
var isPara=function(t){return /^\d{1,3}\.$/.test(t)||/^\d{1,3}\. .+$/.test(t)};
var LAB=/^([IVX]+|[A-Z])\.$/;
function nextNB(i){for(var j=i+1;j<body.length;j++)if(body[j].t.trim())return j;return -1}
function headLike(t){return t.length<=90&&/^[A-Z]/.test(t)&&!/[.;:,?\d]$/.test(t)&&!/[.;,:?]["”’')]$/.test(t)}
function headTail(t){return t.length<=90&&/^[a-z(]/.test(t)&&!/[.;:,?\d]$/.test(t)&&!/[.;,:?]["”’')]$/.test(t)}
var paras=[],headings=[],events=[],cur=null,started=false,curPart=null,curSub=null,curUn=null,curSection=null;
for(var i=0;i<body.length;i++){
 var l=body[i],t=l.t.trim(),m;
 if(!t)continue;
 if((m=t.match(/^(\d{1,3})\.$/))||(m=t.match(/^(\d{1,3})\. (.+)$/))){
  started=true;
  cur={n:+m[1],lines:[],section:curSection,part:curPart,path:[curPart,curSub,curUn].filter(Boolean).join(' › ')};
  l.kind='paragraph';l.para=cur.n;
  if(m[2])cur.lines.push({t:m[2].trim(),page:l.page,src:l});
  paras.push(cur);events.push({type:'para',p:cur});
  continue;
 }
 if((m=t.match(LAB))){
  started=true;l.kind='heading';
  var j=i+1,title=[];
  while(j<body.length){
   var u=body[j].t.trim();
   if(!u){
    if(!title.length){j++;continue}
    var nj=nextNB(j);
    if(nj>=0&&/^[a-z(]/.test(body[nj].t.trim())){j=nj;continue}
    break;
   }
   if(isPara(u)||LAB.test(u))break;
   title.push(u);body[j].kind='heading';j++;
  }
  i=j-1;
  var roman=/^[IVX]+$/.test(m[1]);
  var h={labelled:true,level:roman?'part':'sub',text:m[1]+'. '+title.join(' '),before:paras.length+1};
  h.text=h.text.replace(/\s+$/,'');
  headings.push(h);events.push({type:'heading',h:h});
  if(roman){curPart=h.text;curSub=null;curUn=null}else{curSub=h.text;curUn=null}
  curSection=h.text;cur=null;continue;
 }
 if(!cur){ if(!started){l.kind='cover'} continue; }
 var nx=nextNB(i),made=false;
 if(nx>=0&&isPara(body[nx].t.trim())&&body[nx].page===l.page){
  var prev=cur.lines[cur.lines.length-1];
  var pOk=prev&&prev.page===l.page&&cur.lines.length>1;
  var texts=null,srcs=null;
  if(headLike(t)){
   texts=[t];srcs=[l];
   if(pOk&&headLike(prev.t)){cur.lines.pop();texts.unshift(prev.t);srcs.unshift(prev.src)}
   made=true;
  }else if(headTail(t)&&pOk&&headLike(prev.t)){
   cur.lines.pop();texts=[prev.t,t];srcs=[prev.src,l];made=true;
  }
  if(made){
   srcs.forEach(function(s){s.kind='heading'});
   var hh={labelled:false,level:'un',text:texts.join(' ').replace(/\s+/g,' '),before:paras.length+1};
   headings.push(hh);events.push({type:'heading',h:hh});
   curUn=hh.text;curSection=hh.text;cur=null;
  }
 }
 if(!made){l.kind='paragraph';l.para=cur.n;cur.lines.push({t:t,page:l.page,src:l})}
}
var hyph=0;
allLines.forEach(function(l){if(l.kind==='paragraph'&&/[A-Za-z]-$/.test(l.t.trim()))hyph++});

var ABBR=/^(no|nos|art|arts|para|paras|p|pp|vol|ch|chap|sect|e\.g|i\.e|cf)\.$/i;
function sixWords(text){
 var toks=text.split(/\s+/).filter(Boolean),out=[];
 for(var q=0;q<toks.length&&out.length<6;q++){
  var w=toks[q];
  if(/^\d{1,3}$/.test(w)){
   var pv=out[out.length-1];
   if(pv&&/[.,”’"]$/.test(pv)&&!ABBR.test(pv))continue;
  }else{
   var mm=w.match(/^(.*[a-z.,;:)\]”’"'])(\d{1,3})$/);
   if(mm)w=mm[1];
  }
  out.push(w);
 }
 return out.join(' ');
}
function trigger(s){
 if(/^\d{1,3}$/.test(s))return'bare number';
 if(/^\* /.test(s))return'starts with an asterisk';
 if(/^\d{1,3} [A-Z“"‘']/.test(s))return'starts with a number and a space';
 return null;
}
paras.forEach(function(p){
 p.text=p.lines.map(function(x){return x.t}).join(' ').replace(/\s+/g,' ').trim();
 p.text_lines=p.lines.map(function(x){return x.t});
 p.words=p.text?p.text.split(/\s+/).length:0;
 p.page_start=p.lines.length?p.lines[0].page:null;
 p.page_end=p.lines.length?p.lines[p.lines.length-1].page:null;
 p.triggers=[];var sp=null;
 p.lines.forEach(function(x){
  var w=trigger(x.t.trim());
  if(sp===x.page){x.suspect=true}
  else if(w){x.suspect=true;sp=x.page;p.triggers.push({page:x.page,why:w})}
  if(x.suspect)x.src.suspect=true;
 });
 p.suspectCount=p.lines.filter(function(x){return x.suspect}).length;
 p.over=p.words>300;
 p.flagged=p.suspectCount>0||p.over;
 p.fw=sixWords(p.text);
 p.ref=hasFW&&REF.first_words[String(p.n)]!=null?String(REF.first_words[String(p.n)]):null;
 p.fm=p.ref===null?null:norm(p.fw)===norm(p.ref);
 p.citation=symbol+', para. '+p.n;
});
var suspectPages={};paras.forEach(function(p){p.lines.forEach(function(x){if(x.suspect)suspectPages[x.page]=1})});
var pagesFlagged=Object.keys(suspectPages).length;
var flaggedParas=paras.filter(function(p){return p.flagged});
var suspectLines=paras.reduce(function(a,p){return a+p.suspectCount},0);
var frows=[];
paras.forEach(function(p,pi){
 var by={};
 p.lines.forEach(function(x){if(x.suspect){by[x.page]=by[x.page]||{n:0,why:[]};by[x.page].n++}});
 p.triggers.forEach(function(tr){if(by[tr.page]&&by[tr.page].why.indexOf(tr.why)<0)by[tr.page].why.push(tr.why)});
 Object.keys(by).forEach(function(pg){frows.push({page:+pg,pi:pi,n:by[pg].n,why:by[pg].why.join('; ')})});
 if(p.over)frows.push({page:p.page_start,pi:pi,n:0,why:'paragraph over 300 words'});
});
frows.sort(function(a,b){return a.page-b.page||a.pi-b.pi});
var fwMismatch=paras.filter(function(p){return p.fm===false});
var fwMatch=paras.filter(function(p){return p.fm===true}).length;

/* ---------- exports ---------- */
function limits(p){return p.flagged?('footnotes not separated; '+(p.suspectCount?p.suspectCount+' line'+(p.suspectCount>1?'s':'')+' may sit inside this paragraph':'paragraph over 300 words, may contain footnote text')):'footnotes not separated'}
function buildJSON(){
 return paras.map(function(p){return{symbol:symbol,paragraph:p.n,section:p.section||'',part:p.part||'',page_start:p.page_start,page_end:p.page_end,text:p.text,text_lines:p.text_lines.join(' | '),flagged:p.flagged,first_words_match:p.fm,citation:p.citation,doc_url:DOC.doc_url||'',limitations:limits(p)}});
}
function buildMD(){
 var o=['---','title: '+JSON.stringify(DOC.title||''),'symbol: '+JSON.stringify(symbol),'adopted: '+JSON.stringify(REF&&REF.adopted?String(REF.adopted):''),'source_url: '+JSON.stringify(DOC.doc_url||''),'extracted: '+new Date().toISOString().slice(0,10),'paragraphs_found: '+paras.length,'paragraphs_expected: '+(hasN?REF.paragraphs:'unknown'),'pages_flagged: '+pagesFlagged,'footnotes: '+JSON.stringify('not separated; the document has '+(REF&&REF.footnotes!=null?REF.footnotes:'an unknown number')),'---',''];
 events.forEach(function(e){
  if(e.type==='heading')o.push((e.h.level==='part'?'## ':'### ')+e.h.text,'');
  else o.push('**'+e.p.n+'** '+e.p.text+(e.p.flagged?' (flagged: may contain footnote text)':''),'');
 });
 return o.join('\n');
}
function fname(ext){return (symbol||'document').replace(/\//g,'-')+'.'+ext}
function download(name,mime,content){
 var b=new Blob([content],{type:mime+';charset=utf-8'}),u=URL.createObjectURL(b),a=document.createElement('a');
 a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u)},1000);
}

/* ---------- checks ---------- */
var checks=[];
function chk(name,expect,found,status,rows,list){checks.push({name:name,expect:expect,found:found,status:status,rows:rows||null,list:list||null})}
(function(){
 var n=paras.length;
 chk('Paragraph count','the numbered paragraphs found equal the reference count',n+' found'+(hasN?' / '+REF.paragraphs+' expected':' / no reference'),hasN?(n===REF.paragraphs?'pass':'fail'):'notrun');
 var exp=1,issues=[],bad=[];
 paras.forEach(function(p){
  if(p.n===exp){exp++}
  else if(p.n>exp){issues.push('gap: para. '+exp+(p.n-1>exp?'–'+(p.n-1):'')+' missing before para. '+p.n+' (page '+p.page_start+')');bad.push(p.n);exp=p.n+1}
  else{issues.push('duplicate or out of order: para. '+p.n+' (page '+p.page_start+')');bad.push(p.n)}
 });
 chk('Numbering','paragraphs are numbered exactly 1 to n in order',n?(issues.length?issues.length+' problem(s)':'1 to '+(exp-1)+', no gaps or duplicates'):'no paragraphs',n&&!issues.length?'pass':'fail',bad,issues);
 chk('First words','the first six words of each paragraph equal the reference',hasFW?fwMismatch.length+' differ, '+fwMatch+' match':'no reference',hasFW?(fwMismatch.length?'fail':'pass'):'notrun',fwMismatch.map(function(p){return p.n}));
 chk('Pages flagged','pages where footnote text may sit inside a paragraph (a flag, not a failure: the count can be right while footnote text is inside)',pagesFlagged+' pages flagged, '+flaggedParas.length+' paragraphs to check against the PDF','note',flaggedParas.map(function(p){return p.n}));
 var sp={};paras.forEach(function(p){if(p.suspectCount)sp[p.n]=1});
 chk('Suspect lines','suspect lines are counted and none is removed',suspectLines+' suspect lines on '+pagesFlagged+' pages, in '+Object.keys(sp).length+' paragraphs; none removed','note');
 chk('Headers','the first line of every page is the symbol',headerPages.length+' of '+P+' pages',headerPages.length===P&&P>0?'pass':'fail',null,warnings);
 var firstPg=recs.length?recs[0].page:null,missNum=recs.filter(function(r){return r.page!==firstPg&&numPages.indexOf(r.page)<0}).map(function(r){return r.page});
 chk('Page numbers in footers','every page except the first has its page number in the footer',numPages.length+' pages have one'+(missNum.length?'; missing on '+missNum.join(', '):''),missNum.length?'fail':'pass');
 chk('Displaced footnote numbers','bare numbers in the footer other than the page number are removed, not put back',displaced.length+' removed',"note",null,displaced.map(function(d){return'page '+d.page+': '+d.value}));
 var lab=headings.filter(function(h){return h.labelled}),un=headings.filter(function(h){return!h.labelled});
 chk('Headings','headings are kept apart from paragraph text; unlabelled ones are listed so a paragraph\'s last line mistaken for a heading can be spotted',lab.length+' labelled, '+un.length+' unlabelled','note',null,un.map(function(h){return'before para. '+h.before+': '+h.text}));
 chk('Line-end hyphens','lines ending with a hyphen would need joining; none is expected',hyph+' such lines; no hyphen joining done','note');
 var nonEmpty=allLines.filter(function(l){return l.t.trim()}),cnt={},unc=[];
 nonEmpty.forEach(function(l){if(l.kind){cnt[l.kind]=(cnt[l.kind]||0)+1}else unc.push(l)});
 var sum=0;Object.keys(cnt).forEach(function(k){sum+=cnt[k]});
 var plines=paras.reduce(function(a,p){return a+p.lines.length},0);
 var ok=sum===nonEmpty.length&&!unc.length&&plines===(cnt.paragraph||0);
 chk('Nothing lost','every non-empty line is classified exactly once; the counts sum to the total',Object.keys(cnt).map(function(k){return k+' '+cnt[k]}).join(', ')+' = '+sum+' of '+nonEmpty.length+' lines',ok?'pass':'fail',null,unc.map(function(l){return'page '+l.page+': '+l.t}));
 var rt=-1;try{rt=JSON.parse(JSON.stringify(buildJSON())).length}catch(e){}
 chk('Export round trip','the JSON to download parses back with as many records as the table has rows',rt+' records / '+paras.length+' rows',rt===paras.length?'pass':'fail');
})();
var failN=checks.filter(function(c){return c.status==='fail'}).length;
var passN=checks.filter(function(c){return c.status==='pass'||c.status==='note'}).length;

/* ---------- UI ---------- */
var S={tab:0,open:{},raw:{},sec:{checks:false,flagged:false,heads:false},frow:null,filter:null,focus:null};
function pageRange(p){return p.page_start===p.page_end?String(p.page_start):p.page_start+'–'+p.page_end}
function firstLine(t){return t.length<=120?t:t.slice(0,120).replace(/\s+\S*$/,'')+'…'}
function checkCell(p){
 var r=[];
 if(p.flagged)r.push('<span class="red">may contain footnote text</span>');
 if(p.fm===false)r.push('<span class="red">first words differ</span>');
 if(!r.length)return p.fm===null?'<span class="mono">no reference</span>':'<span class="green">OK</span>';
 return r.join('; ');
}
function stLabel(c){
 return c.status==='pass'?'<b class="green">pass</b>':c.status==='fail'?'<b class="red">check failed</b>':c.status==='notrun'?'<b>not run</b>':'<b>noted</b>';
}
function renderHead(){
 document.getElementById('title').textContent=DOC.title||'(untitled document)';
 document.getElementById('meta').innerHTML=(symbol?'<a href="'+esc(DOC.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(symbol)+'</a>':'')+' · adopted '+esc(REF&&REF.adopted?REF.adopted:'unknown')+' · '+P+' pages · '+esc(DOC.source||'');
 var good=failN===0;
 document.getElementById('status').innerHTML='<div><span class="dot" style="background:'+(good?'var(--green)':'var(--red)')+'"></span>'+(good?passN+' of '+checks.length+' checks pass':failN+' check'+(failN>1?'s':'')+' failed')+'</div><div class="'+(pagesFlagged?'red':'')+'">'+pagesFlagged+' pages flagged</div>';
}
function renderRail(){
 var n=paras.length,N=hasN?REF.paragraphs:null,eq=hasN&&n===N;
 var h='<div class="mono">DOCUMENT</div><div class="card"><div class="sym">'+esc(symbol)+'</div><div class="t">'+esc(DOC.title||'')+'</div></div>';
 h+='<div class="big">'+n+'</div><div class="bignote">paragraphs'+(hasN?' of '+N:' (no reference)')+'</div>';
 h+='<div class="bar"><i style="width:'+(hasN&&N?Math.min(100,n/N*100):100)+'%;background:'+(eq?'var(--green)':'var(--red)')+'"></i></div>';
 h+='<div class="big '+(pagesFlagged?'red':'')+'">'+pagesFlagged+'</div><div class="bignote">pages flagged of '+P+': footnote text may sit inside a paragraph</div>';
 h+='<div class="bar"></div><div class="mono">'+passN+' of '+checks.length+' checks pass</div>';
 document.getElementById('rail').innerHTML=h;
}
function tile(label,big,sub,cls,how){
 return '<div class="tile"><div class="mono">'+label+'</div><div class="big '+(cls||'')+'">'+big+'</div><div class="sub '+(cls||'')+'">'+sub+'</div><div class="how">How this is computed: '+how+'</div></div>';
}
function render1(){
 var n=paras.length,h='<p class="q">Did the app find everything the document has?</p>';
 if(!n){h+='<p><b class="red">No numbered paragraphs were found in this file.</b> Exports are disabled.</p>'}
 var diff=hasN?n-REF.paragraphs:0;
 h+='<div class="tiles">';
 h+=tile('PARAGRAPHS FOUND',n,hasN?'the document has '+REF.paragraphs+(diff?' ('+Math.abs(diff)+(diff<0?' short':' over')+')':' — equal'):'no reference in this file',hasN?(diff?'red':'green'):'','lines that are a number and a full stop, alone or followed by text, counted in page order.');
 h+=tile('FIRST WORDS MATCH',hasFW&&hasN?fwMatch+' of '+REF.paragraphs:'—',hasFW?(fwMismatch.length?fwMismatch.length+' differ':'none differ'):'no reference in this file',hasFW&&fwMismatch.length?'red':'','six first words of each paragraph, footnote marks removed, quotes and dashes normalised, against reference.first_words.');
 h+=tile('PAGES FLAGGED',pagesFlagged+' of '+P,'footnote text may sit inside a paragraph: check these paragraphs against the PDF',pagesFlagged?'red':'','pages with a line like "7 E/2003/22…" or a bare number inside a paragraph.');
 h+=tile('FOOTNOTES','not separated','the document has '+(REF&&REF.footnotes!=null?REF.footnotes:'an unknown number')+'; this version leaves them in place and flags them','','not computed: footnote lines stay in the paragraph text.');
 h+='</div>';
 if(fwMismatch.length){
  h+='<h2 class="fig">First words that differ</h2><div class="note">found / reference</div>';
  fwMismatch.slice(0,10).forEach(function(p){h+='<div class="hl"><span class="red">para. '+p.n+':</span> found <i>'+esc(p.fw)+'</i> / reference <i>'+esc(p.ref)+'</i></div>'});
  if(fwMismatch.length>10)h+='<div class="note">and '+(fwMismatch.length-10)+' more</div>';
 }
 h+='<h2 class="fig">Take the paragraphs away</h2><div class="note">JSON and Markdown carry the source, the fields and the known limits.</div>';
 h+='<button class="btn" data-act="dlj"'+(n?'':' disabled')+'>Download JSON</button><button class="btn" data-act="dlm"'+(n?'':' disabled')+'>Download Markdown</button><div style="height:18px"></div>';
 h+='<button class="sec" data-act="sec" data-k="checks" aria-expanded="'+S.sec.checks+'" data-focus="sec-checks"><span>Every check ('+checks.length+')</span><span>'+(S.sec.checks?'−':'+')+'</span></button>';
 if(S.sec.checks){
  h+='<ul class="checks">';
  checks.forEach(function(c,i){
   h+='<li><span class="nm">'+esc(c.name)+'</span> — '+stLabel(c)+'<br>Given this document, having run this code, we expect: '+esc(c.expect)+'.<br><span class="mono">FOUND</span> '+esc(c.found);
   if(c.rows&&c.rows.length)h+=' · <button class="linkbtn" data-act="filter" data-k="'+i+'">show the '+c.rows.length+' row'+(c.rows.length>1?'s':'')+'</button>';
   if(c.list&&c.list.length){h+='<br><span class="note">'+c.list.slice(0,25).map(esc).join('<br>')+(c.list.length>25?'<br>and '+(c.list.length-25)+' more':'')+'</span>'}
   h+='</li>';
  });
  h+='</ul>';
 }
 h+='<button class="sec" data-act="sec" data-k="flagged" aria-expanded="'+S.sec.flagged+'" data-focus="sec-flagged" style="border-bottom:1px solid var(--rule)"><span>Flagged pages ('+pagesFlagged+')</span><span>'+(S.sec.flagged?'−':'+')+'</span></button>';
 if(S.sec.flagged){
  h+='<p class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</p>';
  if(!frows.length)h+='<p>No page is flagged.</p>';
  else{
   h+='<table><caption><span class="mono">TAB.02</span>'+pagesFlagged+' pages flagged, '+flaggedParas.length+' paragraphs to check</caption><thead><tr><th scope="col" class="num">Page</th><th scope="col" class="num">Paragraph</th><th scope="col" class="num">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>';
   frows.forEach(function(f,i){
    var p=paras[f.pi],open=S.frow===i;
    h+='<tr class="row" data-act="frow" data-k="'+i+'"><td class="num"><button class="linkbtn" aria-expanded="'+open+'" data-focus="fr'+i+'" data-act="frow" data-k="'+i+'">'+f.page+'</button></td><td class="num red">'+p.n+'</td><td class="num">'+f.n+'</td><td>'+esc(f.why)+'</td></tr>';
    if(open){
     h+='<tr class="detail"><td colspan="4"><div class="mono">PAGE '+f.page+' · RAW LINES · SUSPECT LINES BOXED · SITS IN PARAGRAPH '+p.n+'</div>';
     (pagesMap[f.page]||[]).forEach(function(l){
      if(!l.t.trim())return;
      var lab=l.kind==='paragraph'?'para '+l.para:(l.kind||'unclassified');
      h+='<div class="ln"><b>'+esc(lab)+'</b>'+(l.suspect?'<span class="sus">'+esc(l.t)+'</span>':esc(l.t))+'</div>';
     });
     h+='<p><button class="linkbtn" data-act="goto" data-k="'+f.pi+'">open paragraph '+p.n+' on tab 02</button></p></td></tr>';
    }
   });
   h+='</tbody></table>';
  }
 }
 document.getElementById('p0').innerHTML=h;
}
function render2(){
 var h='<p class="q">What does each paragraph say, and how do I cite it?</p>';
 h+='<button class="sec" data-act="sec" data-k="heads" aria-expanded="'+S.sec.heads+'" data-focus="sec-heads"><span>Headings found: '+headings.length+'</span><span>'+(S.sec.heads?'−':'+')+'</span></button>';
 if(S.sec.heads){
  h+='<div class="note">Listed so that none can hide inside a paragraph.</div>';
  headings.forEach(function(x){h+='<div class="hl"><span class="mono">'+(x.labelled?(x.level==='part'?'SECTION':'SUBSECTION'):'UNLABELLED')+' · before para. '+x.before+'</span><br>'+esc(x.text)+'</div>'});
 }
 var list=paras.map(function(p,i){return i});
 if(S.filter){
  list=list.filter(function(i){return S.filter.set.indexOf(paras[i].n)>=0});
  h+='<div class="chip" style="margin-top:10px">'+esc(S.filter.name)+': '+list.length+' row'+(list.length===1?'':'s')+' <button data-act="clear" aria-label="Clear filter">×</button></div>';
 }
 if(!paras.length){h+='<p>No numbered paragraphs were found.</p>';document.getElementById('p1').innerHTML=h;return}
 h+='<table><caption><span class="mono">TAB.01</span>'+paras.length+' paragraphs found'+(hasN?', '+REF.paragraphs+' expected':', no reference')+'</caption><thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody>';
 list.forEach(function(i){
  var p=paras[i],op=!!S.open[i];
  h+='<tr class="row" data-act="row" data-k="'+i+'"><td class="n num"><button aria-expanded="'+op+'" data-focus="row'+i+'" data-act="row" data-k="'+i+'" aria-label="Paragraph '+p.n+'">'+p.n+'</button></td><td>'+esc(p.section||'—')+'</td><td>'+pageRange(p)+'</td><td>'+esc(firstLine(p.text))+'</td><td>'+checkCell(p)+'</td></tr>';
  if(op){
   h+='<tr class="detail"><td colspan="5"><div class="mono">'+esc(p.path||'no heading above')+' · '+p.words+' words · page '+pageRange(p)+'</div>';
   h+='<p class="para">'+p.lines.map(function(x){return x.suspect?'<span class="sus">'+esc(x.t)+'</span>':esc(x.t)}).join(' ')+'</p>';
   if(p.flagged)h+='<div class="note red">Boxed lines may be footnote text; check against the PDF.'+(p.over?' Paragraph over 300 words.':'')+'</div>';
   h+='<div class="cmp"><div><span class="mono">REFERENCE FIRST SIX WORDS</span><br>'+(p.ref===null?'no reference in this file':esc(p.ref))+'</div><div><span class="mono">FOUND</span><br>'+esc(p.fw)+'</div></div>';
   h+='<button class="linkbtn" data-act="raw" data-k="'+i+'" aria-expanded="'+!!S.raw[i]+'" data-focus="raw'+i+'">Show the PDF\'s lines</button>';
   if(S.raw[i]){
    var lp=null,o=[];
    p.lines.forEach(function(x){if(x.page!==lp){o.push('<span class="pg">— page '+x.page+' begins —</span>');lp=x.page}o.push(x.suspect?'<span class="sus">'+esc(x.t)+'</span>':esc(x.t))});
    h+='<pre>'+o.join('\n')+'</pre>';
   }
   h+='<p><button class="btn" data-act="copy" data-k="'+i+'">Copy citation</button><span class="mono">'+esc(p.citation)+'</span></p></td></tr>';
  }
 });
 h+='</tbody></table>';
 document.getElementById('p1').innerHTML=h;
}
function render(){
 renderHead();renderRail();render1();render2();
 [0,1].forEach(function(i){
  var on=S.tab===i;
  document.getElementById('p'+i).hidden=!on;
  var t=document.getElementById('t'+i);t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;
 });
 if(S.focus){var el=document.querySelector('[data-focus="'+S.focus+'"]');if(el)el.focus();S.focus=null}
}
function setTab(i,focus){S.tab=i;render();if(focus)document.getElementById('t'+i).focus()}
document.getElementById('tabs').addEventListener('click',function(e){var b=e.target.closest('[role=tab]');if(b)setTab(+b.dataset.i)});
document.getElementById('tabs').addEventListener('keydown',function(e){
 var k=e.key;if(k==='ArrowRight'||k==='ArrowLeft'||k==='Home'||k==='End'){
  e.preventDefault();var i=k==='Home'?0:k==='End'?1:(S.tab+(k==='ArrowRight'?1:-1)+2)%2;setTab(i,true);
 }
});
function copyText(s,btn){
 var done=function(){var o=btn.textContent;btn.textContent='Copied';setTimeout(function(){btn.textContent='Copy citation'},2000)};
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(s).then(done,function(){fallback()})}else fallback();
 function fallback(){var ta=document.createElement('textarea');ta.value=s;document.body.appendChild(ta);ta.select();try{document.execCommand('copy')}catch(e){}ta.remove();done()}
}
document.addEventListener('click',function(e){
 var b=e.target.closest('[data-act]');if(!b)return;
 var a=b.dataset.act,k=b.dataset.k;
 if(a==='dlj'){download(fname('json'),'application/json',JSON.stringify(buildJSON(),null,2));return}
 if(a==='dlm'){download(fname('md'),'text/markdown',buildMD());return}
 if(a==='copy'){copyText(paras[+k].citation,b);return}
 if(a==='sec'){S.sec[k]=!S.sec[k];S.focus='sec-'+k}
 else if(a==='row'){S.open[k]=!S.open[k];S.focus='row'+k}
 else if(a==='raw'){S.raw[k]=!S.raw[k];S.focus='raw'+k}
 else if(a==='frow'){S.frow=S.frow===+k?null:+k;S.focus='fr'+k}
 else if(a==='filter'){var c=checks[+k];S.filter={name:c.name,set:c.rows};S.tab=1}
 else if(a==='clear'){S.filter=null}
 else if(a==='goto'){S.tab=1;S.open[k]=true;S.focus='row'+k}
 render();
 if(a==='filter'||a==='goto')window.scrollTo(0,0);
});
document.getElementById('foot').innerHTML='Source: '+esc(DOC.source||'—')+' · built '+esc(DOC.built||'—')+' · Done by this page\'s code; no model was called and nothing left the browser.';
render();
})();
</script>
</body>
</html>
```