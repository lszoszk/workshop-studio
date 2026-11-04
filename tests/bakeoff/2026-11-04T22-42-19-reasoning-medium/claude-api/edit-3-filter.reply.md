I added a "Document kind" select under heading 02, next to Mechanism, Body and Type. The data has no field for document type, so the app derives it from `mechanism` and the symbol. Treaty-body symbols containing "/CO/" count as concluding observations, other treaty-body documents are grouped separately, and UPR and Special Procedures keep one kind each. Because this is a pattern rule, check unusual symbols on tab 03 or in the records table.

```edit
<<<<<<< SEARCH
      <label for="fType">Type</label><select id="fType"></select>
=======
      <label for="fType">Type</label><select id="fType"></select>
      <label for="fDk">Document kind</label><select id="fDk"></select>
      <div class="hint" style="margin-top:4px">derived from mechanism and symbol ("/CO/" = concluding observations)</div>
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  const m=o.text.match(PARA_RE);o.para=m?m[1]:null;
=======
  const m=o.text.match(PARA_RE);o.para=m?m[1]:null;
  o.dkind=o.mechanism===UPR?'UPR report (recommendations)':o.mechanism==='Treaty bodies'?(/\/CO\//i.test(o.symbol)?'Concluding observations':'Other treaty-body document'):o.mechanism==='Special Procedures'?'Special Procedures report':o.mechanism;
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
const S={kw:'',mech:'',body:'',type:'',state:'',yf:'',yt:'',sdg:'',themes:[],tab:0,open:null,asc:false,limit:50,row:null,uprList:false};
=======
const S={kw:'',mech:'',body:'',type:'',dkind:'',state:'',yf:'',yt:'',sdg:'',themes:[],tab:0,open:null,asc:false,limit:50,row:null,uprList:false};
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  if(S.type&&r.type!==S.type)return false;
=======
  if(S.type&&r.type!==S.type)return false;
  if(S.dkind&&r.dkind!==S.dkind)return false;
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  if(S.type)d.push({l:'Type: '+S.type,rm:()=>{S.type=''}});
=======
  if(S.type)d.push({l:'Type: '+S.type,rm:()=>{S.type=''}});
  if(S.dkind)d.push({l:'Document kind: '+S.dkind,rm:()=>{S.dkind=''}});
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  const yo=YEARS.map(y=>opt(y,y)).join('');
=======
  const dk={};RECS.forEach(r=>dk[r.dkind]=(dk[r.dkind]||0)+1);
  $('fDk').innerHTML=opt('','All document kinds')+Object.keys(dk).sort((a,b)=>dk[b]-dk[a]).map(k=>opt(k,k+' ('+fmt(dk[k])+')')).join('');
  const yo=YEARS.map(y=>opt(y,y)).join('');
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  $('fMech').value=S.mech;$('fType').value=S.type;$('fState').value=S.state;
=======
  $('fMech').value=S.mech;$('fType').value=S.type;$('fState').value=S.state;$('fDk').value=S.dkind;
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
$('fType').onchange=e=>{S.type=e.target.value;go()};
=======
$('fType').onchange=e=>{S.type=e.target.value;go()};
$('fDk').onchange=e=>{S.dkind=e.target.value;go()};
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
$('clearAll').onclick=()=>{S.kw='';S.mech='';
=======
$('clearAll').onclick=()=>{S.kw='';S.dkind='';S.mech='';
>>>>>>> REPLACE
```