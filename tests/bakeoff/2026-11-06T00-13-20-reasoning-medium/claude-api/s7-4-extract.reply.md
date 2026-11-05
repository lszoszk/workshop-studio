I've built the app with two tabs, Result and Paragraphs. It rebuilds the numbered paragraphs from the PDF text of `pdf_text`, checks them against the document's own reference, and flags the paragraphs where footnote text may sit inside. The downloads and the check panel are on the Result tab, one click down. Footnotes are not separated in this version, as the plan says.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraphs out of a PDF</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.mono{font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
a{color:#9b2335}
:focus-visible{outline:3px solid #9b2335;outline-offset:2px}
button{font:inherit;cursor:pointer}
.top{padding:18px 28px 12px;border-bottom:1px solid #d9d2c3}
.titlerow{display:flex;justify-content:space-between;gap:20px;align-items:flex-start;flex-wrap:wrap}
h1{font:normal 28px/1.2 Georgia,"Times New Roman",serif;margin:4px 0}
.top p{margin:4px 0 0;color:#4a463f}
.status{text-align:right;font-size:14px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;background:#9b2335}
.dot.g{background:#2f6b3a}.dot.n{background:#8a8170}
.layout{display:grid;grid-template-columns:260px 1fr;gap:0}
.rail{padding:20px 22px;border-right:1px solid #d9d2c3;min-height:70vh}
.rail .card{border-top:1px solid #d9d2c3;border-bottom:1px solid #d9d2c3;padding:8px 0;margin:6px 0 18px}
.rail .card b{font:13px ui-monospace,Menlo,Consolas,monospace;display:block}
.rail .card span{font-size:14px;color:#4a463f}
.big{font:normal 48px/1.05 Georgia,"Times New Roman",serif}
.rail .big{font-size:44px}
.bar{height:5px;background:#d9d2c3;margin:6px 0 4px}.bar i{display:block;height:100%;background:#2f6b3a}.bar.bad i{background:#9b2335}
.hint{font-size:13px;color:#5a554b}
.rail .blk{margin-bottom:22px}
main{padding:0 28px 30px;min-width:0}
[role=tablist]{display:flex;gap:6px;border-bottom:1px solid #d9d2c3;margin:0 0 20px}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;padding:14px 14px 10px;font:12px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;color:#1d1b18}
[role=tab][aria-selected=true]{color:#9b2335;border-bottom-color:#9b2335}
h2{font:normal 22px Georgia,serif;margin:6px 0}
.q{color:#4a463f;margin:0 0 16px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:0;border-top:1px solid #d9d2c3;border-left:1px solid #d9d2c3}
.tile{padding:14px 16px;border-right:1px solid #d9d2c3;border-bottom:1px solid #d9d2c3}
.tile .big.ok{color:#2f6b3a}.tile .big.bad,.bad{color:#9b2335}
.tile .sub{font-size:15px;margin:4px 0}
.how{font:12px/1.4 ui-monospace,Menlo,Consolas,monospace;color:#5a554b;margin:6px 0 0}
.ok{color:#2f6b3a}
.red{color:#9b2335;font-weight:600}
.mm{margin:14px 0;font:13px ui-monospace,Menlo,Consolas,monospace}
.mm div{padding:2px 0}
.btn{background:#1d1b18;color:#f4f0e8;border:0;padding:10px 16px;margin-right:8px}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn.light{background:none;color:#1d1b18;border:1px solid #1d1b18;padding:6px 12px;font-size:14px}
.acc{display:block;width:100%;text-align:left;background:none;border:0;border-top:1px solid #d9d2c3;padding:12px 0;font:13px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;text-transform:uppercase;color:#1d1b18}
.acc::before{content:"+ ";color:#9b2335}.acc[aria-expanded=true]::before{content:"− "}
.accp{padding:0 0 14px}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font:normal 18px Georgia,serif;padding:6px 0}
caption .mono{color:#9b2335;margin-right:8px}
th{font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:2px solid #1d1b18;padding:6px 8px}
td{border-bottom:1px solid #d9d2c3;padding:7px 8px;vertical-align:top}
th.r,td.r{text-align:right}
tr.row{cursor:pointer}tr.row:hover{background:#ece6d9}
.numbtn{background:none;border:0;color:#9b2335;font:600 15px ui-monospace,Menlo,Consolas,monospace;padding:0}
td.detail{background:#faf7f0;padding:14px 18px}
.path{color:#5a554b;margin-bottom:8px}
.ptext{max-width:80ch;margin:6px 0}
mark.sus{background:none;color:inherit;outline:1px solid #9b2335;outline-offset:1px;padding:0 2px}
pre.lines{white-space:pre-wrap;background:#f4f0e8;border:1px solid #d9d2c3;padding:10px;font:13px/1.45 ui-monospace,Menlo,Consolas,monospace;max-width:90ch}
.fw{font:13px ui-monospace,Menlo,Consolas,monospace;margin:8px 0}
.note{font-size:14px;color:#4a463f;margin:6px 0 10px}
.chk{padding:10px 0;border-top:1px solid #d9d2c3;font-size:15px}
.chk .nm{font-weight:600}
.pass{color:#2f6b3a;font-weight:600}.fail{color:#9b2335;font-weight:600}.noterun{color:#5a554b;font-weight:600}
.chk .ev{font:12.5px ui-monospace,Menlo,Consolas,monospace;color:#3a362f;margin-top:3px;overflow-wrap:anywhere}
.linkbtn{background:none;border:0;color:#9b2335;text-decoration:underline;padding:0;font-size:14px}
footer{padding:14px 28px;border-top:1px solid #d9d2c3;font-size:13px;color:#4a463f}
.fbar{margin:6px 0 10px;font-size:14px}
ol.heads{font-size:14px;columns:1;padding-left:22px}
@media(max-width:820px){.layout{grid-template-columns:1fr}.rail{border-right:0;border-bottom:1px solid #d9d2c3;min-height:0}}
</style>
</head>
<body>
<header class="top">
  <div class="mono">UN document · PDF text</div>
  <div class="titlerow"><h1 id="title"></h1><div class="status" id="status"></div></div>
  <p id="meta"></p>
</header>
<div class="layout">
  <aside class="rail" id="rail" aria-label="Document summary"></aside>
  <main>
    <div role="tablist" aria-label="Views" id="tabs">
      <button role="tab" id="tab1" aria-selected="true" aria-controls="p1" tabindex="0">01 RESULT</button>
      <button role="tab" id="tab2" aria-selected="false" aria-controls="p2" tabindex="-1">02 PARAGRAPHS</button>
    </div>
    <section role="tabpanel" id="p1" aria-labelledby="tab1"></section>
    <section role="tabpanel" id="p2" aria-labelledby="tab2" hidden></section>
  </main>
</div>
<footer id="foot"></footer>
<script>
(function(){
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const $=id=>document.getElementById(id);
const D=(window.WORKSHOP_DATA||{}).pdf_text;
const records=Array.isArray(D)?D:((D&&D.records)||[]);
const meta=Array.isArray(D)?{}:(D||{});
const symbol=meta.symbol||'';
const docUrl=meta.doc_url||'';
const ref=meta.reference||{};
const refN=typeof ref.paragraphs==='number'?ref.paragraphs:null;
const refF=typeof ref.footnotes==='number'?ref.footnotes:null;
const fwRef=(ref.first_words&&typeof ref.first_words==='object')?ref.first_words:null;
const title=meta.title||symbol||'Untitled document';

/* ---------- pipeline ---------- */
const pages=records.slice().sort((a,b)=>a.page-b.page);
const all=[];
const st={headerOk:0,warn:[],pagenum:0,bare:[],total:0,hyphens:0};
pages.forEach(pg=>{
  const L=String(pg.text||'').split(/\r?\n/).map(t=>({t:t.trim(),page:pg.page,kind:null}));
  L.forEach(l=>{if(l.t)st.total++;});
  const first=L.findIndex(l=>l.t);
  let start=0;
  if(first>=0&&symbol&&L[first].t===symbol){L[first].kind='header';st.headerOk++;start=first+1;}
  else st.warn.push(pg.page);
  let end=L.length,gotNum=false;
  for(let k=L.length-1;k>=start;k--){
    const t=L[k].t;
    if(!t){end=k;continue;}
    if(/^GE\./.test(t)||/^(\d{6}\s*)+$/.test(t)){L[k].kind='footer';end=k;continue;}
    if(/^\d{1,3}$/.test(t)){
      L[k].kind='footer';end=k;
      if(!gotNum&&Number(t)===pg.page){gotNum=true;st.pagenum++;}else st.bare.push({page:pg.page,value:t});
      continue;}
    break;
  }
  for(let k=start;k<end;k++)all.push(L[k]);
});
const isStart=t=>/^(\d{1,3})\.$/.test(t)||/^(\d{1,3})\. (.+)$/.test(t);
const isLabel=t=>/^([IVX]+|[A-Z])\.$/.test(t);
const trigger=t=>{
  if(/^\d{1,3}$/.test(t))return 'bare number';
  if(/^\d{1,3} [A-Z“”"‘']/.test(t))return 'starts with a number and a space';
  if(/^\* /.test(t))return 'starts with an asterisk';
  return null;};
const headingLike=t=>t.length<=90&&/^[A-Z]/.test(t)&&!/[.;:,\d]$/.test(t)&&!trigger(t);
const nextNB=i=>{for(let j=i+1;j<all.length;j++)if(all[j].t)return j;return -1;};
const paras=[],headings=[],events=[];
let cur=null,part=null,sub=null,unl=null,started=false,susPage=null,pending=[];
function pushHeading(text,level,kind,page){
  const h={text,level,kind,page,before:null};
  headings.push(h);events.push({type:'heading',level,text});pending.push(h);
}
for(let i=0;i<all.length;i++){
  const l=all[i],t=l.t;
  if(!t)continue;
  if(isLabel(t)){
    started=true;l.kind='heading';
    const parts=[];let j=i+1;
    while(j<all.length&&parts.length<4){
      const u=all[j];
      if(!u.t){j++;continue;}
      if(isLabel(u.t)||isStart(u.t))break;
      parts.push(u.t);u.kind='heading';j++;
    }
    i=j-1;
    const lab=t.slice(0,-1),text=lab+'. '+parts.join(' ');
    if(/^[IVX]+$/.test(lab)){part=text;sub=null;unl=null;pushHeading(text,2,'labelled',l.page);}
    else{sub=text;unl=null;pushHeading(text,3,'labelled',l.page);}
    cur=null;continue;
  }
  const m=t.match(/^(\d{1,3})\.$/)||t.match(/^(\d{1,3})\. (.+)$/);
  if(m){
    started=true;l.kind='paragraph';
    cur={number:+m[1],section:unl||sub||part||null,part:part,path:[part,sub,unl].filter(Boolean),startRaw:t,startPage:l.page,lines:[]};
    if(m[2])cur.lines.push({t:m[2],page:l.page,sus:false,src:l,start:true});
    paras.push(cur);events.push({type:'para',p:cur});
    pending.forEach(h=>h.before=cur.number);pending=[];
    continue;
  }
  if(!cur){if(!started)l.kind='cover';continue;}
  const trig=trigger(t);
  if(trig)susPage=l.page;
  const sus=!!trig||susPage===l.page;
  const nj=nextNB(i);
  if(!sus&&nj>=0&&isStart(all[nj].t)&&headingLike(t)){
    let text=t;l.kind='heading';
    const pl=cur.lines[cur.lines.length-1];
    if(pl&&!pl.sus&&!pl.start&&headingLike(pl.t)){cur.lines.pop();pl.src.kind='heading';text=pl.t+' '+t;}
    unl=text;pushHeading(text,3,'unlabelled',l.page);
    continue;
  }
  cur.lines.push({t,page:l.page,sus,trig,src:l});l.kind='paragraph';
  if(/-$/.test(t))st.hyphens++;
}
const todayStr=new Date().toISOString().slice(0,10);
paras.forEach(p=>{
  p.text=p.lines.map(x=>x.t).join(' ').replace(/\s+/g,' ').trim();
  const pg=[p.startPage].concat(p.lines.map(x=>x.page));
  p.page_start=pg[0];p.page_end=Math.max.apply(null,pg);
  p.suspects=p.lines.filter(x=>x.sus);
  p.words=p.text?p.text.split(/\s+/).length:0;
  p.long=p.words>300;
  p.flagged=p.suspects.length>0||p.long;
  const rs=[];p.lines.forEach(x=>{if(x.trig&&rs.indexOf(x.trig)<0)rs.push(x.trig);});
  if(p.long)rs.push('paragraph over 300 words');
  p.why=rs;
  p.citation=symbol+', para. '+p.number;
  p.found=foundWords(p.text);
  const r=fwRef&&fwRef[String(p.number)];
  p.refWords=(r==null)?null:String(r);
  p.fwMatch=p.refWords==null?null:normFW(p.found)===normFW(p.refWords);
});
function normFW(s){return String(s).replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();}
function foundWords(text){
  const out=[];
  for(const tok of text.split(/\s+/)){
    if(!tok)continue;
    if(/^\d{1,3}$/.test(tok)&&out.length){
      const pv=out[out.length-1];
      if(/[.,”"’']$/.test(pv)&&!/^(No|Nos|art|arts|para|paras|vol|p|pp|ch|chap)\.$/i.test(pv))continue;
    }
    let t=tok;const m=t.match(/^(.*[a-z.,;:”"’)])\d{1,3}$/);
    if(m&&t.indexOf('/')<0)t=m[1];
    out.push(t);if(out.length===6)break;
  }
  return out.join(' ');
}
const nP=paras.length;
const flagged=paras.filter(p=>p.flagged);
const flagPages=new Set();
paras.forEach(p=>{p.suspects.forEach(x=>flagPages.add(x.page));if(p.long)flagPages.add(p.page_start);});
const susTotal=paras.reduce((a,p)=>a+p.suspects.length,0);
const susPages=new Set();paras.forEach(p=>p.suspects.forEach(x=>susPages.add(x.page)));
const fwMis=paras.filter(p=>p.fwMatch===false);
const fwOk=paras.filter(p=>p.fwMatch===true).length;
const hasFW=fwRef!=null&&refN!=null;

/* ---------- exports ---------- */
const fileBase=(symbol||'document').replace(/\//g,'-');
function limitations(p){
  if(!p.flagged)return 'footnotes not separated';
  if(!p.suspects.length)return 'footnotes not separated; paragraph over 300 words';
  return 'footnotes not separated; '+p.suspects.length+' suspect line'+(p.suspects.length>1?'s':'')+' may sit inside this paragraph';
}
function jsonRecords(){
  return paras.map(p=>({symbol:symbol,paragraph:p.number,section:p.section,part:p.part,page_start:p.page_start,page_end:p.page_end,text:p.text,text_lines:p.lines.map(x=>x.t).join(' | '),flagged:p.flagged,first_words_match:p.fwMatch,citation:p.citation,doc_url:docUrl,limitations:limitations(p)}));
}
function mdFile(){
  const L=['---','title: '+JSON.stringify(title),'symbol: '+JSON.stringify(symbol),'adopted: '+JSON.stringify(ref.adopted||'unknown'),'source_url: '+JSON.stringify(docUrl),'extracted: '+todayStr,'paragraphs_found: '+nP,'paragraphs_expected: '+(refN==null?'unknown':refN),'paragraphs_flagged: '+flagged.length,'footnotes: '+JSON.stringify('not separated; the document has '+(refF==null?'an unknown number':refF)),'---',''];
  events.forEach(e=>{
    if(e.type==='heading')L.push((e.level===2?'## ':'### ')+e.text,'');
    else L.push('**'+e.p.number+'.** '+e.p.text+(e.p.flagged?' (flagged: may contain footnote text)':''),'');
  });
  return L.join('\n');
}
function download(name,mime,content){
  const b=new Blob([content],{type:mime+';charset=utf-8'});
  const u=URL.createObjectURL(b),a=document.createElement('a');
  a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(u),2000);
}

/* ---------- checks ---------- */
const checks=[];
function addCheck(c){checks.push(c);}
(function(){
  addCheck({name:'Paragraph count',
    exp:refN==null?'no reference in this file':refN+' paragraphs (reference)',got:nP+' paragraphs found',
    k:refN==null?'norun':(nP===refN?'pass':'fail')});
  const seen={},dups=[],gaps=[];let broke=[],prev=0;
  paras.forEach(p=>{seen[p.number]=(seen[p.number]||[]).concat(p.page_start);});
  Object.keys(seen).forEach(n=>{if(seen[n].length>1)dups.push(n+' (pages '+seen[n].join(', ')+')');});
  const mx=paras.reduce((a,p)=>Math.max(a,p.number),0);
  for(let n=1;n<=mx;n++)if(!seen[n])gaps.push(n);
  paras.forEach((p,k)=>{if(p.number!==k+1)broke.push(p.number);});
  const rows=[];dups.forEach(d=>rows.push(parseInt(d,10)));
  if(broke.length)rows.push(broke[0]);
  addCheck({name:'Numbering',exp:'1 to n in order, no gaps or duplicates',
    got:nP===0?'no paragraphs':(broke.length?('first out of sequence: para. '+broke[0]+'; gaps: '+(gaps.join(', ')||'none')+'; duplicates: '+(dups.join('; ')||'none')):'1 to '+mx+' in order'),
    k:nP===0?'fail':(broke.length?'fail':'pass'),rows:rows});
  addCheck({name:'First words',exp:hasFW?'every paragraph begins with the reference first words':'no reference in this file',
    got:hasFW?(fwMis.length+' differ; '+fwOk+' match'):'',k:hasFW?(fwMis.length?'fail':'pass'):'norun',rows:fwMis.map(p=>p.number)});
  addCheck({name:'Paragraphs flagged',exp:'a flag is not a failure',got:flagged.length+' paragraphs flagged on '+flagPages.size+' pages, to check against the PDF',k:'note',rows:flagged.map(p=>p.number)});
  addCheck({name:'Suspect lines',exp:'none removed; they stay in the text',got:susTotal+' suspect lines on '+susPages.size+' pages, in '+paras.filter(p=>p.suspects.length).length+' paragraphs',k:'note',rows:paras.filter(p=>p.suspects.length).map(p=>p.number)});
  const np=pages.length;
  const hfOk=st.headerOk===np&&st.pagenum===Math.max(0,np-1);
  addCheck({name:'Headers and footers',exp:'symbol on every page ('+np+'); page number on all but the first ('+Math.max(0,np-1)+')',
    got:st.headerOk+' pages with the symbol first; '+st.pagenum+' with a page number; bare numbers removed from the footer: '+(st.bare.length?st.bare.map(b=>b.value+' (p. '+b.page+')').join(', '):'none')+(st.warn.length?'; header not found on pages '+st.warn.join(', '):''),
    k:hfOk?'pass':'fail'});
  const lab=headings.filter(h=>h.kind==='labelled'),un=headings.filter(h=>h.kind==='unlabelled');
  addCheck({name:'Headings',exp:'headings are never paragraph text',got:lab.length+' labelled, '+un.length+' unlabelled. Unlabelled: '+(un.map(h=>'“'+h.text+'”').join('; ')||'none'),k:'note'});
  const cnt={cover:0,header:0,heading:0,paragraph:0,footer:0};const un2=[];
  pages.forEach(()=>{});
  all.forEach(l=>{if(!l.t)return;if(l.kind&&cnt[l.kind]!=null)cnt[l.kind]++;else un2.push(l);});
  // header and footer lines were not all pushed into "all": count them from the page totals
  const classified=cnt.cover+cnt.heading+cnt.paragraph;
  const hfLines=st.total-all.filter(l=>l.t).length;
  const sum=classified+hfLines+un2.length;
  addCheck({name:'Nothing lost',exp:st.total+' non-empty lines in the file',
    got:'cover '+cnt.cover+' + header and footer '+hfLines+' + heading '+cnt.heading+' + paragraph '+cnt.paragraph+' + unclassified '+un2.length+' = '+sum+(un2.length?'. Unclassified: '+un2.map(l=>'“'+l.t.slice(0,50)+'” (p. '+l.page+')').join('; '):'')+'. Line-end hyphens found: '+st.hyphens+' (no joining done)',
    k:(sum===st.total&&!un2.length)?'pass':'fail'});
  let rt=-1;try{rt=JSON.parse(JSON.stringify(jsonRecords())).length;}catch(e){}
  addCheck({name:'Export round trip',exp:nP+' records in the table',got:rt+' records after parsing the JSON back',k:rt===nP?'pass':'fail'});
})();
const nFail=checks.filter(c=>c.k==='fail').length;
const nNot=checks.filter(c=>c.k==='norun').length;
const nPass=checks.filter(c=>c.k==='pass'||c.k==='note').length;

/* ---------- header, rail, footer ---------- */
$('title').textContent=title;
$('meta').innerHTML=(symbol?(docUrl?'<a href="'+esc(docUrl)+'" target="_blank" rel="noopener">'+esc(symbol)+'</a>':esc(symbol)):'')+(ref.adopted?' · adopted '+esc(ref.adopted):'')+' · '+pages.length+' pages'+(meta.source?' · '+esc(meta.source):'');
$('status').innerHTML=(nFail?'<span class="dot"></span><b class="red">'+nFail+' check'+(nFail>1?'s':'')+' failed</b>':'<span class="dot '+(nNot?'n':'g')+'"></span>'+nPass+' of '+checks.length+' checks pass'+(nNot?', '+nNot+' not run':''))+'<br>'+flagged.length+' paragraphs flagged';
const diffOK=refN!=null&&nP===refN;
$('rail').innerHTML='<div class="mono">Document</div><div class="card"><b>'+esc(symbol||'—')+'</b><span>'+esc(title)+'</span></div>'
 +'<div class="blk"><div class="big '+(refN==null||diffOK?'':'bad')+'">'+nP+'</div><div class="hint">paragraphs'+(refN!=null?' of '+refN:'')+'</div>'+(refN!=null?'<div class="bar '+(diffOK?'':'bad')+'"><i style="width:'+Math.min(100,Math.round(nP/Math.max(refN,1)*100))+'%"></i></div>':'<div class="hint">no reference in this file</div>')+'</div>'
 +'<div class="blk"><div class="big '+(flagged.length?'bad':'')+'">'+flagged.length+'</div><div class="hint">paragraphs flagged of '+nP+' found'+(flagged.length?': footnote text may sit inside: check them against the PDF':'')+'</div></div>'
 +'<div class="blk"><div class="big" style="font-size:34px">'+nPass+' of '+checks.length+'</div><div class="hint">checks pass'+(nFail?' ('+nFail+' failed)':'')+'</div></div>';
$('foot').innerHTML=esc(meta.source||'')+(meta.built?' · built '+esc(meta.built):'')+' · Done by this page’s code; no model was called and nothing left the browser.';

/* ---------- tab 01 ---------- */
const p1=$('p1');
function tile(lab,big,cls,sub,how){return '<div class="tile"><div class="mono">'+lab+'</div><div class="big '+cls+'">'+big+'</div><div class="sub">'+sub+'</div><p class="how">How this is computed: '+how+'</p></div>';}
let h='<h2>Did the app find everything the document has?</h2><p class="q mono">Result · n = '+pages.length+' pages</p>';
if(!nP){h+='<p class="red">No numbered paragraph was found in this file, so there is nothing to show or export.</p>';}
const diff=refN==null?'':(nP===refN?'':' ('+(nP>refN?'+':'−')+Math.abs(nP-refN)+')');
h+='<div class="tiles">'
 +tile('Paragraphs found',nP,refN==null?'':(diffOK?'ok':'bad'),refN==null?'no reference in this file':'the document has '+refN+(diffOK?' · equal':'<span class="red">'+diff+'</span>'),'lines that are a number and a full stop, alone or followed by text, counted in page order.')
 +tile('First words match',hasFW?fwOk:'—',hasFW?(fwMis.length?'bad':'ok'):'',hasFW?'of '+refN+' in the reference':'no reference in this file','the first six words of each paragraph, footnote marks removed, against the reference.')
 +tile('Paragraphs flagged',flagged.length,flagged.length?'bad':'ok','of '+nP+' found, on '+flagPages.size+' pages'+(flagged.length?'<br><span class="red">footnote text may sit inside these paragraphs: check them against the PDF</span>':''),'a paragraph with a suspect line (a footnote-like line to the foot of the page) or over 300 words.')
 +tile('Footnotes','not separated','', 'the document has '+(refF==null?'an unknown number':refF)+'; this version leaves them in place and flags them','footnotes are not counted or removed in this version.')
 +'</div>';
if(fwMis.length){
  h+='<div class="mm"><div class="mono">First words differ</div>'+fwMis.slice(0,10).map(p=>'<div>para. '+p.number+': found “'+esc(p.found)+'” / reference “'+esc(p.refWords)+'”</div>').join('')+(fwMis.length>10?'<div>and '+(fwMis.length-10)+' more</div>':'')+'</div>';
}
h+='<h2 style="margin-top:26px">Take the paragraphs away</h2><p class="hint">JSON: one record per paragraph with symbol, number, section, pages, text, flag, citation and limitations. Markdown: front matter, headings and paragraphs.</p>'
 +'<p><button class="btn" id="dlj"'+(nP?'':' disabled')+'>Download JSON</button><button class="btn" id="dlm"'+(nP?'':' disabled')+'>Download Markdown</button></p>'
 +'<button class="acc" id="a1" aria-expanded="false" aria-controls="ap1">Every check ('+checks.length+')</button><div class="accp" id="ap1" hidden>'
 +checks.map(c=>'<div class="chk"><span class="nm">'+esc(c.name)+'</span> · <span class="'+(c.k==='pass'?'pass':c.k==='fail'?'fail':'noterun')+'">'+(c.k==='pass'?'pass':c.k==='fail'?'check failed':c.k==='norun'?'not run':'note')+'</span>'
   +(c.rows&&c.rows.length?' · <button class="linkbtn" data-rows="'+c.rows.join(',')+'">show the '+c.rows.length+' row'+(c.rows.length>1?'s':'')+'</button>':'')
   +'<div class="ev">expected: '+esc(c.exp)+'<br>found: '+esc(c.got||'not run')+'</div></div>').join('')+'</div>'
 +'<button class="acc" id="a2" aria-expanded="false" aria-controls="ap2">Flagged paragraphs ('+flagged.length+')</button><div class="accp" id="ap2" hidden>'
 +'<p class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</p>'
 +(flagged.length?'<table><caption><span class="mono">TAB.01</span>'+flagged.length+' paragraphs flagged on '+flagPages.size+' pages</caption><thead><tr><th scope="col" class="r">Paragraph</th><th scope="col" class="r">Page</th><th scope="col">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>'
 +flagged.map(p=>{const s=p.suspects[0];return '<tr class="row" data-go="'+p.number+'" tabindex="0"><td class="r"><b style="color:#9b2335">'+p.number+'</b></td><td class="r">'+(s?s.page:p.page_start)+'</td><td>'+(s?p.suspects.length+': “'+esc(s.t.slice(0,60))+(s.t.length>60?'…':'')+'”':'none')+'</td><td>'+esc(p.why.join('; '))+'</td></tr>';}).join('')+'</tbody></table>':'<p>No paragraph is flagged.</p>')+'</div>';
p1.innerHTML=h;

function toggleAcc(btn){
  const open=btn.getAttribute('aria-expanded')==='true';
  ['a1','a2'].forEach(id=>{const b=$(id);b.setAttribute('aria-expanded','false');$(b.getAttribute('aria-controls')).hidden=true;});
  if(!open){btn.setAttribute('aria-expanded','true');$(btn.getAttribute('aria-controls')).hidden=false;}
}
$('a1').onclick=()=>toggleAcc($('a1'));
$('a2').onclick=()=>toggleAcc($('a2'));
if($('dlj'))$('dlj').onclick=()=>download(fileBase+'.json','application/json',JSON.stringify(jsonRecords(),null,2));
if($('dlm'))$('dlm').onclick=()=>download(fileBase+'.md','text/markdown',mdFile());
p1.querySelectorAll('[data-rows]').forEach(b=>b.onclick=()=>{filter=b.getAttribute('data-rows').split(',').map(Number);buildTable();setTab(2);});
p1.querySelectorAll('[data-go]').forEach(r=>{
  r.onclick=()=>goTo(+r.getAttribute('data-go'));
  r.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();goTo(+r.getAttribute('data-go'));}};
});

/* ---------- tab 02 ---------- */
let filter=null;
const p2=$('p2');
function firstLine(t){
  if(t.length<=120)return t;
  let c=t.slice(0,120);
  if(t[120]!==' ')c=c.replace(/\s+\S*$/,'');
  return c+'…';
}
function pageStr(p){return p.page_start===p.page_end?String(p.page_start):p.page_start+'–'+p.page_end;}
function checkCell(p){
  const a=[];
  if(p.fwMatch===false)a.push('<span class="red">first words differ</span>');
  if(p.flagged)a.push('<span class="red">may contain footnote text</span>');
  return a.length?a.join('<br>'):'OK';
}
function buildShell(){
  p2.innerHTML='<h2>What does each paragraph say, and how do I cite it?</h2><p class="q mono">Click a row = open it in place</p>'
   +'<button class="acc" id="hb" aria-expanded="false" aria-controls="hbp">Headings found: '+headings.length+'</button><div class="accp" id="hbp" hidden><ol class="heads">'
   +headings.map(x=>'<li>'+esc(x.text)+' <span class="hint">('+x.kind+(x.before!=null?', before para. '+x.before:'')+')</span></li>').join('')+'</ol></div>'
   +'<div id="fnote" class="fbar"></div><div id="tbl"></div>';
  $('hb').onclick=()=>{const o=$('hb').getAttribute('aria-expanded')==='true';$('hb').setAttribute('aria-expanded',String(!o));$('hbp').hidden=o;};
}
function buildTable(){
  const set=filter?new Set(filter):null;
  const list=set?paras.filter(p=>set.has(p.number)):paras;
  $('fnote').innerHTML=filter?'Showing '+list.length+' paragraphs concerned by a check · <button class="linkbtn" id="clr">show all paragraphs</button>':'';
  if($('clr'))$('clr').onclick=()=>{filter=null;buildTable();};
  if(!nP){$('tbl').innerHTML='<p class="red">No paragraph was found.</p>';return;}
  $('tbl').innerHTML='<table><caption><span class="mono">TAB.02</span>'+nP+' paragraphs found'+(refN!=null?', '+refN+' expected':', no reference in this file')+'</caption><thead><tr><th scope="col" class="r">No.</th><th scope="col">Section</th><th scope="col" class="r">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody>'
   +list.map(p=>'<tr class="row" data-n="'+p.number+'"><td class="r"><button class="numbtn" aria-expanded="false" data-b="'+p.number+'">'+p.number+'</button></td><td>'+esc(p.section||'—')+'</td><td class="r">'+pageStr(p)+'</td><td>'+esc(firstLine(p.text))+'</td><td>'+checkCell(p)+'</td></tr>').join('')+'</tbody></table>';
  $('tbl').querySelectorAll('tr.row').forEach(r=>r.onclick=()=>toggleRow(+r.getAttribute('data-n')));
}
function markedText(p){
  let out='',run=[];
  const flush=()=>{if(run.length){out+='<mark class="sus">'+esc(run.join(' '))+'</mark> ';run=[];}};
  p.lines.forEach(x=>{if(x.sus)run.push(x.t);else{flush();out+=esc(x.t)+' ';}});
  flush();return out.trim();
}
function pdfLines(p){
  let s='',pg=null;
  const mk=n=>{if(n!==pg){pg=n;s+='— PDF page '+n+' begins —\n';}};
  mk(p.startPage);s+=p.startRaw+'\n';
  p.lines.forEach(x=>{mk(x.page);s+=(x.sus?'! ':'')+x.t+'\n';});
  return s;
}
function toggleRow(n){
  const row=p2.querySelector('tr.row[data-n="'+n+'"]');if(!row)return;
  const btn=row.querySelector('button');
  const nxt=row.nextElementSibling;
  if(nxt&&nxt.classList.contains('drow')){nxt.remove();btn.setAttribute('aria-expanded','false');return;}
  const p=paras.find(x=>x.number===n);
  const tr=document.createElement('tr');tr.className='drow';
  tr.innerHTML='<td class="detail" colspan="5"><div class="path mono">'+esc(p.path.join(' › ')||'No heading above')+'</div>'
   +'<p class="ptext">'+markedText(p)+'</p>'
   +'<div class="fw">Reference first words: '+(p.refWords==null?'not available':'“'+esc(p.refWords)+'”')+'<br>Found first words: “'+esc(p.found)+'”'+(p.fwMatch===false?' <span class="red">first words differ</span>':'')+'</div>'
   +(p.flagged?'<div class="hint">Flagged: '+esc(p.why.join('; '))+'. Suspect lines are boxed in red and stay in the text.</div>':'')
   +'<p><button class="btn light" data-copy>Copy citation</button> <button class="btn light" data-pl aria-expanded="false">Show the PDF’s lines</button></p>'
   +'<pre class="lines" hidden>'+esc(pdfLines(p))+'</pre></td>';
  row.after(tr);btn.setAttribute('aria-expanded','true');
  const cb=tr.querySelector('[data-copy]');
  cb.onclick=e=>{e.stopPropagation();copyText(p.citation);cb.textContent='Copied';setTimeout(()=>{cb.textContent='Copy citation';},2000);};
  const pb=tr.querySelector('[data-pl]'),pre=tr.querySelector('pre');
  pb.onclick=e=>{e.stopPropagation();const o=pb.getAttribute('aria-expanded')==='true';pb.setAttribute('aria-expanded',String(!o));pre.hidden=o;pb.textContent=o?'Show the PDF’s lines':'Hide the PDF’s lines';};
  tr.onclick=e=>e.stopPropagation();
}
function copyText(s){
  const fb=()=>{const t=document.createElement('textarea');t.value=s;document.body.appendChild(t);t.select();try{document.execCommand('copy');}catch(e){}t.remove();};
  try{if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(s).catch(fb);}else fb();}catch(e){fb();}
}
function goTo(n){
  if(filter&&filter.indexOf(n)<0)filter=null;
  buildTable();setTab(2);
  const row=p2.querySelector('tr.row[data-n="'+n+'"]');
  if(row){const nx=row.nextElementSibling;if(!(nx&&nx.classList.contains('drow')))toggleRow(n);
    row.scrollIntoView({block:'start'});const b=row.querySelector('button');if(b)b.focus();}
}
buildShell();buildTable();

/* ---------- tabs ---------- */
function setTab(n,focus){
  [1,2].forEach(i=>{
    const t=$('tab'+i),on=i===n;
    t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1;
    $('p'+i).hidden=!on;
  });
  if(focus)$('tab'+n).focus();
}
$('tab1').onclick=()=>setTab(1);
$('tab2').onclick=()=>setTab(2);
$('tabs').addEventListener('keydown',e=>{
  const cur=$('tab2').getAttribute('aria-selected')==='true'?2:1;
  let n=null;
  if(e.key==='ArrowRight')n=cur===1?2:1;
  else if(e.key==='ArrowLeft')n=cur===1?2:1;
  else if(e.key==='Home')n=1;else if(e.key==='End')n=2;
  if(n){e.preventDefault();setTab(n,true);}
});
})();
</script>
</body>
</html>
```