Two small edits: a new Year column with its own sortable header, and the sort logic.

```edit
<<<<<<< SEARCH
        <th scope="col"><button class="act" id="sortbtn" style="padding:0;border:none;font:inherit;text-transform:uppercase;letter-spacing:.05em;font-size:12px;font-family:ui-monospace,Menlo,Consolas,monospace">Date ${S.sortDesc?"▾":"▴"}</button></th>
        <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col">Para.</th>
=======
        <th scope="col"><button class="act" data-sort="date" style="padding:0;border:none;font:inherit;text-transform:uppercase;letter-spacing:.05em;font-size:12px;font-family:ui-monospace,Menlo,Consolas,monospace">Date ${S.sortBy==="date"?(S.sortDesc?"▾":"▴"):""}</button></th>
        <th scope="col"><button class="act" data-sort="year" style="padding:0;border:none;font:inherit;text-transform:uppercase;letter-spacing:.05em;font-size:12px;font-family:ui-monospace,Menlo,Consolas,monospace">Year ${S.sortBy==="year"?(S.sortDesc?"▾":"▴"):""}</button></th>
        <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col">Para.</th>
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
function sortSet(set){
  const a=[...set];
  a.sort((x,y)=>{
    const d=S.sortDesc?new Date(y.r.date)-new Date(x.r.date):new Date(x.r.date)-new Date(y.r.date);
    if(d)return d;
=======
function sortSet(set){
  const a=[...set];
  a.sort((x,y)=>{
    let d;
    if(S.sortBy==="year") d=S.sortDesc?(y.r.year-x.r.year):(x.r.year-y.r.year);
    else d=S.sortDesc?new Date(y.r.date)-new Date(x.r.date):new Date(x.r.date)-new Date(y.r.date);
    if(d)return d;
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
  document.getElementById("tcap").textContent=`Showing ${fmt(shown.length)} of ${fmt(set.length)} matching records, newest first (click the Date header to reverse). Source: UN records, current filter.`;
=======
  document.getElementById("tcap").textContent=`Showing ${fmt(shown.length)} of ${fmt(set.length)} matching records, ${S.sortBy==="year"?("by year, "+(S.sortDesc?"latest first":"earliest first")):("newest first, by document date")}. Click the Date or Year header to change. Source: UN records, current filter.`;
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
  const sb=document.getElementById("sortbtn");
  if(sb)sb.addEventListener("click",()=>{S.sortDesc=!S.sortDesc;renderTable();});
=======
  el.querySelectorAll("button[data-sort]").forEach(b=>{
    b.addEventListener("click",()=>{
      const k=b.dataset.sort;
      if(S.sortBy===k)S.sortDesc=!S.sortDesc;
      else {S.sortBy=k;S.sortDesc=true;}
      renderTable();
    });
  });
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
    tr.innerHTML=`<td style="white-space:nowrap">${esc(r.date)}</td><td>${esc(r.body)}</td>
      <td class="doclink"><a href="${esc(r.doc_url)}" target="_blank" rel="noopener" onclick="event.stopPropagation()">${esc(r.symbol)}</a></td>
      <td>${p?esc(p):"—"}</td><td class="firstline">${hl(firstLine(r.text||""))}</td><td>${stTxt}</td>`;
=======
    tr.innerHTML=`<td style="white-space:nowrap">${esc(r.date)}</td><td class="num">${esc(r.year)}</td><td>${esc(r.body)}</td>
      <td class="doclink"><a href="${esc(r.doc_url)}" target="_blank" rel="noopener" onclick="event.stopPropagation()">${esc(r.symbol)}</a></td>
      <td>${p?esc(p):"—"}</td><td class="firstline">${hl(firstLine(r.text||""))}</td><td>${stTxt}</td>`;
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
  ex.innerHTML=`<td colspan="6">
=======
  ex.innerHTML=`<td colspan="7">
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
const S = {kw:"", mech:"all", body:"all", type:"all", st:"all", yFrom:YEARS[0], yTo:YEARS[YEARS.length-1], sdg:"all", themes:[], sortDesc:true, page:1, tab:0, seed:1, sample:null, tally:null};
=======
const S = {kw:"", mech:"all", body:"all", type:"all", st:"all", yFrom:YEARS[0], yTo:YEARS[YEARS.length-1], sdg:"all", themes:[], sortDesc:true, sortBy:"date", page:1, tab:0, seed:1, sample:null, tally:null};
>>>>>>> REPLACE
```

The Year column sits next to Date (right-aligned, like other numbers), and clicking its header sorts by year — first click descending, second click ascending; the Date header still works as before, and the table caption always says how rows are currently ordered.