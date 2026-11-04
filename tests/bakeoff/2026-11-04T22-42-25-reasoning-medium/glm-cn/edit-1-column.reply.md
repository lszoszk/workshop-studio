Three edits: a new "Year" column header (sortable), the year value in each row, and the sort comparator plus caption.

```edit
<<<<<<< SEARCH
  const s=filtered.slice();
  s.sort((a,b)=>{
    const d = (a.date<b.date?-1:a.date>b.date?1:0) * (dateDesc?-1:1);
    if(d)return d;
    if(a.body!==b.body)return a.body<b.body?-1:1;
=======
  const s=filtered.slice();
  s.sort((a,b)=>{
    if(sortCol==='year'){
      if(a.year!==b.year)return (a.year-b.year)*(dateDesc?-1:1);
      if(a.date!==b.date)return (a.date<b.date?-1:1)*(dateDesc?-1:1);
    }else{
    const d = (a.date<b.date?-1:a.date>b.date?1:0) * (dateDesc?-1:1);
    if(d)return d;
    }
    if(a.body!==b.body)return a.body<b.body?-1:1;
>>>>>>> REPLACE
```