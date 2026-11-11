I added the failing-document panel to tab 03, between the table and the downloads. It shows the first document with a failed check and, per failed check, the lines the rules tripped on, each with its page. "Copy for the model" copies your request followed by those lines. The panel is computed from the checks, so after a rule change it moves to the next failing document by itself. No rule is changed. I have not run it on the real data.

The "rule changes" list starts empty. It is filled from a `RULE_CHANGES` list in the code, which the model edits when you paste its answer back.

```edit
<<<<<<< SEARCH
  const info={page:pg.page,header:false,pageNumber:false,displaced:[]};
=======
  const info={page:pg.page,header:false,pageNumber:false,displaced:[],first:'',last:''};
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
    if(ls[f].text===symbol){ls[f].kind='header';info.header=true;}
=======
    info.first=ls[f].text;
    if(ls[f].text===symbol){ls[f].kind='header';info.header=true;}
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  let k=ls.length-1;
=======
  for(let z=ls.length-1;z>=0;z--){if(ls[z].text!==''){info.last=ls[z].text;break;}}
  let k=ls.length-1;
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
const cPass=checks.filter(c=>c.status==='pass').length,cFail=checks.filter(c=>c.status==='fail').length;
=======
function numLines(n){const out=[];all.forEach(l=>{const t=l.text;if(t!==''&&(t===String(n)||t===n+'.'||t.indexOf(n+'. ')===0))out.push({page:l.page,text:t});});return out;}
const startTrip=p=>({page:p.startPage,text:p.number+'. '+(p.lines[0]?p.lines[0].text:'')});
checks.forEach(c=>{
  const tr=[];c.trips=tr;
  if(c.status!=='fail')return;
  if(c.name==='Paragraph count'&&refFW){
    const have=new Set(nums.map(String));
    paras.forEach(p=>{if(refFW[String(p.number)]==null)tr.push(startTrip(p));});
    Object.keys(refFW).forEach(k=>{if(!have.has(k))numLines(k).forEach(x=>tr.push(x));});
  }else if(c.name==='Numbering'){
    let pv=0;paras.forEach(p=>{if(p.number!==pv+1)tr.push(startTrip(p));pv=p.number;});
  }else if(c.name==='First words'){
    fwBad.forEach(x=>{
      const p=paras.find(q=>q.number===x.n);
      if(p){const s=startTrip(p);tr.push({page:s.page,text:s.text+'   [found: '+x.found+' / reference: '+x.ref+']'});}
      else numLines(x.n).forEach(y=>tr.push(y));
    });
  }else if(c.name==='Headers and footers'){
    pageInfo.forEach((x,i)=>{
      if(!x.header)tr.push({page:x.page,text:'first line: '+(x.first||'(empty page)')});
      if(i>0&&!x.pageNumber)tr.push({page:x.page,text:'last line: '+(x.last||'(none)')+' (no page number found in the footer)'});
    });
  }else if(c.name==='Nothing lost'){
    unclassified.forEach(l=>tr.push({page:l.page,text:l.text}));
  }
});
const cPass=checks.filter(c=>c.status==='pass').length,cFail=checks.filter(c=>c.status==='fail').length;
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
const S={tab:1,sel:0,open:new Set(),pdf:new Set(),checks:false,flags:false,heads:false,focus:null,copied:null};
=======
const S={tab:1,sel:0,open:new Set(),pdf:new Set(),checks:false,flags:false,heads:false,focus:null,copied:null,cm:false};
/* List of rule changes. Each entry: {change:'what was changed', fixed:['symbol', ...]} */
const RULE_CHANGES=[];
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
function p3(){
  const totP=AN.reduce((a,x)=>a+x.paras.length,0);
=======
function failFirst(){return AN.find(A=>A.cFail>0)||null;}
function modelText(A){
  let o='Here are the lines that broke the rules for '+A.symbol+'. Change the rule so that this document passes and every document that passed before still passes, and add the change to a list of rule changes on tab 03, with the documents it fixed.\n';
  A.checks.filter(c=>c.status==='fail').forEach(c=>{
    o+='\nCheck failed: '+c.name+' ('+c.got+')\n';
    if(!c.trips.length)o+='  (no single line to show for this check)\n';
    c.trips.slice(0,40).forEach(x=>{o+='  page '+x.page+': '+x.text+'\n';});
    if(c.trips.length>40)o+='  and '+(c.trips.length-40)+' more\n';
  });
  return o;
}
function failPanel(){
  const A=failFirst();
  let h='<div class="sec"><h2 class="q">First document that fails</h2>';
  if(!A)h+='<p class="ok">No document has a failed check.</p>';
  else{
    h+='<div class="hint">'+esc(A.symbol)+' · '+A.cFail+' failed check'+(A.cFail>1?'s':'')+'. The lines the rules tripped on, each with its page. How this is computed: the same checks as tab 01, with the lines behind each failure.</div>';
    A.checks.filter(c=>c.status==='fail').forEach(c=>{
      h+='<div style="margin-top:14px"><b>'+esc(c.name)+'</b> <span class="bad">check failed</span><div class="hint">'+esc(c.got)+'</div>';
      if(!c.trips.length)h+='<div class="hl">No single line to show for this check.</div>';
      c.trips.slice(0,20).forEach(x=>{h+='<div class="hl"><span class="mono red">page '+esc(x.page)+'</span> '+esc(x.text)+'</div>';});
      if(c.trips.length>20)h+='<div class="hl">and '+(c.trips.length-20)+' more (all are in the copied text, up to 40)</div>';
      h+='</div>';
    });
    h+='<div style="margin-top:12px"><button class="btn pri" data-act="copyModel" data-key="cm">'+(S.cm?'Copied':'Copy for the model')+'</button></div>';
  }
  h+='<div style="margin-top:14px"><div class="mono">Rule changes ('+RULE_CHANGES.length+')</div>';
  if(!RULE_CHANGES.length)h+='<div class="hint">No rule change yet.</div>';
  else h+='<ol>'+RULE_CHANGES.map(r=>'<li>'+esc(r.change)+' <span class="hint">fixed: '+esc((r.fixed||[]).join(', ')||'none')+'</span></li>').join('')+'</ol>';
  return h+'</div></div>';
}
function p3(){
  const totP=AN.reduce((a,x)=>a+x.paras.length,0);
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  h+='<div class="sec"><h2 class="q">Take all '+AN.length+' documents away</h2><div class="hint" style="margin-bottom:8px">One file with every paragraph of every document, each record with its symbol.</div>'
=======
  h+=failPanel();
  h+='<div class="sec"><h2 class="q">Take all '+AN.length+' documents away</h2><div class="hint" style="margin-bottom:8px">One file with every paragraph of every document, each record with its symbol.</div>'
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  else if(act==='jump'){jump(n);}
=======
  else if(act==='jump'){jump(n);}
  else if(act==='copyModel'){
    const F=failFirst();
    if(F)copyText(modelText(F),()=>{S.cm=true;S.focus='cm';render();setTimeout(()=>{S.cm=false;render();},2000);});
  }
>>>>>>> REPLACE
```