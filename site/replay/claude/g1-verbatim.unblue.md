I built the verbatim finder on the attached General Comments: type words or a "quoted phrase" and see every matching paragraph exactly as stored, with its symbol linked to the UN document and a button that copies the citation. It runs only in your browser and always shows how many paragraphs were searched. What it cannot do is listed at the bottom of the page.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Verbatim finder for General Comments</title>
<style>
:root{--ink:#1a2a3a;--panel:#eef4f8;--blue:#009edb;--deep:#00598a;--rule:#cfdde8;--mute:#44566a}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:#fff;color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.wrap{max-width:920px;margin:0 auto;padding:0 20px 80px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
header{padding:28px 0 18px;border-bottom:4px solid var(--blue)}
header .mono{color:var(--mute);margin:0 0 6px}
h1{font-size:34px;line-height:1.15;margin:0 0 8px;font-weight:700}
header p.sub{margin:0;color:var(--mute)}
section{margin-top:26px}
label.mono{display:block;margin-bottom:6px;color:var(--mute)}
input[type=search]{width:100%;font:inherit;font-size:20px;padding:12px 14px;border:2px solid var(--ink);border-radius:4px;background:#fff;color:var(--ink)}
.hint{margin:6px 0 0;color:var(--mute);font-size:14px}
.examples{margin-top:12px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.examples .mono{color:var(--mute)}
button{font:inherit;font-size:15px;cursor:pointer;border:2px solid var(--blue);background:var(--blue);color:var(--ink);padding:7px 14px;border-radius:4px;font-weight:600}
button.quiet{background:#fff;border-color:var(--ink)}
button:disabled{opacity:.55;cursor:default}
button:hover:not(:disabled){filter:brightness(.94)}
:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
a{color:var(--deep)}
.stats{background:var(--panel);padding:16px 18px;border-radius:4px;display:flex;flex-wrap:wrap;gap:6px 28px;align-items:baseline}
.big{font-size:52px;line-height:1;font-weight:700}
.stats .lbl{font-size:18px}
.stats .searched{margin-left:auto;font-weight:600}
.how{margin:8px 0 0;color:var(--mute);font-size:14px}
ul.list,ol.list{list-style:none;margin:16px 0 0;padding:0}
li.res{border-top:1px solid var(--rule);padding:16px 0}
li.res .meta{color:var(--mute);margin:0 0 4px}
li.res .cite{margin:0 0 8px;font-weight:700;font-size:18px}
li.res .txt{margin:0 0 10px;white-space:pre-wrap;max-width:75ch}
.btns{display:flex;gap:8px;flex-wrap:wrap}
mark{background:#b9e4f5;color:var(--ink);border-bottom:2px solid var(--blue);padding:0 1px}
.more{margin-top:16px}
.panel{background:var(--panel);padding:16px 18px;border-radius:4px}
.panel h2{font-size:20px;margin:0 0 8px}
.panel ul{margin:8px 0 0;padding-left:20px}
.panel li{margin-bottom:4px}
.draftrow{border-top:1px solid var(--rule);padding:10px 0}
.draftrow p{margin:0 0 6px}
.empty{color:var(--mute)}
#toast{position:fixed;right:16px;bottom:16px;background:var(--ink);color:#fff;padding:10px 14px;border-radius:4px;font-size:15px;max-width:80vw}
@media (max-width:600px){h1{font-size:26px}.stats .searched{margin-left:0}.big{font-size:44px}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <p class="mono" id="srcLabel">WORKSHOP_DATA.gc</p>
  <h1>Verbatim finder for General Comments</h1>
  <p class="sub" id="srcLine">Loading the file...</p>
</header>

<main>
<section aria-label="Search">
  <label class="mono" for="q">Words or "quoted phrase"</label>
  <input id="q" type="search" autocomplete="off" spellcheck="false" placeholder="best interests, or &quot;right to be heard&quot;">
  <p class="hint mono">all words, any order · quotes = phrase together · child finds children · not synonyms</p>
  <div class="examples">
    <span class="mono">Try</span>
    <button type="button" class="quiet ex">"best interests"</button>
    <button type="button" class="quiet ex">"right to be heard"</button>
    <button type="button" class="quiet ex">"juvenile justice"</button>
  </div>
</section>

<section aria-label="Result summary">
  <div class="stats">
    <span class="big" id="count">&ndash;</span>
    <span class="lbl" id="countLbl">Type a word or a phrase.</span>
    <span class="searched" id="searched"></span>
  </div>
  <p class="how" id="how">How this is computed: a paragraph matches when every word you typed begins a word in it and every quoted phrase appears exactly, ignoring capitals and apostrophe shape. Results keep the order of the file.</p>
</section>

<section aria-label="Results">
  <ol class="list" id="results"></ol>
  <div class="more"><button type="button" id="more" hidden>Show 25 more</button></div>
</section>

<section id="draft" aria-label="Draft">
  <div class="panel">
    <h2>Your draft <span class="mono" id="draftN">0 paragraphs</span></h2>
    <div class="btns">
      <button type="button" id="copyAll" disabled>Copy all</button>
      <button type="button" id="download" class="quiet" disabled>Download</button>
    </div>
    <div id="draftList"><p class="empty">Nothing added yet. Use "Add to draft" under a result.</p></div>
  </div>
</section>

<section id="limits" aria-label="Limits">
  <div class="panel">
    <h2>What this tool cannot do</h2>
    <ul>
      <li>It matches letters, not meaning: no synonyms, no summaries, no paraphrase. A typed word finds words that begin with it (child finds children and child&rsquo;s, but children does not find child).</li>
      <li>It searches only the attached General Comments, in English: no concluding observations, no case law, no translation.</li>
      <li>It does not check the file against the UN original. Open the linked symbol and compare before you quote. Footnote marks such as [[fn:12]] are shown as stored.</li>
      <li>A line-end hyphen or a different dash in the stored text can stop a phrase from matching; try fewer words.</li>
      <li>One symbol can cover several documents (for example A/48/18, or two symbols joined in one field). For those, the copied citation adds the short title; check it against the original.</li>
    </ul>
  </div>
</section>
</main>
</div>
<div id="toast" role="status" aria-live="polite" hidden></div>

<script>
(function(){
var D=(window.WORKSHOP_DATA||{}).gc||{};
var recs=Array.isArray(D.records)?D.records:[];
var PAGE=25;
var $=function(id){return document.getElementById(id);};
function el(tag,attrs){
  var e=document.createElement(tag);
  attrs=attrs||{};
  for(var k in attrs){
    var v=attrs[k];
    if(k==='class')e.className=v;
    else if(k.slice(0,2)==='on')e.addEventListener(k.slice(2),v);
    else if(v===true)e.setAttribute(k,'');
    else if(v!==false&&v!=null)e.setAttribute(k,v);
  }
  for(var i=2;i<arguments.length;i++){
    var c=arguments[i];
    if(Array.isArray(c)){c.forEach(function(x){if(x!=null)e.append(x);});}
    else if(c!=null)e.append(c);
  }
  return e;
}
var nf=function(n){return Number(n).toLocaleString('en');};

/* header facts, read from the data */
(function(){
  var years=recs.map(function(r){return r.year;}).filter(function(y){return typeof y==='number';});
  var coms={};recs.forEach(function(r){if(r.committee)coms[r.committee]=1;});
  var span=years.length?(Math.min.apply(null,years)+'–'+Math.max.apply(null,years)):'years not given';
  $('srcLabel').textContent='WORKSHOP_DATA.gc · '+(D.title||'General Comments, paragraph by paragraph');
  $('srcLine').textContent='Source: '+(D.source||'UN treaty bodies')+' · n = '+nf(recs.length)+' paragraphs · '+nf(Object.keys(coms).length)+' committees · '+span;
  $('searched').textContent=nf(recs.length)+' paragraphs searched';
})();

/* citations */
var titles=new Map();
recs.forEach(function(r){
  if(!titles.has(r.symbol))titles.set(r.symbol,new Set());
  titles.get(r.symbol).add(r.short_title||r.title||'');
});
var multiRe=/[–—;]\s*[A-Z][\w.]*\//;
function isMulti(r){return (titles.get(r.symbol)||new Set()).size>1||multiRe.test(r.symbol||'');}
function cite(r){
  var b=r.symbol+', para. '+r.paragraph;
  return (isMulti(r)&&r.short_title)?b+' ('+r.short_title+')':b;
}

/* clipboard and toast */
var toastTimer;
function toast(msg){
  var t=$('toast');t.textContent=msg;t.hidden=false;
  clearTimeout(toastTimer);toastTimer=setTimeout(function(){t.hidden=true;},2500);
}
function copyText(text){
  function fallback(){
    try{
      var ta=document.createElement('textarea');
      ta.value=text;ta.style.position='fixed';ta.style.opacity='0';
      document.body.append(ta);ta.select();
      var ok=document.execCommand('copy');ta.remove();return ok;
    }catch(e){return false;}
  }
  if(navigator.clipboard&&navigator.clipboard.writeText){
    return navigator.clipboard.writeText(text).then(function(){return true;},function(){return fallback();});
  }
  return Promise.resolve(fallback());
}
function copyWithLabel(btn,text,okMsg){
  copyText(text).then(function(ok){
    if(ok){
      var old=btn.textContent;btn.textContent='Copied';
      setTimeout(function(){btn.textContent=old;},1500);
      toast(okMsg);
    }else toast('Copy was blocked here. Select the text and copy it by hand.');
  });
}

/* matching */
function parse(q){
  var out=[],re=/["“”]([^"“”]*)["“”]|(\S+)/g,m;
  while((m=re.exec(q))){
    var t=(m[1]!==undefined?m[1]:m[2].replace(/["“”]/g,'')).trim();
    if(t)out.push(t);
  }
  return out;
}
function toRe(t){
  var s=t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')
    .replace(/['’‘ʼ`]/g,"['’‘ʼ]")
    .replace(/\s+/g,'\\s+');
  return new RegExp('(?<![\\p{L}\\p{N}])'+s,'iu');
}

var results=[],shown=0,regs=[],hre=null,terms=[];
function hl(text){
  if(!hre)return text;
  var out=[],last=0,m;
  hre.lastIndex=0;
  while((m=hre.exec(text))){
    if(m[0]==='')break;
    out.push(text.slice(last,m.index),el('mark',{},m[0]));
    last=m.index+m[0].length;
  }
  out.push(text.slice(last));
  return out;
}

var inDraft=new Map();   /* id -> {cite, text} */

function resultItem(r){
  var text=String(r.text==null?'':r.text);
  var c=cite(r);
  var copyBtn=el('button',{type:'button',class:'quiet'},'Copy citation');
  copyBtn.addEventListener('click',function(){copyWithLabel(copyBtn,c,'Copied: '+c);});
  var addBtn=el('button',{type:'button'},inDraft.has(r.id)?'In draft':'Add to draft');
  if(inDraft.has(r.id))addBtn.disabled=true;
  addBtn.addEventListener('click',function(){
    inDraft.set(r.id,{cite:c,text:text});
    addBtn.textContent='In draft';addBtn.disabled=true;
    renderDraft();toast('Added to draft: '+c);
  });
  return el('li',{class:'res'},
    el('p',{class:'meta mono'},[r.committee,r.year,r.short_title].filter(Boolean).join(' · ')),
    el('p',{class:'cite'},
      el('a',{href:r.doc_url,target:'_blank',rel:'noopener'},r.symbol),
      ', para. '+r.paragraph),
    el('p',{class:'txt'},hl(text)),
    el('div',{class:'btns'},copyBtn,addBtn)
  );
}

function render(){
  var list=$('results');
  list.textContent='';
  if(!recs.length){
    $('count').textContent='0';
    $('countLbl').textContent='The attached file has no paragraphs. Attach the General Comments file and try again.';
    $('more').hidden=true;return;
  }
  if(!terms.length){
    $('count').textContent='–';
    $('countLbl').textContent='Type a word or a phrase.';
    $('more').hidden=true;return;
  }
  var n=results.length;
  $('count').textContent=nf(n);
  var matched=terms.map(function(t){return /\s/.test(t)?'"'+t+'"':t;}).join(' + ');
  $('countLbl').textContent=(n===1?'paragraph contains ':'paragraphs contain ')+matched;
  if(n===0){
    list.append(el('li',{class:'res'},el('p',{class:'empty'},'No paragraph contains all of these. Nothing is shown rather than a near match; try fewer words or drop the quotes.')));
    $('more').hidden=true;return;
  }
  results.slice(0,shown).forEach(function(r){list.append(resultItem(r));});
  var left=n-shown;
  $('more').hidden=left<=0;
  if(left>0)$('more').textContent='Show '+Math.min(PAGE,left)+' more ('+nf(left)+' not yet shown)';
}

function run(){
  terms=parse($('q').value);
  regs=terms.map(toRe);
  if(!terms.length){results=[];hre=null;shown=0;render();return;}
  var srcs=regs.map(function(r){return r.source;}).sort(function(a,b){return b.length-a.length;});
  hre=new RegExp(srcs.join('|'),'giu');
  results=recs.filter(function(r){
    var t=String(r.text==null?'':r.text);
    return regs.every(function(re){return re.test(t);});
  });
  shown=PAGE;
  render();
}

/* draft */
function draftText(){
  var parts=[];
  inDraft.forEach(function(v){parts.push(v.cite+'\n“'+v.text+'”');});
  return parts.join('\n\n')+'\n';
}
function renderDraft(){
  var n=inDraft.size,box=$('draftList');
  $('draftN').textContent=n+(n===1?' paragraph':' paragraphs');
  $('copyAll').disabled=!n;$('download').disabled=!n;
  box.textContent='';
  if(!n){box.append(el('p',{class:'empty'},'Nothing added yet. Use "Add to draft" under a result.'));return;}
  inDraft.forEach(function(v,id){
    var rm=el('button',{type:'button',class:'quiet'},'Remove');
    rm.addEventListener('click',function(){inDraft.delete(id);renderDraft();render();});
    box.append(el('div',{class:'draftrow'},
      el('p',{class:'mono'},v.cite),
      el('p',{style:'white-space:pre-wrap;max-width:75ch'},'“'+v.text+'”'),
      rm));
  });
}
$('copyAll').addEventListener('click',function(){
  copyWithLabel($('copyAll'),draftText(),'Copied '+inDraft.size+' paragraphs');
});
$('download').addEventListener('click',function(){
  try{
    var blob=new Blob([draftText()],{type:'text/plain;charset=utf-8'});
    var u=URL.createObjectURL(blob);
    var a=el('a',{href:u,download:'draft-quotations.txt'});
    document.body.append(a);a.click();a.remove();
    setTimeout(function(){URL.revokeObjectURL(u);},1000);
  }catch(e){toast('Download was blocked here. Use "Copy all" instead.');}
});

/* wiring */
var timer;
$('q').addEventListener('input',function(){clearTimeout(timer);timer=setTimeout(run,120);});
Array.prototype.forEach.call(document.querySelectorAll('button.ex'),function(b){
  b.addEventListener('click',function(){$('q').value=b.textContent;run();$('q').focus();});
});
$('more').addEventListener('click',function(){shown+=PAGE;render();});
run();renderDraft();
})();
</script>
</body>
</html>
```
