I added a Year column right after Date. Click either the Date or the Year header to sort by it; clicking the active header again reverses the order. Sorting by year breaks ties by date, then body, then paragraph number.

```edit
<<<<<<< SEARCH
let F=F0(),FS=[],S={tab:1,openF:0,shown:50,dir:-1,open:null,states:false};
=======
let F=F0(),FS=[],S={tab:1,openF:0,shown:50,dir:-1,key:'date',open:null,states:false};
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  return rs.slice().sort((a,b)=>{
    if(a.date!==b.date)return (a.date<b.date?-1:1)*d;
=======
  return rs.slice().sort((a,b)=>{
    if(S.key==='year'){const ya=isFinite(a.year)?a.year:-1,yb=isFinite(b.year)?b.year:-1;if(ya!==yb)return (ya-yb)*d;}
    if(a.date!==b.date)return (a.date<b.date?-1:1)*d;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
matching records shown, '+(S.dir<0?'newest':'oldest')+' first':
=======
matching records shown, sorted by '+S.key+', '+(S.dir<0?'newest':'oldest')+' first':
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    '<th scope="col" aria-sort="'+(S.dir<0?'descending':'ascending')+'"><button type="button" id="dateSort" title="Reverse the order">Date '+(S.dir<0?'▼':'▲')+'</button></th><th scope="col">Body</th>
=======
    '<th scope="col"'+(S.key==='date'?' aria-sort="'+(S.dir<0?'descending':'ascending')+'"':'')+'><button type="button" id="dateSort" title="Sort by date">Date '+(S.key==='date'?(S.dir<0?'▼':'▲'):'')+'</button></th><th scope="col" class="r"'+(S.key==='year'?' aria-sort="'+(S.dir<0?'descending':'ascending')+'"':'')+'><button type="button" id="yearSort" title="Sort by year">Year '+(S.key==='year'?(S.dir<0?'▼':'▲'):'')+'</button></th><th scope="col">Body</th>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
<td>'+esc(r.date)+'</td><td>'+esc(r.body)+'</td>
=======
<td>'+esc(r.date)+'</td><td class="r">'+(isFinite(r.year)?r.year:'–')+'</td><td>'+esc(r.body)+'</td>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
colspan="'+(showState?6:5)+'"
=======
colspan="'+(showState?7:6)+'"
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  $('#dateSort').onclick=()=>{S.dir*=-1;renderRecords();};
=======
  $('#dateSort').onclick=()=>{if(S.key==='date')S.dir*=-1;else{S.key='date';S.dir=-1;}renderRecords();};
  $('#yearSort').onclick=()=>{if(S.key==='year')S.dir*=-1;else{S.key='year';S.dir=-1;}renderRecords();};
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  if(e.target.closest('a')||e.target.closest('#dateSort'))return;
=======
  if(e.target.closest('a')||e.target.closest('#dateSort')||e.target.closest('#yearSort'))return;
>>>>>>> REPLACE
```