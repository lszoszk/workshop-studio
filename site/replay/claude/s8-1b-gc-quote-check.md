I added a fifth tab, "05 CHECK A QUOTATION". It opens with a sample passage already checked: one correct quotation, one with a wrong paragraph and one invented. Verdicts come from code only, so the same text always gets the same verdicts. The tab checks against the whole file, not the filtered set, so the left rail is hidden there.

```edit
<<<<<<< SEARCH
</div>
<div class="shell" id="shell">
=======
  <button role="tab" id="t4" aria-controls="p4" aria-selected="false" tabindex="-1"><span class="tl">05 CHECK A QUOTATION</span></button>
</div>
<div class="shell" id="shell">
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    <section role="tabpanel" id="p3" aria-labelledby="t3" hidden><div id="chk"></div></section>
=======
    <section role="tabpanel" id="p3" aria-labelledby="t3" hidden><div id="chk"></div></section>
    <section role="tabpanel" id="p4" aria-labelledby="t4" hidden>
      <h2 class="h2">Check a quotation</h2>
      <p class="hint mono">Paste your own text. Quotations of 5+ words with a citation within 80 characters are checked against the paragraphs in the file.</p>
      <label class="mono lbl" for="qtext">Your passage</label>
      <textarea id="qtext" style="width:100%;height:12em;font:16px/1.5 system-ui,sans-serif;padding:8px;border:1px solid var(--ink);background:#fffdf8;color:var(--ink)"></textarea>
      <div class="bar"><button type="button" class="btn" id="qgo">Check quotations</button><button type="button" class="btn ghost" id="qsample">Use the sample passage</button></div>
      <p class="note">Code only, no model: the same text always gets the same verdicts. Quotation marks read: "…" “…” „…” «…». Words are compared ignoring case and punctuation. An ellipsis or a [bracketed change] splits a quotation into parts; every part of 3+ words must be found, in order, in one paragraph. A citation is a document symbol (CCPR/C/GC/37) or a short form (“General Comment No. 37” with the committee named nearby), with or without “para. N”; the citation nearest to the quotation is used. The sample passage is built from this file when the tab first opens.</p>
      <div id="qres" aria-live="polite"></div>
    </section>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
.empty{color:var(--grey);padding:20px 0}
=======
.empty{color:var(--grey);padding:20px 0}
.qv{border-top:1px solid var(--rule);padding:12px 0}
.qv .vd{font:700 13px var(--mono);letter-spacing:.06em;text-transform:uppercase}
.vd.vok{color:var(--green)}.vd.vcit{color:#8a5a00}.vd.vno{color:var(--red)}
.qv blockquote{margin:6px 0;padding-left:12px;border-left:3px solid var(--rule);max-width:80ch;white-space:pre-wrap}
.qv ul{margin:4px 0;padding-left:20px}
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
function renderActive(){[renderOverview,renderParagraphs,renderDraft,renderCheck][S.tab]();}
=======
function renderActive(){[renderOverview,renderParagraphs,renderDraft,renderCheck,renderQuote][S.tab]();}
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
var tabs=[0,1,2,3].map(function(k){return $('#t'+k);}),panels=[0,1,2,3].map(function(k){return $('#p'+k);});
=======
var tabs=[0,1,2,3,4].map(function(k){return $('#t'+k);}),panels=[0,1,2,3,4].map(function(k){return $('#p'+k);});
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
$('#shell').classList.toggle('norail',i===2);rail.hidden=i===2;
=======
$('#shell').classList.toggle('norail',i===2||i===4);rail.hidden=(i===2||i===4);
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
if(e.key==='ArrowRight')i=(i+1)%4;else if(e.key==='ArrowLeft')i=(i+3)%4;else if(e.key==='Home')i=0;else if(e.key==='End')i=3;else return;
=======
if(e.key==='ArrowRight')i=(i+1)%5;else if(e.key==='ArrowLeft')i=(i+4)%5;else if(e.key==='Home')i=0;else if(e.key==='End')i=4;else return;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
/* ---------- tabs and events ---------- */
=======
/* ---------- check a quotation ---------- */
var QX=null,qDone=false;
var SYMRX=/\b(?:CCPR|CESCR|CERD|CEDAW|CAT|CRC|CMW|CRPD|CED|HRI|A|E)\/[A-Za-z0-9.\-\/]*\d[A-Za-z0-9.\-\/]*/g;
var CNAMES=[['CCPR',/\bCCPR\b|human rights committee/i],['CESCR',/\bCESCR\b|economic, social and cultural rights/i],['CERD',/\bCERD\b|elimination of racial discrimination/i],['CEDAW',/\bCEDAW\b|discrimination against women/i],['CAT',/\bCAT\b|committee against torture/i],['CRC',/\bCRC\b|rights of the child/i],['CMW',/\bCMW\b|migrant workers/i],['CRPD',/\bCRPD\b|rights of persons with disabilities/i],['CED',/\bCED\b|enforced disappearances/i]];
function qWords(s){return String(s).replace(FNG,'').toLowerCase().replace(/['’‘`´]/g,'').split(/[^\p{L}\p{N}]+/u).filter(Boolean);}
function qInit(){
  if(QX)return;
  QX={sym:new Map()};
  D.forEach(function(d){
    d.w=' '+qWords(d.text).join(' ')+' ';
    d.sym.split(/\s*[–—,]\s*/).forEach(function(p){p=p.trim();if(!p)return;if(!QX.sym.has(p))QX.sym.set(p,new Set());QX.sym.get(p).add(d.title);});
  });
}
function qFind(txt){
  var re=/“([^“”]+)”|„([^„“”]+)[”“]|«([^«»]+)»|"([^"]+)"/g,m,out=[];
  while((m=re.exec(txt))){out.push({q:m[1]||m[2]||m[3]||m[4],s:m.index,e:m.index+m[0].length});}
  return out;
}
function qParts(q){
  var arr=q.split(/(…|\.\.\.|\[[^\]]*\])/),out=[],i,p,w;
  for(i=0;i<arr.length;i+=2){
    p=arr[i];
    var prev=arr[i-1],next=arr[i+1];
    if(prev&&prev[0]==='['&&/^\p{L}/u.test(p))p=p.replace(/^\S+/,'');
    if(next&&next[0]==='['&&/\p{L}$/u.test(p))p=p.replace(/\S+$/,'');
    w=qWords(p);
    if(w.length>=3)out.push(w);
  }
  return out;
}
function qCite(txt,k,list){
  var x=list[k],prevEnd=k>0?list[k-1].e:0,nextS=k<list.length-1?list[k+1].s:txt.length;
  var bef=txt.slice(Math.max(prevEnd,x.s-80),x.s),aft=txt.slice(x.e,Math.min(nextS,x.e+80));
  var both=bef+' '+aft,cands=[],paras=[];
  [[bef,true],[aft,false]].forEach(function(pr){
    var s=pr[0],isB=pr[1],m,re;
    var dist=function(idx,len){return isB?s.length-(idx+len):idx;};
    re=new RegExp(SYMRX.source,'g');
    while((m=re.exec(s))){var sy=m[0].replace(/[.\-\/]+$/,'');cands.push({k:'sym',sym:sy,label:sy,d:dist(m.index,m[0].length)});}
    re=/General\s+(?:Comment|Recommendation)s?\s*(?:No\.?|nr\.?|number|n°)?\s*(\d{1,3})(?!\d)/gi;
    while((m=re.exec(s)))cands.push({k:'gc',n:m[1],label:m[0],d:dist(m.index,m[0].length)});
    re=/\bG[CR]\s?(\d{1,3})(?!\d)/g;
    while((m=re.exec(s)))cands.push({k:'gc',n:m[1],label:m[0],d:dist(m.index,m[0].length)});
    re=/\b(?:paras?|paragraphs?|par)\.?\s*(\d{1,3})(?:\s*[–-]\s*(\d{1,3}))?/gi;
    while((m=re.exec(s)))paras.push({lo:+m[1],hi:m[2]?+m[2]:+m[1],label:m[0],d:dist(m.index,m[0].length)});
    re=/§\s*(\d{1,3})/g;
    while((m=re.exec(s)))paras.push({lo:+m[1],hi:+m[1],label:m[0],d:dist(m.index,m[0].length)});
  });
  var coms=CNAMES.filter(function(c){return c[1].test(both);}).map(function(c){return c[0];});
  cands=cands.filter(function(c){return c.k==='sym'||coms.length;}).sort(function(a,b){return a.d-b.d;});
  if(!cands.length)return null;
  paras.sort(function(a,b){return a.d-b.d;});
  var best=cands[0],titles=new Set();
  if(best.k==='sym'){
    var t0=QX.sym.get(best.sym);
    if(t0){
      t0.forEach(function(t){titles.add(t);});
      if(titles.size>1){
        var nm=/\bNo\.?\s*(\d{1,3})(?!\d)/.exec(both);
        if(nm){var rx=new RegExp('No\\.?\\s*0*'+nm[1]+'(?!\\d)','i'),f=[];titles.forEach(function(t){if(rx.test(t))f.push(t);});if(f.length)titles=new Set(f);}
      }
    }
  }else{
    var rxg=new RegExp('General\\s+(?:Comment|Recommendation)\\s+No\\.?\\s*0*'+best.n+'(?!\\d)','i');
    grp.forEach(function(a,t){
      if(rxg.test(t)&&a[0].committees.some(function(cc){return coms.some(function(c){return cc===c||cc.indexOf(c+'-')===0;});}))titles.add(t);
    });
  }
  return {best:best,para:paras[0]||null,titles:titles};
}
function qCheck(txt){
  qInit();
  var list=qFind(txt),res=[],skipShort=0,noCit=[];
  list.forEach(function(x,k){
    if(qWords(x.q).length<5){skipShort++;return;}
    var c=qCite(txt,k,list);
    if(!c){noCit.push(x);return;}
    var P=qParts(x.q);
    if(!P.length){res.push({x:x,c:c,v:'skip',P:P,cnt:[],match:[]});return;}
    var cnt=P.map(function(){return 0;}),match=[];
    D.forEach(function(d){
      var pos=0,ok=true;
      P.forEach(function(w,j){
        var s=' '+w.join(' ')+' ';
        if(d.w.indexOf(s)>=0)cnt[j]++;
        if(!ok)return;
        var i=d.w.indexOf(s,pos);
        if(i<0){ok=false;return;}
        pos=i+s.length-1;
      });
      if(ok)match.push(d);
    });
    var good=match.filter(function(d){return c.titles.has(d.title)&&(!c.para||(d.para>=c.para.lo&&d.para<=c.para.hi));});
    match.sort(function(a,b){return (c.titles.has(b.title)?1:0)-(c.titles.has(a.title)?1:0)||a.i-b.i;});
    res.push({x:x,c:c,P:P,cnt:cnt,match:match,good:good,v:!match.length?'no':good.length?'ok':'cit'});
  });
  return {res:res,skipShort:skipShort,noCit:noCit,total:list.length};
}
function qLink(d){return (d.r.doc_url?'<a href="'+esc(d.r.doc_url)+'" target="_blank" rel="noopener">'+esc(d.sym)+'</a>':esc(d.sym))+', <b>'+esc(d.pin)+'</b> · '+esc(d.st)+' · '+(isFinite(d.year)?d.year:'year not given');}
function samplePassage(){
  var c=D.filter(function(d){
    var w=d.copied.replace(/\s+/g,' ').trim().split(' ');
    return !d.shared&&!d.joint&&d.para>0&&!d.lettered&&!d.mismatch&&d.dupeN===1&&d.marks===0&&w.length>=20&&!/["“”„«»]/.test(d.copied)&&/^(CCPR|CESCR|CERD|CEDAW|CAT|CRC|CMW|CRPD|CED|HRI|A|E)\//.test(d.sym)&&/^[A-Za-z0-9.\/\-]+$/.test(d.sym);
  });
  if(c.length<3)return '';
  var a=c[0],b=c[Math.floor(c.length/3)],z=c[Math.floor(2*c.length/3)];
  var first=function(d,n){return d.copied.replace(/\s+/g,' ').trim().split(' ').slice(0,n).join(' ').replace(/[,;:]$/,'');};
  var inv='States parties must guarantee every person a free annual medical examination in every district of the country, financed entirely by regional authorities';
  return 'The Committee has stated that “'+first(a,18)+'” ('+a.sym+', para. '+a.para+'). Elsewhere it says “'+first(b,14)+'” ('+b.sym+', para. '+(b.para+7)+'). A third claim reads: “'+inv+'” ('+z.sym+', para. '+z.para+').';
}
function runQuote(){
  var txt=$('#qtext').value,box=$('#qres');
  if(!txt.trim()){box.innerHTML='<p class="empty">Paste a passage first.</p>';return;}
  var r=qCheck(txt),cnt={ok:0,cit:0,no:0,skip:0};
  r.res.forEach(function(x){cnt[x.v]++;});
  var h='<h3 class="fig"><span class="mono">RESULT</span>'+r.res.length+' quotation'+(r.res.length===1?'':'s')+' checked</h3>';
  h+='<p class="sumline"><span class="ok">✓ '+cnt.ok+' correct</span> · <span style="color:#8a5a00">≈ '+cnt.cit+' words right, citation wrong</span> · <span class="bad">✗ '+cnt.no+' not in the data</span>'+(cnt.skip?' · '+cnt.skip+' too fragmented to check':'')+'</p>';
  h+='<p class="hint mono">'+r.total+' quotation'+(r.total===1?'':'s')+' found · '+r.skipShort+' under five words ignored · '+r.noCit.length+' without a citation within 80 characters not checked · same text, same verdicts</p>';
  r.res.forEach(function(x){
    var c=x.c,pl=c.para?', para. '+(c.para.lo===c.para.hi?c.para.lo:c.para.lo+'–'+c.para.hi):'';
    var cited='Cited as: '+esc(c.best.label+pl)+(c.titles.size?' (found in the file: '+esc(Array.from(c.titles).slice(0,2).map(function(t){return docName(t)||t;}).join('; '))+(c.titles.size>2?' …':'')+')':' (no such document in this file)');
    h+='<div class="qv"><span class="vd '+(x.v==='ok'?'vok':x.v==='cit'?'vcit':x.v==='no'?'vno':'')+'">'+(x.v==='ok'?'✓ correct':x.v==='cit'?'≈ words right, citation wrong':x.v==='no'?'✗ not in the data':'not checked')+'</span>';
    h+='<blockquote>'+esc(x.x.q)+'</blockquote><p class="sub2">'+cited+(x.P.length?' · '+x.P.length+' part'+(x.P.length===1?'':'s')+' compared':'')+'</p>';
    if(x.v==='ok'){h+='<p>Found at: '+x.good.slice(0,3).map(qLink).join('<br>')+(x.good.length>3?'<br>and '+(x.good.length-3)+' more':'')+'</p>';}
    else if(x.v==='cit'){
      var inDoc=x.match.filter(function(d){return c.titles.has(d.title);});
      h+='<p>'+(inDoc.length?'The words are in the cited document, but not at the cited paragraph. Correct citation:':'The words are in a different document. Correct citation:')+'</p><ul>'+(inDoc.length?inDoc:x.match).slice(0,5).map(function(d){return '<li>'+qLink(d)+'<br><span class="mono2">'+esc(d.cit)+'</span></li>';}).join('')+'</ul>'+(x.match.length>5?'<p class="sub2">and '+(x.match.length-5)+' more paragraphs</p>':'');
    }else if(x.v==='no'){
      h+='<p>No paragraph of the file contains these words'+(x.P.length>1?' in order':'')+'. Paragraphs containing each part: '+x.P.map(function(w,j){return '“'+esc(w.slice(0,6).join(' '))+(w.length>6?' …':'')+'” '+x.cnt[j];}).join(' · ')+'.</p>';
    }
    h+='</div>';
  });
  if(r.noCit.length)h+='<h3 class="fig"><span class="mono">NOT CHECKED</span>No citation within 80 characters</h3><ul>'+r.noCit.map(function(x){var q=x.q.length>100?x.q.slice(0,100)+'…':x.q;return '<li>'+esc(q)+'</li>';}).join('')+'</ul>';
  if(!r.total)h+='<p class="empty">No quotation in quotation marks was found in this text.</p>';
  box.innerHTML=h;
}
function renderQuote(){
  if(qDone)return;
  qDone=true;
  var t=$('#qtext');
  if(!t.value)t.value=samplePassage();
  if(t.value)runQuote();
}
$('#qgo').addEventListener('click',runQuote);
$('#qsample').addEventListener('click',function(){$('#qtext').value=samplePassage();runQuote();});

/* ---------- tabs and events ---------- */
>>>>>>> REPLACE
```