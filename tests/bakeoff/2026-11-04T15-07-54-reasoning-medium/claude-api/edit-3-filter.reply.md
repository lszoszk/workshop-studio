I added a "Document type" selector under heading 02 of the filters, so the rail still has three headings. The data has no document-type field, so the app derives it from the mechanism and the symbol: "Concluding observations" are treaty-body symbols containing "/CO/", and the other treaty-body documents are grouped separately. A note under the selector says this, so nobody reads it as a UN label.

```edit
<<<<<<< SEARCH
        <label for="selType">Type</label><select id="selType"></select>
=======
        <label for="selType">Type</label><select id="selType"></select>
        <label for="selDtype">Document type</label><select id="selDtype"></select>
        <p class="hint">derived by this app: mechanism + "/CO/" in the symbol; not a UN label</p>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
const R=(D.records||[]).map((r,i)=>{
=======
function docType(r){
  if(r.mechanism===UPR)return 'UPR report';
  if(r.mechanism==='Treaty bodies')return /\/CO\//i.test(r.symbol||'')?'Concluding observations':'Other treaty-body document';
  if(r.mechanism==='Special Procedures')return 'Special Procedures report';
  return 'Other document';
}
const R=(D.records||[]).map((r,i)=>{
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
para:m?m[1]:null,isU,
=======
para:m?m[1]:null,isU,dtype:docType(r),
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
const TYPES=Array.from(new Set(R.map(r=>r.type))).sort();
=======
const TYPES=Array.from(new Set(R.map(r=>r.type))).sort();
const DTC=new Map();R.forEach(r=>DTC.set(r.dtype,(DTC.get(r.dtype)||0)+1));
const DTYPES=Array.from(DTC.entries()).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
const F0=()=>({kw:'',mech:'',body:'',type:'',state:'',from:YMIN,to:YMAX,sdg:'',themes:[]});
=======
const F0=()=>({kw:'',mech:'',body:'',type:'',dtype:'',state:'',from:YMIN,to:YMAX,sdg:'',themes:[]});
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
(!F.type||r.type===F.type)&&
=======
(!F.type||r.type===F.type)&&(!F.dtype||r.dtype===F.dtype)&&
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  if(F.type)a.push('type: '+F.type);
=======
  if(F.type)a.push('type: '+F.type);
  if(F.dtype)a.push('document type: '+F.dtype);
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  if(F.type)add(F.type,()=>{F.type='';});
=======
  if(F.type)add(F.type,()=>{F.type='';});
  if(F.dtype)add(F.dtype,()=>{F.dtype='';});
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  $('#selType').innerHTML=opt('','All types')+TYPES.map(x=>opt(x,x)).join('');
=======
  $('#selType').innerHTML=opt('','All types')+TYPES.map(x=>opt(x,x)).join('');
  $('#selDtype').innerHTML=opt('','All document types')+DTYPES.map(x=>opt(x[0],x[0]+' ('+fmt(x[1])+')')).join('');
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
$('#selType').value=F.type;
=======
$('#selType').value=F.type;$('#selDtype').value=F.dtype;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
$('#selType').onchange=e=>{F.type=e.target.value;update();};
=======
$('#selType').onchange=e=>{F.type=e.target.value;update();};
$('#selDtype').onchange=e=>{F.dtype=e.target.value;update();};
>>>>>>> REPLACE
```