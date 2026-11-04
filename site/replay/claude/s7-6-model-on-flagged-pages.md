I added the button “Check the flagged pages with the model” at the top of tab 03, with a line saying how many pages will leave the browser (the flagged pages of both documents plus one unflagged control page each), progress and a Stop button. The model gets one page per call and returns only line numbers; the code cuts the text, takes the footnotes out where an answer passes your three tests, and the checks on tab 04 now count the footnotes against the reference. Tab 03 then shows, for each document, what the script found, what the model changed and the pages that still need a person.

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
[data-source=ai]{border-bottom:1px dotted var(--red)}
.mbox{border-top:1px solid var(--ink);border-bottom:1px solid var(--rule);padding:12px 0 14px;margin:0 0 18px}
.mbox p{margin:6px 0;max-width:820px}
.prog{height:6px;background:var(--rule);margin:8px 0 4px;max-width:520px}.prog i{display:block;height:100%;background:var(--red);width:0}
.btn{max-width:100%;white-space:normal;text-align:left}
.btn:disabled{opacity:.5;cursor:not-allowed}
table.data td ul{margin:0;padding-left:16px}
.c-footnote{background:#d6ebe6}
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
      <p class="what">This page splits the converter's text into its numbered paragraphs, removes headers and footers, flags the pages where footnote text may sit inside a paragraph, checks itself against the document's own reference and lists every repair. An optional model check on tab 03 can read the flagged pages.</p>
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
const KIND={header:'header line removed',footer:'footer line removed',bare:'bare number removed from the footer',split:'number and text split',join:'paragraph joined across a page break',hsep:'heading separated from paragraph text',hjoin:'heading title joined from two lines',fn:'footnote taken out of a paragraph (model’s line choice)'};
const REASON={num:'starts with a number and a space',bare:'bare number',star:'starts with an asterisk and a space',long:'paragraph over 300 words'};
const CODE={cover:'C',header:'H',heading:'T',paragraph:'P',suspect:'S',footer:'F',footnote:'N'};
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

/* Footnote marks in a run of paragraph text, same rules as for the first words */
function footMarks(text){
  const toks=text.split(/\s+/).filter(Boolean),out=[];let prev='';
  toks.forEach(w=>{
    let m,v=null;
    if(/^\d{1,3}$/.test(w)){
      const pa=prev.toLowerCase().replace(/^[("“‘']+/,'');
      if(prev&&/[.,”’"']$/.test(prev)&&!ABBR.has(pa)&&!/^\d+,$/.test(prev))v=+w;
    }else if(w.indexOf('/')<0){
      if((m=/^(.*[.,;:?!”’"')])(\d{1,3})$/.exec(w))&&!/\d[.,]$/.test(m[1])&&!ABBR.has(m[1].toLowerCase().replace(/^[("“‘']+/,'')))v=+m[2];
      else if((m=/^([A-Za-zÀ-ɏ][a-zß-ɏ]{2,})(\d{1,3})$/.exec(w)))v=+m[2];
    }
    if(v!==null)out.push(v);prev=w;
  });
  return out;
}

function analyse(D,fx,ms){
  const symbol=String(D.symbol||'');
  const recs=(D.records||[]).filter(r=>r&&typeof r.text==='string').map((r,i)=>({page:num(r.page)==null?i+1:num(r.page),text:r.text})).sort((a,b)=>a.page-b.page);
  const ref=D.reference&&typeof D.reference==='object'?D.reference:null;
  const R={paragraphs:ref?num(ref.paragraphs):null,footnotes:ref?num(ref.footnotes):null,fw:ref&&ref.first_words&&typeof ref.first_words==='object'?ref.first_words:null,adopted:ref&&ref.adopted?String(ref.adopted):''};
  const repairs=[],warnings=[],rawPages=[],body=[],pageStat=[],paras=[],heads=[],pending=[];
  let total=0;
  const rep=(o,p)=>{o.para=p?p.number:null;repairs.push(o);if(p)p.repairs.push(o);};
  recs.forEach(r=>{
    const pl_=r.text.split(/\r?\n/).map((s,i)=>({page:r.page,ln:i+1,t:s.trim(),cls:s.trim()===''?'blank':null,sus:null,pt:null,pn:null}));
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
  const fnOf={},fnGroups=[];
  Object.keys(fx||{}).forEach(pg=>{const m=new Map();fx[pg].groups.forEach(gr=>{const o={number:gr.number,lines:[],para:null};fnGroups.push(o);gr.lines.forEach(ln=>m.set(ln,o));});fnOf[pg]=m;});
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
      L.pn=cur.number;paras.push(cur);pending.forEach(h=>{h.next=cur.number;});pending.length=0;
      if(m[2]){L.pt=m[2].trim();cur.lines.push(L);rep({page:L.page,ln:L.ln,kind:KIND.split,before:t,after:m[1]+'. | '+L.pt},cur);}
      continue;
    }
    if(!started||!cur){L.cls='cover';continue;}
    const fg=fnOf[L.page]&&fnOf[L.page].get(L.ln);
    if(fg){L.cls='footnote';fg.lines.push(L);if(!fg.para)fg.para=cur;continue;}
    if(!fnOf[L.page]){
      if(foot)L.sus='follows';
      else{const r=susReason(t);if(r){foot=true;L.sus=r;}}
    }
    if(!L.sus&&i+1<body.length&&START.test(body[i+1].t)){
      const prev=cur.lines.length?cur.lines[cur.lines.length-1]:null;
      const prevOk=!!prev&&!prev.sus&&headLike(prev.pt);
      const own=headLike(t),tail=/^[a-z(]/.test(t)&&t.length<=90&&!endsSentence(t);
      if(own||(tail&&prevOk)){
        const two=prevOk,tailText=cur.lines.length>(two?1:0)?cur.lines[cur.lines.length-(two?2:1)].pt:'';
        const text=two?prev.pt+' '+t:t;
        if(two){cur.lines.pop();prev.cls='heading';prev.pn=null;}
        L.cls='heading';
        rep({page:L.page,ln:L.ln,kind:KIND.hsep,before:'… '+tailText.slice(-30)+' '+text,after:'heading: '+text},cur);
        if(two)rep({page:L.page,ln:L.ln,kind:KIND.hjoin,before:prev.pt+' | '+t,after:text},cur);
        mkHead('plain',text,two?prev.page:L.page,two?prev.ln:L.ln);hP=text;
        continue;
      }
    }
    L.cls='paragraph';L.pt=t;L.pn=cur.number;cur.lines.push(L);
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
  const fns=[];
  fnGroups.forEach(g=>{
    if(!g.lines.length)return;
    const t=g.lines.map(l=>l.t).join(' ').replace(/ {2,}/g,' ').replace(new RegExp('^'+g.number+'\\s+'),'').trim();
    const f={page:g.lines[0].page,ln:g.lines[0].ln,number:g.number,text:t,para:g.para?g.para.number:null};
    fns.push(f);
    rep({page:f.page,ln:f.ln,kind:KIND.fn,before:t,after:'footnote '+f.number+' taken out of para. '+f.para,ai:true},g.para);
  });
  fns.sort((a,b)=>a.page-b.page||a.ln-b.ln);
  repairs.sort((a,b)=>a.page-b.page||a.ln-b.ln);

  const fpm=new Map();
  const fp=pg=>{if(!fpm.has(pg))fpm.set(pg,{page:pg,paras:[],sus:[],reasons:new Set()});return fpm.get(pg);};
  paras.forEach(p=>{
    p.sus.forEach(s=>{const e=fp(s.page);if(e.paras.indexOf(p.number)<0)e.paras.push(p.number);e.sus.push(s);if(s.reason!=='follows')e.reasons.add(s.reason);});
    if(p.long){const e=fp(p.pageStart);if(e.paras.indexOf(p.number)<0)e.paras.push(p.number);e.reasons.add('long');}
  });
  const A={D,symbol,R,rawPages,pageStat,paras,heads,repairs,warnings,hyphen,total,fns,ms:ms||null,fnOn:Object.keys(fx||{}).length>0,flagPages:[...fpm.values()].sort((a,b)=>a.page-b.page)};
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
  const add=(id,name,status,line,items,x)=>C.push(Object.assign({id,name,status,line,items:items||[]},x||{}));
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
  add('sus','Suspect lines',kept?'pass':'fail',pl(sl.length,'suspect line')+' on '+pl(slPages.size,'page')+', in '+pl(slParas.length,'paragraph')+'; '+(kept?'none was removed':'some are missing from the text')+(A.fnOn?'; on the pages the model checked, footnote lines were taken out of the paragraphs (see Footnotes)':''));
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
  const cnt={cover:0,header:0,heading:0,paragraph:0,footer:0,footnote:0},unk=[];let s2=0;
  A.rawPages.forEach(pg=>pg.lines.forEach(l=>{if(l.t==='')return;if(cnt[l.cls]!==undefined){cnt[l.cls]++;s2++;}else unk.push(l);}));
  add('lost','Nothing lost',!unk.length&&s2===A.total?'pass':'fail',s2+' of '+A.total+' non-empty lines classified: cover '+cnt.cover+', header '+cnt.header+', heading '+cnt.heading+', paragraph '+cnt.paragraph+' (suspect '+sl.length+'), footer '+cnt.footer+(A.fnOn?', footnote (model) '+cnt.footnote:''),unk.map(l=>({t:'page '+l.page+', line '+l.ln+': “'+cut(l.t,60)+'”',go:'raw:'+l.page})));
  /* the model's control page and the footnotes */
  const ms=A.ms;
  if(!ms){
    add('ctl','Model control','info','not run yet; the button on tab 03 sends one unflagged page to the model and compares its answer with the script',[],{label:'NOT RUN YET'});
    add('fn','Footnotes','info',(R.footnotes!=null?'the document has '+R.footnotes+' footnotes; ':'')+'the script alone does not separate them; the model check on tab 03 counts them',[],{label:'NOT RUN YET'});
  }else{
    const c=ms.ctl;
    if(c.state==='none')add('ctl','Model control','info','this document has no unflagged page, so the model could not be tested on a page the script says is clean; its answers were accepted on the three page checks alone',[],{label:'NO CONTROL PAGE'});
    else if(c.state==='agree')add('ctl','Model control','pass','page '+c.page+' (not flagged): the model agrees with the script on every line and finds no footnote',[],{ai:true});
    else if(c.state==='unsent')add('ctl','Model control','notrun','the run was stopped before the control page was sent; no answer for this document was used',[],{ai:true});
    else add('ctl','Model control','fail','page '+c.page+' (not flagged): '+(c.state==='error'?'no usable answer':'the model disagrees with the script')+'; none of its answers for this document was used',c.diffs.map(t=>({t,go:null})),{ai:true});
    const acc=Object.keys(ms.pages).filter(k=>ms.pages[k].state==='accepted').length;
    const open=A.flagPages.map(e=>({t:'page '+e.page+': '+why(ms.pages[e.page]),go:'page:'+e.page}));
    const f=A.fns.length,nums=A.fns.map(x=>x.number).sort((a,b)=>a-b),top=nums.length?nums[nums.length-1]:0,miss=[];
    for(let v=1;v<=top;v++)if(nums.indexOf(v)<0)miss.push(v);
    const tail='; '+pl(acc,'page')+' accepted, '+pl(A.flagPages.length,'page')+' still flagged'+(miss.length?'; footnote numbers missing: '+miss.slice(0,12).join(', ')+(miss.length>12?' …':''):'');
    if(R.footnotes==null)add('fn','Footnotes','notrun','the accepted pages hold '+f+' footnotes; the file has no reference count'+tail,open,{ai:true});
    else{
      const d=f-R.footnotes;
      add('fn','Footnotes',d===0&&!open.length?'pass':'fail','footnotes taken out: '+f+' / reference '+R.footnotes+(d?' (difference '+(d>0?'+':'')+d+')':'')+tail,open,{ai:true});
    }
  }
  return C;
}
const why=m=>!m?'not checked by the model':m.state==='rejected'?'answer not accepted: '+m.reasons.slice(0,3).join('; ')+(m.reasons.length>3?' …':''):m.state==='error'?'no usable answer ('+m.err+')':m.state==='skipped'?'not sent: the model did not pass the control page':m.state==='unsent'?'not sent: the run was stopped':m.state==='accepted'?'accepted, but a paragraph is still over 300 words':'not checked by the model';

/* ---------- state and views ---------- */
const keys=Object.keys(WD).filter(k=>{const d=WD[k];return d&&typeof d==='object'&&Array.isArray(d.records)&&d.records.length&&d.records.every(r=>r&&typeof r.text==='string'&&r.page!=null);});
const cache={},fixed={},MS={};let sel=0,tab=1,RUN=null;
const base=i=>{const k=keys[i];if(!cache[k]){try{cache[k]=analyse(WD[k]);}catch(e){cache[k]={err:String(e&&e.message||e),D:WD[k]};}}return cache[k];};
const an=i=>{const b=base(i);return fixed[keys[i]]||b;};
const cur=()=>an(sel);
const rng=p=>p.pageStart===p.pageEnd?String(p.pageStart):p.pageStart+'–'+p.pageEnd;
const aiw=(r,h)=>r.ai?'<span data-source="ai">'+h+'</span>':h;
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
    (A.flagPages.length?'<p>Footnote text may sit inside a paragraph; '+link('tab:3','see tab 03')+'.</p>':'<p class="ok">No page has suspect lines.</p>')+'<p>'+(A.ms?'<span data-source="ai">The model check took out '+A.fns.length+' footnotes</span>'+(R.footnotes!=null?'; the document has '+R.footnotes+'. ':'. ')+link('tab:3','Details on tab 03'):R.footnotes!=null?'The document has '+R.footnotes+' footnotes; the script alone does not separate them.':'The script alone does not separate footnotes.')+'</p>',
    'a page is flagged when a line inside a paragraph is a bare number or starts with a number, a space and a capital letter; the rest of that page is then suspect. After a model check, pages whose answer passed the code’s tests are no longer flagged.');
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
    if(p.repairs.some(r=>r.ai))c.push('<span class="sm" data-source="ai">footnote text taken out</span>');
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
const legend='<div class="legend" aria-label="Legend"><span class="c-cover">C cover</span><span class="c-header">H header</span><span class="c-heading">T heading</span><span class="c-paragraph">P paragraph</span><span class="c-suspect">S suspect line</span><span class="c-footer">F footer</span><span class="c-footnote">N footnote (model)</span></div>';

function tab3(A){
  const F=A.flagPages,ms=A.ms,q='<h2 class="q">Which paragraphs should I check against the PDF?</h2>';
  const head=q+modelPanel()+modelResults();
  if(!F.length)return head+'<p>No page is flagged'+(ms?' after the model check: every flagged page passed the code’s tests':': no line inside a paragraph looks like footnote text')+'.</p>';
  const nc=ms?5:4;
  const rows=F.map(e=>{
    const wy=[...e.reasons].map(r=>REASON[r]).join('; ');
    const first=e.sus.length?'<span class="mn">'+esc(cut(e.sus[0].text,36))+'</span>':'–';
    const m=ms&&ms.pages[e.page];
    return '<tr class="prow"><td class="r num"><button class="rowbtn" aria-expanded="false" aria-controls="f'+e.page+'">'+e.page+'</button></td><td class="r num">'+e.paras.join(', ')+'</td><td>'+e.sus.length+(e.sus.length?' · first: '+first:'')+'</td><td>'+esc(wy||'follows a suspect line')+'</td>'+(ms?'<td>'+(m?STATE[m.state]:'–')+'</td>':'')+'</tr><tr id="f'+e.page+'" data-page="'+e.page+'" hidden><td colspan="'+nc+'"></td></tr>';
  }).join('');
  return head
   +(ms?'<p>These pages are still flagged: the model’s answer was not accepted, it was not asked, or a paragraph is still very long. Check their paragraphs against the PDF before you quote them.</p>'
       :'<p>The script alone does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF. The model check above can separate them.</p>')
   +'<p class="how">A <b>suspect line</b> is a line inside a paragraph that looks like a footnote: a bare number, a number and a capital letter, or an asterisk. The rest of that page is suspect too. A <b>flagged page</b> has at least one.</p>'
   +'<table class="data"><caption><span class="mono">TAB.02</span>'+F.length+' of '+A.pages+' pages flagged</caption><thead><tr><th scope="col" class="r">Page</th><th scope="col" class="r">Paragraph</th><th scope="col">Suspect lines</th><th scope="col">Why</th>'+(ms?'<th scope="col">Model</th>':'')+'</tr></thead><tbody>'+rows+'</tbody></table><p class="src">Source: '+esc(A.symbol)+', raw text. Suspect lines stay in the paragraph text unless the model check took them out.</p>';
}

function tab4(A){
  const st={pass:'PASS',fail:'CHECK FAILED',info:'FLAGGED',notrun:'NOT RUN'};
  const chk=A.checks.map(c=>{
    const lim=c.items.slice(0,14);
    const li=lim.map(i=>'<li>'+(i.go?'<button data-go="'+esc(i.go)+'">'+esc(i.t)+'</button>':esc(i.t))+'</li>').join('')+(c.items.length>14?'<li>and '+(c.items.length-14)+' more</li>':'');
    return '<li><div class="ch"><span class="st '+c.status+'">'+(c.label||(c.status==='info'&&c.id==='head'?'FOR INFORMATION':st[c.status]))+'</span><strong>'+c.name+'</strong><span'+(c.ai?' data-source="ai"':'')+'>'+esc(c.line)+'</span></div>'+(li?'<ul class="items">'+li+'</ul>':'')+'</li>';
  }).join('');
  const kinds=Object.keys(KIND).map(k=>'<span>'+KIND[k]+': <b>'+A.repairs.filter(r=>r.kind===KIND[k]).length+'</b></span>').join('');
  const rl=A.repairs.map(r=>'<tr><td class="r num">'+r.page+'</td><td>'+(r.para!=null?'para. '+r.para:'page')+'</td><td>'+esc(r.kind)+'</td><td class="mn" title="'+esc(r.before)+'">'+aiw(r,esc(cut(r.before,110)))+'</td><td class="mn" title="'+esc(r.after)+'">'+aiw(r,esc(cut(r.after,110)))+'</td></tr>').join('');
  const opts=A.rawPages.map((p,i)=>'<option value="'+i+'">'+p.page+'</option>').join('');
  return '<h2 class="q">Can I trust this, and can I take it away?</h2>'
   +'<h3 class="mono">CHECKS · TAB.04</h3><ul class="checks">'+chk+'</ul>'
   +'<ol class="steps"><li>Header and footer lines are removed page by page; every page’s remaining lines are joined in page order.</li><li>A line like “12.” or “12. Text” starts a paragraph; roman and lettered lines open headings.</li><li>Unlabelled headings are lines just before a paragraph number that look like titles.</li><li>Lines are joined with one space; '+pl(A.hyphen,'line')+' ended with a hyphen, none was joined.</li><li>'+(A.fnOn?'Footnote text is taken out only on pages where the model’s line choice passed the code’s tests; on other pages it is flagged.':'Footnote text is not separated; it is flagged.')+'</li></ol>'
   +'<h3 style="margin:24px 0 0"><button class="head" data-toggle="replog" aria-expanded="false" aria-controls="replog" id="replogbtn">Repair log ('+A.repairs.length+')</button></h3><div id="replog" hidden><div class="kinds">'+kinds+'</div><table class="data"><caption><span class="mono">TAB.03</span>'+A.repairs.length+' repairs, in document order</caption><thead><tr><th scope="col" class="r">Page</th><th scope="col">Paragraph or footnote</th><th scope="col">What was done</th><th scope="col">Before</th><th scope="col">After</th></tr></thead><tbody>'+rl+'</tbody></table></div>'
   +'<h3 style="margin:18px 0 0"><button class="head" data-toggle="rawbox" aria-expanded="false" aria-controls="rawbox" id="rawbtn">Raw pages</button></h3><div id="rawbox" hidden><p><label>Show raw page <select id="rawsel">'+opts+'</select></label></p>'+legend+'<div class="raw" id="rawview" tabindex="0"></div><p class="how">Each line is coloured by what the script decided it was, and carries a letter code. A red outline marks a line that no rule classified.</p></div>'
   +'<h3 class="mono">DOWNLOAD</h3><button class="btn pri" id="csv">Download paragraphs as CSV</button><span class="copied" id="csvmsg" role="status"></span>';
}

function paraDetail(A,p){
  const th=p.lines.map(l=>{const s=esc(l.pt).replace(/ {2,}/g,' ');return l.sus?'<mark class="sus">'+s+'</mark>':s;}).join(' ');
  let lp=null,pre='';
  p.lines.forEach(l=>{if(l.page!==lp){pre+='<span class="pg">── page '+l.page+(lp==null?'':' begins')+' ──</span>\n';lp=l.page;}pre+=(l.sus?'<mark class="sus">'+esc(l.t)+'</mark>':esc(l.t))+'\n';});
  const reps=p.repairs.length?'<ul style="margin:0;padding-left:18px">'+p.repairs.map(r=>'<li>'+(r.ai?aiw(r,esc(r.kind+': '+cut(r.before,160)))+' ':esc(r.kind)+' ')+'<span class="sm">(page '+r.page+')</span></li>').join('')+'</ul>':'none';
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

/* ---------- the model check (only when the button is pressed) ---------- */
const STATE={accepted:'accepted',rejected:'not accepted',error:'no answer',skipped:'not sent',unsent:'not sent'};
const hasAsk=()=>typeof studio!=='undefined'&&studio&&typeof studio.ask==='function';
const lst=(a,n)=>a.slice(0,n||6).join(', ')+(a.length>(n||6)?' … ('+a.length+' in all)':'');
function controlPage(B){
  const fl=new Set(B.flagPages.map(e=>e.page));let best=null,bn=-1;
  B.rawPages.forEach(pg=>{if(fl.has(pg.page))return;const n=pg.lines.filter(l=>l.cls==='paragraph').length;if(n>bn){bn=n;best=pg;}});
  return best;
}
function plan(){
  const docs=[];let flagged=0,controls=0,chars=0;
  keys.forEach((k,i)=>{
    const B=base(i);if(B.err||!B.flagPages.length)return;
    const f=B.flagPages.map(e=>B.rawPages.find(p=>p.page===e.page)),c=controlPage(B);
    docs.push({k,i,B,control:c,flagged:f});flagged+=f.length;controls+=c?1:0;
    f.concat(c?[c]:[]).forEach(pg=>{chars+=pg.lines.reduce((a,l)=>a+l.t.length+1,0);});
  });
  return {docs,flagged,controls,pages:flagged+controls,chars};
}
function prevPara(B,page){let v=null;B.rawPages.forEach(pg=>{if(pg.page<page)pg.lines.forEach(l=>{if(l.cls==='paragraph'&&l.pn!=null)v=l.pn;});});return v;}
function pagePrompt(B,pg){
  const pv=prevPara(B,pg.page);
  return 'Below is page '+pg.page+' of the UN document '+B.symbol+', as raw text from a PDF converter. Each line has a number, a colon and the text of the line (nothing after the colon for a blank line). The converter mixed numbered paragraphs, footnotes, page headers and footers, and headings.\n\n'
   +'Assign every line number to exactly one of three groups. Answer with line numbers only. Never retype, quote, correct or shorten any text.\n'
   +'1. "paragraphs": the numbered paragraphs of the document. For each, give its paragraph number and all the lines that hold its text, including the line that carries the number itself ("12." alone, or "12. Text"). A footnote mark inside a paragraph (a small number glued to a word, like "waste.2") stays on its paragraph line.'+(pv!=null?' Lines at the top of the page before the first paragraph number continue paragraph '+pv+' from the page before: give them the number '+pv+'.':'')+'\n'
   +'2. "footnotes": the footnotes at the foot of the page. For each, give its footnote number and the lines of its text, including a line that holds only its number. If the converter moved a footnote number away from its text to a bare number among the last lines of the page, give that number to the footnote text that has none, and put the bare number line under "other".\n'
   +'3. "other": page headers, page numbers, job codes, date stamps, headings (a roman numeral or letter with its title, or a short title line just before a paragraph), cover text before the first numbered paragraph, and all blank lines.\n\n'
   +'Every line number from 1 to '+pg.lines.length+' must appear exactly once. Reply with JSON only, in this form (the numbers are only an example of the format): {"paragraphs":[{"number":7,"lines":[4,5,6]}],"footnotes":[{"number":2,"lines":[30,31]}],"other":[1,2,3,29,32]}\n\n'
   +pg.lines.map(l=>l.ln+': '+l.t).join('\n');
}
function jsonOf(raw){
  if(raw&&typeof raw==='object')return raw;
  const t=String(raw==null?'':raw).trim().replace(/^\x60{3}(?:json)?\s*/i,'').replace(/\x60{3}\s*$/,'');
  try{return JSON.parse(t);}catch(e){const a=t.indexOf('{'),b=t.lastIndexOf('}');if(a>=0&&b>a)try{return JSON.parse(t.slice(a,b+1));}catch(e2){}}
  return null;
}
function toLines(a){
  const out=[];
  (Array.isArray(a)?a:[]).forEach(v=>{
    const m=/^\s*(\d+)\s*(?:[-–]\s*(\d+))?\s*$/.exec(String(v));
    if(!m){out.push(NaN);return;}
    const x=+m[1],y=m[2]?+m[2]:x;
    if(y<x||y-x>300){out.push(NaN);return;}
    for(let j=x;j<=y;j++)out.push(j);
  });
  return out;
}
function readAnswer(raw){
  const o=jsonOf(raw);
  if(!o||typeof o!=='object'||Array.isArray(o))return {err:'the answer is not valid JSON'};
  if(!Array.isArray(o.paragraphs)||!Array.isArray(o.other))return {err:'the answer lacks the “paragraphs” or “other” list'};
  const grp=a=>(Array.isArray(a)?a:[]).map(g=>({number:Number(g&&g.number),lines:toLines(g&&g.lines)}));
  const r={paras:grp(o.paragraphs),fns:grp(o.footnotes),other:toLines(o.other)};
  const all=[].concat(r.other,...r.paras.map(g=>g.lines),...r.fns.map(g=>g.lines));
  if(all.some(Number.isNaN)||r.paras.concat(r.fns).some(g=>!Number.isInteger(g.number)||g.number<1))return {err:'a number in the answer is not a whole number'};
  return {a:r};
}
/* Compare one answer with the page: coverage, the script's own classification, the footnote rules. */
function judge(pg,a){
  const N=pg.lines.length,use=Array(N+1).fill(0),kind=Array(N+1).fill(''),pn=Array(N+1).fill(null);
  const res={cov:[],dis:[],fnr:[],groups:[],fnLines:[]};
  const put=(arr,k,num)=>arr.forEach(n=>{if(n<1||n>N){res.cov.push('line '+n+' does not exist');return;}use[n]++;kind[n]=k;pn[n]=num;});
  a.paras.forEach(g=>put(g.lines,'p',g.number));a.fns.forEach(g=>put(g.lines,'f',g.number));put(a.other,'o',null);
  const miss=[],dup=[];
  for(let n=1;n<=N;n++){if(!use[n])miss.push(n);else if(use[n]>1)dup.push(n);}
  if(miss.length)res.cov.push('lines not used: '+lst(miss));
  if(dup.length)res.cov.push('lines used twice: '+lst(dup));
  if(res.cov.length)return res;
  const bad={para:[],num:[],hf:[],head:[]};let lastP=0,firstF=N+1;const txt=[];
  for(let n=1;n<=N;n++){
    const L=pg.lines[n-1];if(L.t==='')continue;const k=kind[n];
    if(k==='p'){lastP=n;txt.push(L.t);}
    if(k==='f'){res.fnLines.push(n);if(n<firstF)firstF=n;}
    if(L.cls==='paragraph'){if(k==='o')bad.para.push(n);else if(k==='p'&&pn[n]!==L.pn)bad.num.push(n);}
    else if(L.cls==='header'||L.cls==='footer'){if(k==='p')bad.hf.push(n);}
    else if(k!=='o')bad.head.push(n);
  }
  if(bad.para.length)res.dis.push('lines '+lst(bad.para)+': paragraph text that the model put under “other”');
  if(bad.num.length)res.dis.push('lines '+lst(bad.num)+': a paragraph number that differs from the script’s');
  if(bad.hf.length)res.dis.push('lines '+lst(bad.hf)+': header or footer lines put in paragraph text');
  if(bad.head.length)res.dis.push('lines '+lst(bad.head)+': heading or cover lines put in a paragraph or a footnote');
  if(firstF<lastP)res.fnr.push('footnote text on line '+firstF+' sits above paragraph text on line '+lastP);
  a.fns.forEach(g=>{
    const nb=g.lines.filter(n=>pg.lines[n-1]&&pg.lines[n-1].t!=='');
    if(!nb.length)res.fnr.push('footnote '+g.number+' has no text lines');else res.groups.push({number:g.number,lines:g.lines.slice(),first:Math.min.apply(null,nb)});
  });
  res.groups.sort((x,y)=>x.first-y.first);
  for(let i=1;i<res.groups.length;i++)if(res.groups[i].number!==res.groups[i-1].number+1){res.fnr.push('footnote numbers are not in sequence ('+res.groups[i-1].number+', then '+res.groups[i].number+')');break;}
  const have=new Set(res.groups.map(g=>g.number)),lost=[];
  footMarks(txt.join(' ')).forEach(m=>{if(!have.has(m)&&lost.indexOf(m)<0)lost.push(m);});
  if(lost.length)res.fnr.push('footnote mark'+(lost.length>1?'s ':' ')+lost.join(', ')+' in the paragraph text '+(lost.length>1?'have':'has')+' no footnote on this page');
  return res;
}
async function ask(B,pg){
  if(RUN.stop)return {skip:true};
  RUN.sent++;paint();
  try{
    const raw=await studio.ask(pagePrompt(B,pg),{json:true});
    RUN.got++;paint();
    return readAnswer(raw);
  }catch(e){RUN.got++;RUN.fail++;paint();return {err:String(e&&e.message||e)};}
}
async function pool(list,n,fn){
  let i=0;
  const w=async()=>{while(i<list.length&&!RUN.stop){const t=list[i++];await fn(t);}};
  await Promise.all(Array.from({length:Math.min(n,list.length)},w));
}
function newMs(d){
  const ms={ctl:{state:d.control?'unsent':'none',page:d.control?d.control.page:null,diffs:[]},pages:{},trusted:false};
  d.flagged.forEach(pg=>{ms.pages[pg.page]={role:'flagged',state:'unsent',reasons:[],fns:[],ans:null};});
  return ms;
}
async function runDoc(d){
  const B=d.B,ms=MS[d.k]=newMs(d);
  RUN.doc=B.symbol;paint();
  if(d.control){
    const r=await ask(B,d.control),c=ms.ctl;
    if(r.skip)c.state='unsent';
    else if(r.err){c.state='error';c.diffs=[r.err];}
    else{
      const j=judge(d.control,r.a);
      c.diffs=j.cov.concat(j.dis);
      if(!c.diffs.length&&j.fnLines.length)c.diffs.push('the model finds footnote text on lines '+lst(j.fnLines)+', where the script finds none');
      c.state=c.diffs.length?'disagree':'agree';
    }
    ms.trusted=c.state==='agree';
  }else ms.trusted=true;
  if(ms.trusted)await pool(d.flagged,3,async pg=>{const r=await ask(B,pg);if(!r.skip)ms.pages[pg.page].ans=r;});
  finalize(d);
}
/* Pages in order: accept or reject each answer, footnote numbers must continue from the page before. */
function finalize(d){
  const ms=MS[d.k],fx={};
  let last=0,open=false;
  d.flagged.forEach(pg=>{
    const m=ms.pages[pg.page],r=m.ans;
    if(!ms.trusted){m.state=ms.ctl.state==='unsent'||ms.ctl.state==='none'?'unsent':'skipped';open=true;return;}
    if(!r){m.state='unsent';open=true;return;}
    if(r.err){m.state='error';m.err=r.err;open=true;return;}
    const j=judge(pg,r.a),bad=j.cov.concat(j.dis);
    if(!bad.length){
      j.fnr.forEach(t=>bad.push(t));
      const g=j.groups;
      if(g.length){
        if(!open&&g[0].number!==last+1)bad.push('footnote numbers should continue at '+(last+1)+' but start at '+g[0].number);
        else if(open&&g[0].number<=last)bad.push('footnote numbers start at '+g[0].number+', not after '+last+' (the last accepted number)');
      }
    }
    if(bad.length){m.state='rejected';m.reasons=bad;open=true;return;}
    m.state='accepted';m.fns=j.groups;
    fx[pg.page]={groups:j.groups};
    if(j.groups.length)last=j.groups[j.groups.length-1].number;
  });
  try{fixed[d.k]=analyse(WD[d.k],fx,ms);}catch(e){delete fixed[d.k];ms.error=String(e&&e.message||e);}
}
async function runModel(){
  if((RUN&&RUN.on)||!hasAsk())return;
  const P=plan();if(!P.pages)return;
  RUN={on:true,stop:false,total:P.pages,sent:0,got:0,fail:0,doc:'',msg:''};
  P.docs.forEach(d=>{delete fixed[d.k];delete MS[d.k];});
  render();
  for(const d of P.docs){
    if(RUN.stop)break;
    try{await runDoc(d);}catch(e){RUN.fail++;}
  }
  P.docs.forEach(d=>{if(!MS[d.k]){MS[d.k]=newMs(d);finalize(d);}});
  RUN.on=false;
  RUN.msg=(RUN.stop?'Stopped. ':'Done. ')+pl(RUN.sent,'page')+' left the browser'+(RUN.fail?'; '+RUN.fail+' call'+(RUN.fail===1?'':'s')+' failed':'')+'. The results are below and on every tab.';
  render();
  const h=$('#modelres');if(h)h.scrollIntoView({block:'start'});
}
function paint(){
  const el=$('#runstat');if(!el||!RUN)return;
  const pct=RUN.total?Math.round(RUN.got/RUN.total*100):0;
  el.innerHTML=RUN.on?'Sent '+RUN.sent+' of '+RUN.total+' pages · '+RUN.got+' answers back'+(RUN.fail?' · '+RUN.fail+' failed':'')+(RUN.doc?' · now: '+esc(RUN.doc):'')+(RUN.stop?' · stopping: no new page is sent':'')+'<div class="prog" aria-hidden="true"><i style="width:'+pct+'%"></i></div>':esc(RUN.msg||'');
}
function modelPanel(){
  const P=plan(),running=RUN&&RUN.on;
  let h='<div class="mbox"><div class="mono sm">MODEL CHECK · OPTIONAL · SLOW AND IT COSTS MONEY</div>';
  if(!P.pages)return h+'<p>No page is flagged in any document, so there is nothing to send to the model.</p><div id="runstat" role="status" class="how"></div></div>';
  h+='<p><b>'+pl(P.pages,'page')+' will leave the browser</b>: '+pl(P.flagged,'flagged page')+' and '+pl(P.controls,'control page')+' (one page per document that the script did not flag), from '+pl(P.docs.length,'document')+', about '+Math.max(1,Math.round(P.chars/1000))+'k characters of raw converter text, one page per call.</p>'
   +'<p>The model is asked only which lines are paragraph text, footnotes, or headers, footers and blanks. It never retypes text: this page’s code cuts the text from the line numbers, takes the footnotes out of the paragraphs where its tests pass, and runs the checks again.</p>'
   +'<p class="how">Accepted only if every line is used exactly once, the footnote numbers continue from the page before, and every footnote mark in the paragraphs has its footnote. The control page is sent first: if the model disagrees with the script there, none of its answers for that document is used and the document’s other pages are not sent.</p>';
  if(!hasAsk())h+='<p class="bad">The model is not available in this preview, so the button is switched off.</p><button class="btn pri" disabled>Check the flagged pages with the model</button>';
  else h+=running?'<button class="btn" data-stop="1">Stop</button>':'<button class="btn pri" data-run="1">Check the flagged pages with the model</button>';
  return h+'<div id="runstat" role="status" aria-live="polite" class="how"></div></div>';
}
function ctlText(c){
  return c.state==='none'?'no unflagged page to test on':c.state==='agree'?'page '+c.page+' agrees with the script':c.state==='disagree'?'page '+c.page+' disagrees with the script, so the model was not used':c.state==='error'?'page '+c.page+': no usable answer, so the model was not used':'not sent';
}
const fnTxt=m=>{const n=m.fns.map(g=>g.number);return n.length?(n.length===1?n[0]:n[0]+'–'+n[n.length-1])+' ('+n.length+')':'–';};
function modelResults(){
  if(!keys.some(k=>MS[k]))return '';
  const rows=keys.map((k,i)=>{
    const B=base(i),ms=MS[k],F=an(i);
    const nm='<td><span class="mn">'+esc(B.symbol||k)+'</span></td>';
    if(B.err)return '<tr>'+nm+'<td colspan="3">could not be read</td></tr>';
    const sus=B.paras.reduce((a,p)=>a+p.sus.length,0),sp=B.paras.filter(p=>p.sus.length).length,rf=B.R.footnotes;
    const script=B.flagPages.length+' of '+B.pages+' pages flagged; '+pl(sus,'suspect line')+' in '+pl(sp,'paragraph')+'; footnotes not counted'+(rf!=null?' (the document has '+rf+')':'');
    if(!ms)return '<tr>'+nm+'<td>'+esc(script)+'</td><td colspan="2" class="mut">nothing flagged, nothing sent</td></tr>';
    const pg=Object.keys(ms.pages).map(x=>ms.pages[x]),cnt=st=>pg.filter(m=>m.state===st).length;
    const sent=cnt('accepted')+cnt('rejected')+cnt('error')+(['agree','disagree','error'].indexOf(ms.ctl.state)>=0?1:0);
    const model='<span data-source="ai">control: '+esc(ctlText(ms.ctl))+'<br>'+pl(sent,'page')+' sent, '+cnt('accepted')+' accepted, '+cnt('rejected')+' not accepted'+(cnt('error')?', '+cnt('error')+' without an answer':'')+'<br><b>'+F.fns.length+'</b> footnotes taken out of paragraphs'+(rf!=null?' (the document has '+rf+')':'')+'<br>pages flagged: '+B.flagPages.length+' → '+F.flagPages.length+'</span>';
    const need=F.flagPages.map(e=>e.page);
    return '<tr>'+nm+'<td>'+esc(script)+'</td><td>'+model+'</td><td>'+(need.length?pl(need.length,'page')+': '+esc(lst(need,30)):'none')+'</td></tr>';
  }).join('');
  let h='<div id="modelres" tabindex="-1"><table class="data"><caption><span class="mono">TAB.06</span>What the script found, what the model changed, what still needs a person</caption><thead><tr><th scope="col">Document</th><th scope="col">Script alone</th><th scope="col">After the model</th><th scope="col">Still needs a person</th></tr></thead><tbody>'+rows+'</tbody></table><p class="src">Dotted underline: a value that came from the model. Counting, accepting and cutting are done by this page’s code. “Still needs a person” are the pages that are still flagged.</p>';
  const k=keys[sel],ms=MS[k];
  if(ms){
    const r=[];
    if(ms.ctl.page!=null)r.push('<tr><td class="r num">'+ms.ctl.page+'</td><td>control</td><td>'+(ms.ctl.state==='agree'?'agrees':ms.ctl.state==='disagree'?'disagrees':ms.ctl.state==='error'?'no answer':'not sent')+'</td><td class="r num">–</td><td><span data-source="ai">'+esc(ms.ctl.diffs.join('; ')||(ms.ctl.state==='agree'?'same lines as the script, no footnote':''))+'</span></td></tr>');
    Object.keys(ms.pages).map(Number).sort((a,b)=>a-b).forEach(p=>{
      const m=ms.pages[p];
      r.push('<tr><td class="r num">'+p+'</td><td>flagged</td><td>'+STATE[m.state]+'</td><td class="r num"><span data-source="ai">'+fnTxt(m)+'</span></td><td><span data-source="ai">'+esc(m.state==='accepted'?pl(m.fns.length,'footnote')+' taken out':why(m))+'</span></td></tr>');
    });
    h+='<table class="data"><caption><span class="mono">TAB.07</span>'+esc((cache[k]||{}).symbol||k)+': page by page</caption><thead><tr><th scope="col" class="r">Page</th><th scope="col">Role</th><th scope="col">Model answer</th><th scope="col" class="r">Footnotes</th><th scope="col">Why</th></tr></thead><tbody>'+r.join('')+'</tbody></table><p class="src">Footnotes: the numbers the model gave, first to last, and how many. Choose the other document in the left rail to see its pages.</p>';
  }
  return h+'</div>';
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
  if((x=t.closest('[data-run]'))){runModel();return;}
  if((x=t.closest('[data-stop]'))){if(RUN){RUN.stop=true;paint();}return;}
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

function footTxt(){
  return RUN&&RUN.sent?'<p>A language model was called on '+pl(RUN.sent,'page')+' of raw converter text: those pages left the browser. It was asked only for line numbers. Counting, splitting, matching, flagging, accepting and cutting the text are done by this page’s code.</p>'
    :'<p>Counting, splitting, matching and flagging are done by this page’s code; no model has been called and nothing has left the browser. The button on tab 03 sends pages to a model only when you press it.</p>';
}
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
    $('#foot').innerHTML='<p>Nothing was computed for this document.</p>'+footTxt();
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
  $('#foot').innerHTML='<p>Source: '+esc(D.source||D.title||A.symbol)+(D.built?' · built '+esc(D.built):'')+'</p>'+footTxt();
  setTab(tab,false);
  paint();
}
render();
})();
</script>
</body>
</html>
```
