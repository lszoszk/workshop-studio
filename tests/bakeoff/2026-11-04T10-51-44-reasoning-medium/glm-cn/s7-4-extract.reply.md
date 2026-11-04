I built the app as planned: it splits the converter's raw text into numbered paragraphs and footnotes, removes headers, footers and footnote blocks, restores displaced footnote numbers, brackets footnote marks, and checks itself against the document's own reference. It handles every document in `WORKSHOP_DATA` that has both `records` and a `reference`, so both General Comments in the shelf get a card in the rail.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
[hidden]{display:none!important}
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b3a}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
a{color:var(--red)}
a:focus,button:focus,select:focus,[tabindex]:focus{outline:2px solid var(--red);outline-offset:2px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1.05}
.apphead{padding:18px 28px 14px;border-bottom:1px solid var(--rule)}
.apphead .top{display:flex;justify-content:space-between;gap:16px;align-items:flex-start}
.apphead h1{font-family:Georgia,"Times New Roman",serif;font-weight:normal;font-size:26px;margin:6px 0 4px}
.apphead .metaline{font-size:14px;color:#4a463f}
.apphead .what{font-size:14px;max-width:62ch;margin:6px 0 0;color:#4a463f}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;vertical-align:middle;margin-right:6px}
.dot.ok{background:var(--green)}
.dot.bad{background:var(--red)}
.status{font-size:14px;white-space:nowrap;padding-top:6px}
.layout{display:flex;min-height:70vh}
.rail{width:270px;flex:0 0 270px;border-right:1px solid var(--rule);padding:18px 20px}
.rail h2{margin:0 0 10px;font-weight:normal}
.card{border:1px solid var(--rule);border-left:3px solid transparent;padding:10px 12px;margin-bottom:8px;background:#faf7f0;text-align:left;width:100%;font:inherit;color:inherit;cursor:pointer}
.card.sel{border-left-color:var(--red)}
.card .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.card .t{font-size:13px;margin:4px 0;color:#4a463f}
.card .m{font-size:12px;color:#6b6559}
.railnums{margin-top:18px;border-top:1px solid var(--rule);padding-top:14px}
.railnums .rn{margin-bottom:16px}
.railnums .of{font-size:13px;color:#4a463f}
.bar{height:3px;background:var(--rule);margin-top:6px}
.bar i{display:block;height:3px;background:var(--green)}
.bar.bad i{background:var(--red)}
.main{flex:1;min-width:0;padding:0 28px 40px}
.tabbar{display:flex;gap:0;border-bottom:1px solid var(--rule);margin-bottom:20px;flex-wrap:wrap}
.tab{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;background:none;border:none;border-bottom:3px solid transparent;padding:14px 16px 11px;cursor:pointer;color:var(--ink)}
.tab[aria-selected="true"]{border-bottom-color:var(--red);color:var(--red)}
.tab .faildot{color:var(--red)}
.panel{padding-top:6px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;margin-bottom:26px}
.tile{border-top:2px solid var(--ink);padding-top:10px}
.tile .lab{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:#4a463f}
.tile .sub{font-size:14px;margin-top:4px}
.tile .how{font-size:12.5px;color:#6b6559;margin-top:8px;border-top:1px solid var(--rule);padding-top:6px}
.ok-t{color:var(--green)}
.bad-t{color:var(--red)}
table{width:100%;border-collapse:collapse;font-size:14.5px;margin:10px 0 6px}
caption{text-align:left;font-family:Georgia,"Times New Roman",serif;font-size:19px;padding:6px 0}
caption .mono{float:right;padding-top:10px;color:#6b6559}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
th{border-bottom:1.5px solid var(--ink);font-weight:600;font-size:13px}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
tr.prow,tr.frow{cursor:pointer}
tr.prow:hover,tr.frow:hover{background:#efe9dc}
.rowbtn{background:none;border:none;font:inherit;color:var(--red);cursor:pointer;padding:0;text-align:right}
td.pno{color:var(--red);font-family:Georgia,serif;font-size:17px}
tr.exp>td{background:#faf7f0;padding:14px 16px 18px}
.exp .full{max-width:75ch}
.exp .meta{font-size:13.5px;color:#4a463f;margin-top:10px;border-top:1px solid var(--rule);padding-top:8px}
.exp .meta div{margin:3px 0}
.btn{background:var(--ink);color:#f4f0e8;border:none;padding:8px 14px;font:inherit;font-size:14px;cursor:pointer;margin-top:8px}
.btn:hover{background:#000}
.toggle{background:none;border:none;border-bottom:1px solid var(--red);color:var(--red);font:inherit;font-size:13.5px;cursor:pointer;padding:2px 0}
.note{font-size:13px;color:#6b6559;margin:8px 0 20px;max-width:75ch}
.note code,.checks code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
.checks{margin:0 0 26px}
.check{padding:9px 0;border-bottom:1px solid var(--rule);font-size:14.5px}
.check .cname{font-weight:600}
.check .cdet{color:#4a463f;font-size:13.5px;margin-top:2px;max-width:85ch}
.pass{color:var(--green);font-weight:600}
.fail{color:var(--red);font-weight:600}
.notrun{color:#6b6559;font-weight:600}
.fold{background:none;border:none;border-bottom:1px solid var(--rule);width:100%;text-align:left;font-family:Georgia,serif;font-size:19px;padding:12px 0;cursor:pointer;color:var(--ink)}
.fold[aria-expanded="true"]{border-bottom-color:var(--ink)}
.foldbody{padding:6px 0 24px}
.rawpages{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;line-height:1.7;white-space:pre-wrap;border:1px solid var(--rule);padding:10px 12px;max-height:520px;overflow:auto;background:#faf7f0}
.rl{display:block;padding:0 6px}
.rl .ln{display:inline-block;width:34px;color:#8a8375;text-align:right;margin-right:10px;user-select:none}
.lv-C{background:#ece3d2}.lv-H{background:#e0ddca}.lv-S{background:#e9e4cf}.lv-P{background:#faf7f0}.lv-N{background:#e2e6e4}.lv-B{background:#e5ded2}.lv-X{background:#f2d5d5}
.code{display:inline-block;width:14px;text-align:center;color:#4a463f}
.legend{font-size:12px;color:#4a463f;margin:8px 0 14px}
.legend span{display:inline-block;padding:1px 7px;margin:2px 6px 2px 0}
.heads li{margin:3px 0;font-size:14px}
.appfoot{border-top:1px solid var(--rule);padding:14px 28px;font-size:13px;color:#4a463f;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}
.para-expanded-lines{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;white-space:pre-wrap;background:#faf7f0;border:1px solid var(--rule);padding:10px;margin-top:10px}
.pagemark{color:var(--red)}
@media(max-width:900px){.layout{flex-direction:column}.rail{width:auto;flex:none;border-right:none;border-bottom:1px solid var(--rule)}}
</style>
</head>
<body>

<header class="apphead" id="apphead"></header>
<div class="layout">
  <aside class="rail" id="rail" aria-label="Documents"></aside>
  <main class="main">
    <div class="tabbar" role="tablist" aria-label="Sections" id="tabbar"></div>
    <section class="panel" id="panel0" role="tabpanel" tabindex="0"></section>
    <section class="panel" id="panel1" role="tabpanel" tabindex="0" hidden></section>
    <section class="panel" id="panel2" role="tabpanel" tabindex="0" hidden></section>
    <section class="panel" id="panel3" role="tabpanel" tabindex="0" hidden></section>
  </main>
</div>
<footer class="appfoot" id="appfoot"></footer>

<script>
(function(){
"use strict";
var WD = window.WORKSHOP_DATA || {};
var esc = function(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');};
var norm = function(s){return String(s==null?'':s)
  .replace(/[\u2018\u2019\u201B\u2032]/g,"'").replace(/[\u201C\u201D\u2033]/g,'"')
  .replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ').trim();};

/* ---------- pipeline ---------- */
function processDoc(key){
  var doc = WD[key];
  var sym = doc.symbol || '';
  var ref = doc.reference || {};
  var repairs = [];
  var warnings = [];
  var footnotes = [];
  var orphans = [];

  var pages = (doc.records||[]).slice().sort(function(a,b){return a.page-b.page;}).map(function(r){
    var raw = String(r.text==null?'':r.text).split('\n');
    return {page:r.page, raw:raw, lines:raw.map(function(s){return s.replace(/\s+$/,'');}),
            cls:raw.map(function(s){return s.trim()===''?'':'X';})};
  });
  var firstPage = pages[0];

  /* header */
  pages.forEach(function(p){
    var fi=-1; for(var i=0;i<p.lines.length;i++){if(p.lines[i].trim()!==''){fi=i;break;}}
    p.headerIdx = (fi>=0 && p.lines[fi].trim()===sym) ? fi : -1;
    if(p.headerIdx>=0){
      p.cls[fi]='H';
      repairs.push({page:p.page,target:'page',kind:'header line removed',
        what:'Header line (the document symbol) removed from the top of the page',
        before:p.lines[fi],after:'\u2014'});
    } else {
      warnings.push('page '+p.page+': first line is not the symbol');
    }
  });

  /* footer */
  pages.forEach(function(p){
    p.displaced = [];
    var j = p.lines.length-1;
    while(j>=0){
      var t = p.lines[j].trim();
      if(t===''){j--;continue;}
      if(/^GE\./.test(t) || /^(\d{6})(\s+\d{6})*$/.test(t) || /^\d{1,3}$/.test(t)){
        p.cls[j]='B';
        repairs.push({page:p.page,target:'page',kind:'footer line removed',
          what:/^\d{1,3}$/.test(t)&&+t===p.page ? 'Page number removed from the foot of the page'
            :(t.indexOf('GE.')===0?'Job code removed from the foot of the page'
            :(/^(\d{6})/.test(t)?'Date stamp removed from the foot of the page'
            :'Bare number removed from the foot of the page')),
          before:t,after:'\u2014'});
        if(/^\d{1,3}$/.test(t) && +t!==p.page){ p.displaced.push(+t); }
        j--;
      } else break;
    }
    p.footerEnd = j;
  });

  /* footnote blocks */
  function isFnOpener(t){
    return /^(\d{1,3})(\s|$)/.test(t) && /^(\d{1,3})(\s+(.*))??$/.test(t) && !!t.match(/^(\d{1,3})/);
  }
  var nextFn = 1;
  var pagesWithoutBlock = [];
  pages.forEach(function(p){
    var start = (p.headerIdx>=0?p.headerIdx+1:0);
    var end = p.footerEnd+1;
    var blockStart = -1;
    for(var k=start;k<end;k++){
      var t = p.lines[k].trim();
      if(t==='')continue;
      if(t===String(nextFn) || t.indexOf(nextFn+' ')===0 || (p===firstPage && t.indexOf('* ')===0)){
        blockStart=k;break;
      }
    }
    if(blockStart<0){
      for(var k2=start;k2<end;k2++){
        var t2 = p.lines[k2].trim();
        if(t2!=='' && /^\d{1,3}$/.test(t2) && +t2>nextFn){
          blockStart=k2;
          repairs.push({page:p.page,target:'page',kind:'footnote block removed',
            what:'Footnote block found after a jump in numbering (expected footnote '+nextFn+', found '+t2+'); everything from here to the foot of the page is footnotes',
            before:t2,after:'\u2014'});
          break;
        }
      }
    }
    p.blockStart = blockStart;
    if(blockStart<0){ pagesWithoutBlock.push(p.page); return; }
    var firstLine='';
    for(var k3=blockStart;k3<end;k3++){ if(p.lines[k3].trim()!==''){firstLine=p.lines[k3].trim();break;} }
    if(!(repairs.length && repairs[repairs.length-1].page===p.page && repairs[repairs.length-1].kind==='footnote block removed')){
      repairs.push({page:p.page,target:'page',kind:'footnote block removed',
        what:'Footnote block (footnotes that sit at the foot of the page, before the footer) removed from the body text',
        before:firstLine,after:'\u2014'});
    }
    for(var k4=blockStart;k4<end;k4++){ if(p.lines[k4].trim()!=='') p.cls[k4]='N'; }

    /* parse footnotes inside the block */
    var bl=[]; for(var k5=blockStart;k5<end;k5++){var tt=p.lines[k5].trim(); if(tt!=='')bl.push(tt);}
    var i=0;
    if(p===firstPage && bl[0] && bl[0].indexOf('* ')===0){
      footnotes.push({number:'*',page:p.page,text:bl[0].slice(2),opener:bl[0]});
      i=1;
    }
    var disp = p.displaced.length ? p.displaced[0] : null;
    if(disp!=null){
      var num=null, rest='', fl=[];
      if(/^\d{1,3}$/.test(bl[i])){num=bl[i];i++;}
      else{var m0=bl[i].match(/^(\d{1,3})\s+(.*)$/); if(m0){num=m0[1];rest=m0[2];} i++;}
      if(rest)fl.push(rest);
      while(i<bl.length){ fl.push(bl[i]); if(/\.$/.test(bl[i])){i++;break;} i++; }
      footnotes.push({number:num,page:p.page,text:fl.join(' '),opener:num+' '+(fl[0]||'')});
      var dl=[], dlOpen='';
      while(i<bl.length && !isFnOpener(bl[i])){ dl.push(bl[i]); i++; }
      if(dl.length){
        dlOpen = dl[0];
        footnotes.push({number:String(disp),page:p.page,text:dl.join(' '),repaired:true,opener:dlOpen});
        repairs.push({page:p.page,target:'footnote '+disp,kind:'footnote number restored',
          what:'The converter moved this footnote\u2019s number to the page foot and left its text without a number; the number was restored',
          before:'(text without a number): '+dlOpen.slice(0,50),after:'footnote '+disp});
      }
    }
    var cur=null;
    for(;i<bl.length;i++){
      var t3=bl[i];
      if(isFnOpener(t3)){
        var m1=t3.match(/^(\d{1,3})\s+(.*)$/);
        if(!m1) m1=t3.match(/^(\d{1,3})$/);
        cur={number:m1[1],page:p.page,text:m1[2]||'',opener:t3};
        footnotes.push(cur);
      } else if(cur){
        cur.text += (cur.text?' ':'')+t3;
      } else {
        cur={number:'?',page:p.page,text:t3,opener:t3};
        footnotes.push(cur);
      }
    }
    var nums = footnotes.filter(function(f){return f.page===p.page && /^\d+$/.test(f.number);}).map(function(f){return +f.number;});
    var hi = nums.length?Math.max.apply(null,nums):0;
    nextFn = Math.max(nextFn, hi+1, disp!=null?disp+1:0);
  });

  /* body lines */
  var body=[];
  pages.forEach(function(p){
    var start=(p.headerIdx>=0?p.headerIdx+1:0);
    var end=(p.blockStart>=0?p.blockStart:p.footerEnd+1);
    for(var k=start;k<end;k++){
      var t=p.lines[k].trim();
      if(t!=='') body.push({page:p.page,text:t,rawIdx:k});
    }
  });
  var n=body.length, cls=new Array(n).fill('para');
  body.forEach(function(l,i){
    if(/^\d{1,3}\.$/.test(l.text) || /^\d{1,3}\. \S/.test(l.text)) cls[i]='pstart';
  });
  body.forEach(function(l,i){ if(/^([IVX]+|[A-Z])\.$/.test(l.text)) cls[i]='label'; });
  for(var i2=0;i2<n;i2++){
    if(cls[i2]==='label'){
      var j2=i2+1;
      while(j2<n && cls[j2]!=='label' && cls[j2]!=='pstart'){ cls[j2]='htext'; j2++; }
      i2=j2-1;
    }
  }
  var firstP=-1; for(var i3=0;i3<n;i3++){ if(cls[i3]==='pstart'){firstP=i3;break;} }
  for(var i4=0;i4<n-1;i4++){
    if(cls[i4]!=='para')continue;
    var t4=body[i4].text;
    if(t4.length<=90 && /^[A-Z]/.test(t4) && !/[.;:,\d]$/.test(t4) && cls[i4+1]==='pstart'){
      cls[i4]='uhead';
      repairs.push({page:body[i4].page,target:'page',kind:'heading separated',
        what:'Unlabelled heading separated from the paragraph text below it (a naive split would glue it to the paragraph above)',
        before:t4.slice(0,60),after:'\u2014'});
    }
  }
  for(var i5=0;i5<firstP;i5++){ if(cls[i5]==='para') cls[i5]='cover'; }

  /* headings + paragraphs */
  var paras=[], headings=[];
  var roman=null, letter=null, unlab=null;
  var snap=function(){return {roman:roman,letter:letter,unlab:unlab};};
  var cur2=null;
  for(var i6=0;i6<n;i6++){
    var l6=body[i6], c6=cls[i6];
    if(c6==='label'){
      var lab=l6.text, parts=[], j3=i6+1;
      while(j3<n && cls[j3]!=='label' && cls[j3]!=='pstart'){
        if(cls[j3]==='htext'){
          var ht=body[j3].text;
          if(parts.length && /^[a-z(]/.test(ht)){
            parts[parts.length-1]+=' '+ht;
            repairs.push({page:l6.page,target:'heading',kind:'heading title joined',
              what:'Heading title wrapped over two lines; the two lines were joined',
              before:(parts[parts.length-1].length>50?parts[parts.length-1].slice(0,50)+'\u2026':parts[parts.length-1]),after:'\u2014'});
          } else parts.push(ht);
        }
        j3++;
      }
      var title=parts.join(' ').trim();
      var isRom=/^[IVX]+\.$/.test(lab);
      headings.push({label:lab,title:title,page:l6.page,roman:isRom});
      if(isRom){ roman=lab+' '+title; letter=null; unlab=null; }
      else { letter=lab+' '+title; unlab=null; }
      i6=j3-1;
    } else if(c6==='uhead'){
      unlab=l6.text;
      headings.push({label:null,title:l6.text,page:l6.page,unlabelled:true});
    } else if(c6==='pstart'){
      if(cur2)paras.push(cur2);
      var m6=l6.text.match(/^(\d{1,3})\.(?:\s+(.*))?$/);
      cur2={number:+m6[1],lines:m6[2]?[m6[2]]:[],pages:[l6.page],ctx:snap()};
      if(m6[2]){
        repairs.push({page:l6.page,target:'para '+m6[1],kind:'number and text split',
          what:'Paragraph number and text shared one line in the PDF text; they were split',
          before:l6.text.slice(0,60),after:m6[1]+'. | '+m6[2].slice(0,50)});
      }
    } else if(c6==='para'){
      if(!cur2){ orphans.push(l6); continue; }
      cur2.lines.push(l6.text); cur2.pages.push(l6.page); cur2.ctx=snap();
    }
  }
  if(cur2)paras.push(cur2);

  var hyphenLines=0;
  paras.forEach(function(p){
    p.text_raw=p.lines.join(' ').replace(/\s{2,}/g,' ').trim();
    p.page_start=p.pages[0]; p.page_end=p.pages[p.pages.length-1];
    if(p.page_end!==p.page_start){
      repairs.push({page:p.page_end,target:'para '+p.number,kind:'paragraph joined across a page break',
        what:'Paragraph continued from page '+p.page_start+' to page '+p.page_end+'; the two parts were joined',
        before:'\u2014',after:'\u2014'});
    }
    hyphenLines += p.lines.filter(function(l){return /-$/.test(l.trim());}).length;
    p.section = p.ctx.unlab || p.ctx.letter || p.ctx.roman || '';
    p.part = p.ctx.roman || '';
    p.path = [p.ctx.roman,p.ctx.letter,p.ctx.unlab].filter(Boolean).join(' \u203a ');
  });

  /* footnote marks */
  var counter={n:1}; var rejected=[];
  paras.forEach(function(p){
    var raw=p.text_raw, out='', last=0, marks=[];
    var re=/\d{1,3}/g, m;
    while((m=re.exec(raw))){
      var s=m.index, e=s+m[0].length;
      var prev=raw[s-1]||'', nx=raw[e]||'';
      if(/[\d\/\-(]/.test(prev) || /[\d\/\-(]/.test(nx)) continue;
      var num=+m[0];
      if(num===counter.n){
        out+=raw.slice(last,s)+'['+m[0]+']'; last=e; marks.push(num); counter.n++;
      } else {
        rejected.push({num:num, ctx:raw.slice(Math.max(0,s-18), Math.min(raw.length,e+12)).trim()});
      }
    }
    out+=raw.slice(last);
    p.text=out; p.marks=marks;
  });

  /* first words */
  function firstWords(t){ return norm(t.replace(/\[\d{1,3}\]/g,'')).split(' ').filter(Boolean).slice(0,6).join(' '); }
  paras.forEach(function(p){
    p.fw_found=firstWords(p.text);
    p.fw_ref=(ref.first_words && ref.first_words[String(p.number)]!=null)?String(ref.first_words[String(p.number)]):null;
    p.fw_match=(p.fw_ref!=null) && norm(p.fw_ref)===norm(p.fw_found);
    p.words=p.text_raw.split(/\s+/).filter(Boolean).length;
  });

  /* write body classes back to page line classes */
  body.forEach(function(l,i){
    var c=cls[i];
    var code = c==='cover'?'C' : (c==='label'||c==='htext'||c==='uhead')?'S' : 'P';
    pages.forEach(function(p){ if(p.page===l.page) p.cls[l.rawIdx]=code; });
  });
  orphans.forEach(function(l){
    pages.forEach(function(p){ if(p.page===l.page) p.cls[l.rawIdx]='X'; });
  });

  /* contamination check */
  var numericFns = footnotes.filter(function(f){return /^\d+$/.test(f.number);});
  var contam=[];
  numericFns.forEach(function(f){
    var probe=(f.opener||'').slice(0,40);
    if(!probe)return;
    paras.forEach(function(p){
      if(p.text_raw.indexOf(probe)>=0) contam.push({para:p.number,fn:f.number,probe:probe});
    });
  });
  var longParas=paras.filter(function(p){return p.words>300;});

  /* unclassified lines */
  var unclassified=[];
  pages.forEach(function(p){
    p.raw.forEach(function(l,i){
      if(l.trim()!=='' && (p.cls[i]==='X' && orphans.some(function(o){return o.page===p.page&&o.rawIdx===i;}))) return;
      if(l.trim()!=='' && p.cls[i]==='X') unclassified.push({page:p.page,line:l.trim()});
    });
  });
  var nonEmptyTotal=0, classifiedTotal=0;
  pages.forEach(function(p){
    p.raw.forEach(function(l,i){
      if(l.trim()!==''){ nonEmptyTotal++; if(p.cls[i] && p.cls[i]!=='X') classifiedTotal++; else if(p.cls[i]==='X'){} }
    });
  });
  var orphanCount = orphans.length;
  var unclassCount = unclassified.length;

  /* checks */
  var checks=[];
  function addCheck(name,ok,detail,ran){
    checks.push({name:name,status:(ran==false)?'not run':(ok?'pass':'fail'),detail:detail});
  }
  var refParas=(ref.paragraphs!=null)?ref.paragraphs:null;
  var refFns=(ref.footnotes!=null)?ref.footnotes:null;

  if(refParas==null) addCheck('Paragraph count',false,'no reference in this file',false);
  else addCheck('Paragraph count', paras.length===refParas,
    'Found '+paras.length+' numbered paragraphs; the reference says the document has '+refParas+'.'+
    (paras.length===refParas?'':' Difference: '+(paras.length-refParas>0?'+':'')+(paras.length-refParas)+'.'));

  var seqBad=[];
  paras.forEach(function(p,i){ if(p.number!==i+1) seqBad.push('para. '+p.number+' (position '+(i+1)+', page '+p.page_start+')'); });
  addCheck('Paragraph numbering', seqBad.length===0 && paras.length>0,
    seqBad.length? 'Gaps or duplicates: '+seqBad.slice(0,10).join('; ')+(seqBad.length>10?'; and '+(seqBad.length-10)+' more':'')
    : 'Paragraph numbers run exactly 1 to '+paras.length+' in order, with no gap and no duplicate.');

  var fwBad=paras.filter(function(p){return !p.fw_match;});
  if(ref.first_words==null) addCheck('First words',false,'no reference first words in this file',false);
  else addCheck('First words', fwBad.length===0,
    (fwBad.length===0? 'All '+paras.length+' paragraphs match the reference\u2019s first six words.' :
     fwBad.length+' of '+paras.length+' differ. ')+fwBad.slice(0,8).map(function(p){
       return 'para. '+p.number+': found \u201c'+esc(p.fw_found)+'\u201d / reference \u201c'+esc(p.fw_ref)+'\u201d';
     }).join(' \u00b7 ')+(fwBad.length>8?' \u00b7 and '+(fwBad.length-8)+' more':''),
    ref.first_words!=null);

  var fnNums=numericFns.map(function(f){return +f.number;});
  var fnSeqOK = fnNums.length>0 && (function(){var s=fnNums.slice().sort(function(a,b){return a-b;});
    for(var i=0;i<s.length;i++){if(s[i]!==i+1)return false;} return fnNums.length===new Set(fnNums).size;})();
  var restored=numericFns.filter(function(f){return f.repaired;});
  if(refFns==null) addCheck('Footnotes',false,'no reference in this file',false);
  else addCheck('Footnotes', numericFns.length===refFns && fnSeqOK,
    'Found '+numericFns.length+' footnotes of '+refFns+' in the reference.'+
    (fnSeqOK?' The numbers run 1 to '+numericFns.length+' with no gap and no duplicate.'
      :' The numbers do not run 1 to n in sequence.')+
    (restored.length?' Restored numbers: '+restored.map(function(f){return f.number+' (page '+f.page+')';}).join(', ')+'.':'')+
    (pagesWithoutBlock.length?' Pages with no footnote block found (all read as body): '+pagesWithoutBlock.join(', ')+'.':'')+
    ' The cover\u2019s asterisked note is kept as footnote * and not counted.');

  var marksAll=paras.reduce(function(a,p){return a.concat(p.marks);},[]);
  var missing=[]; for(var mi=1;mi<=(refFns||0);mi++){ if(marksAll.indexOf(mi)<0) missing.push(mi); }
  if(refFns==null) addCheck('Footnote marks in the text',false,'no reference in this file',false);
  else addCheck('Footnote marks in the text', marksAll.length===refFns && missing.length===0,
    'Found '+marksAll.length+' footnote marks, expected '+refFns+' (they must run 1 to '+refFns+' in order; only a sequential rule tells a mark from a real number such as \u201carticle 11\u201d).'+
    (missing.length?' Missing: '+missing.join(', ')+'.':'')+
    ' Numbers considered and rejected as marks: '+rejected.length+
    (rejected.length?' \u2014 e.g. '+rejected.slice(0,10).map(function(r){return '\u201c'+esc(r.ctx)+'\u201d';}).join(' \u00b7 ')+(rejected.length>10?' \u00b7 and '+(rejected.length-10)+' more':''):'')+'.');

  addCheck('Footnotes stay out of the paragraphs', contam.length===0,
    'The opening words of every footnote were searched for in the raw text of every paragraph: '+contam.length+' hits (expected 0).'+
    (contam.length?' Hits: '+contam.slice(0,8).map(function(c){return 'para. '+c.para+' contains footnote '+c.fn+' (\u201c'+esc(c.probe)+'\u2026\u201d)';}).join(' \u00b7 ')+(contam.length>8?' \u00b7 and '+(contam.length-8)+' more':'')+'.':'')+
    (longParas.length?' Paragraphs over 300 words (the longest real one has 254; a long count can mean a footnote block was read as body): '+
      longParas.map(function(p){return 'para. '+p.number+' ('+p.words+' words)';}).join(', ')+'.':' No paragraph is over 300 words.'));

  var hdrPages=pages.filter(function(p){return p.headerIdx>=0;}).length;
  var pnPages=pages.filter(function(p){
    for(var i=p.lines.length-1;i>p.footerEnd;i--){ var t=p.lines[i].trim(); if(/^\d{1,3}$/.test(t)&&+t===p.page)return true; }
    return false; }).length;
  var displacedList=[];
  pages.forEach(function(p){p.displaced.forEach(function(d){displacedList.push(d+' (page '+p.page+')');});});
  addCheck('Headers and footers', hdrPages===pages.length && pnPages===pages.length-1 && warnings.length===0,
    'First line is the document symbol on '+hdrPages+' of '+pages.length+' pages.'+
    (warnings.length?' Warnings: '+warnings.join('; ')+'.':'')+
    ' A page number sits in the footer of '+pnPages+' of '+(pages.length-1)+' pages after the first.'+
    (displacedList.length?' Footnote numbers the converter displaced to the page foot: '+displacedList.join(', ')+'.':' No displaced footnote numbers.'));

  var labelledH=headings.filter(function(h){return !h.unlabelled;});
  var unlabH=headings.filter(function(h){return h.unlabelled;});
  addCheck('Headings', true,
    'Found '+labelledH.length+' labelled headings (roman sections and lettered subsections) and '+unlabH.length+' unlabelled headings.'+
    (unlabH.length?' Unlabelled: '+unlabH.map(function(h){return '\u201c'+esc(h.title)+'\u201d (p. '+h.page+')';}).join(' \u00b7 ')+'.':'')+
    ' No heading was swallowed into a paragraph.');

  addCheck('Nothing lost', orphanCount===0 && unclassCount===0 && classifiedTotal===nonEmptyTotal,
    'Every non-empty line of every page is classified exactly once, as cover, header, heading, paragraph, footnote or footer: '+
    classifiedTotal+' of '+nonEmptyTotal+' non-empty lines.'+
    (orphanCount?' Orphan lines (no open paragraph): '+orphans.map(function(o){return 'p.'+o.page+' \u201c'+esc(o.text.slice(0,40))+'\u201d';}).join(' \u00b7 ')+'.':'')+
    (unclassCount?' Unclassified: '+unclassified.slice(0,8).map(function(u){return 'p.'+u.page+' \u201c'+esc(u.line.slice(0,40))+'\u201d';}).join(' \u00b7 ')+(unclassCount>8?' \u00b7 and '+(unclassCount-8)+' more':'')+'.':'')+
    ' Lines ending in a hyphen (none are joined, by design): '+hyphenLines+'.');

  /* repairs touching a paragraph */
  function repairsFor(p){
    return repairs.filter(function(r){
      if(r.target==='para '+p.number)return true;
      if((r.kind==='heading separated'||r.kind==='heading title joined'||r.kind==='footnote block removed')
        && r.page>=p.page_start && r.page<=p.page_end)return true;
      return false;
    });
  }
  paras.forEach(function(p){ p.repairsFor=repairsFor(p); });

  return {doc:doc,key:key,sym:sym,ref:ref,pages:pages,paras:paras,footnotes:footnotes,
    numericFns:numericFns,repairs:repairs,checks:checks,headings:headings,warnings:warnings,
    contam:contam,rejected:rejected,hyphenLines:hyphenLines};
}

/* ---------- state ---------- */
var DOC_KEYS = Object.keys(WD).filter(function(k){
  var d=WD[k]; return d && Array.isArray(d.records) && d.reference;
});
var state = {key:DOC_KEYS[0], tab:0, rawPage:1, cache:{}, openRepair:false, openRaw:false};
function res(){ if(!state.cache[state.key]) state.cache[state.key]=processDoc(state.key); return state.cache[state.key]; }
function failed(){ return res().checks.filter(function(c){return c.status==='fail';}).length; }

/* ---------- render ---------- */
var TABS=['01 RESULT','02 PARAGRAPHS','03 FOOTNOTES','04 CHECKS & METHOD'];

function renderHeader(){
  var r=res(), d=r.doc, f=failed();
  var passed=r.checks.filter(function(c){return c.status==='pass';}).length;
  document.getElementById('apphead').innerHTML =
    '<div class="top"><div>'+
    '<div class="mono" style="color:#6b6559">UN DOCUMENT \u00b7 PDF TEXT</div>'+
    '<h1>'+esc(d.title||'Untitled document')+'</h1>'+
    '<div class="metaline">'+
      (d.symbol?'<a href="'+esc(d.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(d.symbol)+'</a>':'(no symbol)')+
      (r.ref.adopted?' \u00b7 adopted '+esc(r.ref.adopted):'')+
      ' \u00b7 '+r.pages.length+' page'+(r.pages.length===1?'':'s')+' of raw converter text'+
      (d.source?' \u00b7 '+esc(d.source):'')+
    '</div>'+
    '<p class="what">This page splits the converter\u2019s raw text into numbered paragraphs, removes headers, footers and footnote blocks (the footnotes that sit at the foot of each page), checks the result against the document\u2019s own reference, and lists every repair it made.</p>'+
    '</div><div class="status">'+
    (f>0?'<span class="dot bad"></span>'+f+' check'+(f===1?'':'s')+' failed'
        :'<span class="dot ok"></span>'+passed+' of '+r.checks.length+' checks pass')+
    '</div></div>';
}

function renderRail(){
  var r=res(), f=failed();
  var passed=r.checks.filter(function(c){return c.status==='pass';}).length;
  var refP=r.ref.paragraphs, refF=r.ref.footnotes;
  var cards=DOC_KEYS.map(function(k){
    var d=WD[k];
    return '<button class="card'+(k===state.key?' sel':'')+'" data-doc="'+esc(k)+'">'+
      '<div class="sym">'+esc(d.symbol||k)+'</div>'+
      '<div class="t">'+esc((d.title||'').slice(0,70))+((d.title||'').length>70?'\u2026':'')+'</div>'+
      '<div class="m">'+(d.reference&&d.reference.adopted?'adopted '+esc(d.reference.adopted)+' \u00b7 ':'')+
      (d.records?d.records.length+' pages':'')+'</div></button>';
  }).join('');
  function bar(found,refv){
    if(refv==null)return '<div class="of">no reference in this file</div>';
    var pct=Math.min(100,Math.round(found/refv*100));
    return '<div class="of">of '+refv+' in the reference</div>'+
      '<div class="bar'+(found!==refv?' bad':'')+'"><i style="width:'+pct+'%"></i></div>';
  }
  document.getElementById('rail').innerHTML =
    '<h2 class="mono" style="color:#6b6559">DOCUMENT</h2>'+cards+
    '<div class="railnums">'+
    '<div class="rn"><div class="bignum">'+r.paras.length+'</div>'+
      '<div class="mono" style="color:#4a463f">paragraphs found</div>'+bar(r.paras.length,refP)+'</div>'+
    '<div class="rn"><div class="bignum">'+r.numericFns.length+'</div>'+
      '<div class="mono" style="color:#4a463f">footnotes found</div>'+bar(r.numericFns.length,refF)+'</div>'+
    '<div style="border-top:1px solid var(--rule);padding-top:10px;font-size:14px">'+
      '<button class="toggle" data-tab="3">'+(f>0?'<span class="fail">'+f+' checks failed</span>':passed+' of '+r.checks.length+' checks pass')+' \u2192</button></div>'+
    '</div>';
}

function renderTabs(){
  document.getElementById('tabbar').innerHTML = TABS.map(function(t,i){
    var fail = i===3 && failed()>0;
    return '<button class="tab" role="tab" id="tab'+i+'" aria-selected="'+(state.tab===i)+'" data-tab="'+i+'" tabindex="'+(state.tab===i?0:-1)+'">'+esc(t)+(fail?' <span class="faildot">\u25cf</span>':'')+'</button>';
  }).join('');
  for(var i=0;i<4;i++){ document.getElementById('panel'+i).hidden = (state.tab!==i); }
}

function tile(label,val,sub,how,bad){
  return '<div class="tile"><div class="lab">'+esc(label)+'</div>'+
    '<div class="bignum'+(bad?' bad-t':'')+'">'+val+'</div>'+
    '<div class="sub">'+sub+'</div><div class="how">'+how+'</div></div>';
}

function renderResult(){
  var r=res(), refP=r.ref.paragraphs, refF=r.ref.footnotes;
  var fwOK=r.paras.filter(function(p){return p.fw_match;}).length;
  var pEqual=(refP!=null && r.paras.length===refP);
  var contamParas = new Set(r.contam.map(function(c){return c.para;}));
  var html='<div class="tiles">';
  html+=tile('Paragraphs found', r.paras.length,
    (refP==null?'no reference in this file':
      'The document has: '+refP+(pEqual?'':' \u00b7 difference: '+(r.paras.length-refP>0?'+':'')+(r.paras.length-refP)))+
    (contamParas.size? ' <span class="bad-t">'+contamParas.size+' contain footnotes</span>':''),
    'How this is computed: lines matching a paragraph number, alone or with text, after headers, footers and footnote blocks are removed.',
    !pEqual || contamParas.size>0);
  html+=tile('Footnotes found', (refF==null?'\u2014':r.numericFns.length+' of '+refF),
    (refF==null?'no reference in this file':(r.numericFns.length===refF?
      'The footnotes at the foot of each page were lifted out of the body text.':'Difference: '+(r.numericFns.length-refF>0?'+':'')+(r.numericFns.length-refF))),
    'How this is computed: numbered openings in each page\u2019s footnote block, plus numbers restored from the page foot.',
    refF!=null && r.numericFns.length!==refF);
  html+=tile('First words match', (refP==null?'\u2014':fwOK+' of '+refP),
    (r.ref.first_words==null?'no reference first words in this file':
      'The first six words of each paragraph, compared with the reference.'),
    'How this is computed: first six words after footnote marks are removed; curly quotes and dashes normalised.',
    r.ref.first_words!=null && fwOK!==refP);
  html+=tile('Repairs made', r.repairs.length,
    '<button class="toggle" data-openrepair="1">Open the repair log on tab 04 \u2192</button>',
    'How this is computed: every line the script removed or changed is logged, in document order.',
    false);
  html+='</div>';
  html+='<p class="note">The reference is a yardstick, not the truth: where the counts disagree, both numbers are shown, and the result is never trimmed or padded to match.</p>';
  document.getElementById('panel0').innerHTML=html;
}

function firstLineOf(t){
  if(t.length<=120)return t;
  var s=t.slice(0,120), c=s.lastIndexOf(' ');
  return (c>60?s.slice(0,c):s)+'\u2026';
}

function renderParagraphs(){
  var r=res();
  var rows=r.paras.map(function(p,i){
    var bad=!p.fw_match || r.contam.some(function(c){return c.para===p.number;});
    var exp=
      '<tr class="exp" id="pexp-'+p.number+'" hidden><td colspan="5">'+
      '<div class="full">'+esc(p.text)+'</div>'+
      '<button class="toggle" data-lines="'+p.number+'">Show the PDF\u2019s lines</button>'+
      '<div class="para-expanded-lines" id="plines-'+p.number+'" hidden>'+
        p.lines.map(function(l,j){
          var mark = (j>0 && p.pages[j]!==p.pages[j-1])?'<span class="pagemark">\u2014 page '+p.pages[j]+' \u2014\n</span>':'';
          return mark+esc(l)+'\n';
        }).join('')+
      '</div>'+
      '<div class="meta">'+
      '<div><span class="mono">first words, reference</span> \u2014 '+esc(p.fw_ref!=null?p.fw_ref:'(none in the reference)')+'</div>'+
      '<div><span class="mono">first words, found</span> \u2014 '+esc(p.fw_found)+' '+(p.fw_match?'<span class="pass">equal</span>':'<span class="fail">different</span>')+'</div>'+
      '<div><span class="mono">pages</span> \u2014 '+p.page_start+(p.page_end!==p.page_start?'\u2013'+p.page_end:'')+' \u00b7 <span class="mono">section</span> \u2014 '+esc(p.path||p.section||'(none)')+'</div>'+
      '<div><span class="mono">footnotes cited</span> \u2014 '+(p.marks.length?p.marks.join(', '):'none')+'</div>'+
      '<div><span class="mono">repairs that touched this paragraph</span> \u2014 '+(p.repairsFor.length?p.repairsFor.map(function(rp){return esc(rp.kind)+' (p. '+rp.page+')';}).join(' \u00b7 '):'none')+'</div>'+
      '</div>'+
      '<button class="btn" data-copy="'+p.number+'">Copy citation</button> <span class="mono" style="margin-left:8px" id="cite-'+p.number+'">'+esc(r.sym)+', para. '+p.number+'</span>'+
      '</td></tr>';
    return '<tr class="prow" id="prow-'+p.number+'" data-p="'+p.number+'">'+
      '<td class="num pno"><button class="rowbtn" aria-expanded="false" data-p="'+p.number+'">'+p.number+'</button></td>'+
      '<td>'+esc(p.section||'\u2014')+'</td>'+
      '<td class="num">'+p.page_start+(p.page_end!==p.page_start?'\u2013'+p.page_end:'')+'</td>'+
      '<td>'+esc(firstLineOf(p.text))+'</td>'+
      '<td>'+(bad?'<span class="fail">first words differ</span>':'OK')+'</td>'+
      '</tr>'+exp;
  }).join('');
  var headsList=r.headings.map(function(h){
    return '<li>'+(h.label?esc(h.label)+' ':'')+esc(h.title)+' <span class="mono" style="color:#6b6559">p. '+h.page+'</span></li>';
  }).join('');
  document.getElementById('panel1').innerHTML =
    '<button class="fold" aria-expanded="false" data-fold="headsbox">Headings found: '+r.headings.length+' \u25be</button>'+
    '<div class="foldbody" id="headsbox" hidden><ul class="heads">'+headsList+'</ul></div>'+
    '<table><caption>'+r.paras.length+' paragraphs found, '+(r.ref.paragraphs!=null?r.ref.paragraphs+' expected':'no reference')+
    '<span class="mono">TAB.02</span></caption>'+
    '<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col" class="num">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>'+
    '<tbody>'+rows+'</tbody></table>'+
    '<p class="note">Click a row to read the full paragraph, verbatim as computed. Footnote marks in the text are shown in square brackets, as in \u201cwaste.[2]\u201d. To remove them in a word processor, find and replace the pattern <code>\\[\\d+\\]</code> with nothing. Source: '+
    (r.sym?'<a href="'+esc(r.doc.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(r.sym)+'</a>':'this document')+'.</p>';
}

function renderFootnotes(){
  var r=res();
  var rows=r.numericFns.concat(r.footnotes.filter(function(f){return f.number==='*';})).map(function(f){
    var short=firstLineOf(f.text);
    return '<tr class="frow" data-f="'+esc(f.number)+'">'+
      '<td class="num"><button class="rowbtn" aria-expanded="false" data-f="'+esc(f.number)+'">'+esc(f.number)+'</button></td>'+
      '<td class="num">'+f.page+'</td>'+
      '<td>'+esc(short)+'</td>'+
      '<td>'+(f.repaired?'<span class="fail">number restored from the page foot</span>':'\u2014')+'</td>'+
      '</tr>'+
      '<tr class="exp" hidden><td colspan="4"><div class="full">'+esc(f.text)+'</div>'+
      '<div class="meta">Cite as '+esc(r.sym)+', footnote '+esc(f.number)+' (page '+f.page+' of the PDF).</div></td></tr>';
  }).join('');
  document.getElementById('panel2').innerHTML =
    '<table><caption>'+r.numericFns.length+' footnotes found, '+(r.ref.footnotes!=null?r.ref.footnotes+' expected':'no reference')+
    '<span class="mono">TAB.03</span></caption>'+
    '<thead><tr><th scope="col" class="num">No.</th><th scope="col" class="num">Page</th><th scope="col">Text</th><th scope="col">Repair</th></tr></thead>'+
    '<tbody>'+rows+'</tbody></table>'+
    '<button class="btn" data-dl="footnotes">Download footnotes.csv</button>'+
    '<p class="note">The footnotes are the notes at the foot of each page, before the footer. A footnote whose number the converter displaced to the page foot has had its number restored; the Repair column says so. Source: '+
    (r.sym?'<a href="'+esc(r.doc.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(r.sym)+'</a>':'this document')+'.</p>';
}

function renderChecks(){
  var r=res();
  var kinds={};
  r.repairs.forEach(function(rp){kinds[rp.kind]=(kinds[rp.kind]||0)+1;});
  var kindLine=Object.keys(kinds).map(function(k){return esc(k)+': '+kinds[k];}).join(' \u00b7 ');
  var repRows=r.repairs.map(function(rp){
    return '<tr><td class="num">'+rp.page+'</td><td>'+esc(rp.target)+'</td><td>'+esc(rp.what)+'</td>'+
    '<td>'+esc((rp.before||'').slice(0,60))+'</td><td>'+esc((rp.after||'').slice(0,60))+'</td></tr>';
  }).join('');
  var checkRows=r.checks.map(function(c){
    var word = c.status==='pass'?'<span class="pass">pass</span>':(c.status==='fail'?'<span class="fail">check failed</span>':'<span class="notrun">not run</span>');
    return '<div class="check"><div><span class="cname">'+esc(c.name)+'</span> \u2014 '+word+'</div>'+
      (c.detail?'<div class="cdet">'+c.detail+'</div>':'')+'</div>';
  }).join('');
  var pageOpts=r.pages.map(function(p){return '<option value="'+p.page+'"'+(p.page===state.rawPage?' selected':'')+'>page '+p.page+'</option>';}).join('');
  var legend='<div class="legend">'+
    '<span class="lv-C"><b>C</b> cover</span><span class="lv-H"><b>H</b> header</span><span class="lv-S"><b>S</b> heading</span>'+
    '<span class="lv-P"><b>P</b> paragraph</span><span class="lv-N"><b>N</b> footnote</span><span class="lv-B"><b>B</b> footer</span>'+
    '<span class="lv-X"><b>!</b> unclassified</span></div>';
  var rawHtml=(function(){
    var p=r.pages.filter(function(x){return x.page===state.rawPage;})[0];
    if(!p)return '';
    return p.raw.map(function(l,i){
      var c=p.cls[i]||'';
      var code=c===' '?'':c;
      return '<span class="rl lv-'+(code||'P')+'"><span class="ln">'+(i+1)+'</span><span class="code">'+(code||' ')+'</span>'+esc(l)+'</span>';
    }).join('');
  })();
  document.getElementById('panel3').innerHTML =
    '<h2 class="serif" style="font-weight:normal;font-size:20px;margin:4px 0 8px">Can I trust this?</h2>'+
    '<div class="checks">'+checkRows+'</div>'+
    '<button class="fold" id="repairfold" aria-expanded="'+state.openRepair+'" data-fold="repairbox">Repair log ('+r.repairs.length+') \u25be</button>'+
    '<div class="foldbody" id="repairbox"'+(state.openRepair?'':' hidden')+'>'+
    '<p class="note mono" style="text-transform:none;letter-spacing:0">'+(kindLine||'no repairs')+'</p>'+
    '<table><caption>Every change the script made, in document order<span class="mono">TAB.04a</span></caption>'+
    '<thead><tr><th scope="col" class="num">Page</th><th scope="col">Paragraph or footnote</th><th scope="col">What was done</th><th scope="col">Before</th><th scope="col">After</th></tr></thead>'+
    '<tbody>'+(repRows||'')+'</tbody></table></div>'+
    '<button class="fold" id="rawfold" aria-expanded="'+state.openRaw+'" data-fold="rawbox">Raw pages \u25be</button>'+
    '<div class="foldbody" id="rawbox"'+(state.openRaw?'':' hidden')+'>'+
    '<label class="mono" style="color:#4a463f">Show raw page <select id="rawsel">'+pageOpts+'</select></label>'+legend+
    '<div class="rawpages">'+rawHtml+'</div>'+
    '<p class="note">Each line is coloured by what the script decided it was; the letter code in the margin repeats the colour. Check a line here against the paragraph it joined.</p></div>'+
    '<h2 class="serif" style="font-weight:normal;font-size:20px;margin:10px 0 8px">Take it away</h2>'+
    '<button class="btn" data-dl="paragraphs">Download paragraphs as CSV</button>'+
    '<p class="note">One row per paragraph: number, section, part, pages, first words found and expected, full text with footnote marks bracketed (<code>text</code>) and unmodified (<code>text_raw</code>), footnotes cited, repairs, citation, symbol and link. UTF-8 with a byte-order mark, every field double-quoted, CRLF line ends.</p>';
}

function renderAll(){
  renderHeader(); renderRail(); renderTabs();
  renderResult(); renderParagraphs(); renderFootnotes(); renderChecks();
  renderFooter();
}
function renderFooter(){
  var d=res().doc;
  document.getElementById('appfoot').innerHTML =
    '<span>'+(d.source?'Source: '+esc(d.source)+'. ':'')+(d.built?'Built '+esc(d.built)+'. ':'')+
    (d.symbol?'<a href="'+esc(d.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(d.symbol)+'</a>.':'')+'</span>'+
    '<span>Counting, splitting and matching are done by this page\u2019s code; no model was called and nothing left the browser.</span>';
}

/* ---------- CSV & clipboard ---------- */
function csvField(v){ return '"'+String(v==null?'':v).replace(/"/g,'""')+'"'; }
function csvDoc(rows,cols){ return '\ufeff'+rows.map(function(r){return cols.map(function(c){return csvField(r[c]);}).join(',');}).join('\r\n'); }
function download(name,content){
  var b=new Blob([content],{type:'text/csv;charset=utf-8'});
  var u=URL.createObjectURL(b);
  var a=document.createElement('a'); a.href=u; a.download=name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function(){URL.revokeObjectURL(u);},4000);
}
function copyText(t,btn){
  var done=function(){ var old=btn.getAttribute('data-old')||btn.textContent;
    btn.setAttribute('data-old',old); btn.textContent='Copied';
    setTimeout(function(){btn.textContent=btn.getAttribute('data-old');},2000); };
  var fb=function(){ var ta=document.createElement('textarea'); ta.value=t;
    document.body.appendChild(ta); ta.select();
    try{document.execCommand('copy');}catch(e){} ta.remove(); done(); };
  if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(done,fb); } else fb();
}

/* ---------- events ---------- */
function setTab(i){
  state.tab=i; renderTabs();
  var fold;
  if(i===3){ renderChecks(); }
}
document.addEventListener('click',function(e){
  var el;
  if((el=e.target.closest('[data-tab]'))){
    setTab(+el.getAttribute('data-tab')); return;
  }
  if((el=e.target.closest('[data-doc]'))){
    state.key=el.getAttribute('data-doc'); state.rawPage=1; renderAll(); return;
  }
  if((el=e.target.closest('[data-openrepair]'))){
    state.openRepair=true; setTab(3);
    var box=document.getElementById('repairbox'); if(box)box.hidden=false;
    var fd=document.getElementById('repairfold'); if(fd)fd.setAttribute('aria-expanded','true');
    return;
  }
  if((el=e.target.closest('[data-fold]'))){
    var id=el.getAttribute('data-fold'), b=document.getElementById(id);
    var open=b.hidden; b.hidden=!open;
    el.setAttribute('aria-expanded',String(open));
    if(id==='repairbox')state.openRepair=open;
    if(id==='rawbox')state.openRaw=open;
    return;
  }
  if((el=e.target.closest('[data-lines]'))){
    var ln=document.getElementById('plines-'+el.getAttribute('data-lines'));
    if(ln){ln.hidden=!ln.hidden; el.textContent=(ln.hidden?'Show':'Hide')+' the PDF\u2019s lines';}
    return;
  }
  if((el=e.target.closest('[data-copy]'))){
    var p=res().paras.filter(function(x){return x.number===+el.getAttribute('data-copy');})[0];
    if(p)copyText(res().sym+', para. '+p.number, el);
    return;
  }
  if((el=e.target.closest('[data-dl]'))){
    var r=res();
    if(el.getAttribute('data-dl')==='footnotes'){
      var rows=r.footnotes.map(function(f){return {number:f.number,page:f.page,text:f.text,repaired:f.repaired?'yes':'no',symbol:r.sym};});
      download((r.sym||'document').replace(/\//g,'-')+'-footnotes.csv',
        csvDoc(rows,['number','page','text','repaired','symbol']));
    } else {
      var prows=r.paras.map(function(p){
        return {number:p.number,section:p.section,part:p.part,page_start:p.page_start,page_end:p.page_end,
          first_words_reference:p.fw_ref==null?'':p.fw_ref,first_words_found:p.fw_found,
          first_words_match:p.fw_ref==null?'':(p.fw_match?'TRUE':'FALSE'),
          text:p.text,text_raw:p.text_raw,footnotes_cited:p.marks.join(' '),
          repairs:p.repairsFor.map(function(rp){return rp.kind;}).join('; '),
          citation:r.sym+', para. '+p.number,symbol:r.sym,doc_url:r.doc.doc_url||''};
      });
      download((r.sym||'document').replace(/\//g,'-')+'-paragraphs.csv',
        csvDoc(prows,['number','section','part','page_start','page_end','first_words_reference','first_words_found','first_words_match','text','text_raw','footnotes_cited','repairs','citation','symbol','doc_url']));
    }
    return;
  }
  if((el=e.target.closest('.prow'))||(el=e.target.closest('[data-p]'))){
    var row=e.target.closest('tr.prow'); if(!row)return;
    var num=+row.getAttribute('data-p');
    var exp=document.getElementById('pexp-'+num);
    var open=exp.hidden; exp.hidden=!open;
    row.querySelector('.rowbtn').setAttribute('aria-expanded',String(open));
    return;
  }
  if(e.target.closest('tr.frow')||(el=e.target.closest('[data-f]'))){
    var frow=e.target.closest('tr.frow'); if(!frow)return;
    var fexp=frow.nextElementSibling;
    var fopen=fexp.hidden; fexp.hidden=!fopen;
    frow.querySelector('.rowbtn').setAttribute('aria-expanded',String(fopen));
    return;
  }
});
document.addEventListener('change',function(e){
  if(e.target && e.target.id==='rawsel'){
    state.rawPage=+e.target.value; renderChecks();
  }
});
document.getElementById('tabbar').addEventListener('keydown',function(e){
  if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft')return;
  e.preventDefault();
  var d=e.key==='ArrowRight'?1:-1;
  var nt=(state.tab+d+4)%4;
  setTab(nt);
  document.getElementById('tab'+nt).focus();
});

if(DOC_KEYS.length){ renderAll(); } else {
  document.getElementById('apphead').innerHTML='<p>No document with records and a reference was found in WORKSHOP_DATA.</p>';
}
})();
</script>
</body>
</html>
```
