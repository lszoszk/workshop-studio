Built: a four-tab app that parses the attached OHCHR HTML into numbered paragraphs with their headings, restores missing spaces rule by rule (logging every one), checks the result against the document's own reference, and exports the paragraphs as JSON or Markdown. Every number is computed by the page's code — no model is called and nothing leaves the browser.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN document HTML — numbered paragraphs</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1f6b3a;--dim:#6b675f}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
a{color:var(--red)}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.85em}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase}
.hint{color:var(--dim);text-transform:none;letter-spacing:.03em;font-size:11px}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;padding:22px 28px 14px;border-bottom:1px solid var(--rule)}
.label{color:var(--red);margin-bottom:6px}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:27px;line-height:1.2;margin:0 0 8px;max-width:62ch}
.meta{font-size:14px;color:var(--dim)}
.hright{white-space:nowrap;text-align:right;padding-bottom:4px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.dot.g{background:var(--green)}.dot.r{background:var(--red)}
nav[role=tablist]{display:flex;padding:0 20px;border-bottom:1px solid var(--rule)}
nav [role=tab]{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.12em;background:none;border:none;border-bottom:2px solid transparent;padding:12px 14px 10px;cursor:pointer;color:var(--ink)}
nav [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.layout{display:flex;align-items:flex-start}
aside{flex:0 0 250px;width:250px;border-right:1px solid var(--rule);padding:18px 20px 28px;position:sticky;top:0;max-height:100vh;overflow:auto}
.railhead{color:var(--red);border-bottom:1px solid var(--rule);padding-bottom:8px;margin-bottom:12px}
.doccard{border:1px solid var(--rule);padding:10px 12px;margin-bottom:18px}
.sym{color:var(--red)}
.shorttitle{font-family:Georgia,serif;font-size:14px;line-height:1.35;margin-top:6px}
.railnum{margin-bottom:20px}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1}
.bignum.red,.bignum.bad{color:var(--red)}
.bignum.ok{color:var(--green)}
.railsub{font-size:13px;color:var(--dim);margin-top:5px}
.bar{height:4px;background:var(--rule);margin-top:9px}
.bar i{display:block;height:100%;background:var(--green)}
.bar.bad i{background:var(--red)}
.railchecks{display:block;width:100%;background:none;border:none;border-top:1px solid var(--rule);padding:12px 0 0;cursor:pointer;font:inherit;font-size:13px;color:var(--red);text-align:left}
main{flex:1;min-width:0;padding:20px 28px 48px}
section[role=tabpanel]{max-width:1080px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr))}
.tile{padding:16px 20px 18px;border-left:1px solid var(--rule)}
.tile:first-child{border-left:none;padding-left:0}
.tlabel{color:var(--dim);margin-bottom:10px}
.tsub{font-size:14px;margin-top:6px}
.how{font-size:12.5px;color:var(--dim);margin-top:10px;border-top:1px solid var(--rule);padding-top:8px}
.notice{border:1px solid var(--red);padding:14px 16px;max-width:75ch}
.btitle{font-family:Georgia,serif;font-weight:400;font-size:21px;margin:28px 0 8px}
.btitle .cnt{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.1em;color:var(--dim);margin-left:10px;text-transform:uppercase}
table{border-collapse:collapse;width:100%;margin:10px 0 18px}
caption{text-align:left;font-family:Georgia,serif;font-size:17px;padding:6px 0 10px}
caption .mono{display:block;color:var(--dim);margin-bottom:3px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:400;text-align:left;border-bottom:1px solid var(--ink);padding:6px 14px 6px 0}
td{border-bottom:1px solid var(--rule);padding:8px 14px 8px 0;vertical-align:top;font-size:15px;overflow-wrap:anywhere}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
tr.prow{cursor:pointer}
tr.prow:hover{background:#ece6d8}
tr.prow .num{font-family:Georgia,serif;font-size:18px;color:var(--red)}
tr.pdet td{background:#efe9dc;padding:16px 20px}
tr.pdet .full{max-width:78ch;margin:8px 0 12px}
.path{color:var(--dim)}
.fw,.reps{font-size:14px;margin:6px 0}
.fix{outline:1px solid var(--red);padding:0 1px}
.ok{color:var(--green)}.bad{color:var(--red)}.notrun,.dim{color:var(--dim)}
.btn{font:inherit;font-size:15px;background:none;border:1px solid var(--ink);padding:8px 16px;cursor:pointer;margin:4px 8px 4px 0}
.btn:hover{background:#eae3d3}
.btn[disabled]{opacity:.4;cursor:not-allowed}
.acc{display:block;width:100%;text-align:left;background:none;border:none;border-top:1px solid var(--rule);padding:12px 0;cursor:pointer;font-family:Georgia,serif;font-size:18px;color:var(--ink)}
.acc::after{content:" +";color:var(--red)}
.acc[aria-expanded=true]::after{content:" –"}
.acc:hover{color:var(--red)}
.hlist{list-style:none;margin:8px 0 20px;padding:0}
.hlist li{padding:5px 0;border-bottom:1px solid var(--rule);font-size:15px}
.hlist .mono{color:var(--red);margin-right:8px}
.rrow{cursor:pointer}
.rrow:hover{background:#ece6d8}
.checks{margin:8px 0;padding-left:22px}
.checks li{margin:7px 0;font-size:15px;max-width:95ch}
.note{font-size:14px;color:var(--dim);max-width:85ch}
.ruleline{color:var(--dim);margin:4px 0 0}
footer{border-top:1px solid var(--rule);padding:14px 28px 24px;font-size:13px;color:var(--dim)}
.credits{margin-top:6px;font-size:12px}
@media (max-width:840px){.layout{flex-direction:column}aside{position:static;width:auto;flex:none;max-height:none;border-right:none;border-bottom:1px solid var(--rule)}header{flex-direction:column;align-items:flex-start;gap:8px}}
</style>
</head>
<body>
<header>
  <div>
    <div class="mono label">UN DOCUMENT · HTML</div>
    <h1 id="doctitle"></h1>
    <div class="meta" id="docmeta"></div>
  </div>
  <div class="hright" id="hstatus"></div>
</header>
<nav role="tablist" id="tablist" aria-label="Views of the document">
  <button role="tab" id="tab-1" aria-controls="p1" aria-selected="true">01 RESULT</button>
  <button role="tab" id="tab-2" aria-controls="p2" aria-selected="false" tabindex="-1">02 PARAGRAPHS</button>
  <button role="tab" id="tab-3" aria-controls="p3" aria-selected="false" tabindex="-1">03 LOST &amp; CHANGED</button>
  <button role="tab" id="tab-4" aria-controls="p4" aria-selected="false" tabindex="-1">04 CHECKS &amp; EXPORT</button>
</nav>
<div class="layout">
  <aside>
    <div class="mono railhead">DOCUMENT</div>
    <div class="doccard">
      <div class="mono sym" id="railsym"></div>
      <div class="shorttitle" id="railtitle"></div>
    </div>
    <div class="railnum">
      <div class="bignum" id="railp"></div>
      <div class="railsub" id="railpsub"></div>
      <div class="bar" id="railbar"><i></i></div>
    </div>
    <div class="railnum">
      <div class="bignum red">0</div>
      <div class="railsub">of <span id="railftotal"></span> footnotes — not in this HTML</div>
    </div>
    <button class="railchecks" id="railchecks"></button>
  </aside>
  <main>
    <section id="p1" role="tabpanel" aria-labelledby="tab-1"></section>
    <section id="p2" role="tabpanel" aria-labelledby="tab-2" hidden></section>
    <section id="p3" role="tabpanel" aria-labelledby="tab-3" hidden></section>
    <section id="p4" role="tabpanel" aria-labelledby="tab-4" hidden></section>
  </main>
</div>
<footer id="foot"></footer>
<script>
(function(){
'use strict';
var W = window.WORKSHOP_DATA || {};
var raw = W.html_doc;
var doc = Array.isArray(raw) ? (raw[0] || {}) : (raw || {});
var ref = doc.reference || null;
var symbol = doc.symbol || '(no symbol)';
var docUrl = doc.doc_url || '';
var title = doc.title || '(untitled)';
var source = doc.source || '';
var adopted = (ref && ref.adopted) ? ref.adopted : null;
var refParas = (ref && typeof ref.paragraphs === 'number') ? ref.paragraphs : null;
var refFoots = (ref && typeof ref.footnotes === 'number') ? ref.footnotes : null;
var firstWords = (ref && ref.first_words) ? ref.first_words : null;

function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function collapse(s){return String(s==null?'':s).replace(/\s+/g,' ').trim();}
function norm(s){return String(s==null?'':s).replace(/[\u201C\u201D]/g,'"').replace(/\u2019/g,"'").replace(/\u2013/g,'-').replace(/\u2011/g,'-').replace(/\u00A0/g,' ').replace(/\s+/g,' ').trim();}

/* ---- parse the HTML into block elements, in order ---- */
var blocks=[];
try{
  var parsed=new DOMParser().parseFromString(doc.html||'','text/html');
  if(parsed.body){
    (function walk(el){
      for(var i=0;i<el.children.length;i++){
        var c=el.children[i],t=c.tagName.toLowerCase();
        if(t==='div'||t==='section'||t==='article'||t==='main') walk(c); else blocks.push(c);
      }
    })(parsed.body);
  }
}catch(e){ blocks=[]; }

/* ---- repairs: insert a space only where the characters prove one was there ---- */
var RULES=[
  {key:'sentence',name:'sentence join',re:/([a-z])\.([A-Z])/g,ins:2},
  {key:'comma',name:'comma join',re:/([a-z]),([A-Za-z])/g,ins:2},
  {key:'quote',name:'quote join',re:/([a-z])\u201C/g,ins:1},
  {key:'dash',name:'dash join',re:/\u2013([A-Za-z])/g,ins:1}
];
function repair(rawText,num){
  var s=rawText,mask=[],i;
  for(i=0;i<rawText.length;i++) mask.push(false);
  var log=[];
  RULES.forEach(function(r){
    var ns='',nm=[],last=0;
    s.replace(r.re,function(m){
      var off=arguments[arguments.length-2],j;
      ns+=s.slice(last,off); for(j=last;j<off;j++) nm.push(mask[j]);
      var fixed=m.slice(0,r.ins)+' '+m.slice(r.ins);
      ns+=fixed;
      for(j=0;j<r.ins;j++) nm.push(mask[off+j]);
      nm.push(true);
      for(j=r.ins;j<m.length;j++) nm.push(mask[off+j]);
      last=off+m.length;
      log.push({para:num,rule:r.key,ruleName:r.name,match:m,fixed:fixed,
        prefix:s.slice(Math.max(0,off-20),off),
        suffix:s.slice(off+m.length,off+m.length+20)});
      return m;
    });
    ns+=s.slice(last); for(var k=last;k<s.length;k++) nm.push(mask[k]);
    s=ns; mask=nm;
  });
  return {text:s,mask:mask,log:log};
}

/* ---- classification ---- */
var paras=[],headings=[],flow=[],elements=[];
var coverN=0,titleText=null,lineN=0,otherEls=[];
var curSec=null,curPart=null,seenTitle=false;
var byNum={};

blocks.forEach(function(el){
  var tag=el.tagName.toLowerCase();
  var text=collapse(el.textContent);
  var clsAs;
  if(tag==='table'){ coverN++; clsAs='cover'; }
  else if(tag==='p'){
    var m=text.match(/^(\d{1,3})\.\s*(.*)$/);
    if(m){
      var num=parseInt(m[1],10);
      var rawText=collapse(m[2]);
      var rep=repair(rawText,num);
      var p={num:num,text_raw:rawText,text:rep.text,mask:rep.mask,repairs:rep.log,
             section:curSec,part:curPart,firstMatch:null,found6:'',ref6:''};
      paras.push(p); byNum[num]=p; flow.push({kind:'p',num:num});
      clsAs='paragraph';
    } else { lineN++; clsAs='committee line'; }
  }
  else if(tag==='h2'||tag==='h3'){
    if(tag==='h2'&&!seenTitle){
      seenTitle=true; titleText=text; clsAs='title';
      flow.push({kind:'h',tag:'h1',display:text});
    } else {
      var hm=text.match(/^([IVX]+|[A-Z])\.\s*(.+)$/);
      var label=null,htext=text,glued=false,display=text;
      if(hm){
        label=hm[1]; htext=collapse(hm[2]);
        glued=!/\s/.test(text.charAt(label.length+1));
        display=label+'. '+htext;
      }
      var isPart=(tag==='h2'&&label&&/^[IVX]+$/.test(label));
      headings.push({tag:tag,raw:text,label:label,text:htext,glued:glued,display:display,part:isPart});
      flow.push({kind:'h',tag:tag,display:display});
      curSec=display; if(isPart) curPart=display;
      clsAs='heading ('+tag+')';
    }
  }
  else { otherEls.push({tag:tag,text:text}); clsAs='unclassified'; }
  elements.push({tag:tag,cls:el.className||'',text:text.slice(0,80),clsAs:clsAs});
});

/* ---- first words against the reference ---- */
paras.forEach(function(p){
  p.found6=norm(p.text.split(/\s+/).slice(0,6).join(' '));
  if(firstWords){
    var rv=firstWords[String(p.num)];
    if(rv!=null){ p.ref6=norm(rv); p.firstMatch=(p.found6===p.ref6); }
  }
});

/* ---- characters counted over all paragraph texts ---- */
var CHARS=[
  {name:'en dash',glyph:'\u2013',cp:'U+2013',chars:'\u2013'},
  {name:'double quotes',glyph:'\u201C \u201D',cp:'U+201C / U+201D',chars:'\u201C\u201D'},
  {name:'right single quote',glyph:'\u2019',cp:'U+2019',chars:'\u2019'},
  {name:'non-breaking hyphen',glyph:'\u2011',cp:'U+2011',chars:'\u2011'},
  {name:'non-breaking space',glyph:'\u00A0',cp:'U+00A0',chars:'\u00A0'}
];
var charStats=CHARS.map(function(c){
  var count=0,example='';
  paras.forEach(function(p){
    for(var i=0;i<p.text.length;i++){
      if(c.chars.indexOf(p.text[i])>=0){
        count++;
        if(!example){
          var a=Math.max(0,i-25);
          var g=(p.text[i]==='\u00A0')?'\u2423':p.text[i];
          example=(a>0?'\u2026':'')+p.text.slice(a,i)+'['+g+']'+p.text.slice(i+1,i+26)+(i+26<p.text.length?'\u2026':'');
        }
      }
    }
  });
  return {name:c.name,glyph:c.glyph,cp:c.cp,count:count,example:example};
});

/* ---- repairs aggregated ---- */
var allRepairs=[];
paras.forEach(function(p){ p.repairs.forEach(function(r){ allRepairs.push(r); }); });
var perRule={sentence:0,comma:0,quote:0,dash:0};
allRepairs.forEach(function(r){ perRule[r.rule]++; });
var repairParas=paras.filter(function(p){ return p.repairs.length>0; }).length;

/* ---- exports ---- */
function footnoteSentence(){
  return 'no footnotes in this HTML version; the document has '+(refFoots!=null?refFoots:'an unknown number of')+' footnotes';
}
var records=paras.map(function(p){
  return {symbol:symbol,paragraph:p.num,section:p.section||'',part:p.part||'',
    text:p.text,text_raw:p.text_raw,
    first_words_match:(p.firstMatch===null?null:p.firstMatch),
    citation:symbol+', para. '+p.num,doc_url:docUrl,limitations:footnoteSentence()};
});
var jsonStr=JSON.stringify(records,null,2);
function buildMarkdown(){
  var L=['---',
    'title: '+JSON.stringify(title),
    'symbol: '+JSON.stringify(symbol),
    'adopted: '+JSON.stringify(adopted||'unknown'),
    'source_url: '+JSON.stringify(docUrl),
    'extracted: '+new Date().toISOString().slice(0,10),
    'paragraphs_found: '+paras.length,
    'paragraphs_expected: '+(refParas!=null?refParas:'unknown'),
    'footnotes: '+JSON.stringify(footnoteSentence()),
    '---',''];
  flow.forEach(function(f){
    if(f.kind==='h'){
      L.push((f.tag==='h1'?'# ':f.tag==='h2'?'## ':'### ')+f.display);
    } else {
      var p=byNum[f.num];
      L.push('**'+p.num+'.** '+p.text); L.push('');
    }
  });
  return L.join('\n');
}
var mdStr=buildMarkdown();

/* ---- checks ---- */
var checks=[];
function addCheck(name,detail,status,linkTab,linkLabel,note){
  checks.push({name:name,detail:detail,status:status,linkTab:(linkTab==null?null:linkTab),linkLabel:linkLabel||'',note:note||''});
}
if(refParas!=null){
  var ok=paras.length===refParas, diff=paras.length-refParas;
  addCheck('Paragraph count','found '+paras.length+' \u00B7 reference.paragraphs '+refParas+(ok?'':' ('+(diff>0?'+':'')+diff+')'),
    ok?'pass':'fail',ok?null:1,'see tab 02');
}else addCheck('Paragraph count','no reference in this file','notrun');

if(paras.length){
  var nums=paras.map(function(p){return p.num;});
  var dups=nums.filter(function(n,i){return nums.indexOf(n)!==i;});
  var max=Math.max.apply(null,nums);
  var gaps=[]; for(var gi=1;gi<=max;gi++) if(nums.indexOf(gi)<0) gaps.push(gi);
  var ordered=nums.every(function(n,j){return n===j+1;});
  var prob=dups.concat(gaps);
  addCheck('Numbering','numbers '+nums[0]+'\u2013'+nums[nums.length-1]+'; '+dups.length+' duplicates, '+gaps.length+' gaps'+(prob.length?' ('+prob.slice(0,10).join(', ')+')':''),
    ordered?'pass':'fail',ordered?null:1,'see tab 02');
}else addCheck('Numbering','no paragraphs found','notrun');

if(firstWords&&paras.length){
  var mm=paras.filter(function(p){return p.firstMatch===false;});
  var run=paras.filter(function(p){return p.firstMatch!==null;}).length;
  var det=run+' of '+paras.length+' paragraphs compared';
  if(mm.length) det+='; mismatches: '+mm.slice(0,10).map(function(p){
    return 'para. '+p.num+': found \u201C'+esc(p.found6)+'\u201D / reference \u201C'+esc(p.ref6)+'\u201D';
  }).join(' \u00B7 ');
  addCheck('First words',det,mm.length?'fail':'pass',mm.length?1:null,'see the flagged rows on tab 02');
}else addCheck('First words','no reference in this file','notrun');

if(refFoots!=null) addCheck('Footnotes','this HTML has 0 \u00B7 reference.footnotes '+refFoots,'limit',null,'','the HTML version has no footnotes: a limit of the source, not of the app');
else addCheck('Footnotes','no reference in this file','notrun');

addCheck('Repairs',allRepairs.length+' spaces restored in '+repairParas+' paragraphs \u2014 sentence '+perRule.sentence+', comma '+perRule.comma+', quote '+perRule.quote+', dash '+perRule.dash,
  'pass',2,'every one listed on tab 03','text_raw keeps the text as found');

var h2n=headings.filter(function(h){return h.tag==='h2';}).length;
var gluedN=headings.filter(function(h){return h.glued;}).length;
addCheck('Headings',h2n+' h2 + '+(headings.length-h2n)+' h3 = '+headings.length+' headings; '+gluedN+' glued labels separated (no space after the label\u2019s full stop)','pass');

var total=elements.length;
var sum=coverN+(titleText?1:0)+headings.length+paras.length+lineN+otherEls.length;
var uncls=otherEls.length?' \u2014 unclassified: '+otherEls.slice(0,5).map(function(o){return '&lt;'+esc(o.tag)+'&gt; '+esc(o.text.slice(0,40));}).join('; '):'';
addCheck('Nothing lost',total+' block elements: '+coverN+' cover, '+(titleText?1:0)+' title, '+headings.length+' headings, '+paras.length+' paragraphs, '+lineN+' committee lines, '+otherEls.length+' unclassified'+uncls,
  (sum===total&&otherEls.length===0)?'pass':'fail');

var rt='parse error';
try{ rt=JSON.parse(jsonStr).length; }catch(e){}
addCheck('Export round trip',(rt===paras.length)?('the JSON to download parses back to '+rt+' records = '+paras.length+' rows on tab 02'):('parse-back gave '+rt+', expected '+paras.length),
  rt===paras.length?'pass':'fail');

var nPass=checks.filter(function(c){return c.status==='pass';}).length;
var nFail=checks.filter(function(c){return c.status==='fail';}).length;
var nLimit=checks.filter(function(c){return c.status==='limit';}).length;
var nNotRun=checks.filter(function(c){return c.status==='notrun';}).length;
var nRun=nPass+nFail;

/* ---- header and rail ---- */
document.title=symbol+' \u2014 numbered paragraphs (HTML)';
document.getElementById('doctitle').textContent=title;
document.getElementById('docmeta').innerHTML=
  (docUrl?'<a href="'+esc(docUrl)+'" target="_blank" rel="noopener">'+esc(symbol)+'</a>':esc(symbol))+
  (adopted?' \u00B7 adopted '+esc(adopted):'')+
  ' \u00B7 '+paras.length+' paragraphs'+
  (source?' \u00B7 '+esc(source):'');
document.getElementById('hstatus').innerHTML=
  '<span class="dot '+(nFail>0?'r':'g')+'"></span><span class="mono">'+(nFail>0?nFail+' checks failed':nPass+' of '+nRun+' checks pass')+'</span>'+
  (nLimit?' <span class="mono bad">\u00B7 '+nLimit+' source limit</span>':'')+
  (nNotRun?' <span class="mono notrun">\u00B7 '+nNotRun+' not run</span>':'');

document.getElementById('railsym').textContent=symbol;
document.getElementById('railtitle').textContent=title;
document.getElementById('railp').textContent=paras.length;
document.getElementById('railpsub').textContent=refParas!=null?('of '+refParas+' paragraphs'):'paragraphs found';
var bar=document.getElementById('railbar');
bar.firstElementChild.style.width=(refParas!=null?Math.min(100,paras.length/refParas*100):100)+'%';
if(refParas!=null&&paras.length!==refParas) bar.classList.add('bad');
document.getElementById('railftotal').textContent=refFoots!=null?refFoots:'?';
var rc=document.getElementById('railchecks');
rc.textContent=(nFail>0?nFail+' checks failed':nPass+' of '+nRun+' checks pass')+' \u2014 see tab 04';

/* ---- tab 01: result ---- */
function tile(label,big,cls,sub,how){
  return '<div class="tile"><div class="mono tlabel">'+label+'</div><div class="bignum '+cls+'">'+big+'</div><div class="tsub">'+sub+'</div><div class="how">How this is computed: '+how+'</div></div>';
}
var matchCount=paras.filter(function(p){return p.firstMatch===true;}).length;
var p1=document.getElementById('p1');
var notice=paras.length===0?'<p class="notice">No paragraphs were found in this HTML: no &lt;p&gt; element starts with a number and a full stop. The exports on tab 04 are disabled.</p>':'';
var t1cls=(refParas!=null)?(paras.length===refParas?'ok':'bad'):'';
var t1sub=refParas!=null?('the document has '+refParas+(paras.length===refParas?' \u2014 equal':(paras.length>refParas?' \u2014 '+(paras.length-refParas)+' extra':' \u2014 '+(refParas-paras.length)+' short'))):'no reference in this file';
var t2big=firstWords?matchCount:'\u2014';
var t2cls=firstWords?((matchCount===paras.length&&paras.length>0)?'ok':(matchCount<paras.length?'bad':'')):'';
var t2sub=firstWords?('of '+(refParas!=null?refParas:paras.length)+' paragraphs match'):'no reference in this file';
p1.innerHTML=notice+'<div class="tiles">'+
  tile('Paragraphs found',paras.length,t1cls,t1sub,'every &lt;p&gt; in the parsed HTML whose text starts with a number and a full stop; compared with reference.paragraphs')+
  tile('First words match',t2big,t2cls,t2sub,'the first six words of each paragraph, normalised (curly quotes straight, en dashes and non-breaking hyphens to hyphens, non-breaking spaces to spaces), against reference.first_words')+
  tile('Footnotes','0','bad','of '+(refFoots!=null?refFoots:'?')+' footnotes \u2014 this HTML version has none; <a href="#" data-tab="2">see tab 03</a>','counted in the parsed HTML: this version has no footnote text and no footnote marks; reference.footnotes is the document\u2019s own count')+
  tile('Spaces repaired or flagged',allRepairs.length,'','in '+repairParas+' paragraphs \u2014 <a href="#" data-tab="2">see tab 03</a>','four rules insert a space only where the characters prove one was there; every insertion is logged and listed on tab 03')+
'</div>';

/* ---- tab 02: paragraphs ---- */
function firstLine(t){
  if(t.length<=120) return t;
  var s=t.slice(0,120),sp=s.lastIndexOf(' ');
  if(sp>0) s=s.slice(0,sp);
  return s+'\u2026';
}
function markedHtml(p){
  var out='',i;
  for(i=0;i<p.text.length;i++){
    if(p.mask[i]){
      var inner=esc(p.text[i]);
      if(i+1<p.text.length&&!p.mask[i+1]){ inner+=esc(p.text[i+1]); i++; }
      out+='<span class="fix" title="space restored here \u2014 see tab 03">'+inner+'</span>';
    } else out+=esc(p.text[i]);
  }
  return out;
}
function detailHtml(p){
  var path=(p.part&&p.section&&p.part!==p.section)?(p.part+' \u203A '+p.section):(p.section||p.part||'\u2014');
  var h='<div class="mono path">'+esc(path)+'</div>';
  h+='<p class="full">'+markedHtml(p)+'</p>';
  if(p.firstMatch===null) h+='<p class="fw notrun">first words: not run \u2014 no reference in this file</p>';
  else h+='<p class="fw '+(p.firstMatch?'ok':'bad')+'">first words \u2014 found: \u201C'+esc(p.found6)+'\u201D \u00B7 reference: \u201C'+esc(p.ref6)+'\u201D</p>';
  if(p.repairs.length){
    h+='<p class="reps">spaces restored here: '+p.repairs.length+' \u2014 '+p.repairs.map(function(r){
      return esc(r.ruleName)+' \u201C'+esc(r.match)+'\u201D \u2192 \u201C'+esc(r.fixed)+'\u201D';
    }).join(' \u00B7 ')+'</p>';
  } else h+='<p class="reps dim">no spaces restored in this paragraph</p>';
  var cite=symbol+', para. '+p.num;
  h+='<button class="btn copy" data-cite="'+esc(cite)+'">Copy citation</button> <span class="mono hint">citation: '+esc(cite)+'</span>';
  return h;
}
var p2=document.getElementById('p2');
var hbox='<button class="acc" id="hbox" aria-expanded="false">Headings found: '+headings.length+'</button>'+
  '<div id="hbody" hidden><ul class="hlist">'+headings.map(function(hh){
    return '<li><span class="mono">'+hh.tag.toUpperCase()+'</span>'+esc(hh.display)+(hh.glued?' <span class="mono hint">glued label separated</span>':'')+'</li>';
  }).join('')+'</ul></div>';
var rows=paras.map(function(p){
  var chk=p.firstMatch===true?'<span class="ok">OK</span>':(p.firstMatch===false?'<span class="bad">first words differ</span>':'<span class="notrun">not run</span>');
  return '<tr class="prow" data-n="'+p.num+'" tabindex="0" role="button" aria-expanded="false">'+
    '<td class="num">'+p.num+'</td><td>'+esc(p.section||'\u2014')+'</td><td>'+esc(firstLine(p.text))+'</td><td>'+chk+'</td></tr>'+
    '<tr class="pdet" data-n="'+p.num+'" hidden><td colspan="4">'+detailHtml(p)+'</td></tr>';
}).join('');
p2.innerHTML=hbox+
  '<table><caption><span class="mono">TAB.02</span>'+paras.length+' paragraphs found'+(refParas!=null?', '+refParas+' expected':'')+' \u2014 click a row for the full text, verbatim</caption>'+
  '<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>'+
  '<tbody>'+rows+'</tbody></table>';

/* ---- tab 03: lost & changed ---- */
var p3=document.getElementById('p3');
var footBlock='<h3 class="btitle">Lost: footnotes <span class="cnt">'+(refFoots!=null?('0 of '+refFoots):'0')+'</span></h3>'+
  '<p>The document has '+(refFoots!=null?refFoots:'an unknown number of')+' footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title\u2019s asterisk points to is missing. To cite a footnote, use the PDF or Word version.</p>';
var spaceBlock='<h3 class="btitle">Changed: spaces <span class="cnt">'+allRepairs.length+' restored in '+repairParas+' paragraphs</span></h3>'+
  '<p class="mono ruleline">SENTENCE '+perRule.sentence+' \u00B7 COMMA '+perRule.comma+' \u00B7 QUOTE '+perRule.quote+' \u00B7 DASH '+perRule.dash+'</p>'+
  '<table><caption><span class="mono">TAB.03</span>Every missing space the rules found and restored \u2014 click a row to open the paragraph on tab 02</caption>'+
  '<thead><tr><th scope="col" class="num">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead><tbody>'+
  allRepairs.map(function(r){
    return '<tr class="rrow" data-n="'+r.para+'" tabindex="0" role="button"><td class="num">'+r.para+'</td>'+
      '<td>'+esc(r.prefix)+'<span class="fix">'+esc(r.match)+'</span>'+esc(r.suffix)+'</td>'+
      '<td>'+esc(r.prefix)+'<span class="fix">'+esc(r.fixed)+'</span>'+esc(r.suffix)+'</td>'+
      '<td>'+esc(r.ruleName)+'</td></tr>';
  }).join('')+'</tbody></table>'+
  '<p class="note">Rules restore a space only where the characters prove it was there. Word pairs such as \u2018Giventhe\u2019 are not touched; the first-words check catches them only in a paragraph\u2019s first six words.</p>';
var charBlock='<h3 class="btitle">Changed: characters <span class="cnt">kept as published</span></h3>'+
  '<table><caption><span class="mono">TAB.03</span>Characters a keyboard does not type \u2014 counted over all paragraph texts</caption>'+
  '<thead><tr><th scope="col">Character</th><th scope="col" class="num">Count</th><th scope="col">Example</th></tr></thead><tbody>'+
  charStats.map(function(c){
    return '<tr><td><code>'+esc(c.glyph)+'</code> '+esc(c.name)+' <span class="mono hint">'+esc(c.cp)+'</span></td><td class="num">'+c.count+'</td><td>'+esc(c.example||'\u2014')+'</td></tr>';
  }).join('')+'</tbody></table>'+
  '<p class="mono hint">on a keyboard: a hyphen and straight quotes</p>'+
  '<p class="note">Kept exactly as published, in the table and in every export. A search for \u2018business-related\u2019 typed with the hyphen key will not find \u2018business\u2011related\u2019: normalise the text before searching it.</p>';
p3.innerHTML=footBlock+spaceBlock+charBlock;

/* ---- tab 04: checks & export ---- */
var p4=document.getElementById('p4');
var checksHtml='<h3 class="btitle">Checks <span class="cnt">'+nPass+' pass \u00B7 '+nFail+' failed'+(nLimit?' \u00B7 '+nLimit+' source limit':'')+(nNotRun?' \u00B7 '+nNotRun+' not run':'')+'</span></h3>'+
  '<ol class="checks">'+checks.map(function(c){
    var st=c.status==='pass'?'<span class="ok">pass</span>':c.status==='fail'?'<span class="bad">check failed</span>':c.status==='limit'?'<span class="bad">source limit</span>':'<span class="notrun">not run</span>';
    var link=c.linkTab!=null?' <a href="#" data-tab="'+c.linkTab+'">'+(c.linkLabel||'see the rows')+'</a>':'';
    return '<li><strong>'+esc(c.name)+'</strong> \u2014 '+c.detail+' '+st+link+(c.note?' <span class="dim">'+esc(c.note)+'</span>':'')+'</li>';
  }).join('')+'</ol>';
var expHtml='<h3 class="btitle">Export</h3>'+
  '<p class="note">The dataset travels with its source, its fields and its known limitations: every record carries symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url and limitations.</p>'+
  '<button class="btn" id="dljson"'+(paras.length?'':' disabled')+'>Download JSON</button>'+
  '<button class="btn" id="dlmd"'+(paras.length?'':' disabled')+'>Download Markdown</button>'+
  (paras.length?'':'<p class="bad">No paragraphs found \u2014 the exports are disabled.</p>')+
  '<p class="mono hint">file name: '+esc(symbol.replace(/\//g,'-'))+'.json / .md \u00B7 UTF-8 \u00B7 Blob URL</p>';
var elHtml='<button class="acc" id="elbox" aria-expanded="false">Elements found ('+elements.length+')</button>'+
  '<div id="elbody" hidden><table><caption><span class="mono">TAB.04</span>Every block element in the parsed HTML, in order, classified exactly once</caption>'+
  '<thead><tr><th scope="col">Tag</th><th scope="col">Classified as</th><th scope="col">Text (first 80 characters)</th></tr></thead><tbody>'+
  elements.map(function(e){
    return '<tr><td><code>&lt;'+esc(e.tag)+'&gt;</code>'+(e.cls?' <span class="mono hint">.'+esc(e.cls)+'</span>':'')+'</td><td>'+esc(e.clsAs)+'</td><td>'+esc(e.text)+'</td></tr>';
  }).join('')+'</tbody></table></div>';
p4.innerHTML=checksHtml+expHtml+elHtml;

/* ---- footer ---- */
document.getElementById('foot').innerHTML=
  '<span class="mono">SOURCE</span> '+esc(source)+(doc.built?' \u00B7 <span class="mono">BUILT</span> '+esc(doc.built):'')+
  ' \u00B7 Done by this page\u2019s code; no model was called and nothing left the browser.'+
  '<div class="credits">Method and citation practice follow The Turing Way, \u201CDocumentation and metadata\u201D (CC BY 4.0); the UK Government Analysis Function, \u201CQuality assurance of code for analysis and research: Testing code\u201D; and the Dag Hammarskj\u00F6ld Library, \u201CHow should I cite a UN document?\u201D.</div>';

/* ---- tabs ---- */
var tabs=Array.prototype.slice.call(document.querySelectorAll('#tablist [role=tab]'));
var panels=[document.getElementById('p1'),document.getElementById('p2'),document.getElementById('p3'),document.getElementById('p4')];
function activateTab(i){
  tabs.forEach(function(t,j){
    var on=(i===j);
    t.setAttribute('aria-selected',on?'true':'false');
    t.tabIndex=on?0:-1;
    panels[j].hidden=!on;
  });
}
tabs.forEach(function(t,i){ t.addEventListener('click',function(){ activateTab(i); }); });
document.getElementById('tablist').addEventListener('keydown',function(e){
  var i=tabs.indexOf(document.activeElement);
  if(i<0) return;
  var n=null;
  if(e.key==='ArrowRight') n=(i+1)%tabs.length;
  else if(e.key==='ArrowLeft') n=(i-1+tabs.length)%tabs.length;
  else if(e.key==='Home') n=0;
  else if(e.key==='End') n=tabs.length-1;
  if(n!==null){ e.preventDefault(); tabs[n].focus(); activateTab(n); }
});
document.addEventListener('click',function(e){
  var t=e.target&&e.target.closest?e.target.closest('[data-tab]'):null;
  if(t){ e.preventDefault(); activateTab(parseInt(t.getAttribute('data-tab'),10)); }
});
rc.addEventListener('click',function(){ activateTab(3); });

/* ---- paragraph rows ---- */
function toggleRow(r){
  var det=p2.querySelector('tr.pdet[data-n="'+r.getAttribute('data-n')+'"]');
  if(!det) return;
  var show=det.hidden;
  det.hidden=!show;
  r.setAttribute('aria-expanded',show?'true':'false');
}
p2.addEventListener('click',function(e){
  var c=e.target.closest?e.target.closest('.copy'):null;
  if(c){ copyCite(c); return; }
  var r=e.target.closest?e.target.closest('tr.prow'):null;
  if(r) toggleRow(r);
});
p2.addEventListener('keydown',function(e){
  if(e.key!=='Enter'&&e.key!==' ') return;
  var r=e.target.closest?e.target.closest('tr.prow'):null;
  if(r){ e.preventDefault(); toggleRow(r); }
});
function openParagraph(n){
  activateTab(1);
  var r=p2.querySelector('tr.prow[data-n="'+n+'"]');
  if(!r) return;
  var det=p2.querySelector('tr.pdet[data-n="'+n+'"]');
  if(det&&det.hidden){ det.hidden=false; r.setAttribute('aria-expanded','true'); }
  r.scrollIntoView({block:'center'});
}
p3.addEventListener('click',function(e){
  var r=e.target.closest?e.target.closest('tr.rrow'):null;
  if(r) openParagraph(parseInt(r.getAttribute('data-n'),10));
});
p3.addEventListener('keydown',function(e){
  if(e.key!=='Enter'&&e.key!==' ') return;
  var r=e.target.closest?e.target.closest('tr.rrow'):null;
  if(r){ e.preventDefault(); openParagraph(parseInt(r.getAttribute('data-n'),10)); }
});

/* ---- accordions ---- */
function bindAcc(btnId,bodyId){
  var b=document.getElementById(btnId),d=document.getElementById(bodyId);
  if(!b||!d) return;
  b.addEventListener('click',function(){
    var open=d.hidden;
    d.hidden=!open;
    b.setAttribute('aria-expanded',open?'true':'false');
  });
}
bindAcc('hbox','hbody');
bindAcc('elbox','elbody');

/* ---- copy citation ---- */
function copyCite(btn){
  var t=btn.getAttribute('data-cite');
  function done(){ var old=btn.textContent; btn.textContent='Copied'; setTimeout(function(){ btn.textContent=old; },2000); }
  function fb(){
    var ta=document.createElement('textarea');
    ta.value=t; ta.setAttribute('readonly',''); ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select();
    var ok=false; try{ ok=document.execCommand('copy'); }catch(err){}
    document.body.removeChild(ta);
    if(ok) done();
    else { btn.textContent=t; setTimeout(function(){ btn.textContent='Copy citation'; },2000); }
  }
  if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(done,fb); } else fb();
}

/* ---- downloads ---- */
function download(name,content,type){
  var blob=new Blob([content],{type:type+';charset=utf-8'});
  var url=URL.createObjectURL(blob);
  var a=document.createElement('a');
  a.href=url; a.download=name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function(){ URL.revokeObjectURL(url); },1500);
}
var baseName=symbol.replace(/\//g,'-');
var dj=document.getElementById('dljson'),dm=document.getElementById('dlmd');
if(dj) dj.addEventListener('click',function(){ if(paras.length) download(baseName+'.json',jsonStr,'application/json'); });
if(dm) dm.addEventListener('click',function(){ if(paras.length) download(baseName+'.md',mdStr,'text/markdown'); });

activateTab(0);
})();
</script>
</body>
</html>
```