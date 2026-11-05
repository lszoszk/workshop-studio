I built the app as a single page with the two tabs you described, RESULT and PARAGRAPHS. It runs the whole pipeline on load from `WORKSHOP_DATA.pdf_text` and compares the result with the document's own reference. I have not run it against the real file, so the counts and checks will only show once you open it.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraphs out of a PDF</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
a{color:#9b2335}
:focus-visible{outline:3px solid #9b2335;outline-offset:2px}
header.top{padding:18px 28px 12px;border-bottom:1px solid #d9d2c3;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}
header.top h1{font:normal 28px/1.2 Georgia,"Times New Roman",serif;margin:4px 0 6px;max-width:820px}
.meta{font-size:14px}
.status{text-align:right;font-size:14px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;background:#1f5f3a}
.dot.red{background:#9b2335}
.wrap{display:grid;grid-template-columns:250px 1fr;gap:0}
aside{border-right:1px solid #d9d2c3;padding:20px 22px}
main{padding:0 28px 28px;min-width:0}
.card{border:1px solid #d9d2c3;padding:10px 12px;margin:8px 0 18px;font-size:14px}
.card b{display:block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;margin-bottom:4px}
.big{font:normal 48px/1 Georgia,"Times New Roman",serif}
.red{color:#9b2335}.green{color:#1f5f3a}
.bar{height:5px;background:#d9d2c3;margin:6px 0 16px}.bar i{display:block;height:5px;background:#1f5f3a}.bar i.r{background:#9b2335}
.hint{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;color:#5b564c}
[role=tablist]{display:flex;gap:4px;border-bottom:1px solid #d9d2c3;margin:0 0 20px}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;padding:14px 16px 10px;cursor:pointer;color:#1d1b18;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em}
[role=tab][aria-selected=true]{color:#9b2335;border-bottom-color:#9b2335}
h2.q{font:normal 22px/1.3 Georgia,"Times New Roman",serif;margin:0 0 16px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:0;border-top:1px solid #d9d2c3;border-left:1px solid #d9d2c3}
.tile{padding:14px 16px 12px;border-right:1px solid #d9d2c3;border-bottom:1px solid #d9d2c3}
.tile .big{margin:6px 0 4px}
.tile p{margin:4px 0;font-size:14px}
.how{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;color:#5b564c;margin-top:8px}
.list{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;margin:12px 0 0;padding:0;list-style:none}
h3.s{font:normal 20px Georgia,serif;margin:28px 0 8px}
.btn{font:inherit;font-size:15px;background:#fff;border:1px solid #1d1b18;padding:7px 14px;margin-right:8px;cursor:pointer;color:#1d1b18}
.btn:disabled{opacity:.4;cursor:not-allowed}
.acc{display:block;width:100%;text-align:left;background:none;border:0;border-top:1px solid #d9d2c3;padding:12px 0;cursor:pointer;font:inherit;color:#1d1b18}
.acc .mono::before{content:"+ ";color:#9b2335}
.acc[aria-expanded=true] .mono::before{content:"− "}
.accbody{padding:0 0 14px}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{caption-side:top;text-align:left;font:normal 18px Georgia,serif;padding:6px 0}
caption .mono{display:block;color:#5b564c;font-size:11px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:1px solid #1d1b18;padding:6px 8px}
td{border-bottom:1px solid #d9d2c3;padding:7px 8px;vertical-align:top}
.num{text-align:right}
td.n button,.rowbtn{font:inherit;background:none;border:0;color:#9b2335;font-weight:bold;cursor:pointer;padding:2px 6px;text-decoration:underline}
tr.row{cursor:pointer}
tr.row:hover{background:#ece6d8}
.detail{padding:10px 8px 16px 16px;border-left:3px solid #9b2335;background:#faf7f0}
.ptext{font-size:16px;line-height:1.6;max-width:80ch}
.sus{border:1px solid #9b2335;padding:0 2px}
pre.lines{white-space:pre-wrap;font:13px/1.5 ui-monospace,Menlo,Consolas,monospace;background:#fff;border:1px solid #d9d2c3;padding:10px;max-width:90ch}
.pg{color:#9b2335}
.cols{display:flex;gap:30px;flex-wrap:wrap;margin:6px 0 10px;font-size:14px}
.link{background:none;border:0;color:#9b2335;text-decoration:underline;cursor:pointer;font:inherit;font-size:14px;padding:2px 0;margin-right:12px}
.chk{list-style:none;padding:0;margin:0}
.chk li{border-bottom:1px solid #d9d2c3;padding:9px 0;font-size:14.5px}
.pass{color:#1f5f3a;font-weight:bold}.fail{color:#9b2335;font-weight:bold}.note{color:#5b564c;font-weight:bold}
.warn{border-left:3px solid #9b2335;padding:6px 12px;margin:6px 0 12px;font-size:14px;background:#faf7f0}
footer{border-top:1px solid #d9d2c3;padding:14px 28px;font-size:13px;color:#5b564c}
.dim{color:#8a8374}
@media(max-width:820px){.wrap{grid-template-columns:1fr}aside{border-right:0;border-bottom:1px solid #d9d2c3}}
</style>
</head>
<body>
<header class="top" id="top"></header>
<div class="wrap">
<aside id="rail" aria-label="Document summary"></aside>
<main>
<div role="tablist" aria-label="Views" id="tabs">
<button role="tab" id="t1" aria-controls="p1" aria-selected="true" tabindex="0">01 RESULT</button>
<button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">02 PARAGRAPHS</button>
</div>
<section role="tabpanel" id="p1" aria-labelledby="t1"></section>
<section role="tabpanel" id="p2" aria-labelledby="t2" hidden></section>
</main>
</div>
<footer id="foot"></footer>
<script>
(function(){
var D=(window.WORKSHOP_DATA&&window.WORKSHOP_DATA.pdf_text)||{};
var records=Array.isArray(D.records)?D.records.slice().sort(function(a,b){return a.page-b.page}):[];
var ref=D.reference||{};
var symbol=D.symbol||'';
var esc=function(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
var $=function(id){return document.getElementById(id)};
function numOrNull(x){return (x!==undefined&&x!==null&&x!==''&&isFinite(Number(x)))?Number(x):null}
var refP=numOrNull(ref.paragraphs), refFN=numOrNull(ref.footnotes);
var refFW=(ref.first_words&&typeof ref.first_words==='object')?ref.first_words:null;

if(!records.length){
  $('top').innerHTML='<div><div class="mono">UN DOCUMENT · PDF TEXT</div><h1>No pages found</h1></div>';
  $('p1').innerHTML='<p>The attached file has no pages. Drag the PDF text file into the chat again.</p>';
  return;
}

/* ---------- pipeline ---------- */
var warns=[],pageStore={},body=[],footerNums=[],pagesWithNum=0,headerOk=0,hyph=0,totalNonEmpty=0,allLines=[];
records.forEach(function(r){
  var raw=String(r.text||'').replace(/\r/g,'').split('\n');
  var L=raw.map(function(t,i){var tr=t.trim();return {page:r.page,i:i,text:t,tr:tr,kind:tr===''?'empty':'body',sus:false,para:null}});
  pageStore[r.page]=L;
  var first=null;for(var a=0;a<L.length;a++){if(L[a].kind!=='empty'){first=L[a];break}}
  if(first&&first.tr===symbol){first.kind='header';headerOk++}else warns.push('page '+r.page+': first line is not the symbol');
  var hasNum=false;
  for(var k=L.length-1;k>=0;k--){
    var l=L[k];if(l.kind==='empty')continue;if(l.kind==='header')break;
    var t=l.tr;
    if(/^GE\./.test(t)||/^\d{6}(\s+\d{6})*$/.test(t)){l.kind='footer'}
    else if(/^\d{1,3}$/.test(t)){l.kind='footer';if(Number(t)===Number(r.page)&&!hasNum)hasNum=true;else footerNums.push({page:r.page,num:t})}
    else break;
  }
  if(hasNum)pagesWithNum++;
  L.forEach(function(l){
    if(l.kind!=='empty'){totalNonEmpty++;allLines.push(l)}
    if(l.kind==='body'){body.push(l);if(/[A-Za-z]-$/.test(l.tr))hyph++}
  });
});
var N=body;
var reA=/^(\d{1,3})\.$/,reB=/^(\d{1,3})\. (.+)$/,reLabel=/^([IVX]+|[A-Z])\.$/;
function startOf(t){var m=reA.exec(t);if(m)return {n:+m[1],rest:''};m=reB.exec(t);if(m)return {n:+m[1],rest:m[2]};return null}
function cand(l){if(!l)return false;var t=l.tr;return t.length<=90&&/^[A-Z]/.test(t)&&!/[.;:,\d]$/.test(t)&&!startOf(t)&&!reLabel.test(t)}
function cand2(l){if(!l)return false;var t=l.tr;return t.length<=90&&/^[A-Za-z(]/.test(t)&&!/[.;:,\d]$/.test(t)&&!startOf(t)&&!reLabel.test(t)}
var heads=[],paras=[],items=[];
var sec='',part='',sub='',unl='',cur=null;
function addHead(lab,text,level,page){
  var full=(lab?lab+' ':'')+text;full=full.trim();
  var h={label:lab,text:text,level:level,page:page,full:full,kind:lab?'labelled':'unlabelled'};
  if(level===1){part=full;sub='';unl=''}else if(level===2){sub=full;unl=''}else{unl=full}
  sec=full;heads.push(h);items.push({type:'h',h:h});
}
var firstReal=-1;
for(var q=0;q<N.length;q++){if(reLabel.test(N[q].tr)||startOf(N[q].tr)){firstReal=q;break}}
var stop=firstReal<0?N.length:firstReal;
for(var c0=0;c0<stop;c0++)N[c0].kind='cover';
var i=stop;
while(i<N.length){
  var l=N[i],t=l.tr,st=startOf(t);
  if(st){
    cur={n:st.n,section:sec,part:part,path:[part,sub,unl].filter(Boolean).join(' › '),lines:[],objs:[l],page_start:l.page};
    l.kind='para';
    if(st.rest)cur.lines.push({page:l.page,text:st.rest,obj:l,first:true});
    paras.push(cur);items.push({type:'p',p:cur});
    i++;continue;
  }
  var lm=reLabel.exec(t);
  if(lm){
    l.kind='heading';
    var j=i+1,hl=[];
    while(j<N.length&&hl.length<4&&!reLabel.test(N[j].tr)&&!startOf(N[j].tr)){hl.push(N[j]);j++}
    var entries=[];
    hl.forEach(function(x){x.kind='heading';if(entries.length&&/^[a-z(]/.test(x.tr))entries[entries.length-1].text+=' '+x.tr;else entries.push({text:x.tr,page:x.page})});
    var lab=lm[1]+'.',lvl=/^[IVX]+$/.test(lm[1])?1:2;
    if(!entries.length)addHead(lab,'',lvl,l.page);
    entries.forEach(function(e,ix){if(ix===0)addHead(lab,e.text,lvl,l.page);else addHead('',e.text,3,e.page)});
    cur=null;
    i=j;continue;
  }
  if(cand(l)&&N[i+1]&&cand2(N[i+1])&&N[i+2]&&startOf(N[i+2].tr)){
    l.kind='heading';N[i+1].kind='heading';addHead('',l.tr+' '+N[i+1].tr,3,l.page);i+=2;continue;
  }
  if(cand(l)&&N[i+1]&&startOf(N[i+1].tr)){
    l.kind='heading';addHead('',l.tr,3,l.page);i++;continue;
  }
  if(cur){cur.lines.push({page:l.page,text:l.tr,obj:l});cur.objs.push(l);l.kind='para'}
  else l.kind='cover';
  i++;
}
/* suspect lines */
function susReason(t){
  if(/^\d{1,3}$/.test(t))return 'bare number';
  if(/^\d{1,3} (?:[A-Z]|["“”‘’'])/.test(t))return 'starts with a number and a space';
  if(/^\* /.test(t))return 'starts with an asterisk';
  return null;
}
var flagPages={};
var ABBR=/^\(?(?:no|nos|art|arts|para|paras|p|pp)\.$/i;
function cleanTokens(text){
  var raw=text.split(/\s+/).filter(Boolean).slice(0,24),out=[];
  raw.forEach(function(tok){
    if(/^\d+$/.test(tok)){var pv=out[out.length-1];if(pv&&/[.,”"’']$/.test(pv)&&!ABBR.test(pv))return;out.push(tok);return}
    var m=/^(.*[A-Za-z.,;:”"’')])\d{1,3}$/.exec(tok);
    out.push(m&&!ABBR.test(m[1])?m[1]:tok);
  });
  return out;
}
function norm(s){return String(s).replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[–—]/g,'-').replace(/\s+/g,' ').trim()}
paras.forEach(function(p){
  var curPage=null,flag=false;
  p.lines.forEach(function(ln){
    if(ln.page!==curPage){curPage=ln.page;flag=false}
    var reason=null;
    if(!flag&&!ln.first){reason=susReason(ln.obj.tr);if(reason)flag=true}
    ln.sus=flag&&!ln.first;ln.obj.sus=ln.sus;
    if(ln.sus){
      var fp=flagPages[ln.page]=flagPages[ln.page]||{page:ln.page,paras:[],count:0,reasons:[]};
      fp.count++;if(fp.paras.indexOf(p.n)<0)fp.paras.push(p.n);
      if(reason&&fp.reasons.indexOf(reason)<0)fp.reasons.push(reason);
    }
  });
  p.susCount=p.lines.filter(function(x){return x.sus}).length;
  p.text=p.lines.map(function(x){return x.text.trim()}).join(' ').replace(/\s+/g,' ').trim();
  p.words=p.text?p.text.split(' ').length:0;
  p.long=p.words>300;
  p.flagged=p.susCount>0||p.long;
  p.page_end=p.lines.length?p.lines[p.lines.length-1].page:p.page_start;
  p.found6=cleanTokens(p.text).slice(0,6).join(' ');
  var rf=refFW&&refFW[String(p.n)];
  p.ref6=(rf!==undefefined_())?rf:null;
  p.fwMatch=(refFW&&rf!==undefined&&rf!==null)?norm(p.found6)===norm(rf):null;
  p.citation=symbol+', para. '+p.n;
  p.text_lines=p.lines.map(function(x){return x.text.trim()}).join(' | ');
});
function undefefefined(){}
function undefefined_(){return void 0}
paras.forEach(function(p,ix){p.idx=ix});
var fpList=Object.keys(flagPages).map(Number).sort(function(a,b){return a-b}).map(function(k){return flagPages[k]});
var nPages=records.length,nFlagPages=fpList.length;
var flaggedParas=paras.filter(function(p){return p.flagged});
var totalSus=0;paras.forEach(function(p){totalSus+=p.susCount});
var susParas=paras.filter(function(p){return p.susCount>0});

/* ---------- exports ---------- */
function limitations(p){return p.flagged?'footnotes not separated; '+(p.susCount||'some')+(p.susCount?' line'+(p.susCount>1?'s':'')+' may sit inside this paragraph':' text may sit inside this paragraph (paragraph over 300 words)'):'footnotes not separated'}
var exportRecords=paras.map(function(p){return {symbol:symbol,paragraph:p.n,section:p.section,part:p.part,page_start:p.page_start,page_end:p.page_end,text:p.text,text_lines:p.text_lines,flagged:p.flagged,first_words_match:p.fwMatch,citation:p.citation,doc_url:D.doc_url||'',limitations:limitations(p)}});
var jsonStr=JSON.stringify(exportRecords,null,2);
function mdStr(){
  var today=new Date().toISOString().slice(0,10);
  var o=['---','title: '+JSON.stringify(D.title||''),'symbol: '+symbol,'adopted: '+JSON.stringify(ref.adopted||'not stated'),'source_url: '+(D.doc_url||''),'extracted: '+today,'paragraphs_found: '+paras.length,'paragraphs_expected: '+(refP!==null?refP:'unknown'),'pages_flagged: '+nFlagPages,'footnotes: '+JSON.stringify('not separated; the document has '+(refFN!==null?refFN:'an unknown number of them')),'---',''];
  items.forEach(function(it){
    if(it.type==='h'){o.push((it.h.level===1?'## ':'### ')+it.h.full,'')}
    else o.push('**'+it.p.n+'.** '+it.p.text+(it.p.flagged?' (flagged: may contain footnote text)':''),'');
  });
  return o.join('\n');
}
function fname(ext){return (symbol||'document').replace(/\//g,'-')+'.'+ext}
function download(name,content,type){
  var b=new Blob([content],{type:type+';charset=utf-8'});var u=URL.createObjectURL(b);
  var a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();
  setTimeout(function(){URL.revokeObjectURL(u);a.remove()},500);
}

/* ---------- checks ---------- */
var checks=[];
var nums=paras.map(function(p){return p.n});
var numIssues=[],prev=0;
paras.forEach(function(p){
  if(p.n===prev+1){}
  else if(p.n>prev+1)numIssues.push('gap: after '+prev+' comes '+p.n+' (page '+p.page_start+')');
  else numIssues.push('duplicate or out of order: '+p.n+' after '+prev+' (page '+p.page_start+')');
  prev=Math.max(prev,p.n);
  if(p.n===prev&&false){}
});
(function(){
  var f=paras.length;
  checks.push(refP===null?{t:'Paragraph count',s:'notrun',d:'No reference paragraph count in this file: not run.'}:
    {t:'Paragraph count',s:f===refP?'pass':'fail',d:'Given the converter\'s text of '+nPages+' pages, having counted each line that starts a numbered paragraph, we expect '+refP+'; found '+f+'.',rows:f!==refP?[]:null});
  checks.push({t:'Numbering',s:numIssues.length?'fail':'pass',d:'We expect the numbers 1 to '+(paras.length?Math.max.apply(null,nums):0)+' once each, in order; '+(numIssues.length?numIssues.join('; '):'no gaps, no duplicates')+'.'});
  if(!refFW)checks.push({t:'First words',s:'notrun',d:'No first words in the reference: not run.'});
  else{
    var bad=[];Object.keys(refFW).forEach(function(k){var p=paras.filter(function(x){return x.n===+k})[0];if(!p||p.fwMatch!==true)bad.push(+k)});
    checks.push({t:'First words',s:bad.length?'fail':'pass',d:'We expect the first six words of every paragraph to equal the reference; '+bad.length+' of '+Object.keys(refFW).length+' differ'+(bad.length?' (para. '+bad.slice(0,15).join(', ')+(bad.length>15?', …':'')+')':'')+'.',rows:bad});
  }
  checks.push({t:'Pages flagged',s:'info',d:nFlagPages+' pages flagged, '+flaggedParas.length+' paragraphs to check against the PDF. A flag is not a failure.',rows:flaggedParas.map(function(p){return p.n})});
  checks.push({t:'Suspect lines',s:'info',d:totalSus+' suspect lines on '+nFlagPages+' pages, in '+susParas.length+' paragraphs; none is removed.'});
  checks.push({t:'Headers',s:headerOk===nPages?'pass':'fail',d:'We expect the symbol as first line of every page; found on '+headerOk+' of '+nPages+' pages.'});
  checks.push({t:'Footers',s:pagesWithNum===nPages-1?'pass':'fail',d:'We expect a page number in the footer on all pages but the first; found on '+pagesWithNum+' of '+nPages+' pages. Bare numbers removed from the footer (displaced footnote numbers, not put back): '+(footerNums.length?footerNums.map(function(x){return x.num+' (page '+x.page+')'}).join(', '):'none')+'.'});
  var lab=heads.filter(function(h){return h.kind==='labelled'}),un=heads.filter(function(h){return h.kind==='unlabelled'});
  checks.push({t:'Headings',s:'info',d:lab.length+' labelled and '+un.length+' unlabelled headings. Unlabelled: '+(un.length?un.map(function(h){return '“'+h.text+'” (p. '+h.page+')'}).join('; '):'none')+'. Look for a paragraph\'s last line mistaken for a heading.'});
  var cnt={cover:0,header:0,heading:0,para:0,footer:0},unc=[];
  allLines.forEach(function(l){if(cnt[l.kind]!==undefined)cnt[l.kind]++;else unc.push(l)});
  var sum=cnt.cover+cnt.header+cnt.heading+cnt.para+cnt.footer;
  checks.push({t:'Nothing lost',s:(sum===totalNonEmpty&&!unc.length)?'pass':'fail',d:'Every non-empty line is classified once: cover '+cnt.cover+' + header '+cnt.header+' + heading '+cnt.heading+' + paragraph '+cnt.para+' + footer '+cnt.footer+' = '+sum+' of '+totalNonEmpty+' lines.'+(unc.length?' Unclassified: '+unc.map(function(l){return '“'+esc(l.tr)+'” (page '+l.page+')'}).join('; '):'')});
  checks.push({t:'Hyphenated line ends',s:'info',d:hyph+' lines end with a hyphen; no hyphen joining is done.'});
  var rt=-1;try{rt=JSON.parse(jsonStr).length}catch(e){}
  checks.push({t:'Export round trip',s:rt===paras.length?'pass':'fail',d:'The JSON to download is parsed back: '+rt+' records, the table has '+paras.length+'.'});
})();
var failed=checks.filter(function(c){return c.s==='fail'}).length;
var passed=checks.filter(function(c){return c.s==='pass'}).length;
var mTot=checks.filter(function(c){return c.s!=='info'}).length;

/* ---------- render ---------- */
var found=paras.length;
var fwMatches=0;
if(refFW)Object.keys(refFW).forEach(function(k){var p=paras.filter(function(x){return x.n===+k})[0];if(p&&p.fwMatch===true)fwMatches++});
var fwTotal=refP!==null?refP:(refFW?Object.keys(refFW).length:null);

$('top').innerHTML='<div><div class="mono">UN DOCUMENT · PDF TEXT</div><h1>'+esc(D.title||symbol)+'</h1><div class="meta">'+
 (D.doc_url?'<a href="'+esc(D.doc_url)+'" target="_blank" rel="noopener">'+esc(symbol)+'</a>':esc(symbol))+' · adopted '+esc(ref.adopted||'not stated')+' · '+nPages+' pages · '+esc(D.source||'source not stated')+'</div></div>'+
 '<div class="status"><div><span class="dot'+(failed?' red':'')+'"></span>'+(failed?'<b class="red">'+failed+' check'+(failed>1?'s':'')+' failed</b>':passed+' of '+mTot+' checks pass')+'</div><div class="'+(nFlagPages?'red':'')+'">'+nFlagPages+' pages flagged</div></div>';

var short=(found===refP);
$('rail').innerHTML='<div class="mono">DOCUMENT</div><div class="card"><b>'+esc(symbol)+'</b>'+esc(D.title||'')+'</div>'+
 '<div class="big '+(refP!==null&&!short?'red':'')+'">'+found+'</div><div>paragraphs of '+(refP!==null?refP:'? (no reference)')+'</div>'+
 '<div class="bar"><i class="'+(refP!==null&&!short?'r':'')+'" style="width:'+(refP?Math.min(100,found/refP*100):0)+'%"></i></div>'+
 '<div class="big '+(nFlagPages?'red':'')+'">'+nFlagPages+'</div><div>of '+nPages+' pages flagged</div><div class="hint">footnote text may sit inside a paragraph</div>'+
 '<div class="bar"></div><div class="hint">'+passed+' of '+mTot+' checks pass</div>';

/* tab 01 */
function acc(id,title,html){return '<button class="acc" data-acc="'+id+'" aria-expanded="false" aria-controls="'+id+'"><span class="mono">'+title+'</span></button><div class="accbody" id="'+id+'" hidden>'+html+'</div>'}
var t1='<h2 class="q">Did the app find everything the document has?</h2>';
if(!found)t1+='<div class="warn"><b class="red">No numbered paragraph was found</b> in the text of this file. The exports are disabled.</div>';
var diff=refP===null?'':(found===refP?'':' ('+Math.abs(found-refP)+(found<refP?' short':' over')+')');
t1+='<div class="tiles">'+
 '<div class="tile"><div class="mono">PARAGRAPHS FOUND</div><div class="big">'+found+'</div><p class="'+(refP===null?'':(found===refP?'green':'red'))+'">'+(refP===null?'no reference in this file':'the document has '+refP+(diff?diff:' · equal'))+'</p><div class="how">How this is computed: each line that is a number and a full stop starts a paragraph.</div></div>'+
 '<div class="tile"><div class="mono">FIRST WORDS MATCH</div><div class="big">'+(fwTotal===null?'–':fwMatches)+'</div><p class="'+(fwTotal===null?'':(fwMatches===fwTotal?'green':'red'))+'">'+(fwTotal===null?'no reference in this file':'of '+fwTotal)+'</p><div class="how">How this is computed: first six words, footnote marks removed, quotes and dashes made equal, compared with the reference.</div></div>'+
 '<div class="tile"><div class="mono">PAGES FLAGGED</div><div class="big '+(nFlagPages?'red':'')+'">'+nFlagPages+'</div><p>of '+nPages+' pages. Footnote text may sit inside a paragraph: check these paragraphs against the PDF.</p><div class="how">How this is computed: a line inside a paragraph that looks like a footnote starts a suspect block that runs to the foot of the page.</div></div>'+
 '<div class="tile"><div class="mono">FOOTNOTES</div><div class="big" style="font-size:34px;padding-top:10px">not separated</div><p>the document has '+(refFN!==null?refFN:'an unknown number (no reference)')+'; this version leaves them in place and flags them.</p><div class="how">How this is computed: not computed; the reference count is shown for comparison.</div></div></div>';
if(refFW){
  var ml=[];Object.keys(refFW).map(Number).sort(function(a,b){return a-b}).forEach(function(k){
    var p=paras.filter(function(x){return x.n===k})[0];
    if(!p)ml.push('para. '+k+': not found / reference “'+esc(refFW[k])+'”');
    else if(p.fwMatch!==true)ml.push('para. '+k+': found “'+esc(p.found6)+'” / reference “'+esc(refFW[k])+'”');
  });
  if(ml.length){t1+='<ul class="list">'+ml.slice(0,10).map(function(x){return '<li class="red">'+x+'</li>'}).join('')+(ml.length>10?'<li>and '+(ml.length-10)+' more</li>':'')+'</ul>'}
}
t1+='<h3 class="s">Take the paragraphs away</h3><div><button class="btn" id="dlj"'+(found?'':' disabled')+'>Download JSON</button><button class="btn" id="dlm"'+(found?'':' disabled')+'>Download Markdown</button></div><div class="how">JSON: one record per paragraph with symbol, number, section, pages, text, flags, citation and limitations. Markdown: front matter, headings and paragraphs in order.</div>';
var ck='<ul class="chk">'+checks.map(function(c){
  var w=c.s==='pass'?'<span class="pass">pass</span>':c.s==='fail'?'<span class="fail">check failed</span>':c.s==='notrun'?'<span class="note">not run</span>':'<span class="note">note</span>';
  var rows=(c.rows&&c.rows.length)?' <button class="link" data-goto="'+c.rows[0]+'">see rows (para. '+c.rows[0]+(c.rows.length>1?' and '+(c.rows.length-1)+' more':'')+')</button>':'';
  return '<li><b>'+esc(c.t)+'</b> · '+w+'<br>'+(c.t==='Nothing lost'?c.d:esc(c.d))+rows+'</li>';
}).join('')+'</ul>';
t1+=acc('a-checks','EVERY CHECK ('+checks.length+')',ck);
var fpTable='<div class="warn">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</div>';
if(!fpList.length)fpTable+='<p>No page has a suspect line.</p>';
else fpTable+='<table><caption><span class="mono">TAB.01</span>'+nFlagPages+' flagged pages, '+totalSus+' suspect lines</caption><thead><tr><th scope="col" class="num">Page</th><th scope="col">Paragraph</th><th scope="col" class="num">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>'+
 fpList.map(function(f){
  var why=f.reasons.slice();
  f.paras.forEach(function(n){var p=paras.filter(function(x){return x.n===n})[0];if(p&&p.long&&why.indexOf('paragraph over 300 words')<0)why.push('paragraph over 300 words')});
  return '<tr class="row" data-fp="'+f.page+'"><td class="num"><button class="rowbtn" aria-expanded="false" data-fpb="'+f.page+'">'+f.page+'</button></td><td>'+f.paras.join(', ')+'</td><td class="num">'+f.count+'</td><td>'+esc(why.join('; '))+'</td></tr><tr hidden id="fpd-'+f.page+'"><td colspan="4"></td></tr>';
 }).join('')+'</tbody></table>';
t1+=acc('a-flag','FLAGGED PAGES ('+nFlagPages+')',fpTable);
$('p1').innerHTML=t1;

/* tab 02 */
var t2='<h2 class="q">What does each paragraph say, and how do I cite it?</h2>';
var hlist='<ul class="list">'+heads.map(function(h){return '<li>'+(h.level===1?'':h.level===2?'&nbsp;&nbsp;':'&nbsp;&nbsp;&nbsp;&nbsp;')+esc(h.full)+' <span class="dim">· p. '+h.page+(h.kind==='unlabelled'?' · unlabelled':'')+'</span></li>'}).join('')+'</ul>';
t2+=acc('a-heads','HEADINGS FOUND: '+heads.length,hlist);
function pageRange(p){return p.page_start===p.page_end?String(p.page_start):p.page_start+'–'+p.page_end}
function firstLine(t){if(t.length<=120)return t;var c=t.slice(0,120),sp=c.lastIndexOf(' ');return c.slice(0,sp>60?sp:120)+'…'}
if(!found)t2+='<p>No paragraph was found.</p>';
else t2+='<table><caption><span class="mono">TAB.02</span>'+found+' paragraphs found'+(refP!==null?', '+refP+' expected':', no reference count')+'</caption><thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody>'+
 paras.map(function(p){
  var ck=[];if(p.fwMatch===false)ck.push('<span class="fail">first words differ</span>');if(p.flagged)ck.push('<span class="fail">may contain footnote text</span>');
  var cs=ck.length?ck.join('; '):(p.fwMatch===true?'<span class="pass">OK</span>':'<span class="note">first words not checked</span>');
  return '<tr class="row" data-p="'+p.idx+'"><td class="num"><button class="rowbtn" aria-expanded="false" data-pb="'+p.idx+'" aria-controls="pd-'+p.idx+'">'+p.n+'</button></td><td>'+esc(p.section)+'</td><td>'+pageRange(p)+'</td><td>'+esc(firstLine(p.text))+'</td><td>'+cs+'</td></tr><tr hidden id="pd-'+p.idx+'"><td colspan="5"></td></tr>';
 }).join('')+'</tbody></table>';
$('p2').innerHTML=t2;
$('foot').innerHTML=esc(D.source||'')+' · built '+esc(D.built||'not stated')+'<br>Done by this page\'s code; no model was called and nothing left the browser.';

/* detail renderers */
function paraDetail(p){
  var spans=p.lines.map(function(l){return l.sus?'<span class="sus">'+esc(l.text.trim())+'</span>':esc(l.text.trim())}).join(' ');
  var pre=[],lastPage=null;
  p.objs.forEach(function(o){if(o.page!==lastPage){pre.push('<span class="pg">[page '+o.page+' begins]</span>');lastPage=o.page}pre.push(o.sus?'<span class="sus">'+esc(o.tr)+'</span>':esc(o.tr))});
  return '<div class="detail"><div class="hint">PATH</div><div>'+esc(p.path||p.section||'(no heading)')+'</div>'+
   '<div class="cols"><div><span class="hint">REFERENCE, FIRST SIX WORDS</span><br>'+(p.ref6!==null?esc(p.ref6):'<i>none in this file</i>')+'</div><div><span class="hint">FOUND, FIRST SIX WORDS</span><br>'+esc(p.found6)+'</div></div>'+
   (p.flagged?'<div class="warn">'+(p.susCount?p.susCount+' suspect line'+(p.susCount>1?'s':'')+' (thin red box) may be footnote text. ':'')+(p.long?'The paragraph has '+p.words+' words. ':'')+'Check against the PDF.</div>':'')+
   '<p class="ptext">'+spans+'</p>'+
   '<button class="link" data-showlines="'+p.idx+'" aria-expanded="false">Show the PDF\'s lines</button><pre class="lines" id="pl-'+p.idx+'" hidden>'+pre.join('\n')+'</pre>'+
   '<div><button class="btn" data-copy="'+p.idx+'">Copy citation</button><span class="hint" role="status" id="cp-'+p.idx+'"></span></div></div>';
}
function pageDetail(pg){
  var L=pageStore[pg]||[];
  var out=L.filter(function(l){return l.kind!=='empty'}).map(function(l){
    var c=l.sus?'sus':(l.kind==='footer'||l.kind==='header'?'dim':'');
    return '<span class="'+c+'">'+esc(l.tr)+'</span>';
  }).join('\n');
  var f=flagPages[pg];
  return '<div class="detail"><div class="hint">RAW LINES OF PAGE '+pg+' (suspect lines boxed, header and footer greyed)</div><pre class="lines">'+out+'</pre>'+
   f.paras.map(function(n){var p=paras.filter(function(x){return x.n===n})[0];return p?'<div>Sits in paragraph '+n+': “'+esc(firstLine(p.text))+'” <button class="link" data-goto="'+p.n+'">open paragraph '+n+'</button></div>':''}).join('')+'</div>';
}

/* events */
document.addEventListener('click',function(e){
  var el=e.target.closest('button,tr.row');if(!el)return;
  if(el.dataset.acc){var open=el.getAttribute('aria-expanded')==='true';el.setAttribute('aria-expanded',String(!open));$(el.dataset.acc).hidden=open;return}
  if(el.id==='dlj'){download(fname('json'),jsonStr,'application/json');return}
  if(el.id==='dlm'){download(fname('md'),mdStr(),'text/markdown');return}
  if(el.dataset.goto){goPara(+el.dataset.goto);return}
  if(el.dataset.showlines){var pre=$('pl-'+el.dataset.showlines),o=el.getAttribute('aria-expanded')==='true';el.setAttribute('aria-expanded',String(!o));pre.hidden=o;el.textContent=o?"Show the PDF's lines":"Hide the PDF's lines";return}
  if(el.dataset.copy){var p=paras[+el.dataset.copy];copyText(p.citation);var s=$('cp-'+p.idx);s.textContent=' Copied';setTimeout(function(){s.textContent=''},2000);return}
  var b=null;
  if(el.tagName==='TR'){b=el.querySelector('button.rowbtn')}else if(el.classList.contains('rowbtn'))b=el;
  if(!b)return;
  if(b.dataset.pb!==undefined)togglePara(+b.dataset.pb,null);
  else if(b.dataset.fpb!==undefined)toggleFp(+b.dataset.fpb);
});
function togglePara(i,forceOpen){
  var b=document.querySelector('button[data-pb="'+i+'"]'),r=$('pd-'+i);if(!b)return;
  var open=forceOpen===null?b.getAttribute('aria-expanded')!=='true':forceOpen;
  b.setAttribute('aria-expanded',String(open));r.hidden=!open;
  if(open&&!r.firstChild.innerHTML)r.firstChild.innerHTML=paraDetail(paras[i]);
}
function toggleFp(pg){
  var b=document.querySelector('button[data-fpb="'+pg+'"]'),r=$('fpd-'+pg);
  var open=b.getAttribute('aria-expanded')!=='true';
  b.setAttribute('aria-expanded',String(open));r.hidden=!open;
  if(open&&!r.firstChild.innerHTML)r.firstChild.innerHTML=pageDetail(pg);
}
function copyText(s){
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(s).catch(function(){fb(s)})}else fb(s);
  function fb(x){var t=document.createElement('textarea');t.value=x;document.body.appendChild(t);t.select();try{document.execCommand('copy')}catch(e){}t.remove()}
}
function goPara(n){
  var p=paras.filter(function(x){return x.n===n})[0];if(!p)return;
  selectTab(1);togglePara(p.idx,true);
  var b=document.querySelector('button[data-pb="'+p.idx+'"]');if(b){b.scrollIntoView({block:'center'});b.focus()}
}
/* tabs */
var tabs=[$('t1'),$('t2')],panels=[$('p1'),$('p2')];
function selectTab(i,focus){
  tabs.forEach(function(t,k){t.setAttribute('aria-selected',String(k===i));t.tabIndex=k===i?0:-1;panels[k].hidden=k!==i});
  if(focus)tabs[i].focus();
}
tabs.forEach(function(t,i){
  t.addEventListener('click',function(){selectTab(i)});
  t.addEventListener('keydown',function(e){
    var k=null;
    if(e.key==='ArrowRight')k=(i+1)%tabs.length;else if(e.key==='ArrowLeft')k=(i+tabs.length-1)%tabs.length;else if(e.key==='Home')k=0;else if(e.key==='End')k=tabs.length-1;
    if(k!==null){e.preventDefault();selectTab(k,true)}
  });
});
})();
</script>
</body>
</html>
```