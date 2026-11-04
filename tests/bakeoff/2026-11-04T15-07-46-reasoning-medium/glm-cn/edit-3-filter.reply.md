I added a "Document type" filter (fourth select in the "Mechanism, body, type" heading) that classifies each document by its symbol and mechanism — concluding observations, UPR recommendations, Special Procedures reports, and any other treaty-body documents — and applies it to every record from that document.

```edit
<<<<<<< SEARCH
      <label for="ftype">Type</label><select id="ftype"></select>
      <div id="fstatewrap" hidden><label for="fstate">Recommending State (UPR)</label><select id="fstate"></select></div>
=======
      <label for="ftype">Type</label><select id="ftype"></select>
      <label for="fdockind">Document type</label><select id="fdockind"></select>
      <div id="fstatewrap" hidden><label for="fstate">Recommending State (UPR)</label><select id="fstate"></select></div>
>>>>>>> REPLACE
```````
```edit
<<<<<<< SEARCH
const stateCounts={};
recs.forEach(r=>{if(r.mechanism==='Universal Periodic Review'&&r._states){r._states.forEach(s=>stateCounts[s]=(stateCounts[s]||0)+1);}});
const stateList=Object.keys(stateCounts).sort((a,b)=>stateCounts[b]-stateCounts[a]);
=======
const stateCounts={};
recs.forEach(r=>{if(r.mechanism==='Universal Periodic Review'&&r._states){r._states.forEach(s=>stateCounts[s]=(stateCounts[s]||0)+1);}});
const stateList=Object.keys(stateCounts).sort((a,b)=>stateCounts[b]-stateCounts[a]);
/* document type: one class per distinct symbol, from its mechanism and symbol */
const docKind={};
recs.forEach(r=>{
  if(docKind[r.symbol]!==undefined)return;
  let k;
  if(r.mechanism==='Universal Periodic Review')k='UPR recommendations';
  else if(r.mechanism==='Special Procedures')k='Special Procedures reports';
  else if(/\/CO\//.test(r.symbol))k='Concluding observations';
  else k='Other treaty-body documents';
  docKind[r.symbol]=k;
});
>>>>>>> REPLACE
```````
```edit
<<<<<<< SEARCH
const F={kw:'',mech:'',body:'',type:'',state:'',yfrom:'',yto:'',sdg:'',theme:''};
=======
const F={kw:'',mech:'',body:'',type:'',state:'',dockind:'',yfrom:'',yto:'',sdg:'',theme:''};
>>>>>>> REPLACE
```````
```edit
<<<<<<< SEARCH
    if(F.type&&r.type!==F.type)return false;
    if(F.state&&!(r._states&&r._states.includes(F.state)))return false;
=======
    if(F.type&&r.type!==F.type)return false;
    if(F.dockind&&docKind[r.symbol]!==F.dockind)return false;
    if(F.state&&!(r._states&&r._states.includes(F.state)))return false;
>>>>>>> REPLACE
```````
```edit
<<<<<<< SEARCH
  sel('fstate',[{v:'',t:'all'}].concat(stateList.map(s=>({v:s,t:s+' ('+stateCounts[s]+')'}))),F.state);
  document.getElementById('fstatewrap').hidden = !stateList.length;
}
=======
  sel('fstate',[{v:'',t:'all'}].concat(stateList.map(s=>({v:s,t:s+' ('+stateCounts[s]+')'}))),F.state);
  const dk={};pool.forEach(r=>{const k=docKind[r.symbol];dk[k]=(dk[k]||0)+1;});
  sel('fdockind',[{v:'',t:'all'}].concat(Object.keys(dk).sort().map(k=>({v:k,t:k+' ('+dk[k]+')'}))),F.dockind);
  document.getElementById('fstatewrap').hidden = !stateList.length;
}
>>>>>>> REPLACE
```````
```edit
<<<<<<< SEARCH
  if(F.type)add(F.type,'type');
  if(F.state)add(F.state,'state');
=======
  if(F.type)add(F.type,'type');
  if(F.dockind)add(F.dockind,'dockind');
  if(F.state)add(F.state,'state');
>>>>>>> REPLACE
```````
```edit
<<<<<<< SEARCH
document.getElementById('clearall').onclick=()=>{F.kw='';F.mech='';F.body='';F.type='';F.state='';F.theme='';F.yfrom='';F.yto='';F.sdg='';syncInputs();apply();};
=======
document.getElementById('clearall').onclick=()=>{F.kw='';F.mech='';F.body='';F.type='';F.state='';F.dockind='';F.theme='';F.yfrom='';F.yto='';F.sdg='';syncInputs();apply();};
>>>>>>> REPLACE
```````
```edit
<<<<<<< SEARCH
document.getElementById('fstate').onchange=e=>{F.state=e.target.value;apply();};
=======
document.getElementById('fdockind').onchange=e=>{F.dockind=e.target.value;apply();};
document.getElementById('fstate').onchange=e=>{F.state=e.target.value;apply();};
>>>>>>> REPLACE
```````
```edit
<<<<<<< SEARCH
  lines.push('# Filters applied: '+(F.kw?'keyword="'+F.kw+'" ':'')+(F.mech?'mechanism='+F.mech+' ':'')+(F.body?'body='+F.body+' ':'')+(F.type?'type='+F.type+' ':'')+(F.state?'state='+F.state+' ':'')+(F.theme?'theme='+F.theme+' ':'')+((F.yfrom!==''||F.yto!=='')?'years='+ (F.yfrom||years[0])+'-'+(F.yto||years[years.length-1])+' ':'')+(F.sdg!==''?'sdg='+F.sdg+' ':'')+'(none)' .replace(' (none)',''));
=======
  lines.push('# Filters applied: '+(F.kw?'keyword="'+F.kw+'" ':'')+(F.mech?'mechanism='+F.mech+' ':'')+(F.body?'body='+F.body+' ':'')+(F.type?'type='+F.type+' ':'')+(F.dockind?'document type='+F.dockind+' ':'')+(F.state?'state='+F.state+' ':'')+(F.theme?'theme='+F.theme+' ':'')+((F.yfrom!==''||F.yto!=='')?'years='+ (F.yfrom||years[0])+'-'+(F.yto||years[years.length-1])+' ':'')+(F.sdg!==''?'sdg='+F.sdg+' ':'')+'(none)' .replace(' (none)',''));
>>>>>>> REPLACE
```````
```edit
<<<<<<< SEARCH
  '<p><strong>Filters</strong> combine with AND. Mechanism, body, type, State and theme are exact matches on the field. Year is inclusive between the two selects; a reversed range is swapped. SDG matches records listing that goal. The keyword is lower-cased and every word must occur as a substring of the text or symbol \u2014 literal, not synonyms.</p>',
=======
  '<p><strong>Filters</strong> combine with AND. Mechanism, body, type, State and theme are exact matches on the field. <strong>Document type</strong> classifies each distinct symbol once: UPR documents are \u201cUPR recommendations\u201d, Special Procedures are \u201cSpecial Procedures reports\u201d, treaty-body symbols containing \u201c/CO/\u201d are \u201cConcluding observations\u201d, and other treaty-body symbols are \u201cOther treaty-body documents\u201d; the class applies to every record from that document. Year is inclusive between the two selects; a reversed range is swapped. SDG matches records listing that goal. The keyword is lower-cased and every word must occur as a substring of the text or symbol \u2014 literal, not synonyms.</p>',
>>>>>>> REPLACE
``````