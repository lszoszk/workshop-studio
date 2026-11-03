I built a reader for the attached General comment: it splits the converter's raw text into numbered paragraphs, compares the result with the document's own reference and lists every repair it made. It has five numbered tabs (result, paragraphs, footnotes, checks, method and export). Nothing is typed in by hand and nothing leaves the browser.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--accent:#9b2335;--muted:#5a554b;--ok:#1d6b34;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;--sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 var(--sans)}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.mono{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
header.top{padding:22px 0 10px}
h1{font:400 34px/1.15 var(--serif);margin:6px 0 8px}
.meta{margin:0 0 6px}
.meta a{color:var(--accent);font-weight:600}
.what{margin:0;color:var(--muted);max-width:760px}
[role=tablist]{display:flex;flex-wrap:wrap;gap:0 4px;border-bottom:1px solid var(--rule);margin-top:14px}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;padding:10px 12px 8px;cursor:pointer;color:var(--ink);font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase}
[role=tab] .tn{color:var(--muted);margin-right:4px}
[role=tab][aria-selected=true]{color:var(--accent);border-bottom-color:var(--accent);font-weight:700}
[role=tab][aria-selected=true] .tn{color:var(--accent)}
[role=tabpanel]{padding:20px 0 30px}
h2.q{font:400 24px/1.25 var(--serif);margin:0 0 16px}
h2.q .mono{display:block;color:var(--muted);margin-bottom:2px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:0}
.tile{border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:14px 16px 12px 0;margin-right:16px}
.tile .lab{color:var(--muted)}
.pair{display:flex;gap:22px;align-items:baseline;flex-wrap:wrap}
.big{font:400 52px/1.1 var(--serif)}
.big small{display:block;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.ok{color:var(--ok)}.bad{color:var(--accent)}.mut{color:var(--muted)}
.sub{font-weight:600;min-height:1.5em}
.how{margin:8px 0 0;font-size:14px;color:var(--muted)}
.how .mono{display:block;font-size:11px}
.lnk{background:none;border:0;padding:0;color:var(--accent);text-decoration:underline;cursor:pointer;font:inherit}
.checkline{margin:18px 0 6px;font-size:18px}
.gloss{max-width:760px;color:var(--muted);font-size:15px;margin-top:14px}
table{width:100%;border-collapse:collapse}
caption{text-align:left;padding:4px 0 10px;font:400 20px/1.3 var(--serif)}
caption .mono{display:block;color:var(--muted)}
th{font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:2px solid var(--ink);padding:6px 8px;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:7px 8px;vertical-align:top;overflow-wrap:anywhere}
th.r,td.r{text-align:right}
.c-no{width:70px}.c-sec{width:20%}.c-pg{width:70px}.c-ck{width:150px}
tr.prow{cursor:pointer}
tr.prow:hover td{background:#ece6d8}
tr.flag td:first-child{box-shadow:inset 3px 0 0 var(--accent)}
tr.hit td{background:#f3dfe2}
.rowbtn{background:none;border:0;font:700 16px var(--serif);color:var(--accent);cursor:pointer;padding:2px 4px}
.rowbtn::after{content:" +";font:12px var(--mono);color:var(--muted)}
.rowbtn[aria-expanded=true]::after{content:" \2212"}
.drow>td{background:#fbf9f4;padding:14px 16px 18px}
.ptext{font:18px/1.55 var(--serif);max-width:860px;margin:6px 0 10px}
.path{color:var(--muted)}
.tog,.copy,.dl{font:inherit;background:none;border:1px solid var(--ink);padding:6px 12px;cursor:pointer;color:var(--ink)}
.dl{border-color:var(--accent);color:var(--accent);font-weight:600}
.copy[disabled]{opacity:.7}
pre.lines{font:13px/1.5 var(--mono);white-space:pre-wrap;background:#eee9dc;padding:10px;margin:8px 0;overflow-wrap:anywhere}
.blk{margin:12px 0 0}
.blk .mono{color:var(--muted);display:block}
ul.plain,ol.plain{margin:4px 0;padding-left:20px}
.hbox{border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-bottom:16px}
.hbox>button,.logh{width:100%;text-align:left;background:none;border:0;padding:10px 0;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;cursor:pointer;color:var(--ink)}
.hbox>button::after,.logh::after{content:" +"}
.hbox>button[aria-expanded=true]::after,.logh[aria-expanded=true]::after{content:" \2212"}
.hbox ol{margin:0 0 10px;padding-left:28px;columns:2}
.note{font-size:14px;color:var(--muted);max-width:820px}
code{font:13px var(--mono);background:#e9e3d4;padding:1px 4px}
ol.checks{list-style:none;margin:0;padding:0}
li.chk{border-bottom:1px solid var(--rule);padding:10px 0}
.chk-line{display:flex;flex-wrap:wrap;gap:4px 14px;align-items:baseline}
.chk-line strong{min-width:150px}
.chk-line .vals{flex:1;min-width:200px}
.st-pass{color:var(--ok);font-weight:700}.st-fail{color:var(--accent);font-weight:700}.st-notrun{color:var(--muted);font-weight:700}
.story{margin:2px 0 0;font-size:14px;color:var(--muted)}
.det{margin:4px 0 0;font-size:14px}
.det ul{margin:2px 0;padding-left:20px}
.ctx{font:13px var(--mono);color:var(--muted)}
.kinds{display:flex;flex-wrap:wrap;gap:4px 18px;margin:8px 0 12px;padding:0;list-style:none;font-size:14px}
.kinds b{font-family:var(--serif);font-size:18px}
td.ba{font:12px/1.4 var(--mono)}
.raw{border:1px solid var(--rule);margin-top:8px}
.rl{display:grid;grid-template-columns:3.4em 1.8em 1fr;font:13px/1.5 var(--mono);white-space:pre-wrap;overflow-wrap:anywhere}
.rl .ln{color:var(--muted);text-align:right;padding-right:8px}
.rl .cd{font-weight:700;text-align:center}
.c-C{background:#e6e1f0}.c-H{background:#dde9f2}.c-S{background:#f4e8bf}.c-P{background:#e3eedb}.c-N{background:#f6e0d0}.c-F{background:#e2e1dc}.c-blank{color:#a09a8c}
.c-X{background:#f4c4cb;color:#7a1626;font-weight:700}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;margin:8px 0;font:12px var(--mono)}
.legend span{padding:2px 8px}
select{font:inherit;padding:6px 8px;background:#fff;border:1px solid var(--ink);color:var(--ink)}
footer{border-top:1px solid var(--rule);padding:14px 0 30px;color:var(--muted);font-size:14px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
@media (max-width:700px){h1{font-size:26px}.big{font-size:42px}.hbox ol{columns:1}}
</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <div class="mono" style="color:var(--muted)">UN DOCUMENT &middot; PDF TEXT</div>
  <h1 id="title">Loading&hellip;</h1>
  <p class="meta" id="meta"></p>
  <p class="what">This page splits the converter's raw text into numbered paragraphs, removes the headers, footers and footnotes, checks itself against the document's own figures, and lists every repair it made.</p>
</header>
<div role="tablist" aria-label="Views" id="tablist">
  <button role="tab" id="t0" aria-controls="p0" aria-selected="true" tabindex="0"><span class="tn">01</span>RESULT</button>
  <button role="tab" id="t1" aria-controls="p1" aria-selected="false" tabindex="-1"><span class="tn">02</span>PARAGRAPHS</button>
  <button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1"><span class="tn">03</span>FOOTNOTES</button>
  <button role="tab" id="t3" aria-controls="p3" aria-selected="false" tabindex="-1"><span class="tn">04</span>CHECKS</button>
  <button role="tab" id="t4" aria-controls="p4" aria-selected="false" tabindex="-1"><span class="tn">05</span>METHOD AND EXPORT</button>
</div>
<main>
  <section id="p0" role="tabpanel" aria-labelledby="t0" tabindex="0">
    <h2 class="q"><span class="mono">01 RESULT</span>Did the app find everything the document has?</h2>
    <div id="r0"></div>
  </section>
  <section id="p1" role="tabpanel" aria-labelledby="t1" hidden>
    <h2 class="q"><span class="mono">02 PARAGRAPHS</span>What does each paragraph say, and how do I cite it?</h2>
    <div id="r1"></div>
  </section>
  <section id="p2" role="tabpanel" aria-labelledby="t2" hidden>
    <h2 class="q"><span class="mono">03 FOOTNOTES</span>What do the footnotes say?</h2>
    <div id="r2"></div>
  </section>
  <section id="p3" role="tabpanel" aria-labelledby="t3" hidden>
    <h2 class="q"><span class="mono">04 CHECKS</span>Can I trust this?</h2>
    <div id="r3"></div>
  </section>
  <section id="p4" role="tabpanel" aria-labelledby="t4" hidden>
    <h2 class="q"><span class="mono">05 METHOD AND EXPORT</span>How was it done, and can I take it away?</h2>
    <div id="r4"></div>
  </section>
</main>
<footer id="foot"></footer>
</div>
<script>
(function(){
'use strict';
var WD=window.WORKSHOP_DATA||{},D=WD.pdf_text;
function $(id){return document.getElementById(id);}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function cut(s,n){s=String(s||'');if(s.length<=n)return s;var c=s.slice(0,n),k=c.lastIndexOf(' ');if(k>n*0.5)c=c.slice(0,k);return c.replace(/[\s,;:]+$/,'')+'…';}
function tail(s,n){s=String(s||'');return s.length>n?'…'+s.slice(s.length-n):s;}
function norm(s){return String(s||'').replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();}
function num(n){return n==null?'–':String(n);}
function plural(n,w){return n+' '+w+(n===1?'':'s');}

var tabs=[].slice.call(document.querySelectorAll('[role=tab]')),panels=[0,1,2,3,4].map(function(i){return $('p'+i);}),curTab=0;
function selectTab(i,focus){
  curTab=i;
  tabs.forEach(function(t,k){var on=k===i;t.setAttribute('aria-selected',on?'true':'false');t.tabIndex=on?0:-1;panels[k].hidden=!on;if(on)panels[k].setAttribute('tabindex','0');else panels[k].removeAttribute('tabindex');});
  if(focus)tabs[i].focus();
}
tabs.forEach(function(t,i){t.addEventListener('click',function(){selectTab(i);});});
$('tablist').addEventListener('keydown',function(e){
  var k=e.key,i=curTab,n=tabs.length;
  if(k==='ArrowRight')i=(i+1)%n;else if(k==='ArrowLeft')i=(i-1+n)%n;else if(k==='Home')i=0;else if(k==='End')i=n-1;else return;
  e.preventDefault();selectTab(i,true);
});

if(!D||!Array.isArray(D.records)||!D.records.length){
  $('title').textContent='No PDF text was attached';
  $('r0').innerHTML='<p>This page needs the raw text of one PDF. Drag the file from "Your files" into the chat and ask again.</p>';
  return;
}
var M;

/* ---------- the pipeline ---------- */
function build(){
  var recs=D.records.slice().sort(function(a,b){return (a.page||0)-(b.page||0);});
  var ref=(D.reference&&typeof D.reference==='object')?D.reference:null;
  function rn(k){return ref&&typeof ref[k]==='number'?ref[k]:null;}
  var refPar=rn('paragraphs'),refFn=rn('footnotes');
  var refFW=(ref&&ref.first_words&&typeof ref.first_words==='object')?ref.first_words:null;
  var symbol=D.symbol||'';
  var logArr=[],seq=0;
  function log(kind,page,where,before,after){var e={kind:kind,page:page,where:where||'–',before:before,after:after,seq:seq++};logArr.push(e);return e;}
  var pages=[],footnotes=[],B=[],nextFn=1,firstPage=recs[0].page;

  recs.forEach(function(r){
    var raw=String(r.text==null?'':r.text).replace(/\r\n?/g,'\n').split('\n');
    var L=raw.map(function(t,i){var s=t.trim();return {n:i+1,t:t,s:s,cls:s===''?'blank':null,page:r.page};});
    var P={page:r.page,lines:L,header:false,pageNo:false,displaced:[],block:false};
    pages.push(P);
    var first=-1,k;
    for(k=0;k<L.length;k++){if(L[k].s!==''){first=k;break;}}
    var start=0;
    if(first>=0&&L[first].s===symbol){L[first].cls='header';P.header=true;log('header line removed',r.page,'–',L[first].s,'(removed)');start=first+1;}
    /* footer: lines from the end */
    var end=L.length-1;
    while(end>=start){
      var s=L[end].s;
      if(s===''){end--;continue;}
      var isF=false;
      if(/^GE\./.test(s)||/^\d{6}(\s+\d{6})*$/.test(s))isF=true;
      else if(/^\d{1,3}$/.test(s)){isF=true;var nn=+s;if(nn===r.page&&!P.pageNo)P.pageNo=true;else P.displaced.push(nn);}
      if(!isF)break;
      L[end].cls='footer';log('footer line removed',r.page,'–',s,'(removed)');end--;
    }
    /* footnote block */
    function isOpen(x,n){return x===String(n)||x.indexOf(n+' ')===0;}
    function findFrom(n){for(var q=start;q<=end;q++){var x=L[q].s;if(x==='')continue;if(isOpen(x,n)||(r.page===firstPage&&x.indexOf('* ')===0))return q;}return -1;}
    var bs=findFrom(nextFn),cand=nextFn,g=0;
    while(bs<0&&P.displaced.indexOf(cand)>=0&&g++<6){
      cand++;var q2=findFrom(cand);
      if(q2>=0){var b0=q2;while(b0-1>=start&&L[b0-1].s!=='')b0--;bs=b0;}
    }
    var maxD=P.displaced.length?Math.max.apply(null,P.displaced):0;
    if(bs>=0){
      P.block=true;
      var pf=[],cur=null,exp=nextFn,afterBlank=false;
      var newFn=function(no,lines){var f={no:no,page:r.page,lines:lines,repaired:false};footnotes.push(f);pf.push(f);return f;};
      for(var q=bs;q<=end;q++){
        var l=L[q],x=l.s,mm;
        l.cls='footnote';
        if(x===''){if(cur&&cur.lines.length)afterBlank=true;continue;}
        if(r.page===firstPage&&x.indexOf('* ')===0&&pf.length===0){cur=newFn('*',[x.slice(2)]);afterBlank=false;}
        else if(/^\d{1,3}$/.test(x)&&+x===exp){cur=newFn(exp,[]);exp++;afterBlank=false;}
        else if((mm=/^(\d{1,3}) (.+)$/.exec(x))&&+mm[1]===exp){cur=newFn(exp,[mm[2]]);exp++;afterBlank=false;}
        else{
          if(cur&&(cur.lines.length===0||!afterBlank))cur.lines.push(x);
          else if(P.displaced.indexOf(exp)>=0){
            cur=newFn(exp,[x]);cur.repaired=true;
            log('footnote number restored',r.page,'fn '+exp,'(no number) '+cut(x,60),String(exp)+' (from the bare number at the page foot)').fn=exp;
            exp++;
          }
          else if(cur)cur.lines.push(x);
          else cur=newFn(null,[x]);
          afterBlank=false;
        }
      }
      var cnt=0;pf.forEach(function(f){if(typeof f.no==='number')cnt++;});
      log('footnote block removed',r.page,'–',cut(L[bs].s,60)+' ('+plural(end-bs+1,'line')+')',plural(cnt,'footnote')+' kept in the footnote list');
      nextFn=Math.max(exp,maxD+1);
    }else if(maxD)nextFn=Math.max(nextFn,maxD+1);
    /* body lines of this page */
    var a=start,z=(bs>=0?bs:end+1)-1;
    while(a<=z&&L[a].s==='')a++;
    while(z>=a&&L[z].s==='')z--;
    for(var q3=a;q3<=z;q3++)B.push({t:L[q3].s,page:r.page,ref:L[q3]});
  });
  footnotes.forEach(function(f){f.text=f.lines.join(' ').replace(/\s+/g,' ').trim();});

  /* paragraphs and headings */
  var paras=[],headings=[],pending=[],chain={roman:null,letter:null,unl:null},lastH=null,lastRoman=0,curP=null;
  function isPS(s){return /^\d{1,3}\.$/.test(s)||/^\d{1,3}\. .+$/.test(s);}
  function romanVal(s){var v={I:1,V:5,X:10},t=0;for(var i=0;i<s.length;i++){var c=v[s[i]],n=v[s[i+1]]||0;t+=c<n?-c:c;}return t;}
  function addH(text,kind,page){var h={text:text,kind:kind,page:page};headings.push(h);lastH=text;return h;}
  for(var i=0;i<B.length;i++){
    var b=B[i],s=b.t;
    if(s==='')continue;
    var m1=/^(\d{1,3})\.$/.exec(s),m2=/^(\d{1,3})\. (.+)$/.exec(s);
    if(m1||m2){
      var pn=+(m1||m2)[1];
      curP={number:pn,lines:[],raw:[{t:s,page:b.page}],section:lastH,part:chain.roman,path:[chain.roman,chain.letter,chain.unl].filter(Boolean),repairs:[],page0:b.page};
      if(m2){
        curP.lines.push({t:m2[2],page:b.page});
        curP.repairs.push(log('number and text split',b.page,'para. '+pn,s.length>70?cut(s,70):s,'number "'+pn+'." and text "'+cut(m2[2],40)+'"'));
      }
      pending.forEach(function(e){e.where='para. '+pn;e.para=pn;curP.repairs.push(e);});
      pending=[];
      b.ref.cls='paragraph';
      paras.push(curP);
      continue;
    }
    var ml=/^([IVX]+|[A-Z])\.$/.exec(s);
    if(ml){
      var label=ml[1],isRoman=false;
      if(/^[IVX]+$/.test(label)){var rv=romanVal(label);if(rv===lastRoman+1){isRoman=true;lastRoman=rv;}}
      b.ref.cls='heading';
      var tl=[],j=i+1;
      for(;j<B.length;j++){
        var t=B[j].t;
        if(t==='')continue;
        if(/^([IVX]+|[A-Z])\.$/.test(t)||isPS(t))break;
        B[j].ref.cls='heading';
        if(tl.length&&/^[a-z(]/.test(t)){
          var last=tl[tl.length-1];
          pending.push(log('heading title joined from two lines',B[j].page,'',last.text+' | '+t,last.text+' '+t));
          last.text+=' '+t;
        }else tl.push({text:t,page:B[j].page});
      }
      i=j-1;
      var ft=tl.length?tl.shift():null;
      var htxt=label+'.'+(ft?' '+ft.text:'');
      addH(htxt,isRoman?'roman':'letter',b.page);
      if(isRoman){chain.roman=htxt;chain.letter=null;chain.unl=null;}else{chain.letter=htxt;chain.unl=null;}
      tl.forEach(function(x){addH(x.text,'further',x.page);chain.unl=x.text;});
      continue;
    }
    var nx=B[i+1];
    if(nx&&isPS(nx.t)&&s.length<=90&&/^[A-Z]/.test(s)&&!/[.;:,\d]$/.test(s)&&!/[.;:,][)\]"'”’]$/.test(s)){
      b.ref.cls='heading';
      addH(s,'unlabelled',b.page);chain.unl=s;
      var pl=curP&&curP.lines.length?curP.lines[curP.lines.length-1].t:'';
      pending.push(log('heading separated from paragraph text',b.page,'',(pl?tail(pl,40)+' ':'')+s,(pl?'paragraph ends "'+tail(pl,40)+'"; ':'')+'heading "'+s+'"'));
      continue;
    }
    if(curP){curP.lines.push({t:s,page:b.page});curP.raw.push({t:s,page:b.page});b.ref.cls='paragraph';}
    else b.ref.cls='cover';
  }

  /* paragraph fields */
  var mc=1,rejected=[],hyphen=0;
  B.forEach(function(x){if(/-$/.test(x.t))hyphen++;});
  paras.forEach(function(p,idx){
    p.idx=idx;
    p.textRaw=p.lines.map(function(l){return l.t;}).join(' ').replace(/\s+/g,' ').trim();
    p.textLines=p.lines.map(function(l){return l.t;}).join(' | ');
    p.pageStart=p.page0;
    p.pageEnd=p.raw.reduce(function(m,l){return Math.max(m,l.page);},p.page0);
    for(var k=1;k<p.raw.length;k++){
      if(p.raw[k].page!==p.raw[k-1].page){
        p.repairs.push(log('paragraph joined across a page break',p.raw[k-1].page,'para. '+p.number,'page '+p.raw[k-1].page+' ends "'+tail(p.raw[k-1].t,45)+'" / page '+p.raw[k].page+' begins "'+cut(p.raw[k].t,45)+'"','one paragraph, lines joined with a space'));
      }
    }
    /* footnote marks */
    var text=p.textRaw,out='',lastI=0,re=/\d+/g,m;
    p.marks=[];
    while((m=re.exec(text))){
      var d=m[0],ix=m.index,ex=ix+d.length;
      if(d.length>3)continue;
      var pc=text.charAt(ix-1),nc=text.charAt(ex);
      if(/[\/\-–—(]/.test(pc)||/[\/\-–—(]/.test(nc))continue;
      var guard=pc===' '&&/[A-Za-z]/.test(text.charAt(ix-2));
      if(+d===mc&&!guard){
        out+=text.slice(lastI,ix);
        if(pc===' ')out=out.replace(/ $/,'');
        out+='['+d+']';
        lastI=ex;p.marks.push(mc);mc++;
      }else rejected.push({n:d,para:p.number,ctx:text.slice(Math.max(0,ix-26),Math.min(text.length,ex+26)),guard:guard});
    }
    out+=text.slice(lastI);
    p.text=out;
    p.clean=out.replace(/\[\d+\]/g,'').replace(/\s+/g,' ').trim();
    p.fwFound=p.clean.split(/\s+/).slice(0,6).join(' ');
    p.fwRef=refFW&&refFW[String(p.number)]!=null?String(refFW[String(p.number)]):null;
    p.fwOk=p.fwRef==null?null:norm(p.fwRef)===norm(p.fwFound);
    p.citation=symbol+', para. '+p.number;
  });
  var marksFound=mc-1;
  var fnByNo={};
  footnotes.forEach(function(f){if(typeof f.no==='number'&&!fnByNo[f.no])fnByNo[f.no]=f;});
  paras.forEach(function(p){p.fns=p.marks.map(function(n){return fnByNo[n];}).filter(Boolean);});

  logArr.sort(function(a,b){return (a.page-b.page)||(a.seq-b.seq);});

  /* classification counts */
  var kinds={cover:'C',header:'H',heading:'S',paragraph:'P',footnote:'N',footer:'F'};
  var counts={cover:0,header:0,heading:0,paragraph:0,footnote:0,footer:0},unclassified=[],totalNE=0;
  recs.forEach(function(r,pi){
    String(r.text==null?'':r.text).replace(/\r\n?/g,'\n').split('\n').forEach(function(t){if(t.trim()!=='')totalNE++;});
  });
  pages.forEach(function(P){P.lines.forEach(function(l){
    if(l.cls==='blank')return;
    if(l.cls&&counts.hasOwnProperty(l.cls))counts[l.cls]++;else{l.cls=null;unclassified.push(l);}
  });});

  return {recs:recs,ref:ref,refPar:refPar,refFn:refFn,refFW:refFW,symbol:symbol,log:logArr,pages:pages,footnotes:footnotes,paras:paras,headings:headings,marksFound:marksFound,rejected:rejected,hyphen:hyphen,counts:counts,kinds:kinds,unclassified:unclassified,totalNE:totalNE,fnByNo:fnByNo};
}

/* ---------- checks ---------- */
var KINDS=['header line removed','footer line removed','number and text split','paragraph joined across a page break','heading separated from paragraph text','heading title joined from two lines','footnote number restored','footnote block removed'];
function lp(n){return '<button type="button" class="lnk" data-para="'+n+'">para. '+n+'</button>';}
function lf(n){return '<button type="button" class="lnk" data-fn="'+n+'">fn '+n+'</button>';}
function checks(){
  var out=[],p=M.paras,N=M.pages.length,noref='no reference in this file';
  function add(name,status,vals,story,det){out.push({name:name,status:status,vals:vals,story:story,det:det||''});}
  /* 1 count */
  var d1=M.refPar==null?null:p.length-M.refPar;
  add('Paragraph count',d1==null?'notrun':d1===0?'pass':'fail','found '+p.length+' · reference '+(M.refPar==null?noref:M.refPar),
    "Given the converter's text, having split it at the paragraph numbers, we expect as many paragraphs as the document says it has.",
    d1!==0&&d1!=null?'<div class="det">Difference: '+(d1>0?'+':'−')+Math.abs(d1)+'. <button type="button" class="lnk" data-tab="1">Show the paragraph rows</button></div>':'');
  /* 2 numbering */
  var seen={},dups=[],gaps=[],order=[];
  p.forEach(function(x,i){if(seen[x.number])dups.push(x);seen[x.number]=1;if(x.number!==i+1)order.push(x);});
  var mx=p.reduce(function(m,x){return Math.max(m,x.number);},0);
  for(var n=1;n<=mx;n++)if(!seen[n])gaps.push(n);
  var ok2=!dups.length&&!gaps.length&&!order.length&&p.length>0;
  add('Numbering',ok2?'pass':'fail',ok2?'numbers run 1 to '+p.length+' in order':plural(gaps.length,'gap')+' · '+plural(dups.length,'duplicate'),
    'Given the paragraph numbers found, we expect exactly 1 to n, once each, in order.',
    ok2?'':'<div class="det">'+(gaps.length?'<div>Missing: '+gaps.slice(0,40).join(', ')+'</div>':'')+(dups.length?'<div>Duplicated: '+dups.map(function(x){return lp(x.number)+' (page '+x.pageStart+')';}).join(', ')+'</div>':'')+(order.length&&!gaps.length&&!dups.length?'<div>Out of order from '+lp(order[0].number)+'</div>':'')+'</div>');
  /* 3 first words */
  var bad=p.filter(function(x){return x.fwOk===false;});
  var haveFW=M.refFW!=null;
  add('First words',!haveFW?'notrun':bad.length?'fail':'pass',haveFW?plural(bad.length,'mismatch')+' of '+p.length+' paragraphs':'reference first words: '+noref,
    "Given each paragraph's first six words, we expect them to equal the document's own list, after straightening quotes and dashes.",
    bad.length?'<div class="det"><ul>'+bad.slice(0,40).map(function(x){return '<li>'+lp(x.number)+': found "'+esc(x.fwFound)+'" / reference "'+esc(x.fwRef)+'"</li>';}).join('')+'</ul></div>':'');
  /* 4 footnotes */
  var numd=M.footnotes.filter(function(f){return typeof f.no==='number';}),unn=M.footnotes.filter(function(f){return f.no===null;});
  var fs={},fd=[],fg=[];
  numd.forEach(function(f){if(fs[f.no])fd.push(f.no);fs[f.no]=1;});
  var tgt=M.refFn!=null?M.refFn:numd.length;
  for(var q=1;q<=tgt;q++)if(!fs[q])fg.push(q);
  var rest=M.footnotes.filter(function(f){return f.repaired;});
  var disp=[];M.pages.forEach(function(P){P.displaced.forEach(function(v){disp.push({page:P.page,n:v});});});
  var noblock=M.pages.filter(function(P){return !P.block;});
  var ok4=M.refFn!=null&&numd.length===M.refFn&&!fd.length&&!fg.length&&!unn.length&&rest.length===disp.length;
  add('Footnotes',M.refFn==null?'notrun':ok4?'pass':'fail','found '+numd.length+' · reference '+(M.refFn==null?noref:M.refFn),
    'Given the footnote block of each page and the numbers at the page foot, we expect footnotes 1 to the reference count, once each, with every displaced number restored.',
    '<div class="det">'+(fg.length?'<div>Missing numbers: '+fg.slice(0,30).join(', ')+'</div>':'')+(fd.length?'<div>Duplicated numbers: '+fd.join(', ')+'</div>':'')+(unn.length?'<div>Footnotes without a number: '+unn.length+' (page '+unn.map(function(f){return f.page;}).join(', ')+')</div>':'')+(noblock.length?'<div>Pages with no footnote block: '+noblock.map(function(P){return P.page;}).join(', ')+'</div>':'')+
    '<div>Restored as repairs ('+rest.length+' of '+disp.length+' displaced numbers): '+(rest.length?rest.map(function(f){return lf(f.no)+' (page '+f.page+')';}).join(', '):'none')+'</div></div>');
  /* 5 marks */
  var miss=[];if(M.refFn!=null)for(var w=M.marksFound+1;w<=M.refFn;w++)miss.push(w);
  var nofn=[];for(var v=1;v<=M.marksFound;v++)if(!M.fnByNo[v])nofn.push(v);
  var ok5=M.refFn!=null&&M.marksFound===M.refFn&&!nofn.length;
  add('Footnote marks',M.refFn==null?'notrun':ok5?'pass':'fail','marks found '+M.marksFound+' · reference '+(M.refFn==null?noref:M.refFn),
    'Given each paragraph read in order with a counter, we expect marks 1 to the reference count with no gap, and every mark to have its footnote.',
    '<div class="det">'+(miss.length?'<div>Marks not found: '+miss.slice(0,30).join(', ')+(miss.length>30?' …':'')+'</div>':'')+(nofn.length?'<div>Marks without a footnote text: '+nofn.join(', ')+'</div>':'')+
    '<div>Numbers read as text, not as marks ('+M.rejected.length+'; for example "article 11" stays as it is):</div><div class="ctx" style="max-height:150px;overflow:auto;border:1px solid var(--rule);padding:4px 8px;background:#fbf9f4">'+(M.rejected.length?M.rejected.map(function(x){return 'para. '+x.para+': …'+esc(x.ctx)+'… ['+x.n+']';}).join('<br>'):'none')+'</div></div>');
  /* 6 headers / footers */
  var hh=M.pages.filter(function(P){return P.header;}).length,pn=M.pages.filter(function(P){return P.pageNo;}).length;
  var ok6=hh===N&&pn===Math.max(N-1,0)&&rest.length===disp.length;
  add('Headers and footers',ok6?'pass':'fail','symbol header on '+hh+' of '+N+' pages · page number on '+pn+' of '+Math.max(N-1,0)+' expected · '+plural(disp.length,'displaced number'),
    'Given the first and last lines of each page, we expect the symbol on every page, a page number on every page but the first, and each displaced number matched to a footnote.',
    '<div class="det">'+(hh<N?'<div>Pages without the symbol as first line: '+M.pages.filter(function(P){return !P.header;}).map(function(P){return P.page;}).join(', ')+'</div>':'')+'<div>Displaced footnote numbers: '+(disp.length?disp.map(function(x){return x.n+' (page '+x.page+')';}).join(', '):'none')+'</div></div>');
  /* 7 headings */
  var lab=M.headings.filter(function(h){return h.kind==='roman'||h.kind==='letter';}),unl=M.headings.filter(function(h){return h.kind==='unlabelled'||h.kind==='further';});
  var ok7=M.headings.length>0&&p.length>0&&M.headings.every(function(h){return h.page<=p[p.length-1].pageEnd;});
  add('Headings',ok7?'pass':'fail',lab.length+' labelled · '+unl.length+' unlabelled',
    'Given the lines that sit before paragraph numbers, we expect headings to be kept out of the paragraph text. Read the list: a paragraph\'s last line taken for a heading would show here.',
    '<div class="det"><div>Unlabelled headings:</div><ul>'+(unl.length?unl.map(function(h){return '<li>'+esc(h.text)+' <span class="ctx">(page '+h.page+')</span></li>';}).join(''):'<li>none</li>')+'</ul></div>');
  /* 8 nothing lost */
  var sum=0,c=M.counts;for(var key in c)sum+=c[key];
  var ok8=sum===M.totalNE&&!M.unclassified.length;
  add('Nothing lost',ok8?'pass':'fail','classified '+sum+' of '+M.totalNE+' non-empty lines',
    'Given every non-empty line of every page, we expect each one to be counted exactly once as cover, header, heading, paragraph, footnote or footer.',
    '<div class="det"><div>Cover '+c.cover+' · header '+c.header+' · heading '+c.heading+' · paragraph '+c.paragraph+' · footnote '+c.footnote+' · footer '+c.footer+' · lines ending in a hyphen: '+M.hyphen+' (no hyphen joining is done)</div>'+
    (M.unclassified.length?'<div class="bad">Unclassified: '+M.unclassified.slice(0,20).map(function(l){return 'page '+l.page+', line '+l.n+': '+esc(cut(l.s,50));}).join('; ')+'. <button type="button" class="lnk" data-tab="4">Show the raw page viewer</button></div>':'')+'</div>');
  return out;
}

/* ---------- rendering ---------- */
var CK;
function render(){
  CK=checks();
  var ref=M.ref;
  $('title').textContent=D.title||M.symbol||'Untitled document';
  var meta=(D.doc_url?'<a href="'+esc(D.doc_url)+'" target="_blank" rel="noopener">'+esc(M.symbol)+'</a>':esc(M.symbol));
  if(ref&&ref.adopted)meta+=' · adopted '+esc(ref.adopted);
  meta+=' · '+plural(M.recs.length,'page')+' of raw converter text'+(D.source?' · '+esc(D.source):'');
  $('meta').innerHTML=meta;
  $('foot').innerHTML='<div>Source: '+esc(D.source||'the attached PDF text')+(D.built?' · built '+esc(D.built):'')+'. Counting, splitting and matching are done by this page\'s code; no model was called and nothing left the browser.</div>';
  renderResult();renderParas();renderFootnotes();renderChecks();renderMethod();
}
function renderResult(){
  var p=M.paras,d=M.refPar==null?null:p.length-M.refPar,nf=M.footnotes.filter(function(f){return typeof f.no==='number';}).length;
  var fwOk=p.filter(function(x){return x.fwOk===true;}).length;
  var passN=CK.filter(function(c){return c.status==='pass';}).length;
  function tile(lab,body,sub,how){return '<div class="tile"><div class="mono lab">'+lab+'</div>'+body+'<div class="sub">'+sub+'</div><p class="how"><span class="mono">How this is computed</span>'+how+'</p></div>';}
  var t1=tile('Paragraphs found','<div class="pair"><div class="big '+(d==null?'':d===0?'ok':'bad')+'">'+p.length+'<small>found</small></div><div class="big">'+(M.refPar==null?'?':M.refPar)+'<small>the document has</small></div></div>',
    d==null?'<span class="mut">no reference in this file</span>':d===0?'<span class="ok">equal</span>':'<span class="bad">differs by '+(d>0?'+':'−')+Math.abs(d)+'</span>',
    'Lines that are a number and a full stop ("12." alone, or "12. Text") start a paragraph. The document\'s own count comes from its reference.');
  var t2=tile('Footnotes found','<div class="big '+(M.refFn==null?'':nf===M.refFn?'ok':'bad')+'">'+nf+'<small>of '+(M.refFn==null?'?':M.refFn)+'</small></div>',
    M.refFn==null?'<span class="mut">no reference in this file</span>':nf===M.refFn?'<span class="ok">equal</span>':'<span class="bad">differs by '+(nf>M.refFn?'+':'−')+Math.abs(nf-M.refFn)+'</span>',
    'Footnotes whose number opens a line in the foot of a page, plus numbers put back from the page footer.');
  var t3=tile('First words match','<div class="big '+(M.refFW==null?'':fwOk===(M.refPar==null?p.length:M.refPar)?'ok':'bad')+'">'+fwOk+'<small>of '+(M.refPar==null?'?':M.refPar)+'</small></div>',
    M.refFW==null?'<span class="mut">no reference in this file</span>':fwOk===M.refPar?'<span class="ok">all equal</span>':'<span class="bad">'+(M.refPar-fwOk)+' differ or are missing</span>',
    'The first six words of each paragraph are compared with the document\'s list, after straightening quotes and dashes.');
  var t4=tile('Repairs made','<div class="big">'+M.log.length+'<small>changes by the script</small></div>','<button type="button" class="lnk" data-repairs="1">Open the repair log</button>','Every line removed, split, joined or restored is counted once and listed on tab 04.');
  $('r0').innerHTML='<div class="tiles">'+t1+t2+t3+t4+'</div><p class="checkline"><button type="button" class="lnk" data-tab="3">'+passN+' of '+CK.length+' checks pass</button></p>'+
    '<p class="gloss"><span class="mono">Words used here</span><br>The <b>footer</b> is the lines at the bottom of each page (page number, job code, date stamp). The <b>footnote block</b> is the footnotes printed at the foot of a page. A <b>displaced number</b> is a footnote number the converter moved into the footer, away from its footnote.</p>';
}
function pageStr(a,b){return a===b?String(a):a+'–'+b;}
function renderParas(){
  var p=M.paras;
  var cap=plural(p.length,'paragraph')+' found'+(M.refPar!=null?', '+M.refPar+' expected':', no reference to compare');
  var h='<div class="hbox"><button type="button" id="hbtn" aria-expanded="false" aria-controls="hlist">Headings found: '+M.headings.length+'</button><ol id="hlist" hidden>'+
    M.headings.map(function(x){return '<li>'+esc(x.text)+' <span class="ctx">(page '+x.page+', '+(x.kind==='roman'||x.kind==='letter'?'labelled':'unlabelled')+')</span></li>';}).join('')+'</ol></div>';
  h+='<table><caption><span class="mono">TAB.01</span>'+esc(cap)+'</caption><thead><tr><th scope="col" class="r c-no">No.</th><th scope="col" class="c-sec">Section</th><th scope="col" class="r c-pg">Page</th><th scope="col">First line</th><th scope="col" class="c-ck">Check</th></tr></thead><tbody id="pbody">';
  p.forEach(function(x,i){
    h+='<tr class="prow'+(x.fwOk===false?' flag':'')+'" data-i="'+i+'"><td class="r"><button type="button" class="rowbtn" id="b'+i+'" aria-expanded="false" aria-controls="d'+i+'" aria-label="Paragraph '+x.number+'">'+x.number+'</button></td><td>'+esc(x.section||'–')+'</td><td class="r">'+pageStr(x.pageStart,x.pageEnd)+'</td><td>'+esc(cut(x.text,120))+'</td><td>'+(x.fwOk===true?'OK':x.fwOk===false?'<span class="bad">first words differ</span>':'<span class="mut">not run</span>')+'</td></tr>';
    h+='<tr class="drow" id="d'+i+'" hidden><td colspan="5"></td></tr>';
  });
  h+='</tbody></table><p class="note">Source: '+esc(M.symbol)+', raw text from the PDF converter, split by this page. Footnote marks inside the text are shown in square brackets, like waste.[2], in this table, in the open paragraph and in the CSV. To remove them with find-and-replace, search for <code>\\[\\d+\\]</code> and replace with nothing. <span class="mono">click a row = open it</span></p>';
  $('r1').innerHTML=h;
}
function paraDetail(x){
  var i=x.idx,h='';
  h+='<div class="path mono">'+esc(x.path.length?x.path.join(' › '):'No heading above this paragraph')+'</div>';
  h+='<p class="ptext">'+esc(x.text)+'</p>';
  h+='<button type="button" class="tog" aria-expanded="false" aria-controls="pl'+i+'">Show the PDF\'s lines</button><pre class="lines" id="pl'+i+'" hidden>';
  var lastPg=null;
  x.raw.forEach(function(l){if(l.page!==lastPg){h+='<span class="bad">— page '+l.page+' begins —</span>\n';lastPg=l.page;}h+=esc(l.t)+'\n';});
  h+='</pre>';
  h+='<div class="blk"><span class="mono">First six words</span>Reference: '+(x.fwRef==null?'<span class="mut">no reference</span>':'"'+esc(x.fwRef)+'"')+' · found: "'+esc(x.fwFound)+'" · '+(x.fwOk===true?'<b class="ok">equal</b>':x.fwOk===false?'<b class="bad">different</b>':'<span class="mut">not run</span>')+'</div>';
  h+='<div class="blk"><span class="mono">Pages</span>'+(x.pageStart===x.pageEnd?'Page '+x.pageStart:'Pages '+x.pageStart+' to '+x.pageEnd+' (the paragraph crosses a page break)')+'</div>';
  h+='<div class="blk"><span class="mono">Repairs that touched this paragraph</span>'+(x.repairs.length?'<ul class="plain">'+x.repairs.map(function(e){return '<li>'+esc(e.kind)+': <span class="ctx">'+esc(cut(e.before,90))+' → '+esc(cut(e.after,90))+'</span></li>';}).join('')+'</ul>':'None')+'</div>';
  h+='<div class="blk"><span class="mono">Footnotes cited</span>'+(x.fns.length?'<ul class="plain">'+x.fns.map(function(f){return '<li><b>'+f.no+'</b> '+esc(f.text)+'</li>';}).join('')+'</ul>':'None')+'</div>';
  h+='<div class="blk"><button type="button" class="copy" data-cite="'+esc(x.citation)+'">Copy citation</button> <span class="mono">'+esc(x.citation)+'</span> <span class="ok" aria-live="polite" data-st></span></div>';
  return h;
}
function togglePara(i,open){
  var b=$('b'+i),d=$('d'+i);if(!b||!d)return;
  var on=open===true?true:b.getAttribute('aria-expanded')!=='true';
  b.setAttribute('aria-expanded',on?'true':'false');d.hidden=!on;
  if(on&&!d.getAttribute('data-built')){d.firstChild.innerHTML=paraDetail(M.paras[i]);d.setAttribute('data-built','1');}
}
function renderFootnotes(){
  var f=M.footnotes.filter(function(x){return typeof x.no==='number';});
  var cap='Footnotes found: '+f.length+' of '+(M.refFn==null?'?':M.refFn);
  var h='<table><caption><span class="mono">TAB.02</span>'+esc(cap)+'</caption><thead><tr><th scope="col" class="r c-no">No.</th><th scope="col" class="c-pg r">Page</th><th scope="col">Text</th><th scope="col" class="c-ck">Repair</th></tr></thead><tbody>';
  M.footnotes.forEach(function(x,i){
    if(typeof x.no!=='number')return;
    h+='<tr id="fr'+i+'" tabindex="-1"><td class="r"><b style="color:var(--accent);font-family:var(--serif)">'+x.no+'</b></td><td class="r">'+x.page+'</td><td>'+esc(x.text)+'</td><td>'+(x.repaired?'<span class="bad">number restored from the page foot</span>':'–')+'</td></tr>';
  });
  h+='</tbody></table><p class="note">Source: '+esc(M.symbol)+', footnote blocks of the raw PDF text. The cover\'s asterisked note is kept apart and is not counted. A footnote marked "restored" lost its number in the converter; the number was found at the page foot.</p>';
  h+='<p><button type="button" class="dl" id="dlf">Download footnotes.csv</button> <span class="mono" id="stf" aria-live="polite"></span></p>';
  $('r2').innerHTML=h;
}
function renderChecks(){
  var h='<ol class="checks">';
  CK.forEach(function(c,i){
    h+='<li class="chk"><div class="chk-line"><span class="mono">CHK.0'+(i+1)+'</span><strong>'+c.name+'</strong><span class="vals">'+c.vals+'</span><span class="st-'+c.status+'">'+(c.status==='pass'?'pass':c.status==='fail'?'check failed':'not run')+'</span></div><p class="story">'+esc(c.story)+'</p>'+c.det+'</li>';
  });
  h+='</ol>';
  var counts={};M.log.forEach(function(e){counts[e.kind]=(counts[e.kind]||0)+1;});
  h+='<div style="margin-top:22px"><button type="button" class="logh" id="logbtn" aria-expanded="false" aria-controls="logbody">Repair log ('+M.log.length+')</button><div id="logbody" hidden>';
  h+='<ul class="kinds">'+KINDS.map(function(k){return '<li><b>'+(counts[k]||0)+'</b> '+k+'</li>';}).join('')+'</ul>';
  h+='<table><caption><span class="mono">TAB.03</span>'+plural(M.log.length,'change')+' made by the script, in document order</caption><thead><tr><th scope="col" class="r">Page</th><th scope="col">Paragraph or footnote</th><th scope="col">What was done</th><th scope="col">Before</th><th scope="col">After</th></tr></thead><tbody>';
  M.log.forEach(function(e){h+='<tr><td class="r">'+e.page+'</td><td>'+esc(e.where)+'</td><td>'+esc(e.kind)+'</td><td class="ba">'+esc(cut(e.before,130))+'</td><td class="ba">'+esc(cut(e.after,130))+'</td></tr>';});
  h+='</tbody></table><p class="note">Source: the raw converter text of '+esc(M.symbol)+'. Nothing is changed in the stored text; the repairs are made on copies.</p></div></div>';
  $('r3').innerHTML=h;
}
function renderMethod(){
  var h='<ol class="plain" style="max-width:820px"><li>The header line (the document symbol) and the footer lines (page number, job code, date stamp) are taken off each page.</li><li>The footnote block at the foot of each page is cut off and kept as footnotes, counted in order 1, 2, 3.</li><li>The body lines of all pages are joined in page order, so a paragraph that crosses a page break is whole again.</li><li>A number and a full stop at the start of a line opens a paragraph. Headings are kept out of the paragraph text.</li><li>Footnote marks are found by counting: the first number 1 in the text is mark 1, the next 2, and so on. Other numbers (like "article 11") are left alone. A number straight after a word and a space is never taken as a mark.</li><li>The result is compared with the document\'s own reference (see tab 04).</li></ol>';
  h+='<div class="legend" aria-label="Legend"><span class="c-C">C cover</span><span class="c-H">H header</span><span class="c-S">S heading</span><span class="c-P">P paragraph</span><span class="c-N">N footnote</span><span class="c-F">F footer</span><span class="c-X">? not classified</span></div>';
  h+='<p><label for="rawsel"><span class="mono">Show raw page n</span></label> <select id="rawsel">'+M.pages.map(function(P,i){return '<option value="'+i+'">Page '+P.page+'</option>';}).join('')+'</select></p><div class="raw" id="rawv"></div>';
  h+='<h3 style="font:400 20px var(--serif);margin:26px 0 6px">Download</h3><p><button type="button" class="dl" id="dlp">Download paragraphs as CSV</button> <span class="mono" id="stp" aria-live="polite"></span></p><p class="note">One row per paragraph. UTF-8 with a byte-order mark, every field in double quotes, CRLF line ends. The column <code>text</code> keeps the footnote marks as [n]; <code>text_raw</code> does not.</p>';
  $('r4').innerHTML=h;
  showRaw(0);
  $('rawsel').addEventListener('change',function(){showRaw(+this.value);});
}
function showRaw(i){
  var P=M.pages[i],h='';
  P.lines.forEach(function(l){
    var code=l.cls==='blank'?'':l.cls?M.kinds[l.cls]:'?',cl=l.cls==='blank'?'c-blank':l.cls?'c-'+M.kinds[l.cls]:'c-X';
    h+='<div class="rl '+cl+'"><span class="ln">'+l.n+'</span><span class="cd">'+code+'</span><span>'+(l.t===''?'':esc(l.t))+'</span></div>';
  });
  $('rawv').innerHTML=h;
}

/* ---------- actions ---------- */
function gotoPara(n){
  var idx=-1;M.paras.some(function(p,i){if(p.number===n){idx=i;return true;}return false;});
  if(idx<0)return;
  selectTab(1);togglePara(idx,true);
  var b=$('b'+idx);b.scrollIntoView({block:'center'});b.focus();
}
function gotoFn(n){
  var idx=-1;M.footnotes.some(function(f,i){if(f.no===n){idx=i;return true;}return false;});
  if(idx<0)return;
  selectTab(2);
  [].forEach.call(document.querySelectorAll('tr.hit'),function(r){r.classList.remove('hit');});
  var r=$('fr'+idx);r.classList.add('hit');r.scrollIntoView({block:'center'});r.focus();
}
function openLog(){
  selectTab(3);
  var b=$('logbtn');b.setAttribute('aria-expanded','true');$('logbody').hidden=false;
  b.scrollIntoView({block:'start'});b.focus();
}
function csvCell(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"';}
function download(rows,name,statusId){
  var body='﻿'+rows.map(function(r){return r.map(csvCell).join(',');}).join('\r\n')+'\r\n';
  var blob=new Blob([body],{type:'text/csv;charset=utf-8'}),a=document.createElement('a');
  a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();document.body.removeChild(a);
  setTimeout(function(){URL.revokeObjectURL(a.href);},1500);
  $(statusId).textContent=(rows.length-1)+' rows prepared: '+name;
}
function fileBase(){return (M.symbol||'paragraphs').replace(/[\/\\]/g,'-');}
function dlParas(){
  var rows=[['number','section','part','page_start','page_end','first_words_reference','first_words_found','first_words_match','text','text_raw','footnotes_cited','repairs','citation','symbol','doc_url','text_lines']];
  M.paras.forEach(function(x){rows.push([x.number,x.section||'',x.part||'',x.pageStart,x.pageEnd,x.fwRef==null?'':x.fwRef,x.fwFound,x.fwOk==null?'':x.fwOk?'yes':'no',x.text,x.textRaw,x.marks.join('; '),x.repairs.map(function(e){return e.kind;}).join('; '),x.citation,M.symbol,D.doc_url||'',x.textLines]);});
  download(rows,fileBase()+'.csv','stp');
}
function dlFn(){
  var rows=[['number','page','text','repair','symbol','doc_url']];
  M.footnotes.forEach(function(f){if(typeof f.no==='number')rows.push([f.no,f.page,f.text,f.repaired?'number restored from the page foot':'',M.symbol,D.doc_url||'']);});
  download(rows,'footnotes.csv','stf');
}
function copyText(t,done,fail){
  function fb(){
    var ta=document.createElement('textarea');ta.value=t;ta.setAttribute('readonly','');ta.style.cssText='position:fixed;opacity:0';
    document.body.appendChild(ta);ta.select();var ok=false;try{ok=document.execCommand('copy');}catch(e){}
    document.body.removeChild(ta);if(ok)done();else fail();
  }
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,fb);}else fb();
}
document.addEventListener('click',function(e){
  var t=e.target;if(!t.closest)return;
  var el;
  if((el=t.closest('[data-repairs]'))){openLog();return;}
  if((el=t.closest('[data-tab]'))){selectTab(+el.getAttribute('data-tab'),false);return;}
  if((el=t.closest('[data-para]'))){gotoPara(+el.getAttribute('data-para'));return;}
  if((el=t.closest('[data-fn]'))){gotoFn(+el.getAttribute('data-fn'));return;}
  if((el=t.closest('.tog'))){var pre=$(el.getAttribute('aria-controls')),on=el.getAttribute('aria-expanded')!=='true';el.setAttribute('aria-expanded',on?'true':'false');pre.hidden=!on;return;}
  if((el=t.closest('.copy'))){
    var st=el.parentNode.querySelector('[data-st]');
    copyText(el.getAttribute('data-cite'),function(){st.textContent='Copied';setTimeout(function(){st.textContent='';},2000);},function(){st.textContent='Copy was blocked: select the citation next to the button.';});
    return;
  }
  if((el=t.closest('#logbtn'))){var o=el.getAttribute('aria-expanded')!=='true';el.setAttribute('aria-expanded',o?'true':'false');$('logbody').hidden=!o;return;}
  if((el=t.closest('#hbtn'))){var o2=el.getAttribute('aria-expanded')!=='true';el.setAttribute('aria-expanded',o2?'true':'false');$('hlist').hidden=!o2;return;}
  if(t.closest('#dlp')){dlParas();return;}
  if(t.closest('#dlf')){dlFn();return;}
  var tr=t.closest('tr.prow');
  if(tr&&!t.closest('.drow'))togglePara(+tr.getAttribute('data-i'));
});
try{M=build();render();}
catch(err){$('title').textContent='The page could not read this file';$('r0').innerHTML='<p class="bad">Error: '+esc(err&&err.message)+'</p>';}
})();
</script>
</body>
</html>
```
