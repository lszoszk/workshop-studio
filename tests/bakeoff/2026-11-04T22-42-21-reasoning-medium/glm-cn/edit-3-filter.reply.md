Good idea — one honest note first: the file has no document-type field, so the app derives it (a “/CO/” in the symbol means concluding observations; the UPR mechanism means UPR recommendations; the rest are Special Procedures reports or other documents). The filter states this on screen. Here are the edits:

```edit
<<<<<<< SEARCH
 recs.forEach((r,i)=>{r._i=i;r._para=paraNum(r.text);
   r._states=r.mechanism==="Universal Periodic Review"?extractStates(r.text):null;});
=======
 function docType(r){
   if(r.mechanism==="Universal Periodic Review")return"UPR recommendations";
   if(/\/CO\//.test(r.symbol||""))return"Concluding observations";
   if(r.mechanism==="Special Procedures")return"Special Procedures report";
   return"Other document";
 }
 recs.forEach((r,i)=>{r._i=i;r._para=paraNum(r.text);
   r._states=r.mechanism==="Universal Periodic Review"?extractStates(r.text):null;
   r._doctype=docType(r);});
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
 const F={keyword:"",mechanism:"",body:"",type:"",state:"",yearFrom:"",yearTo:"",sdg:"",themes:[]};
=======
 const F={keyword:"",mechanism:"",body:"",type:"",state:"",doctype:"",yearFrom:"",yearTo:"",sdg:"",themes:[]};
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
     if(F.type&&r.type!==F.type)return false;
     if(F.state&&!(r._states&&r._states.includes(F.state)))return false;
=======
     if(F.type&&r.type!==F.type)return false;
     if(F.doctype&&r._doctype!==F.doctype)return false;
     if(F.state&&!(r._states&&r._states.includes(F.state)))return false;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
 function onePanel(id){
  [["fh1","fp1"],["fh2","fp2"],["fh3","fp3"]].forEach(([h,p])=>{
=======
 function onePanel(id){
  [["fh1","fp1"],["fh2","fp2"],["fh3","fp3"],["fh4","fp4"]].forEach(([h,p])=>{
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
 ["fh1","fh2","fh3"].forEach(h=>$(h).addEventListener("click",()=>{
=======
 ["fh1","fh2","fh3","fh4"].forEach(h=>$(h).addEventListener("click",()=>{
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
     <button class="fhead" id="fh3" aria-expanded="false" aria-controls="fp3"><span>03 Years and SDG</span><span aria-hidden="true">+</span></button>
     <div class="fpanel" id="fp3" hidden>
=======
     <button class="fhead" id="fh4" aria-expanded="false" aria-controls="fp4"><span>04 Document type</span><span aria-hidden="true">+</span></button>
    <div class="fpanel" id="fp4" hidden>
      <label for="selDoc">Document type</label><select id="selDoc"></select>
      <div class="hint">Derived in this page: “/CO/” in the symbol = concluding observations; UPR mechanism = UPR recommendations; otherwise Special Procedures report or other document. The file itself has no document-type field.</div>
    </div>
    <button class="fhead" id="fh3" aria-expanded="false" aria-controls="fp3"><span>03 Years and SDG</span><span aria-hidden="true">+</span></button>
    <div class="fpanel" id="fp3" hidden>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
   fillSel($("selSdg"),[{v:"",l:"all"}].concat(presentSdgs.map(g=>({v:g,l:`${g}. ${sdgNames[String(g)]||""}`}))),F.sdg);
=======
   fillSel($("selSdg"),[{v:"",l:"all"}].concat(presentSdgs.map(g=>({v:g,l:`${g}. ${sdgNames[String(g)]||""}`}))),F.sdg);
  const dts={};recs.forEach(r=>dts[r._doctype]=(dts[r._doctype]||0)+1);
  fillSel($("selDoc"),[{v:"",l:"all"}].concat(Object.keys(dts).sort().map(d=>({v:d,l:`${d} (${dts[d]})`}))),F.doctype);
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
 ["selBody","selType","selState","selSdg"].forEach(id=>$(id).addEventListener("change",e=>{
  F[{selBody:"body",selType:"type",selState:"state",selSdg:"sdg"}[id]]=e.target.value;refresh();}));
=======
 ["selBody","selType","selState","selDoc","selSdg"].forEach(id=>$(id).addEventListener("change",e=>{
  F[{selBody:"body",selType:"type",selState:"state",selDoc:"doctype",selSdg:"sdg"}[id]]=e.target.value;refresh();}));
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
   Object.assign(F,{keyword:"",mechanism:"",body:"",type:"",state:"",yearFrom:"",yearTo:"",sdg:"",themes:[]});
=======
   Object.assign(F,{keyword:"",mechanism:"",body:"",type:"",state:"",doctype:"",yearFrom:"",yearTo:"",sdg:"",themes:[]});
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
   if(F.state)h+=chip(F.state,"state");
   if(F.yearFrom||F.yearTo)h+=chip(`${F.yearFrom||"…"}–${F.yearTo||"…"}`,"years");
=======
   if(F.state)h+=chip(F.state,"state");
   if(F.doctype)h+=chip(F.doctype+" (derived)","doctype");
   if(F.yearFrom||F.yearTo)h+=chip(`${F.yearFrom||"…"}–${F.yearTo||"…"}`,"years");
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  if(F.state)p.push(`State: ${F.state}`);
   if(F.yearFrom||F.yearTo)p.push(`years: ${F.yearFrom||"…"}–${F.yearTo||"…"}`);
=======
  if(F.state)p.push(`State: ${F.state}`);
  if(F.doctype)p.push(`document type (derived): ${F.doctype}`);
   if(F.yearFrom||F.yearTo)p.push(`years: ${F.yearFrom||"…"}–${F.yearTo||"…"}`);
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
 buildSelects();onePanel("fh2");showTab(1);
=======
 buildSelects();onePanel("fh2");showTab(1);
>>>>>>> REPLACE
```