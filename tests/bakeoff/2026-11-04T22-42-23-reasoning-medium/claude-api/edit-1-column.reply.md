I added a Year column right after Date. Both the Date and Year headers now sort the table: the first click on a header sorts by it, newest first, and clicking again reverses the order. The table caption states which sort is active. Records with the same year are ordered by date, then body, then paragraph number.

```edit
<<<<<<< SEARCH
function sorted(){
  const d=dirDesc?-1:1;
  return filtered.slice().sort((a,b)=>d*String(a.date||'').localeCompare(String(b.date||''))||String(a.body).localeCompare(String(b.body))||pcmp(a.para,b.para)||a._i-b._i);
=======
let sortKey='date';
function sorted(){
  const d=dirDesc?-1:1;
  return filtered.slice().sort((a,b)=>(sortKey==='year'?d*((a.year||0)-(b.year||0)):0)||d*String(a.date||'').localeCompare(String(b.date||''))||String(a.body).localeCompare(String(b.body))||pcmp(a.para,b.para)||a._i-b._i);
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
<th scope="col"><button id="dsort" aria-label="Reverse date order">Date '+(dirDesc?'↓':'↑')+'</button></th><th scope="col">Body</th>
=======
<th scope="col"><button id="dsort" aria-label="Sort by date, click again to reverse">Date'+(sortKey==='date'?(dirDesc?' ↓':' ↑'):'')+'</button></th><th scope="col" class="n"><button id="ysort" aria-label="Sort by year, click again to reverse">Year'+(sortKey==='year'?(dirDesc?' ↓':' ↑'):'')+'</button></th><th scope="col">Body</th>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
<td>'+esc(r.date)+'</td><td>'+esc(r.body)+'</td>
=======
<td>'+esc(r.date)+'</td><td class="n">'+(r.year!=null?esc(r.year):'—')+'</td><td>'+esc(r.body)+'</td>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
'+(dirDesc?'newest first':'oldest first')+'</caption>
=======
'+(sortKey==='year'?'by year, ':'by date, ')+(dirDesc?'newest first':'oldest first')+'</caption>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  if(e.target.id==='dsort'){dirDesc=!dirDesc;render2();return}
=======
  if(e.target.id==='dsort'){if(sortKey==='date')dirDesc=!dirDesc;else{sortKey='date';dirDesc=true}render2();return}
  if(e.target.id==='ysort'){if(sortKey==='year')dirDesc=!dirDesc;else{sortKey='year';dirDesc=true}render2();return}
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
<tr class="ex"><td colspan="6">
=======
<tr class="ex"><td colspan="7">
>>>>>>> REPLACE
```