I added a Year column right after Date. Both Date and Year headers are now sort buttons: the first click on Year gives latest first, a second click reverses it, and ties within a year follow the usual newest-first order. The caption says which sort is active.

```edit
<<<<<<< SEARCH
<th scope="col">Body</th>
=======
<th scope="col" class="n" id="thyear" aria-sort="none"><button class="lnk" id="sorty" style="font:inherit;text-transform:uppercase;letter-spacing:.07em;font-size:11px;text-decoration:none;color:inherit;padding:0">Year</button></th><th scope="col">Body</th>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
shown:50,desc:true,
=======
shown:50,desc:true,key:'date',
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  const rows=F.slice().sort((a,b)=>S.desc?cmp(a,b):cmp(b,a));
=======
  const rows=F.slice().sort(S.key==='year'?((a,b)=>(S.desc?(b.year-a.year):(a.year-b.year))||cmp(a,b)):((a,b)=>S.desc?cmp(a,b):cmp(b,a)));
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
(S.desc?'newest first':'oldest first')
=======
(S.key==='year'?(S.desc?'latest year first':'earliest year first'):(S.desc?'newest first':'oldest first'))
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  $('sortd').textContent='Date '+(S.desc?'▼':'▲');
  $('thdate').setAttribute('aria-sort',S.desc?'descending':'ascending');
=======
  $('sortd').textContent='Date'+(S.key==='date'?(S.desc?' ▼':' ▲'):'');
  $('sorty').textContent='Year'+(S.key==='year'?(S.desc?' ▼':' ▲'):'');
  $('thdate').setAttribute('aria-sort',S.key==='date'?(S.desc?'descending':'ascending'):'none');
  $('thyear').setAttribute('aria-sort',S.key==='year'?(S.desc?'descending':'ascending'):'none');
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
<td>'+esc(r.date||'')+'</td>
=======
<td>'+esc(r.date||'')+'</td><td class="n">'+esc(r.year==null?'':r.year)+'</td>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
<tr class="exp"><td colspan="6">
=======
<tr class="exp"><td colspan="7">
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
$('sortd').onclick=()=>{S.desc=!S.desc;renderRecs()};
=======
$('sortd').onclick=()=>{if(S.key==='date')S.desc=!S.desc;else{S.key='date';S.desc=true}renderRecs()};
$('sorty').onclick=()=>{if(S.key==='year')S.desc=!S.desc;else{S.key='year';S.desc=true}renderRecs()};
>>>>>>> REPLACE
```