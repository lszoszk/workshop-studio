I built a checker that splits the General Comment's raw PDF text into its numbered paragraphs, removes headers and footers, and flags every page where footnote text may still sit inside a paragraph. It compares the result with the document's own reference (paragraph count and first words), lists every repair it made, and offers a CSV download. It uses only the attached text, runs offline and calls no model.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1f6b3a;--muted:#5a5448;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;--sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0}
body{background:var(--paper);color:var(--ink);font:16px/1.5 var(--sans)}
a{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
button{font:inherit;color:inherit}
.mono,.lab,th,.tab,.legend,.cap2{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.bad{color:var(--red)} .ok{color:var(--green)} .muted{color:var(--muted)}
.app{display:flex;flex-direction:column;min-height:100vh}
.top{display:flex;gap:24px;justify-content:space-between;align-items:flex-start;padding:14px 24px 12px;border-bottom:1px solid var(--rule)}
.top h1{font:400 26px/1.2 var(--serif);margin:4px 0}
.top p{margin:0}
.meta{font-size:14px}
.what{font-size:14px;color:var(--muted);max-width:95ch;margin-top:4px!important}
.status{display:flex;align-items:center;gap:8px;font:700 13px var(--mono);white-space:nowrap;padding-top:4px}
.dot{width:11px;height:11px;border-radius:50%;display:inline-block;background:var(--muted);flex:none}
.dot.ok{background:var(--green)} .dot.bad{background:var(--red)}
.mid{display:grid;grid-template-columns:290px minmax(0,1fr);flex:1;min-height:0}
.rail{border-right:1px solid var(--rule);padding:16px 18px}
.main{padding:0 24px 24px;min-width:0}
@media(min-width:900px) and (min-height:620px){.app{height:100vh}.rail,.main{overflow:auto}}
@media(max-width:899px){.mid{grid-template-columns:1fr}.rail{border-right:0;border-bottom:1px solid var(--rule)}.top{flex-direction:column;gap:8px}.main{padding:0 14px 24px}}
.rail h2{font:inherit;margin:0 0 10px}
.card{display:block;width:100%;text-align:left;background:none;border:0;border-left:4px solid transparent;border-bottom:1px solid var(--rule);padding:8px 10px;cursor:pointer}
.card[aria-pressed=true]{border-left-color:var(--red)}
.card .sym{font:600 13px var(--mono);display:block}
.card .sh{display:block;font-size:14px}
.card .ad{display:block;font-size:13px;color:var(--muted)}
.rn{padding:14px 0 12px;border-bottom:1px solid var(--rule)}
.rn .big{font-size:44px}
.rn p{margin:2px 0 0}
.bar{height:6px;background:var(--rule);margin-top:6px}
.bar i{display:block;height:100%;background:var(--green)}
.bar.short i{background:var(--red)}
.big{font:400 48px/1.05 var(--serif);display:block}
.tabs{display:flex;flex-wrap:wrap;border-bottom:1px solid var(--rule);position:sticky;top:0;background:var(--paper);z-index:2}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:13px 14px 9px;cursor:pointer;color:var(--ink);display:flex;gap:6px;align-items:center}
.tab[aria-selected=true]{color:var(--red);border-bottom-color:var(--red);font-weight:700}
.panel{padding-top:18px}
.panel h2.q{font:400 22px/1.25 var(--serif);margin:0 0 12px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));border-top:1px solid var(--rule);border-left:1px solid var(--rule)}
.tile{padding:16px 18px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.tile p{margin:4px 0 0}
.pair{display:flex;gap:28px;flex-wrap:wrap}
.pair .cap2{display:block;color:var(--muted);margin-top:2px}
.how{font-size:13.5px;color:var(--muted);margin-top:10px!important}
.how .mono{display:block;font-size:10.5px}
table{border-collapse:collapse;width:100%;margin-top:6px}
caption{font:400 18px/1.3 var(--serif);text-align:left;padding:4px 0 8px}
caption .mono{display:block;color:var(--red);margin-bottom:2px}
th{text-align:left;border-bottom:2px solid var(--ink);padding:6px 8px;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:7px 8px;vertical-align:top}
.num{text-align:right;font-variant-numeric:tabular-nums}
td.pn{color:var(--red);font:700 16px var(--serif);text-align:right}
td.sec{font-size:13.5px;color:var(--muted);width:20%}
.src{font-size:13px;color:var(--muted);margin:6px 0 0}
.note{border-left:3px solid var(--rule);padding:2px 12px;margin:0 0 12px;font-size:15px}
.rowbtn,.hbtn,.tgl{background:none;border:0;cursor:pointer;text-align:left;padding:0}
.rowbtn::before,.hbtn::before,.tgl::before{content:"+";font-family:var(--mono);color:var(--red);display:inline-block;width:1.1em}
.rowbtn[aria-expanded=true]::before,.hbtn[aria-expanded=true]::before,.tgl[aria-expanded=true]::before{content:"\2212"}
tr.open>td{background:#efe9dc}
.hbtn{font:400 20px/1.3 var(--serif);padding:6px 0;width:100%;border-top:1px solid var(--rule)}
.tgl{font-size:14px;margin:8px 0}
.detail>td{background:#efe9dc;padding:12px 14px}
.ptext{font-size:17px;max-width:75ch;margin:6px 0}
mark{background:#f2cfcb;color:var(--ink);padding:0 2px}
dl.facts{display:grid;grid-template-columns:max-content 1fr;gap:3px 16px;margin:10px 0;font-size:14.5px}
dl.facts dt{font:11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
dl.facts dd{margin:0}
.btn{background:var(--ink);color:var(--paper);border:0;padding:8px 14px;cursor:pointer;font:600 14px var(--sans)}
.btn.line{background:none;color:var(--ink);border:1px solid var(--ink)}
.pre{font:13px/1.45 var(--mono);white-space:pre-wrap;word-break:break-word;margin:6px 0;border:1px solid var(--rule);background:#fbf9f4;padding:8px;max-height:320px;overflow:auto}
.pre .pgm{color:var(--red);display:block}
.checks{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}
.chk{display:grid;grid-template-columns:96px 1fr;gap:12px;padding:10px 0;border-bottom:1px solid var(--rule)}
.chk .st{font:700 12px var(--mono);letter-spacing:.06em;text-transform:uppercase}
.chk.pass .st{color:var(--green)} .chk.fail .st{color:var(--red)} .chk.notrun .st{color:var(--muted)}
.chk p{margin:0}
.chk ul,.chk ol{margin:4px 0 0;padding-left:20px;font-size:14px}
.chk details summary{cursor:pointer;font-size:14px}
.kinds{display:flex;flex-wrap:wrap;gap:6px 18px;margin:8px 0;font-size:14px}
.kinds b{font-family:var(--serif);font-size:18px}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;margin:8px 0}
.legend span{padding:1px 6px}
.raw{font:12.5px/1.45 var(--mono);border:1px solid var(--rule);max-height:420px;overflow:auto;background:#fbf9f4}
.rl{display:grid;grid-template-columns:3.2em 2em 1fr;white-space:pre-wrap;word-break:break-word;min-height:1.45em}
.rl .ln{text-align:right;color:var(--muted);padding-right:.6em}
.rl .cd{font-weight:700;text-align:center}
.k-cover{background:#e6e1ee}.k-header{background:#dce7f0}.k-heading{background:#f1e6c4}.k-paragraph{background:#f9f6ef}.k-suspect{background:#f2cfcb}.k-footer{background:#dcead9}.k-x{background:#fff;outline:2px solid var(--red)}
.foot{border-top:1px solid var(--rule);padding:10px 24px;font-size:13px;color:var(--muted)}
.foot p{margin:0}
select{font:inherit;padding:4px 6px;background:#fbf9f4;border:1px solid var(--ink)}
ul.heads{list-style:none;margin:6px 0 10px;padding:0;font-size:14.5px}
ul.heads li{padding:3px 0;border-bottom:1px solid var(--rule)}
</style>
</head>
<body>
<div class="app">
<header class="top">
  <div>
    <p class="mono muted">UN DOCUMENT · PDF TEXT</p>
    <h1 id="title">Paragraphs out of a PDF</h1>
    <p class="meta" id="meta"></p>
    <p class="what">This page splits the converter's text into its numbered paragraphs, removes headers and footers, flags the pages where footnote text may sit inside a paragraph, checks itself and lists every repair. A footer is the lines at the foot of a page; a suspect line is a line that looks like footnote text; a flagged page is a page with at least one suspect line.</p>
  </div>
  <div class="status" id="status" role="status"></div>
</header>
<div class="mid">
  <aside class="rail" id="rail" aria-label="Document"></aside>
  <main class="main">
    <div class="tabs" role="tablist" aria-label="Views" id="tabs">
      <button class="tab" role="tab" id="t-result" aria-controls="p-result" data-tab="result">01 Result</button>
      <button class="tab" role="tab" id="t-paragraphs" aria-controls="p-paragraphs" data-tab="paragraphs">02 Paragraphs</button>
      <button class="tab" role="tab" id="t-flagged" aria-controls="p-flagged" data-tab="flagged">03 Flagged pages</button>
      <button class="tab" role="tab" id="t-checks" aria-controls="p-checks" data-tab="checks">04 Checks &amp; method<span id="t-dot"></span></button>
    </div>
    <section class="panel" role="tabpanel" id="p-result" aria-labelledby="t-result"></section>
    <section class="panel" role="tabpanel" id="p-paragraphs" aria-labelledby="t-paragraphs" hidden></section>
    <section class="panel" role="tabpanel" id="p-flagged" aria-labelledby="t-flagged" hidden></section>
    <section class="panel" role="tabpanel" id="p-checks" aria-labelledby="t-checks" hidden></section>
  </main>
</div>
<footer class="foot" id="foot"></footer>
</div>

<script id="pipeline">
/* ---------- pipeline: raw converter text -> paragraphs, flags, repairs, checks ---------- */
function normQ(s){return String(s).replace(/[“”„]/g,'"').replace(/[‘’‚]/g,"'").replace(/[–—]/g,"-").replace(/\s+/g," ").trim();}
var ABBR=/^(?:No|Nos|Art|Arts|art|arts|Para|Paras|para|paras|p|pp|Vol|vol|sect)\.$/;
function firstWords(text){
  var raw=String(text).split(/\s+/).filter(Boolean),out=[];
  for(var i=0;i<raw.length&&out.length<6;i++){
    var w=raw[i];
    if(/^\d+$/.test(w)){
      /* a lone number after a full stop or comma is a footnote mark, unless it follows "No.", "art." and the like */
      var pv=raw[i-1];
      if(i>0&&/[.,;:\u201D\u2019")]$/.test(pv)&&!ABBR.test(pv))continue;
    }else w=w.replace(/(\D)\d{1,3}$/,"$1");
    out.push(w);
  }
  return out.join(" ");
}
function suspectReason(s){
  if(/^\d{1,3}$/.test(s))return "bare number";
  if(/^\d{1,3} [A-ZÀ-Þ“”"‘'«]/.test(s))return "starts with a number and a space";
  if(/^\* /.test(s))return "starts with an asterisk and a space";
  return null;
}
function isStart(s){
  var m=/^(\d{1,3})\.$/.exec(s); if(m)return {num:+m[1],rest:""};
  m=/^(\d{1,3})\. (.+)$/.exec(s); return m?{num:+m[1],rest:m[2]}:null;
}
function analyse(doc){
  var symbol=String(doc.symbol||"");
  var ref=doc.reference&&typeof doc.reference==="object"?doc.reference:null;
  var fwRef=ref&&ref.first_words&&typeof ref.first_words==="object"?ref.first_words:null;
  var recs=doc.records.slice().sort(function(x,y){return x.page-y.page;});
  var A={symbol:symbol,pages:[],paragraphs:[],headings:[],log:[],warnings:[],bare:[],hyphenLines:0};
  var seq=0;
  function note(kind,page,n,para,before,after,pageLabel){var e={kind:kind,page:page,n:n,para:para,before:before,after:after,pageLabel:pageLabel||String(page),seq:seq++};A.log.push(e);return e;}
  var B=[];
  recs.forEach(function(rec){
    var lines=String(rec.text==null?"":rec.text).split(/\r?\n/).map(function(t,i){return {page:rec.page,n:i+1,text:t,kind:null,blank:t.trim()===""};});
    var pg={page:rec.page,lines:lines,header:false,pageNo:false};
    A.pages.push(pg);
    var first=lines.find(function(l){return !l.blank;});
    if(first&&first.text.trim()===symbol){first.kind="header";pg.header=true;note("header line removed",rec.page,first.n,null,symbol,"(removed)");}
    else A.warnings.push("Page "+rec.page+": the first line is not the document symbol.");
    for(var k=lines.length-1;k>=0;k--){
      var l=lines[k]; if(l.kind)break; if(l.blank)continue;
      var t=l.text.trim();
      if(t.indexOf("GE.")===0||/^\d{6}(\s+\d{6})*$/.test(t)){l.kind="footer";note("footer line removed",rec.page,l.n,null,t,"(removed)");}
      else if(/^\d{1,3}$/.test(t)){
        l.kind="footer";
        if(+t===rec.page&&!pg.pageNo){pg.pageNo=true;note("footer line removed",rec.page,l.n,null,t+" (page number)","(removed)");}
        else{A.bare.push({page:rec.page,number:+t});note("bare number removed from the footer",rec.page,l.n,"footnote "+t+", number displaced",t,"(removed)");}
      }else break;
    }
    lines.forEach(function(l){if(!l.kind&&!l.blank)B.push(l);});
  });

  var mode="cover",cur=null,hb=null,part=null,sub=null,unl=null,last=null,susPage=null,pend=[];
  function addHead(kind,label,text,L){
    var h={kind:kind,label:label,text:text,page:L.page,n:L.n,para:null};
    A.headings.push(h);
    if(kind==="part"){part=h;sub=null;unl=null;}else if(kind==="sub"){sub=h;unl=null;}else unl=h;
    last=h;pend.push(h);return h;
  }
  function hText(h){return h?((h.label?h.label+" ":"")+h.text):"";}
  function closeHead(){
    if(!hb)return;
    if(!hb.lines.length)addHead(hb.kind,hb.label,"",hb.L);
    hb.lines.forEach(function(x,i){if(i===0)addHead(hb.kind,hb.label,x.text,x.L);else addHead("unl",null,x.text,x.L);});
    hb=null;
  }
  function finish(){
    if(!cur)return;
    var p=cur;cur=null;
    var ls=p.lines;
    p.text=ls.map(function(l){return l.text;}).join(" ").replace(/\s+/g," ").trim();
    p.textLines=ls.map(function(l){return l.text;});
    p.page_start=p.startLine.page;
    p.page_end=ls.length?ls[ls.length-1].page:p.page_start;
    p.suspect=ls.filter(function(l){return l.suspect;});
    p.words=p.text?p.text.split(" ").length:0;
    p.long=p.words>300;
    p.flagged=p.suspect.length>0||p.long;
    ls.forEach(function(l){if(/-$/.test(l.text))A.hyphenLines++;});
    if(p.page_end!==p.page_start){
      var j=ls.find(function(l){return l.page!==p.page_start;});
      var before=ls.filter(function(l){return l.page===p.page_start;}).map(function(l){return l.text;}).join(" ");
      note("paragraph joined across a page break",j.page,j.n,p.number,"page "+p.page_start+" ends: …"+before.slice(-45),"page "+j.page+" continues: "+j.text.slice(0,45)+"…",p.page_start+"–"+p.page_end);
    }
    p.first_found=firstWords(p.text);
    p.first_ref=fwRef&&fwRef[String(p.number)]!=null?String(fwRef[String(p.number)]):null;
    p.first_match=p.first_ref==null?null:normQ(p.first_found)===normQ(p.first_ref);
    A.paragraphs.push(p);
  }
  for(var i=0;i<B.length;i++){
    var L=B[i],s=L.text.trim();
    var st=isStart(s);
    if(st){
      closeHead();finish();
      pend.forEach(function(o){o.para=st.num;});pend=[];
      var path=[part,sub,unl].filter(Boolean).map(hText).join(" › ");
      cur={number:st.num,startLine:L,lines:[],part:hText(part),section:hText(last),path:path,repairs:[]};
      L.kind="paragraph";mode="para";
      if(st.rest){
        cur.lines.push({page:L.page,n:L.n,text:st.rest,suspect:false,src:L});
        note("number and text split",L.page,L.n,st.num,s.slice(0,70)+(s.length>70?"…":""),st.num+". | "+st.rest.slice(0,60)+(st.rest.length>60?"…":""));
      }
      continue;
    }
    var lb=/^([IVX]+|[A-Z])\.$/.exec(s);
    if(lb&&!(mode==="para"&&susPage===L.page)){
      closeHead();L.kind="heading";
      hb={label:lb[1]+".",kind:/^[IVX]+$/.test(lb[1])?"part":"sub",lines:[],L:L};mode="heading";continue;
    }
    if(mode==="cover"){L.kind="cover";continue;}
    if(mode==="heading"){
      L.kind="heading";
      var lh=hb.lines[hb.lines.length-1];
      if(lh&&/^[a-z(]/.test(s)){
        var b4=lh.text;lh.text=lh.text+" "+s;
        pend.push(note("heading title joined from two lines",L.page,L.n,null,b4+" | "+s,lh.text));
      }else{
        hb.lines.push({text:s,L:L});
        if(hb.lines.length>1)pend.push(note("heading separated from paragraph text",L.page,L.n,null,s,"heading (not paragraph text)"));
      }
      continue;
    }
    var why=suspectReason(s);
    if(susPage===L.page||why){
      var trig=susPage!==L.page;if(trig)susPage=L.page;
      L.kind="suspect";
      cur.lines.push({page:L.page,n:L.n,text:s,suspect:true,reason:why||"after a suspect line",trigger:trig,src:L});
      continue;
    }
    var nx=B[i+1];
    var cand=nx&&s.length<=90&&!/[.;:,\d]$/.test(s)&&isStart(nx.text.trim());
    if(cand&&/^[A-Z]/.test(s)){
      L.kind="heading";addHead("unl",null,s,L);
      pend.push(note("heading separated from paragraph text",L.page,L.n,null,s,"heading (not paragraph text)"));
      continue;
    }
    if(cand&&/^[a-z(]/.test(s)){
      /* an unlabelled heading that wraps: its first line is the paragraph's last line so far */
      var pl=cur.lines[cur.lines.length-1];
      if(pl&&!pl.suspect&&pl.src.text.trim()===pl.text&&pl.text.length<=90&&/^[A-Z]/.test(pl.text)&&!/[.;:,\d]$/.test(pl.text)){
        cur.lines.pop();pl.src.kind="heading";L.kind="heading";
        var jt=pl.text+" "+s;addHead("unl",null,jt,pl.src);
        pend.push(note("heading title joined from two lines",L.page,L.n,null,pl.text+" | "+s,jt));
        pend.push(note("heading separated from paragraph text",pl.src.page,pl.src.n,null,jt,"heading (not paragraph text)"));
        continue;
      }
    }
    L.kind="paragraph";
    cur.lines.push({page:L.page,n:L.n,text:s,suspect:false,src:L});
  }
  closeHead();finish();
  A.log.sort(function(a,b){return a.page-b.page||a.n-b.n||a.seq-b.seq;});
  A.paragraphs.forEach(function(p){p.repairs=A.log.filter(function(e){return e.para===p.number;});});
  var fp={};
  A.paragraphs.forEach(function(p){p.suspect.forEach(function(l){
    var f=fp[l.page]||(fp[l.page]={page:l.page,lines:[],paras:[],why:[]});
    f.lines.push(l);if(f.paras.indexOf(p.number)<0)f.paras.push(p.number);
    if(l.trigger&&f.why.indexOf(l.reason)<0)f.why.push(l.reason);
    if(p.long&&f.why.indexOf("paragraph over 300 words")<0)f.why.push("paragraph over 300 words");
  });});
  A.flaggedPages=Object.keys(fp).map(function(k){return fp[k];}).sort(function(a,b){return a.page-b.page;});
  A.kinds={cover:0,header:0,heading:0,paragraph:0,suspect:0,footer:0};A.total=0;A.unclassified=[];
  A.pages.forEach(function(pg){pg.lines.forEach(function(l){
    if(l.blank)return;A.total++;
    if(l.kind&&A.kinds[l.kind]!=null)A.kinds[l.kind]++;else A.unclassified.push(l);
  });});
  return A;
}
function runChecks(A,doc){
  var ref=doc.reference&&typeof doc.reference==="object"?doc.reference:null;
  var refN=ref&&ref.paragraphs!=null&&!isNaN(+ref.paragraphs)?+ref.paragraphs:null;
  var fw=ref&&ref.first_words&&typeof ref.first_words==="object"?ref.first_words:null;
  var P=A.paragraphs,N=A.pages.length,C=[];
  C.push({id:"count",name:"Paragraph count",tab:"paragraphs",given:N+" pages of raw converter text",expect:refN==null?"a reference count, but the file has none":refN+" paragraphs (reference.paragraphs)",found:P.length+" paragraphs"+(refN!=null&&P.length!==refN?", a difference of "+Math.abs(P.length-refN):""),status:refN==null?"notrun":(P.length===refN?"pass":"fail"),items:[]});
  var seen={},ni=[],prev=0,max=0;
  P.forEach(function(p){
    if(seen[p.number])ni.push("para. "+p.number+" appears twice (page "+p.page_start+")");
    seen[p.number]=1;
    if(p.number<prev)ni.push("para. "+p.number+" comes after para. "+prev+" (page "+p.page_start+")");
    prev=p.number;max=Math.max(max,p.number);
  });
  for(var k=1;k<=max;k++)if(!seen[k]){var bf=P.filter(function(p){return p.number<k;}).pop();ni.push("para. "+k+" is missing"+(bf?" (after para. "+bf.number+", page "+bf.page_end+")":""));}
  C.push({id:"num",name:"Numbering",tab:"paragraphs",given:"the paragraph numbers found",expect:"exactly 1 to "+(max||"n")+", in order, each once",found:ni.length?ni.length+" problem(s)":"no gaps, no duplicates, in order",status:P.length&&!ni.length?"pass":"fail",items:ni});
  var fi=[];
  P.forEach(function(p){if(p.first_match===false)fi.push("para. "+p.number+": found “"+p.first_found+"” / reference “"+p.first_ref+"”");});
  var withRef=P.filter(function(p){return p.first_match!==null;}).length;
  C.push({id:"words",name:"First words",tab:"paragraphs",para:fi.length?P.filter(function(p){return p.first_match===false;})[0].number:null,given:"the first six words of each paragraph, footnote marks dropped",expect:"each equal to reference.first_words after normalising quotes, dashes and spaces",found:fw?(withRef-fi.length)+" of "+withRef+" match, "+fi.length+" mismatch(es)"+(withRef<P.length?"; "+(P.length-withRef)+" paragraph(s) have no reference words":""):"no reference.first_words in this file",status:!fw?"notrun":(fi.length||!withRef?"fail":"pass"),items:fi});
  var sl=0,lostS=[];
  P.forEach(function(p){p.suspect.forEach(function(l){sl++;if(p.text.indexOf(l.text)<0)lostS.push("page "+l.page+", line "+l.n);});});
  C.push({id:"susp",name:"Suspect lines",tab:"flagged",given:"the lines that look like footnote text",expect:"every one still inside its paragraph's text, none removed",found:sl+" suspect lines on "+A.flaggedPages.length+" pages, in "+P.filter(function(p){return p.suspect.length;}).length+" paragraphs"+(lostS.length?"; removed: "+lostS.join(", "):""),status:lostS.length?"fail":"pass",items:[]});
  var fl=A.flaggedPages.map(function(f){return "page "+f.page+": para. "+f.paras.join(", ");});
  P.filter(function(p){return p.long;}).forEach(function(p){fl.push("para. "+p.number+" has "+p.words+" words (over 300), page "+p.page_start);});
  C.push({id:"flag",name:"Pages flagged",tab:"flagged",given:"the suspect lines found inside paragraphs",expect:"each flagged page tied to a paragraph; a flag is not a failure",found:A.flaggedPages.length+" of "+N+" pages flagged, "+P.filter(function(p){return p.long;}).length+" paragraph(s) over 300 words",status:A.flaggedPages.every(function(f){return f.paras.length;})?"pass":"fail",items:fl});
  var hdr=A.pages.filter(function(p){return p.header;}).length,pno=A.pages.filter(function(p){return p.pageNo;}).length;
  var hi=A.bare.map(function(b){return "page "+b.page+": bare number "+b.number+" removed";}).concat(A.warnings);
  C.push({id:"hf",name:"Headers and footers",tab:"checks",open:"raw",given:N+" pages",expect:"the symbol on the first line of all "+N+" pages; a page number in the footer on all but the first ("+Math.max(N-1,0)+")",found:hdr+" headers removed, "+pno+" page numbers removed, "+A.bare.length+" other bare numbers removed",status:hdr===N&&pno>=N-1?"pass":"fail",items:hi});
  var lab=A.headings.filter(function(h){return h.label;}).length,un=A.headings.filter(function(h){return h.kind==="unl";});
  var swallowed=A.headings.filter(function(h){return P.some(function(p){return p.lines.some(function(l){return l.page===h.page&&l.n===h.n;});});});
  C.push({id:"head",name:"Headings",tab:"paragraphs",given:"the section titles in the text",expect:"no heading line left inside a paragraph",found:lab+" labelled and "+un.length+" unlabelled headings"+(swallowed.length?"; "+swallowed.length+" kept inside paragraphs":"")+(un.length?". Unlabelled ones, so a paragraph's last line mistaken for a heading can be spotted:":""),status:swallowed.length?"fail":"pass",items:un.map(function(h){return "“"+h.text+"” (page "+h.page+(h.para!=null?", before para. "+h.para:"")+")";})});
  var sum=0;Object.keys(A.kinds).forEach(function(k){sum+=A.kinds[k];});
  var K=A.kinds;
  C.push({id:"lost",name:"Nothing lost",tab:"checks",open:"raw",given:A.total+" non-empty lines in the file",expect:"each line classified exactly once, so the counts add up to "+A.total,found:"cover "+K.cover+" + header "+K.header+" + heading "+K.heading+" + paragraph "+(K.paragraph+K.suspect)+" (of which suspect "+K.suspect+") + footer "+K.footer+" = "+sum+"; unclassified "+A.unclassified.length,status:sum===A.total&&!A.unclassified.length?"pass":"fail",items:A.unclassified.map(function(l){return "page "+l.page+", line "+l.n+": "+l.text;})});
  return C;
}
</script>

<script id="ui">
/* ---------- interface ---------- */
var $=function(s,r){return (r||document).querySelector(s);};
var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
function cut(s,n){s=String(s);if(s.length<=n)return s;var c=s.slice(0,n),i=c.lastIndexOf(" ");return (i>n*0.5?c.slice(0,i):c).replace(/[\s,;:]+$/,"")+"…";}
var TABS=["result","paragraphs","flagged","checks"];
var KINDS=["header line removed","footer line removed","bare number removed from the footer","number and text split","paragraph joined across a page break","heading separated from paragraph text","heading title joined from two lines"];
var CODES={cover:["C","Cover"],header:["H","Header"],heading:["T","Heading"],paragraph:["P","Paragraph"],suspect:["S","Suspect line"],footer:["F","Footer"],x:["?","Unclassified"]};
var W=window.WORKSHOP_DATA||{};
var D=[];
Object.keys(W).forEach(function(k){
  var d=W[k];
  if(d&&Array.isArray(d.records)&&d.records.length&&d.reference&&typeof d.reference==="object"&&d.records.every(function(r){return r&&r.page!=null&&typeof r.text==="string";})){
    try{var a=analyse(d);D.push({key:k,doc:d,a:a,checks:runChecks(a,d)});}
    catch(e){D.push({key:k,doc:d,error:String(e&&e.message||e)});}
  }
});
var S={doc:0,tab:"result"};
function cur(){return D[S.doc];}
function stats(d){
  var pass=d.checks.filter(function(c){return c.status==="pass";}).length,fail=d.checks.filter(function(c){return c.status==="fail";}).length;
  return {pass:pass,fail:fail,total:d.checks.length,notrun:d.checks.length-pass-fail};
}
function refInfo(d){
  var r=d.doc.reference||{};
  return {n:r.paragraphs!=null&&!isNaN(+r.paragraphs)?+r.paragraphs:null,fn:r.footnotes!=null?r.footnotes:null,adopted:r.adopted||""};
}
function cite(d,p){return d.a.symbol+", para. "+p.number;}
function pageLabel(p){return p.page_start===p.page_end?String(p.page_start):p.page_start+"–"+p.page_end;}

function renderTop(d){
  $("#title").textContent=d.doc.title||d.a.symbol;
  var r=refInfo(d);
  $("#meta").innerHTML=(d.doc.doc_url?'<a href="'+esc(d.doc.doc_url)+'" target="_blank" rel="noopener">'+esc(d.a.symbol)+'</a>':esc(d.a.symbol))
    +(r.adopted?" · adopted "+esc(r.adopted):"")+" · "+d.a.pages.length+" pages of raw converter text"+(d.doc.source?" · "+esc(d.doc.source):"");
  var s=stats(d);
  $("#status").innerHTML=s.fail?'<span class="dot bad"></span><span class="bad">'+s.fail+' check'+(s.fail>1?'s':'')+' failed</span>'
    :'<span class="dot '+(s.notrun?'':'ok')+'"></span><span class="'+(s.notrun?'muted':'ok')+'">'+s.pass+' of '+s.total+' checks pass</span>';
  $("#t-dot").innerHTML=s.fail?'<span class="dot bad" aria-hidden="true"></span><span class="sr">checks failed</span>':"";
}
function renderRail(){
  var h='<h2 class="mono muted">DOCUMENT</h2>';
  D.forEach(function(x,i){
    var t=String(x.doc.title||x.key).replace(/,.*$/,"");
    h+='<button class="card" data-doc="'+i+'" aria-pressed="'+(i===S.doc)+'"><span class="sym">'+esc(x.doc.symbol||x.key)+'</span><span class="sh">'+esc(t)+'</span><span class="ad">'+(x.doc.reference&&x.doc.reference.adopted?"adopted "+esc(x.doc.reference.adopted)+" · ":"")+x.doc.records.length+' pages</span></button>';
  });
  var d=cur();
  if(d&&d.a){
    var r=refInfo(d),n=d.a.paragraphs.length,fp=d.a.flaggedPages.length,s=stats(d);
    var short=r.n==null||n!==r.n,share=r.n?Math.min(100,Math.round(100*n/r.n)):0;
    h+='<div class="rn"><span class="big'+(short&&r.n!=null?' bad':'')+'">'+n+'</span><p>paragraphs'+(r.n!=null?' of '+r.n:' (no reference in this file)')+'</p><div class="bar'+(short?' short':'')+'" aria-hidden="true"><i style="width:'+share+'%"></i></div></div>';
    h+='<div class="rn"><span class="big'+(fp?' bad':'')+'">'+fp+'</span><p>pages flagged of '+d.a.pages.length+(fp?' · <a href="#t-flagged" data-goto="flagged">see tab 03</a>':'')+'</p></div>';
    h+='<div class="rn"><span class="big'+(s.fail?' bad':'')+'">'+s.pass+' of '+s.total+'</span><p>checks pass · <a href="#t-checks" data-goto="checks">see tab 04</a></p></div>';
  }
  $("#rail").innerHTML=h;
}
function tile(lab,body,note){return '<div class="tile"><p class="mono muted">'+lab+'</p>'+body+'<p class="how"><span class="mono">How this is computed</span>'+note+'</p></div>';}
function renderResult(d){
  var a=d.a,r=refInfo(d),n=a.paragraphs.length,eq=r.n!=null&&n===r.n,fp=a.flaggedPages.length,fl=a.paragraphs.filter(function(p){return p.flagged;}).length;
  var withRef=a.paragraphs.filter(function(p){return p.first_match!==null;}).length,fm=a.paragraphs.filter(function(p){return p.first_match===true;}).length;
  var h='<h2 class="q">Did the app find everything the document has?</h2><div class="tiles">';
  h+=tile("Paragraphs",'<div class="pair"><div><span class="big">'+n+'</span><span class="cap2">Paragraphs found</span></div><div><span class="big '+(r.n==null?'muted':eq?'ok':'bad')+'">'+(r.n==null?'—':r.n)+'</span><span class="cap2">The document has</span></div></div>'
    +'<p class="'+(r.n==null?'muted':eq?'ok':'bad')+'">'+(r.n==null?'no reference in this file':eq?'equal':'differs by '+Math.abs(n-r.n))+'</p>'
    +(fp?'<p class="bad">'+fl+' may contain footnote text</p>':''),
    'Every line that starts with a number and a full stop opens a paragraph; the count is compared with the document’s own.');
  h+=tile("Pages flagged",'<span class="big'+(fp?' bad':'')+'">'+fp+'</span><p>of the document’s '+a.pages.length+' pages</p>'
    +(fp?'<p class="bad">footnote text may sit inside a paragraph; <a href="#t-flagged" data-goto="flagged">see tab 03</a></p>':'<p class="ok">no suspect line inside a paragraph</p>')
    +'<p>'+(r.fn!=null?'The document has '+esc(r.fn)+' footnotes; ':'')+'this version does not separate them.</p>',
    'A page is flagged when a line inside a paragraph is a bare number or starts with a number and a capital letter; every line after it to the foot of the page is suspect too.');
  h+=tile("First words match",'<span class="big '+(r.n==null||!withRef?'muted':fm===withRef?'ok':'bad')+'">'+fm+'</span><p>of '+(r.n!=null?r.n:withRef)+' paragraphs'+(withRef?'':' (no reference words in this file)')+'</p>',
    'The first six words of each paragraph, footnote marks dropped, against the document’s list, after normalising quotes, dashes and spaces.');
  h+=tile("Repairs made",'<span class="big">'+a.log.length+'</span><p><a href="#repairs" data-goto="checks" data-open="repairs">Open the repair log</a></p>',
    'Every header, footer, split, join and heading the script changed is logged, in document order.');
  return h+'</div>';
}
function checkCell(p){
  var h=[];
  if(p.first_match===false)h.push('<span class="bad">first words differ</span>');
  if(p.flagged){
    var pg=p.suspect.length?p.suspect[0].page:null;
    h.push(pg!=null?'<a class="bad" href="#t-flagged" data-goto="flagged" data-page="'+pg+'">may contain footnote text</a>':'<span class="bad">may contain footnote text (over 300 words)</span>');
  }
  return h.length?h.join("<br>"):"OK"+(p.first_match===null?' <span class="muted">(first words not checked)</span>':"");
}
function renderParas(d){
  var a=d.a,r=refInfo(d);
  var cap=a.paragraphs.length+' paragraphs found'+(r.n!=null?', '+r.n+' expected':'');
  var h='<h2 class="q">What does each paragraph say, and how do I cite it?</h2>';
  h+='<button class="hbtn" id="heads-btn" data-toggle="heads" aria-expanded="false" aria-controls="heads">Headings found: '+a.headings.length+'</button><div id="heads" hidden><ul class="heads">';
  a.headings.forEach(function(x){h+='<li><span class="mono muted">'+(x.kind==="part"?"PART":x.kind==="sub"?"SUB":"UNLABELLED")+'</span> '+esc(hText2(x))+' <span class="muted">· page '+x.page+'</span></li>';});
  h+=(a.headings.length?'':'<li>No heading found.</li>')+'</ul></div>';
  h+='<table><caption><span class="mono">TAB.02</span>'+esc(cap)+'</caption><thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody>';
  a.paragraphs.forEach(function(p,i){
    h+='<tr data-kind="para" data-i="'+i+'" data-para="'+p.number+'"><td class="pn">'+p.number+'</td><td class="sec">'+esc(cut(p.section,40))+'</td><td>'+pageLabel(p)+'</td><td><button class="rowbtn" aria-expanded="false" aria-controls="det-p'+i+'">'+esc(cut(p.text,120))+'</button></td><td>'+checkCell(p)+'</td></tr>';
  });
  h+='</tbody></table><p class="src">Source: '+esc(a.symbol)+', text as the PDF converter produced it; counted by this page’s code. Paragraph numbers are the document’s own.</p>';
  h+='<p class="how muted">How this is computed: a heading is never part of a paragraph’s text; the section is the nearest heading above; the check compares the first six words with the reference.</p>';
  return h;
}
function hText2(h){return (h.label?h.label+" ":"")+h.text;}
function paraDetail(d,p){
  var i=d.a.paragraphs.indexOf(p),h='<div>';
  h+='<p class="muted" style="font-size:13.5px;margin:0">'+(p.path?esc(p.path):'No section above this paragraph')+'</p>';
  h+='<p class="ptext">'+p.lines.map(function(l){return l.suspect?'<mark>'+esc(l.text)+'</mark>':esc(l.text);}).join(" ")+'</p>';
  h+='<button class="tgl" aria-expanded="false" aria-controls="pl'+i+'" data-toggle="pl'+i+'">Show the PDF’s lines</button><div id="pl'+i+'" hidden><div class="pre">';
  var lp=null;
  p.lines.forEach(function(l){
    if(l.page!==lp){h+='<span class="pgm">── page '+l.page+' begins ──</span>';lp=l.page;}
    h+=(l.suspect?'<mark>':'')+esc(("   "+l.n).slice(-3)+"  "+l.text)+(l.suspect?'</mark>':'')+"\n";
  });
  h+='</div></div><dl class="facts">';
  h+='<dt>First words, reference</dt><dd>'+(p.first_ref==null?'<span class="muted">none in this file</span>':esc(p.first_ref))+'</dd>';
  h+='<dt>First words, extracted</dt><dd>'+esc(p.first_found)+' '+(p.first_match===null?'':p.first_match?'<span class="ok">equal</span>':'<span class="bad">different</span>')+'</dd>';
  h+='<dt>Page(s)</dt><dd>'+pageLabel(p)+'</dd>';
  h+='<dt>Repairs</dt><dd>'+(p.repairs.length?p.repairs.map(function(e){return esc(e.kind);}).join("; "):'none')+'</dd>';
  if(p.suspect.length)h+='<dt>Suspect lines</dt><dd class="bad">'+p.suspect.length+' (highlighted above)</dd>';
  h+='</dl><button class="btn" data-cite="'+esc(cite(d,p))+'">Copy citation</button> <code>'+esc(cite(d,p))+'</code></div>';
  return h;
}
function rawLines(pg,onlySuspect){
  return pg.lines.map(function(l){
    var k=l.blank?"":(l.kind||"x");
    var cls=k&&(!onlySuspect||k==="suspect")?" k-"+k:"";
    return '<div class="rl'+cls+'"><span class="ln">'+l.n+'</span><span class="cd">'+(k&&(!onlySuspect||k==="suspect")?CODES[k][0]:"")+'</span><span>'+esc(l.text)+'</span></div>';
  }).join("");
}
function renderFlagged(d){
  var a=d.a,fp=a.flaggedPages;
  var h='<h2 class="q">Which paragraphs should I check against the PDF?</h2>';
  h+='<p class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF. The next step can separate them.</p>';
  if(!fp.length){return h+'<p>No page is flagged: no suspect line was found inside a paragraph.</p>';}
  h+='<table><caption><span class="mono">TAB.03</span>'+fp.length+' of '+a.pages.length+' pages flagged</caption><thead><tr><th scope="col" class="num">Page</th><th scope="col">Paragraph</th><th scope="col" class="num">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>';
  fp.forEach(function(f,i){
    h+='<tr data-kind="flag" data-i="'+i+'" data-page="'+f.page+'"><td class="num"><button class="rowbtn" aria-expanded="false" aria-controls="det-f'+i+'">'+f.page+'</button></td><td>'+f.paras.join(", ")+'</td><td class="num">'+f.lines.length+'</td><td>'+(f.why.length?f.why.map(esc).join("; "):"after a suspect line")+'</td></tr>';
  });
  h+='</tbody></table><p class="src">Source: '+esc(a.symbol)+'; the page’s raw lines are shown when a row opens.</p>';
  h+='<p class="how muted">How this is computed: the first suspect line on a page starts the footnote block; it and every line after it to the foot of the page stay in the paragraph’s text and are flagged.</p>';
  return h;
}
function flagDetail(d,f){
  var pg=d.a.pages.filter(function(x){return x.page===f.page;})[0],h='<div>';
  f.paras.forEach(function(n){
    var p=d.a.paragraphs.filter(function(q){return q.number===n;})[0];
    h+='<p>Suspect lines sit in <a href="#paragraphs" data-goto="paragraphs" data-para="'+n+'">paragraph '+n+'</a>'+(p?' ("'+esc(cut(p.text,90))+'")':'')+'.</p>';
  });
  h+='<p class="mono muted">RAW LINES OF PAGE '+f.page+' · S = suspect line</p><div class="raw" tabindex="0" role="region" aria-label="Raw lines of page '+f.page+'">'+(pg?rawLines(pg,true):"")+'</div></div>';
  return h;
}
function renderChecks(d){
  var a=d.a,s=stats(d);
  var h='<h2 class="q">Can I trust this, and can I take it away?</h2>';
  h+='<p class="mono muted">TAB.04 · '+s.pass+' of '+s.total+' checks pass'+(s.fail?' · '+s.fail+' failed':'')+'</p><ol class="checks">';
  d.checks.forEach(function(c){
    var lab=c.status==="pass"?"pass":c.status==="fail"?"check failed":"not run";
    var link=c.open?'<a href="#raw" data-goto="checks" data-open="'+c.open+'">see the raw pages</a>':'<a href="#t-'+c.tab+'" data-goto="'+c.tab+'"'+(c.para!=null?' data-para="'+c.para+'"':'')+'>see the rows</a>';
    h+='<li class="chk '+c.status+'"><span class="st">'+lab+'</span><div><p><strong>'+esc(c.name)+'.</strong> Given '+esc(c.given)+', having run the script, we expect '+esc(c.expect)+'. Found: '+esc(c.found)+'. '+link+'</p>';
    if(c.items.length){
      var li=c.items.map(function(x){return '<li>'+esc(x)+'</li>';}).join("");
      h+=c.items.length>12?'<details><summary>List ('+c.items.length+')</summary><ul>'+li+'</ul></details>':'<ul>'+li+'</ul>';
    }
    h+='</div></li>';
  });
  h+='</ol>';
  var cnt={};KINDS.forEach(function(k){cnt[k]=0;});a.log.forEach(function(e){cnt[e.kind]=(cnt[e.kind]||0)+1;});
  h+='<button class="hbtn" id="repairs-btn" data-toggle="repairs" aria-expanded="false" aria-controls="repairs">Repair log ('+a.log.length+')</button><div id="repairs" hidden><div class="kinds">'
    +KINDS.map(function(k){return '<span>'+esc(k)+' <b>'+cnt[k]+'</b></span>';}).join("")+'</div>';
  h+='<table><caption><span class="mono">TAB.04</span>'+a.log.length+' changes, in document order</caption><thead><tr><th scope="col" class="num">Page</th><th scope="col">Paragraph or footnote</th><th scope="col">What was done</th><th scope="col">Before</th><th scope="col">After</th></tr></thead><tbody>';
  a.log.forEach(function(e){h+='<tr><td class="num">'+esc(e.pageLabel)+'</td><td>'+(e.para==null?"—":esc(e.para))+'</td><td>'+esc(e.kind)+'</td><td>'+esc(e.before)+'</td><td>'+esc(e.after)+'</td></tr>';});
  h+='</tbody></table><p class="src">Source: this page’s code, run on '+esc(a.symbol)+'. Lines ending in a hyphen: '+a.hyphenLines+' (no hyphen joining is done).</p></div>';
  h+='<button class="hbtn" id="raw-btn" data-toggle="raw" aria-expanded="false" aria-controls="raw">Raw pages</button><div id="raw" hidden>';
  h+='<p><label for="rawsel">Show raw page </label><select id="rawsel">'+a.pages.map(function(p){return '<option value="'+p.page+'">'+p.page+'</option>';}).join("")+'</select></p>';
  h+='<div class="legend">'+["cover","header","heading","paragraph","suspect","footer","x"].map(function(k){return '<span class="k-'+k+'">'+CODES[k][0]+' = '+CODES[k][1]+'</span>';}).join("")+'</div>';
  h+='<div class="raw" id="rawview" tabindex="0" role="region" aria-label="Raw page text"></div></div>';
  h+='<h3 class="mono muted" style="margin:18px 0 6px">Download</h3><button class="btn" id="dl">Download paragraphs as CSV</button> <span class="muted" id="dlmsg" role="status"></span>';
  return h;
}
function csvFor(d){
  var cols=["number","section","part","page_start","page_end","first_words_reference","first_words_found","first_words_match","text","text_raw","flagged","suspect_lines","repairs","citation","symbol","doc_url"];
  var rows=[cols];
  d.a.paragraphs.forEach(function(p){
    rows.push([p.number,p.section,p.part,p.page_start,p.page_end,p.first_ref==null?"":p.first_ref,p.first_found,p.first_match==null?"":p.first_match,p.text,p.textLines.join(" | "),p.flagged,
      p.suspect.map(function(l){return "page "+l.page+" line "+l.n+": "+l.text;}).join(" | "),p.repairs.map(function(e){return e.kind;}).join("; "),cite(d,p),d.a.symbol,d.doc.doc_url||""]);
  });
  return "﻿"+rows.map(function(r){return r.map(function(v){return '"'+String(v).replace(/"/g,'""')+'"';}).join(",");}).join("\r\n")+"\r\n";
}
function download(){
  var d=cur(),blob=new Blob([csvFor(d)],{type:"text/csv;charset=utf-8"}),url=URL.createObjectURL(blob);
  var name=String(d.a.symbol||"paragraphs").replace(/\//g,"-")+".csv",a=document.createElement("a");
  a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();
  setTimeout(function(){URL.revokeObjectURL(url);},4000);
  $("#dlmsg").textContent=name+" · "+d.a.paragraphs.length+" rows";
}
function copyText(t){
  var fallback=function(){try{var ta=document.createElement("textarea");ta.value=t;ta.style.cssText="position:fixed;opacity:0";document.body.appendChild(ta);ta.select();var ok=document.execCommand("copy");ta.remove();return ok;}catch(e){return false;}};
  if(navigator.clipboard&&navigator.clipboard.writeText)return navigator.clipboard.writeText(t).then(function(){return true;},function(){return fallback();});
  return Promise.resolve(fallback());
}
function renderRaw(){
  var d=cur(),sel=$("#rawsel");if(!sel||!d)return;
  var pg=d.a.pages.filter(function(p){return String(p.page)===sel.value;})[0];
  $("#rawview").innerHTML=pg?rawLines(pg,false):"";
}
function renderAll(){
  var d=cur();
  renderRail();
  if(!d){
    $("#p-result").innerHTML='<p>No document with raw PDF text and a reference was found in the attached data. Drag the General Comment PDF text from "Your files" into the chat and ask again.</p>';
    $("#foot").innerHTML="<p>Nothing to show.</p>";return;
  }
  if(d.error){
    $("#title").textContent=d.doc.title||d.key;
    $("#p-result").innerHTML='<p class="bad">The script could not read this document: '+esc(d.error)+'</p>';
    return;
  }
  renderTop(d);
  $("#p-result").innerHTML=renderResult(d);
  $("#p-paragraphs").innerHTML=renderParas(d);
  $("#p-flagged").innerHTML=renderFlagged(d);
  $("#p-checks").innerHTML=renderChecks(d);
  renderRaw();
  $("#foot").innerHTML='<p>Source: '+esc(d.doc.source||d.a.symbol)+(d.doc.built?' · built '+esc(d.doc.built):'')+'. Counting, splitting, matching and flagging are done by this page’s code; no model was called and nothing left the browser.</p>';
}
function setTab(t,focus){
  S.tab=t;
  TABS.forEach(function(k){
    var b=$("#t-"+k),p=$("#p-"+k),on=k===t;
    b.setAttribute("aria-selected",on);b.tabIndex=on?0:-1;
    p.hidden=!on;if(on)p.tabIndex=0;else p.removeAttribute("tabindex");
  });
  if(focus)$("#t-"+t).focus();
}
function toggleRow(tr){
  var btn=$("button.rowbtn",tr),d=cur();
  if(btn.getAttribute("aria-expanded")==="true"){
    var nx=tr.nextElementSibling;if(nx&&nx.classList.contains("detail"))nx.remove();
    btn.setAttribute("aria-expanded","false");tr.classList.remove("open");return;
  }
  var i=+tr.dataset.i,row=document.createElement("tr");row.className="detail";
  row.id=btn.getAttribute("aria-controls");
  row.innerHTML='<td colspan="'+tr.children.length+'">'+(tr.dataset.kind==="para"?paraDetail(d,d.a.paragraphs[i]):flagDetail(d,d.a.flaggedPages[i]))+'</td>';
  tr.after(row);btn.setAttribute("aria-expanded","true");tr.classList.add("open");
}
function goTo(tab,o){
  o=o||{};setTab(tab,false);
  var el=null;
  if(tab==="checks"&&o.open){
    var b=$("#"+o.open+"-btn");
    if(b){if(b.getAttribute("aria-expanded")!=="true")b.click();el=b;}
  }else if(tab==="flagged"&&o.page){
    var tr=$('#p-flagged tr[data-page="'+o.page+'"]');
    if(tr){if($("button.rowbtn",tr).getAttribute("aria-expanded")!=="true")toggleRow(tr);el=$("button.rowbtn",tr);}
  }else if(tab==="paragraphs"&&o.para){
    var tp=$('#p-paragraphs tr[data-para="'+o.para+'"]');if(tp)el=$("button.rowbtn",tp);
  }
  if(el){el.scrollIntoView({block:"center"});el.focus();}else $("#t-"+tab).focus();
}
document.addEventListener("click",function(e){
  var t=e.target,el;
  if((el=t.closest("[data-goto]"))){e.preventDefault();goTo(el.dataset.goto,{page:el.dataset.page,para:el.dataset.para,open:el.dataset.open});return;}
  if((el=t.closest("[data-tab]"))){setTab(el.dataset.tab,false);return;}
  if((el=t.closest("[data-doc]"))){S.doc=+el.dataset.doc;renderAll();setTab(S.tab,false);return;}
  if((el=t.closest("[data-toggle]"))){
    var on=el.getAttribute("aria-expanded")!=="true";
    el.setAttribute("aria-expanded",on);$("#"+el.dataset.toggle).hidden=!on;
    return;
  }
  if((el=t.closest("[data-cite]"))){
    var txt=el.dataset.cite;
    copyText(txt).then(function(ok){el.textContent=ok?"Copied":"Copy failed: select the text beside it";setTimeout(function(){el.textContent="Copy citation";},2000);});
    return;
  }
  if(t.closest("#dl")){download();return;}
  if(t.closest("a"))return;
  if((el=t.closest("tr[data-kind]")))toggleRow(el);
});
document.addEventListener("change",function(e){if(e.target.id==="rawsel")renderRaw();});
$("#tabs").addEventListener("keydown",function(e){
  var i=TABS.indexOf(S.tab),n=i;
  if(e.key==="ArrowRight")n=(i+1)%TABS.length;
  else if(e.key==="ArrowLeft")n=(i+TABS.length-1)%TABS.length;
  else if(e.key==="Home")n=0;
  else if(e.key==="End")n=TABS.length-1;
  else return;
  e.preventDefault();setTab(TABS[n],true);
});
renderAll();
setTab("result",false);
</script>
</body>
</html>
```
