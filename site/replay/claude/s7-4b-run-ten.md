I rewrote the app so one pipeline runs unchanged over all ten documents; the changes touch most of the file, so this is the full document. The left rail lists the ten documents, tabs 01 and 02 show the selected one, and the new tab 03 compares them and downloads all ten as one JSON or Markdown file. I have not run it on the real data, so the numbers for the nine new documents are untested. Any rule that does not fit a different layout will show up as a failed check, not as a silent change.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraphs out of a PDF: ten General Comments</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase}
a{color:#9b2335}
button{font:inherit;color:inherit;cursor:pointer}
:focus-visible{outline:3px solid #9b2335;outline-offset:2px}
header.top{padding:18px 28px 12px;border-bottom:1px solid #d9d2c3;display:flex;gap:24px;justify-content:space-between;flex-wrap:wrap}
header.top h1{font:normal 28px/1.2 Georgia,"Times New Roman",serif;margin:4px 0 6px}
.meta{font-size:14px;color:#4a463f}
.status{text-align:right;font-size:14px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
.dot.g{background:#2a6b3a}.dot.r{background:#9b2335}
.wrap{display:grid;grid-template-columns:270px 1fr;min-height:60vh}
aside{border-right:1px solid #d9d2c3;padding:18px 18px}
main{padding:0 28px 28px;min-width:0}
.big{font:normal 46px/1.05 Georgia,"Times New Roman",serif}
.rl{margin:0 0 16px}
.bar{height:5px;background:#e3dccc;margin:6px 0}
.bar i{display:block;height:100%;background:#2a6b3a}
.bar.bad i{background:#9b2335}
.hint{font-size:13px;color:#5a554b}
.red{color:#9b2335}.ok{color:#2a6b3a}.bad{color:#9b2335;font-weight:600}
.docs{list-style:none;margin:6px 0 18px;padding:0;border-top:1px solid #d9d2c3}
.docs li{border-bottom:1px solid #d9d2c3}
.docbtn{display:block;width:100%;text-align:left;background:none;border:0;border-left:3px solid transparent;padding:7px 6px 7px 8px;font-size:13px;line-height:1.35}
.docbtn[aria-current=true]{border-left-color:#9b2335;background:#ece6d8}
.docbtn b{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;display:block}
[role=tablist]{display:flex;gap:4px;border-bottom:1px solid #d9d2c3;margin:0 0 20px;flex-wrap:wrap}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;padding:14px 14px 10px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
[role=tab][aria-selected=true]{color:#9b2335;border-bottom-color:#9b2335}
h2.q{font:normal 22px Georgia,serif;margin:0 0 14px}
.tiles{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid #d9d2c3}
.tile{padding:14px 18px 14px 0;border-bottom:1px solid #d9d2c3}
.tile:nth-child(even){padding-left:18px;border-left:1px solid #d9d2c3}
.tile .big{font-size:48px}
.tile .how{font-size:12.5px;color:#5a554b;margin-top:6px}
.sec{margin-top:26px}
.btn{background:#fff;border:1px solid #1d1b18;padding:8px 14px;margin:0 8px 8px 0}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn.pri{background:#9b2335;border-color:#9b2335;color:#fff}
.hd{display:block;width:100%;text-align:left;background:none;border:0;border-top:1px solid #d9d2c3;padding:12px 0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.hd::before{content:"+ ";color:#9b2335}
.hd[aria-expanded=true]::before{content:"– "}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font:normal 18px Georgia,serif;padding:6px 0 8px}
caption .mono{display:block;color:#9b2335;margin-bottom:2px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;text-align:left;border-bottom:2px solid #1d1b18;padding:6px 8px;font-weight:normal}
td{border-bottom:1px solid #d9d2c3;padding:7px 8px;vertical-align:top}
th.n,td.n{text-align:right}
tr.r{cursor:pointer}
tr.r:hover{background:#ece6d8}
tr.cur{background:#ece6d8}
.numbtn{background:none;border:0;color:#9b2335;font-family:Georgia,serif;font-weight:bold;font-size:16px;padding:2px 4px;text-decoration:underline}
.detail td{background:#faf7f0;padding:14px 18px}
.ptext{max-width:80ch;margin:8px 0}
.sus{outline:1px solid #9b2335;padding:0 2px}
.lines div{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;white-space:pre-wrap}
.lines .pg{color:#9b2335;margin-top:6px}
.chk{list-style:none;padding:0;margin:0}
.chk li{border-top:1px solid #d9d2c3;padding:10px 0;font-size:14.5px}
.chk .st{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;text-transform:uppercase}
.linkbtn{background:none;border:0;color:#9b2335;text-decoration:underline;padding:0}
.note{font-size:14px;background:#ece6d8;padding:8px 12px;margin:8px 0}
.hl{font-size:14px;margin:4px 0}
footer{border-top:1px solid #d9d2c3;padding:14px 28px;font-size:13px;color:#4a463f}
@media(max-width:860px){.wrap{grid-template-columns:1fr}aside{border-right:0;border-bottom:1px solid #d9d2c3}.tiles{grid-template-columns:1fr}.tile:nth-child(even){padding-left:0;border-left:0}}
</style>
</head>
<body>
<header class="top">
 <div>
  <div class="mono">UN documents · PDF text · ten General Comments</div>
  <h1 id="title"></h1>
  <div class="meta" id="meta"></div>
 </div>
 <div class="status" id="status"></div>
</header>
<div class="wrap">
 <aside id="rail" aria-label="Documents"></aside>
 <main>
  <div role="tablist" aria-label="Views">
   <button role="tab" id="t1" aria-selected="true" aria-controls="p1" data-tab="1">01 Result</button>
   <button role="tab" id="t2" aria-selected="false" aria-controls="p2" data-tab="2" tabindex="-1">02 Paragraphs</button>
   <button role="tab" id="t3" aria-selected="false" aria-controls="p3" data-tab="3" tabindex="-1">03 All documents</button>
  </div>
  <section id="p1" role="tabpanel" aria-labelledby="t1"></section>
  <section id="p2" role="tabpanel" aria-labelledby="t2" hidden></section>
  <section id="p3" role="tabpanel" aria-labelledby="t3" hidden></section>
 </main>
</div>
<footer id="foot"></footer>
<script>
(function(){
const W=window.WORKSHOP_DATA||{};
const TEN=W.pdf_ten||{};
const DOCS=Array.isArray(TEN.records)?TEN.records:[];
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function normQ(s){return String(s).replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();}
const ABBR=/(^|[^A-Za-z])(No|Nos|art|arts|Art|Arts|para|paras|Para|Paras|p|pp|vol|Vol|Res|res)\.$/;
function firstWords(text){
  const toks=text.split(/\s+/).filter(Boolean),out=[];
  for(let i=0;i<toks.length&&out.length<6;i++){
    let w=toks[i];
    if(/^\d{1,3}$/.test(w)){
      const prev=out[out.length-1];
      if(prev&&/[.,”"’']$/.test(prev)&&!ABBR.test(prev))continue;
    }
    const m=w.match(/^(.*[A-Za-z.,;:)”’"])(\d{1,3})$/);
    if(m&&!/[\/-]$/.test(m[1]))w=m[1];
    out.push(w);
  }
  return out.join(' ');
}
const isLabel=t=>/^([IVX]+|[A-Z])\.$/.test(t);
const isStart=t=>/^\d{1,3}\.$/.test(t)||/^\d{1,3}\. .+$/.test(t);
const headLike=t=>t.length>0&&t.length<=90&&/^[A-Z]/.test(t)&&!/[.;:,\d]$/.test(t);
function suspectReason(t){
  if(/^\d{1,3}$/.test(t))return 'bare number';
  if(/^\d{1,3} ([A-Z]|[“"‘'])/.test(t))return 'starts with a number and a space';
  if(/^\* /.test(t))return 'starts with an asterisk';
  return null;
}
function romanVal(s){const m={I:1,V:5,X:10};let v=0;for(let i=0;i<s.length;i++){const a=m[s[i]],b=m[s[i+1]]||0;v+=a<b?-a:a;}return v;}

/* ---------- the one pipeline, run on every document ---------- */
function analyze(D){
const pages=(D.pages||[]).slice().sort((a,b)=>a.page-b.page);
const symbol=D.symbol||'';
const ref=D.reference||{};
const refParas=typeof ref.paragraphs==='number'?ref.paragraphs:null;
const refFoot=typeof ref.footnotes==='number'?ref.footnotes:null;
const refFW=(ref.first_words&&typeof ref.first_words==='object')?ref.first_words:null;
const all=[],pageInfo=[],warnings=[];
let totalNonEmpty=0;
pages.forEach(pg=>{
  const raw=String(pg.text||'').split('\n').map(s=>s.trim());
  totalNonEmpty+=raw.filter(t=>t!=='').length;
  const ls=raw.map(t=>({page:pg.page,text:t,kind:t===''?'blank':null}));
  const info={page:pg.page,header:false,pageNumber:false,displaced:[]};
  const f=ls.findIndex(l=>l.kind!=='blank');
  if(f>=0){
    if(ls[f].text===symbol){ls[f].kind='header';info.header=true;}
    else warnings.push('page '+pg.page+': first line is not the symbol');
  }
  let k=ls.length-1;
  while(k>=0){
    const l=ls[k],t=l.text;
    if(l.kind==='blank'){k--;continue;}
    if(l.kind==='header')break;
    if(/^GE\./.test(t)||/^\d{6}(\s+\d{6})*$/.test(t)){l.kind='footer';k--;continue;}
    if(/^\d{1,3}$/.test(t)){
      l.kind='footer';
      if(Number(t)===pg.page)info.pageNumber=true;else info.displaced.push(t);
      k--;continue;
    }
    break;
  }
  pageInfo.push(info);
  all.push.apply(all,ls);
});
const body=all.filter(l=>l.kind!=='header'&&l.kind!=='footer');
const paras=[],headings=[],events=[];
let cur=null,started=false,part=null,letter=null,unl=null,lastRoman=0,suspectPage=null;
const pathNow=()=>[part,letter,unl].filter(Boolean);
function nextNonBlank(i){let j=i+1;while(body[j]&&body[j].text==='')j++;return body[j]||null;}
for(let i=0;i<body.length;i++){
  const l=body[i],t=l.text;
  if(t==='')continue;
  const lm=t.match(/^([IVX]+|[A-Z])\.$/);
  if(lm){
    l.kind='heading';
    const parts=[];
    let j=i+1;
    while(j<body.length){
      const x=body[j];
      if(x.text===''){j++;continue;}
      if(isLabel(x.text)||isStart(x.text))break;
      x.kind='heading';parts.push(x.text);j++;
    }
    const txt=parts.join(' ').replace(/\s+/g,' ').trim();
    const full=lm[1]+'. '+txt;
    const roman=/^[IVX]+$/.test(lm[1])&&romanVal(lm[1])===lastRoman+1;
    if(roman){lastRoman=romanVal(lm[1]);part=full;letter=null;unl=null;}
    else{letter=full;unl=null;}
    headings.push({kind:'labelled',level:roman?2:3,text:full,page:l.page});
    events.push({type:'heading',level:roman?2:3,text:full});
    i=j-1;
    continue;
  }
  const sm=t.match(/^(\d{1,3})\.(?: (.+))?$/);
  if(sm){
    l.kind='paragraph';
    suspectPage=null;started=true;
    cur={number:Number(sm[1]),startPage:l.page,lines:[],part:part,section:pathNow().slice(-1)[0]||'',path:pathNow().join(' › ')};
    if(sm[2])cur.lines.push({page:l.page,text:sm[2],suspect:false,trigger:null,src:l});
    paras.push(cur);events.push({type:'para',p:cur});
    continue;
  }
  if(!started){l.kind='cover';continue;}
  const reason=suspectReason(t);
  if(reason)suspectPage=l.page;
  const inSus=suspectPage===l.page;
  const nx=nextNonBlank(i);
  if(!inSus&&headLike(t)&&nx&&isStart(nx.text)){
    l.kind='heading';
    let txt=t;
    const prev=cur.lines[cur.lines.length-1];
    if(prev&&prev.src===body[i-1]&&!prev.suspect&&headLike(prev.text)){
      cur.lines.pop();prev.src.kind='heading';txt=prev.text+' '+t;
    }
    unl=txt;
    headings.push({kind:'unlabelled',level:3,text:txt,page:l.page});
    events.push({type:'heading',level:3,text:txt});
    continue;
  }
  l.kind='paragraph';
  cur.lines.push({page:l.page,text:t,suspect:inSus,trigger:reason,src:l});
}
const HYPH=[];
paras.forEach(p=>{
  p.text=p.lines.map(x=>x.text).join(' ').replace(/\s+/g,' ').trim();
  p.words=p.text?p.text.split(/\s+/).length:0;
  p.page_start=p.lines.length?p.lines[0].page:p.startPage;
  p.page_end=p.lines.length?p.lines[p.lines.length-1].page:p.startPage;
  p.suspectLines=p.lines.filter(x=>x.suspect);
  p.reasons=[];
  p.lines.forEach(x=>{if(x.trigger&&p.reasons.indexOf(x.trigger)<0)p.reasons.push(x.trigger);if(/-$/.test(x.text))HYPH.push(p.number);});
  p.over=p.words>300;
  if(p.over)p.reasons.push('paragraph over 300 words');
  p.flagged=p.suspectLines.length>0||p.over;
  p.found=firstWords(p.text);
  p.ref=refFW&&refFW[String(p.number)]!=null?String(refFW[String(p.number)]):null;
  p.fwMatch=p.ref==null?null:normQ(p.found)===normQ(p.ref);
  p.citation=symbol+', para. '+p.number;
  p.firstLine=(function(){const t=p.text;if(t.length<=120)return t;const c=t.slice(0,120);const s=c.lastIndexOf(' ');return (s>60?c.slice(0,s):c)+'…';})();
  p.pageLabel=p.page_start===p.page_end?String(p.page_start):p.page_start+'–'+p.page_end;
});
const flagged=paras.filter(p=>p.flagged);
const flagPages=[...new Set(flagged.map(p=>p.page_end))];
const suspectTotal=paras.reduce((a,p)=>a+p.suspectLines.length,0);
const suspectPages=new Set();paras.forEach(p=>p.suspectLines.forEach(x=>suspectPages.add(x.page)));
const suspectParas=paras.filter(p=>p.suspectLines.length);
function records(){
  return paras.map(p=>({
    symbol:symbol,paragraph:p.number,section:p.section,part:p.part||'',
    page_start:p.page_start,page_end:p.page_end,text:p.text,
    text_lines:p.lines.map(x=>x.text).join(' | '),
    flagged:p.flagged,first_words_match:p.fwMatch,citation:p.citation,doc_url:D.doc_url||'',
    limitations:p.flagged?'footnotes not separated; '+p.suspectLines.length+' may sit inside this paragraph':'footnotes not separated'
  }));
}
const q=s=>'"'+String(s==null?'':s).replace(/"/g,'\\"')+'"';
function mdFront(today){
  return '---\ntitle: '+q(D.title)+'\nsymbol: '+q(symbol)+'\nadopted: '+q(ref.adopted||'')+'\nsource_url: '+q(D.doc_url||'')+'\nextracted: '+today+'\nparagraphs_found: '+paras.length+'\nparagraphs_expected: '+(refParas==null?'unknown':refParas)+'\nparagraphs_flagged: '+flagged.length+'\nfootnotes: '+q('not separated; the document has '+(refFoot==null?'an unknown number':refFoot))+'\n---\n\n';
}
function mdBody(){
  let o='';
  events.forEach(e=>{
    if(e.type==='heading')o+=(e.level===2?'## ':'### ')+e.text+'\n\n';
    else o+='**'+e.p.number+'.** '+e.p.text+(e.p.flagged?' (flagged: may contain footnote text)':'')+'\n\n';
  });
  return o;
}
/* checks */
const checks=[];
const nums=paras.map(p=>p.number);
checks.push({name:'Paragraph count',
  story:'Given the converter text of '+pages.length+' pages, having run the paragraph rule, we expect as many numbered paragraphs as the reference lists.',
  got:'found '+paras.length+' · reference '+(refParas==null?'none':refParas),
  status:refParas==null?'notrun':(paras.length===refParas?'pass':'fail'),rows:[]});
const numIssues=[];let prevN=0;
paras.forEach(p=>{if(p.number!==prevN+1)numIssues.push('para. '+p.number+' (page '+p.page_start+') follows '+prevN);prevN=p.number;});
checks.push({name:'Numbering',story:'Given the paragraphs in page order, we expect exactly 1 to n with no gap or duplicate.',
  got:numIssues.length?numIssues.length+' problem(s)':(paras.length?'1 to '+paras.length+' in order':'no paragraphs'),
  status:paras.length&&!numIssues.length?'pass':'fail',detail:numIssues,rows:numIssues.length&&paras.length?[paras[0].number]:[]});
const fwBad=[];
if(refFW){
  paras.forEach(p=>{if(p.fwMatch===false)fwBad.push({n:p.number,found:p.found,ref:p.ref});});
  const have=new Set(nums.map(String));
  Object.keys(refFW).forEach(k=>{if(!have.has(k))fwBad.push({n:Number(k),found:null,ref:refFW[k]});});
}
const fwOK=paras.filter(p=>p.fwMatch===true).length;
checks.push({name:'First words',story:'Given the first six words of each paragraph (footnote marks removed, quotes and dashes normalised), we expect each to equal the reference.',
  got:refFW?fwBad.length+' differ · '+fwOK+' match':'no reference',
  status:refFW?(fwBad.length?'fail':'pass'):'notrun',rows:fwBad.filter(x=>x.found!=null).slice(0,1).map(x=>x.n)});
checks.push({name:'Paragraphs flagged',story:'Given the rule for suspect lines, we expect footnote text may sit in the paragraph that runs at the foot of a page.',
  got:flagged.length+' paragraphs flagged on '+flagPages.length+' pages, to check against the PDF',status:'info',rows:flagged.length?[flagged[0].number]:[]});
checks.push({name:'Suspect lines',story:'Given lines that look like footnotes, we expect them counted, not removed.',
  got:suspectTotal+' suspect lines on '+suspectPages.size+' pages, in '+suspectParas.length+' paragraphs; none removed',status:'info',rows:suspectParas.length?[suspectParas[0].number]:[]});
const hdrN=pageInfo.filter(x=>x.header).length,pnN=pageInfo.filter(x=>x.pageNumber).length;
const disp=[];pageInfo.forEach(x=>x.displaced.forEach(n=>disp.push('page '+x.page+': '+n)));
checks.push({name:'Headers and footers',story:'Given each page, we expect the symbol on its first line (all pages) and a page number in the footer (all but the first).',
  got:hdrN+' of '+pages.length+' pages with symbol header · '+pnN+' with page number · '+disp.length+' bare numbers removed from the footer',
  status:pages.length&&hdrN===pages.length&&pnN>=pages.length-1?'pass':'fail',detail:disp.length?['Removed: '+disp.join('; ')]:[],rows:[]});
const lab=headings.filter(h=>h.kind==='labelled'),unlab=headings.filter(h=>h.kind==='unlabelled');
checks.push({name:'Headings',story:'Given heading rules, we expect section titles kept out of paragraph text.',
  got:lab.length+' labelled, '+unlab.length+' unlabelled',status:'info',
  detail:unlab.map(h=>'Unlabelled (page '+h.page+'): '+h.text),rows:[]});
checks.push({name:'Hyphenated line ends',story:'Given lines ending with a hyphen, we expect none, so no hyphen joining is done.',
  got:HYPH.length+' lines',status:'info',rows:[]});
const kinds={};all.forEach(l=>{if(l.kind!=='blank'){const k=l.kind||'unclassified';kinds[k]=(kinds[k]||0)+1;}});
const unclassified=all.filter(l=>l.kind===null);
const classified=['cover','header','heading','paragraph','footer'].reduce((a,k)=>a+(kinds[k]||0),0);
checks.push({name:'Nothing lost',story:'Given every non-empty line, we expect each to be cover, header, heading, paragraph or footer exactly once.',
  got:totalNonEmpty+' non-empty lines · cover '+(kinds.cover||0)+', header '+(kinds.header||0)+', heading '+(kinds.heading||0)+', paragraph '+(kinds.paragraph||0)+', footer '+(kinds.footer||0)+' = '+classified,
  status:classified===totalNonEmpty&&!unclassified.length?'pass':'fail',
  detail:unclassified.map(l=>'Unclassified on page '+l.page+': '+l.text),rows:[]});
let rt=-1;try{rt=JSON.parse(JSON.stringify(records())).length;}catch(e){}
checks.push({name:'Export round trip',story:'Given the JSON to download, parsed back, we expect as many records as the table has rows.',
  got:rt+' records parsed · '+paras.length+' rows',status:rt===paras.length?'pass':'fail',rows:[]});
const cPass=checks.filter(c=>c.status==='pass').length,cFail=checks.filter(c=>c.status==='fail').length;
return {D,symbol,ref,refParas,refFoot,refFW,pages,paras,headings,events,flagged,flagPages,suspectTotal,warnings,checks,cPass,cFail,cTot:cPass+cFail,fwBad,fwOK,records,mdFront,mdBody,pageInfo};
}

const AN=DOCS.map(analyze);
const SOURCE=TEN.source||'';
const S={tab:1,sel:0,open:new Set(),pdf:new Set(),checks:false,flags:false,heads:false,focus:null,copied:null};
const $=id=>document.getElementById(id);
const fileSafe=s=>(s||'document').replace(/\//g,'-');
function download(name,type,content){
  const url=URL.createObjectURL(new Blob([content],{type:type+';charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}
const today=()=>new Date().toISOString().slice(0,10);

function head(){
  const A=AN[S.sel];
  const totFail=AN.reduce((a,x)=>a+x.cFail,0);
  if(!A){$('title').textContent='No documents in this file';$('meta').textContent='';$('status').textContent='';return;}
  $('title').textContent=A.D.title||'No title';
  $('meta').innerHTML=(A.D.doc_url?'<a href="'+esc(A.D.doc_url)+'" target="_blank" rel="noopener">'+esc(A.symbol)+'</a>':esc(A.symbol))+' · adopted '+esc(A.ref.adopted||'unknown')+' · '+A.pages.length+' pages · '+esc(SOURCE);
  $('status').innerHTML='<div><span class="dot '+(A.cFail?'r':'g')+'"></span>'+(A.cFail?'<b class="red">'+A.cFail+' check'+(A.cFail>1?'s':'')+' failed</b>':'<b class="ok">'+A.cPass+' of '+A.cTot+' checks pass</b>')+'</div><div>'+A.flagged.length+' paragraphs flagged</div><div class="hint">all '+AN.length+' documents: '+totFail+' failed checks</div>';
  $('foot').innerHTML=esc(SOURCE)+(TEN.built?' · built '+esc(TEN.built):'')+' · Done by this page\'s code; no model was called and nothing left the browser.';
}
function rail(){
  let h='<div class="mono">Documents ('+AN.length+')</div><ul class="docs">';
  AN.forEach((A,i)=>{
    const okp=A.refParas!=null&&A.paras.length===A.refParas;
    h+='<li><button class="docbtn" data-act="sel" data-i="'+i+'" data-key="s'+i+'" aria-current="'+(i===S.sel)+'"><b>'+esc(A.symbol)+'</b><span class="'+(okp?'ok':'bad')+'">'+A.paras.length+' of '+(A.refParas==null?'?':A.refParas)+' paragraphs</span><br><span class="'+(A.cFail?'bad':'ok')+'">'+A.cPass+' of '+A.cTot+' checks pass</span></button></li>';
  });
  h+='</ul>';
  const A=AN[S.sel];
  if(A){
    const eq=A.refParas!=null&&A.paras.length===A.refParas;
    const pct=A.refParas?Math.min(100,A.paras.length/A.refParas*100):0;
    h+='<div class="rl"><div class="big">'+A.paras.length+'</div><div class="hint">paragraphs of '+(A.refParas==null?'(no reference)':A.refParas)+'</div><div class="bar'+(eq?'':' bad')+'"><i style="width:'+pct+'%"></i></div></div>'
    +'<div class="rl"><div class="big '+(A.flagged.length?'red':'')+'">'+A.flagged.length+'</div><div class="hint">paragraphs flagged of the '+A.paras.length+' found: footnote text may sit inside: check them against the PDF</div></div>';
  }
  $('rail').innerHTML=h;
}
function tile(label,big,sub,how,cls){
  return '<div class="tile"><div class="mono">'+label+'</div><div class="big '+(cls||'')+'">'+big+'</div><div>'+sub+'</div><div class="how"><b>How this is computed:</b> '+how+'</div></div>';
}
function statusHtml(c){
  return c.status==='pass'?'<span class="st ok">pass</span>':c.status==='fail'?'<span class="st bad">check failed</span>':c.status==='info'?'<span class="st">for information</span>':'<span class="st">not run</span>';
}
function p1(){
  const A=AN[S.sel];
  if(!A){$('p1').innerHTML='<p class="bad">No documents.</p>';return;}
  if(!A.paras.length){$('p1').innerHTML='<h2 class="q">Did the app find everything the document has?</h2><p class="bad">No numbered paragraph was found in '+esc(A.symbol)+'. Exports are disabled.</p>';return;}
  const diff=A.refParas==null?null:A.paras.length-A.refParas;
  let h='<h2 class="q">Did the app find everything '+esc(A.symbol)+' has?</h2><div class="tiles">';
  h+=tile('Paragraphs found',A.paras.length,A.refParas==null?'no reference in this file':'the document has '+A.refParas+(diff===0?' · <span class="ok">equal</span>':' · <span class="bad">difference '+(diff>0?'+':'')+diff+'</span>'),'lines starting with a number and a full stop are paragraph starts, over all pages in order.',diff===0?'ok':(diff==null?'':'red'));
  h+=tile('First words match',A.refFW?A.fwOK:'–',A.refFW?'of '+(A.refParas==null?A.paras.length:A.refParas):'no reference in this file','first six words of each paragraph, footnote marks removed, against reference.first_words.',A.refFW&&A.fwBad.length?'red':'');
  h+=tile('Paragraphs flagged',A.flagged.length,'of the '+A.paras.length+' found, on '+A.flagPages.length+' pages'+(A.flagged.length?'<br><span class="red">footnote text may sit inside these paragraphs: check them against the PDF</span>':''),'a paragraph with a footnote-looking line, or over 300 words.',A.flagged.length?'red':'');
  h+=tile('Footnotes','<span style="font-size:34px">not separated</span>','the document has '+(A.refFoot==null?'an unknown number':A.refFoot)+'; this version leaves them in place and flags them','nothing is removed; suspect lines stay in the text.','');
  h+='</div>';
  if(A.fwBad.length){
    h+='<div class="sec"><div class="mono">First words differ</div>';
    A.fwBad.slice(0,10).forEach(x=>{h+='<div class="hl"><b class="red">para. '+x.n+'</b>: found '+(x.found==null?'(paragraph not found)':esc(x.found))+' / reference '+esc(x.ref)+'</div>';});
    if(A.fwBad.length>10)h+='<div class="hl">and '+(A.fwBad.length-10)+' more</div>';
    h+='</div>';
  }
  h+='<div class="sec"><h2 class="q">Take the paragraphs away</h2><div class="hint" style="margin-bottom:8px">This document only. Tab 03 downloads all ten.</div>'
   +'<button class="btn pri" data-act="dlJson">Download JSON</button><button class="btn" data-act="dlMd">Download Markdown</button></div>';
  h+='<div class="sec"><button class="hd" data-act="toggleChecks" data-key="tc" aria-expanded="'+S.checks+'">Every check ('+A.checks.length+')</button>';
  if(S.checks){
    h+='<ul class="chk">'+A.checks.map(c=>'<li><b>'+esc(c.name)+'</b> '+statusHtml(c)+'<div class="hint">'+esc(c.story)+'</div><div>'+esc(c.got)+'</div>'
      +(c.detail&&c.detail.length?'<div class="hint">'+c.detail.slice(0,12).map(esc).join('<br>')+(c.detail.length>12?'<br>and '+(c.detail.length-12)+' more':'')+'</div>':'')
      +(c.rows&&c.rows.length&&c.status!=='pass'?'<button class="linkbtn" data-act="jump" data-n="'+c.rows[0]+'">see rows</button>':'')+'</li>').join('')+'</ul>';
    if(A.warnings.length)h+='<div class="note">'+A.warnings.slice(0,12).map(esc).join('<br>')+(A.warnings.length>12?'<br>and '+(A.warnings.length-12)+' more':'')+'</div>';
  }
  h+='</div><div><button class="hd" data-act="toggleFlags" data-key="tf" aria-expanded="'+S.flags+'">Flagged paragraphs ('+A.flagged.length+')</button>';
  if(S.flags){
    h+='<div class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</div>';
    h+='<table><caption><span class="mono">TAB.01</span>'+A.flagged.length+' of '+A.paras.length+' paragraphs flagged</caption><thead><tr><th scope="col" class="n">Paragraph</th><th scope="col">Page</th><th scope="col" class="n">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>'
    +A.flagged.map(p=>'<tr class="r" data-act="jump" data-n="'+p.number+'"><td class="n"><button class="numbtn" data-act="jump" data-n="'+p.number+'">'+p.number+'</button></td><td>'+p.pageLabel+'</td><td class="n">'+p.suspectLines.length+'</td><td>'+esc(p.reasons.join('; '))+'</td></tr>').join('')
    +'</tbody></table>';
  }
  h+='</div>';
  $('p1').innerHTML=h;
}
function pdfLines(p){
  let h='<div class="lines">',pg=null;
  p.lines.forEach(x=>{
    if(x.page!==pg){pg=x.page;h+='<div class="pg">— page '+pg+' begins —</div>';}
    h+='<div>'+esc(x.text)+'</div>';
  });
  return h+'</div>';
}
function p2(){
  const A=AN[S.sel];
  if(!A){$('p2').innerHTML='';return;}
  let h='<h2 class="q">What does each paragraph of '+esc(A.symbol)+' say, and how do I cite it?</h2>';
  h+='<button class="hd" data-act="toggleHeads" data-key="th" aria-expanded="'+S.heads+'">Headings found: '+A.headings.length+'</button>';
  if(S.heads)h+='<ul class="chk">'+A.headings.map(x=>'<li><span class="mono">'+(x.kind==='labelled'?(x.level===2?'section':'subsection'):'unlabelled')+' · page '+x.page+'</span><br>'+esc(x.text)+'</li>').join('')+'</ul>';
  if(!A.paras.length){$('p2').innerHTML=h+'<p class="bad">No paragraph found.</p>';return;}
  h+='<table style="margin-top:14px"><caption><span class="mono">TAB.02</span>'+A.paras.length+' paragraphs found'+(A.refParas==null?'':', '+A.refParas+' expected')+'</caption><thead><tr><th scope="col" class="n">No.</th><th scope="col">Section</th><th scope="col">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody>';
  A.paras.forEach(p=>{
    const open=S.open.has(p.number);
    const ck=[];
    if(p.fwMatch===false)ck.push('<span class="bad">first words differ</span>');
    if(p.flagged)ck.push('<span class="bad">may contain footnote text</span>');
    h+='<tr class="r" id="row-'+p.number+'" data-act="row" data-n="'+p.number+'"><td class="n"><button class="numbtn" data-act="row" data-n="'+p.number+'" data-key="r'+p.number+'" aria-expanded="'+open+'">'+p.number+'</button></td><td>'+esc(p.section)+'</td><td>'+p.pageLabel+'</td><td>'+esc(p.firstLine)+'</td><td>'+(ck.length?ck.join('<br>'):(p.fwMatch===null?'not compared':'OK'))+'</td></tr>';
    if(open){
      const txt=p.lines.map(x=>x.suspect?'<span class="sus">'+esc(x.text)+'</span>':esc(x.text)).join(' ');
      const pdfOn=S.pdf.has(p.number);
      h+='<tr class="detail"><td colspan="5"><div class="mono">'+esc(p.path||'(no heading)')+'</div><div class="ptext">'+txt+'</div>'
       +(p.suspectLines.length?'<div class="hint red">Boxed lines look like footnote text or a footer; they are kept in the text.</div>':'')
       +'<div class="hint">Found first words: <b>'+esc(p.found)+'</b> · Reference: <b>'+(p.ref==null?'none':esc(p.ref))+'</b></div>'
       +'<div style="margin-top:8px"><button class="btn" data-act="copy" data-n="'+p.number+'" data-key="c'+p.number+'">'+(S.copied===p.number?'Copied':'Copy citation')+'</button>'
       +'<button class="btn" data-act="pdf" data-n="'+p.number+'" data-key="p'+p.number+'" aria-expanded="'+pdfOn+'">Show the PDF\'s lines</button></div>'
       +(pdfOn?pdfLines(p):'')+'</td></tr>';
    }
  });
  h+='</tbody></table>';
  $('p2').innerHTML=h;
}
function p3(){
  const totP=AN.reduce((a,x)=>a+x.paras.length,0);
  let h='<h2 class="q">How did the same rules do on each document?</h2>';
  h+='<table><caption><span class="mono">TAB.03</span>'+AN.length+' documents, '+totP+' paragraphs found in all</caption><thead><tr><th scope="col">Symbol</th><th scope="col">Committee</th><th scope="col" class="n">Year</th><th scope="col" class="n">Found</th><th scope="col" class="n">Expected</th><th scope="col" class="n">First words match</th><th scope="col" class="n">Flagged</th><th scope="col" class="n">Checks passed</th></tr></thead><tbody>';
  AN.forEach((A,i)=>{
    const cOk=A.refParas!=null&&A.paras.length===A.refParas;
    const fOk=A.refFW&&A.fwBad.length===0;
    h+='<tr class="r'+(i===S.sel?' cur':'')+'" data-act="sel" data-i="'+i+'"><td>'+(A.D.doc_url?'<a href="'+esc(A.D.doc_url)+'" target="_blank" rel="noopener">'+esc(A.symbol)+'</a>':esc(A.symbol))+(i===S.sel?' <span class="hint">(selected)</span>':'')+'</td><td>'+esc(A.D.committee||'')+'</td><td class="n">'+esc(A.D.year==null?'':A.D.year)+'</td>'
    +'<td class="n '+(cOk?'':'bad')+'">'+A.paras.length+'</td><td class="n">'+(A.refParas==null?'–':A.refParas)+'</td>'
    +'<td class="n '+(fOk?'':(A.refFW?'bad':''))+'">'+(A.refFW?A.fwOK:'–')+'</td><td class="n">'+A.flagged.length+'</td>'
    +'<td class="n '+(A.cFail?'bad':'')+'">'+A.cPass+' of '+A.cTot+'</td></tr>';
  });
  h+='</tbody></table><div class="hint">Red = fails its check (count differs from the reference, first words differ, or a check failed). Flagged is not a failure. Click a row to select the document for tabs 01 and 02.</div>';
  h+='<div class="sec"><h2 class="q">Take all '+AN.length+' documents away</h2><div class="hint" style="margin-bottom:8px">One file with every paragraph of every document, each record with its symbol.</div>'
   +'<button class="btn pri" data-act="dlAllJson"'+(totP?'':' disabled')+'>Download all as JSON</button><button class="btn" data-act="dlAllMd"'+(totP?'':' disabled')+'>Download all as Markdown</button></div>';
  $('p3').innerHTML=h;
}
function tabs(){
  [1,2,3].forEach(n=>{
    const t=$('t'+n),on=S.tab===n;
    t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;$('p'+n).hidden=!on;
  });
}
function render(){
  head();rail();p1();p2();p3();tabs();
  if(S.focus){const e=document.querySelector('[data-key="'+S.focus+'"]');if(e)e.focus();S.focus=null;}
}
function select(i){S.sel=i;S.open=new Set();S.pdf=new Set();S.copied=null;}
function jump(n){
  S.tab=2;S.open.add(n);S.focus='r'+n;render();
  const r=$('row-'+n);if(r)r.scrollIntoView({block:'center'});
}
function copyText(s,cb){
  const fb=()=>{const ta=document.createElement('textarea');ta.value=s;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');}catch(e){}ta.remove();cb();};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(s).then(cb,fb);else fb();
}
document.addEventListener('click',e=>{
  const t=e.target.closest('[data-tab]');
  if(t){S.tab=Number(t.dataset.tab);render();return;}
  const a=e.target.closest('[data-act]');
  if(!a||e.target.closest('a'))return;
  const act=a.dataset.act,n=Number(a.dataset.n),A=AN[S.sel];
  if(act==='sel'){select(Number(a.dataset.i));S.focus=a.tagName==='BUTTON'?'s'+a.dataset.i:null;render();}
  else if(act==='toggleChecks'){S.checks=!S.checks;S.focus='tc';render();}
  else if(act==='toggleFlags'){S.flags=!S.flags;S.focus='tf';render();}
  else if(act==='toggleHeads'){S.heads=!S.heads;S.focus='th';render();}
  else if(act==='row'){if(S.open.has(n))S.open.delete(n);else S.open.add(n);S.focus='r'+n;render();}
  else if(act==='pdf'){if(S.pdf.has(n))S.pdf.delete(n);else S.pdf.add(n);S.focus='p'+n;render();}
  else if(act==='jump'){jump(n);}
  else if(act==='copy'){
    const p=A.paras.find(x=>x.number===n);
    copyText(p.citation,()=>{S.copied=n;S.focus='c'+n;render();setTimeout(()=>{if(S.copied===n){S.copied=null;render();}},2000);});
  }
  else if(act==='dlJson'&&A.paras.length)download(fileSafe(A.symbol)+'.json','application/json',JSON.stringify(A.records(),null,2));
  else if(act==='dlMd'&&A.paras.length)download(fileSafe(A.symbol)+'.md','text/markdown',A.mdFront(today())+A.mdBody());
  else if(act==='dlAllJson'){
    const rec=[];AN.forEach(x=>x.records().forEach(r=>rec.push(r)));
    download('general-comments-all.json','application/json',JSON.stringify(rec,null,2));
  }
  else if(act==='dlAllMd'){
    const tp=AN.reduce((s,x)=>s+x.paras.length,0);
    let o='---\ntitle: "'+String(TEN.title||'General Comments').replace(/"/g,'\\"')+'"\nsource: "'+String(SOURCE).replace(/"/g,'\\"')+'"\nextracted: '+today()+'\ndocuments: '+AN.length+'\nparagraphs_found: '+tp+'\nfootnotes: "not separated; flagged paragraphs may contain footnote text"\n---\n\n';
    AN.forEach(x=>{
      o+='# '+x.symbol+(x.D.title?': '+x.D.title:'')+'\n\n'
       +'*'+x.paras.length+' paragraphs found, '+(x.refParas==null?'unknown number':x.refParas)+' expected; '+x.flagged.length+' flagged; '+(x.D.doc_url||'')+'*\n\n'+x.mdBody();
    });
    download('general-comments-all.md','text/markdown',o);
  }
});
document.querySelector('[role=tablist]').addEventListener('keydown',e=>{
  let n=null;
  if(e.key==='ArrowRight')n=S.tab%3+1;
  else if(e.key==='ArrowLeft')n=((S.tab+1)%3)+1;
  else if(e.key==='Home')n=1;else if(e.key==='End')n=3;
  if(n){e.preventDefault();S.tab=n;render();$('t'+n).focus();}
});
render();
})();
</script>
</body>
</html>
```