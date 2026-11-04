I added FIG.03 to the Overview, below FIG.02. It shows records per year as stacked bars split by `type`, so recommendations and concerns/observations are told apart. Every year from the first to the last appears, so empty years show as gaps, and it follows the current filters.

```edit
<<<<<<< SEARCH
      <p class="note" id="src2"></p>
=======
      <p class="note" id="src2"></p>
      <h2 id="f3t"></h2>
      <div class="cwrap s"><canvas id="c3" role="img" aria-label="Stacked bars of records per year by type, recommendations and observations"></canvas></div>
      <p class="note">How this is computed: records per year (of the document date) and per type, spelled as in the data, in the filtered set. Recommendations and concerns/observations are the two main types; any other type is shown as its own colour.</p>
      <p class="note" id="src4"></p>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
let TOP=[],ch1=null,ch2=null;
=======
let TOP=[],ch1=null,ch2=null,ch3=null;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  if(ch1){ch1.destroy();ch1=null;}if(ch2){ch2.destroy();ch2=null;}
=======
  if(ch1){ch1.destroy();ch1=null;}if(ch2){ch2.destroy();ch2=null;}if(ch3){ch3.destroy();ch3=null;}
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      scales:{x:{stacked:true,grid:{display:false},ticks:{autoSkip:true,maxRotation:0}},y:{stacked:true,beginAtZero:true,ticks:{precision:0}}}}});
=======
      scales:{x:{stacked:true,grid:{display:false},ticks:{autoSkip:true,maxRotation:0}},y:{stacked:true,beginAtZero:true,ticks:{precision:0}}}}});
  const tcnt={};FS.forEach(r=>{const k=r.year+'|'+r.type;tcnt[k]=(tcnt[k]||0)+1;});
  const tcol=t=>t==='Recommendations'?'#9b2335':t==='Concerns/Observations'?'#5a554c':'#bdb5a3';
  ch3=new Chart($('#c3'),{type:'bar',data:{labels,datasets:TYPES.filter(t=>FS.some(r=>r.type===t)).map(t=>({label:t||'(no type)',backgroundColor:tcol(t),data:labels.map(y=>tcnt[y+'|'+t]||0)}))},
    options:{responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{position:'bottom'}},
      scales:{x:{stacked:true,grid:{display:false},ticks:{autoSkip:true,maxRotation:0}},y:{stacked:true,beginAtZero:true,ticks:{precision:0}}}}});
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  $('#src1').textContent=src;$('#src2').textContent=src;$('#src3').textContent=src;
=======
  $('#src1').textContent=src;$('#src2').textContent=src;$('#src3').textContent=src;$('#src4').textContent=src;
  $('#f3t').textContent='FIG.03 Recommendations and observations per year, '+fmt(n)+' filtered records';
>>>>>>> REPLACE
```