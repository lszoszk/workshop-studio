Here is the verbatim finder, built to your plan: type words or "a phrase" and it lists every General Comment paragraph that contains them, word for word, with symbol, paragraph number and a copy-ready citation. The number of paragraphs searched is always on screen, and the second tab runs checks on the file and lists what the tool cannot do. Your draft list lives only on the page, so download it before you close it.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Verbatim finder: torture and ill-treatment</title>
<style>
:root{--paper:#fbfaf7;--ink:#111;--soft:#4a473f;--rule:#c8c3b6;--hl:#ffe066;
--cond:"Arial Narrow","Roboto Condensed","Liberation Sans Narrow","Helvetica Neue",Arial,sans-serif;
--mono:ui-monospace,Menlo,Consolas,monospace;--serif:Georgia,"Times New Roman",serif}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.wrap{max-width:960px;margin:0 auto;padding:24px 20px 96px}
.mono{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
.soft{color:var(--soft)}
h1,h2,h3{font-family:var(--cond);font-stretch:condensed;text-transform:uppercase;font-weight:700;letter-spacing:.02em;margin:0}
h1{font-size:clamp(34px,7vw,60px);line-height:.98;padding:8px 0 14px;border-bottom:8px solid #000}
h2{font-size:26px;line-height:1.1;margin:34px 0 10px}
h3{font-size:20px;line-height:1.15}
.source{margin:12px 0 0;font-size:15px;color:var(--soft)}
.source strong{color:var(--ink)}
[role=tablist]{display:flex;gap:0;margin:18px 0 0;border-bottom:1px solid var(--ink);flex-wrap:wrap}
[role=tab]{font:inherit;font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;background:transparent;color:var(--ink);border:0;border-bottom:4px solid transparent;padding:12px 18px;min-height:44px;cursor:pointer}
[role=tab]:hover{background:var(--hl)}
[role=tab][aria-selected=true]{background:#000;color:#fff;border-bottom-color:#000}
:focus-visible{outline:3px solid #000;outline-offset:3px}
[role=tab]:focus-visible{outline-offset:-3px;outline-color:#fff;box-shadow:inset 0 0 0 6px #000}
[role=tab][aria-selected=false]:focus-visible{outline-color:#000;box-shadow:none}
section[role=tabpanel]{padding-top:22px}
label.mono{display:block;margin-bottom:6px}
#q{width:100%;font:inherit;font-size:22px;padding:14px 16px;border:2px solid #000;background:#fff;color:#000;border-radius:0;-webkit-appearance:none;appearance:none}
.hint{margin:8px 0 0;color:var(--soft);line-height:1.7}
.try{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:14px 0 0}
.btn{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;border:1.5px solid #000;background:var(--paper);color:#000;padding:9px 14px;min-height:40px;cursor:pointer;border-radius:0}
.btn:hover{background:var(--hl)}
.btn.solid{background:#000;color:#fff}
.btn.solid:hover{background:#333}
.btn[aria-pressed=true]{background:var(--hl)}
.try .btn{font-family:inherit;font-size:15px;letter-spacing:0;text-transform:none}
.stat{display:flex;gap:18px;align-items:baseline;flex-wrap:wrap;margin:26px 0 0;padding-top:14px;border-top:1px solid var(--ink)}
.big{font-family:var(--serif);font-size:clamp(44px,9vw,56px);line-height:1;font-weight:700}
.statlabel{font-family:var(--cond);font-stretch:condensed;text-transform:uppercase;font-weight:700;font-size:22px;line-height:1.1}
.how{margin:10px 0 0;color:var(--soft);line-height:1.7}
.empty{margin:26px 0 0;font-size:18px;max-width:62ch}
#list{list-style:none;margin:16px 0 0;padding:0}
.res{border-top:1px solid var(--rule);padding:18px 0 20px}
.res .meta{display:flex;gap:14px;color:var(--soft);margin-bottom:4px}
.res .cite{margin:6px 0 10px;display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;overflow-wrap:anywhere}
.res .cite a{font-weight:700;color:#000;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:3px}
.res .text{margin:0 0 14px;max-width:72ch;overflow-wrap:anywhere}
.acts{display:flex;gap:8px;flex-wrap:wrap}
mark{background:var(--hl);color:#000;padding:0 1px}
.fn{font-family:var(--mono);font-size:.72em;color:var(--soft);vertical-align:super}
.more{margin:18px 0 0}
#draft{margin-top:44px;border-top:8px solid #000;padding-top:6px}
#draft .head{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:6px 0 4px}
#draft ol{padding:0;margin:14px 0 0;list-style:none}
#draft li{border-top:1px solid var(--rule);padding:14px 0}
#draft .c{font-family:var(--mono);font-size:13px;font-weight:700;overflow-wrap:anywhere}
#draft .t{margin:6px 0 10px;max-width:72ch;overflow-wrap:anywhere}
.btn.small{padding:5px 10px;min-height:32px}
.tblwrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:16px}
caption{text-align:left;font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;padding:0 0 8px;color:var(--soft)}
th,td{text-align:left;padding:8px 10px 8px 0;border-top:1px solid var(--rule);vertical-align:top}
thead th{border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;font-weight:400}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;padding-right:0}
.barwrap{display:flex;align-items:center;gap:8px;min-width:150px;justify-content:flex-end}
.bar{display:block;height:12px;background:#000}
.v{min-width:3.4em;text-align:right;font-variant-numeric:tabular-nums}
.figt{font-family:var(--cond);font-stretch:condensed;text-transform:uppercase;font-weight:700;font-size:20px;margin:0 0 4px}
.cannot li,.how2 li{margin:0 0 8px;max-width:70ch}
details{margin-top:6px}
summary{cursor:pointer;font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
details ul{margin:8px 0 0;padding-left:20px;font-size:14px;overflow-wrap:anywhere}
#toast{position:fixed;left:16px;bottom:16px;max-width:calc(100% - 32px);background:#000;color:#fff;font-family:var(--mono);font-size:12px;letter-spacing:.06em;padding:10px 14px;z-index:5;overflow-wrap:anywhere}
#toast:empty{display:none}
@media (max-width:560px){.wrap{padding:16px 14px 96px}[role=tab]{padding:12px 12px}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="mono soft">WORKSHOP_DATA.gc · General Comments, paragraph by paragraph</div>
  <h1>Verbatim finder: torture and ill-treatment</h1>
  <p class="source" id="source"></p>
</header>

<div role="tablist" aria-label="Sections">
  <button role="tab" id="tab0" aria-selected="true" aria-controls="p0" tabindex="0">01 Find</button>
  <button role="tab" id="tab1" aria-selected="false" aria-controls="p1" tabindex="-1">02 Checks &amp; limits</button>
</div>

<section id="p0" role="tabpanel" aria-labelledby="tab0">
  <form id="f" role="search" autocomplete="off">
    <label class="mono" for="q">01 Search the paragraphs</label>
    <input id="q" type="search" placeholder="e.g. cruel inhuman  or  &quot;ill-treatment&quot;" spellcheck="false">
  </form>
  <p class="hint mono">All words, any order · "quotes" = exact phrase · child also finds children · case and apostrophe shape ignored</p>
  <div class="try" id="try"><span class="mono soft">Try</span></div>

  <div class="stat" id="stat" aria-live="polite" hidden>
    <div class="big" id="bigN">0</div>
    <div>
      <div class="statlabel" id="statLabel"></div>
      <div class="mono soft" id="readAs"></div>
    </div>
  </div>
  <p class="empty" id="empty"></p>
  <p class="how mono" id="how">How this is computed: this page checks every paragraph in the file, in the file's order. A word also matches longer words that start with it. Words in quotes must match exactly. Not found here: summaries, synonyms, other sources, footnote texts (tab 02).</p>
  <ul id="list"></ul>
  <p class="more" id="more" hidden><button class="btn" id="moreBtn" type="button"></button></p>

  <div id="draft" hidden>
    <div class="head"><h2 style="margin:0">Your draft (<span id="dn">0</span>)</h2></div>
    <p class="hint mono">Kept only on this page, in the order you added them · download before you close it</p>
    <div class="acts" style="margin-top:10px">
      <button class="btn solid" id="copyAll" type="button">Copy all</button>
      <button class="btn" id="dl" type="button">Download .txt</button>
    </div>
    <ol id="dlist"></ol>
  </div>
</section>

<section id="p1" role="tabpanel" aria-labelledby="tab1" hidden>
  <p class="figt">FIG.01 · Paragraphs searched, by committee</p>
  <div class="tblwrap"><table id="tblCom"></table></div>
  <p class="how mono">How this is computed: records counted by their committee field; documents = distinct symbols (one symbol can hold several documents).</p>

  <h2>Checks run on this file, just now</h2>
  <div class="tblwrap"><table id="tblChk"></table></div>
  <p class="how mono">How this is computed: each row is counted by this page from the attached file when it opened.</p>

  <h2>What this tool cannot do</h2>
  <ul class="cannot" id="cannot"></ul>

  <h2>How you can check it</h2>
  <ol class="how2">
    <li>Search, in quotation marks, a phrase you know. It appears in a result word for word, apostrophes included.</li>
    <li>Click a result's symbol (it links to the UN document) and compare the paragraph with the original.</li>
    <li>Click "Copy citation", paste it into any document: symbol and paragraph number are the ones the result showed.</li>
  </ol>
</section>
</div>
<div id="toast" role="status" aria-live="polite"></div>

<script>
(function(){
var PAGE=50;
var FN=/\[\[fn:[^\]]*\]\]/g;
var gc=(window.WORKSHOP_DATA||{}).gc||{};
var recs=Array.isArray(gc.records)?gc.records:[];
var N=recs.length;
function $(id){return document.getElementById(id)}
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function fmt(n){return Number(n).toLocaleString('en')}
function plural(n,a,b){return n===1?a:b}

/* ---------- prepare the data ---------- */
var masked=recs.map(function(r){
  return String(r.text==null?'':r.text).replace(FN,function(m){return '\u0001'.repeat(m.length)});
});
var titlesBySym={};
recs.forEach(function(r){
  var s=r.symbol||'';
  (titlesBySym[s]=titlesBySym[s]||new Set()).add(r.short_title||r.title||'');
});
var ambList=Object.keys(titlesBySym).filter(function(s){return titlesBySym[s].size>1});
var ambSet=new Set(ambList);
var years=recs.map(function(r){return r.year}).filter(function(y){return typeof y==='number'&&isFinite(y)});
var y0=years.length?Math.min.apply(null,years):null, y1=years.length?Math.max.apply(null,years):null;

$('source').innerHTML='Source: '+esc(gc.source||gc.title||'UN General Comments')+'. <strong>n = '+fmt(N)+' paragraphs searched</strong>'+(y0!==null?', '+y0+'–'+y1:'')+'. The search covers every General Comment in the file; the examples are about torture.';

/* ---------- tabs ---------- */
var tabs=[$('tab0'),$('tab1')], panels=[$('p0'),$('p1')];
function selectTab(k,focus){
  tabs.forEach(function(t,j){
    var on=j===k;
    t.setAttribute('aria-selected',on?'true':'false');
    t.tabIndex=on?0:-1;
    panels[j].hidden=!on;
  });
  if(focus)tabs[k].focus();
}
tabs.forEach(function(t,k){
  t.addEventListener('click',function(){selectTab(k,false)});
  t.addEventListener('keydown',function(e){
    var n=tabs.length,j=null;
    if(e.key==='ArrowRight')j=(k+1)%n;
    else if(e.key==='ArrowLeft')j=(k-1+n)%n;
    else if(e.key==='Home')j=0;
    else if(e.key==='End')j=n-1;
    if(j!==null){e.preventDefault();selectTab(j,true)}
  });
});

/* ---------- search ---------- */
var state={q:'',terms:[],compiled:[],matches:[],shown:PAGE};
var draft=[];

function parse(q){
  q=q.replace(/[“”„]/g,'"');
  var out=[],re=/"([^"]*)(?:"|$)|([^\s"]+)/g,m;
  while((m=re.exec(q))){
    if(m[1]!==undefined){var s=m[1].trim();if(s)out.push({s:s,quoted:true});}
    else out.push({s:m[2],quoted:false});
  }
  return out;
}
function pat(s){
  var o='';
  for(var ch of s.trim()){
    if(/\s/.test(ch)){if(!/\\s\+\\u0001\*$/.test(o))o+='\\u0001*\\s+\\u0001*';}
    else if(/['’‘ʼ]/.test(ch))o+="['’‘ʼ]";
    else if(/[-‐‑]/.test(ch))o+='[-\\u2010\\u2011]';
    else if(/[.*+?^${}()|[\]\\\/]/.test(ch))o+='\\'+ch;
    else o+=ch;
  }
  return o;
}
function compile(terms){
  return terms.map(function(t){
    var src='(?<![\\p{L}\\p{N}])'+pat(t.s)+(t.quoted?'(?![\\p{L}\\p{N}])':'');
    return {test:new RegExp(src,'iu'),all:new RegExp(src,'giu')};
  });
}
function run(q){
  state.q=q;state.terms=parse(q);state.shown=PAGE;state.matches=[];
  try{state.compiled=compile(state.terms)}catch(e){state.compiled=[];state.terms=[];}
  if(state.compiled.length){
    for(var i=0;i<N;i++){
      var ok=true;
      for(var k=0;k<state.compiled.length;k++){if(!state.compiled[k].test.test(masked[i])){ok=false;break}}
      if(ok)state.matches.push(i);
    }
  }
  renderResults();
}
function rangesFor(i){
  var r=[],m,s=masked[i];
  state.compiled.forEach(function(c){
    c.all.lastIndex=0;
    while((m=c.all.exec(s))){r.push([m.index,m.index+m[0].length]);if(m[0].length===0)c.all.lastIndex++;}
  });
  r.sort(function(a,b){return a[0]-b[0]||b[1]-a[1]});
  var merged=[];
  r.forEach(function(x){
    var l=merged[merged.length-1];
    if(l&&x[0]<=l[1])l[1]=Math.max(l[1],x[1]);else merged.push([x[0],x[1]]);
  });
  return merged;
}
function paintText(text,ranges){
  var marks=[],m,re=new RegExp(FN.source,'g');
  while((m=re.exec(text)))marks.push([m.index,m.index+m[0].length]);
  var pts=new Set([0,text.length]);
  ranges.concat(marks).forEach(function(r){pts.add(r[0]);pts.add(r[1])});
  var p=Array.from(pts).sort(function(a,b){return a-b}),o='';
  for(var k=0;k<p.length-1;k++){
    var a=p[k],b=p[k+1];if(a===b)continue;
    var s=esc(text.slice(a,b));
    if(marks.some(function(r){return r[0]<=a&&b<=r[1]}))s='<span class="fn">'+s+'</span>';
    if(ranges.some(function(r){return r[0]<=a&&b<=r[1]}))s='<mark>'+s+'</mark>';
    o+=s;
  }
  return o;
}
function citation(i){
  var r=recs[i],c=r.symbol+', para. '+r.paragraph;
  if(ambSet.has(r.symbol||''))c+=' ('+(r.short_title||r.title||'')+')';
  return c;
}
function card(i){
  var r=recs[i];
  var sym=r.doc_url?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener noreferrer">'+esc(r.symbol)+'</a>':'<strong>'+esc(r.symbol)+'</strong>';
  return '<li class="res"><div class="meta mono"><span>'+esc(r.committee)+'</span><span>'+esc(r.year)+'</span></div>'+
    '<h3>'+esc(r.short_title||r.title||'')+'</h3>'+
    '<p class="cite">'+sym+'<span class="mono">para. '+esc(r.paragraph)+'</span></p>'+
    '<p class="text">'+paintText(String(r.text==null?'':r.text),rangesFor(i))+'</p>'+
    '<div class="acts"><button class="btn solid" type="button" data-act="copy" data-i="'+i+'">Copy citation</button>'+
    '<button class="btn" type="button" data-act="add" data-i="'+i+'" aria-pressed="false">Add to draft</button></div></li>';
}
function renderResults(){
  var T=state.terms,M=state.matches;
  if(!T.length){
    $('stat').hidden=true;$('list').innerHTML='';$('more').hidden=true;
    $('empty').textContent=state.q.trim()?'Nothing to search for yet. Type a word, or put a phrase in quotation marks.':'Type a word or a phrase above, or pick an example. '+fmt(N)+' paragraphs are ready to be searched.';
    return;
  }
  $('stat').hidden=false;
  $('bigN').textContent=fmt(M.length);
  var docs=new Set(M.map(function(i){return recs[i].symbol})).size;
  $('statLabel').textContent=plural(M.length,'matching paragraph','matching paragraphs')+(M.length?' in '+fmt(docs)+' '+plural(docs,'symbol','symbols'):'');
  $('readAs').textContent='Searched '+fmt(N)+' paragraphs · read as: '+T.map(function(t){return t.quoted?'“'+t.s+'”':t.s}).join('  AND  ');
  if(!M.length){
    $('empty').textContent='No paragraph contains all of these. 0 of '+fmt(N)+' paragraphs match. Every word must be present; try fewer words, or take the quotation marks off.';
    $('list').innerHTML='';$('more').hidden=true;return;
  }
  var shown=Math.min(state.shown,M.length);
  $('empty').textContent=M.length>shown?'Showing the first '+fmt(shown)+' of '+fmt(M.length)+', in the file’s order.':'';
  $('list').innerHTML=M.slice(0,shown).map(card).join('');
  var left=M.length-shown;
  $('more').hidden=left<=0;
  $('moreBtn').textContent='Show '+fmt(Math.min(PAGE,left))+' more ('+fmt(left)+' left)';
  syncAdd();
}
function syncAdd(){
  Array.prototype.forEach.call(document.querySelectorAll('button[data-act=add]'),function(b){
    var on=draft.indexOf(+b.dataset.i)>-1;
    b.setAttribute('aria-pressed',on?'true':'false');
    b.textContent=on?'In draft ✓ (click to remove)':'Add to draft';
  });
}

/* ---------- copy, draft, download ---------- */
var toastT;
function toast(msg){
  var t=$('toast');t.textContent=msg;clearTimeout(toastT);
  toastT=setTimeout(function(){t.textContent=''},4000);
}
function copyText(text){
  function fallback(){
    var ta=document.createElement('textarea');ta.value=text;ta.setAttribute('readonly','');
    ta.style.cssText='position:fixed;left:-9999px;top:0';document.body.appendChild(ta);ta.select();
    var ok=false;try{ok=document.execCommand('copy')}catch(e){}
    ta.remove();return ok;
  }
  if(navigator.clipboard&&navigator.clipboard.writeText){
    return navigator.clipboard.writeText(text).then(function(){return true},function(){return fallback()});
  }
  return Promise.resolve(fallback());
}
function draftText(){
  return draft.map(function(i){return citation(i)+'\n'+String(recs[i].text==null?'':recs[i].text)}).join('\n\n')+'\n';
}
function renderDraft(){
  $('draft').hidden=!draft.length;
  $('dn').textContent=draft.length;
  $('dlist').innerHTML=draft.map(function(i){
    var r=recs[i];
    return '<li><div class="c">'+esc(citation(i))+'</div><p class="t">'+paintText(String(r.text==null?'':r.text),[])+'</p>'+
      '<button class="btn small" type="button" data-act="rm" data-i="'+i+'">Remove</button></li>';
  }).join('');
  syncAdd();
}
function toggleDraft(i){
  var k=draft.indexOf(i);
  if(k>-1)draft.splice(k,1);else draft.push(i);
  renderDraft();
  toast(k>-1?'Removed from draft: '+citation(i):'Added to draft: '+citation(i));
}
document.addEventListener('click',function(e){
  var b=e.target.closest('button[data-act]');
  if(!b)return;
  var i=+b.dataset.i,act=b.dataset.act;
  if(act==='copy'){
    var c=citation(i);
    copyText(c).then(function(ok){
      toast(ok?'Copied: '+c:'The browser blocked copying. Select this citation by hand: '+c);
      if(ok){var old=b.textContent;b.textContent='Copied ✓';setTimeout(function(){b.textContent=old},1500)}
    });
  }else if(act==='add'||act==='rm'){toggleDraft(i)}
});
$('moreBtn').addEventListener('click',function(){state.shown+=PAGE;renderResults()});
$('copyAll').addEventListener('click',function(){
  copyText(draftText()).then(function(ok){toast(ok?'Copied '+draft.length+' '+plural(draft.length,'paragraph','paragraphs')+' with citations':'The browser blocked copying. Use Download instead.')});
});
$('dl').addEventListener('click',function(){
  var blob=new Blob([draftText()],{type:'text/plain;charset=utf-8'});
  var url=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=url;a.download='draft-quotes.txt';document.body.appendChild(a);a.click();a.remove();
  setTimeout(function(){URL.revokeObjectURL(url)},1500);
  toast('Download started. If nothing happened, use Copy all.');
});

/* ---------- input ---------- */
var timer;
var q=$('q');
q.addEventListener('input',function(){clearTimeout(timer);timer=setTimeout(function(){run(q.value)},140)});
$('f').addEventListener('submit',function(e){e.preventDefault();clearTimeout(timer);run(q.value)});
['"cruel, inhuman or degrading"','"ill-treatment"','torture "corporal punishment"'].forEach(function(ex){
  var b=document.createElement('button');b.type='button';b.className='btn';b.textContent=ex;
  b.addEventListener('click',function(){q.value=ex;clearTimeout(timer);run(ex);q.focus()});
  $('try').appendChild(b);
});

/* ---------- tab 02: checks and limits ---------- */
function missing(f){return recs.filter(function(r){return r[f]==null||r[f]===''}).length}
function renderChecks(){
  var by={};
  recs.forEach(function(r){
    var c=r.committee||'(none)';
    var o=by[c]=by[c]||{n:0,s:new Set(),a:Infinity,b:-Infinity};
    o.n++;o.s.add(r.symbol);
    if(typeof r.year==='number'&&isFinite(r.year)){o.a=Math.min(o.a,r.year);o.b=Math.max(o.b,r.year)}
  });
  var names=Object.keys(by).sort(function(x,y){return by[y].n-by[x].n});
  var max=names.length?by[names[0]].n:1;
  $('tblCom').innerHTML='<caption>Paragraphs per committee, largest first</caption>'+
    '<thead><tr><th scope="col">Committee</th><th scope="col" class="num">Symbols</th><th scope="col">Years</th><th scope="col" class="num">Paragraphs</th></tr></thead><tbody>'+
    names.map(function(c){
      var o=by[c];
      return '<tr><td><strong>'+esc(c)+'</strong></td><td class="num">'+fmt(o.s.size)+'</td><td>'+(isFinite(o.a)?(o.a===o.b?o.a:o.a+'–'+o.b):'—')+'</td>'+
        '<td class="num"><div class="barwrap"><span class="bar" style="width:'+Math.max(2,Math.round(o.n/max*100))+'px"></span><span class="v">'+fmt(o.n)+'</span></div></td></tr>';
    }).join('')+'</tbody>';

  var joint=Object.keys(titlesBySym).filter(function(s){return s.split(/\s*[–—]\s*/).length>1});
  var fnN=recs.filter(function(r){return String(r.text||'').indexOf('[[fn:')>-1}).length;
  var keys={};
  recs.forEach(function(r){var k=r.symbol+'|'+r.paragraph;keys[k]=(keys[k]||0)+1});
  var dup=Object.keys(keys).filter(function(k){return keys[k]>1}).length;
  var miss=['committee','short_title','symbol','doc_url','paragraph','text','year'].map(function(f){return [f,missing(f)]}).filter(function(x){return x[1]>0});
  function list(a,withTitles){
    if(!a.length)return '';
    return '<details><summary>Show them</summary><ul>'+a.slice(0,40).map(function(s){
      return '<li>'+esc(s)+(withTitles?' — '+fmt(titlesBySym[s].size)+' titles':'')+'</li>';
    }).join('')+(a.length>40?'<li>…and '+fmt(a.length-40)+' more</li>':'')+'</ul></details>';
  }
  var rows=[
    ['Paragraphs searched',fmt(N),'Every record in the file; the same number as in the header.'],
    ['Records with a field left empty',miss.length?miss.map(function(x){return x[0]+': '+fmt(x[1])}).join(', '):'none','Checked: committee, short title, symbol, link, paragraph, text, year.'],
    ['Symbols that hold more than one title',fmt(ambList.length),'For these, "Copy citation" adds the short title after the paragraph number, so the citation is unambiguous.'+list(ambList,true)],
    ['Joint symbols (two documents in one field)',fmt(joint.length),'Shown and cited exactly as stored.'+list(joint,false)],
    ['Same symbol and paragraph number more than once',fmt(dup),'Each such pair belongs to a symbol that holds several documents.'],
    ['Paragraphs with footnote marks like [[fn:12]]',fmt(fnN),'The marks stay in the text as stored (shown small). The footnotes themselves are not in the file.']
  ];
  $('tblChk').innerHTML='<caption>What this page found in the attached file</caption><thead><tr><th scope="col">Check</th><th scope="col" class="num">Result</th><th scope="col">What it means</th></tr></thead><tbody>'+
    rows.map(function(r){return '<tr><td>'+esc(r[0])+'</td><td class="num">'+esc(r[1])+'</td><td>'+r[2]+'</td></tr>'}).join('')+'</tbody>';

  $('cannot').innerHTML=[
    'It does not summarise, paraphrase or find synonyms: it finds only the words you typed. "Torture" will not find a paragraph that says "ill-treatment" unless that word is also in it.',
    'It searches only this file of General Comments and General Recommendations. Concluding observations, case law, reports and other sources are not here.',
    'English only. There is no translation.',
    'A word also matches longer words that start with it (child finds children, but rights will not find copyright). For an exact word, put it in quotation marks.',
    'Footnote texts are not in the file, only their marks. A phrase is found across a footnote mark only where the phrase has a space.',
    'It cannot tell you the paragraph is current or complete. The file is a copy: before you quote in a submission, open the symbol and compare.',
    'A paragraph is shown as stored. If the file has a typing or conversion error, the error is shown too.',
    'The draft list is not saved. Download it or copy it before you close the page. Nothing leaves your browser: this page makes no network requests.'
  ].map(function(s){return '<li>'+esc(s)+'</li>'}).join('');
}

/* ---------- start ---------- */
renderChecks();
renderResults();
if(!N){
  q.disabled=true;
  $('empty').textContent='The General Comments file is not attached, so there is nothing to search. Drag it from "Your files" into the chat.';
}
})();
</script>
</body>
</html>
```
