Here are the edits: a new Year column after Date, with its own sortable header (click toggles ascending/descending, like the Date header).

```edit
<<<<<<< SEARCH
      <th scope="col" class="date-cell"><button id="dateSort" style="background:none;border:none;cursor:pointer;font:inherit;padding:0;text-transform:inherit;letter-spacing:inherit">Date ▾</button></th>
      <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th>
=======
      <th scope="col" class="date-cell"><button id="dateSort" style="background:none;border:none;cursor:pointer;font:inherit;padding:0;text-transform:inherit;letter-spacing:inherit">Date ▾</button></th>
      <th scope="col" class="num"><button id="yearSort" style="background:none;border:none;cursor:pointer;font:inherit;padding:0;text-transform:inherit;letter-spacing:inherit">Year ⇅</button></th>
      <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
let sortDesc=true,shown=50,openRow=null;
=======
let sortDesc=true,sortKey="date",shown=50,openRow=null;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
function sortSet(set){
  const s=[...set];
  s.sort((a,b)=>{
    if(a.date!==b.date)return sortDesc?(a.date<b.date?1:-1):(a.date<b.date?-1:1);
    if(a.body!==b.body)return a.body.localeCompare(b.body);
    const pa=a._para!==null?parseFloat(a._para):Infinity,pb=b._para!==null?parseFloat(b._para):Infinity;
    if(pa!==pb)return pa-pb;
    return a._i-b._i;});
  return s;
}
=======
function sortSet(set){
  const s=[...set];
  s.sort((a,b)=>{
    if(sortKey==="year"&&a.year!==b.year)return sortDesc?b.year-a.year:a.year-b.year;
    if(a.date!==b.date)return sortDesc?(a.date<b.date?1:-1):(a.date<b.date?-1:1);
    if(a.body!==b.body)return a.body.localeCompare(b.body);
    const pa=a._para!==null?parseFloat(a._para):Infinity,pb=b._para!==null?parseFloat(b._para):Infinity;
    if(pa!==pb)return pa-pb;
    return a._i-b._i;});
  return s;
}
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  cap.textContent=`Showing ${Math.min(shown,set.length)} of ${fmt(set.length)} matching records · newest first (click “Date” to reverse) · click a row to read the full paragraph · date is the document's date`;
=======
  cap.textContent=`Showing ${Math.min(shown,set.length)} of ${fmt(set.length)} matching records · sorted by ${sortKey==="year"?"year":"date"} (${sortDesc?"descending":"ascending"}; click “Date” or “Year” to change) · click a row to read the full paragraph · date is the document's date`;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    return`<tr class="recrew" tabindex="0" data-id="${esc(r.id)}" aria-expanded="false">
    <td class="date-cell">${esc(r.date||r.year)}</td><td>${esc(r.body)}</td>
=======
    return`<tr class="recrew" tabindex="0" data-id="${esc(r.id)}" aria-expanded="false">
    <td class="date-cell">${esc(r.date||r.year)}</td><td class="num">${esc(r.year)}</td><td>${esc(r.body)}</td>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    `<tr><td colspan="6">No records match the current filter.</td></tr>`;
=======
    `<tr><td colspan="7">No records match the current filter.</td></tr>`;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  dr.innerHTML=`<td colspan="6">
=======
  dr.innerHTML=`<td colspan="7">
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
$("dateSort").addEventListener("click",()=>{sortDesc=!sortDesc;
  $("dateSort").textContent=sortDesc?"Date ▾":"Date ▴";renderTable(filtered());});
=======
$("dateSort").addEventListener("click",()=>{sortKey="date";sortDesc=!sortDesc;
  $("dateSort").textContent=sortDesc?"Date ▾":"Date ▴";
  $("yearSort").textContent="Year ⇅";renderTable(filtered());});
$("yearSort").addEventListener("click",()=>{
  if(sortKey==="year")sortDesc=!sortDesc;else{sortKey="year";sortDesc=true;}
  $("yearSort").textContent=sortDesc?"Year ▾":"Year ▴";
  $("dateSort").textContent="Date ⇅";renderTable(filtered());});
>>>>>>> REPLACE
```