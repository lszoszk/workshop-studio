I added a "Document type" select under heading 02 in the left rail, so the rail still has three headings. The data has no such field, so the app derives it from `mechanism` and `symbol`:

- UPR records are "UPR recommendations".
- Treaty-body records with `/CO/` in the symbol are "Concluding observations".
- Other treaty-body records are "Other treaty-body document".
- Special Procedures records are "Special Procedures report".

I have not run it on your data. The filter also shows as a chip and is included in the CSV.

```edit
<<<<<<< SEARCH
        <label class="lab" for="ftype">Type</label><select id="ftype"></select>
=======
        <label class="lab" for="ftype">Type</label><select id="ftype"></select>
        <label class="lab" for="fdt">Document type</label><select id="fdt"></select>
        <div class="hint">derived from mechanism and symbol (/CO/ = concluding observations), not a UN label</div>
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  r._fl=firstLine(t);
=======
  r._fl=firstLine(t);
  r._dt=docType(r);
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
const uniq=a=>[...new Set(a)];
=======
function docType(r){
  if(r.mechanism===UPR)return 'UPR recommendations';
  if(r.mechanism==='Treaty bodies')return /\/CO\//i.test(r.symbol||'')?'Concluding observations':'Other treaty-body document';
  if(r.mechanism==='Special Procedures')return 'Special Procedures report';
  return 'Other document';
}
const uniq=a=>[...new Set(a)];
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
const typeOf=r=>r.type==null||r.type===''?'(no type)':r.type;
=======
const typeOf=r=>r.type==null||r.type===''?'(no type)':r.type;
const dts=uniq(R.map(r=>r._dt)).sort();
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
const S={tab:0,open:-1,kw:'',mech:'',body:'',type:'',state:'',yf:'',yt:'',sdg:'',themes:[],shown:50
=======
const S={tab:0,open:-1,kw:'',mech:'',body:'',type:'',state:'',yf:'',yt:'',sdg:'',dt:'',themes:[],shown:50
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
$('fyf').innerHTML=opt('','Earliest')+years.map(y=>opt(y,y)).join('');
=======
$('fdt').innerHTML=opt('','All document types')+dts.map(d=>opt(d,d+' ('+fmt(R.filter(r=>r._dt===d).length)+')')).join('');
$('fyf').innerHTML=opt('','Earliest')+years.map(y=>opt(y,y)).join('');
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
    if(S.type&&typeOf(r)!==S.type)return false;
=======
    if(S.type&&typeOf(r)!==S.type)return false;
    if(S.dt&&r._dt!==S.dt)return false;
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  if(S.type)c.push({l:'Type: '+S.type,f:()=>{S.type=''}});
=======
  if(S.type)c.push({l:'Type: '+S.type,f:()=>{S.type=''}});
  if(S.dt)c.push({l:'Document: '+S.dt,f:()=>{S.dt=''}});
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
const sig=()=>JSON.stringify([S.kw.trim(),S.mech,S.body,S.type,S.state,
=======
const sig=()=>JSON.stringify([S.kw.trim(),S.mech,S.body,S.type,S.dt,S.state,
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  $('fmech').value=S.mech;$('fbody').value=S.body;$('ftype').value=S.type;$('fst').value=S.state;
=======
  $('fmech').value=S.mech;$('fbody').value=S.body;$('ftype').value=S.type;$('fst').value=S.state;$('fdt').value=S.dt;
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
$('ftype').onchange=e=>{S.type=e.target.value;update()};
=======
$('ftype').onchange=e=>{S.type=e.target.value;update()};
$('fdt').onchange=e=>{S.dt=e.target.value;update()};
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
S.type='';S.state='';S.yf='';S.yt='';S.sdg='';S.themes=[];fillBody();
=======
S.type='';S.dt='';S.state='';S.yf='';S.yt='';S.sdg='';S.themes=[];fillBody();
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  o+=['date','mechanism','body','type','symbol',
=======
  o+=['date','mechanism','body','type','document_type','symbol',
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
rows.forEach(r=>{o+=[r.date,r.mechanism,r.body,r.type,r.symbol,
=======
rows.forEach(r=>{o+=[r.date,r.mechanism,r.body,r.type,r._dt,r.symbol,
>>>>>>> REPLACE
```