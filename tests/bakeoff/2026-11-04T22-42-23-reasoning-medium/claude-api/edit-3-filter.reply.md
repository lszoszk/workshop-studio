I've added a "Document type" select under heading 02 in the left rail. The data has no field with that name, so the app derives it from the mechanism and the document symbol. It lists "Concluding observations" (treaty-body symbols containing /CO/), "Other treaty-body documents", "UPR working group reports" and "Special Procedures reports". This is the app's own grouping, not a UN label, and it works as a filter, a removable chip and a line in the CSV filter notes.

```edit
<<<<<<< SEARCH
        <label>Type<select id="ft"></select></label>
=======
        <label>Type<select id="ft"></select></label>
        <label>Document type <span class="hint">derived from symbol</span><select id="fdt"></select></label>
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
const recs=(U.records||[]).map((r,i)=>{
=======
function docType(r){
  const s=String(r.symbol||'');
  if(r.mechanism==='Universal Periodic Review')return 'UPR working group reports';
  if(r.mechanism==='Special Procedures')return 'Special Procedures reports';
  if(r.mechanism==='Treaty bodies')return /\/CO\//i.test(s)?'Concluding observations':'Other treaty-body documents';
  return r.mechanism||'Other';
}
const recs=(U.records||[]).map((r,i)=>{
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
    para:pm?pm[1]:null,isU:isU,sts:isU?states(t):[],
=======
    para:pm?pm[1]:null,isU:isU,sts:isU?states(t):[],dt:docType(r),
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
let F={kw:'',mech:'',body:'',type:'',state:'',yf:'',yt:'',sdg:'',themes:[]};
=======
let F={kw:'',mech:'',body:'',type:'',dtype:'',state:'',yf:'',yt:'',sdg:'',themes:[]};
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  if(F.type&&r.type!==F.type)return false;
=======
  if(F.type&&r.type!==F.type)return false;
  if(F.dtype&&r.dt!==F.dtype)return false;
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  if(F.type)a.push('type = '+F.type);
=======
  if(F.type)a.push('type = '+F.type);
  if(F.dtype)a.push('document type = '+F.dtype);
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  if(F.type)c.push([F.type,()=>F.type='']);
=======
  if(F.type)c.push([F.type,()=>F.type='']);
  if(F.dtype)c.push([F.dtype,()=>F.dtype='']);
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
$('fsw').hidden=!stNames.length;
=======
$('fsw').hidden=!stNames.length;
const dtNames=uniq(recs.map(r=>r.dt)).sort();
opts($('fdt'),[['','All document types']].concat(dtNames.map(m=>[m,m+' ('+fmt(recs.filter(r=>r.dt===m).length)+')'])));
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  $('fm').value=F.mech;$('fb').value=F.body;$('ft').value=F.type;$('fs').value=F.state;
=======
  $('fm').value=F.mech;$('fb').value=F.body;$('ft').value=F.type;$('fs').value=F.state;$('fdt').value=F.dtype;
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
[['fm','mech'],['fb','body'],
=======
[['fm','mech'],['fdt','dtype'],['fb','body'],
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
$('clear').addEventListener('click',()=>{F={kw:'',mech:'',body:'',type:'',state:'',yf:'',yt:'',sdg:'',themes:[]};update()});
=======
$('clear').addEventListener('click',()=>{F={kw:'',mech:'',body:'',type:'',dtype:'',state:'',yf:'',yt:'',sdg:'',themes:[]};update()});
>>>>>>> REPLACE
```