I built the app on the converter's text of the document you attached. It runs once on load and shows two tabs, the result and the paragraphs, with every check and the flagged pages one click deeper. Nothing is typed in by hand, and no model is called.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraphs out of a PDF</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
[hidden]{display:none!important}
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1f6b3a;--mute:#5c564c}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
a{color:var(--ink)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
button{font:inherit;color:inherit;cursor:pointer}
header{padding:18px 24px 12px;border-bottom:1px solid var(--rule);display:flex;gap:24px;justify-content:space-between;flex-wrap:wrap}
header h1{font-family:Georgia,"Times New Roman",serif;font-weight:normal;font-size:26px;margin:2px 0 4px;line-height:1.2}
header .meta{color:var(--mute);font-size:14px}
.status{text-align:right;font-size:14px}
.dot{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.ok{color:var(--green)}.bad{color:var(--red)}
.layout{display:grid;grid-template-columns:250px 1fr;min-height:60vh}
.rail{border-right:1px solid var(--rule);padding:18px 20px}
.rail .card{border-top:1px solid var(--ink);border-bottom:1px solid var(--rule);padding:8px 0;margin:6px 0 18px}
.rail .card .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px}
.rail .card .short{font-size:14px;color:var(--mute)}
.big{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1.05}
.rail .big{font-size:42px}
.bar{height:5px;background:var(--rule);margin:6px 0 4px}.bar i{display:block;height:5px;background:var(--red)}
.bar.good i{background:var(--green)}
.hint{color:var(--mute);font-size:13px}
.rail section{margin-bottom:18px}
main{padding:0 24px 24px;min-width:0}
[role=tablist]{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin-bottom:18px}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;padding:12px 14px 9px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
[role=tab][aria-selected=true]{border-bottom-color:var(--red);color:var(--red);font-weight:bold}
h2.q{font-family:Georgia,"Times New Roman",serif;font-weight:normal;font-size:22px;margin:0 0 14px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:1px solid var(--ink)}
.tile{padding:14px 18px 14px 0;border-bottom:1px solid var(--rule)}
.tile:nth-child(even){padding-left:18px;border-left:1px solid var(--rule)}
.tile .big{margin:4px 0}
.tile .sub{font-size:15px}
.how{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;color:var(--mute);margin-top:6px}
.take{margin-top:24px;border-top:1px solid var(--ink);padding-top:10px}
.btn{background:transparent;border:1px solid var(--ink);padding:8px 14px;margin:6px 8px 6px 0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.btn:hover:not(:disabled){background:var(--ink);color:var(--paper)}
.btn:disabled{opacity:.45;cursor:not-allowed}
.fold{margin-top:18px;border-top:1px solid var(--rule)}
.foldbtn{display:flex;width:100%;justify-content:space-between;background:none;border:0;border-bottom:1px solid var(--rule);padding:11px 2px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;text-align:left}
.foldbtn[aria-expanded=true]{color:var(--red)}
.foldbtn::after{content:"+"}.foldbtn[aria-expanded=true]::after{content:"–"}
.foldpanel{padding:10px 0 4px}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{font-family:Georgia,"Times New Roman",serif;font-size:18px;text-align:left;padding:4px 0 8px}
caption .mono{color:var(--mute);margin-right:8px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.07em;text-transform:uppercase;text-align:left;border-bottom:1px solid var(--ink);padding:6px 8px;color:var(--mute)}
td{border-bottom:1px solid var(--rule);padding:7px 8px;vertical-align:top}
.num{text-align:right}
tr[data-p],tr[data-fp]{cursor:pointer}
tr[data-p]:hover td,tr[data-fp]:hover td{background:#ece6d9}
.rowbtn{background:none;border:0;padding:0;color:var(--red);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px;font-weight:bold}
.detail td{background:#faf7f0;padding:12px 14px}
.detail .path{color:var(--mute);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;margin-bottom:8px}
.ptext{max-width:75ch;font-size:16px;line-height:1.6}
.sus{border:1px solid var(--red);padding:0 2px}
.cmp{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;margin:10px 0}
pre.lines{background:#fff;border:1px solid var(--rule);padding:8px;white-space:pre-wrap;font:12px/1.5 ui-monospace,Menlo,Consolas,monospace;max-height:340px;overflow:auto}
pre.lines .pg{color:var(--red)}
pre.lines .dim{color:#8a8376}
ul.checks{list-style:none;margin:0;padding:0}
ul.checks li{border-bottom:1px solid var(--rule);padding:9px 0}
.st{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;text-transform:uppercase;letter-spacing:.06em;font-weight:bold}
.st.pass{color:var(--green)}.st.fail{color:var(--red)}
.linkbtn{background:none;border:0;padding:0;text-decoration:underline;color:var(--ink);font-size:13px}
.note{font-size:14px;margin:0 0 10px}
.mm{list-style:none;padding:0;margin:14px 0 0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.mm li{border-bottom:1px solid var(--rule);padding:4px 0}
footer{border-top:1px solid var(--rule);padding:14px 24px;color:var(--mute);font-size:13px}
.hl{margin:0;padding:0;list-style:none}.hl li{padding:3px 0;border-bottom:1px solid var(--rule);font-size:14px}
@media(max-width:820px){.layout{grid-template-columns:1fr}.rail{border-right:0;border-bottom:1px solid var(--rule)}.tiles{grid-template-columns:1fr}.tile:nth-child(even){padding-left:0;border-left:0}.status{text-align:left}}
</style>
</head>
<body>
<header>
  <div>
    <div class="mono" style="color:var(--mute)">UN document · PDF text</div>
    <h1 id="h-title"></h1>
    <div class="meta" id="h-meta"></div>
  </div>
  <div class="status" id="h-status"></div>
</header>
<div class="layout">
  <aside class="rail" aria-label="Document summary" id="rail"></aside>
  <main>
    <div role="tablist" aria-label="Views" id="tabs">
      <button role="tab" id="tab0" aria-selected="true" aria-controls="panel0" tabindex="0">01 Result</button>
      <button role="tab" id="tab1" aria-selected="false" aria-controls="panel1" tabindex="-1">02 Paragraphs</button>
    </div>
    <div role="tabpanel" id="panel0" aria-labelledby="tab0"></div>
    <div role="tabpanel" id="panel1" aria-labelledby="tab1" hidden></div>
  </main>
</div>
<footer id="foot"></footer>

<script>
(function(){
const D = window.WORKSHOP_DATA || {};
const DOC = D.pdf_text || {};
const REF = DOC.reference || null;
const symbol = DOC.symbol || '';
const recs = (Array.isArray(DOC.records)?DOC.records:[]).slice().sort((a,b)=>a.page-b.page);
const esc = s => String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const START1=/^(\d{1,3})\.$/, START2=/^(\d{1,3})\. (.+)$/, LABEL=/^([IVX]+|[A-Z])\.$/;
const isStart = t => START1.test(t)||START2.test(t);
const isSuspectLine = t => /^\d{1,3}$/.test(t) || /^\d{1,3} [A-Z“"‘']/.test(t) || /^\* /.test(t);
const collapse = s => s.replace(/\s+/g,' ').trim();
const norm = s => collapse(String(s).replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[–—]/g,'-'));

/* ---------- 1. pages: header and footer ---------- */
const pages=[]; let totalNonEmpty=0; const headerWarn=[];
recs.forEach(r=>{
  const raw=String(r.text||'').replace(/\r/g,'').split('\n');
  const lines=raw.map((t,i)=>({page:r.page,i,t:t.trim(),kind:t.trim()?'?':'blank',foot:false}));
  totalNonEmpty+=lines.filter(l=>l.t).length;
  const pi={page:r.page,header:false,pageNo:false,displaced:[],lines};
  const f=lines.findIndex(l=>l.t);
  if(f>=0 && lines[f].t===symbol){lines[f].kind='header';pi.header=true;} else headerWarn.push(r.page);
  for(let e=lines.length-1;e>=0;e--){
    const l=lines[e],t=l.t;
    if(l.kind==='header')break;
    if(t===''||/^GE\./.test(t)||/^\d{6}(\s+\d{6})*$/.test(t)||/^\d{1,3}$/.test(t)){
      l.foot=true;
      if(t){l.kind='footer';
        if(/^\d{1,3}$/.test(t)){ if(+t===r.page)pi.pageNo=true; else pi.displaced.push(t); } }
    } else break;
  }
  pages.push(pi);
});
const body=[]; pages.forEach(p=>p.lines.forEach(l=>{ if(l.kind!=='header'&&!l.foot) body.push(l); }));

/* ---------- 2. footnote zones ---------- */
(function(){
  let started=false,zone=false,lastPage=null;
  body.forEach(l=>{
    if(!l.t){l.zone=zone;return;}
    if(l.page!==lastPage){zone=false;lastPage=l.page;}
    if(isStart(l.t)){started=true;zone=false;l.suspect=false;}
    else if(LABEL.test(l.t)){started=true;zone=false;l.suspect=false;}
    else{ if(started&&isSuspectLine(l.t))zone=true; l.suspect=zone&&started; }
    l.zone=zone;
  });
})();

/* ---------- 3. paragraphs and headings ---------- */
const paras=[],heads=[],unclassified=[];
(function(){
  const nextNE=i=>{let k=i;while(k<body.length&&!body[k].t)k++;return k;};
  const headTest=t=>t.length<=90&&/^[A-Z]/.test(t)&&!/[.;:,0-9]$/.test(t)&&!/\.[”’"]$/.test(t)&&!isStart(t)&&!LABEL.test(t)&&!isSuspectLine(t);
  const canHead=(l,nx)=>headTest(l.t)&&!l.suspect&&!(l.zone&&nx&&l.page!==nx.page);
  let cur=null,phase='cover',part=null,sub=null,unl=null,section=null;
  for(let i=0;i<body.length;i++){
    const l=body[i]; if(!l.t)continue;
    let m=START1.exec(l.t)||START2.exec(l.t);
    if(m){
      cur={number:+m[1],lines:[],startPage:l.page,section:section,part:part,path:[part,sub,unl].filter(Boolean).join(' › ')};
      paras.push(cur);phase='body';l.kind='paragraph';
      if(m[2])cur.lines.push({t:m[2],page:l.page,suspect:false});
      continue;
    }
    if(LABEL.test(l.t)){
      phase='body';l.kind='heading';
      const label=l.t.slice(0,-1);const parts=[];let j=i+1;
      while(j<body.length){
        const x=body[j];
        if(!x.t){
          let k=j+1;while(k<body.length&&!body[k].t)k++;
          if(!parts.length){j++;continue;}
          if(k<body.length&&/^[a-z(]/.test(body[k].t)){j=k;continue;}
          break;
        }
        if(isStart(x.t)||LABEL.test(x.t))break;
        parts.push(x.t);x.kind='heading';j++;
      }
      const text=collapse(parts.join(' '));const roman=/^[IVX]+$/.test(label);
      const full=label+'. '+text;
      if(roman){part=full;sub=null;unl=null;}else{sub=full;unl=null;}
      section=full;
      heads.push({level:roman?1:2,label,text,full,before:paras.length,page:l.page});
      i=j-1;continue;
    }
    if(phase==='cover'){l.kind='cover';continue;}
    const n1=nextNE(i+1),nx=body[n1];
    let hd=null,span=1;
    if(nx&&canHead(l,nx)&&isStart(nx.t)){hd=l.t;}
    else if(nx&&n1===i+1&&canHead(l,nx)){
      const n2=nextNE(n1+1),nx2=body[n2];
      if(nx2&&canHead(nx,nx2)&&isStart(nx2.t)){hd=l.t+' '+nx.t;span=2;}
    }
    if(hd){
      body[i].kind='heading'; if(span===2)body[i+1].kind='heading';
      unl=collapse(hd);section=unl;
      heads.push({level:3,label:'',text:unl,full:unl,before:paras.length,page:l.page});
      i+=span-1;continue;
    }
    if(!cur){l.kind='unclassified';unclassified.push(l);continue;}
    cur.lines.push({t:l.t,page:l.page,suspect:!!l.suspect});l.kind='paragraph';
  }
})();

/* ---------- 4. paragraph fields ---------- */
const ABBR=new Set(['no.','nos.','art.','arts.','para.','paras.','p.','pp.','vol.','sect.','cf.','e.g.','i.e.','ch.','chap.']);
function firstSix(text){
  const toks=text.split(/\s+/).filter(Boolean),out=[];
  for(let k=0;k<toks.length&&out.length<6;k++){
    let t=toks[k];
    if(/^\d{1,3}$/.test(t)&&out.length){const pv=out[out.length-1];if(/[.,”’"']$/.test(pv)&&!ABBR.has(pv.toLowerCase()))continue;}
    t=t.replace(/(?<=[A-Za-z.,;:”’"')])\d{1,3}$/,'');
    if(t==='')continue;
    out.push(t);
  }
  return out.join(' ');
}
const FW = REF && REF.first_words && typeof REF.first_words==='object' ? REF.first_words : null;
paras.forEach(p=>{
  p.text=collapse(p.lines.map(l=>l.t).join(' '));
  p.text_raw=p.lines.map(l=>l.t).join('\n');
  p.words=p.text?p.text.split(/\s+/).length:0;
  p.page_start=p.startPage;p.page_end=p.lines.length?p.lines[p.lines.length-1].page:p.startPage;
  p.suspectCount=p.lines.filter(l=>l.suspect).length;
  p.long=p.words>300;
  p.flagged=p.suspectCount>0||p.long;
  p.found=firstSix(p.text);
  p.ref=FW?FW[String(p.number)]:undefined;
  p.match=FW?(p.ref!==undefined&&norm(p.found)===norm(p.ref)):null;
  p.citation=symbol+', para. '+p.number;
  p.limitations=p.flagged?('footnotes not separated; '+(p.suspectCount||'some')+' line'+(p.suspectCount===1?'':'s')+' may sit inside this paragraph'):'footnotes not separated';
});
const paraHTML=p=>p.lines.map(l=>l.suspect?'<span class="sus">'+esc(l.t)+'</span>':esc(l.t)).join(' ');

/* ---------- 5. flagged pages ---------- */
const fpMap={};
function fp(page){return fpMap[page]||(fpMap[page]={page,paras:new Set(),suspect:0,reasons:new Set()});}
paras.forEach(p=>{
  p.lines.forEach(l=>{ if(l.suspect){const e=fp(l.page);e.paras.add(p.number);e.suspect++;
    e.reasons.add(/^\d{1,3}$/.test(l.t)?'bare number':/^\* /.test(l.t)?'starts with an asterisk':'starts with a number and a space');}});
  if(p.long){const e=fp(p.page_start);e.paras.add(p.number);e.reasons.add('paragraph over 300 words');}
});
const flaggedPages=Object.values(fpMap).sort((a,b)=>a.page-b.page);
const flaggedParas=paras.filter(p=>p.flagged);
const suspectTotal=paras.reduce((s,p)=>s+p.suspectCount,0);
const suspectPages=new Set();paras.forEach(p=>p.lines.forEach(l=>{if(l.suspect)suspectPages.add(l.page);}));
const suspectParas=paras.filter(p=>p.suspectCount>0).length;

/* ---------- 6. exports ---------- */
const today=new Date().toISOString().slice(0,10);
function exportRecords(){return paras.map(p=>({symbol,paragraph:p.number,section:p.section,part:p.part,page_start:p.page_start,page_end:p.page_end,text:p.text,text_lines:p.lines.map(l=>l.t).join(' | '),flagged:p.flagged,first_words_match:p.match,citation:p.citation,doc_url:DOC.doc_url||'',limitations:p.limitations}));}
function exportMarkdown(){
  const q=s=>JSON.stringify(String(s==null?'':s));
  const o=['---','title: '+q(DOC.title),'symbol: '+q(symbol),'adopted: '+q(REF&&REF.adopted),'source_url: '+q(DOC.doc_url),'extracted: '+today,
    'paragraphs_found: '+paras.length,'paragraphs_expected: '+(REF&&REF.paragraphs!=null?REF.paragraphs:'unknown'),'pages_flagged: '+flaggedPages.length,
    'footnotes: '+q('not separated; the document has '+(REF&&REF.footnotes!=null?REF.footnotes:'an unknown number')),'---',''];
  const hs=heads.slice();
  paras.forEach((p,idx)=>{
    hs.filter(h=>h.before===idx).forEach(h=>{o.push((h.level===1?'## ':'### ')+h.full,'');});
    o.push('**'+p.number+'.** '+p.text+(p.flagged?' (flagged: may contain footnote text)':''),'');
  });
  hs.filter(h=>h.before>=paras.length).forEach(h=>o.push((h.level===1?'## ':'### ')+h.full,''));
  return o.join('\n');
}
function download(name,mime,content){
  const b=new Blob([content],{type:mime+';charset=utf-8'});const u=URL.createObjectURL(b);
  const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1000);
}
const fileBase=(symbol||'document').replace(/\//g,'-');

/* ---------- 7. checks ---------- */
const checks=[];
const refP=REF&&REF.paragraphs!=null?REF.paragraphs:null;
const refF=REF&&REF.footnotes!=null?REF.footnotes:null;
const mism=FW?paras.filter(p=>!p.match):[];
checks.push(refP==null?{name:'Paragraph count',expect:'Given the reference, the app finds as many paragraphs as it states.',got:'no reference in this file',status:'notrun'}
 :{name:'Paragraph count',expect:'Given the converter text, having run the paragraph-start rule, we expect '+refP+' paragraphs.',got:paras.length+' found, '+refP+' expected',status:paras.length===refP?'pass':'fail',go:paras.length===refP?null:'para'});
(function(){
  const issues=[];let expected=1;
  paras.forEach(p=>{
    if(p.number===expected)expected++;
    else if(p.number<expected)issues.push('para '+p.number+' repeated or out of order (page '+p.page_start+')');
    else{issues.push('missing '+expected+(p.number-1>expected?'–'+(p.number-1):'')+' before para '+p.number+' (page '+p.page_start+')');expected=p.number+1;}
  });
  checks.push({name:'Numbering',expect:'Given the paragraphs found, we expect exactly 1 to n in order.',got:issues.length?issues.join('; '):'1 to '+paras.length+', no gaps or duplicates',status:issues.length?'fail':'pass',go:issues.length?'para':null});
})();
checks.push(!FW?{name:'First words',expect:'Given the reference, the first six words of each paragraph should match.',got:'no reference in this file',status:'notrun'}
 :{name:'First words',expect:'Given each paragraph text, after removing footnote marks, we expect its first six words to equal the reference.',got:mism.length+' differ of '+paras.length,status:mism.length?'fail':'pass',go:mism.length?'para':null});
checks.push({name:'Pages flagged',expect:'A flag is not a failure: the count can be right while footnote text sits inside a paragraph.',got:flaggedPages.length+' pages flagged, '+flaggedParas.length+' paragraphs to check against the PDF',status:'note',go:flaggedPages.length?'flagged':null});
checks.push({name:'Suspect lines',expect:'Lines that look like footnotes stay in the text.',got:suspectTotal+' suspect lines on '+suspectPages.size+' pages, in '+suspectParas+' paragraphs; none is removed',status:'note'});
const nPages=pages.length,hdrN=pages.filter(p=>p.header).length,pnN=pages.filter(p=>p.pageNo).length;
const displaced=[];pages.forEach(p=>p.displaced.forEach(d=>displaced.push(d+' (p. '+p.page+')')));
checks.push({name:'Headers and footers',expect:'Given every page, we expect the symbol first on all pages and a page number in the footer on all but the first.',
 got:hdrN+' of '+nPages+' pages start with the symbol; '+pnN+' pages have a page number in the footer; '+displaced.length+' bare numbers removed from the footer',
 detail:displaced.length?'Removed: '+displaced.join(', ')+'. The app does not put them back.':'',
 status:(hdrN===nPages&&pnN>=nPages-1)?'pass':'fail'});
const hyph=body.filter(l=>l.t&&/-$/.test(l.t)).length;
checks.push({name:'Hyphenated line ends',expect:'No hyphen joining is done.',got:hyph+' lines end with a hyphen',status:'note'});
const unlHeads=heads.filter(h=>h.level===3);
checks.push({name:'Headings',expect:'A reader can spot a paragraph last line mistaken for a heading.',got:heads.filter(h=>h.level<3).length+' labelled, '+unlHeads.length+' unlabelled',
 detail:unlHeads.length?'Unlabelled: '+unlHeads.map(h=>esc(h.text)+' (p. '+h.page+')').join('; '):'',detailHtml:true,status:'note'});
const kinds={header:0,footer:0,cover:0,heading:0,paragraph:0,unclassified:0};
pages.forEach(p=>p.lines.forEach(l=>{if(!l.t)return;const k=kinds[l.kind]!==undefined?l.kind:'unclassified';kinds[k]++;}));
const kSum=Object.values(kinds).reduce((a,b)=>a+b,0);
const uncl=[];pages.forEach(p=>p.lines.forEach(l=>{if(l.t&&kinds[l.kind]===undefined)uncl.push(l);}));
checks.push({name:'Nothing lost',expect:'Every non-empty line is classified exactly once.',
 got:'cover '+kinds.cover+' + header '+kinds.header+' + heading '+kinds.heading+' + paragraph '+kinds.paragraph+' + footer '+kinds.footer+' + unclassified '+kinds.unclassified+' = '+kSum+' of '+totalNonEmpty+' lines',
 detail:uncl.length?'Unclassified: '+uncl.map(l=>'p. '+l.page+': '+esc(l.t)).join(' | '):'',detailHtml:true,detailBad:true,
 status:(kSum===totalNonEmpty&&kinds.unclassified===0)?'pass':'fail'});
let rt=false;try{rt=JSON.parse(JSON.stringify(exportRecords())).length===paras.length;}catch(e){}
checks.push({name:'Export round trip',expect:'The JSON to download, parsed back, has as many records as the table.',got:(rt?paras.length:'different')+' records in the file, '+paras.length+' in the table',status:rt?'pass':'fail'});
const cPass=checks.filter(c=>c.status==='pass').length,cFail=checks.filter(c=>c.status==='fail').length,cRun=cPass+cFail;

/* ---------- 8. render ---------- */
const title=DOC.title||'Untitled document';
document.getElementById('h-title').textContent=title;
document.title=title;
document.getElementById('h-meta').innerHTML=(symbol?(DOC.doc_url?'<a href="'+esc(DOC.doc_url)+'" target="_blank" rel="noopener">'+esc(symbol)+'</a>':esc(symbol)):'')
 +(REF&&REF.adopted?' · adopted '+esc(REF.adopted):'')+' · '+nPages+' pages'+(DOC.source?' · '+esc(DOC.source):'');
const stHtml=(cFail>0?'<span class="bad"><span class="dot" style="background:var(--red)"></span>'+cFail+' check'+(cFail===1?'':'s')+' failed</span>'
  :'<span class="ok"><span class="dot" style="background:var(--green)"></span>'+cPass+' of '+cRun+' checks pass</span>');
document.getElementById('h-status').innerHTML=stHtml+'<br><span class="'+(flaggedPages.length?'bad':'')+'">'+flaggedPages.length+' pages flagged</span>';

const foundOK=refP!=null&&paras.length===refP;
document.getElementById('rail').innerHTML=
 '<div class="mono" style="color:var(--mute)">Document</div>'
 +'<div class="card"><div class="sym">'+esc(symbol)+'</div><div class="short">'+esc(title.length>90?title.slice(0,88)+'…':title)+'</div></div>'
 +'<section><div class="big '+(refP!=null&&!foundOK?'bad':'')+'">'+paras.length+'</div><div>paragraphs of '+(refP!=null?refP:'?')+'</div>'
 +'<div class="bar '+(foundOK?'good':'')+'"><i style="width:'+(refP?Math.min(100,paras.length/refP*100):0)+'%"></i></div>'
 +'<div class="hint">'+(refP==null?'no reference in this file':foundOK?'equal to the reference':'differs from the reference by '+Math.abs(paras.length-refP))+'</div></section>'
 +'<section><div class="big '+(flaggedPages.length?'bad':'')+'">'+flaggedPages.length+'</div><div>pages flagged of '+nPages+'</div><div class="hint">footnote text may sit inside a paragraph</div></section>'
 +'<section><div class="mono '+(cFail?'bad':'ok')+'">'+cPass+' of '+cRun+' checks pass</div></section>';

function tile(label,big,cls,sub,how){return '<div class="tile"><div class="mono" style="color:var(--mute)">'+label+'</div><div class="big '+cls+'">'+big+'</div><div class="sub">'+sub+'</div><div class="how">How this is computed: '+how+'</div></div>';}
let p0='<h2 class="q">Did the app find everything the document has?</h2>';
if(!paras.length){
  p0+='<p class="bad"><strong>No numbered paragraph was found in this file.</strong> The exports are disabled.</p>';
}
const fwOK=FW?paras.filter(p=>p.match).length:null;
p0+='<div class="tiles">'
 +tile('Paragraphs found',paras.length,foundOK?'ok':(refP==null?'':'bad'),
   refP==null?'no reference in this file':'the document has '+refP+(foundOK?' <span class="ok">· equal</span>':' <span class="bad">· difference of '+(paras.length-refP>0?'+':'')+(paras.length-refP)+'</span>'),
   'lines matching “n.” alone or “n. text” are paragraph starts; the reference count is read from the file.')
 +tile('First words match',FW?fwOK:'–',FW&&fwOK!==paras.length?'bad':'',FW?'of '+(refP!=null?refP:paras.length):'no reference in this file',
   'the first six words of each paragraph, footnote marks removed, equal to reference.first_words.')
 +tile('Pages flagged',flaggedPages.length,flaggedPages.length?'bad':'ok','of '+nPages+' pages'+(flaggedPages.length?' · footnote text may sit inside a paragraph: check these paragraphs against the PDF':''),
   'a page is flagged when a line inside a paragraph looks like a footnote (a number and a capital, a bare number, an asterisk).')
 +tile('Footnotes','not separated',' " style="font-size:32px','the document has '+(refF!=null?refF:'an unknown number')+'; this version leaves them in place and flags them',
   'nothing is removed; flagged lines stay in the paragraph text.')
 +'</div>';
if(mism.length){
  p0+='<ul class="mm" aria-label="First words that differ">'+mism.slice(0,10).map(p=>'<li><span class="bad">para. '+p.number+'</span>: found “'+esc(p.found)+'” / reference “'+esc(p.ref===undefined?'—':p.ref)+'”</li>').join('')
   +(mism.length>10?'<li>and '+(mism.length-10)+' more</li>':'')+'</ul>';
}
p0+='<div class="take"><div class="mono" style="color:var(--mute)">Take the paragraphs away</div>'
 +'<button class="btn" data-dl="json"'+(paras.length?'':' disabled')+'>Download JSON</button><button class="btn" data-dl="md"'+(paras.length?'':' disabled')+'>Download Markdown</button>'
 +'<div class="how">Each record carries its symbol, paragraph number, section, pages, text, citation, link and known limits. File names use the symbol.</div></div>';
p0+='<div class="fold"><button class="foldbtn" data-toggle aria-expanded="false" aria-controls="f-checks"><span>Every check ('+checks.length+')</span></button>'
 +'<div class="foldpanel" id="f-checks" hidden><ul class="checks">'
 +checks.map((c,i)=>'<li><span class="mono" style="color:var(--mute)">CHK.'+String(i+1).padStart(2,'0')+'</span> <strong>'+esc(c.name)+'</strong> · '
   +'<span class="st '+(c.status==='pass'?'pass':c.status==='fail'?'fail':'')+'">'+(c.status==='pass'?'pass':c.status==='fail'?'check failed':c.status==='notrun'?'not run':'note')+'</span>'
   +(c.go?' · <button class="linkbtn" data-go="'+c.go+'">see the rows</button>':'')
   +'<div class="hint">'+esc(c.expect)+'</div><div>'+esc(c.got)+'</div>'
   +(c.detail?'<div class="hint '+(c.detailBad?'bad':'')+'">'+(c.detailHtml?c.detail:esc(c.detail))+'</div>':'')+'</li>').join('')
 +'</ul></div></div>';
p0+='<div class="fold" style="margin-top:0;border-top:0"><button class="foldbtn" data-toggle aria-expanded="false" aria-controls="f-flag"><span>Flagged pages ('+flaggedPages.length+')</span></button>'
 +'<div class="foldpanel" id="f-flag" hidden><p class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF. A page also counts when an over-300-word paragraph starts on it.</p>';
if(flaggedPages.length){
  p0+='<table><caption><span class="mono">TAB.02</span>'+flaggedPages.length+' pages flagged, '+flaggedParas.length+' paragraphs to check</caption><thead><tr><th scope="col">Page</th><th scope="col">Paragraph</th><th scope="col" class="num">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody id="fpbody">'
  +flaggedPages.map((f,i)=>'<tr data-fp="'+i+'"><td><button class="rowbtn" aria-expanded="false">p. '+f.page+'</button></td><td>'+Array.from(f.paras).join(', ')+'</td><td class="num">'+f.suspect+'</td><td>'+esc(Array.from(f.reasons).join('; '))+'</td></tr>').join('')
  +'</tbody></table>';
}else p0+='<p>No page is flagged.</p>';
p0+='</div></div>';
document.getElementById('panel0').innerHTML=p0;

let p1='<h2 class="q">What does each paragraph say, and how do I cite it?</h2>';
p1+='<div class="fold" style="margin-top:0"><button class="foldbtn" data-toggle aria-expanded="false" aria-controls="f-heads"><span>Headings found: '+heads.length+'</span></button><div class="foldpanel" id="f-heads" hidden><ul class="hl">'
 +heads.map(h=>'<li style="padding-left:'+((h.level-1)*18)+'px"><span class="mono" style="color:var(--mute)">p. '+h.page+' · before para. '+(h.before<paras.length?paras[h.before].number:'end')+'</span> '+esc(h.full)+'</li>').join('')
 +'</ul></div></div><div style="height:12px"></div>';
p1+='<table><caption><span class="mono">TAB.01</span>'+paras.length+' paragraphs found, '+(refP!=null?refP+' expected':'no reference to compare')+'</caption>'
 +'<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody id="pbody">'
 +paras.map((p,i)=>{
   let fl=p.text;if(fl.length>120){fl=fl.slice(0,120);const s=fl.lastIndexOf(' ');if(s>60)fl=fl.slice(0,s);fl+='…';}
   const chk=[];
   if(p.match===false)chk.push('<span class="bad">first words differ</span>');
   if(p.flagged)chk.push('<span class="bad">may contain footnote text</span>');
   if(!chk.length)chk.push(p.match===null?'no reference':'OK');
   return '<tr data-p="'+i+'"><td class="num"><button class="rowbtn" aria-expanded="false" aria-label="Paragraph '+p.number+'">'+p.number+'</button></td><td>'+esc(p.section||'—')+'</td><td>'+(p.page_start===p.page_end?p.page_start:p.page_start+'–'+p.page_end)+'</td><td>'+esc(fl)+'</td><td>'+chk.join('<br>')+'</td></tr>';
 }).join('')+'</tbody></table>';
document.getElementById('panel1').innerHTML=p1;

document.getElementById('foot').innerHTML=esc(DOC.source||'')+(DOC.built?' · built '+esc(DOC.built):'')+'<br>Done by this page’s code; no model was called and nothing left the browser.';

/* ---------- 9. interaction ---------- */
const tabs=[document.getElementById('tab0'),document.getElementById('tab1')];
const panels=[document.getElementById('panel0'),document.getElementById('panel1')];
function selectTab(n){tabs.forEach((t,i)=>{t.setAttribute('aria-selected',i===n);t.tabIndex=i===n?0:-1;panels[i].hidden=i!==n;});}
tabs.forEach((t,i)=>{
  t.addEventListener('click',()=>selectTab(i));
  t.addEventListener('keydown',e=>{
    let n=null;
    if(e.key==='ArrowRight')n=(i+1)%tabs.length;else if(e.key==='ArrowLeft')n=(i-1+tabs.length)%tabs.length;
    else if(e.key==='Home')n=0;else if(e.key==='End')n=tabs.length-1;
    if(n!==null){e.preventDefault();selectTab(n);tabs[n].focus();}
  });
});
function openFold(id){const b=document.querySelector('[aria-controls="'+id+'"]');if(b){b.setAttribute('aria-expanded','true');document.getElementById(id).hidden=false;return b;}}
function copyText(s){
  if(navigator.clipboard&&navigator.clipboard.writeText){return navigator.clipboard.writeText(s).catch(()=>fallback(s));}
  fallback(s);return Promise.resolve();
}
function fallback(s){const t=document.createElement('textarea');t.value=s;document.body.appendChild(t);t.select();try{document.execCommand('copy');}catch(e){}t.remove();}
function pdfLines(p){
  let out='',last=null;
  p.lines.forEach(l=>{ if(l.page!==last){out+='<span class="pg">— page '+l.page+' begins —</span>\n';last=l.page;} out+=(l.suspect?'<span class="sus">'+esc(l.t)+'</span>':esc(l.t))+'\n'; });
  return out||'(no lines)';
}
function paraDetail(p){
  return '<div class="path">'+esc(p.path||'—')+'</div>'
   +'<div class="ptext">'+paraHTML(p)+'</div>'
   +'<div class="cmp">Reference: '+(p.ref===undefined?'—':esc(p.ref))+'<br>Found: &nbsp;&nbsp;&nbsp;'+esc(p.found)+(p.match===false?' <span class="bad">· differ</span>':'')+'</div>'
   +(p.flagged?'<div class="note bad">Lines in a red box look like footnote text; they stay in the paragraph. Check this paragraph against the PDF.</div>':'')
   +'<button class="btn" data-pdf>Show the PDF’s lines</button><button class="btn" data-copy="'+esc(p.citation)+'">Copy citation</button>'
   +'<pre class="lines" hidden>'+pdfLines(p)+'</pre>';
}
document.addEventListener('click',e=>{
  const t=e.target;
  const tg=t.closest('[data-toggle]');
  if(tg){const open=tg.getAttribute('aria-expanded')==='true';tg.setAttribute('aria-expanded',String(!open));document.getElementById(tg.getAttribute('aria-controls')).hidden=open;return;}
  const dl=t.closest('[data-dl]');
  if(dl){ if(dl.dataset.dl==='json')download(fileBase+'.json','application/json',JSON.stringify(exportRecords(),null,2)); else download(fileBase+'.md','text/markdown',exportMarkdown()); return; }
  const go=t.closest('[data-go]');
  if(go){ if(go.dataset.go==='para')selectTab(1); else {selectTab(0);const b=openFold('f-flag');if(b)b.scrollIntoView({block:'start'});} return; }
  const cp=t.closest('[data-copy]');
  if(cp){copyText(cp.dataset.copy).then(()=>{const o=cp.textContent;cp.textContent='Copied';setTimeout(()=>{cp.textContent='Copy citation';},2000);});return;}
  const pb=t.closest('[data-pdf]');
  if(pb){const pre=pb.parentNode.querySelector('pre.lines');pre.hidden=!pre.hidden;pb.textContent=pre.hidden?'Show the PDF’s lines':'Hide the PDF’s lines';return;}
  if(t.closest('.detail'))return;
  const tr=t.closest('tr[data-p]');
  if(tr){
    const btn=tr.querySelector('.rowbtn'),nx=tr.nextElementSibling;
    if(nx&&nx.classList.contains('detail')){nx.remove();btn.setAttribute('aria-expanded','false');}
    else{const p=paras[+tr.dataset.p];const d=document.createElement('tr');d.className='detail';d.innerHTML='<td colspan="5">'+paraDetail(p)+'</td>';tr.after(d);btn.setAttribute('aria-expanded','true');}
    return;
  }
  const fr=t.closest('tr[data-fp]');
  if(fr){
    const btn=fr.querySelector('.rowbtn'),nx=fr.nextElementSibling;
    if(nx&&nx.classList.contains('detail')){nx.remove();btn.setAttribute('aria-expanded','false');}
    else{
      const f=flaggedPages[+fr.dataset.fp];const pi=pages.find(x=>x.page===f.page);
      const raw=pi?pi.lines.map(l=>{
        if(!l.t)return '';
        const cls=(l.kind==='header'||l.kind==='footer')?'dim':'';
        const s=esc(l.t)+(l.kind==='header'||l.kind==='footer'?'   ['+l.kind+']':'');
        return l.suspect?'<span class="sus">'+s+'</span>':(cls?'<span class="dim">'+s+'</span>':s);
      }).join('\n'):'';
      const ps=paras.filter(p=>f.paras.has(p.number));
      const d=document.createElement('tr');d.className='detail';
      d.innerHTML='<td colspan="4"><div class="mono" style="color:var(--mute)">Raw lines of page '+f.page+' · red box = suspect</div><pre class="lines">'+raw+'</pre>'
        +ps.map(p=>'<div class="path">Paragraph '+p.number+' (pages '+p.page_start+(p.page_end!==p.page_start?'–'+p.page_end:'')+')</div><div class="ptext">'+paraHTML(p)+'</div>').join('')+'</td>';
      fr.after(d);btn.setAttribute('aria-expanded','true');
    }
  }
});
})();
</script>
</body>
</html>
```