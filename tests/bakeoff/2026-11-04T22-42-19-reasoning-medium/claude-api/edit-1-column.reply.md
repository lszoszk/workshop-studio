I added a Year column right after Date. Clicking either the Date or Year header sorts the table by it, and clicking the same header again reverses the order.

```edit
<<<<<<< SEARCH
<thead><tr><th scope="col"><button id="sortDate" title="Reverse the date order">Date ▼</button></th><th scope="col">Body</th>
=======
<thead><tr><th scope="col"><button id="sortDate" title="Sort by date; click again to reverse">Date ▼</button></th><th scope="col" class="r"><button id="sortYear" title="Sort by year; click again to reverse">Year</button></th><th scope="col">Body</th>
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
function renderRecords(){
  const sorted=F.slice().sort((a,b)=>{
    const x=a.date||'',y=b.date||'';const d=x<y?-1:x>y?1:0;
=======
let sortKey='date';
function renderRecords(){
  const sorted=F.slice().sort((a,b)=>{
    const yd=sortKey==='year'?(a.year-b.year):0;
    if(yd)return S.asc?yd:-yd;
    const x=a.date||'',y=b.date||'';const d=x<y?-1:x>y?1:0;
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
  $('sortDate').textContent='Date '+(S.asc?'▲':'▼');
=======
  $('sortDate').textContent='Date'+(sortKey==='date'?(S.asc?' ▲':' ▼'):'');
  $('sortYear').textContent='Year'+(sortKey==='year'?(S.asc?' ▲':' ▼'):'');
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
<td>'+esc(r.date||'')+'</td><td>'+esc(r.body)+'</td>
=======
<td>'+esc(r.date||'')+'</td><td class="r">'+(isNaN(r.year)?'–':esc(r.year))+'</td><td>'+esc(r.body)+'</td>
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
<tr class="det"><td colspan="6">
=======
<tr class="det"><td colspan="7">
>>>>>>> REPLACE
```
```edit
<<<<<<< SEARCH
$('sortDate').onclick=()=>{S.asc=!S.asc;renderRecords()};
=======
function setSort(k){if(sortKey===k)S.asc=!S.asc;else{sortKey=k;S.asc=false}renderRecords()}
$('sortDate').onclick=()=>setSort('date');
$('sortYear').onclick=()=>setSort('year');
>>>>>>> REPLACE
```