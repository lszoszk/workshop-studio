I added General Comment No. 32 as a second card in the left rail; the tabs, checks, repair log and CSV all follow the card you select, and the pipeline is the same, with no rule changed. Under the cards there is a small table with, for each document, the paragraphs found next to the reference, the pages flagged and the checks passed. Because no rule changed, a heading written on one line as "I. GENERAL REMARKS" is not recognised by the heading rule, so look at the Headings check on tab 04 before you trust the sections of this document.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6a3b;--mut:#5c574e;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 var(--sans)}
a{color:var(--ink)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
button{font:inherit;color:inherit}
.wrap{max-width:1200px;margin:0 auto;padding:0 20px}
.mono{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.sm{font-size:12px;color:var(--mut)}
.ser{font-family:var(--serif)}
.bad{color:var(--red)}.ok{color:var(--green)}.mut{color:var(--mut)}
.sr{position:absolute;left:-9999px}
header.top{border-bottom:1px solid var(--rule);padding:22px 0 16px}
header.top .hrow{display:flex;gap:24px;justify-content:space-between;align-items:flex-start;flex-wrap:wrap}
h1{font:400 34px/1.15 var(--serif);margin:6px 0 8px;max-width:800px}
.meta{margin:0 0 6px;color:var(--mut)}
.what{margin:0;max-width:780px}
.status{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap;padding-top:8px}
.dot{display:inline-block;width:.75em;height:.75em;border-radius:50%;margin-right:.45em;background:var(--mut);vertical-align:baseline}
.dot.ok{background:var(--green)}.dot.bad{background:var(--red)}
.layout{display:grid;grid-template-columns:320px minmax(0,1fr);gap:36px;padding-top:24px;padding-bottom:30px}
aside h2{margin:0 0 10px;font-weight:400}
.card{border:0;border-left:3px solid transparent;border-bottom:1px solid var(--rule);padding:8px 0 10px 12px;margin:0 0 6px;display:block;width:100%;text-align:left;background:none}
.card.sel{border-left-color:var(--red)}
button.card{cursor:pointer}
.card .sym{font-family:var(--mono);font-size:13px;display:block}
.card .st2{display:block}
.card .sub{display:block;color:var(--mut);font-size:14px}
.cmpw{overflow-x:auto;margin:14px 0 0}
.cmp{width:100%;border-collapse:collapse;font-size:14px}
.cmp caption{text-align:left;padding:0 0 6px 12px;font:400 16px/1.3 var(--serif)}
.cmp caption .mono{margin-right:8px;color:var(--mut)}
.cmp th,.cmp td{padding:5px 4px;border-bottom:1px solid var(--rule);vertical-align:top;font-weight:400;text-align:left}
.cmp thead th{border-bottom:2px solid var(--ink);vertical-align:bottom}
.cmp thead th.c{font-family:var(--mono);font-size:12px;word-break:break-all;text-align:right}
.cmp thead th.c.sel{color:var(--red);box-shadow:inset 0 -3px 0 var(--red)}
.cmp tbody th{padding-left:12px;color:var(--mut)}
.cmp td{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.cmp td.sel{background:#ece6d8}
.cmpnote{margin:6px 0 0 12px}
.rn{margin:18px 0 0;padding-left:12px}
.big{font:400 48px/1.05 var(--serif)}
.cap{color:var(--mut);font-size:14px}
.bar{height:5px;background:var(--rule);margin:6px 0 4px}.bar i{display:block;height:100%;background:var(--green)}.bar.bad i{background:var(--red)}
.rn a{display:block;margin-bottom:16px;text-decoration:none}
.rn a:hover .big{text-decoration:underline}
#tabs{display:flex;flex-wrap:wrap;border-bottom:1px solid var(--rule);margin-bottom:22px}
#tabs button{background:none;border:0;border-bottom:3px solid transparent;padding:10px 16px 9px 0;margin-right:18px;cursor:pointer;font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
#tabs button[aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
h2.q{font:400 24px/1.25 var(--serif);margin:0 0 16px}
h3.mono{font-weight:400;margin:26px 0 8px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:0 36px}
.tile{border-top:1px solid var(--rule);padding:14px 0 18px}
.tile .pair{display:flex;gap:30px;flex-wrap:wrap;align-items:flex-end}
.how{font-family:var(--mono);font-size:12px;color:var(--mut);margin:8px 0 0;line-height:1.5}
.tile p{margin:6px 0 0}
table.data{width:100%;border-collapse:collapse;margin:8px 0 0}
table.data caption{text-align:left;padding:0 0 8px;font:400 19px/1.3 var(--serif)}
table.data caption .mono{margin-right:10px;color:var(--mut)}
table.data th{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:2px solid var(--ink);padding:6px 8px;font-weight:400}
table.data td{border-bottom:1px solid var(--rule);padding:7px 8px;vertical-align:top}
table.data .r{text-align:right}
table.data td.num{font-variant-numeric:tabular-nums}
tr.prow{cursor:pointer}tr.prow:hover{background:#ece6d8}
.rowbtn{background:none;border:0;padding:0 2px;cursor:pointer;color:var(--red);font:inherit;font-weight:600;font-variant-numeric:tabular-nums}
.src{font-family:var(--mono);font-size:12px;color:var(--mut);margin:8px 0 0}
.pd{padding:6px 4px 14px;max-width:880px}
.ptext{font-size:17px;line-height:1.6;margin:8px 0 12px}
mark.sus{background:#f3d3d3;color:var(--ink);padding:0 2px}
.path{margin:2px 0 0;color:var(--mut)}
pre.lines,.raw{font:12.5px/1.5 var(--mono);white-space:pre-wrap;margin:8px 0;background:#fffdf8;border:1px solid var(--rule);padding:8px 10px;overflow:auto;max-height:420px}
.pg{color:var(--red)}
dl.kv{display:grid;grid-template-columns:150px 1fr;gap:4px 12px;margin:12px 0}
dl.kv dt{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);padding-top:3px}
dl.kv dd{margin:0}
.tgl,.btn,button.head{background:none;border:1px solid var(--ink);padding:5px 12px;cursor:pointer;font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.btn.pri{background:var(--ink);color:var(--paper)}
button.head{border:0;border-bottom:1px solid var(--ink);padding:6px 0;width:100%;text-align:left;font-size:13px}
button.head::before{content:"+ "}button.head[aria-expanded=true]::before{content:"\2212  "}
.tgl:hover,.btn:hover{background:#ece6d8}.btn.pri:hover{background:#000}
.copied{margin-left:10px;font-family:var(--mono);font-size:12px}
.box{border:1px solid var(--rule);padding:4px 12px 10px;margin:0 0 14px;background:#faf7f0}
.box ol{margin:6px 0 0;padding-left:22px}
.checks{list-style:none;padding:0;margin:0}
.checks>li{border-top:1px solid var(--rule);padding:9px 0}
.ch{display:grid;grid-template-columns:130px 170px 1fr;gap:4px 14px}
.st{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;font-weight:700;padding-top:3px}
.st.pass{color:var(--green)}.st.fail{color:var(--red)}.st.info,.st.notrun{color:var(--ink)}
.items{margin:6px 0 0 144px;padding-left:18px;font-size:14px}
.items button,.lnk{background:none;border:0;padding:0;text-decoration:underline;cursor:pointer;font:inherit}
.steps{font-size:14px;color:var(--mut);margin:10px 0 0;padding-left:20px}
.kinds{display:flex;flex-wrap:wrap;gap:4px 22px;margin:8px 0 12px;font-family:var(--mono);font-size:12px}
td.mn,.mn{font-family:var(--mono);font-size:12px;word-break:break-word}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-family:var(--mono);font-size:12px;margin:8px 0}
.legend span{padding:1px 8px}
.rl{display:grid;grid-template-columns:3em 1.6em 1fr;gap:0 6px;padding:0 4px}
.rl .ln{color:var(--mut);text-align:right}
.c-cover{background:#e7e2f0}.c-header{background:#dce9f2}.c-heading{background:#f1e3c3}.c-paragraph{background:#fffdf8}.c-suspect{background:#f3d3d3}.c-footer{background:#dbe8d9}.c-blank{background:#f4f0e8;color:var(--mut)}.c-unk{background:#fff;outline:2px solid var(--red)}
footer.foot{border-top:1px solid var(--rule);padding:14px 0 28px;color:var(--mut);font-size:14px}
footer.foot p{margin:2px 0}
@media (max-width:860px){.layout{grid-template-columns:1fr;gap:18px}.tiles{grid-template-columns:1fr}.ch{grid-template-columns:1fr}.items{margin-left:18px}h1{font-size:27px}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <div class="mono sm">UN DOCUMENT · PDF TEXT</div>
  <div class="hrow">
    <div>
      <h1 id="title">Paragraphs out of a PDF</h1>
      <p class="meta" id="meta"></p>
      <p class="what">This page splits the converter's text into its numbered paragraphs, removes headers and footers, flags the pages where footnote text may sit inside a paragraph, checks itself against the document's own reference and lists every repair.</p>
    </div>
    <div class="status" id="status" role="status"></div>
  </div>
</div></header>
<div class="wrap layout">
  <aside id="rail" aria-label="Document"></aside>
  <main>
    <div id="tabs" role="tablist" aria-label="Views"></div>
    <section id="p1" role="tabpanel" aria-labelledby="t1" hidden></section>
    <section id="p2" role="tabpanel" aria-labelledby="t2" hidden></section>
    <section id="p3" role="tabpanel" aria-labelledby="t3" hidden></section>
    <section id="p4" role="tabpanel" aria-labelledby="t4" hidden></section>
  </main>
</div>
<footer class="foot"><div class="wrap" id="foot"></div></footer>
<script>
(function(){
'use strict';
const WD=window.WORKSHOP_DATA||{};
const KIND={header:'header line removed',footer:'footer line removed',bare:'bare number removed from the footer',split:'number and text split',join:'paragraph joined across a page break',hsep:'heading separated from paragraph text',hjoin:'heading title joined from two lines'};
const REASON={num:'starts with a number and a space',bare:'bare number',star:'starts with an asterisk and a space',long:'paragraph over 300 words'};
const CODE={cover:'C',header:'H',heading:'T',paragraph:'P',suspect:'S',footer:'F'};
const START=/^(\d{1,3})\.(?: (.+))?$/, LABEL=/^([IVX]+|[A-Z])\.$/;
const ABBR=new Set(['no.','nos.','art.','arts.','para.','paras.','p.','pp.','vol.','ch.','chap.','sec.','sect.','res.','cf.','fig.','e.g.','i.e.','rev.','add.','s.','ss.']);
const $=s=>document.querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const cut=(s,n)=>{s=String(s);if(s.length<=n)return s;let c=s.slice(0,n);const k=c.lastIndexOf(' ');if(k>n*.5)c=c.slice(0,k);return c.replace(/[\s,;:]+$/,'')+'…';};
const safeUrl=u=>/^https?:\/\//i.test(u||'')?u:'';
const pl=(n,w)=>n+' '+w+(n===1?'':/(ch|s|x)$/.test(w)?'es':'s');
const num=v=>(v===null||v===undefined||v===''||!isFinite(Number(v)))?null:Number(v);
const normW=s=>String(s).replace(/[“”„‟]/g,'"').replace(/[‘’‚‛]/g,"'").replace(/[–—‑‐−]/g,'-').replace(/\s+/g,' ').trim();
const endsSentence=t=>/[.;:,\d]$/.test(t.replace(/[”’"']+$/,''));
const headLike=t=>t.length<=90&&/^[A-Z]/.test(t)&&!endsSentence(t);
const susReason=t=>/^\d{1,3}$/.test(t)?'bare':/^\d{1,3} (?:[A-Z]|["“”‘’'])/.test(t)?'num':/^\* /.test(t)?'star':null;

/* Footnote marks removed from the first six words only */
function firstWords(text,n){
  const toks=text.split(/\s+/).filter(Boolean),out=[];let prev='';
  for(let i=0;i<toks.length&&out.length<n;i++){
    let w=toks[i];const raw=w;let m;
    if(/^\d{1,3}$/.test(w)){
      const pa=prev.toLowerCase().replace(/^[("“‘']+/,'');
      if(prev&&/[.,”’"']$/.test(prev)&&!ABBR.has(pa)&&!/^\d+,$/.test(prev)){prev=raw;continue;}
    }else if(w.indexOf('/')<0){
      if((m=/^(.*[.,;:?!”’"')])(\d{1,3})$/.exec(w))&&!/\d[.,]$/.test(m[1])&&!ABBR.has(m[1].toLowerCase().replace(/^[("“‘']+/,'')))w=m[1];
      else if((m=/^([A-Za-zÀ-ɏ][a-zß-ɏ]{2,})\d{1,3}$/.exec(w)))w=m[1];
    }
    out.push(w);prev=raw;
  }
  return out;
}

function analyse(D){
  const symbol=String(D.symbol||'');
  const recs=(D.records||[]).filter(r=>r&&typeof r.text==='string').map((r,i)=>({page:num(r.page)==null?i+1:num(r.page),text:r.text})).sort((a,b)=>a.page-b.page);
  const ref=D.reference&&typeof D.reference==='object'?D.reference:null;
  const R={paragraphs:ref?num(ref.paragraphs):null,footnotes:ref?num(ref.footnotes):null,fw:ref&&ref.first_words&&typeof ref.first_words==='object'?ref.first_words:null,adopted:ref&&ref.adopted?String(ref.adopted):''};
  const repairs=[],warnings=[],rawPages=[],body=[],pageStat=[],paras=[],heads=[],pending=[];
  let total=0;
  const rep=(o,p)=>{o.para=p?p.number:null;repairs.push(o);if(p)p.repairs.push(o);};
  recs.forEach(r=>{
    const pl_=r.text.split(/\r?\n/).map((s,i)=>({page:r.page,ln:i+1,t:s.trim(),cls:s.trim()===''?'blank':null,sus:null,pt:null}));
    rawPages.push({page:r.page,lines:pl_});
    total+=pl_.filter(l=>l.t!=='').length;
    const st={page:r.page,header:false,pageNo:false,bare:[]};pageStat.push(st);
    const first=pl_.findIndex(l=>l.t!=='');
    if(first>=0&&symbol&&pl_[first].t===symbol){
      pl_[first].cls='header';st.header=true;
      rep({page:r.page,ln:pl_[first].ln,kind:KIND.header,before:pl_[first].t,after:'(removed)'});
    }else warnings.push('Page '+r.page+': the first line is not the symbol, so no header was removed.');
    const lo=st.header?first:-1;
    for(let k=pl_.length-1;k>lo;k--){
      const l=pl_[k],t=l.t;if(t==='')continue;
      let note;
      if(/^GE\./.test(t))note='job code';
      else if(/^\d{6}(?:\s+\d{6})*$/.test(t))note='date stamp';
      else if(/^\d{1,3}$/.test(t)){if(!st.pageNo&&+t===r.page){st.pageNo=true;note='page number';}else note='bare';}
      else break;
      l.cls='footer';
      if(note==='bare'){st.bare.push(t);rep({page:r.page,ln:l.ln,kind:KIND.bare,before:t,after:'(removed; the footnote is not put back)'});}
      else rep({page:r.page,ln:l.ln,kind:KIND.footer,before:t,after:'(removed: '+note+')'});
    }
    pl_.forEach(l=>{if(l.cls===null)body.push(l);});
  });

  /* split into paragraphs and headings */
  let cur=null,hR=null,hL=null,hP=null,started=false,foot=false,lastPage=null;
  const mkHead=(kind,text,page,ln)=>{const h={kind,text,page,ln,next:null};heads.push(h);pending.push(h);};
  for(let i=0;i<body.length;i++){
    const L=body[i],t=L.t;let m;
    if(lastPage!==L.page){foot=false;lastPage=L.page;}
    if((m=LABEL.exec(t))){
      const roman=/^[IVX]+$/.test(m[1]);
      L.cls='heading';started=true;foot=false;
      const parts=[];let j=i+1;
      while(j<body.length){
        const B=body[j];
        if(LABEL.test(B.t)||START.test(B.t)||B.t.length>120||parts.length>=6)break;
        B.cls='heading';
        if(parts.length&&/^[a-z(]/.test(B.t)){const q=parts[parts.length-1];rep({page:B.page,ln:B.ln,kind:KIND.hjoin,before:q.text+' | '+B.t,after:q.text+' '+B.t});q.text+=' '+B.t;}
        else parts.push({text:B.t,page:B.page,ln:B.ln});
        j++;
      }
      i=j-1;cur=null;
      const first=parts.shift(),label=m[1]+'.',text=first?label+' '+first.text:label;
      mkHead(roman?'roman':'letter',text,L.page,L.ln);
      if(roman){hR=text;hL=null;hP=null;}else{hL=text;hP=null;}
      parts.forEach(q=>{mkHead('plain',q.text,q.page,q.ln);hP=q.text;});
      continue;
    }
    if((m=START.exec(t))){
      L.cls='paragraph';started=true;foot=false;
      cur={number:+m[1],lines:[],repairs:[],part:hR||'',sect:[hR,hL,hP].filter(Boolean),startPage:L.page};
      paras.push(cur);pending.forEach(h=>{h.next=cur.number;});pending.length=0;
      if(m[2]){L.pt=m[2].trim();cur.lines.push(L);rep({page:L.page,ln:L.ln,kind:KIND.split,before:t,after:m[1]+'. | '+L.pt},cur);}
      continue;
    }
    if(!started||!cur){L.cls='cover';continue;}
    if(foot)L.sus='follows';
    else{const r=susReason(t);if(r){foot=true;L.sus=r;}}
    if(!L.sus&&i+1<body.length&&START.test(body[i+1].t)){
      const prev=cur.lines.length?cur.lines[cur.lines.length-1]:null;
      const prevOk=!!prev&&!prev.sus&&headLike(prev.pt);
      const own=headLike(t),tail=/^[a-z(]/.test(t)&&t.length<=90&&!endsSentence(t);
      if(own||(tail&&prevOk)){
        const two=prevOk,tailText=cur.lines.length>(two?1:0)?cur.lines[cur.lines.length-(two?2:1)].pt:'';
        const text=two?prev.pt+' '+t:t;
        if(two){cur.lines.pop();prev.cls='heading';}
        L.cls='heading';
        rep({page:L.page,ln:L.ln,kind:KIND.hsep,before:'… '+tailText.slice(-30)+' '+text,after:'heading: '+text},cur);
        if(two)rep({page:L.page,ln:L.ln,kind:KIND.hjoin,before:prev.pt+' | '+t,after:text},cur);
        mkHead('plain',text,two?prev.page:L.page,two?prev.ln:L.ln);hP=text;
        continue;
      }
    }
    L.cls='paragraph';L.pt=t;cur.lines.push(L);
  }

  let hyphen=0;
  paras.forEach(p=>{
    const ls=p.lines;
    p.text=ls.map(l=>l.pt).join(' ').replace(/ {2,}/g,' ').trim();
    p.textRaw=ls.map(l=>l.t).join(' | ');
    p.pageStart=ls.length?ls[0].page:p.startPage;
    p.pageEnd=ls.length?ls[ls.length-1].page:p.startPage;
    p.words=p.text?p.text.split(/\s+/).length:0;
    p.sus=ls.filter(l=>l.sus).map(l=>({page:l.page,ln:l.ln,text:l.t,reason:l.sus}));
    p.long=p.words>300;p.flagged=p.sus.length>0||p.long;
    p.flagPage=p.sus.length?p.sus[0].page:p.pageStart;
    p.section=p.sect.length?p.sect[p.sect.length-1]:'';
    ls.forEach((l,k)=>{
      if(/-$/.test(l.pt))hyphen++;
      if(k&&l.page!==ls[k-1].page)rep({page:l.page,ln:l.ln,kind:KIND.join,before:'…'+ls[k-1].pt.slice(-30)+' [p. '+ls[k-1].page+' | p. '+l.page+'] '+l.pt.slice(0,30)+'…',after:'one paragraph, pages '+ls[k-1].page+'–'+l.page},p);
    });
    p.fwFound=firstWords(p.text,6).join(' ');
    p.fwRef=R.fw&&R.fw[String(p.number)]!=null?String(R.fw[String(p.number)]):null;
    p.fwMatch=p.fwRef==null?null:normW(p.fwFound)===normW(p.fwRef);
    p.citation=symbol+', para. '+p.number;
  });
  repairs.sort((a,b)=>a.page-b.page||a.ln-b.ln);

  const fpm=new Map();
  const fp=pg=>{if(!fpm.has(pg))fpm.set(pg,{page:pg,paras:[],sus:[],reasons:new Set()});return fpm.get(pg);};
  paras.forEach(p=>{
    p.sus.forEach(s=>{const e=fp(s.page);if(e.paras.indexOf(p.number)<0)e.paras.push(p.number);e.sus.push(s);if(s.reason!=='follows')e.reasons.add(s.reason);});
    if(p.long){const e=fp(p.pageStart);if(e.paras.indexOf(p.number)<0)e.paras.push(p.number);e.reasons.add('long');}
  });
  const A={D,symbol,R,rawPages,pageStat,paras,heads,repairs,warnings,hyphen,total,flagPages:[...fpm.values()].sort((a,b)=>a.page-b.page)};
  A.pages=rawPages.length;
  A.fwMatches=paras.filter(p=>p.fwMatch===true).length;
  A.flaggedParas=paras.filter(p=>p.flagged).length;
  A.checks=buildChecks(A);
  const cc=A.checks.filter(c=>c.status!=='info');
  A.m=cc.length;A.nPass=cc.filter(c=>c.status==='pass').length;A.nFail=cc.filter(c=>c.status==='fail').length;A.nNot=cc.filter(c=>c.status==='notrun').length;
  return A;
}

function buildChecks(A){
  const P=A.paras,R=A.R,C=[],n=P.length;
  const add=(id,name,status,line,items)=>C.push({id,name,status,line,items:items||[]});
  /* paragraph count */
  if(R.paragraphs==null)add('count','Paragraph count','notrun','found '+n+'; the file has no reference count');
  else{const d=n-R.paragraphs;add('count','Paragraph count',d===0?'pass':'fail','found '+n+' / reference '+R.paragraphs+(d?' (difference '+(d>0?'+':'')+d+')':''));}
  /* numbering */
  const seen={},dup=[],bad=[],gaps=[];
  P.forEach((p,i)=>{if(seen[p.number])dup.push(p);seen[p.number]=1;if(p.number!==i+1&&bad.length<8)bad.push({p,i});});
  const max=P.reduce((a,p)=>Math.max(a,p.number),0);
  for(let v=1;v<=max;v++)if(!seen[v])gaps.push(v);
  const it=[];
  gaps.forEach(v=>{const b=P.filter(p=>p.number<v).pop();it.push({t:'gap: no paragraph '+v+(b?' (after para. '+b.number+', page '+b.pageEnd+')':''),go:b?'para:'+b.number:null});});
  dup.forEach(p=>it.push({t:'duplicate: para. '+p.number+', page '+p.pageStart,go:'para:'+p.number}));
  if(!gaps.length&&!dup.length)bad.forEach(o=>it.push({t:'out of order: position '+(o.i+1)+' holds para. '+o.p.number+', page '+o.p.pageStart,go:'para:'+o.p.number}));
  const okNum=n>0&&P.every((p,i)=>p.number===i+1);
  add('num','Numbering',okNum?'pass':'fail',(n?'expected 1 to '+n+' in order; found '+P[0].number+' to '+P[n-1].number:'no paragraph found')+'; '+pl(gaps.length,'gap')+', '+pl(dup.length,'duplicate'),it);
  /* first words */
  if(!R.fw)add('fw','First words','notrun','the file has no first_words reference');
  else{
    const mis=P.filter(p=>p.fwMatch===false),nor=P.filter(p=>p.fwMatch===null);
    const miss=Object.keys(R.fw).filter(k=>!P.some(p=>String(p.number)===k));
    const it3=mis.map(p=>({t:'para. '+p.number+': found “'+p.fwFound+'” / reference “'+p.fwRef+'”',go:'para:'+p.number}));
    nor.forEach(p=>it3.push({t:'para. '+p.number+': no reference entry',go:'para:'+p.number}));
    miss.forEach(k=>it3.push({t:'reference has para. '+k+'; the app found no such paragraph',go:null}));
    add('fw','First words',it3.length?'fail':'pass',A.fwMatches+' of '+n+' paragraphs found start with the reference’s six words; '+pl(mis.length,'mismatch'),it3);
  }
  /* suspect lines */
  const sl=[].concat(...P.map(p=>p.sus)),slPages=new Set(sl.map(s=>s.page)),slParas=P.filter(p=>p.sus.length);
  const kept=P.every(p=>p.sus.every(s=>p.text.indexOf(s.text.trim())>=0));
  add('sus','Suspect lines',kept?'pass':'fail',pl(sl.length,'suspect line')+' on '+pl(slPages.size,'page')+', in '+pl(slParas.length,'paragraph')+'; '+(kept?'none was removed':'some are missing from the text'));
  /* flagged pages */
  add('flag','Pages flagged',A.flagPages.length?'info':'pass',pl(A.flagPages.length,'page')+' of '+A.pages+' flagged; a flag is not a failure, it says “check this against the PDF”',A.flagPages.map(e=>({t:'page '+e.page+', para. '+e.paras.join(', ')+(e.reasons.has('long')?' (over 300 words)':''),go:'page:'+e.page})));
  /* headers and footers */
  const hdr=A.pageStat.filter(s=>s.header).length,pn=A.pageStat.filter(s=>s.pageNo).length;
  const it6=A.warnings.map(w=>({t:w,go:null}));
  A.pageStat.forEach(s=>s.bare.forEach(b=>it6.push({t:'page '+s.page+': bare number '+b+' removed from the footer (not put back)',go:'raw:'+s.page})));
  add('hf','Headers and footers',hdr===A.pages&&pn>=A.pages-1&&A.pages>0?'pass':'fail',hdr+' of '+A.pages+' pages start with the symbol; '+pn+' page numbers found, '+Math.max(A.pages-1,0)+' expected; '+pl(A.pageStat.reduce((a,s)=>a+s.bare.length,0),'bare number')+' removed',it6);
  /* headings */
  const lab=A.heads.filter(h=>h.kind!=='plain').length,unl=A.heads.filter(h=>h.kind==='plain');
  add('head','Headings','info',lab+' labelled and '+unl.length+' unlabelled; check that no heading is a paragraph’s last line',unl.map(h=>({t:'page '+h.page+': “'+h.text+'”',go:h.next!=null?'para:'+h.next:null})));
  /* nothing lost */
  const cnt={cover:0,header:0,heading:0,paragraph:0,footer:0},unk=[];let s2=0;
  A.rawPages.forEach(pg=>pg.lines.forEach(l=>{if(l.t==='')return;if(cnt[l.cls]!==undefined){cnt[l.cls]++;s2++;}else unk.push(l);}));
  add('lost','Nothing lost',!unk.length&&s2===A.total?'pass':'fail',s2+' of '+A.total+' non-empty lines classified: cover '+cnt.cover+', header '+cnt.header+', heading '+cnt.heading+', paragraph '+cnt.paragraph+' (suspect '+sl.length+'), footer '+cnt.footer,unk.map(l=>({t:'page '+l.page+', line '+l.ln+': “'+cut(l.t,60)+'”',go:'raw:'+l.page})));
  return C;
}

/* ---------- state and views ---------- */
const keys=Object.keys(WD).filter(k=>{const d=WD[k];return d&&typeof d==='object'&&Array.isArray(d.records)&&d.records.length&&d.records.every(r=>r&&typeof r.text==='string'&&r.page!=null);});
const cache={};let sel=0,tab=1;
const an=i=>{const k=keys[i];if(!cache[k]){try{cache[k]=analyse(WD[k]);}catch(e){cache[k]={err:String(e&&e.message||e),D:WD[k]};}}return cache[k];};
const cur=()=>an(sel);
const rng=p=>p.pageStart===p.pageEnd?String(p.pageStart):p.pageStart+'–'+p.pageEnd;
const link=(go,txt,cls)=>'<a href="#" data-go="'+esc(go)+'"'+(cls?' class="'+cls+'"':'')+'>'+txt+'</a>';

function compare(){
  if(keys.length<2)return '';
  const B=keys.map((k,i)=>an(i));
  const cell=(i,txt,bad)=>'<td class="'+(i===sel?'sel':'')+(bad?' bad':'')+'">'+txt+'</td>';
  const row=(lab,f)=>'<tr><th scope="row">'+lab+'</th>'+B.map((b,i)=>b.err?cell(i,'–',false):f(b,i)).join('')+'</tr>';
  const head=keys.map((k,i)=>'<th scope="col" class="c'+(i===sel?' sel':'')+'">'+esc(WD[k].symbol||k)+(i===sel?'<span class="sr"> (selected)</span>':'')+'</th>').join('');
  const body=row('Paragraphs found',(b,i)=>cell(i,b.paras.length,b.R.paragraphs!=null&&b.paras.length!==b.R.paragraphs))
    +row('Paragraphs in the reference',(b,i)=>cell(i,b.R.paragraphs!=null?b.R.paragraphs:'none',false))
    +row('Pages flagged',(b,i)=>cell(i,b.flagPages.length+' of '+b.pages,b.flagPages.length>0))
    +row('Checks passed',(b,i)=>cell(i,b.nPass+' of '+b.m,b.nFail>0));
  const bad=B.some(b=>b.err)?'<p class="how bad cmpnote">A document marked “–” could not be read.</p>':'';
  return '<div class="cmpw"><table class="cmp"><caption><span class="mono">TAB.05</span>The documents side by side</caption><thead><tr><th scope="col"><span class="sr">Measure</span></th>'+head+'</tr></thead><tbody>'+body+'</tbody></table></div>'
    +'<p class="how cmpnote">Same pipeline for every document, no rule changed. Red: count differs from the reference, pages flagged, or a check failed.</p>'+bad;
}
function rail(A){
  const D=A.D,R=A.R||{};
  const cards=keys.map((k,i)=>{
    const d=WD[k],inner='<span class="sym">'+esc(d.symbol||k)+'</span><span class="st2 ser">'+esc(d.short_title||cut(d.title||'',60))+'</span><span class="sub">'+(i===sel&&R.adopted?'adopted '+esc(R.adopted)+' · ':'')+pl((d.records||[]).length,'page')+'</span>';
    return keys.length>1?'<button class="card'+(i===sel?' sel':'')+'" data-doc="'+i+'"'+(i===sel?' aria-pressed="true"':' aria-pressed="false"')+'>'+inner+'</button>':'<div class="card sel">'+inner+'</div>';
  }).join('');
  if(A.err)return '<h2 class="mono">DOCUMENT</h2>'+cards+compare();
  const n=A.paras.length,hasR=R.paragraphs!=null,eq=hasR&&n===R.paragraphs;
  const share=hasR&&R.paragraphs>0?Math.min(100,Math.round(n/R.paragraphs*100)):0;
  return '<h2 class="mono">DOCUMENT</h2>'+cards+compare()+'<div class="rn"><div><div class="big">'+n+'</div><div class="cap">paragraphs'+(hasR?' of '+R.paragraphs:' · no reference in this file')+'</div>'+(hasR?'<div class="bar'+(eq?'':' bad')+'" role="img" aria-label="'+share+' percent of the reference count found"><i style="width:'+share+'%"></i></div>':'')+'</div>'
   +'<a href="#" data-go="tab:3" style="margin-top:16px"><div class="big'+(A.flagPages.length?' bad':'')+'">'+A.flagPages.length+'</div><div class="cap">pages flagged of '+A.pages+'</div></a>'
   +'<a href="#" data-go="tab:4"><div class="big" style="font-size:34px">'+A.nPass+' of '+A.m+'</div><div class="cap">checks pass'+(A.nNot?' · '+A.nNot+' not run':'')+'</div></a></div>';
}

function tile(lab,big,extra,how){return '<article class="tile"><div class="mono sm">'+lab+'</div>'+big+extra+'<p class="how">How this is computed: '+how+'</p></article>';}
function tab1(A){
  const R=A.R,n=A.paras.length,hasR=R.paragraphs!=null,d=hasR?n-R.paragraphs:0;
  const t1=tile('PARAGRAPHS FOUND','<div class="pair"><div><div class="big">'+n+'</div><div class="cap">found</div></div><div><div class="big '+(!hasR?'':d===0?'ok':'bad')+'">'+(hasR?R.paragraphs:'–')+'</div><div class="cap">the document has</div></div></div>',
    (hasR?(d===0?'<p class="ok">Same count.</p>':'<p class="bad">'+Math.abs(d)+' '+(d<0?'fewer':'more')+' than the document has.</p>'):'<p>No reference in this file.</p>')+(A.flaggedParas?'<p class="bad">'+A.flaggedParas+' may contain footnote text.</p>':''),
    'every line that is a number and a full stop (“12.” alone, or “12. Text”) starts a paragraph; the reference is the document’s own count.');
  const t2=tile('PAGES FLAGGED','<div class="big'+(A.flagPages.length?' bad':'')+'">'+A.flagPages.length+'<span class="cap"> of '+A.pages+' pages</span></div>',
    (A.flagPages.length?'<p>Footnote text may sit inside a paragraph; '+link('tab:3','see tab 03')+'.</p>':'<p class="ok">No page has suspect lines.</p>')+'<p>'+(R.footnotes!=null?'The document has '+R.footnotes+' footnotes; this version does not separate them.':'This version does not separate footnotes.')+'</p>',
    'a page is flagged when a line inside a paragraph is a bare number or starts with a number, a space and a capital letter; the rest of that page is then suspect.');
  const t3=tile('FIRST WORDS MATCH','<div class="big">'+(R.fw?A.fwMatches:'–')+'<span class="cap"> of '+(R.paragraphs!=null?R.paragraphs:'?')+'</span></div>',R.fw?(A.fwMatches===R.paragraphs?'<p class="ok">Every paragraph starts as the reference says.</p>':'<p class="bad">'+(A.paras.length-A.fwMatches)+' found paragraphs differ or have no reference entry.</p>'):'<p>No reference in this file.</p>',
    'the first six words of each paragraph, footnote marks removed, against the reference’s words; quotes and dashes are normalised, case is kept.');
  const t4=tile('REPAIRS MADE','<div class="big">'+A.repairs.length+'</div>','<p>'+link('repairs','Open the repair log')+'</p>','every line the script removed, split or joined, one entry each; nothing is changed silently.');
  const note=hasR&&d===0&&A.flagPages.length?'<p>The count is right, but footnote text may still sit inside some paragraphs. Check the flagged ones against the PDF before you quote them.</p>':'';
  return '<h2 class="q">Did the app find everything the document has?</h2><div class="tiles">'+t1+t2+t3+t4+'</div>'+note;
}

function tab2(A){
  const R=A.R,P=A.paras,hasR=R.paragraphs!=null;
  const rows=P.map(p=>{
    const c=[];
    if(p.fwMatch===false)c.push('<span class="bad">first words differ</span>');
    if(p.flagged)c.push(link('page:'+p.flagPage,'may contain footnote text','bad'));
    if(!c.length)c.push(p.fwMatch===null?'<span class="mut">no reference</span>':'OK');
    return '<tr class="prow"><td class="r num"><button class="rowbtn" aria-expanded="false" aria-controls="d'+p.number+'">'+p.number+'</button></td><td>'+esc(p.section||'–')+'</td><td class="r num">'+rng(p)+'</td><td>'+esc(cut(p.text,120)||'(empty)')+'</td><td>'+c.join('<br>')+'</td></tr><tr id="d'+p.number+'" data-n="'+p.number+'" hidden><td colspan="5"></td></tr>';
  }).join('');
  const hd=A.heads.map(h=>'<li>'+esc(h.text)+' <span class="sm">· page '+h.page+(h.kind==='plain'?' · unlabelled':'')+(h.next!=null?' · '+link('para:'+h.next,'before para. '+h.next):'')+'</span></li>').join('');
  return '<h2 class="q">What does each paragraph say, and how do I cite it?</h2>'
   +'<div class="box"><h3 style="margin:0"><button class="head" data-toggle="hbox" aria-expanded="false" aria-controls="hbox">Headings found: '+A.heads.length+'</button></h3><div id="hbox" hidden><p class="how">Headings are kept out of the paragraph text. Unlabelled ones were found by their position just before a paragraph number.</p>'+(hd?'<ol>'+hd+'</ol>':'<p>No headings found.</p>')+'</div></div>'
   +(P.length?'<table class="data"><caption><span class="mono">TAB.01</span>'+P.length+' paragraphs found, '+(hasR?R.paragraphs+' expected':'no reference in this file')+'</caption><thead><tr><th scope="col" class="r">No.</th><th scope="col">Section</th><th scope="col" class="r">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody>'+rows+'</tbody></table><p class="src">Source: '+esc(A.symbol)+', raw text of '+pl(A.pages,'page')+'. Click a row to read the paragraph and copy its citation.</p>':'<p>No numbered paragraph was found in this text.</p>');
}

function rawLines(pg){
  return pg.lines.map(l=>{
    const k=l.t===''?'blank':l.sus?'suspect':(l.cls&&CODE[l.cls]?l.cls:'unk');
    return '<div class="rl c-'+k+'"><span class="ln">'+l.ln+'</span><span class="code" aria-label="'+k+'">'+(k==='blank'?'':k==='unk'?'?':CODE[k])+'</span><span>'+esc(l.t)+'</span></div>';
  }).join('');
}
const legend='<div class="legend" aria-label="Legend"><span class="c-cover">C cover</span><span class="c-header">H header</span><span class="c-heading">T heading</span><span class="c-paragraph">P paragraph</span><span class="c-suspect">S suspect line</span><span class="c-footer">F footer</span></div>';

function tab3(A){
  const F=A.flagPages;
  if(!F.length)return '<h2 class="q">Which paragraphs should I check against the PDF?</h2><p>No page is flagged: no line inside a paragraph looks like footnote text.</p>';
  const rows=F.map(e=>{
    const why=[...e.reasons].map(r=>REASON[r]).join('; ');
    const first=e.sus.length?'<span class="mn">'+esc(cut(e.sus[0].text,36))+'</span>':'–';
    return '<tr class="prow"><td class="r num"><button class="rowbtn" aria-expanded="false" aria-controls="f'+e.page+'">'+e.page+'</button></td><td class="r num">'+e.paras.join(', ')+'</td><td>'+e.sus.length+(e.sus.length?' · first: '+first:'')+'</td><td>'+esc(why||'follows a suspect line')+'</td></tr><tr id="f'+e.page+'" data-page="'+e.page+'" hidden><td colspan="4"></td></tr>';
  }).join('');
  return '<h2 class="q">Which paragraphs should I check against the PDF?</h2>'
   +'<p>This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF. The next step can separate them.</p>'
   +'<p class="how">A <b>suspect line</b> is a line inside a paragraph that looks like a footnote: a bare number, a number and a capital letter, or an asterisk. The rest of that page is suspect too. A <b>flagged page</b> has at least one.</p>'
   +'<table class="data"><caption><span class="mono">TAB.02</span>'+F.length+' of '+A.pages+' pages flagged</caption><thead><tr><th scope="col" class="r">Page</th><th scope="col" class="r">Paragraph</th><th scope="col">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>'+rows+'</tbody></table><p class="src">Source: '+esc(A.symbol)+', raw text. Suspect lines stay in the paragraph text; none is removed.</p>';
}

function tab4(A){
  const st={pass:'PASS',fail:'CHECK FAILED',info:'FLAGGED',notrun:'NOT RUN'};
  const chk=A.checks.map(c=>{
    const lim=c.items.slice(0,14);
    const li=lim.map(i=>'<li>'+(i.go?'<button data-go="'+esc(i.go)+'">'+esc(i.t)+'</button>':esc(i.t))+'</li>').join('')+(c.items.length>14?'<li>and '+(c.items.length-14)+' more</li>':'');
    return '<li><div class="ch"><span class="st '+c.status+'">'+(c.status==='info'&&c.id==='head'?'FOR INFORMATION':st[c.status])+'</span><strong>'+c.name+'</strong><span>'+esc(c.line)+'</span></div>'+(li?'<ul class="items">'+li+'</ul>':'')+'</li>';
  }).join('');
  const kinds=Object.keys(KIND).map(k=>'<span>'+KIND[k]+': <b>'+A.repairs.filter(r=>r.kind===KIND[k]).length+'</b></span>').join('');
  const rl=A.repairs.map(r=>'<tr><td class="r num">'+r.page+'</td><td>'+(r.para!=null?'para. '+r.para:'page')+'</td><td>'+esc(r.kind)+'</td><td class="mn" title="'+esc(r.before)+'">'+esc(cut(r.before,110))+'</td><td class="mn" title="'+esc(r.after)+'">'+esc(cut(r.after,110))+'</td></tr>').join('');
  const opts=A.rawPages.map((p,i)=>'<option value="'+i+'">'+p.page+'</option>').join('');
  return '<h2 class="q">Can I trust this, and can I take it away?</h2>'
   +'<h3 class="mono">CHECKS · TAB.04</h3><ul class="checks">'+chk+'</ul>'
   +'<ol class="steps"><li>Header and footer lines are removed page by page; every page’s remaining lines are joined in page order.</li><li>A line like “12.” or “12. Text” starts a paragraph; roman and lettered lines open headings.</li><li>Unlabelled headings are lines just before a paragraph number that look like titles.</li><li>Lines are joined with one space; '+pl(A.hyphen,'line')+' ended with a hyphen, none was joined.</li><li>Footnote text is not separated; it is flagged.</li></ol>'
   +'<h3 style="margin:24px 0 0"><button class="head" data-toggle="replog" aria-expanded="false" aria-controls="replog" id="replogbtn">Repair log ('+A.repairs.length+')</button></h3><div id="replog" hidden><div class="kinds">'+kinds+'</div><table class="data"><caption><span class="mono">TAB.03</span>'+A.repairs.length+' repairs, in document order</caption><thead><tr><th scope="col" class="r">Page</th><th scope="col">Paragraph or footnote</th><th scope="col">What was done</th><th scope="col">Before</th><th scope="col">After</th></tr></thead><tbody>'+rl+'</tbody></table></div>'
   +'<h3 style="margin:18px 0 0"><button class="head" data-toggle="rawbox" aria-expanded="false" aria-controls="rawbox" id="rawbtn">Raw pages</button></h3><div id="rawbox" hidden><p><label>Show raw page <select id="rawsel">'+opts+'</select></label></p>'+legend+'<div class="raw" id="rawview" tabindex="0"></div><p class="how">Each line is coloured by what the script decided it was, and carries a letter code. A red outline marks a line that no rule classified.</p></div>'
   +'<h3 class="mono">DOWNLOAD</h3><button class="btn pri" id="csv">Download paragraphs as CSV</button><span class="copied" id="csvmsg" role="status"></span>';
}

function paraDetail(A,p){
  const th=p.lines.map(l=>{const s=esc(l.pt).replace(/ {2,}/g,' ');return l.sus?'<mark class="sus">'+s+'</mark>':s;}).join(' ');
  let lp=null,pre='';
  p.lines.forEach(l=>{if(l.page!==lp){pre+='<span class="pg">── page '+l.page+(lp==null?'':' begins')+' ──</span>\n';lp=l.page;}pre+=(l.sus?'<mark class="sus">'+esc(l.t)+'</mark>':esc(l.t))+'\n';});
  const reps=p.repairs.length?'<ul style="margin:0;padding-left:18px">'+p.repairs.map(r=>'<li>'+esc(r.kind)+' <span class="sm">(page '+r.page+')</span></li>').join('')+'</ul>':'none';
  const fw=p.fwRef==null?'no reference entry':'reference “'+esc(p.fwRef)+'”<br>found “'+esc(p.fwFound)+'” · '+(p.fwMatch?'<b class="ok">equal</b>':'<b class="bad">different</b>');
  return '<div class="pd"><div class="path mono">'+esc(p.sect.join(' › ')||'no heading above')+'</div><p class="ptext">'+(th||'(no text)')+'</p>'
   +(p.sus.length?'<p class="how bad">Highlighted: '+pl(p.sus.length,'suspect line')+' that may be footnote text. Check this paragraph against the PDF.</p>':'')+(p.long?'<p class="how bad">'+p.words+' words: longer than 300, check it against the PDF.</p>':'')
   +'<button class="tgl" data-lines="1" aria-expanded="false">Show the PDF’s lines</button><pre class="lines" hidden>'+pre+'</pre>'
   +'<dl class="kv"><dt>First words</dt><dd>'+fw+'</dd><dt>Page(s)</dt><dd>'+rng(p)+'</dd><dt>Repairs</dt><dd>'+reps+'</dd></dl>'
   +'<button class="btn" data-copy="'+esc(p.citation)+'">Copy citation</button> <code>'+esc(p.citation)+'</code><span class="copied" role="status"></span></div>';
}
function pageDetail(A,e){
  const pg=A.rawPages.find(x=>x.page===e.page);
  return '<div class="pd" style="max-width:none"><p>Paragraph'+(e.paras.length>1?'s':'')+' the suspect lines sit in: '+e.paras.map(n=>link('para:'+n,'para. '+n)).join(', ')+'. Highlighted lines are suspect.</p>'+legend+'<div class="raw">'+(pg?rawLines(pg):'')+'</div></div>';
}

/* ---------- interaction ---------- */
function setTab(n,focus){
  tab=n;
  document.querySelectorAll('#tabs button').forEach(b=>{const on=+b.dataset.tab===n;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;if(on&&focus)b.focus();});
  [1,2,3,4].forEach(i=>{const p=$('#p'+i);p.hidden=i!==n;if(i===n)p.tabIndex=0;else p.removeAttribute('tabindex');});
}
function toggle(btn,force){
  const open=force===undefined?btn.getAttribute('aria-expanded')!=='true':force;
  btn.setAttribute('aria-expanded',open);
  const t=document.getElementById(btn.getAttribute('aria-controls'));
  if(t)t.hidden=!open;
  if(open&&t&&t.id==='rawbox')showRaw(+$('#rawsel').value);
  return t;
}
function toggleRow(tr,force){
  const btn=tr.querySelector('button[aria-expanded]');if(!btn)return;
  const det=toggle(btn,force);
  if(det&&!det.hidden&&!det.dataset.built){
    const A=cur();
    det.firstElementChild.innerHTML=det.dataset.n?paraDetail(A,A.paras.find(p=>String(p.number)===det.dataset.n)):pageDetail(A,A.flagPages.find(e=>String(e.page)===det.dataset.page));
    det.dataset.built='1';
  }
}
function showRaw(i){const A=cur(),pg=A.rawPages[i];if(pg)$('#rawview').innerHTML=rawLines(pg);}
function go(spec){
  const [k,v]=spec.split(':');let el=null;
  if(k==='tab'){setTab(+v);return;}
  if(k==='para'){setTab(2);const b=document.querySelector('button[aria-controls="d'+v+'"]');if(b){const tr=b.closest('tr');if(b.getAttribute('aria-expanded')!=='true')toggleRow(tr,true);el=b;}}
  if(k==='page'){setTab(3);const b=document.querySelector('button[aria-controls="f'+v+'"]');if(b){const tr=b.closest('tr');if(b.getAttribute('aria-expanded')!=='true')toggleRow(tr,true);el=b;}}
  if(k==='repairs'){setTab(4);el=$('#replogbtn');toggle(el,true);}
  if(k==='raw'){setTab(4);const b=$('#rawbtn');toggle(b,true);const A=cur();const i=A.rawPages.findIndex(p=>String(p.page)===v);if(i>=0){$('#rawsel').value=i;showRaw(i);}el=$('#rawview');}
  if(el){el.scrollIntoView({block:'center'});el.focus();}
}
function copyText(txt,done){
  const fb=()=>{try{const ta=document.createElement('textarea');ta.value=txt;ta.style.cssText='position:fixed;opacity:0';document.body.appendChild(ta);ta.select();const ok=document.execCommand('copy');ta.remove();return ok;}catch(e){return false;}};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(txt).then(()=>done(true),()=>done(fb()));else done(fb());
}
function downloadCsv(){
  const A=cur(),cols=['number','section','part','page_start','page_end','first_words_reference','first_words_found','first_words_match','text','text_raw','flagged','suspect_lines','repairs','citation','symbol','doc_url'];
  const q=v=>'"'+String(v==null?'':v).replace(/"/g,'""')+'"';
  const rows=A.paras.map(p=>[p.number,p.section,p.part,p.pageStart,p.pageEnd,p.fwRef==null?'':p.fwRef,p.fwFound,p.fwMatch==null?'':p.fwMatch,p.text,p.textRaw,p.flagged,p.sus.map(s=>'p.'+s.page+' l.'+s.ln+': '+s.text).join(' | '),p.repairs.map(r=>r.kind+' (p.'+r.page+')').join('; '),p.citation,A.symbol,A.D.doc_url||'']);
  const csv='﻿'+[cols].concat(rows).map(r=>r.map(q).join(',')).join('\r\n')+'\r\n';
  const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download=(A.symbol||'paragraphs').replace(/[\/\\]+/g,'-')+'.csv';document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),4000);
  $('#csvmsg').textContent=A.paras.length+' rows prepared. If nothing was saved, your browser blocked the download.';
}

document.addEventListener('click',e=>{
  const t=e.target;let x;
  if((x=t.closest('[data-go]'))){e.preventDefault();go(x.dataset.go);return;}
  if((x=t.closest('#tabs [data-tab]'))){setTab(+x.dataset.tab,true);return;}
  if((x=t.closest('[data-doc]'))){sel=+x.dataset.doc;render();const c=document.querySelector('[data-doc="'+sel+'"]');if(c)c.focus();return;}
  if((x=t.closest('[data-copy]'))){const m=x.parentNode.querySelector('.copied');copyText(x.dataset.copy,ok=>{m.textContent=ok?'Copied':'Not copied: select the text and press Ctrl+C';setTimeout(()=>{m.textContent='';},2000);});return;}
  if((x=t.closest('[data-lines]'))){const pre=x.nextElementSibling;const o=x.getAttribute('aria-expanded')!=='true';x.setAttribute('aria-expanded',o);pre.hidden=!o;x.textContent=o?'Hide the PDF’s lines':'Show the PDF’s lines';return;}
  if((x=t.closest('button[data-toggle]'))){toggle(x);return;}
  if(t.closest('#csv')){downloadCsv();return;}
  if((x=t.closest('tr.prow'))){toggleRow(x);}
});
document.addEventListener('change',e=>{if(e.target.id==='rawsel')showRaw(+e.target.value);});
document.addEventListener('keydown',e=>{
  if(!e.target.closest||!e.target.closest('#tabs'))return;
  const k=e.key,i=tab-1;let n=null;
  if(k==='ArrowRight'||k==='ArrowDown')n=(i+1)%4;else if(k==='ArrowLeft'||k==='ArrowUp')n=(i+3)%4;else if(k==='Home')n=0;else if(k==='End')n=3;
  if(n!==null){e.preventDefault();setTab(n+1,true);}
});

function render(){
  if(!keys.length){
    $('#title').textContent='No PDF text in this data';
    $('#meta').textContent='';
    $('#status').textContent='';
    $('main').innerHTML='<p>The workshop data has no document with pages of raw text (records with a page number and a text). Attach a PDF text file from “Your files” and build again.</p>';
    $('#foot').innerHTML='<p>Nothing was computed; no model was called and nothing left the browser.</p>';
    return;
  }
  const A=cur(),D=A.D,u=safeUrl(D.doc_url);
  if(A.err){
    $('#title').textContent=D.title||D.symbol||keys[sel];
    $('#meta').textContent=D.symbol||'';
    $('#status').innerHTML='<span class="dot bad"></span>could not be read';
    $('#rail').innerHTML=rail(A);
    $('#tabs').innerHTML='';
    [1,2,3,4].forEach(i=>{$('#p'+i).innerHTML='';});
    $('#p1').innerHTML='<p class="bad">This document could not be analysed: '+esc(A.err)+'. The other document is not affected; choose it in the rail.</p>';
    $('#foot').innerHTML='<p>Nothing was computed for this document; no model was called and nothing left the browser.</p>';
    setTab(1,false);
    return;
  }
  $('#title').textContent=D.title||A.symbol;
  $('#meta').innerHTML=(u?'<a href="'+esc(u)+'" target="_blank" rel="noopener">'+esc(A.symbol)+'</a>':esc(A.symbol))+(A.R.adopted?' · adopted '+esc(A.R.adopted):'')+' · '+pl(A.pages,'page')+' of raw converter text'+(D.source?' · '+esc(D.source):'');
  $('#status').innerHTML=A.nFail?'<span class="dot bad"></span>'+pl(A.nFail,'check')+' failed':'<span class="dot '+(A.nNot?'':'ok')+'"></span>'+A.nPass+' of '+A.m+' checks pass';
  $('#rail').innerHTML=rail(A);
  const names=['01 RESULT','02 PARAGRAPHS','03 FLAGGED PAGES','04 CHECKS &amp; METHOD'];
  $('#tabs').innerHTML=names.map((nm,i)=>'<button role="tab" id="t'+(i+1)+'" data-tab="'+(i+1)+'" aria-controls="p'+(i+1)+'" aria-selected="false" tabindex="-1">'+nm+(i===3&&A.nFail?' <span class="dot bad"></span><span class="sr">checks failed</span>':'')+'</button>').join('');
  $('#p1').innerHTML=tab1(A);$('#p2').innerHTML=tab2(A);$('#p3').innerHTML=tab3(A);$('#p4').innerHTML=tab4(A);
  $('#foot').innerHTML='<p>Source: '+esc(D.source||D.title||A.symbol)+(D.built?' · built '+esc(D.built):'')+'</p><p>Counting, splitting, matching and flagging are done by this page’s code; no model was called and nothing left the browser.</p>';
  setTab(tab,false);
}
render();
})();
</script>
</body>
</html>
```
